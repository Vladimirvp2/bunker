'''
Config for user settings
'''
import os, sys
cwd = os.getcwd()
PROJECT_DIR = cwd #+ "\\"
print PROJECT_DIR, "Project dir"


import logging
from aglyph.assembler import Assembler
from aglyph.context import XMLContext

import Common.Constants.Language as Language
import Common.Constants.LabelType as LabelType
import tkFont
import copy
import ttk as ttk


#DI content
#context = XMLContext("../movies-context.xml")
projectPath = os.path.abspath(os.path.dirname(__file__))
print projectPath, "Project Path"
#contextPath = os.path.join(projectPath, r"app_context.xml")
contextPath = r"app_context.xml"
context = XMLContext(contextPath)
#context = XMLContext(projectPath + r"\\app_context.xml")
#context = str(os.path.join(projectPath, r"app_context.xml"))

#context = XMLContext(projectPath + r"\\app_context.xml")
#context = XMLContext( cwd + r"../movies-context.xml")
ASSEMBLER = Assembler(context)
#logging.basicConfig(filename=r"D:/example.log",level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

CONFIG_FILE_PATH = r'D:/easypassConfig.db'
#LOCALIZATION_FILES_PATH = r'D:/'

#DATABASE_IMAGE = r'D:/database_icon3.gif'

#DATABASE_DISCONNECTED_IMAGE = r'D:/database_disconnected.gif'
#CATEGORY_IMAGE = r'D:/category_icon.gif'

RESOURCES_CONFIG_PATH = os.path.join('Resources', r'resourceConfig.xml') #r'Resources\\resourceConfig.xml'
LOCALIZATION_FILES_PATH = os.path.join('Resources', r'Localization') #r'Resources\\Localization\\'

#AES base for encryption/decryption. Should be 16, 32, 64..
CRYPTO_ENABLE = True
AES_CRYPTO_BASE = 16

SITE_PATTERN = '[-0-9a-zA-Z_\.//:?#%=]+'

START_LANGUAGE = Language.EN
AUTO_PASSWORD_GENERATION_MIN_LENGTH = 1
AUTO_PASSWORD_GENERATION_MAX_LENGTH = 100
AUTO_PASSWORD_GENERATION_DEFAULT_LENGTH = 8
AUTO_PASSWORD_GENERATION_SAMPLE_NUMBER = 10
AUTO_PASSWORD_GENERATION_COLLECT_ENTROPY_NUMBER = 10

#fonts
#LABEL_FONT = tkFont.Font(size = 12, family='Arial')
#LABEL_FONT_TABFRAME = tkFont.Font(size = 10, family='Arial')
#LABEL_FONT_BUTTON = tkFont.Font(size = 10, family='Arial') 

#buttons settings
BUTTON_FONT_FAMILY = 'Helvetica'
BUTTON_FONT_SIZE = 10
BUTTON_FONT_WEIGHT = 'normal'
BUTTON_STYLE = 'Message.TButton'

LABEL_FONT_FAMILY = 'Helvetica'
LABEL_FONT_SIZE = 10
LABEL_FONT_WEIGHT = 'normal'
LABEL_FONT = 0

LABEL_FONT__TABFRAME_FAMILY = 'Helvetica'
LABEL_FONT__TABFRAME_SIZE = 10
LABEL_FONT__TABFRAME_WEIGHT = 'normal'
LABEL_FONT_TABFRAME = 0


#style of treeview widget id dialogs
TREEVIEW_DIALOG_STYLE = 'D.Treeview'
BUTTON_STYLE = 'B.TButton'


# def setButtonsStyle():
#     s = ttk.Style()
#     s.configure(BUTTON_STYLE, font = (BUTTON_FONT_FAMILY, BUTTON_FONT_SIZE, BUTTON_FONT_WEIGHT))
#      
# def setLabelFont():
#     LABEL_FONT = tkFont.Font(size = LABEL_FONT_SIZE, family=LABEL_FONT_FAMILY, weight=LABEL_FONT_WEIGHT)
#     LABEL_FONT_TABFRAME = tkFont.Font(size = LABEL_FONT__TABFRAME_SIZE, family=LABEL_FONT__TABFRAME_FAMILY, weight=LABEL_FONT__TABFRAME_WEIGHT)
#        
    
def getFont(labelType):
    """
    User fonts settings
    @type labelType: LabelType
    @param labelType: type of the label  
    """
    
    if labelType == LabelType.NORMAL_TEXT:
        return ("Helvetica", 11)
    elif labelType == LabelType.LABEL_FRAME_TITLE:
        return ("Helvetica", 11)
    elif labelType == LabelType.TITEL_TEXT:
        return ("Helvetica", 13, "bold")
    elif labelType == LabelType.RADIO_BUTTON:
        #return ("Helvetica", 11)
        default_font = tkFont.nametofont("TkDefaultFont")
        font = (default_font['family'], default_font['size']+2, default_font['weight'])
        #font.configure(size=12)
        return font
    
    elif labelType == LabelType.LISTBOX:
        default_font = tkFont.nametofont("TkDefaultFont")
        return default_font
        
    
    return ("Helvetica", 14)


def getLabelColor(labelType):
    """
    User color settings for labels
    @type labelType: LabelType
    @param labelType: type of the label  
    """
    
    if labelType == LabelType.NORMAL_TEXT:
        return "black"
    elif labelType == LabelType.LABEL_FRAME_TITLE:
        return "blue"
    elif labelType == LabelType.TITEL_TEXT:
        return "black"
    elif labelType == LabelType.RADIO_BUTTON:
        return "black"
    elif labelType == LabelType.LISTBOX:
        return "black"
    
    return "black"


def setStyles():
    style = ttk.Style()
    #style.configure(".", font=('Helvetica', 8), foreground="white")
    style.configure(TREEVIEW_DIALOG_STYLE, foreground='blue')
    h = TREEVIEW_DIALOG_STYLE + '.Heading'
    style.configure(h, font=('Helvetica', 12))
    
    #set buttons style
    style = ttk.Style()
    default_font = tkFont.nametofont("TkDefaultFont")
    style.configure(BUTTON_STYLE, font=default_font)    
    
    


    

   
    
    

