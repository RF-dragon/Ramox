# Copyright (C) 2023. Weilong Guan.

# See <server.py> for a full notice of the GPL-3 License.

import os
from typing import Union

import win11toast
import win32clipboard
from PIL.Image import Image
from PIL.ImageGrab import grabclipboard
    

def get_file_from_clipboard() -> Union[str, None]:
    """Get the path to the file copied into the clipboard.

    Returns:
        Union[str, None]: The file path. None if the file is invalid.
    """    
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
        return file
    else:
        win32clipboard.CloseClipboard()
        return None
    

def get_img_from_clipboard() -> Union[str, None]:
    """Save the image copied inside the clipboard into a temporary file and
    return its path.

    Returns:
        Union[str, None]: The path to the generated image file. None if the
        image is invalid.
    """    
    img = grabclipboard()
    if isinstance(img, Image):
        file = os.path.abspath(os.path.join('Files', 'temp.png'))
        img.save(file)
        return file
    else:
        return None


def toast(text: str, **kwargs) -> dict:
    """Send a toast notification to the Windows 11 Action Center.

    Args:
        text (str): Main text of the notification.

    Returns:
        dict: A dictionary containing the result of the notification.
    """
    return win11toast.toast('WeChat', text, duration='long', **kwargs)