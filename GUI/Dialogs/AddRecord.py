'''
Classes for adding a new record into category
'''

import Tkinter as tk
import ttk
from abc import ABCMeta, abstractmethod
import Common.Constants.DataField as DataField



class AddRecordI(object):
    """
    Add record view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getSite(self):
        pass
    
    @abstractmethod
    def getUserName(self):
        "Return reference of the username entry"
        pass
    
    @abstractmethod
    def getEmail(self):
        "Return reference of the email entry"
        pass
    
    @abstractmethod
    def getPassword(self):
        "Return reference of the password entry"
        pass
    
    @abstractmethod
    def getComments(self):
        "Return reference of the comments entry"
        pass 
          
    
    
class AddRecord(tk.Toplevel, AddRecordI):
    """Dialog for adding a new record"""

    # ----------------------------------------------
    # Label1                        Entry1
    # Label2                        Entry2 
    # ....
    # CheckBox(Show password)  OK    Cancel
    #-----------------------------------------------
    #constants
    LABEL_WIDTH = 12
    ENTRY_WIDTH = 30
    ROW_PAD_X = 2
    ROW_PAD_Y = 1
    COMMENT_AREA_HIGHT = 2
    OK_BUTTON_WIDTH = 14
    CANCEL_BUTTON_WIDTH = 14
    BUTTON_PAD_X = 2
    BUTTON_PAD_Y = 3
    CHECKBOX_VALUE_ON = '1'
    CHECKBOX_VALUE_OFF = '0'
    
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        #add self to controller
        self.__controller.addView(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.__passwordCheckBoxValue = None
        self._entryRefs = {}
        self.init()
        
        
    def init(self): 
        #set dialog title
        self.title(self.__localization.getWord('add_new_record'))

        fields_data = {DataField.SITE : self.__localization.getWord('site'),
                  DataField.EMAIL : self.__localization.getWord('email'),
                  DataField.USERNAME : self.__localization.getWord('username'),
                  DataField.PASSWORD : self.__localization.getWord('password'),
                  DataField.COMMENTS : self.__localization.getWord('comments')}
        fields = [DataField.SITE, DataField.EMAIL, DataField.USERNAME, DataField.PASSWORD, DataField.COMMENTS]
        #add entries
        for field in fields:
            row = tk.Frame(self)                        
            lab = tk.Label(row, width=AddRecord.LABEL_WIDTH, text=fields_data[field], anchor=tk.W, padx=AddRecord.ROW_PAD_X)  
            #if password field
            if field == DataField.PASSWORD:  
                ent = tk.Entry(row, show="*", width=AddRecord.ENTRY_WIDTH )
            elif field == DataField.COMMENTS:
                ent = tk.Text(row, height=AddRecord.COMMENT_AREA_HIGHT, width=AddRecord.ENTRY_WIDTH )
            else:
                ent = tk.Entry(row,  width=AddRecord.ENTRY_WIDTH )
            row.pack(side=tk.TOP, fill=tk.X)              
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X, padx=AddRecord.ROW_PAD_X, pady=AddRecord.ROW_PAD_Y)
            self._entryRefs[field] = ent
            
        #add password check box
        self.__passwordCheckBoxValue = tk.StringVar()
        c = tk.Checkbutton( self, text=self.__localization.getWord('password_show'), variable=self.__passwordCheckBoxValue,
                            onvalue=AddRecord.CHECKBOX_VALUE_ON, offvalue=AddRecord.CHECKBOX_VALUE_OFF, command=self.passwordCheckBoxCommand)
        c.pack(side=tk.LEFT, padx=1, pady=3) 
        c.deselect() 
        #add buttons
        buttonsData = [{'text' : self.__localization.getWord('cancel'), 'command' : self.cancel, 'width' : 14},
                       {'text' : self.__localization.getWord('ok'), 'command' : self.ok, 'width' : 14} ]
        for data in buttonsData:
            button = ttk.Button(self, text=data['text'], command=data['command'], width=data['width'])
            button.pack(side=tk.RIGHT, padx=AddRecord.BUTTON_PAD_X, pady=AddRecord.BUTTON_PAD_Y)
            
                      
            
    def passwordCheckBoxCommand(self ):
        val = self.__passwordCheckBoxValue.get()
        if val == AddRecord.CHECKBOX_VALUE_OFF:
            self._entryRefs[DataField.PASSWORD].config(show = "*")
        else:
            self._entryRefs[DataField.PASSWORD].config(show = "")
                    
            
    def ok(self):
        self.__controller.okPress()
        
    def cancel(self):
        self.__controller.cancelPress()
        
        
    def getSite(self):
        return self._entryRefs[DataField.SITE].get() 
    
    def getUserName(self):
        return self._entryRefs[DataField.USERNAME].get()
    
    def getEmail(self):
        return self._entryRefs[DataField.EMAIL].get()
    
    def getPassword(self):
        return self._entryRefs[DataField.PASSWORD].get()
    
    def getComments(self):
        return self._entryRefs[DataField.COMMENTS].get("1.0",'end-1c')        

      
if __name__ == '__main__':
    pass
                 
