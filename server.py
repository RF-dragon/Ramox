import os
import threading
from typing import Union

import keyboard
import pyperclip
import win11toast
import win32clipboard
import wxpy
from PIL.Image import Image
from PIL.ImageGrab import grabclipboard

bot = wxpy.Bot(cache_path=True)


def confirm_img(chat: wxpy.Chat, file: str) -> None:
    """Confirm the image with a toast notification.

    Args:
        chat (wxpy.Chat): The chat object.
        file (str): The path of the image.
    """
    res = toast(f'Sending the following image to {chat.name}:',
                image=file,
                buttons=['Yes', 'No'])
    try:
        if res['arguments'] == 'http:Yes':
            chat.send_image(file)
    except Exception:
        pass


def confirm_file(chat: wxpy.Chat, file: str) -> None:
    """Confirm the file with a toast notification.

    Args:
        chat (wxpy.Chat): The chat object.
        file (str): The path of the file.
    """
    res = toast(f'Sending the following file to {chat.name}:\n' + file,
                buttons=['Yes', 'No'])
    try:
        if res['arguments'] == 'http:Yes':
            chat.send_file(file)
    except Exception:
        pass


def confirm_video(chat: wxpy.Chat, file: str) -> None:
    """Confirm the video with a toast notification.

    Args:
        chat (wxpy.Chat): The chat object.
        file (str): The path of the video.
    """
    res = toast(f'Sending the following video to {chat.name}:\n' + file,
                buttons=['Yes', 'No'])
    try:
        if res['arguments'] == 'http:Yes':
            chat.send_video(file)
    except Exception:
        pass


def get_chat(keyword: str) -> Union[wxpy.Chat, None]:
    """Get the chat object by the keyword.

    Args:
        keyword (str): The keyword to search.

    Returns:
        wxpy.Chat: The chat object.
    """
    chat = bot.search(keyword)
    try:
        chat = wxpy.ensure_one(chat)
        return chat
    except ValueError:
        return None


def reply_file(msg: wxpy.Message) -> None:
    """Reply the file with a toast notification.

    Args:
        msg (wxpy.Message): The message to be replied.
    """
    if msg.type == wxpy.TEXT:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}): {msg.text}'
        res = toast(display,
                    input='Enter the path of the file...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the file...'
                    }, 'Send the file from the clipboard', 'Back'])
    elif msg.type == wxpy.PICTURE:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}):'
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        res = toast(display,
                    image=file,
                    input='Enter the path of the file...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the file...'
                    }, 'Send the file from the clipboard', 'Back'])
    elif msg.type in [wxpy.RECORDING, wxpy.ATTACHMENT, wxpy.VIDEO]:
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}) sends you a file:\n{msg.file_name}'
        res = toast(display,
                    input='Enter the path of the file...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the file...'
                    }, {
                        'activationType': 'protocol',
                        'arguments': file,
                        'content': 'Open file'
                    }, {
                        'activationType': 'protocol',
                        'arguments': 'http:Send the file from the clipboard',
                        'content': 'From clipboard'
                    }, 'Back'])
    try:
        if res['arguments'] == 'http:':
            confirm_file(msg.chat,
                         res['user_input']['Enter the path of the file...'])
        elif res['arguments'] == 'http:Send the file from the clipboard':
            win32clipboard.OpenClipboard()
            formats = []
            format = win32clipboard.EnumClipboardFormats(0)
            while format:
                formats.append(format)
                format = win32clipboard.EnumClipboardFormats(format)
            if win32clipboard.CF_HDROP in formats:
                file = win32clipboard.GetClipboardData(
                    win32clipboard.CF_HDROP)[0]
                win32clipboard.CloseClipboard()
                confirm_file(msg.chat, file)
            else:
                win32clipboard.CloseClipboard()
                confirm_file(msg.chat, pyperclip.paste())
        elif res['arguments'] == 'http:Back':
            reply_msg(msg)
    except Exception:
        pass


