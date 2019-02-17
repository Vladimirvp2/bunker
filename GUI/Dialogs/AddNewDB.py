'''
Classes for Add new DB dialog
'''

import Tkinter as tk
import ttk
from abc import ABCMeta, abstractmethod
from tkFileDialog   import asksaveasfilename
import Common.Constants.DataField as DataField


class AddNewDBI(object):
    """
    Add existing DB view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getPath(self):
        "Return path as string"
        pass
    
    @abstractmethod
    def getPasswordEntry(self):
        "Return password as string"
        pass 
    
    @abstractmethod
    def getNameEntry(self):
        "Return name as string"
        pass
     
    
    @abstractmethod
    def getCommentsEntry(self):
        "Return name as string"
        pass           


class AddNewDB(tk.Toplevel, AddNewDBI):
    """Dialog for crating and adding new DB"""
    #==================================================================
    #Label path                    button for choosing a path
    #Label name                    entry
    #Label password                entry
    #Label comments                Text
    
    #check box Show password    Ok button    Cancel button
    #==================================================================    
    LABEL_WIDTH = 12
    LABEL_PAD_X = 2
    ROW_PAD_Y = 2
    BUTTON_CHOOSE_DIALOG_WIDTH = 25
    ENTRY_WIDTH = 35
    PASSWORD_ENTRY_PAD_X = 2
    BUTTON_WIDTH = 20
    BUTTON_PAD_X = 2
    BUTTON_PAD_Y = 3
    CHECKBOX_VALUE_ON = '1'
    CHECKBOX_VALUE_OFF = '0' 
    CHECKBOX_PAD_X = 1 
    CHECKBOX_PAD_Y = 3  
    COMMENT_AREA_HIGHT = 2    
    
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        #add self to controller
        self.__controller.addView(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        
        self.__path = None
        self.__chooseFileButton = None 
        self.__passwordCheckBoxValue = None
        self.__entryRef = {}
        
        self.init()
        
    def init(self):
        #set dialog title
        self.title(self.__localization.getWord('add_existing_db'))
        #add GUI elements
        fields_data = { DataField.PATH : self.__localization.getWord('path_to_file'),
                   DataField.PASSWORD : self.__localization.getWord('password'),
                   DataField.COMMENTS : self.__localization.getWord('comments'),
                   DataField.NAME : self.__localization.getWord('name')}
        fields = [DataField.PATH, DataField.NAME, DataField.PASSWORD, DataField.COMMENTS]
        
        for field in fields:
            row = tk.Frame(self) 
            lab = tk.Label(row, width=AddNewDB.LABEL_WIDTH, text=fields_data[field], anchor=tk.W, padx=AddNewDB.LABEL_PAD_X )
            ent = None
            if field == DataField.PATH:             
                ent = ttk.Button(row, text=self.__localization.getWord('file'), command=self.chooseFile, width=AddNewDB.BUTTON_CHOOSE_DIALOG_WIDTH)
                self.__chooseFileButton = ent
            elif field == DataField.PASSWORD:
                ent = tk.Entry(row, show="*", width=AddNewDB.ENTRY_WIDTH)
            elif field == DataField.COMMENTS:
                ent = tk.Text(row, height=AddNewDB.COMMENT_AREA_HIGHT, width=AddNewDB.ENTRY_WIDTH  ) 
            else:
                ent = tk.Entry(row, width=AddNewDB.ENTRY_WIDTH)                              
                
            row.pack(side=tk.TOP, fill=tk.X, pady=AddNewDB.ROW_PAD_Y)              
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            
            self.__entryRef[field] = ent
        
        #add space
        row = tk.Frame(self)     
        lab = tk.Label(row, width=AddNewDB.LABEL_WIDTH, text=" ", anchor=tk.W, padx=AddNewDB.LABEL_PAD_X ) 
        row.pack(side=tk.TOP, fill=tk.X)              
        lab.pack(side=tk.LEFT)    
            
        #add password check box
        self.__passwordCheckBoxValue = tk.StringVar()
        c = tk.Checkbutton( self, text=self.__localization.getWord('password_show'), variable=self.__passwordCheckBoxValue,
                            onvalue=AddNewDB.CHECKBOX_VALUE_ON, offvalue=AddNewDB.CHECKBOX_VALUE_OFF, command=self.passwordCheckBoxCommand)
        c.pack(side=tk.LEFT, padx=AddNewDB.CHECKBOX_PAD_X, pady=AddNewDB.CHECKBOX_PAD_Y) 
        c.deselect()             
               
        #add buttons
        buttonsData = [{'text' : self.__localization.getWord('cancel'), 'command' : self.cancel, 'width' : AddNewDB.BUTTON_WIDTH},
                        {'text' : self.__localization.getWord('ok'), 'command' : self.ok, 'width' : AddNewDB.BUTTON_WIDTH}]
        for data in buttonsData:
            button = ttk.Button(self, text=data['text'], command=data['command'], width=data['width'])
            button.pack(side=tk.RIGHT, padx=AddNewDB.BUTTON_PAD_X, pady=AddNewDB.BUTTON_PAD_Y) 
    
    
    def chooseFile(self):
        ftypes = [('database file', '.db')]
        self.__path = asksaveasfilename(filetypes=ftypes, title=self.__localization.getWord('path_to_file'),
                                     defaultextension='.db') 
        self.__chooseFileButton.config(text=self.__path)         
        
    def ok(self):
        self.__controller.okPress()
        
    def cancel(self):
        self.__controller.cancelPress()      
        

    def passwordCheckBoxCommand(self ):
        val = self.__passwordCheckBoxValue.get()
        if val == AddNewDB.CHECKBOX_VALUE_OFF:
            self.__entryRef[DataField.PASSWORD].config(show = "*")
        else:
            self.__entryRef[DataField.PASSWORD].config(show = "")
        
       
    def getPath(self):
        return self.__path.encode('utf8') 
    
    
    def getPasswordEntry(self):
        return self.__entryRef[DataField.PASSWORD]
    
    def getNameEntry(self):
        return self.__entryRef[DataField.NAME]

    def getCommentsEntry(self):
        return self.__entryRef[DataField.COMMENTS]
