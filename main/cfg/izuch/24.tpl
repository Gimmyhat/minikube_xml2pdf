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
            {#padding: 0;#}
            {#margin: 0;#}
            {#font-size: 18px;#}
            {#font-family: PT Serif;#}

            {#padding: 25px 0 0 25px;#}
            margin: 0;
            font-size: 13px;
            font-family: PT Serif;
        }
        body {
            {#padding: 1.27cm;#}
        }
        table {
            font-size: .8333rem;
            border-collapse: collapse;
            width: 100%;
            word-break: break-all;
            overflow-wrap: break-word;
            table-layout: fixed;
            page-break-inside: auto;
        }
        table.fsize1 {
            font-size: 1rem;
        }
        tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }
        th, td {
            border: 1px solid black;
            padding: .3rem;
            text-align: center;
        }
        .col1 {
            width: 17%;
        }
        .col2 {
            width: 50%;
        }
        .col3 {
            width: 11%;
        }
        .col4 {
            width: 22%;
        }
    </style>
</head>
<body>
    <p>
        <b>24. Основные результаты по видам изученности</b>
    </p>
    <table id="work-table">
        <col class="col1">
        <col class="col2">
        <col class="col3">
        <col class="col4">
        <tr>
            <th>24.1 Вид изученности</th>
            <th>24.2 Перечень результирующих материалов</th>
            <th>24.3 Масштаб</th>
            <th>24.4 Примечания</th>
        </tr>

        {% set виды_изученности = {1:'Геологическая', 2:'Геофизическая', 3:'Геохимическая',
                                   4:'Инженерно-геологическая', 5:'Гидрогеологическая', 6:'Геоэкологическая'} %}

        {% for вид_изученности in range(1,7) %}
            {% for iматериал, материал in enumerate(data.результирующие_материалы[вид_изученности]) %}
                <tr>
                    {% if iматериал == 0 %}
                        <td class="fsize1" rowspan="{{ data.результирующие_материалы[вид_изученности]|length }}">
                            {{ виды_изученности[вид_изученности] }}
                        </td>
                    {% endif %}
                    <td>
                        {{ материал.название }}
                    </td>
                    <td>
                        {{ материал.масштаб }}
                    </td>
                    <td>
                        {{ материал.примечания }}
                    </td>
                </tr>
            {% endfor %}
        {% endfor %}
    </table>

</body>
</html>