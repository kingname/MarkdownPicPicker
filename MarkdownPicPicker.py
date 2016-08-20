from ImageGrab import ImageGrab
from uploader.SmUploader import Uploader
import sys
import os
try:
    from config import read_config
except Exception as _:
    print('read config error, use default info.')
    read_config = None

__version__ = '1.1.0'
__author__ = 'kingname'


class MarkrdownPicPicker(object):

    def __init__(self, link_only=False):
        self.cwd = ''
        self.picture_folder = 'pic'
        self.picture_suffix = 'png'
        self.picture_host = ''
        self.uploader = None
        self.link_only = link_only
        self.config_path = ''
        self.uploader_info = {}
        self.imageGrab = None
        self.init_environment()

        self.upload_picture()

    def _to_string(self):
        """
        To test if the config reading is ok
        :return: None
        """
        print("folder", self.picture_folder)
        print("suffix", self.picture_suffix)
        print("picture_host", self.picture_host)

    def init_environment(self):
        if not read_config:
            self.uploader = Uploader()
        else:
            self.__dict__.update(read_config())
            self.cwd = os.path.dirname(os.path.dirname(self.config_path))

            uploader_list = self._find_uploader()
            if self.picture_host and self.picture_host in uploader_list:
                self.uploader = __import__('uploader.' + self.picture_host,
                                           globals(), locals(), ['Uploader'], 0).Uploader(self.uploader_info)

        if not os.path.exists(self.picture_folder):
            os.makedirs(self.picture_folder)
        self.imageGrab = ImageGrab(self.picture_folder, self.picture_suffix) if ImageGrab else None
        if not self.imageGrab:
            print('can not find image grab, exit.')
            exit()

    def upload_picture(self):
        picture_path = self.imageGrab.save_picture()
        if not picture_path:
            return False
        else:
            self.uploader.upload(picture_path, link_only=True if self.link_only else False)
            return True

    def _find_uploader(self):
        uploader_folder = os.path.join(self.cwd, 'uploader')
        if os.path.isdir(uploader_folder):
            uploader_list = [uploader_file.split('.')[0] for uploader_file in os.listdir(uploader_folder)]
            if uploader_list:
                return uploader_list

        print('can not find the uploader folder.')
        exit()

if __name__ == '__main__':
    arg = sys.argv[-1]
    if arg == '-linkonly':
        MarkrdownPicPicker(link_only=True)
    else:
        MarkrdownPicPicker()
