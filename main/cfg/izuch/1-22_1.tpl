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
            font-size: 14px;
            font-family: PT Serif;
        }
        #uk-cover {
            {#padding: 1rem;#}
            {#padding: 1.27cm;#}
            {#width: 29.7cm;#}
            width: 100%;
            box-sizing: border-box;
        }
        #uk-cover h3 {
            font-weight: normal;
        }
        #uk-cover table {
            border-collapse: collapse;
            width: 100%;
            word-break: break-all;
            overflow-wrap: break-word;
            table-layout: fixed;
        }
        #uk-cover table.no-break {
            word-break: normal;
        }
        #uk-cover th {
            text-align: center;
        }
        #uk-cover th,
        #uk-cover td {
            border: 1px solid black;
            text-align: center;
        }
        {% for изученность in data.данные_изученности %}
            {% for индекс_работ in изученность.индексы_работ %}
                #uk-cover [data-study-type="{{ индекс_работ.вид }}"] {
                    background-color: #bfbfbf;
                }
            {% endfor %}
        {% endfor %}
        img {
            max-width: 100%;
            max-height: 19cm;
        }
        {##work-table {#}
        {#    font-size: 1rem;#}
        {# }#}
        .page_break {
            page-break-after: always;
        }
        .v-top th {
            vertical-align: top;
        }
        #uk-cover .no-border td {
            border: none;
        }
        #uk-cover .border td {
            border: 1px solid black;
        }
        #uk-cover .text-left td {
            text-align: left;
        }
        #uk-cover .text-center td {
            text-align: center;
        }
        .br-margin8 b {
            margin-right: 8px;
        }
    </style>
