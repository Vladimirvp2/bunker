'''
Own implementation of error, info, confirm dialods
'''

import Tkinter as tk
import ttk, os, string
import tkFont
from Tkinter import *
from abc import ABCMeta, abstractmethod


TEXT_WIDTH = 700
#message font constants
MESSAGE_FONT_FAMILY = 'Helvetica'
MESSAGE_FONT_SIZE = 10
MESSAGE_FONT_WEIGHT = 'bold'
#main frame padding
MAIN_FRAME_PAD_X = 5
MAIN_FRAME_PAD_Y = 10
#image
IMAGE_PAD_X = 5
#buttons
BUTTON_PAD_X = 2
BUTTON_PAD_Y = 5
#button font
BUTTON_FONT_FAMILY = 'Helvetica'
BUTTON_FONT_SIZE = 10
BUTTON_FONT_WEIGHT = 'normal'
BUTTON_STYLE = 'Message.TButton'
NUMBER_DIALOG_DEFAULT_VALUE = -1

import UsConfig as UsConfig

p = os.path.abspath(os.path.dirname(__file__))
IMAGE_PATH = p + '\\Icons\\'
print IMAGE_PATH, "IMAGE_PATH"



class NotEnoughArgumentsException(Exception):
    '''If user provided not the all necessary arguments'''
    def __init__(self, value, message):
        self.value = value
        self.message = message
    def __str__(self):
        return repr(' {}, {}'.format(self.value, self.message))  


class Dialog:
    """Base class for message dialogs"""
    
    WIN_WIDTH = 250
    WIN_HEIGHT = 100
    
    __metaclass__ = ABCMeta

    def __init__(self, master,
                 text='', buttonsText=['Ok'], default=None, cancel=None,
                 title=None, class_=None):
        self.master = master
        if class_:
            self.root = Toplevel(master, class_=class_)
        else:
            self.root = Toplevel(master)
        if title:
            self.root.title(title)
            self.root.iconname(title)
        
        self.root.minsize(width=self.WIN_WIDTH, height=self.WIN_HEIGHT)      
        self.root.resizable(0,0)
        self.root.configure(background = 'white')
        
        
        #add main frame
        fr = Frame(self.root, padx=MAIN_FRAME_PAD_X, pady=MAIN_FRAME_PAD_Y, width=500)
        fr.configure(background = 'white')
        #add error image
        self._image = PhotoImage(file=IMAGE_PATH + self.getImage())
        #self.__image = PhotoImage(file=r"Icons/error_dialog.gif")
        self.im = Label(fr, image = self._image, padx=IMAGE_PAD_X)
        self.im.configure(background = 'white')  
        self.im.pack(side=LEFT)
        #add message  
        self.message = Message(fr, text=text, aspect=TEXT_WIDTH, font=tkFont.Font(family=MESSAGE_FONT_FAMILY,
                                                                                   size=MESSAGE_FONT_SIZE,
                                                                                   weight=MESSAGE_FONT_WEIGHT))
        self.message.configure(background = 'white')
        self.message.pack(side=LEFT, expand=1, fill=BOTH)
        fr.pack(expand=1, fill=tk.BOTH)
        
        #Frame to add additional widgets
        self.frameBody = Frame(self.root, padx=MAIN_FRAME_PAD_X, pady=MAIN_FRAME_PAD_Y)
        self.frameBody.configure(background = 'white')
        self.frameBody.pack(expand = 1, fill=X)
        
        self.num = default
        self.cancel = cancel
        self.default = default
        self.root.bind('<Return>', self.return_event)


        s = ttk.Style()
        s.configure(BUTTON_STYLE, font = (BUTTON_FONT_FAMILY, BUTTON_FONT_SIZE, BUTTON_FONT_WEIGHT))
        #create buttons frame
        self.frame = Frame(self.root)
        self.frame.pack(expand = 1, fill=X)
        self.buttonFrame = Frame(self.frame)
        self.buttonFrame.pack()        
        self.addButtons(self.buttonFrame, buttonsText)   
        
        self.root.protocol('WM_DELETE_WINDOW', self.wm_delete_window)
        self._set_transient(master)
        
    @abstractmethod    
    def getImage(self):
        """Main image for message dialog. Override the method to set a different image"""
        return r"error_dialog.gif"  
    
    @abstractmethod    
    def addButtons(self, frame, buttonsText):
        """Add button panel. Override to add own buttons"""
        button = ttk.Button(frame, text=buttonsText[0], style=BUTTON_STYLE, command=lambda: self.done(0))
        button.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)      
        

    def _set_transient(self, master, relx=0.5, rely=0.3):
        widget = self.root
        widget.withdraw() # Remain invisible while we figure out the geometry
        widget.transient(master)
        widget.update_idletasks() # Actualize geometry information
        if master.winfo_ismapped():
            m_width = master.winfo_width()
            m_height = master.winfo_height()
            m_x = master.winfo_rootx()
            m_y = master.winfo_rooty()
        else:
            m_width = master.winfo_screenwidth()
            m_height = master.winfo_screenheight()
            m_x = m_y = 0
        w_width = widget.winfo_reqwidth()
        w_height = widget.winfo_reqheight()
        x = m_x + (m_width - w_width) * relx
        y = m_y + (m_height - w_height) * rely
        if x+w_width > master.winfo_screenwidth():
            x = master.winfo_screenwidth() - w_width
        elif x < 0:
            x = 0
        if y+w_height > master.winfo_screenheight():
            y = master.winfo_screenheight() - w_height
        elif y < 0:
            y = 0
        widget.geometry("+%d+%d" % (x, y))
        widget.deiconify() # Become visible at the desired location
        

    def go(self):
        self.root.wait_visibility()
        self.root.grab_set()
        self.root.mainloop()
        self.root.destroy()         
        
        return self.num
    

    def return_event(self, event):
        if self.default is None:
            self.root.bell()
        else:
            self.done(self.default)
            

    def wm_delete_window(self):
        self.master.focus_set()    
        self.master.grab_set() 
        if self.cancel is None:
            self.root.bell()
        else:
            self.done(self.cancel)
            

    def done(self, num):
        self.master.focus_set()    
        self.master.grab_set() 
        self.num = num
        self.root.quit() 

        
        
