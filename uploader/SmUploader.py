import requests
import json
import sys
import os

class Uploader(object):
    '''
    you can read this api at https://sm.ms/doc/
    after uploading, you will get a json:
    {
    "code": "success",
    "data": {
        width: 1157,
        height: 680,
        filename: "image_2015-08-26_10-54-48.png",
        storename: "56249afa4e48b.png",
        size: 69525,
        path: "/2015/10/19/56249afa4e48b.png",
        hash: "nLbCw63NheaiJp1",
        timestamp: 1445239546,
        url: "https://ooo.0o0.ooo/2015/10/19/56249afa4e48b.png",
        delete: "https://sm.ms/api/delete/nLbCw63NheaiJp1"
    }
    }
    and the url of this image's key is 'url'

    '''

    DEFAULT_URL = 'https://sm.ms/api/upload'

    def __init__(self, _=None):
        self.url = self.DEFAULT_URL

    def upload(self, picture_path, link_only=False):
        picture_file_handler = open(picture_path, 'rb')
        data = {'smfile': picture_file_handler}
        result_json = requests.post(self.url, files=data).content
        try:
            result_dict = json.loads(result_json.decode())
        except Exception as _:
            print('the result of the picture bed is not standard json.' )
            return None
        finally:
            picture_file_handler.close()
        pic_url = result_dict.get('data', {}).get('url', '')
        if pic_url:
            self.write_markdown_picture_url(pic_url, link_only)

    def write_markdown_picture_url(self, pic_url, link_only=False):
        if link_only:
            markdown_picture_url = pic_url
        else:
            markdown_picture_url = '![]({})'.format(pic_url)
        platform = sys.platform
        command = ''
        if platform == 'win32':
            command = 'echo {} | clip'.format(markdown_picture_url)
        elif platform == 'darwin':
            command = 'echo "{}" | pbcopy'.format(markdown_picture_url)
        os.system(command)
        print('the url is already in your clipboard!')

if __name__ == '__main__':
    uploader = Uploader({'url': 'https://sm.ms/api/upload'})
    uploader.upload('3.png')

