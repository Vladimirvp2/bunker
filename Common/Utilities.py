'''
Auxiliary classes for App
'''

from Tkinter import *

__uniqueValue = 0 

class SuperEnum(object):
    class __metaclass__(type):
        def __iter__(self):
            for item in self.__dict__:
                if item == self.__dict__[item]:
                    yield item
 
 
# class Singleton(type):
#     _instances = {}
#     def __call__(self, *args, **kwargs):
#         if self not in self._instances:
#             self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
#         return self._instances[self]
     
     
def centerTopLevel(win):
    """Used to show a tip level window in the center of the screen"""    
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2 - 40
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    
    
def centerRoot(win):
    """Used to show the root window in the center of the screen. Used separately from centerTopLevel because of deiconify() method
       (root window is hidden at start)
    """     
    win.update_idletasks()
    w = win.winfo_screenwidth()
    h = win.winfo_screenheight()
    size = tuple(int(_) for _ in win.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2 - 40
    win.geometry("%dx%d+%d+%d" % (size + (x, y))) 


def setWaitForClose(win):
    """Make the win to grub the focus and wait for it to close"""
    win.focus_set()    
    win.grab_set()    
    win.wait_window()     


class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"     


#uniqueValue = 0        
def generateUniqueID():
    """Generate unique string id""" 
    global __uniqueValue
    __uniqueValue +=1
    return str(__uniqueValue) 