class ErrorDialog(Dialog):
    def __init__(self, master,
                  text='', buttonsText=['Ok'], default=None, cancel=None,
                  title=None, class_=None):
        Dialog.__init__(self, master, text = text, buttonsText=buttonsText,
                        default = default, cancel = cancel, title = title, class_=class_)
        
    def getImage(self):
        return r"error_dialog.gif"  
        
    def addButtons(self, frame, buttonsText):
        if len(buttonsText) == 0:
            raise NotEnoughArgumentsException(len(buttonsText), "No buttons provided. Should be 1 at least")

        button = ttk.Button(frame, text=buttonsText[0], style=BUTTON_STYLE, command=lambda: self.done(0))
        button.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)
        
        
class WarningDialog(Dialog):
    def __init__(self, master,
                  text='', buttonsText=['Ok'], default=None, cancel=None,
                  title=None, class_=None):
        Dialog.__init__(self, master, text = text, buttonsText=buttonsText,
                        default = default, cancel = cancel, title = title, class_=class_)
        
    def getImage(self):
        return r"warning_dialog.gif"  
        
    def addButtons(self, frame, buttonsText):
        if len(buttonsText) == 0:
            raise NotEnoughArgumentsException(len(buttonsText), "No buttons provided. Should be 1 at least")

        button = ttk.Button(frame, text=buttonsText[0], style=BUTTON_STYLE, command=lambda: self.done(0))
        button.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)
        
        
class InfoDialog(Dialog):
    def __init__(self, master,
                  text='', buttonsText=['Ok'], default=None, cancel=None,
                  title=None, class_=None):
        Dialog.__init__(self, master, text = text, buttonsText=buttonsText,
                        default = default, cancel = cancel, title = title, class_=class_)
        
    def getImage(self):
        return r"info_dialog.gif"   
        
    def addButtons(self, frame, buttonsText):
        if len(buttonsText) == 0:
            raise NotEnoughArgumentsException(len(buttonsText), "No buttons provided. Should be 1 at least")

        button = ttk.Button(frame, text=buttonsText[0], style=BUTTON_STYLE, command=lambda: self.done(0))
        button.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)
        
        