def reply_img(msg: wxpy.Message) -> None:
    """Reply the image with a toast notification.

    Args:
        msg (wxpy.Message): The message to be replied.
    """
    if msg.type == wxpy.TEXT:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}): {msg.text}'
        res = toast(display,
                    input='Enter the path of the image...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the image...'
                    }, 'Send the image from the clipboard', 'Back'])
    elif msg.type == wxpy.PICTURE:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}):'
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        res = toast(display,
                    image=file,
                    input='Enter the path of the image...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the image...'
                    }, 'Send the image from the clipboard', 'Back'])
    elif msg.type in [wxpy.RECORDING, wxpy.ATTACHMENT, wxpy.VIDEO]:
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}) sends you a file:\n{msg.file_name}'
        res = toast(display,
                    input='Enter the path of the image...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the image...'
                    }, {
                        'activationType': 'protocol',
                        'arguments': file,
                        'content': 'Open file'
                    }, {
                        'activationType': 'protocol',
                        'arguments': 'http:Send the image from the clipboard',
                        'content': 'From clipboard'
                    }, 'Back'])
    try:
        if res['arguments'] == 'http:':
            confirm_img(msg.chat,
                        res['user_input']['Enter the path of the image...'])
        elif res['arguments'] == 'http:Send the image from the clipboard':
            img = grabclipboard()
            if isinstance(img, Image):
                file = os.path.abspath(os.path.join('Files', 'temp.png'))
                img.save(file)
                confirm_img(msg.chat, file)
            else:
                win32clipboard.OpenClipboard()
                formats = []
                format = win32clipboard.EnumClipboardFormats(0)
                while format:
                    formats.append(format)
                    format = win32clipboard.EnumClipboardFormats(format)
                if win32clipboard.CF_HDROP in formats:
                    file = win32clipboard.GetClipboardData(
                        win32clipboard.CF_HDROP)[0]
                    win32clipboard.CloseClipboard()
                    confirm_img(msg.chat, file)
                else:
                    win32clipboard.CloseClipboard()
                    confirm_img(msg.chat, pyperclip.paste())
        elif res['arguments'] == 'http:Back':
            reply_msg(msg)
    except Exception:
        pass


def reply_msg(msg: wxpy.Message) -> None:
    """Reply the message with a toast notification.

    Args:
        msg (wxpy.Message): The message to be replied.
    """
    if msg.type == wxpy.TEXT:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}): {msg.text}'
        res = toast(display,
                    input='Enter the message here...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the message here...'
                    }, 'Send image', 'Send file', 'Send video'])
    elif msg.type == wxpy.PICTURE:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}):'
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        res = toast(display,
                    image=file,
                    input='Enter the message here...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the message here...'
                    }, 'Send image', 'Send file', 'Send video'])
    elif msg.type in [wxpy.RECORDING, wxpy.ATTACHMENT, wxpy.VIDEO]:
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}) sends you a file:\n{msg.file_name}'
        res = toast(display,
                    input='Enter the message here...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the message here...'
                    }, {
                        'activationType': 'protocol',
                        'arguments': file,
                        'content': 'Open file'
                    }, 'Send image', 'Send file'])
    else:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}) sends you a message that is currently not supported.'
        toast(display)
        return
    try:
        if res['arguments'] == 'http:':
            msg.reply(res['user_input']['Enter the message here...'])
        elif res['arguments'] == 'http:Send image':
            reply_img(msg)
        elif res['arguments'] == 'http:Send file':
            reply_file(msg)
        elif res['arguments'] == 'http:Send video':
            reply_video(msg)
    except Exception:
        pass


