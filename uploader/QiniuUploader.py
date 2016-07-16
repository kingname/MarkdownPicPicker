from qiniu import Auth, put_file
import os


class QiniuUploader(object):
    def __init__(self, config_info):
        self.upload_handler = None
        self.url = config_info['url']
        self.container_name = config_info.get('container_name')
        self.upload_handler = Auth(config_info.get('access_key'), config_info.get('secret_key'))

    def upload(self, picture_path, picture_name):
        if self.upload_handler:
            token = self.upload_handler.upload_token(self.container_name, picture_name, 3600)
            info = put_file(token, picture_name, picture_path)
            print(info)

    def write_markdown_picture_url(self, picture_name, link_only=False):
        if link_only:
            markdown_picture_url = self.url.format(picture_name)
        else:
            markdown_picture_url = '![]({})'.format(self.url.format(picture_name))
        command = 'echo {} | clip'.format(markdown_picture_url)
        os.system(command)
