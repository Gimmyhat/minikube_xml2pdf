# Базовый образ
FROM ubuntu:22.04

WORKDIR /main

# Копирование данных и установка пакетов
COPY ./base /distr
RUN apt update && apt -y install /distr/wkhtmltox_0.12.6.1-2.jammy_amd64.deb python3 pip && \
    pip install pyproj pyshp pyyaml pillow pypdf2 pdfkit cherrypy untangle jinja2 requests kubernetes lxml && \
    cp -r /distr/PT_Serif /usr/share/fonts/truetype && fc-cache -f -v

# Копирование проекта
COPY ./main /main

# Команда запуска
CMD ["python3", "/main/service.py"]
