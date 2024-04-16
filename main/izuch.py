import pdfkit
from PyPDF2 import PdfMerger, PdfReader
import base64, io, traceback
from PIL import Image, ImageDraw, ImageFont
import lib
from lib import dict_
import map_lib
import cherrypy
from pprint import pprint
import collections
import re
import json


def get_scale_colors(idScales, csv_handler, cfg):
    res_color = None
    for idScale in idScales:
        scale = csv_handler.data['d_scale'][idScale.cdata]['scale']
        if ':' in scale:
            scale = int(scale.split(':')[1].replace(' ', ''))
            for color_scale, color in cfg.object.scale_colors.items():
                if scale <= color_scale:
                    res_color = color
                    break

    return res_color


def draw_maps(xml, map, csv_handler):
    cfg = lib.cfg('izuch/map')
    service_cfg = lib.cfg('service')

    maps = {}
    for section in ['23.1', '23.2', '23.3', '23.4', '23.5', '23.6']:

        efgi_geom = False
        obj_geoms, obj_colors = [], []
        for explorationData in lib.get_xml_value(xml, 'supply/explorationData', list):
            idMethodIndexes = lib.get_xml_value(explorationData, 'e_idMethodIndex', list)
            vids = set()
            for ind in idMethodIndexes:
                vids.add(csv_handler.data['d_method_index'][ind.cdata]['vid'])
            idScale = lib.get_xml_value(explorationData, 'e:idScale', list)
            color = get_scale_colors(idScale, csv_handler, cfg)
            if section[-1] in vids:
                spatialObjects = lib.get_xml_value(explorationData,
                                                   'e_spatialObjects/g_spatialObject', list)
                for spatialObject in spatialObjects:
                    geom_ = lib.get_xml_value(spatialObject, 'geom', str)
                    if geom_:
                        efgi_geom = True
                        geom_ = geom_.replace('coordinates', 'coords')
                        geom = json.loads(geom_)
                        geom = dict_(json.loads(geom))
                        if geom.type == 'MultiPoint':
                            geom = None
                    else:
                        geom = map_lib.geom_from_xml(spatialObject)
                    if geom:
                        obj_geoms.append(geom)
                        obj_colors.append(color)
        if not obj_geoms:
            continue

        if not efgi_geom:
            map.proj_to_3857(obj_geoms)
        obj_b = map_lib.bounds(obj_geoms)
        nom_y0, nom_y1, nom_x0, nom_x1, = 999, -999, 999, -999
        map_b = dict_(x0=9e99, x1=-9e99, y0=9e99, y1=-9e99)
        inom_by_x_y, n_noms = {}, 0
        for inom, nom in enumerate(map.shps['nom']):
            nom_y, nom_x = nom.x, nom.y
            inom_by_x_y[(nom_x, nom_y)] = inom
            if map_lib.intersects(obj_b, nom.bounds):
                n_noms += 1
                nom_y0, nom_x0 = min(nom_y0, nom_y), min(nom_x0, nom_x)
                nom_y1, nom_x1 = max(nom_y1, nom_y), max(nom_x1, nom_x)
                map_b.x0, map_b.x1 = min(map_b.x0, nom.bounds.x0), max(map_b.x1, nom.bounds.x1)
                map_b.y0, map_b.y1 = min(map_b.y0, nom.bounds.y0), max(map_b.y1, nom.bounds.y1)
        if n_noms == 0:
            raise Exception('No noms')
        n_noms = (nom_x1 - nom_x0 + 1) * (nom_y1 - nom_y0 + 1)

        img, meta = map.roseestr(map_b, cfg.img_size)

        draw = ImageDraw.Draw(img, 'RGBA')

        text_img = Image.new('RGBA', (meta.szx, meta.szy), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img, 'RGBA')
        for nom_x in range(nom_x0, nom_x1 + 1):
            for nom_y in range(nom_y0, nom_y1 + 1):
                if (nom_x, nom_y) not in inom_by_x_y:
                    continue
                nom = map.shps['nom'][inom_by_x_y[(nom_x, nom_y)]]
                # рамка вокруг номенклатурного листа
                map.draw_polygon(draw, nom.coords, meta, cfg.nom)
                # подпись номенклатурного листа, например: "Q-44"
                map.draw_text(text_draw, nom.bounds, meta, nom.attr, cfg.nom.label)

        for reg in map.shps['regions']:
            if not map_lib.intersects(reg.bounds, meta):
                continue
            map.draw_polygon(draw, reg.coords, meta, cfg.regions)

        if n_noms <= 4:
            for nom in map.shps['nom_100']:
                if not map_lib.intersects(nom.bounds, meta):
                    continue
                map.draw_polygon(draw, nom.coords, meta, cfg.nom)


        for geom, color in zip(obj_geoms, obj_colors):

            poly_img = Image.new('RGBA', (meta.szx, meta.szy), (255, 255, 255, 0))
            poly_draw = ImageDraw.Draw(poly_img, 'RGBA')

            if geom.type:
                geom.type = geom.type.upper()
            if geom.type == 'POLYGON':
                map.draw_polygon(poly_draw, geom.coords, meta, cfg.object, fill_color=color)
            if geom.type == 'LINE':
                map.draw_line(draw, geom.coords, meta, cfg.object)
            if geom.type in ['POINT', ]:
                map.draw_points(draw, geom.coords, meta, cfg.object)

            img = Image.alpha_composite(img.convert("RGBA"), poly_img)
            draw = ImageDraw.Draw(img)

        # Image варианты смешения изображений:
        #   blend - нет альфа-канала
        #   paste (composite) - один альфа-канал
        #   alpha_composite - два альфа-канала
        # При сбросе инстанса img сбрасывается контекст рисования draw !!!


        img = Image.alpha_composite(img.convert("RGBA"), text_img)

        m = cfg.grad.margin
        all_img = Image.new('RGB', (meta.szx + 2 * m, meta.szy + 2 * m), color='#ffffff')
        all_img.paste(img, (m, m))
        draw = ImageDraw.Draw(all_img, 'RGB')
        font = ImageFont.truetype(font=service_cfg.data_dir + cfg.grad.font, size=cfg.grad.size)

        xgs = []
        for nom_x in range(nom_x0, nom_x1 + 1):
            if (nom_x, nom_y0) not in inom_by_x_y:
                continue
            nom = map.shps['nom'][inom_by_x_y[(nom_x, nom_y0)]]
            xg0, yg0 = map.proj_3857_to_4326.transform(nom.bounds.x0, nom.bounds.y0)
            xg1, yg1 = map.proj_3857_to_4326.transform(nom.bounds.x1, nom.bounds.y1)
            nom_b = [(nom.bounds.x0, nom.bounds.y0), (nom.bounds.x1, nom.bounds.y1)]
            (x0, y0), (x1, y1) = map_lib.img_coords(nom_b, meta)
            xgs.append((int(round(xg0)), x0))
        xgs.append((int(round(xg1)), x1))
        for xg, x in xgs:
            draw.text((x + m, m / 2), str(xg + 90) + '°', fill=tuple(cfg.grad.color),
                      font=font, anchor='mm')
            draw.text((x + m, (meta.szy + 2 * m) - m / 2), str(xg + 90) + '°',
                      fill=tuple(cfg.grad.color),
                      font=font, anchor='mm')

        ygs = []
        for nom_y in range(nom_y0, nom_y1 + 1):
            if (nom_x0, nom_y) not in inom_by_x_y:
                continue
            nom = map.shps['nom'][inom_by_x_y[(nom_x0, nom_y)]]
            xg0, yg0 = map.proj_3857_to_4326.transform(nom.bounds.x0, nom.bounds.y0)
            xg1, yg1 = map.proj_3857_to_4326.transform(nom.bounds.x1, nom.bounds.y1)
            nom_b = [(nom.bounds.x0, nom.bounds.y0), (nom.bounds.x1, nom.bounds.y1)]
            (x0, y0), (x1, y1) = map_lib.img_coords(nom_b, meta)
            ygs.append((int(round(yg0)), y0))
        ygs.append((int(round(yg1)), y1))
        for yg, y in ygs:
            draw.text((m / 2, y + m), str(yg) + '°', fill=tuple(cfg.grad.color),
                      font=font, anchor='mm')
            draw.text(((meta.szx + 2 * m) - m / 2, y + m), str(yg) + '°',
                      fill=tuple(cfg.grad.color),
                      font=font, anchor='mm')

        data = io.BytesIO()
        all_img.save(data, format='PNG')
        data = data.getvalue()

        maps[section] = base64.b64encode(data).decode('ascii')

    return maps

