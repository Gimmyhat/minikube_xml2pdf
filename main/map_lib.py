import pyproj
import shapefile
import math
import io
import os
import requests
from PIL import Image, ImageFont
import lib
from lib import dict_

def geom_from_xml(xml, apply_xg_90=True):

    types_cfg = {'1': 'POINT', '2': 'LINE', '3': 'POLYGON', '4': 'POINT'}

    xml_parts = lib.get_xml_attr(xml, 'g:parts/g_part')
    if xml_parts is None:
        return None
    if not isinstance(xml_parts, list):
        xml_parts = [xml_parts]
    parts = []
    for xml_part in xml_parts:
        coords = []
        for coord in xml_part.g_coord:
            lon = float(coord.g_lon.cdata)
            if apply_xg_90:
                lon = xg_90(lon)
            coords.append([lon, float(coord.g_lat.cdata)])
        parts.append(coords)

    geom = dict_(
        type = types_cfg[xml.g_idGeomType.cdata],
        coords = parts
    )

    return geom

def dms(coord):

    degrees = int(coord)
    fminutes = (coord-degrees)*60
    minutes = int(fminutes)
    seconds = round((fminutes-minutes)*60)

    return '{}\u00B0{:02d}\'{:02d}\"'.format(degrees, minutes, seconds)

def bounds(geoms):

    x0, x1, y0, y1 = 9e99, -9e99, 9e99, -9e99
    for geom in geoms:
        for part in geom.coords:
            for coord in part:
                x, y = coord

                x0, x1 = min(x0, x), max(x1, x)
                y0, y1 = min(y0, y), max(y1, y)

    return dict_(x0=x0, x1=x1, y0=y0, y1=y1)

def intersects(b0, b1):

    return b0.x0 < b1.x1 and b0.x1 > b1.x0 and b0.y0 < b1.y1 and b0.y1 > b1.y0

def get_tile(url, layer, z, x, y):

    url = url.format(z=z, x=x, y=y)
    cache_file = lib.cfg('service').data_dir + 'cache/%s/%s/%s/%s' % (layer, z, x, y)
    if not os.path.exists(cache_file):
        print('Download ' + url)
        for itry in range(10):
            try:
                data = requests.get(url, verify=False).content
            except:
                continue
            try:
                img = Image.open(io.BytesIO(data))
                break
            except:
                continue
        else:
            raise Exception('Bad request or bad image')
        dir = os.path.dirname(cache_file)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(cache_file, 'wb') as f:
            f.write(data)
    else:
        with open(cache_file, 'rb') as f:
            data = f.read()
        try:
            img = Image.open(io.BytesIO(data))
        except:
            os.unlink(cache_file)
            raise Exception('Bad Cache')

    return img

def img_coords(coords, meta):

    coords = [((xm-meta.x0)/meta.scale, (meta.y1-ym)/meta.scale) for xm, ym in coords]

    return coords

def extend_bounds(b, procent):

    szx, szy = b.x1 - b.x0, b.y1 - b.y0
    dx, dy = szx * procent/100, szy * procent/100
    
    return dict_(
        x0 = b.x0 - dx, 
        x1 = b.x1 + dx,    
        y0 = b.y0 - dy, 
        y1 = b.y1 + dy
    )

def xg_90(xg):

    return max(xg-90, -180) if xg > -90 else min((xg+360)-90, 180)
    
