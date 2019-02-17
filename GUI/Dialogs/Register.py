import Tkinter as tk
import ttk
from Common.Utilities import*
from abc import ABCMeta, abstractmethod



class RegisterI(object):
    """
    Register view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getLoginEntry(self):
        "Return reference of the login entry"
        pass
    
    @abstractmethod
    def getPasswordEntry(self):
        "Return reference of the password entry"
        pass
    
    @abstractmethod
    def getConfirmPasswordEntry(self):
        "Return reference of the confirm password entry"
        pass
    
    
    @abstractmethod
    def getLoginInfoLabel(self):
        "Return reference of the login info label"
        pass
    
    @abstractmethod
    def getPasswordInfoLabel(self):
        "Return reference of the password strength label"
        pass
    
    @abstractmethod
    def getConfirmPasswordInfoLabel(self):
        "Return reference of the confirm password OK label"
        pass         
    
    
    
class Register(tk.Toplevel, RegisterI):
    """Dialog for registration. Appear if press register button in the Login dialog"""
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        #references for labels and entries. Needed for the controller
        self.__refs = {}
        #add self to controller
        self.__controller.addView(self)      
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.init()
        
    def init(self):
        #add entries
        self.title(self.__localization.getWord('register_title'))
        fields = [self.__localization.getWord('login'), self.__localization.getWord('password'), self.__localization.getWord('confirm_password')]
        curr_num = 0
        for field in fields:
            row = tk.Frame(self)                        
            lab = tk.Label(row, width=16, text=field, anchor=tk.W, padx=2)  
            infoLabText = ''
            #password
            if  curr_num == 1:  
                ent = tk.Entry(row, show="*", width=35)
                ent.bind("<KeyRelease>", lambda ev: self.__controller.passwordEntryChanged())
                infoLabText = self.__localization.getWord('password_valid_symbols')
            #password confirm
            elif  curr_num == 2:  
                ent = tk.Entry(row, show="*", width=35)
                ent.bind("<KeyRelease>", lambda ev: self.__controller.passwordConfirmEntryChanged())                
            else:
                ent = tk.Entry(row,  width=35)
                ent.bind("<KeyRelease>", lambda ev: self.__controller.loginEntryChanged()) 
                infoLabText = self.__localization.getWord('login_valid_symbols')
                
            lab_info = tk.Label(row, width=8, text=infoLabText, anchor=tk.W, padx=3, pady=1)      
            row.pack(side=tk.TOP, fill=tk.X)              
            lab.pack(side=tk.LEFT)
            lab_info.pack(side=tk.RIGHT) 
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            
            #add references
            key = ' '
            if curr_num == 0:
                key = 'login'
            elif curr_num == 1:
                key = 'password'
            else:
                key = 'confirm_password'
            self.__refs[key+'_ent'] = ent
            self.__refs[key+'_lab'] = lab_info
            
            curr_num+=1  
              
        #add buttons
        buttonsData = [{'text' : self.__localization.getWord('cancel'), 'command' : self.cancel, 'width' : 16}, 
                       {'text' : self.__localization.getWord('ok'), 'command' : self.register, 'width' : 16}]
  
        for data in buttonsData:
            button = ttk.Button(self, text=data['text'], command=data['command'], width=data['width'])
            button.pack(side=tk.RIGHT, padx=1, pady=3) 
                                       
   
    def register(self):
        self.__controller.registerPress()       
     
    def cancel(self):
        self.__controller.cancelPress()
        
    def getLoginEntry(self):
        return self.__refs['login_ent']
    
    def getPasswordEntry(self):
        return self.__refs['password_ent']
    
    def getConfirmPasswordEntry(self):
        return self.__refs['confirm_password_ent']         
         
    def getLoginInfoLabel(self):
        return self.__refs['login_lab']
    
    def getPasswordInfoLabel(self):
        return self.__refs['password_lab']
    
    def getConfirmPasswordInfoLabel(self):
        return self.__refs['confirm_password_lab']        



     
