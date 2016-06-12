from PIL import ImageGrab, ImageFile
from configparser import ConfigParser
from uploader.QiniuUploader import QiniuUploader
import time
import sys
import os
try:
    import pythoncom
except ImportError:
    print('maybe you have not install pywin32 or not in windows system.')
    pythoncom = None
try:
    import pyHook
except ImportError:
    print('maybe you have not install pyHook.')
    pyHook = None

ImageFile.LOAD_TRUNCATED_IMAGES = True

__version__ = '0.2.1'
__author__ = 'kingname'


class MarkrdownPicPicker(object):

    CONFIG_PATH = 'config.ini'

    def __init__(self, link_only=False):

        self.method = ''
        self.picture_folder = ''
        self.picture_suffix = ''
        self.picture_bed = ''
        self.short_key_one = ''
        self.short_key_two = ''
        self.key_one = False
        self.key_two = False
        self.uploader = None
        self.link_only = link_only

        self.init_environment()

        if self.method == 'bat':
            self.upload_picture()
        elif self.method == 'global_listen':
            self.keyboard_listen()

    def init_environment(self):
        self.read_config()
        if not self.method \
                or not self.picture_folder \
                or not self.picture_suffix \
                or not self.picture_bed:
            print('there must be something wrong in config, please check.')
            exit()
        if not os.path.exists(self.picture_folder):
            os.makedirs(self.picture_folder)

    def read_config(self):
        configs = ConfigParser()
        if not os.path.exists(self.CONFIG_PATH):
            print('can not find the config.ini, exit')
            exit()
        configs.read(self.CONFIG_PATH)
        self.method = configs['basic'].get('run_method', '')
        self.picture_folder = configs['basic'].get('picture_folder', '')
        self.picture_suffix = configs['basic'].get('picture_suffix', '')
        self.picture_bed = configs['basic'].get('picture_bed', '')

        if self.picture_bed:
            self.uploader = QiniuUploader(configs['qiniu'])

        if self.method == 'global_listen':
            self.short_key_one = configs['global_listen']['short_key_one']
            self.short_key_two = configs['global_listen']['short_key_two']

    def keyboard_listen(self):
        if not pythoncom or not pyHook:
            print('as pythoncom or pyHook is not exists, please use bat method.')
            exit()
        if not self.short_key_one or not self.short_key_two:
            print('there must be something wrong in the config, please check.')
            exit()
        hm = pyHook.HookManager()
        hm.KeyDown = self.keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()

    def keyboard_event(self, event):
        if event.Key == self.short_key_one and not self.key_one:
            self.key_one = True
        elif event.Key == self.short_key_two and not self.key_two:
            self.key_two = True
        if self.key_one and self.key_two:
            self.upload_picture()
            self.key_one = False
            self.key_two = False
        return True

    def upload_picture(self):
        picture_path, picture_name = self.save_picture()
        if not picture_path:
            return False
        else:
            self.uploader.upload(picture_path, picture_name)
            self.uploader.write_markdown_picture_url(picture_name, link_only=True if self.link_only else False)
            return True

    def save_picture(self):
        date_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        picture_name = date_time + '.' + self.picture_suffix
        picture_path = os.path.join(self.picture_folder, picture_name)
        try:
            picture_data = ImageGrab.grabclipboard()
            if picture_data:
                picture_data.save(picture_path, self.picture_suffix)
                return picture_path, picture_name
            else:
                print('there is no picture in clipboard!')
        except Exception as e:
            print('get picture from clipboard error because: {}'.format(e))
        return '', ''

if __name__ == '__main__':
    arg = sys.argv[-1]
    if arg == '-linkonly':
        MarkrdownPicPicker(link_only=True)
    else:
        MarkrdownPicPicker()
