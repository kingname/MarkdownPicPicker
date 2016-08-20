import sys, os
from configparser import ConfigParser


def read_config():
    _dict = {}
    if getattr(sys, 'frozen', None):
        config_path = os.path.join(os.path.dirname(sys.executable), 'config.ini')
    else:
        config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')
    print(config_path)
    configs = ConfigParser()
    if not os.path.exists(config_path):
        print('can not find the config.ini, exit')
        exit()
    configs.read(config_path)
    _dict['method'] = configs['basic'].get('run_method', '')
    _dict['picture_folder'] = configs['basic'].get('picture_folder', '')
    _dict['picture_suffix'] = configs['basic'].get('picture_suffix', '')
    _dict['picture_bed'] = configs['basic'].get('picture_bed', '')

    if _dict['picture_bed']:
        _dict['uploader_info'] = configs['qiniu']

    if _dict['method'] == 'global_listen':
        _dict['short_key_one'] = configs['global_listen']['short_key_one']
        _dict['short_key_two'] = configs['global_listen']['short_key_two']

    return _dict


if __name__ == '__main__':
    print(read_config())
