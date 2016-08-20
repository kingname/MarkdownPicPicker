import sys
import os
from configparser import ConfigParser


def read_config():
    _dict = {}
    if getattr(sys, 'frozen', None):
        config_path = os.path.join(os.path.dirname(sys.executable), 'config', 'config.ini')
    else:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')

    if not os.path.exists(config_path):
        print('can not find the config.ini, use the default sm uploader.'
              'attention: this website may breakdown in the future, only used temporarily.')
        _dict['picture_host'] = 'SmUploader'
        return _dict
    configs = ConfigParser()
    configs.read(config_path)
    _dict['picture_folder'] = configs['basic'].get('picture_folder', '')
    _dict['picture_suffix'] = configs['basic'].get('picture_suffix', '')
    _dict['picture_host'] = configs['basic'].get('picture_host', '')
    _dict['config_path'] = config_path

    if _dict['picture_host']:
        _dict['uploader_info'] = configs[_dict['picture_host']]

    return _dict


if __name__ == '__main__':
    print(read_config())
