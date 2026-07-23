from tkinter import *
from tkinter import ttk
from zebra import Zebra
import zpl
import os
import sys
import json
import pyperclip
import pathlib

directory :str = os.path.expanduser('~/Documents/CustomLabels')

def TextBoxResize(label : zpl.Label, text : str, width : float, height : float, justification : str = 'L'):
    padding : float = 0.0
    charWidth : float = 3.5
    charHeight : float = 3.5
    newWidth = width - (padding*2)
    newHeight = height - (padding*2)
    maxNumChar : int = int(newWidth / charWidth)
    label.write_text(text, char_width = charWidth, char_height = charHeight, line_width = newWidth, justification=justification)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


    #self.l.write_text(concat, char_height=4.2, char_width=4, line_width=45, justification='L',)