import cherrypy
import os
from lxml import etree as et
import re


class Cache:

    def __init__(self, root):

        self.root = root

    @cherrypy.expose
    def index(self):

        header = '<head><style>div {margin-bottom: .5rem;} a:hover {color: #a18043}</style></head>'
        html = '<h1>Cache</h1>'
        for file in sorted(os.listdir('cache_xml'), reverse=True):
            file_ = self.get_file_id(file)
            html += f"""
                <div>
                    {file_}&ensp;
                    <a href="file/izuch/{file}" target="_blank">izuch</a>&ensp;
                    <a href="file/igi/{file}" target="_blank">igi</a>&ensp;
                    <a href="file/pgi/{file}" target="_blank">pgi</a>&ensp;
                    <a href="file/xml/{file}" target="_blank">xml</a>
                </div>
            """

        return f'<html>{header}<body>{html}</body></html>'

    def get_file_id(self, file_name):

        file_path = 'cache_xml/' + file_name
        if os.path.exists(file_path):
            with open(file_path) as f:
                xml = f.read()
                id_ = self.get_supply_id(xml)
                if id_:
                    file_name = file_name[:-4] + '_' + id_ + file_name[-4:]

        return file_name

    @cherrypy.expose
    def file(self, type, file):

        file_path = 'cache_xml/' + file
        if os.path.exists(file_path):
            with open(file_path) as f:
                xml = f.read()
            if type in ['izuch', 'igi', 'pgi']:
                return self.root.xml_to_pdf(type, xml=xml)
            if type == 'xml':
                cherrypy.response.headers['Content-Type'] = 'text/xml;charset=utf-8'
                cherrypy.response.headers['Content-Disposition'] = f'inline;filename="{self.get_file_id(file)}"'
                return xml

        else:
            return f'file {file} not found'

    def get_supply_id(self, xml):

        id_ = None
        xml = self.parse_xml(xml)
        if xml is not None:
            id_ = self.txt(xml.xpath('/supply/idSupply/text()'))
        return id_

    def parse_xml(self, xml_):

        xml_text = self.remove_ns(xml_)
        xml_text = xml_text.replace('xmlns:', 'xmlns_').replace('xmlns=', 'xmlns_=')
        xml = None
        if xml_text:
            try:
                xml = et.fromstring(bytes(xml_text, encoding='utf-8'))
            except Exception as e:
                print('error', e)
        if xml is None:
            print('xml parsing error')

        return xml

    @staticmethod
    def txt(val):
        if isinstance(val, list):
            if len(val) > 0:
                if len(val) > 1:
                    print('val > 0', val)
                return val[0]
        return None

    @staticmethod
    def remove_ns(xml):

        gr = re.findall('(<[a-z]+:)', xml)
        gr = set(gr)
        for n in gr:
            n = n[1:-1]
            xml = xml.replace(f'<{n}:', f'<{n}_').replace(f'</{n}:', f'</{n}_')

        return xml
