'''
Classes of edit category dialog
'''

from AddCategory import*
import Common.Constants.DataField as DataField
import Tkinter as tk



from abc import ABCMeta, abstractmethod



class EditCategoryI(object):
    """
    Edit category view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def setEditData(self, **data): 
        pass
    


class EditCategory(AddCategory, EditCategoryI):
    """Dialog for editing a category"""
    
    def __init__(self, controller, localization):
        self.__localization = localization
        AddCategory.__init__(self, controller, localization)

    def init(self):
        AddCategory.init(self)
        #set dialog title
        self.title(self.__localization.getWord('edit_category'))
        
    def setEditData(self, **args): 
        for key in args.keys():
            if key in self._refs.keys():
                #text widget for comments
                if key == DataField.COMMENTS:
                    self._refs[key].insert(tk.END, args[key] ) 
                else:
                    self._refs[key].insert(0, args[key] ) 
