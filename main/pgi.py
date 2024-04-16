import sys, os, traceback
import pdfkit
import base64
import lib
from lib import dict_
import cherrypy

def fill_data(xml, data, map_handler, csv_handler):

    for участок_работ in data.отчет.участки_работ:
        участок_работ.n_rows = 0
        if 'методы_работ' not in участок_работ:
            участок_работ.методы_работ = [dict_()]

        sorted(участок_работ.методы_работ, key=lambda item: item.вид_пользования_недрами)

        vid = None
        for метод_работы in участок_работ.методы_работ:
            if vid == метод_работы.вид_пользования_недрами:
                метод_работы.вид_пользования_недрами = None
            else:
                vid = метод_работы.вид_пользования_недрами

        for метод_работы in участок_работ.методы_работ:
            метод_работы.n_rows = 0
            if not метод_работы.материалы:
                метод_работы.материалы = [dict_(название='', объем_и_единицы='', формат='', путь='')]
            for материал in метод_работы.материалы:
                участок_работ.n_rows += 1
                метод_работы.n_rows += 1

    return data

def pdf(data, jinja, in_html=None):

    tpl = jinja.get_template('main.tpl')
    html = tpl.render(data=data)
    service_cfg = lib.cfg('service')

    snum = ''
    if 'номер_поставки' in data:
        snum = f"?snum={data['номер_поставки'].replace('-','')}"

    if in_html:
        return html
    docker_ = '_docker' if service_cfg.docker else ''
    pdf_data = pdfkit.from_string(html, False, options={
        'margin-left': '3cm',
        'orientation': 'Landscape',
        'quiet': '',
        'margin-bottom': '15mm',
        'custom-header': [('Authorization', cherrypy.request.headers['Authorization'])],
        'footer-html': service_cfg.url + 'static/footer_pgi' + docker_ + '.html' + snum,
        'footer-font-size': service_cfg.footer_font_size,
        'footer-spacing': 5,
        'footer-right': '[page]/[toPage]'
    })

    return pdf_data
