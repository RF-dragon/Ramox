import os
from typing import Union

import win11toast
import wxpy

bot = wxpy.Bot(cache_path=True)
context = None
last = None


def show_context() -> None:
    """Print the current context.
    """
    if context is None:
        print('No chat context is available.')
        return
    print(f'Current context: [{context.name}].')


def send(msg: str,
         chat: Union[str, None] = None,
         msg_type: str = 'msg') -> None:
    """Sends a message to a chat.

    Args:
        msg (str): The message to be sent. If msg_type is not 'msg', this needs
            to be a path to the file that needs to be sent.
        chat (Union[str, None], optional): The chat that the message will be
            sent to. If None, it will be send to the current context. Defaults
            to None.
        msg_type (str): The type of the message.
    """
    if chat is None:
        if context is None:
            print('Warning: No chat context is available.')
            return
        else:
            chat = context
    else:
        chat = bot.search(chat)
        try:
            chat = wxpy.ensure_one(chat)
        except ValueError:
            print(
                'Warning: Zero or more than one chat with the given keyword found. Skipping these chats.'
            )
            return
    if msg_type == 'msg':
        chat.send_msg(msg)
    elif msg_type == 'image':
        chat.send_image(msg)
    elif msg_type == 'file':
        chat.send_file(msg)
    elif msg_type == 'video':
        chat.send_video(msg)
    else:
        print('Warning: Invalid message type.')


def switch_context(chat: Union[str, None] = None) -> None:
    """Switch to another context. All message sent without selecting a receiver
    will be sent to the current context.

    Args:
        chat (Union[str, None], optional): The chat to be set as the current
            context. If None, the context will be the chat from which the last
            message is sent. Defaults to None.
    """
    global context
    if chat is None:
        if last is None:
            print('Warning: No existing chat found.')
        else:
            context = last
    else:
        chat = bot.search(chat)
        try:
            context = wxpy.ensure_one(chat)
        except ValueError:
            print(
                'Warning: Zero or more than one chat with the given keyword found. Skipping these chats.'
            )
            return


@bot.register(except_self=False)
def echo(msg: wxpy.Message) -> None:
    """Prints all text messages received to the console.

    Args:
        msg (wxpy.Message): The message received.
    """
    global context, last
    last = msg.chat
    if msg.type == wxpy.TEXT:
        display = f'{msg.chat.name}({msg.sender.name if msg.member is None else msg.member.name}): {msg.text}'
        res = win11toast.toast('WeChat',
                               display,
                               input='Reply to this message...',
                               button={
                                   'activationType': 'protocol',
                                   'arguments': 'http:',
                                   'content': 'Send',
                                   'hint-inputId': 'Reply to this message...'
                               },
                               duration='long')
    else:
        display = f'{msg.chat.name}({msg.sender.name if msg.member is None else msg.member.name})'
        file = os.path.abspath(os.path.join('Files', msg.file_name))
        msg.get_file(file)
        if msg.type == wxpy.PICTURE:
            res = win11toast.toast('WeChat',
                                   display,
                                   image=file,
                                   input='Reply to this message...',
                                   button={
                                       'activationType': 'protocol',
                                       'arguments': 'http:',
                                       'content': 'Send',
                                       'hint-inputId':
                                       'Reply to this message...'
                                   },
                                   duration='long')
        else:
            res = win11toast.toast('WeChat',
                                   display + ' sends you a file.\n' + msg.file_name,
                                   input='Reply to this message...',
                                   buttons=[{
                                       'activationType': 'protocol',
                                       'arguments': file,
                                       'content': 'Open file'
                                   }, {
                                       'activationType':
                                       'protocol',
                                       'arguments':
                                       'http:',
                                       'content':
                                       'Send',
                                       'hint-inputId':
                                       'Reply to this message...'
                                   }],
                                   duration='long')
    try:
        reply = res['user_input']['Reply to this message...']
        if reply:
            msg.chat.send_msg(reply)
    except Exception:
        pass
    if context is None:
        context = msg.chat


if __name__ == '__main__':
    wxpy.embed()