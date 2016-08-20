import os
import time


class OSXGrab(object):
    def __init__(self, picture_folder, picture_suffix):
        self.picture_folder = picture_folder
        self.picture_suffix = picture_suffix

    def save_picture(self):
        date_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        picture_name = date_time + '.' + self.picture_suffix
        picture_path = os.path.join(self.picture_folder, picture_name)
        try:
            os.system('/usr/local/bin/pngpaste {}'.format(picture_path))
            if os.path.exists(picture_path):
                print('get image from pasteboard success.')
                return picture_path
            else:
                print('there is no picture in clipboard!')
        except Exception as e:
            print('get picture from clipboard error because: {}'.format(e))
        return ''

if __name__ == '__main__':
    OSXGrab('.', 'png').save_picture()