'''
Classes views for editing a record
'''

from AddRecord import*
import Common.Constants.DataField as DataField
import Tkinter as tk



from abc import ABCMeta, abstractmethod



class EditRecordI(object):
    """
    Edit record view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def setEditData(self, **data): 
        pass
    


class EditRecord(AddRecord, EditRecordI):
    """Dialog for editing a record"""
    
    def __init__(self, controller, localization):
        self.__localization = localization
        AddRecord.__init__(self, controller, localization)

    def init(self):
        AddRecord.init(self)
        #set dialog title
        self.title(self.__localization.getWord('edit_record'))
        
    def setEditData(self, **args): 
        for key in args.keys():
            if key in self._entryRefs.keys():
                #text widget for comments
                if key == DataField.COMMENTS:
                    self._entryRefs[key].insert(tk.END, args[key] ) 
                else:
                    self._entryRefs[key].insert(0, args[key] )                        