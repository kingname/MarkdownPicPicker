# MarkdownPicPicker

## 项目介绍

MarkdownPicPicker 是一个Markdown写作辅助工具。它能将剪贴板中的图片上传到网络图床中，并将markdown格式的图片链接(\!\[\]\(<图片地址>\))复制到剪贴板中。

## 功能介绍
第0.1版有以下功能：

1. 使用七牛云作为图床。
2. 将图片保存在本地
3. 图片上传成功后将Markdown格式的图片地址保存到剪贴板中
4. 全局监听键盘

## 使用方法

### 配置

以下部分需要做对应的修改：

```
METHOD = 'bat' #设定程序的运行方式，bat为使用bat文件触发，pyHook为全局键盘监听方式
PICTURE_FOLDER = 'pic' #截图的本地保存文件夹，可以根据实际情况修改。
PICTURE_SUFFIX = 'png' #截图的保存格式，可以选择bmp或者png

#以下两行来自于七牛云
ACCESS_KEY = 'Q6sS422O05Aw34523M3FqCcCpF36tqvyQ75Zvzw' 
SECRET_KEY = '6QtAqqTxoSxZP-25643hhxPLX2CCmoOaB2aLObM'

CONTAINER_NAME = 'picturebed' #七牛云的图片储存位置
URL = 'http://7sbpmp.com1.z0.glb.clouddn.com/{}' #七牛云分配的默认域名

SHORT_KEY_ONE = 'Lwin' #快捷键第一个按键
SHORT_KEY_TWO = 'C' #快捷键第二个按键
```

其中`ACCESS_KEY` 和 `SECRET_KEY` 可以在七牛云的控制面板中看到，如图：
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-21-59.png) 
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-22-43.png) 

`CONTAINER_NAME` 为下图所示内容：
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-24-40.png) 

`SHORT_KEY_ONE` 和 `SHORT_KEY_TWO` 为快捷键的两个按键，默认为左侧windows徽标键(`Lwin`) 和 字母 `C`。

### 使用

将程序配置好以后运行，创建一个批处理文件markdownpicpicker.bat, 其内容如下：
```
@echo off
cmd /k "G:\github\MarkdownPicPicker\venv\Scripts\activate & cd /d G:\github\MarkdownPicPicker & python MarkdownPicPicker.py & deactivate & exit"
```
路径请根据实际情况修改。

由于我使用了virtualenv, 所以需要在批处理中进入virtualenv的环境才能正常运行程序。对于将requirements.txt里面包含的库直接安装在全局的情况，bat 可以简化：

```
@echo off
cmd /k "cd /d <MarkdownPicPicker.py脚本所在路径> & python MarkdownPicPicker.py & exit"
```

然后右键选择批处理，发送到桌面快捷方式。接着右键快捷方式，属性，在“快捷键” 这一栏按下字母Q，它将自动填充为 `Ctrl + Alt + Q`, 确定。

![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-05-00-45-03.png) 

只需要首先使用QQ截图或者其他截图工具将图片保存到剪贴板中，然后按下设定好的快捷键即可。Markdown格式的图片链接就已经保存到剪贴板中了。在需要使用的地方直接粘贴。

不过这样设定的快捷键，按下以后会有大概一秒钟的延迟。推荐大家使用AutoHotKey来触发这个bat文件。

## 说明

### Pillow bug修正
本程序使用了Pillow库中的 `ImageGrab.grabclipboard()` 方法来获取剪贴板中的数据，但是由于这个方法有一个bug, 导致可能会爆以下错误：
```
Unsupported BMP bitfields layout
```
这个问题从Pillow 2.8.0开始，一直到3.2.0都没有被官方解决。目前有一个间接的解决办法。
请打开Python安装目录下的\Lib\site-packages\PIL\BmpImagePlugin.py文件，将以下代码：

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

修改为：
```
if file_info['bits'] in SUPPORTED:
    if file_info['bits'] == 32 and file_info['rgba_mask'] in SUPPORTED[file_info['bits']]:
        raw_mode = MASK_MODES[(file_info['bits'], file_info['rgba_mask'])]
        self.mode = "RGBA" if raw_mode in ("BGRA",) else self.mode
    elif file_info['bits'] in (24, 16) and file_info['rgb_mask'] in SUPPORTED[file_info['bits']]:
        raw_mode = MASK_MODES[(file_info['bits'], file_info['rgb_mask'])]
    '''新增内容开始'''
    elif file_info['bits'] == 32 and file_info['rgb_mask'] == (0xff0000, 0xff00, 0xff):
        pass
    '''新增内容结束'''
    else:
        raise IOError("Unsupported BMP bitfields layout")
else:
    raise IOError("Unsupported BMP bitfields layout")
```
就能解决本问题。

### 全局键盘监听

本程序还有一个功能是全局监听键盘，通过特殊的快捷键组合就可以直接触发读取图片上传图片的操作。但是由于这个功能使用到了pyHook这个库。这个库在设计上存在缺陷，如果当前窗体的标题包含Unicode字符时，会导致Python崩溃。因此这个功能默认不启动。

### 获取键盘按键

如果不清楚某个键盘按键对应的字符串是什么样子的，可以运行QueryKey.py这个文件，运行以后按下某个键，控制台上就会显示相应的信息。其中`Key`就是可以设置到`SHORT_KEY_ONE`和`SHORT_KEY_TWO`的内容。如图为按下键盘左Shift键以后显示的信息。
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-23-14-30.png) 

## TODO
* 支持更多的截图方式
* 支持更多的图床
* 窗口隐藏
* 解决pyHook的问题
* 适配Linux 和 Mac OS

