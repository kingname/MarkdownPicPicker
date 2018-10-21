# -*- coding=utf-8
from qcloud_cos import CosConfig, CosS3Client
import sys
import os

class Uploader(object):
    def __init__(self, config_info):
        self.region = config_info.get('region')
        self.config = CosConfig(Region=self.region,
                                SecretId=config_info.get('secret_id'),
                                SecretKey=config_info.get('secret_key'))
        self.client = CosS3Client(self.config)
        self.bucket = config_info.get('bucket')
        self.url = 'https://'+self.bucket+'.cos.'+self.region+'.myqcloud.com/{}'
        
        
    def upload(self, picture_path_list, link_only=False):
        for picture_path in picture_path_list:
            print(picture_path)
            picture_name = os.path.basename(picture_path)
            with open(picture_path, 'rb') as fp:
                response = self.client.put_object(Bucket=self.bucket,
                                                Body=fp,
                                                Key=picture_name)
            print(response['ETag'])
            self.write_markdown_picture_url(picture_path_list, link_only)

    def write_markdown_picture_url(self, picture_path_list, link_only=False):
        uploaded_url_list = []
        for picture_path in picture_path_list:
            picture_name = os.path.basename(picture_path)
            if link_only:
                markdown_picture_url = self.url.format(picture_name)
                uploaded_url_list.append(markdown_picture_url)
            else:
                markdown_picture_url = '![]({})'.format(self.url.format(picture_name))
                uploaded_url_list.append(markdown_picture_url)
        platform = sys.platform
        command = ''
        if platform == 'win32':
            command = 'echo {} | clip'.format('\n'.join(uploaded_url_list))
        elif platform == 'darwin':
            command = 'echo "{}" | pbcopy'.format('\n'.join(uploaded_url_list))
        os.system(command)
        print('the url is already in your clipboard!')

if __name__ == '__main__':
    config_info = {
        "secret_id": "",
        "secret_key": "",
        "region": "",
        "bucket": ""
    }
    uploader = Uploader(config_info)
    uploader.upload(['fire.png'])