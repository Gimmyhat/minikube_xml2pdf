import sys, os
import untangle
import jinja2
import json
from pprint import pprint
from xml.sax.saxutils import escape
import csv

import lib
from lib import dict_
import map_lib

import izuch
import igi
import pgi

def src_types():

    src_types = {}
    main_cfg = lib.cfg('main')
    for src_type in main_cfg.src_types:
        src_types[src_type] = lib.cfg(src_type + '/' + src_type)

    return src_types

def fill_std_data(src_type, root):

    data_cfg = lib.cfg(src_type + '/' + src_type)
    data = fill_std_data_iter(root, data_cfg.xml, root, '')

    return data

def find_link_data(path, link_id, root):

    xmls = [root]
    path = path.split('/')
    for attr in path[:-1]:
        next_xmls = []
        for xml in xmls:
            next_xml = lib.get_xml_attr(xml, attr)
            if next_xml is None:
                continue
            if not isinstance(next_xml, list):
                next_xml = [next_xml]
            next_xmls.extend(next_xml)
        xmls = next_xmls
    for xml in xmls:
        if lib.get_xml_attr(xml, path[-1]).cdata==link_id:
            return xml
    else:
        raise Exception('Can not find link_id', link_id)

def fill_std_data_iter(xml, cfg, root, path):

    if '_xml' in cfg:
        xml = lib.get_xml_attr(xml, cfg._xml)
    elif '_link' in cfg:
        xml = find_link_data(cfg._link, xml.cdata, root)

    type = cfg.get('_type', 'str')
    data = ''
    if type=='str':
        if xml is not None:
            if isinstance(xml, list):
                raise Exception('Element is list', path)
            data = escape(xml.cdata)
    elif type=='object':
        data = dict_()
        if xml is not None:
            for attr, attr_cfg in cfg.items():
                if attr.startswith('_'):
                    continue
                data[attr] = fill_std_data_iter(xml, cfg[attr], root, path + '.' + attr)
    elif type=='list':
        data = []
        if xml is not None:
            if not isinstance(xml, list):
                xml = [xml]
            for item in xml:
                data.append(fill_std_data_iter(item, cfg._items[0], root, path + '.[]'))
    elif type=='csv':
        if xml is not None:
            csv_name, col = cfg._csv.split('.')
            if isinstance(xml, list):
                raise Exception('Element is list', path)
            data = csv_handler.data[csv_name][xml.cdata][col]
    elif type=='skip':
        data = None
    elif type=='bounds':
        geom = map_lib.geom_from_xml(xml, apply_xg_90=False)
        if geom:
            bounds = map_lib.bounds([dict_(coords=geom.coords)])
            data = dict_(x0=map_lib.dms(bounds.x0), x1=map_lib.dms(bounds.x1),
                         y0=map_lib.dms(bounds.y0), y1=map_lib.dms(bounds.y1))
        else:
            data = ''
    else:
        raise Exception('Unknown type', type)

    return data

def test_data_from_cfg(src_type):

    data_cfg = lib.cfg(src_type + '/' + src_type)

    data = test_data_from_cfg_iter(data_cfg.xml)

    return data

def test_data_from_cfg_iter(cfg):

    type = cfg.get('_type', 'str')

    if type in ['str', 'csv', 'skip', 'bounds']:
        data = cfg._test
    elif type=='object':
        data = dict_()
        for attr, attr_cfg in cfg.items():
            if attr.startswith('_'):
                continue
            data[attr] = test_data_from_cfg_iter(cfg[attr])
    elif type=='list':
        if '_test' in cfg:
            return cfg._test
        data = []
        data.append(test_data_from_cfg_iter(cfg._items[0]))
        data.extend(cfg._items[1:])
    else:
        raise Exception('Unknown type')

    return data

def xml_to_data(src_type, xml_text=None, xml_file=None):

    if not xml_text:
        with open(xml_file) as f:
            xml_text = f.read()

    try:
        xml = untangle.parse(xml_text)
    except:
        return 'XML parsing error'

    data = fill_std_data(src_type, xml)

    data.виды_изученности = {
        1: 'Геологическая', 2: 'Геофизическая', 3: 'Геохимическая',
        4: 'Инженерно-геологическая', 5: 'Гидрогеологическая', 6: 'Геоэкологическая'
    }
    # pprint(data)
    if src_type not in modules:
        raise Exception('Unknown source type')
    modules[src_type].fill_data(xml, data, map_handler, csv_handler)

    return data

def data_to_pdf(src_type, data, in_html=False):

    cfg_dir = jinja2.FileSystemLoader(lib.main_dir() + '/cfg/%s/' % src_type)
    jinja = jinja2.Environment(loader=cfg_dir)
    jinja.globals.update(dict(len=len, enumerate=enumerate, json=json,
                              date=lib.russian_date))
    if src_type not in modules:
        raise Exception('Unknown source type')
    pdf = modules[src_type].pdf(data, jinja, in_html)

    return pdf

class CSV:

    def __init__(self):

        self.data_ = {}

    @property
    def data(self):

        for csv, csv_cfg in lib.cfg('csv').items():
            self.data_[csv] = CSV.read(csv, csv_cfg)

        return self.data_

    def read(csv_, csv_cfg):

        data = {}
        with open(lib.cfg('service').data_dir + 'csv/%s.csv' % csv_, encoding='cp1251') as file:
            reader = csv.reader(file)
            for line in reader:
                data[line[0]] = {col: value for col, value in zip(csv_cfg.columns, line[1:])}

        return data

modules = {'izuch': izuch, 'igi': igi, 'pgi': pgi}
map_handler = map_lib.Map()
csv_handler = CSV()

if __name__=='__main__':

    src_types = src_types()
    try:
        if len(sys.argv)!=4:
            raise Exception('Wrong number of arguments')
        src_type, xml_file, pdf_file = sys.argv[1:4]
        if src_type not in src_types:
            raise Exception('Unknown source type')
        if not os.path.exists(xml_file):
            raise Exception('Input xml file not exists')
    except Exception as ex:
        print('Error: %s\n' % ex)
        print('Usage: xml_to_pdf <src_type> <input_xml_file> <output_pdf_file>')
        print('Source types:')
        for src_type, type_cfg in src_types.items():
            print('   %s: %s' % (src_type, type_cfg.title))
        sys.exit(1)

    data = xml_to_data(src_type, xml_file)
    pdf = data_to_pdf(src_type, data)

    if isinstance(pdf, str):
        print('ERROR: ', pdf)
        sys.exit(1)

    with open(pdf_file, 'wb') as f:
        f.write(pdf)

    print('Done')
