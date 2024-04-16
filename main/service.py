import base64
from datetime import datetime
import cherrypy, glob, logging, os
import lib
import xml_to_pdf
from cache import Cache

def login(realm, user, pwd):
    if service_cfg.docker:
        # Получаем значения из переменных среды
        secret_user = os.getenv('USER')
        secret_pwd = os.getenv('PASSWORD')

        # Проверяем совпадение логина и пароля
        return user == secret_user and pwd == secret_pwd
    return user == service_cfg.user and pwd == service_cfg.pwd

class Root():

    def __init__(self):

        self.cfg = service_cfg
        cherrypy.log.screen = False
        self.src_types = xml_to_pdf.src_types()
        self.cache = Cache(self)

        print('Started at ', self.cfg.url)

    @cherrypy.expose
    def index(self):

        html = '<h2>Сервис печати СО РГФ</h2>'

        for src_type in self.src_types:
            html += '<h3>%s</h3>' % self.src_types[src_type].title
            html += 'URL сервиса: <a href="%s"><b>{0}</b></a>'.format(
                service_cfg.url + src_type + '/')
            html += '<br><br><a href="xml_to_pdf/%s/?test_cfg=1" ' \
                    'target="_blank">Образец</a><br><br>' % src_type
            test_files = glob.glob(self.cfg.data_dir + '/xml/*.xml')
            test_files += glob.glob(lib.main_dir() + 'tests/data/*.xml')
            for file in test_files:
                name = os.path.basename(file)[:-4]
                html += '<a href="xml_to_pdf/%s/?test_file=%s" target="_blank">%s</a>&nbsp;' % \
                        (src_type, name, name)

        return html

    def cache_xml(self, xml_file):
        now = datetime.now()
        tm = now.strftime('%Y-%m-%d_%H-%M-%S')
        try:
            name = xml_file.filename
            text = xml_file.fullvalue()
            if not name:
                name = 'xml'
            cache_file = f'cache_xml/{name}_{tm}.xml'
            if not os.path.exists(cache_file):
                dir = os.path.dirname(cache_file)
                if not os.path.exists(dir):
                    os.makedirs(dir)
                with open(cache_file, 'w', encoding=xml_file.charset) as f:
                    f.write(text)
                print('make ' + cache_file)

        except Exception as e:
            print('err cache', e)

    @cherrypy.expose
    def xml_to_pdf(self, src_type, xml=None, xml_file=None, test_file=None, test_cfg=False, in_html=False):

        if src_type not in self.src_types:
            raise cherrypy.HTTPError(status=400, message='Unknown source type')
        if xml_file:
            self.cache_xml(xml_file)
            xml_text = xml_file.fullvalue()
            data = xml_to_pdf.xml_to_data(src_type, xml_text=xml_text)
            pdf = xml_to_pdf.data_to_pdf(src_type, data)
        elif xml:
            data = xml_to_pdf.xml_to_data(src_type, xml_text=xml)
            pdf = xml_to_pdf.data_to_pdf(src_type, data)
        elif test_cfg:
            data = xml_to_pdf.test_data_from_cfg(src_type)
            data.виды_изученности = {
                1: 'Геологическая', 2: 'Геофизическая', 3: 'Геохимическая',
                4: 'Инженерно-геологическая', 5: 'Гидрогеологическая', 6: 'Геоэкологическая'
            }
            xml_to_pdf.modules[src_type].fill_data(xml, data, xml_to_pdf.map_handler, xml_to_pdf.csv_handler)
            pdf = xml_to_pdf.data_to_pdf(src_type, data)
        elif test_file is not None:
            xml_file = lib.main_dir() + 'tests/data/' + test_file + '.xml'
            if not os.path.exists(xml_file):
                xml_file = self.cfg.data_dir + '/xml/' + test_file + '.xml'
            data = xml_to_pdf.xml_to_data(src_type, xml_file)
            pdf = xml_to_pdf.data_to_pdf(src_type, data, in_html)
        elif xml is None:
            raise cherrypy.HTTPError(status=400, message='xml parameter not set')

        if isinstance(pdf, str):
            if self.cfg.production:
                raise cherrypy.HTTPError(status=400, message=pdf)
            else:
                return pdf
        if in_html:
            return pdf

        cherrypy.response.headers['Content-Type'] = 'application/pdf'
        cherrypy.response.headers['Content-Disposition'] = 'inline;filename="izuch.pdf"'

        return pdf

service_cfg = lib.cfg('service')
if service_cfg.production:
    cherrypy.config.update({'environment': 'production'})


config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': service_cfg.port,
        'tools.auth_basic.on': True,
        'tools.auth_basic.realm': 'localhost',
        'tools.auth_basic.checkpassword': login,
        'tools.auth_basic.accept_charset': 'UTF-8',
    },
    '/static': {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': lib.main_dir() + 'static'
    }
}

cherrypy.quickstart(Root(), '', config)