import untangle
import sys
from pprint import pprint
import deepdiff
sys.path.append('../main')
import lib
import xml_to_pdf

print('-'*30)
src_types = xml_to_pdf.src_types()
# src_types = ['pgi']
for src_type in src_types:
    print(src_type)
    data_cfg = lib.cfg(src_type + '/' + src_type)

    xml_file = '../main/tests/data/' + data_cfg.test_file
    xml_data = xml_to_pdf.xml_to_data(src_type, xml_file)
    if 'maps' in xml_data:
        del xml_data.maps

    test_data = xml_to_pdf.test_data_from_cfg(src_type)

    if test_data!=xml_data:
        # print('xml', '-'*10)
        # pprint(xml_data.отчет.интерпретированные_данные)
        # print('test', '-'*10)
        # pprint(test_data.отчет.интерпретированные_данные)
        # print('-'*10)
        # stop
        pprint(deepdiff.DeepDiff(test_data, xml_data))
        stop
    else:
        print('OK!')