def reply_video(msg: wxpy.Message) -> None:
    """Reply the video with a toast notification.

    Args:
        msg (wxpy.Message): The message to be replied.
    """
    if msg.type == wxpy.TEXT:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}): {msg.text}'
        res = toast(display,
                    input='Enter the path of the video...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the video...'
                    }, 'Send the video from the clipboard', 'Back'])
    elif msg.type == wxpy.PICTURE:
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}):'
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        res = toast(display,
                    image=file,
                    input='Enter the path of the video...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the video...'
                    }, 'Send the video from the clipboard', 'Back'])
    elif msg.type in [wxpy.RECORDING, wxpy.ATTACHMENT, wxpy.VIDEO]:
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        display = f'{msg.chat.name}({msg.member.name if msg.member is not None else msg.sender.name}) sends you a file:\n{msg.file_name}'
        res = toast(display,
                    input='Enter the path of the video...',
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Reply',
                        'hint-inputId': 'Enter the path of the video...'
                    }, {
                        'activationType': 'protocol',
                        'arguments': file,
                        'content': 'Open file'
                    }, {
                        'activationType': 'protocol',
                        'arguments': 'http:Send the video from the clipboard',
                        'content': 'From clipboard'
                    }, 'Back'])
    try:
        if res['arguments'] == 'http:':
            confirm_video(msg.chat,
                          res['user_input']['Enter the path of the video...'])
        elif res['arguments'] == 'http:Send the video from the clipboard':
            img = grabclipboard()
            if isinstance(img, Image):
                file = os.path.abspath(os.path.join('Files', 'temp.png'))
                img.save(file)
                confirm_video(msg.chat, file)
            else:
                win32clipboard.OpenClipboard()
                formats = []
                format = win32clipboard.EnumClipboardFormats(0)
                while format:
                    formats.append(format)
                    format = win32clipboard.EnumClipboardFormats(format)
                if win32clipboard.CF_HDROP in formats:
                    file = win32clipboard.GetClipboardData(
                        win32clipboard.CF_HDROP)[0]
                    win32clipboard.CloseClipboard()
                    confirm_video(msg.chat, file)
                else:
                    win32clipboard.CloseClipboard()
                    confirm_video(msg.chat, pyperclip.paste())
        elif res['arguments'] == 'http:Back':
            reply_msg(msg)
    except Exception:
        pass


def send_file() -> None:
    """Send a file to a specific user.
    """
    res = toast(
        'Send a file:',
        inputs=['Nickname, remark, etc.', 'Enter the path of the file...'],
        buttons=[{
            'activationType': 'protocol',
            'arguments': 'http:',
            'content': 'Send',
            'hint-inputId': 'Enter the path of the file...'
        }, 'Send the file from the clipboard', 'Back'])
    try:
        chat = get_chat(res['user_input']['Nickname, remark, etc.'])
        if chat is None:
            toast('Warning: The user is not found.')
            return
        if res['arguments'] == 'http:':
            confirm_file(chat,
                         res['user_input']['Enter the path of the file...'])
        elif res['arguments'] == 'http:Send the file from the clipboard':
            win32clipboard.OpenClipboard()
            formats = []
            format = win32clipboard.EnumClipboardFormats(0)
            while format:
                formats.append(format)
                format = win32clipboard.EnumClipboardFormats(format)
            if win32clipboard.CF_HDROP in formats:
                file = win32clipboard.GetClipboardData(
                    win32clipboard.CF_HDROP)[0]
                win32clipboard.CloseClipboard()
                confirm_file(chat, file)
            else:
                win32clipboard.CloseClipboard()
                confirm_file(chat, pyperclip.paste())
        else:
            send_msg()
    except Exception:
        pass


