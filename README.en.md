# Ramox

Language: [Simplified Chinese](README.md) | English

## Project introduction

This project is based on `wxpy` and `win11toast`. It is a WeChat helper that sends all WeChat messages received to the Windows 11 notification center.

### Project features

- Concise, pretty, light-weighted
- Quick and convenient replication of messages received
- Highly customizable, can implement functions like auto replying and auto accepting friend requests by modifying the code a little bit

### Functions supported

- Receive and display text messages
- Receive and display images
- Receive files, display file names, one-click opening files
- Quickly reply with texts, images, files, or videos.
- Use `Ctrl+Alt+W` to call a notification that allows you to actively send messages.
- Videos and recordings are dealt the same way as files

### Functions to be implemented

- One-click playing recordings
- Displaying history messages

### Functions not currently planned to implement

- UI
- Sending or receiving name cards, money transfers, and maps
- Moment

### Effect

- Text messages

![Text](Images/text.png)

- Images

![Image](Images/image.png)

- Files

![Image](Images/file.png)

- Actively send videos

![Video](Images/video.png)

### Notice

The program can only be used for learning purposes, it should NOT be used for commercial purposes. Abuse of this program might lead to a violation of the Agreement on Software License and Service of Tencent Weixin. Please only use this program according to the agreement. We will not be responsible for any legal consequences brought by the violation of the Agreement on Software License and Service of Tencent Weixin.

## Development environment

- Windows 11 25330.1000
- Python 3.8

Not tested in other systems or environments. A successful deployment is not guaranteed.

## Installation

1. Install [Python](https://www.python.org/).
2. Install all required packages:
```bash
pip install -r requirements.txt
```

## Run

Simply run by double clicking [run.bat](run.bat). After running, all messages will be sent to the Windows notification center in a pretty form. You can reply to those messages in notification boxes conveniently or actively send messages by pressing `Ctrl+Alt+W`.

## Acknowledgements

- [keyboard](https://github.com/boppreh/keyboard)
- [pyperclip](https://github.com/asweigart/pyperclip)
- [pywin32](https://github.com/mhammond/pywin32)
- [win11toast](https://github.com/GitHub30/win11toast)
- [wxpy](https://github.com/youfou/wxpy)

# Update log

## 2023.9.8

- Move the CSDN tutorial version to the branch `tutorial`.
- Add the function of quickly replying to images, files, and videos.
- Add the function of actively sending messages with a notification window.
- Can access images and files in the clipboard now.
- Remove the function of using the terminal to send messages. It is completely replaced by active message sending.