class Map:

    def __init__(self):

        self.cfg = lib.cfg('map')
        self.service_cfg = lib.cfg('service')
        self.proj_4326_to_3857 = pyproj.Transformer.from_crs(4326, 3857, always_xy=True)
        self.proj_3857_to_4326 = pyproj.Transformer.from_crs(3857, 4326, always_xy=True)
        self.shps = {}
        for name, shp_cfg in self.cfg.shps.items():
            shp = shapefile.Reader(self.service_cfg.data_dir + shp_cfg.file, encoding='cp1251')
            features = []
            for item in shp.shapeRecords():
                xg0, yg0, xg1, yg1 = item.shape.bbox
                xg0, xg1 = xg_90(xg0), xg_90(xg1)
                xm0, ym0 = self.proj_4326_to_3857.transform(xg0, yg0)
                xm1, ym1 = self.proj_4326_to_3857.transform(xg1, yg1)
                parts = []
                iparts = list(item.shape.parts) + [len(item.shape.points)]
                for i in range(len(item.shape.parts)):
                    points = item.shape.points[iparts[i]:iparts[i+1]]
                    xg = [xg_90(xg) for xg, yg in points]
                    yg = [yg for xg, yg in points]
                    xm, ym = self.proj_4326_to_3857.transform(xg, yg)
                    parts.append(list(zip(xm, ym)))

                feature = dict_(
                    bounds = dict_(x0=xm0, y0=ym0, x1=xm1, y1=ym1),
                    coords = parts,
                    attr = item.record[shp_cfg.attr_index])
                if name == 'nom':
                    feature.x = item.record[shp_cfg.x_index]
                    feature.y = item.record[shp_cfg.y_index]
                features.append(feature)
            self.shps[name] = features

    def proj_to_3857(self, geoms):

        for geom in geoms:
            parts = []
            for part in geom.coords:
                coords = []
                for coord in part:

                    xg, yg = coord
                    xm, ym = self.proj_4326_to_3857.transform(xg, yg)
                    coords.append([xm, ym])
                parts.append(coords)
            geom.coords = parts

    def roseestr(self, b, img_size):

        xm0, xm1, ym0, ym1 = b.x0, b.x1, b.y0, b.y1
        dm = max(xm1-xm0, ym1-ym0)
        d_earth = 2 * math.pi * 6378137
        for z in range(self.cfg.z_max+1):
            n_tiles = 2**z
            scale = d_earth/n_tiles/256
            if scale * img_size < dm:
                break
        sz_tile = d_earth/n_tiles
        sh = n_tiles//2
        xt0, xt1 = int(xm0/sz_tile)+sh-1, int(xm1/sz_tile)+sh
        yt0, yt1 = int(ym0/sz_tile)+sh-1, int(ym1/sz_tile)+sh
        yt0, yt1 = n_tiles-1-yt1, n_tiles-1-yt0
        ntx, nty = xt1-xt0+1, yt1-yt0+1

        img = Image.new('RGB', (ntx*256, nty*256), (255, 255, 255, 0))
        for x in range(xt0, xt1+1):
            for y in range(yt0, yt1+1):
                background = get_tile(self.cfg.rosreestr.tile, 'tile', z,
                                      (x+sh//2) % n_tiles, y)
                foreground = get_tile(self.cfg.rosreestr.anno, 'anno', z,
                                      (x+sh//2) % n_tiles, y).convert("RGBA")
                background.paste(foreground, (0, 0), foreground)
                img.paste(background, ((x-xt0)*256, (y-yt0)*256))

        ximg0, yimg1 = (xt0-sh)*sz_tile, (n_tiles-yt0-sh)*sz_tile
        x0, y0 = int((xm0-ximg0)/scale), int((yimg1-ym1)/scale)
        x1, y1 = int((xm1-ximg0)/scale), int((yimg1-ym0)/scale)
        img = img.crop((x0, y0, x1, y1))

        meta = dict_(
            szx = img.width,
            szy = img.height,
            x0 = ximg0 + x0*scale,
            y1 = yimg1 - y0*scale,
            scale = scale
        )
        meta.x1 = meta.x0 + meta.szx * scale
        meta.y0 = meta.y1 - meta.szy * scale

        return img, meta

    def draw_polygon(self, draw, parts, meta, cfg, fill_color=None):
        for ipart, part in enumerate(parts):
            coords = img_coords(part, meta)
            if fill_color:
                if ipart == 0:
                    if len(fill_color) == 3:
                        fill_color.append(200)  # add transparency
                    draw.polygon(coords, fill=tuple(fill_color), outline=tuple(cfg.color))
                else:
                    draw.polygon(coords, fill=(0, 0, 0, 0), outline="black")
            else:
                draw.line(coords, fill=tuple(cfg.color), width=cfg.width)

    def draw_line(self, draw, parts, meta, cfg):

        for part in parts:
            coords = img_coords(part, meta)
            draw.line(coords, fill=tuple(cfg.color), width=cfg.width)

    def draw_points(self, draw, parts, meta, cfg):

        sz = cfg.point_size
        for part in parts:
            coords = img_coords(part, meta)
            for x, y in coords:
                draw.ellipse([(x-sz, y-sz), (x+sz, y+sz)], fill=tuple(cfg.color))

    def draw_text(self, draw, b, meta, label, cfg):

        def pos(x0, x1, mode):
            if mode=='C':
                return (x0+x1) / 2
            elif mode=='0':
                return x0
            elif mode=='1':
                return x1

        (x0, y0), (x1, y1) = img_coords([(b.x0, b.y0), (b.x1, b.y1)], meta)
        font = ImageFont.truetype(font=self.service_cfg.data_dir + cfg.font, size=cfg.size)
        xorg = pos(x0, x1, cfg.pos[0]) + cfg.get('dx', 0)
        yorg = pos(y0, y1, cfg.pos[1]) + cfg.get('dy', 0)
        draw.text((xorg, yorg), label, fill=tuple(cfg.color), font=font,
                  anchor=cfg.get('anchor', 'mm'))