def send_img() -> None:
    """Send an image to a specific user.
    """
    res = toast(
        'Send an image:',
        inputs=['Nickname, remark, etc.', 'Enter the path of the image...'],
        buttons=[{
            'activationType': 'protocol',
            'arguments': 'http:',
            'content': 'Send',
            'hint-inputId': 'Enter the path of the image...'
        }, 'Send the image from the clipboard', 'Back'])
    try:
        chat = get_chat(res['user_input']['Nickname, remark, etc.'])
        if chat is None:
            toast('Warning: The user is not found.')
            return
        if res['arguments'] == 'http:':
            confirm_img(chat,
                        res['user_input']['Enter the path of the image...'])
        elif res['arguments'] == 'http:Send the image from the clipboard':
            img = grabclipboard()
            if isinstance(img, Image):
                file = os.path.abspath(os.path.join('Files', 'temp.png'))
                img.save(file)
                confirm_img(chat, file)
            else:
                win32clipboard.OpenClipboard()
                formats = []
                format = win32clipboard.EnumClipboardFormats(0)
                while format:
                    formats.append(format)
                    format = win32clipboard.EnumClipboardFormats(format)
                if win32clipboard.CF_HDROP in formats:
                    file = win32clipboard.GetClipboardData(
                        win32clipboard.CF_HDROP)[0]
                    win32clipboard.CloseClipboard()
                    confirm_img(chat, file)
                else:
                    win32clipboard.CloseClipboard()
                    confirm_img(chat, pyperclip.paste())
        else:
            send_msg()
    except Exception:
        pass


def send_msg() -> None:
    """Send a message to a specific user.
    """
    res = toast('Send a message:',
                inputs=['Nickname, remark, etc.', 'Enter the message here...'],
                buttons=[{
                    'activationType': 'protocol',
                    'arguments': 'http:',
                    'content': 'Send',
                    'hint-inputId': 'Enter the message here...'
                }, 'Send image', 'Send file', 'Send video'])
    try:
        if res['arguments'] == 'http:':
            chat = get_chat(res['user_input']['Nickname, remark, etc.'])
            if chat is None:
                toast('Warning: The user is not found.')
                return
            chat.send(res['user_input']['Enter the message here...'])
        elif res['arguments'] == 'http:Send image':
            send_img()
        elif res['arguments'] == 'http:Send file':
            send_file()
        elif res['arguments'] == 'http:Send video':
            send_video()
    except Exception:
        pass


def send_video() -> None:
    """Send a video to a specific user.
    """
    res = toast(
        'Send a video:',
        inputs=['Nickname, remark, etc.', 'Enter the path of the video...'],
        buttons=[{
            'activationType': 'protocol',
            'arguments': 'http:',
            'content': 'Send',
            'hint-inputId': 'Enter the path of the video...'
        }, 'Send the video from the clipboard', 'Back'])
    try:
        chat = get_chat(res['user_input']['Nickname, remark, etc.'])
        if chat is None:
            toast('Warning: The user is not found.')
            return
        if res['arguments'] == 'http:':
            confirm_video(chat,
                          res['user_input']['Enter the path of the video...'])
        elif res['arguments'] == 'http:Send the video from the clipboard':
            win32clipboard.OpenClipboard()
            formats = []
            format = win32clipboard.EnumClipboardFormats(0)
            while format:
                formats.append(format)
                format = win32clipboard.EnumClipboardFormats(format)
            if win32clipboard.CF_HDROP in formats:
                file = win32clipboard.GetClipboardData(
                    win32clipboard.CF_HDROP)[0]
                win32clipboard.CloseClipboard()
                confirm_video(chat, file)
            else:
                win32clipboard.CloseClipboard()
                confirm_video(chat, pyperclip.paste())
        else:
            send_msg()
    except Exception:
        pass


def toast(text: str, **kwargs) -> dict:
    """Send a toast notification to the Windows 11 Action Center.

    Args:
        text (str): Main text of the notification.

    Returns:
        dict: A dictionary containing the result of the notification.
    """
    return win11toast.toast('WeChat', text, duration='long', **kwargs)


@bot.register(except_self=False)
def get_msg(msg: wxpy.Message):
    reply_msg(msg)


if __name__ == '__main__':
    thread = threading.Thread(target=bot.join)
    thread.start()
    keyboard.add_hotkey('ctrl+alt+w', send_msg)