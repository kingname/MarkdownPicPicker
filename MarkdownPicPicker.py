from PIL import ImageGrab, ImageFile
from qiniu import Auth, put_file
import time
import os
ImageFile.LOAD_TRUNCATED_IMAGES = True

class MarkrdownPicPicker(object):

    PICTURE_FOLDER = 'pic'
    PICTURE_SUFFIX = 'png'
    ACCESS_KEY = 'Q6sS422O05Aw34523M3FqCcCpF36tqvyQ75Zvzw'
    SECRET_KEY = '6QtAqqTxoSxZP-25643hhxPLX2CCmoOaB2aLObM'
    CONTAINER_NAME = 'picturebed'
    URL = 'http://7sbpmp.com1.z0.glb.clouddn.com/{}'
    
    def __init__(self):
        self.upload_handler = None
        self.init_environment()
        self.upload_picture()

    def init_environment(self):
        if not os.path.exists(self.PICTURE_FOLDER):
            os.makedirs(self.PICTURE_FOLDER)

        self.upload_handler = Auth(self.ACCESS_KEY, self.SECRET_KEY)


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
            picture_data.save(picture_path, self.PICTURE_SUFFIX)
            return (picture_path, picture_name)
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

