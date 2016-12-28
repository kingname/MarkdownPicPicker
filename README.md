# MarkdownPicPicker

## Introduce

MarkdownPicPicker is an assistant which can help you add picture in Markdown. It will upload the image in your clipboard to web picture host and copy the Markdown-format link(\!\[\]\(url\)) to your clipboard or pasteboard. Now it supports Windows and Mac OS.

![Preview of MarkdownPicPicker](https://raw.githubusercontent.com/kingname/MarkdownPicPicker/master/screenshots/MarkdownPicPickerPrew.gif)

## Function

Version 1.1.0 can do：

1. Picture host support Qiniu and SM.MS.
2. You can use it as soon as you download it without any config.
3. Through config, you can add your own picture host uploader.
4. Picture will be saved to local first.
3. Copy the Markdown-format link to clipboard or pasteboard.
5. Easy to add your own uploader.

## How to use

### Windows
1. Download MarkdownPicPicker at:[https://github.com/kingname/MarkdownPicPicker/releases/download/v1.0.0/MarkdownPicPicker_v1.0.0.zip](https://github.com/kingname/MarkdownPicPicker/releases/download/v1.0.0/MarkdownPicPicker_v1.0.0.zip)
2. Copy image into clipboard
3. Run MarkdownPicPicker.exe

### Mac OS
1. Install pngpaste: `brew install pngpaste`
2. Clone MarkdownPicPicker source code
3. Copy image into pasteboard
4. `python MarkdownPicPicker.py`

## Config

### Use Qiniu web host

If there is not a config, MarkdownPicpicker will use SM.SM as the default picture host. But this website may breakdown in the future and your data maybe unsafe. If you want to use Qiniu web host, please create a folder called `config` and write the config.ini like follow:

Please Create/Edit `config/config.ini`, every item in it means：
```ini
[basic]
picture_folder = pic # necessary, the local folder to save a copy of image
picture_suffix = png #necessary, the format of your image, 'png' only

picture_host = QiniuUploader 

[QiniuUploader]
access_key = Q6sS422O05AasdfasfafgfCcCpF36tqvyQ75Zvzw
secret_key = 6QtAqqTxoSadffadfgewehxPLX2CCmoOaB2aLObM
container_name = picturebed
url = http://7sbpmp.com1.z0.glb.clouddn.com/{}
```

Notice: please remove the comments in `config.ini`.

In the config, `access_key` and `secret_key` can be found in Qiniu's controlpanel：
![](http://7sbpmp.com1.z0.glb.clouddn.com/20160605083025.png) 
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-22-43.png) 


`container_name` means：
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-24-40.png) 

### Only copy url

If you want to copy the url of image only instead of \!\[\]\(url\)， you can use parameter: `-linkonly` :
```
markdownpicpicker.exe -linkonly

or 

python MarkdownPicPicker.py -linkonly
```

I recommand you to use AutoHotKey to launch MarkdownPicPicker。In this way, the time of add an image can be less than 2 seconds. My AutoHotKey config is：

![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-07-16-11-54-13.png) 

What you need to do is:

* Copy image.
* Press the short key.
* Paste the Markdown format url in your article.

## Develop your own uploader
Now MarkdownPicPicker only support [Qiniu](http://www.qiniu.com/) and [SM.MS](https://sm.ms/). For different countries, there must be more brilliant picture hosts. I hope you can help me add more picture host uploaders, and submit PR to me. It is really very easy but helpful。

### Rules：

* Put your uploader in the `uploader` folder, file name is unlimited, for example:`ExampleUploader.py`
* The class name **must** be `Uploader`
* If the picture host need token or other parameters, please add a parameter called `config_info` in \_\_init\_\_, every parameters in your config will be sent to here in the type of `dict`。
```
def __init__(self, config_info=None):
    self.token = config_info['token']
    self.username = config_info['username']
    self.password = config_info['password']
    self.url = config_info['url']
```
* There must be a method called `upload`, there parameter `picture_path` is the local path of the file：
```
def upload(self, picture_path, link_only=False)
```
* Edit config/config.ini, add the parameters of your own uploader, the Section is your uploader's filename without `.py`, and the `picture_host` in `[basic]` is the Section, for example：
```
[basic]
picture_folder = pic
picture_suffix = png
picture_host = ExampleUploader

[ExampleUploader]
token = 123456
username = xxx
password = yyy
url = http://xxx.xxx/upload
```

## Attention
If you want to use the source code to run MarkdownPicPicker in Windows, please pay attention to follow problem:

### Fix Pillow bug
Windows version use Pillow's method `ImageGrab.grabclipboard()`  to get the image in clipboard, but there is a official bug, this bug will cause this error:
```
Unsupported BMP bitfields layout
```
This bug begin from Pillow 2.8.0 and it is not fixed until Pillow 3.2.0. Here I will tell you how to fix this bug:
Please open \<path to your Python\>\Lib\site-packages\PIL\BmpImagePlugin.py there should be these codes：

```
if file_info['bits'] in SUPPORTED:
    if file_info['bits'] == 32 and file_info['rgba_mask'] in SUPPORTED[file_info['bits']]:
        raw_mode = MASK_MODES[(file_info['bits'], file_info['rgba_mask'])]
        self.mode = "RGBA" if raw_mode in ("BGRA",) else self.mode
    elif file_info['bits'] in (24, 16) and file_info['rgb_mask'] in SUPPORTED[file_info['bits']]:
        raw_mode = MASK_MODES[(file_info['bits'], file_info['rgb_mask'])]
    else:
        raise IOError("Unsupported BMP bitfields layout")
else:
    raise IOError("Unsupported BMP bitfields layout")
```

change them to：
```
if file_info['bits'] in SUPPORTED:
    if file_info['bits'] == 32 and file_info['rgba_mask'] in SUPPORTED[file_info['bits']]:
        raw_mode = MASK_MODES[(file_info['bits'], file_info['rgba_mask'])]
        self.mode = "RGBA" if raw_mode in ("BGRA",) else self.mode
    elif file_info['bits'] in (24, 16) and file_info['rgb_mask'] in SUPPORTED[file_info['bits']]:
        raw_mode = MASK_MODES[(file_info['bits'], file_info['rgb_mask'])]
    '''the code to add begin'''
    elif file_info['bits'] == 32 and file_info['rgb_mask'] == (0xff0000, 0xff00, 0xff):
        pass
    '''the code to add end'''
    else:
        raise IOError("Unsupported BMP bitfields layout")
else:
    raise IOError("Unsupported BMP bitfields layout")
```

## TODO
* More screenshots
* Save image from pasteboard without pngpaste
* More Picture web host
* Hide the terminal windows
* Linux Usable

## Thanks to
[laixintao](https://github.com/laixintao)

