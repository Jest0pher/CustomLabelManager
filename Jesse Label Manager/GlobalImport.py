from tkinter import *
from tkinter import ttk
from zebra import Zebra
import zpl
import os
from observer import Observable as Ob
from observer import Event as obEvent
import json

directory :str = os.path.expanduser('~\Documents\CustomLabels')

def TextBoxResize(label : zpl.Label, text : str, width : float, height : float, justification : str = 'L'):
    padding : float = 0.0
    charWidth : float = 3.5
    charHeight : float = 3.5
    newWidth = width - (padding*2)
    newHeight = height - (padding*2)
    maxNumChar : int = int(newWidth / charWidth)
    label.write_text(text, char_width = charWidth, char_height = charHeight, line_width = newWidth, justification=justification)

    #self.l.write_text(concat, char_height=4.2, char_width=4, line_width=45, justification='L',)