</head>
<body>
    <div id="uk-cover">
        <p>
            <b>1. Виды изученности, на которые составлена учетная карточка по объекту работ</b>
        </p>
        <table>
            <tr>
                <td data-study-type="1">Геологическая</td>
                <td data-study-type="2">Геофизическая</td>
                <td data-study-type="3">Геохимическая</td>
                <td data-study-type="4">Инженерно-геологическая</td>
                <td data-study-type="5">Гидрогеологическая</td>
                <td data-study-type="6">Геоэкологическая</td>
            </tr>
        </table>
        <table class="no-border text-left br-margin8">
            <tr>
                <td>
                    <b>2. Хранилище отчета РГФ</b>
                    <span></span>
                </td>
                <td>
                    <b>3. Инвентарный номер отчета РГФ</b>
                    {% if data.данные_ргф %}
                        <span>{{ data.данные_ргф[0].инв_номер_отчета }}</span>
                    {% endif %}
                </td>
                <td>
                    <b>4. Инв. номер учетной карточки изученности РГФ</b>
                    {% if data.данные_ргф %}
                        <span>{{ data.данные_ргф[0].инв_номер_карточки_изуч }}</span>
                    {% endif %}
                </td>
            </tr>
        </table>
        <p>
            <b>5. Сведения о ТФГИ</b>
        </p>
        <table>
            <tr>
                <th>5.1 Название ТФГИ</th>
                <th>5.2 Инвентарный номер отчета ТФГИ</th>
                <th>5.3 Инв. номер учетной карточки изученности ТФГИ</th>
            </tr>
            {% for x in data.данные_тфги %}
                <tr>
                    <td>{{ x.ид_тфги }}</td>
                    <td>{{ x.инв_номер_отчета }}</td>
                    <td>{{ x.инв_номер_карточки_изуч }}</td>
                </tr>
            {% endfor %}
        </table>
        <p>
            <b>6. Авторы (соавторы)</b>
            <span>{{ data.отчет.авторы }}</span>
        </p>
        <p>
            <b>7. Название отчета</b>
            <span>{{ data.название_отчета }}</span>
        </p>
        <table class="no-border text-left br-margin8">
            <tr>
                <td>
                    <b>8. Организация-исполнитель</b>
                    <span>{{ data.отчет.организация_исполнитель }}</span>
                </td>
                <td>
                    <b>9. Недропользователь (заказчик работ)</b>
                    <span>{{ data.отчет.недропользователь }}</span>
                </td>
            </tr>
            <tr>
                <td>
                    <b>10. Источник финансирования</b>
                    <span>{{ data.отчет.источник_финансирования }}</span>
                </td>
                <td>
                    <b>11. Стоимость работ, руб.</b>
                    <span>{{ data.отчет.стоимость_работ }}</span>
                </td>
            </tr>
        </table>
        <table class="no-border text-left br-margin8">
            <tr>
                <td>
                    <b>12. Номер госрегистрации</b>
                    {% set lst = [] %}
                    {% for номер_гос_регистрации in data.отчет.номера_гос_регистрации %}
                        {{ lst.append(номер_гос_регистрации.номер) or '' }}
                    {% endfor %}
                    <span>{{ lst | join(', ')}}</span>
                </td>
                <td>
                    <b>13. Лицензии</b>
                    {% set lst = [] %}
                    {% for лицензия in data.отчет.лицензии %}
                        {{ lst.append(лицензия.серия) or '' }}
                    {% endfor %}
                    <span>{{ lst | join(', ')}}</span>
                </td>
                <td style="width: 55%">
                    <b>14. Номер и дата заключения экспертизы проектной документации</b>
                    {% set lst = [] %}
                    {% for экспертиза in data.отчет.экспертизы %}
                        {{ lst.append(экспертиза.номер ~ ' ' ~ date(экспертиза.дата)) or '' }}
                    {% endfor %}
                    <span>{{ lst | join(', ')}}</span>
                </td>
            </tr>
        </table>
        <table class="no-border text-left br-margin8">
            <tr>
                <td>
                    <b>15. Государственные (муниципальные) контракты</b>
                    {% set lst = [] %}
                    {% for гос_контракт in data.отчет.гос_контракты %}
                        {{ lst.append(гос_контракт.номер ~ ' ' ~ date(гос_контракт.дата)) or '' }}
                    {% endfor %}
                    <span>{{ lst | join(', ')}}</span>
                </td>
                <td>
                    <b>16. Государственные задания</b>
                    {% set lst = [] %}
                    {% for гос_задание in data.отчет.гос_задания %}
                        {{ lst.append(гос_задание.номер ~ ' ' ~ date(гос_задание.дата)) or '' }}
                    {% endfor %}
                    <span>{{ lst | join(', ')}}</span>
                </td>
            </tr>
        </table>

        <table class="no-border text-left no-break">
            <tr>
                <td style="width: 45%"><b>17. Сроки работ</b></td>
                <td style="width: 10px"></td>
                <td><b>18. Сведения о полезном ископаемом</b></td>
            </tr>
            <tr>
                <td>
                    <table class="text-center border">
                        <tr>
                            <th>17.1 Год, квартал начала работ</th>
                            <th>17.2 Год, квартал окончания работ</th>
                            <th>17.3 Год составления отчета</th>
                        </tr>
                        <tr>
                            <td>{{ data.отчет.год_начала_работ }} {{ data.отчет.квартал_начала_работ }}</td>
                            <td>{{ data.отчет.год_окончания_работ }} {{ data.отчет.квартал_окончания_работ }}</td>
                            <td>{{ data.отчет.год_составления_отчёта }}</td>
                        </tr>
                    </table>
                    <div>
                        <b>19. Административная привязка и общая площадь работ</b>
                    </div>
                    <div>
                        <b>19.1 Федеральный округ</b>
                        {# TODO федеральный_округ? #}
                        <span>{{ data.федеральный_округ }}</span>
                    </div>
                    <div>
                        <b>19.2. Субъект РФ</b>
                        <span>{{ ', '.join(data.отчет.субъекты) }}</span>
                    </div>
                    <div>
                        <b>19.3. Полный перечень номенклатур миллионных листов</b>
                        <span>{{ data.отчет.номенклатура }}</span>
                    </div>
                    <div>
                        <b>19.4 Общая площадь работ, кв.км</b>
                        <span>{{ data.отчет.общая_площадь_работ }}</span>
                    </div>
                </td>
                <td></td>
                <td>
                    <table class="text-center border">
                        <tr>
                            <th rowspan="2">18.1 Полезные ископаемые</th>
                            <th rowspan="2">18.2 Подсчет запасов</th>
                            <th rowspan="2">18.3 Государственная экспертиза запасов</th>
                            <th colspan="2">18.4 Протокол экспертизы запасов</th>
                        </tr>
                        <tr>
                            <td>Номер</td>
                            <td>Дата утверждения</td>
                        </tr>
                        {% for pi in data.отчет.ископаемые_запасы %}
                            {% if pi.n_pis == 1 %}
                                <tr>
                                    <td rowspan="{{ pi.n_protokols }}">{{ pi.ископаемое }}</td>
                                    <td rowspan="{{ pi.n_protokols }}">{{ 'Да' if pi.подсчет_запасов=='1' else 'Нет' }}</td>
                                    <td rowspan="{{ pi.n_protokols }}">{{ 'Да' if pi.экспертиза_запасов=='1' else 'Нет' }}</td>
                                    {% for i, protokol in enumerate(pi.протоколы) %}
                                        {% if i != 0 %}
                                            <tr>
                                        {% endif %}
                                        <td>{{ protokol.номер }}</td>
                                        <td>{{ protokol.дата }}</td>
                                        {% if i != 0 %}
                                            </tr>
                                        {% endif %}
                                    {% endfor %}
                                </tr>
                            {% else %}
                                <tr>
                                    <td>{{ pi.ископаемое }}</td>
                                    <td>{{ 'Да' if pi.подсчет_запасов=='1' else 'Нет' }}</td>
                                    <td>{{ 'Да' if pi.экспертиза_запасов=='1' else 'Нет' }}</td>
                                    {% if pi.n_pis > 1 %}
                                        <td rowspan="{{ pi.n_pis }}">{{ pi.протоколы[0].номер }}</td>
                                        <td rowspan="{{ pi.n_pis }}">{{ pi.протоколы[0].дата }}</td>
                                    {% endif %}
                                </tr>
                            {% endif %}
                        {% endfor %}
{#                    </table>                    #}
{#                    <table class="v-top">#}
                        {% set ns = namespace(count=False) %}
                        {% for pi in data.отчет.ископаемые_ресурсы %}
                            {% if pi.подсчет_ресурсов=='1' %}
                                {% set ns.count = True %}
                            {% endif %}
                        {% endfor %}
                        {% if ns.count %}
                            <tr>
                                <th rowspan="2">18.1 Полезные ископаемые</th>
                                <th rowspan="2">18.5 Оценка прогнозных ресурсов</th>
                                <th rowspan="2">18.6 Апробация прогнозных ресурсов</th>
                                <th colspan="2">18.7 Протокол апробации прогнозных ресурсов</th>
                            </tr>
                            <tr>
                                <td>Номер</td>
                                <td>Дата утверждения</td>
                            </tr>
                            {% for pi in data.отчет.ископаемые_ресурсы %}
                                {% if pi.подсчет_ресурсов=='1' %}
                                    {% if pi.n_pis == 1 %}
                                        <tr>
                                            <td rowspan="{{ pi.n_protokols }}">{{ pi.ископаемое }}</td>
                                            <td rowspan="{{ pi.n_protokols }}">{{ 'Да' if pi.подсчет_ресурсов=='1' else 'Нет' }}</td>
                                            <td rowspan="{{ pi.n_protokols }}">{{ 'Да' if pi.апробация_ресурсов=='1' else 'Нет' }}</td>
                                            {% for i, protokol in enumerate(pi.протоколы) %}
                                                {% if i != 0 %}
                                                    <tr>
                                                {% endif %}
                                                <td>{{ protokol.номер }}</td>
                                                <td>{{ protokol.дата }}</td>
                                                {% if i != 0 %}
                                                    </tr>
                                                {% endif %}
                                            {% endfor %}
                                        </tr>
                                    {% else %}
                                        <tr>
                                            <td>{{ pi.ископаемое }}</td>
                                            <td>{{ 'Да' if pi.подсчет_ресурсов=='1' else 'Нет' }}</td>
                                            <td>{{ 'Да' if pi.апробация_ресурсов=='1' else 'Нет' }}</td>
                                            {% if pi.n_pis > 1 %}
                                                <td rowspan="{{ pi.n_pis }}">{{ pi.протоколы[0].номер }}</td>
                                                <td rowspan="{{ pi.n_pis }}">{{ pi.протоколы[0].дата }}</td>
                                            {% endif %}
                                        </tr>
                                    {% endif %}
                                {% endif %}
                            {% endfor %}
                        {% endif %}
                    </table>
                </td>
            </tr>
        </table>
        <br>
        <table class="text-center">
            <tr>
                <th colspan="2">20. Государственное специализированное хранилище образцов геологических пород, керна</th>
            </tr>
            <tr>
                <th>20.1. Наименование, адрес хранилища</th>
                <th>20.2. Инвентарный номер (номера)</th>
            </tr>
            {% for x in data.отчет.гос_хранилища %}
                <tr>
                    <td>{{ x.хранилище }}</td>
                    <td>{{ x.инвентарный_номер }}</td>
                </tr>
            {% endfor %}
        </table>
        <p>
            <b>21. Целевое назначение</b>
            <span>{{ data.отчет.целевое_назначение }}</span>
        </p>
        <p>
            <b>22.1 Основные результаты, выводы и рекомендации</b>
            <span>{{ data.отчет.выводы }}</span>
        </p>

    </div>


</body>
</html>
