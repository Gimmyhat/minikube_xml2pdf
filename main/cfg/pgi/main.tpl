<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Карточка первичной ГИ</title>
    <meta charset="utf-8">

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
        html {
            box-sizing: border-box;
            font-size: 18px;
            font-family: PT Serif, serif;
        }
        *,
        *::before,
        *::after {
            box-sizing: inherit;
        }
        body {
            margin: 0;
        }
        img {
            max-width: 100%;
        }
        a {
            {#text-decoration: none;#}
            {#color: inherit;#}
        }
        ul {
            margin: 0;
            padding: 0;
            list-style-type: none;
        }
        h2 {
            margin: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            word-break: break-all;
            overflow-wrap: break-word;
            table-layout: fixed;
            box-shadow: 0 0 0 2px #000 inset;
        }
        th, td {
            padding: 3px;
            border: 1px solid #000;
        }
        th:after, td:after {
            content: '';
            display: block;
            width: 100%;
            height: 1px;
            background-color: transparent;
        }
        .main-table td,
        .main-table tr:not(:first-child) th {
            vertical-align: top;
        }
        p:first-child {
            margin-top: 0;
        }
        p:last-child {
            margin-bottom: 0;
        }
        .fixed-container {
            max-width: 1200px;
            padding: 0;
            margin: 0 auto;
        }
        .header, .main {
            margin-bottom: 20px;
        }
        .main-table {
            text-align: center;
            font-size: .8333rem;
        }
        .main-table__col1 { width: 3.75%; }
        {#.main-table__col2 { width: 17.5%; }#}
        .main-table__col2 { width: 21%; }
        .main-table__col3 { width: 8.75%; }
        .main-table__col4 { width: 11.25%; }
        .main-table__col5 { width: 8.75%; }
        {#.main-table__col6 { width: 13.75%; }#}
        .main-table__col6 { width: 17.75%; }
        .main-table__col7 { width: 7.5%; }
        .main-table__col8 { width: 10%; }
        {#.main-table__col9 { width: 7.5%; }#}
        .main-table__col10 { width: 11.25%; }
        .main-table__h2,
        .main-table__h3 {
            font-weight: bold;
            text-align: left;
        }
        .main-table__h2 {
            font-size: 1rem;
        }
        .main-table__methodology {
            font-weight: normal;
            font-style: italic;
        }
        .title {
            text-align: center;
            padding-bottom: 16px;
            font-weight: bold;
        }
        .main-table th {
            word-break: break-word;
            word-wrap: normal;
            vertical-align: top;
        }
    </style>
</head>
<body>
    <div class="title">Пояснительная записка к первичной геологической информации</div>
    <header class="header">
        <div class="fixed-container">
            <table>
                <tr>
                    <th>Пользователь недр</td>
                    <td>{{ data.отчет.недропользователь }}</td>
                </tr>
                <tr>
                    <th>Номер государственной регистрации</td>
                    <td>
                        {% for item_нгр in data.отчет.номера_гос_регистрации %}
                            {{ item_нгр.номер }}{% if not loop.last %}, {% endif %}
                        {% endfor %}
                    </td>
                </tr>
                <tr>
                    <th>Лицензия</td>
                    <td>
                        {% for item in data.отчет.лицензии %}
                            {{ item.серия }} от {{ date(item.дата_регистрации) }}
                            {% if not loop.last %}<br>{% endif %}
                        {% endfor %}
                    </td>
                </tr>
                <tr>
                    <th>Наименование комплекта</td>
                    <td>{{ data.название_отчета }}</td>
                </tr>
                <tr>
                    <th>Номер комплекта</td>
                    <td>{{ data.номер_поставки }}</td>
                </tr>
            </table>
        </div>
    </header>
    <main class="main">
        <div class="fixed-container">
            <table class="main-table">
                <col class="main-table__col1">
                <col class="main-table__col2">
                <col class="main-table__col3">
                <col class="main-table__col4">
                <col class="main-table__col5">
                <col class="main-table__col6">
                <col class="main-table__col7">
                <col class="main-table__col8">
{#                <col class="main-table__col9">#}
                <col class="main-table__col10">
                <tr>
                    <th>№ п/п</th>
                    <th>Метод/модификация</th>
                    <th>Масштаб работ</th>
                    <th>Технические средства</th>
                    <th>Средства контроля</th>
                    <th>Перечень результативных материалов</th>
                    <th>Объем работ</th>
                    <th>Единицы измерения</th>
{#                    <th>Формат</th>#}
                    <th>Примечание</th>
                </tr>
                <tr>
                    {% for i in range(9) %}
                        <td>{{ i + 1 }}</td>
                    {% endfor %}
                </tr>
                {% for iучасток_работ, участок_работ in enumerate(data.отчет.участки_работ) %}
                    <tr><td colspan="11" class="main-table__h2">{{ участок_работ.название }}</td></tr>
                    {% for iметод_работы, метод_работы in enumerate(участок_работ.методы_работ) %}
                        {% if метод_работы.вид_пользования_недрами %}
                            <tr><td colspan="11" class="main-table__h3">
                                {{ метод_работы.вид_пользования_недрами }}</td></tr>
                        {% endif %}
                        {% for iматериал, материал in enumerate(метод_работы.материалы) %}
                            <tr>
                                {% if iматериал==0 %}
                                    <th rowspan="{{ метод_работы.n_rows }}">{{ iметод_работы + 1 }}</th>
                                    <th rowspan="{{ метод_работы.n_rows }}">
                                        {{ метод_работы.метод }}
{#                                        {% if метод_работы.методика %}#}
{#                                            <br>#}
{#                                            <span class="main-table__methodology">#}
{#                                                {{ метод_работы.методика }}#}
{#                                            </span>#}
{#                                            <br><br>#}
{#                                        {% endif %}#}
                                    </th>
                                    <td rowspan="{{ метод_работы.n_rows }}">
                                        {{ метод_работы.масштаб }}
                                    </td>
                                    <td rowspan="{{ метод_работы.n_rows }}">
                                        {% for тех_средство in метод_работы.технические_средства %}
                                            <p>{{ тех_средство.название }}
                                        {% endfor %}
                                    </td>
                                    <td rowspan="{{ метод_работы.n_rows }}">
                                        {% for тех_средство in метод_работы.технические_средства %}
                                            {% for item in тех_средство.путь_к_файлу %}
                                                <p>{{ item.путь_к_файлу }}
                                            {% endfor %}
                                        {% endfor %}
                                    </td>
                                {% endif %}
                                <td>
                                    {% if материал.ссылка %}
                                        <a href="{{ материал.ссылка }}" target="_blank">
                                            {{ iметод_работы + 1 }}.{{ iматериал + 1 }}
                                            {{ материал.название }}
                                        </a>
                                    {% else %}
                                        {{ iметод_работы + 1 }}.{{ iматериал + 1 }}
                                        {{ материал.название }}
                                    {% endif %}
                                </td>
                                {% if iматериал==0 %}
                                    <td rowspan="{{ метод_работы.n_rows }}">
                                        {% for объем_работ in метод_работы.объемы_работ %}
                                            <p>{{ объем_работ.объем }}
                                        {% endfor %}
                                    </td>
                                    <td rowspan="{{ метод_работы.n_rows }}">
                                        {% for объем_работ in метод_работы.объемы_работ %}
                                            <p>{{ объем_работ.единицы_измерения }}
                                        {% endfor %}
                                    </td>
                                {% endif %}
{#                                <td>#}
{#                                    {{ материал.формат }}#}
{#                                </td>#}
                                <td>{{ материал.примечание }}</td>
                            </tr>
                        {% endfor %}
                    {% endfor %}
                {% endfor %}
            </table>
        </div>
    </main>
</body>
</html>
