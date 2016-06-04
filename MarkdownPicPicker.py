from PIL import ImageGrab, ImageFile
from qiniu import Auth, put_file
import pythoncom
import pyHook
import time
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

__version__ = 0.1
__author__ = 'kingname'

class MarkrdownPicPicker(object):

    METHOD = 'bat'
    PICTURE_FOLDER = 'pic'
    PICTURE_SUFFIX = 'png'
    ACCESS_KEY = 'Q6sS422O05Aw345235M3FqCcCpF36tqvyQ75Zvzw'
    SECRET_KEY = '6QtAqqTxoSxZP-2uo23455X2CCmoOaB2aLObM'
    CONTAINER_NAME = 'picturebed'
    URL = 'http://7sbpmp.com1.z0.glb.clouddn.com/{}'

    SHORT_KEY_ONE = 'Lwin'
    SHORT_KEY_TWO = 'C'

    def __init__(self):
        self.upload_handler = None
        self.key_one = False
        self.key_two = False
        self.init_environment()
        '''
        there are some bugs in pyHook, if a windows name is Unicode, it will make
        python crash. wait until pyHook is fixed up.
        '''
        if self.METHOD = 'bat'
            self.upload_picture()
        elif self.METHOD = 'pyHook':
            self.keyboard_listen

    def init_environment(self):
        if not os.path.exists(self.PICTURE_FOLDER):
            os.makedirs(self.PICTURE_FOLDER)

        self.upload_handler = Auth(self.ACCESS_KEY, self.SECRET_KEY)

    def keyboard_listen(self):
        hm = pyHook.HookManager()
        hm.KeyDown = self.keyboard_event
        hm.HookKeyboard()
        pythoncom.PumpMessages()

    def keyboard_event(self, event):
        if event.Key == self.SHORT_KEY_ONE and not self.key_one:
            self.key_one = True
        elif event.Key == self.SHORT_KEY_TWO and not self.key_two:
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
            self.upload(picture_path, picture_name)
            self.write_markdown_picture_url(picture_name)

    def save_picture(self):
        date_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        picture_name = date_time + '.' + self.PICTURE_SUFFIX
        picture_path = os.path.join(self.PICTURE_FOLDER, picture_name)
        try:
            picture_data = ImageGrab.grabclipboard()
            if picture_data:
                picture_data.save(picture_path, self.PICTURE_SUFFIX)
                return (picture_path, picture_name)
            else:
                print('there is no picture in clipboard!')
        except Exception as e:
            print('get picture from clipboard error because: {}'.format(e))
        return ('', '')

    def upload(self, picture_path, picture_name):
        if self.upload_handler:
            token = self.upload_handler.upload_token(self.CONTAINER_NAME, picture_name, 3600)
            info = put_file(token, picture_name, picture_path)
            print(info)

    def write_markdown_picture_url(self, picture_name):
        markdown_picture_url = '![]({})'.format(self.URL.format(picture_name))
        command = 'echo {} | clip'.format(markdown_picture_url)
        os.system(command)

if __name__ == '__main__':
    MarkrdownPicPicker()
