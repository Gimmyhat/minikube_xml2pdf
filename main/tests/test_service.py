import glob
import os
import requests
import sys
sys.path.append('../main')
import lib

cfg = lib.cfg()
test_files = glob.glob(lib.cfg('service').data_dir + '/xml/*.xml')
for file in test_files:
    print('Processing ' + file)
    res = requests.post(cfg.url,
                        data={'xml': open(file).read()},
                        auth=requests.auth.HTTPBasicAuth(cfg.user, cfg.pwd))
    if not res.ok:
        raise Exception(res.text)
    open(os.path.basename(file).replace('.xml', '.pdf'), 'wb').write(res.content)
