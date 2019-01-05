import requests
import json
import sys
import os
import base64


class Uploader(object):
    '''
    you can read this api at https://chevereto.com/docs/api-v1
    after uploading, you will get a json:
{
		"status_code": 200,
		"success": {
			"message": "image uploaded",
			"code": 200
		},
		"image": {
			"name": "example",
			"extension": "png",
			"size": 53237,
			"width": 1151,
			"height": 898,
			"date": "2014-06-04 15:32:33",
			"date_gmt": "2014-06-04 19:32:33",
			"storage_id": null,
			"description": null,
			"nsfw": "0",
			"md5": "c684350d722c956c362ab70299735830",
			"storage": "datefolder",
			"original_filename": "example.png",
			"original_exifdata": null,
			"views": "0",
			"id_encoded": "L",
			"filename": "example.png",
			"ratio": 1.2817371937639,
			"size_formatted": "52 KB",
			"mime": "image/png",
			"bits": 8,
			"channels": null,
			"url": "http://127.0.0.1/images/2014/06/04/example.png",
			"url_viewer": "http://127.0.0.1/image/L",
			"thumb": {
				"filename": "example.th.png",
				"name": "example.th",
				"width": 160,
				"height": 160,
				"ratio": 1,
				"size": 17848,
				"size_formatted": "17.4 KB",
				"mime": "image/png",
				"extension": "png",
				"bits": 8,
				"channels": null,
				"url": "http://127.0.0.1/images/2014/06/04/example.th.png"
			},
			"medium": {
				"filename": "example.md.png",
				"name": "example.md",
				"width": 500,
				"height": 390,
				"ratio": 1.2820512820513,
				"size": 104448,
				"size_formatted": "102 KB",
				"mime": "image/png",
				"extension": "png",
				"bits": 8,
				"channels": null,
				"url": "http://127.0.0.1/images/2014/06/04/example.md.png"
			},
			"views_label": "views",
			"display_url": "http://127.0.0.1/images/2014/06/04/example.md.png",
			"how_long_ago": "moments ago"
		},
		"status_txt": "OK"
	}
    and the url of this image's key is 'image','url'

    '''


    def __init__(self, config_info):
        self.url = config_info['url']
        self.key = config_info['secret_key']
        self.container_name = config_info.get('container_name')

    def tobase64(self,filename):
        with open(filename, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        return encoded_string

    def upload(self, picture_path_list, link_only=False):
        success_uploaded_list = []
        for picture_path in picture_path_list:
            picture_file_handler = self.tobase64(picture_path)
            data = {
                "source":picture_file_handler,
                "action":"upload",
                "key":self.key
                }
            result_json = requests.post(self.url, data=data).content
            try:
                result_dict = json.loads(result_json.decode())
            except Exception as _:
                print('the result of the picture bed is not standard json.' )
                return None
            pic_url = result_dict.get('image',{}).get('url','')
            if pic_url:
                success_uploaded_list.append(pic_url)
        self.write_markdown_picture_url(success_uploaded_list, link_only)

    def write_markdown_picture_url(self, pic_url_list, link_only=False):
        if link_only:
            markdown_picture_url = '\n'.join(pic_url_list)
        else:
            markdown_picture_url_list = []
            for pic_url in pic_url_list:
                markdown_picture_url = '![]({})'.format(pic_url)
                markdown_picture_url_list.append(markdown_picture_url)
            markdown_picture_url = '\n'.join(markdown_picture_url_list)
        platform = sys.platform
        command = ''
        if platform == 'win32':
            command = 'echo {} | clip'.format(markdown_picture_url)
        elif platform == 'darwin':
            command = 'echo "{}" | pbcopy'.format(markdown_picture_url)
        os.system(command)
        print('the url is already in your clipboard!')

if __name__ == '__main__':
    config_info = {
        'url': 'http://test/1/upload',
        'secret_key': '32daf23makjdeb'
    }
    uploader = Uploader(config_info)
    uploader.upload(['1.jpg'])

