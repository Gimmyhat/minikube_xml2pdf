import sys, glob, subprocess
sys.path.append('../main')
import xml_to_pdf

test_files = glob.glob(lib.cfg('service').data_dir + '/xml/*.xml')
src_types = xml_to_pdf.src_types()
# src_types = ['izuch']
for src_type in src_types:
    for file in test_files:
        cmd = 'ipython ../main/xml_to_pdf.py %s %s test.pdf' % (src_type, file)
        print('-'*40)
        print(cmd)
        print('-'*40)
        subprocess.check_call(cmd, shell=True)
