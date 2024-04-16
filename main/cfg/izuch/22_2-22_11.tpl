<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Print Form</title>
    <style>
        table td {
            vertical-align: top;
        }
        table p {
            margin: 0;
        }
        table, tr, td, th, tbody, thead, tfoot {
            page-break-inside: avoid !important;
        }
        html,
        body {
            {#padding: 25px 0 0 25px;#}
            margin: 0;
            font-size: 13px;
            font-family: PT Serif;
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
        tr {
            page-break-inside: avoid;
            page-break-after: auto;
        }
        th, td {
            border: 1px solid black;
            padding: .3rem;
            text-align: center;
        }
        th:after, td:after {
            content: '';
            display: block;
            width: 100%;
            height: 1px;
            background-color: transparent;
        }
        .col_22_2, .col_22_3, .col_22_5,
        .col_22_6, .col_22_8_1, .col_22_8_2 {
            width: 10mm;
        }
        .col_22_9 {
            width: 20mm;
        }
        .col_22_4, .col_22_7 {
            width: 25mm;
        }
        .col_22_10, .col_22_11 {
            width: 35mm;
        }
    </style>
</head>
<body>
    <table id="work-table">
        <col class="col_22_2">
        <col class="col_22_3">
        <col class="col_22_4">
        <col class="col_22_5">
        <col class="col_22_6">
        <col class="col_22_7">
        <col class="col_22_8_1">
        <col class="col_22_8_2">
        <col class="col_22_9">
        <col class="col_22_10">
        <col class="col_22_11">
            <tr>
                <th rowspan="2">22.2 Вид изученности</th>
                <th rowspan="2">22.3 Вид работ (индекс)</th>
                <th rowspan="2">22.4 Угловые координаты контура работ: широта, долгота (град., мин., сек.)</th>
                <th rowspan="2">22.5 Масштаб</th>
                <th rowspan="2">22.6 Площадь</th>
                <th rowspan="2">22.7 Метод/модификация</th>
                <th rowspan="1" colspan="2">22.8</th>
                <th rowspan="2">22.9 Технические средства</th>
                <th rowspan="2">22.10 Методика</th>
                <th rowspan="2">22.11 Камеральные работы</th>
            </tr>
            <tr>
                <th>22.8.1 Объем работ</th>
                <th>22.8.2 Единицы измерения</th>
            </tr>
        {% set виды_изученности = {'1':'Геологическая', '2':'Геофизическая', '3':'Геохимическая',
                                   '4':'Инженерно-геологическая', '5':'Гидрогеологическая', '6':'Геоэкологическая'} %}

        {% for iизученность, изученность in enumerate(data.данные_изученности) %}
            {% for индекс_работ in изученность.индексы_работ %}

                {% if not изученность.links %}
                    <tr>
                        <td rowspan="{{ изученность.n_rows }}">
                            {{ виды_изученности[индекс_работ.вид] }}
                        </td>
                        <td rowspan="{{ изученность.n_rows }}">{{ индекс_работ.индекс }}</td>
                        <td rowspan="{{ изученность.n_rows }}">
                            {% for контур in изученность.контур_работ %}
                                <p>{{ контур.название }}
                                <p>СВ {{ контур.пределы.y1 }} {{ контур.пределы.x1 }}
                                <p>ЮЗ {{ контур.пределы.y0 }} {{ контур.пределы.x0 }}
                            {% endfor %}
                        </td>
                        <td rowspan="{{ изученность.n_rows }}">{{ изученность.масштаб }}</td>
                        <td rowspan="{{ изученность.n_rows }}">{{ изученность.площадь }}</td>
                        <td></td><td></td><td></td><td></td><td></td>
                        <td rowspan="{{ изученность.n_rows }}">{{ изученность.камеральные_работы }}</td>
                    </tr>
                {% endif %}

                {% for ilink, link in enumerate(изученность.links) %}
                    {% for iсредство, средство in enumerate(link.технические_средства) %}
                        <tr>
                            {% if ilink==0 and iсредство==0 %}
                                <td rowspan="{{ изученность.n_rows }}">
                                    {{ виды_изученности[индекс_работ.вид] }}
                                </td>
                                <td rowspan="{{ изученность.n_rows }}">{{ индекс_работ.индекс }}</td>
                            {% endif %}
                            {% if ilink==0 and iсредство==0 %}
                                <td rowspan="{{ изученность.n_rows }}">
                                    {% for контур in изученность.контур_работ %}
                                        <p>{{ контур.название }}
                                        <p>СВ {{ контур.пределы.y1 }} {{ контур.пределы.x1 }}
                                        <p>ЮЗ {{ контур.пределы.y0 }} {{ контур.пределы.x0 }}
                                    {% endfor %}
                                </td>
                                <td rowspan="{{ изученность.n_rows }}">{{ изученность.масштаб }}</td>
                                <td rowspan="{{ изученность.n_rows }}">{{ изученность.площадь }}</td>
                            {% endif %}
                            {% if iсредство==0 %}
                                <td rowspan="{{ link.n_rows }}">
                                    <p>{{ link.метод }}</p>
                                    <p>{{ link.название_участка }}</p>
                                </td>
                                <td rowspan="{{ link.n_rows }}">
                                    {% for item in link.объемы_и_единицы %}
                                        <p>{{ item.объем }}</p>
                                    {% endfor %}
                                </td>
                                <td rowspan="{{ link.n_rows }}">
                                    {% for item in link.объемы_и_единицы %}
                                        <p>{{ item.единицы }}</p>
                                    {% endfor %}
                                </td>
                            {% endif %}
                            <td>{{ средство.название }}</td>
                            {% if iсредство==0 %}
                                <td rowspan="{{ link.n_rows }}">{{ link.методика }}</td>
                            {% endif %}
                            {% if ilink==0 and iсредство==0 %}
                                <td rowspan="{{ изученность.n_rows }}">{{ изученность.камеральные_работы }}</td>
                            {% endif %}
                        </tr>
                    {% endfor %}
                {% endfor %}
            {% endfor %}
        {% endfor %}
    </table>

{#    <pre>{{ json.dumps(data.данные_изученности, indent=2, sort_keys=True, ensure_ascii=False) }}</pre>#}
</body>
</html>