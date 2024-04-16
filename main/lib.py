import os
import yaml

class dict_(dict):

    def __init__(self, *args, **kwargs):
        super(dict_, self).__init__(*args, **kwargs)
        for name,item in self.items():
            if isinstance(item,dict):
                self[name] = dict_(item)
            if isinstance(item,list):
                for ilist,listitem in enumerate(item):
                    if isinstance(listitem,dict):
                        item[ilist]=dict_(listitem)
        self.__dict__ = self

def cfg(name):

    with open(main_dir() + '/cfg/%s.cfg' % name) as f:
        cfg = dict_(yaml.safe_load(f))
    uniq_file = main_dir() + '/cfg/%s__uniq.cfg' % name
    if os.path.exists(uniq_file):
        with open(uniq_file) as f:
            cfg.update(yaml.safe_load(f))
    docker_file = main_dir() + '/cfg/%s__docker.cfg' % name
    if os.path.exists(docker_file):
        with open(docker_file) as f:
            cfg.update(yaml.safe_load(f))

    return dict_(cfg)

def main_dir():

    return os.path.dirname(os.path.abspath(__file__)) + '/'

def get_xml_attr(xml, attr):

    attr = attr.replace(':', '_')
    xml_ = xml
    for subattr in attr.split('/'):
        xml_ = getattr(xml_, subattr, None)
        if xml_ is None:
            return None

    return xml_

def get_xml_value(xml, attr, expected_type=str):

    attr = attr.replace(':', '_')
    xml_ = xml
    for subattr in attr.split('/'):
        xml_ = getattr(xml_, subattr, None)
        if xml_ is None:
            if expected_type == list:
                return []
            else:
                return None

    if expected_type == str:
        return xml_.cdata
    elif expected_type == list:
        if isinstance(xml_, list):
            return xml_
        else:
            return [xml_]
    else:
        raise Exception('Unknown expected type')

def russian_date(iso_date):

    if len(iso_date) == 10 and iso_date[4] == '-' and iso_date[7] == '-':
        return iso_date[8:] + '.' + iso_date[5:7] + '.' + iso_date[:4]
    else:
        return iso_date



