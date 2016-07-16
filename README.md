# MarkdownPicPicker

## 项目介绍

MarkdownPicPicker 是一个Markdown写作辅助工具。它能将剪贴板中的图片上传到网络图床中，并将markdown格式的图片链接(\!\[\]\(<图片地址>\))复制到剪贴板中。

## 功能介绍

第0.2.2版有以下功能：

1. 使用七牛云作为图床。
2. 将图片保存在本地
3. 图片上传成功后将Markdown格式的图片地址保存到剪贴板中
4. 全局监听键盘(默认不开启)
5. 独立配置文件

## 使用方法

### 配置

配置文件保存在`config.ini`文件中，其意义分别如下：
```ini
[basic]
run_method = bat # 设定程序的运行方式，bat为使用bat文件触发，global_listen为全局键盘监听方式
picture_folder = pic #设定程序的运行方式，bat为使用bat文件触发，pyHook为全局键盘监听方式
picture_suffix = png #截图的保存格式，可以选择bmp或者png
# now support qiniu only
picture_bed = qiniu #设定上传图片到七牛云

[global_listen]
short_key_one = Lwin #快捷键第一个按键
short_key_two = C #快捷键第二个按键

[qiniu]
#七牛云的相关配置
access_key = Q6sS422O05AwYD5aVqM3FqCcCpF36tqvyQ75Zvzw
secret_key = 6QtAqqTxoSxZP-2uoXROehxPLX2CCmoOaB2aLObM
container_name = picturebed  #七牛云的图片储存位置
url = http://7sbpmp.com1.z0.glb.clouddn.com/{} #七牛云分配的默认域名
```

其中`access_key` 和 `secret_key` 可以在七牛云的控制面板中看到，如图：
![](http://7sbpmp.com1.z0.glb.clouddn.com/20160605083025.png) 
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-22-43.png) 

`container_name` 为下图所示内容：
![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-06-04-20-24-40.png) 

`short_key_one` 和 `short_key_two` 为快捷键的两个按键，默认为左侧windows徽标键(`Lwin`) 和 字母 `C`。

### 使用

1. 下载最新版程序：[https://github.com/kingname/MarkdownPicPicker/releases/download/v0.2.2/MarkdownPicPicker-v0.2.2.zip](https://github.com/kingname/MarkdownPicPicker/releases/download/v0.2/MarkdownPicPicker-v0.2.2.zip)下
2. 修改config.ini
3. 复制图片到剪贴板
4. 双击运行markdownpicpicker.exe

###只复制图片链接

如果你希望只将图片的url复制到剪贴板中，而不是复制\!\[\]\(图片url\)， 你可以为markdownpicpicker.exe添加上 `-linkonly` 参数。在markdownpicpicker.exe所在目录打开cmd, 输入:
```
markdownpicpicker.exe -linkonly
```

建议大家使用AutoHotKey来启动程序。这样可以把整个流程缩短到2秒钟。AutoHotKey的配置示例如下图所示：

![](http://7sbpmp.com1.z0.glb.clouddn.com/2016-07-16-11-54-13.png) 

需要首先使用QQ截图或者其他截图工具将图片保存到剪贴板中，然后按下设定好的快捷键即可。Markdown格式的图片链接就已经保存到剪贴板中了。在需要使用的地方直接粘贴。

## 说明
如果你希望自己从源代码编译程序，请注意以下问题：

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

