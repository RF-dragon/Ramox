# Copyright (C) 2023. Weilong Guan.

# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.

# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

# Contact the author of this program via email <guanweilong2022@163.com>.

from typing import List
import threading

import keyboard
import pyperclip
import wxpy

from utils import *

bot = wxpy.Bot(cache_path=True)
cache = []


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
            update_cache(chat)
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
            update_cache(chat)
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
            update_cache(chat)
    except Exception:
        pass


def get_cache() -> List[str]:
    """Get a list of chat names from cached chats.

    Returns:
        List[str]: The list of chats.
    """
    return [chat.name for chat in cache]


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
            file = get_file_from_clipboard()
            if file is not None:
                confirm_file(msg.chat, file)
            else:
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
            file = get_img_from_clipboard()
            if file is not None:
                confirm_img(msg.chat, file)
                return
            file = get_file_from_clipboard()
            if file is not None:
                confirm_img(msg.chat, file)
            else:
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
            file = get_file_from_clipboard()
            if file:
                confirm_video(msg.chat, file)
            else:
                confirm_video(msg.chat, pyperclip.paste())
        elif res['arguments'] == 'http:Back':
            reply_msg(msg)
    except Exception:
        pass


def send_file() -> None:
    """Send a file to a specific user.
    """
    if not len(cache):
        res = toast(
            'Send a file:',
            inputs=['Nickname, remark, etc.', 'Enter the path of the file...'],
            buttons=[{
                'activationType': 'protocol',
                'arguments': 'http:',
                'content': 'Send',
                'hint-inputId': 'Enter the path of the file...'
            }, 'Send the file from the clipboard', 'Back'])
    else:
        res = toast(
            'Send a file. You can leave the nickname field blank by selecting a cached chat below.',
            inputs=['Nickname, remark, etc.', 'Enter the path of the file...'],
            selection=get_cache(),
            buttons=[{
                'activationType': 'protocol',
                'arguments': 'http:',
                'content': 'Send',
                'hint-inputId': 'Enter the path of the file...'
            }, 'Send the file from the clipboard', 'Back'])
    try:
        chat = get_chat(res['user_input']['Nickname, remark, etc.'])
        if chat is None:
            chat = get_chat(res['user_input']['selection'])
        if res['arguments'] == 'http:':
            confirm_file(chat,
                         res['user_input']['Enter the path of the file...'])
        elif res['arguments'] == 'http:Send the file from the clipboard':
            file = get_file_from_clipboard()
            if file is not None:
                confirm_file(chat, file)
            else:
                confirm_file(chat, pyperclip.paste())
        else:
            send_msg()
    except Exception:
        pass


def send_img() -> None:
    """Send an image to a specific user.
    """
    if not len(cache):
        res = toast('Send an image:',
                    inputs=[
                        'Nickname, remark, etc.',
                        'Enter the path of the image...'
                    ],
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Send',
                        'hint-inputId': 'Enter the path of the image...'
                    }, 'Send the image from the clipboard', 'Back'])
    else:
        res = toast(
            'Send an image. You can leave the nickname field blank by selecting a cached chat below.',
            inputs=[
                'Nickname, remark, etc.', 'Enter the path of the image...'
            ],
            selection=get_cache(),
            buttons=[{
                'activationType': 'protocol',
                'arguments': 'http:',
                'content': 'Send',
                'hint-inputId': 'Enter the path of the image...'
            }, 'Send the image from the clipboard', 'Back'])
    try:
        chat = get_chat(res['user_input']['Nickname, remark, etc.'])
        if chat is None:
            chat = get_chat(res['user_input']['selection'])
        if res['arguments'] == 'http:':
            confirm_img(chat,
                        res['user_input']['Enter the path of the image...'])
        elif res['arguments'] == 'http:Send the image from the clipboard':
            file = get_img_from_clipboard()
            if file is not None:
                confirm_img(chat, file)
                return
            file = get_file_from_clipboard()
            if file is not None:
                confirm_img(chat, file)
            else:
                confirm_img(chat, pyperclip.paste())
        else:
            send_msg()
    except Exception:
        pass


def send_msg() -> None:
    """Send a message to a specific user.
    """
    if not len(cache):
        res = toast(
            'Send a message:',
            inputs=['Nickname, remark, etc.', 'Enter the message here...'],
            buttons=[{
                'activationType': 'protocol',
                'arguments': 'http:',
                'content': 'Send',
                'hint-inputId': 'Enter the message here...'
            }, 'Send image', 'Send file', 'Send video'])
    else:
        res = toast(
            'Send a message. You can leave the nickname field blank by selecting a cached chat below.',
            inputs=['Nickname, remark, etc.', 'Enter the message here...'],
            selection=get_cache(),
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
                chat = get_chat(res['user_input']['selection'])
            chat.send(res['user_input']['Enter the message here...'])
            update_cache(chat)
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
    if not len(cache):
        res = toast('Send a video:',
                    inputs=[
                        'Nickname, remark, etc.',
                        'Enter the path of the video...'
                    ],
                    buttons=[{
                        'activationType': 'protocol',
                        'arguments': 'http:',
                        'content': 'Send',
                        'hint-inputId': 'Enter the path of the video...'
                    }, 'Send the video from the clipboard', 'Back'])
    else:
        res = toast(
            'Send a video. You can leave the nickname field blank by selecting a cached chat below.',
            inputs=[
                'Nickname, remark, etc.', 'Enter the path of the video...'
            ],
            selection=get_cache(),
            buttons=[{
                'activationType': 'protocol',
                'arguments': 'http:',
                'content': 'Send',
                'hint-inputId': 'Enter the path of the video...'
            }, 'Send the video from the clipboard', 'Back'])
    try:
        chat = get_chat(res['user_input']['Nickname, remark, etc.'])
        if chat is None:
            chat = get_chat(res['user_input']['selection'])
        if res['arguments'] == 'http:':
            confirm_video(chat,
                          res['user_input']['Enter the path of the video...'])
        elif res['arguments'] == 'http:Send the video from the clipboard':
            file = get_file_from_clipboard()
            if file is not None:
                confirm_video(chat, file)
            else:
                confirm_video(chat, pyperclip.paste())
        else:
            send_msg()
    except Exception:
        pass


def update_cache(chat: wxpy.Chat) -> None:
    """Put a new chat into the cache. LRU strategy is used.

    Args:
        chat (wxpy.Chat): The new chat to put into the cache.
    """
    global cache
    for i, item in enumerate(cache):
        if chat.puid == item.puid:
            cache.pop(i)
            cache.append(chat)
            return
    if len(cache) >= 5:
        cache.pop(0)
    cache.append(chat)


@bot.register(except_self=False)
def get_msg(msg: wxpy.Message):
    reply_msg(msg)
    update_cache(msg.chat)


if __name__ == '__main__':
    bot.enable_puid()
    thread = threading.Thread(target=bot.join)
    thread.start()
    keyboard.add_hotkey('ctrl+alt+w', send_msg)