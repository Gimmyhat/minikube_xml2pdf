<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <title>Print Form</title>
        <style>
            table td {
                vertical-align: top;
            }
            p {
                margin: 0;
            }
            table, tr, td, th, tbody, thead, tfoot {
                page-break-inside: avoid !important;
            }
            html,
            body {
                padding: 0;
                margin: 0;
                font-size: 13px;
                font-family: PT Serif;
            }
            body {
                {#padding: 1.27cm;#}
            }
            img {
                max-width: 100%;
                max-height: 19cm;
            }
            .page_break {
                page-break-after: always;
            }
            .margin16 {
                margin-bottom: 16px;
            }
        </style>
    </head>
    <body>
        <p>
            <b>23. Схема размещения контуров изученности</b>
        </p>

        {% set ns = namespace(first_break=False) %}
        {% for vid in range(1,7) %}
            {% if '23.%s' % vid in data.maps %}
                {% if ns.first_break %}
                    <div class="page_break"></div>
                {% endif %}
                {% set ns.first_break = True %}
                <p class="margin16">
                    <span>23.{{ vid }} {{ data.виды_изученности[vid] }} изученность</span>
                </p>
                <p>
                    <img class="img" src="data:image/jpeg;base64,{{ data.maps['23.%s' % vid] }}"/>
                </p>
            {% endif %}
        {% endfor %}
    </body>
</html>