def convert_date(date):
    r = re.compile("([0-9]{4})\-([0-9]{2})\-([0-9]{2})")
    m = re.match(r, date)
    if m:
        g = m.groups()
        return f'{g[2]}.{g[1]}.{g[0]}'
    return date


def fill_data(xml, data, map_handler, csv_handler):
    is_no_pi = False
    for protokol_type in ['протокол_подсчета_запасов', 'протокол_подсчета_ресурсов']:
        protokols_by_mineral_id = collections.defaultdict(list)  # [(mineral_id1,[prot1,prot2]),(mineral_id2,[prot1])]
        for protokol in data.отчет[protokol_type]:
            protokol.дата = convert_date(protokol.дата)
            if not protokol.mineral_ids:
                if not is_no_pi:
                    data.отчет.ископаемые.append({'mineral_id': 'id_no_pi', 'ископаемое': 'Отсутствуют ПИ',
                        'подсчет_запасов': '0', 'экспертиза_запасов': '0'})
                    is_no_pi = True
                protokol.mineral_ids.append('id_no_pi')
            for id in protokol.mineral_ids:
                protokols_by_mineral_id[id].append(protokol)
        pis = sorted([dict_(pi) for pi in data.отчет.ископаемые],  # сортировка пи по первому протоколу
                     key=lambda pi: protokols_by_mineral_id.get(pi.mineral_id)[0].номер \
                         if protokols_by_mineral_id.get(pi.mineral_id) else '')
        first_pi = None
        for pi in pis:
            pi.протоколы = protokols_by_mineral_id.get(pi.mineral_id, [])  # все протоколы для пи
            pi.single_protokol = pi.протоколы[0] if len(pi.протоколы) == 1 else None  # у пи только этот протокол
            if not pi.протоколы:
                pi.протоколы = [dict_(номер='')]
            pi.n_protokols = len(pi.протоколы)
            # если протокол у пи всего один и он совпадает с предыдущим единственным
            if first_pi and pi.single_protokol and pi.single_protokol == first_pi.single_protokol:
                first_pi.n_pis += 1  # объединяем верхнюю ячейку вертикально (rowspan)
                pi.n_pis = 0         # текущую ячейку не печатаем
            else:
                pi.n_pis = 1
                first_pi = pi
        if protokol_type == 'протокол_подсчета_запасов':
            data.отчет.ископаемые_запасы = pis
        if protokol_type == 'протокол_подсчета_ресурсов':
            data.отчет.ископаемые_ресурсы = pis
        # pprint(pis)

    участки = dict_()
    for участок in data.отчет.участки_работ:
        участки[участок['название_объекта']] = [x['ид'] for x in участок['инф_методе_работ']]

    data.результирующие_материалы = {}
    for item in data.данные_изученности:
        item.n_rows = 0
        if 'links' not in item:
            item.links = [dict_(метод='', объемы_и_единицы=[], методика='',
                                технические_средства=[dict_(название='', средства_контроля=[])],
                                n_rows=0, название_участка='')]
        for link in item.links:
            link.n_rows = 0
            id_inf = link.get('ид_инф_методе_работ')
            if id_inf:
                for name, ids in участки.items():
                    if id_inf in ids:
                        link['название_участка'] = name
            if not link.технические_средства:
                link['технические_средства'] = [dict_(название='', средства_контроля=[])]
            for средство in link.технические_средства:
                item.n_rows += 1
                link.n_rows += 1
        for индекс_работ in item.индексы_работ:
            vid = int(индекс_работ.вид)
            for материалы in item.интерпретированные_материалы:
                if vid not in data.результирующие_материалы:
                    data.результирующие_материалы[vid] = []
                материал = dict_(название=материалы.материал.название,
                                 масштаб=материалы.материал.масштаб,
                                 примечания=материалы.материал.примечания)
                data.результирующие_материалы[vid].append(материал)

    try:
        maps = draw_maps(xml, map_handler, csv_handler)
    except:
        # raise
        print('!' * 10, 'Map error', traceback.print_exc())
        maps = {}

    data.maps = maps

    return data


