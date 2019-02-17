"""Classes to implement Login dialog"""

import Tkinter as tk
import ttk
import UsConfig as Config


from abc import ABCMeta, abstractmethod


class LoginI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getLogin(self):
        "Return referance of the login entry"
        pass
    
    @abstractmethod
    def getPassword(self):
        "Return referance of the password entry"
        pass 
    
    
    
class Login(tk.Toplevel, LoginI):
    """Dialog for log-in into app. Is the first dialog to appear"""
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        #add self to controller
        self.__controller.addView(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.init()
        
    def init(self):
        #set dialog title
        self.title(self.__localization.getWord('login_dialog'))
        #add entries
        fields = {'login' : self.__localization.getWord('login'), 'password' : self.__localization.getWord('password')}
        
        for key in fields.keys():
            row = tk.Frame(self)                        
            lab = tk.Label(row, width=10, text=fields[key], anchor=tk.W, padx=2)  
            #if password field
            if key == 'password':  
                ent = tk.Entry(row, show="*", width=35)
                self.__passwordEntry = ent
            else:
                ent = tk.Entry(row,  width=35)
                self.__loginEntry = ent
            row.pack(side=tk.TOP, fill=tk.X)              
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
         
        #add buttons
        buttonsData = [{'text' : self.__localization.getWord('register'), 'command' : self.register, 'width' : 8},
                       {'text' : self.__localization.getWord('cancel'), 'command' : self.cancel, 'width' : 11},
                        {'text' : self.__localization.getWord('login'), 'command' : self.login, 'width' : 11}]
        for data in buttonsData:
            button = ttk.Button(self, text=data['text'], command=data['command'], width=data['width'] )
            button.pack(side=tk.RIGHT, padx=1, pady=3) 
               
        
    def login(self):
        self.__controller.loginPress()
        
    def cancel(self):
        self.__controller.cancelPress()      
        
    def register(self):
        self.__controller.registerPress()
        
       
    def getLogin(self):
        return self.__loginEntry.get()
    
    def getPassword(self):
        return self.__passwordEntry.get()     
    
