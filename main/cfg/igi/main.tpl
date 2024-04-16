<!DOCTYPE html>
<html lang="ru">
<head>
    <title>Карточка интерпретированной ГИ</title>
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
            font-family: PT Serif;
        }
        *,
        *::before,
        *::after {
            box-sizing: inherit;
        }
        body {
            margin: 0;
            font-size: 18px;
        }
        img {
            max-width: 100%;
        }
        a {
            text-decoration: none;
            color: inherit;
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
            border: 2px solid #000;
            width: 100%;
            border-collapse: collapse;
            word-break: break-all;
            overflow-wrap: break-word;
        }
        th, td {
            padding: 5px;
            border: 1px solid #000;
        }
        p:first-child {
            margin-top: 0;
        }
        p:last-child {
            margin-bottom: 0;
        }
        .clearfix::after {
            content: "";
            display: table;
            clear: both;
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
        }
        .main-table tr th:first-child {
            min-width: 3rem;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="fixed-container">
            <table>
                <tr>
                    <th>Пользователь недр</td>
                    <td>{{ data.отчет.недропользователь }}</td>
                </tr>
                <tr>
                    <th>№ государственной регистрации работ</td>
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
                    <th>Название отчета</td>
                    <td>{{ data.название_отчета }}</td>
                </tr>
            </table>
        </div>
    </header>
    <main class="main">
        <div class="fixed-container">
            <table class="main-table">
                <tr>
                    <th>№ п/п</th>
                    <th>Название</th>
                    <th>Интерпретация по виду (методу) работ</th>
                    <th>Формат (расширение) или ПО</th>
                    <th>Путь к файлу/папке</th>
                    <th>Примечание</th>
                </tr>
                {% for irow, item in enumerate(data.отчет.интерпретированные_данные) %}
                    <tr>
                        <td>
                            {{ irow + 1 }}
                        </td>
                        <td>
                            {{ item.данные.название }}
                        </td>
                        <td>
                            {% for method_info in item.ссылка_на_метод %}
                                <p>{{ method_info.метод }}
                            {% endfor %}
                        </td>
                        <td>
                            {{ item.данные.формат }}
                        </td>
                        <td>
                            {% for файл in item.данные.файлы %}
                                <p>{{ файл.путь_к_файлу }}
                            {% endfor %}
                        </td>
                        <td>
                            {{ item.данные.примечание }}
                        </td>
                    </tr>
                {% endfor %}
            </table>
        </div>
    </main>
    <footer class="footer">
        <div class="fixed-container">

        </div>
    </footer>
</body>
</html>