def pdf(data, jinja, in_html=False):
    def pdf_(template, orientation, num_pages, page_offset):

        options = {
            'margin-top': '12mm',
            'margin-left': '12mm',
            'margin-bottom': '15mm',
            'quiet': '',
            'orientation': orientation,
            'custom-header': [
                ('Authorization', cherrypy.request.headers.get('Authorization', 'Basic -'))],
            'footer-spacing': 5,
            'footer-font-size': service_cfg.footer_font_size,
            'footer-right': '[page]/%s' % (num_pages)
        }
        if page_offset:
            options.update({'page-offset': page_offset})

        snum = ''
        if 'номер_поставки' in data:
            snum = f"?snum={data['номер_поставки'].replace('-','')}"

        docker_ = '_docker' if service_cfg.docker else ''
        options.update({'footer-html': service_cfg.url + 'static/footer_izuch' + docker_ + '.html' + snum})
        tpl = jinja.get_template(template)
        html = tpl.render(data=data)
        if in_html:
            return html
        doc = pdfkit.from_string(html, False, options=options)

        return io.BytesIO(doc)

    tpls = [('1-22_1.tpl', 'Landscape'), ('22_2-22_11.tpl', 'Landscape'), ('23.tpl', 'Landscape')]

    if 'результирующие_материалы' in data:
        tpls.append(('24.tpl', 'Landscape'))

    service_cfg = lib.cfg('service')
    if in_html:
        return pdf_('1-22_1.tpl', 'Landscape', 0, 0)
    num_pages = 0
    for tpl in tpls:
        num_pages += len(PdfReader(pdf_(*tpl, 0, 0)).pages)

    merger = PdfMerger()
    page_offset = 0
    for tpl in tpls:
        merger.append(pdf_(*tpl, num_pages, page_offset), import_outline=False)
        page_offset += len(PdfReader(pdf_(*tpl, 0, 0)).pages)

    pdf = io.BytesIO()
    merger.write(pdf)


    return pdf.getvalue()
