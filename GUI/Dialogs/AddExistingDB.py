'''
Classes for add existing database dialog
'''

import Tkinter as tk
import ttk
from abc import ABCMeta, abstractmethod
from tkFileDialog   import askopenfilename
import Common.Constants.DataField as DataField


class AddExistingDBI(object):
    """
    Add existing DB view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getPath(self):
        "Return path as string"
        pass
    
    @abstractmethod
    def getPassword(self):
        "Return password as string"
        pass 


class AddExistingDB(tk.Toplevel, AddExistingDBI):
    """Dialog for log-in into app. Is the first dialog to appear"""
    #==================================================================
    #Label path                    button for choosing a file

    #Label password                entry

    #check box Show password    Ok button    Cancel button
    #==================================================================    
    LABEL_WIDTH = 12
    LABEL_PAD_X = 2
    ROW_PAD_Y = 3
    BUTTON_CHOOSE_DIALOG_WIDTH = 25
    PASSWORD_ENTRY_WIDTH = 35
    PASSWORD_ENTRY_PAD_X = 2
    BUTTON_WIDTH = 20
    BUTTON_PAD_X = 2
    BUTTON_PAD_Y = 3
    CHECKBOX_VALUE_ON = '1'
    CHECKBOX_VALUE_OFF = '0' 
    CHECKBOX_PAD_X = 1 
    CHECKBOX_PAD_Y = 3        
    
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        #add self to controller
        self.__controller.addView(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.__passwordEntry = None
        self.__path = None
        self.__chooseFileButton = None 
        self.__passwordCheckBoxValue = None
        self.init()
        
    def init(self):
        #set dialog title
        self.title(self.__localization.getWord('add_existing_db'))
        #add GUI elements
        fields_data = { DataField.PATH : self.__localization.getWord('path_to_file'),
                   DataField.PASSWORD : self.__localization.getWord('password')}
        fields = [DataField.PATH, DataField.PASSWORD]
        
        for field in fields:
            row = tk.Frame(self) 
            lab = tk.Label(row, width=AddExistingDB.LABEL_WIDTH, text=fields_data[field], anchor=tk.W, padx=AddExistingDB.LABEL_PAD_X )
            ent = None
            if field == DataField.PATH:             
                ent = ttk.Button(row, text=self.__localization.getWord('file'), command=self.chooseFile, width=AddExistingDB.BUTTON_CHOOSE_DIALOG_WIDTH)
                self.__chooseFileButton = ent
            else:
                ent = tk.Entry(row, show="*", width=AddExistingDB.PASSWORD_ENTRY_WIDTH)
                self.__passwordEntry = ent
                
            row.pack(side=tk.TOP, fill=tk.X, pady=AddExistingDB.ROW_PAD_Y)              
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
        
        #add space
        row = tk.Frame(self)     
        lab = tk.Label(row, width=AddExistingDB.LABEL_WIDTH, text=" ", anchor=tk.W, padx=AddExistingDB.LABEL_PAD_X ) 
        row.pack(side=tk.TOP, fill=tk.X)              
        lab.pack(side=tk.LEFT)    
            
        #add password check box
        self.__passwordCheckBoxValue = tk.StringVar()
        c = tk.Checkbutton( self, text=self.__localization.getWord('password_show'), variable=self.__passwordCheckBoxValue,
                            onvalue=AddExistingDB.CHECKBOX_VALUE_ON, offvalue=AddExistingDB.CHECKBOX_VALUE_OFF, command=self.passwordCheckBoxCommand)
        c.pack(side=tk.LEFT, padx=AddExistingDB.CHECKBOX_PAD_X, pady=AddExistingDB.CHECKBOX_PAD_Y) 
        c.deselect()             
               
        #add buttons
        buttonsData = [{'text' : self.__localization.getWord('cancel'), 'command' : self.cancel, 'width' : AddExistingDB.BUTTON_WIDTH},
                        {'text' : self.__localization.getWord('ok'), 'command' : self.ok, 'width' : AddExistingDB.BUTTON_WIDTH}]
        for data in buttonsData:
            button = ttk.Button(self, text=data['text'], command=data['command'], width=data['width'])
            button.pack(side=tk.RIGHT, padx=AddExistingDB.BUTTON_PAD_X, pady=AddExistingDB.BUTTON_PAD_Y) 
    
    
    def chooseFile(self):
        self.__path = askopenfilename() 
        self.__chooseFileButton.config(text=self.__path)         
        
    def ok(self):
        self.__controller.okPress()
        
    def cancel(self):
        self.__controller.cancelPress()      
        

    def passwordCheckBoxCommand(self ):
        val = self.__passwordCheckBoxValue.get()
        if val == AddExistingDB.CHECKBOX_VALUE_OFF:
            self.__passwordEntry.config(show = "*")
        else:
            self.__passwordEntry.config(show = "")
        
       
    def getPath(self):
        return self.__path.encode('utf8') 
    
    def getPassword(self):
        return self.__passwordEntry.get() 