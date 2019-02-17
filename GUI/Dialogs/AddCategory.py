"""Classes to implement add new category dialog"""

import Tkinter as tk
import ttk


from abc import ABCMeta, abstractmethod
import Common.Constants.DataField as DataField


class AddCategoryI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getName(self):
        "Return reference of the name entry"
        pass
    
    @abstractmethod
    def getComments(self):
        "Return reference of the comments entry"
        pass 
    
    
    
class AddCategory(tk.Toplevel, AddCategoryI):
    """Dialog for adding new category"""
    #=================================================================
    #Label name                 Entry name
    #Label comments             Text comments
    
    #   Ok button          Cancel button 
    #=================================================================
    LABEL_WIDTH = 10
    ENTRY_WIDTH = 35
    BUTTON_WIDTH = 16
    COMMENT_AREA_HIGHT = 2
    LABEL_PAD_X = 3
    BUTTON_PAD_X = 1
    BUTTON_PAD_Y = 3
    
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        #add self to controller
        self.__controller.addView(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self._refs = {}
        
        self.init()
        
    def init(self):
        #set dialog title
        self.title(self.__localization.getWord('add_new_category'))
        #add entries
        fields_data = {DataField.NAME : self.__localization.getWord('name'), DataField.COMMENTS : self.__localization.getWord('comments')}
        fields = [ DataField.NAME, DataField.COMMENTS ]
        for field in fields:
            row = tk.Frame(self)                        
            lab = tk.Label(row, width=AddCategory.LABEL_WIDTH, text=fields_data[field], anchor=tk.W, padx=AddCategory.LABEL_PAD_X)
            ent = None
            if field == DataField.COMMENTS:
                ent = tk.Text(row, height=AddCategory.COMMENT_AREA_HIGHT, width=AddCategory.ENTRY_WIDTH ) 
            else: 
                ent = tk.Entry(row,  width=AddCategory.ENTRY_WIDTH)
            self._refs[field] = ent   
            row.pack(side=tk.TOP, fill=tk.X)              
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
         
        #add buttons
        buttonsData = [{'text' : self.__localization.getWord('cancel'), 'command' : self.cancel, 'width' : AddCategory.BUTTON_WIDTH},
                        {'text' : self.__localization.getWord('ok'), 'command' : self.ok, 'width' : AddCategory.BUTTON_WIDTH}]
        for data in buttonsData:
            button = ttk.Button(self, text=data['text'], command=data['command'], width=data['width'])
            button.pack(side=tk.RIGHT, padx=AddCategory.BUTTON_PAD_X, pady=AddCategory.BUTTON_PAD_Y) 
               
        
    def ok(self):
        self.__controller.okPress()
        
    def cancel(self):
        self.__controller.cancelPress()      
            
       
    def getName(self):
        return self._refs[DataField.NAME].get().encode('utf8') 
    

    def getComments(self):
        return self._refs[DataField.COMMENTS].get("1.0",'end-1c').encode('utf8')  
