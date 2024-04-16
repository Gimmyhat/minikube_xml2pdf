import sys, os, traceback
import pdfkit
import base64
import lib
from lib import dict_
import cherrypy

def fill_data(xml, data, map_handler, csv_handler):

    return data

def pdf(data, jinja, in_html=None):

    tpl = jinja.get_template('main.tpl')
    html = tpl.render(data=data)
    service_cfg = lib.cfg('service')

    snum = ''
    if 'номер_поставки' in data:
        snum = f"?snum={data['номер_поставки'].replace('-','')}"

    docker_ = '_docker' if service_cfg.docker else ''
    pdf_data = pdfkit.from_string(html, False, options={
        'margin-left': '3cm',
        'orientation': 'Landscape',
        'quiet': '',
        'margin-bottom': '15mm',
        'custom-header': [('Authorization', cherrypy.request.headers['Authorization'])],
        'footer-html': service_cfg.url + 'static/footer_pgi' + docker_ + '.html' + snum,
        'footer-spacing': 5,
        'footer-font-size': service_cfg.footer_font_size,
        'footer-right': '[page]/[toPage]'
    })

    return pdf_data

