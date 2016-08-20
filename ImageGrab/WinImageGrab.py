import os
import time
from PIL import ImageGrab, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True


class WinImageGrab(object):
    def __init__(self, picture_folder, picture_suffix):
        self.picture_folder = picture_folder
        self.picture_suffix = picture_suffix

    def save_picture(self):
        date_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        picture_name = date_time + '.' + self.picture_suffix
        picture_path = os.path.join(self.picture_folder, picture_name)
        try:
            picture_data = ImageGrab.grabclipboard()
            if picture_data:
                picture_data.save(picture_path, self.picture_suffix)
                return picture_path
            else:
                print('there is no picture in clipboard!')
        except Exception as e:
            print('get picture from clipboard error because: {}'.format(e))
        return ''