class YesNoDialog(Dialog):
    def __init__(self, master,
                  text='', buttonsText=['Yes', 'No'], default=None, cancel=None,
                  title=None, class_=None):
        Dialog.__init__(self, master, text = text, buttonsText=buttonsText,
                        default = default, cancel = cancel, title = title, class_=class_)
        
    def getImage(self):
        return r"question_dialog.gif"   
        
    def addButtons(self, frame, buttonsText):
        if len(buttonsText) < 2:
            raise NotEnoughArgumentsException(len(buttonsText), "To few buttons provided. Should be 2 at least")
        
        buttonYes = ttk.Button(frame, text=buttonsText[0], style=BUTTON_STYLE, command=lambda: self.done(1))
        buttonYes.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y)
        buttonNo = ttk.Button(frame, text=buttonsText[1], style=BUTTON_STYLE, command=lambda: self.done(0))
        buttonNo.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y) 
        
        
class GetNumberDialog(Dialog):
    ENTRY_WIDTH = 20
    ENTRY_PADDING_X = 5
    
    def __init__(self, master,
                  text='', buttonsText=['Ok'], default=None, cancel=None,
                  title=None, class_=None):
        Dialog.__init__(self, master, text = text, buttonsText=buttonsText,
                        default = default, cancel = cancel, title = title, class_=class_)
        
    def getImage(self):
        return r"question_dialog.gif"   
        
    def addButtons(self, frame, buttonsText):
        if len(buttonsText) == 0:
            raise NotEnoughArgumentsException(len(buttonsText), "No buttons provided. Should be 1 at least")
        
        self.ent = tk.Entry(self.frameBody , width=self.ENTRY_WIDTH)
        self.ent.pack(side=tk.BOTTOM, padx=self.ENTRY_PADDING_X )
        self.ent.bind('<KeyPress>', self.printableOnly)
        button = ttk.Button(frame, text=buttonsText[0], style=BUTTON_STYLE, command=lambda: self.getEnretedValue())
        button.pack(side=tk.LEFT, fill=BOTH, expand=1, padx=BUTTON_PAD_X, pady=BUTTON_PAD_Y) 
        
    def printableOnly(self, event):
        if event.char in string.digits:
            pass
        elif event.keysym not in ('Alt_r', 'Alt_L', 'F4', 'BackSpace', 'Delete'):
            return 'break'               

    def getEnretedValue(self):
        value = self.ent.get()
        if len(value) == 0:
            value = NUMBER_DIALOG_DEFAULT_VALUE
        self.done(int(value))
        

        

def showError(root, title = 'Error', text='', buttonsText=['Ok']):
        d = ErrorDialog(root,
                         text=text,
                         buttonsText=buttonsText,
                         default=0,
                         cancel=2,
                         title=title)
        
        return d.go()   
    
    
def showWarning(root, title = 'Warning', text='', buttonsText=['Ok']):
        d = WarningDialog(root,
                         text=text,
                         buttonsText=buttonsText,
                         default=0,
                         cancel=2,
                         title=title)
        
        return d.go()  
    
    
def showInfo(root, title = 'Info', text='', buttonsText=['Ok']):
        d = InfoDialog(root,
                         text=text,
                         buttonsText=buttonsText,
                         default=0,
                         cancel=2,
                         title=title)
        
        return d.go()  
    
    
def showYesNo(root, title = 'Question', text='', buttonsText=['Yes', 'No']):
        d = YesNoDialog(root,
                         text=text,
                         buttonsText=buttonsText,
                         default=0,
                         cancel=0,
                         title=title)
        
        return d.go()
    
    
def showNumber(root, title = 'Question', text='', buttonsText=['Yes', 'No']):
        d = GetNumberDialog(root,
                         text=text,
                         buttonsText=buttonsText,
                         default=NUMBER_DIALOG_DEFAULT_VALUE,
                         cancel=NUMBER_DIALOG_DEFAULT_VALUE,
                         title=title)
        
        return d.go()    


if __name__ == '__main__':

    pass
