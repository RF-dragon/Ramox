# Ramox

语言：简体中文 | [English](README.en.md)

## 项目介绍

本项目为一个基于`wxpy`和`win11toast`的将微信转发到Windows 11通知中心并支持快捷回复的微信机器人。

### 项目特点

- 简洁、美观、轻量化
- 方便、快捷的回复
- 可自定义程度高，只要稍微修改代码即可实现自动回复、自动通过好友请求等功能

### 支持功能

- 接收并显示文字消息
- 接收并显示图片
- 接收文件、显示文件名、一键打开文件
- 自由选择在终端或通知中心中发送消息
- 视频、语音等均按照文件处理

### 待开发功能

- 一键播放语音
- 快速发送文件、图片、视频等

### 暂不计划开发

- 图形用户界面
- 历史消息记录
- 名片、转账、地图等消息的收发
- 朋友圈

### 效果展示

- 文字消息

![Text](Images/text.png)

- 图片

![Image](Images/image.png)

- 文件

![Image](Images/file.png)

### 注意事项

本程序仅供学习用途使用，不得用于商业用途。对本程序的滥用可能违反腾讯微信软件许可及服务协议，请遵循协议使用。本人不承担由于使用本程序而违反腾讯微信软件许可及服务协议所带来的法律责任。

## 开发环境

- Windows 11 25330.1000
- Python 3.8

暂未在其他系统及环境中运行测试，不保证能够运行。

## 安装

1. 安装[Python](https://www.python.org/)。
2. 安装所有依赖的包：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 使用方法

双击[run.bat](run.bat)即可开始运行。运行后，所有信息会以美观的形式被转发到Windows通知中心。你可以在收到通知时快捷地进行回复，或在终端中手动发送信息。

### 使用Windows终端进行操作

详细的函数说明可以在[server.py](server.py)中查看。

#### 查看当前聊天对象

```python
def show_context() -> None:...
```
使用示例：
```bash
In [1]: show_context()
Current context: [文件传输助手].
```

#### 切换聊天对象

```python
def switch_context(chat: Union[str, None] = None) -> None:...
```
使用示例：
```bash
In [2]: switch_context('RFdragon')

In [3]: show_context()
Current context: [RFdragon].
```

#### 向聊天对象发送信息

```python
def send(msg: str, chat: Union[str, None] = None, msg_type: str = 'msg') -> None:
```
使用示例：
```bash
In [4]: send('Hello world!', chat='RFdragon')
```

## 致谢

- [wxpy](https://github.com/youfou/wxpy)
- [win11toast](https://github.com/GitHub30/win11toast)