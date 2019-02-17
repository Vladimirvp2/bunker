"""Classes controllers for add new category dialog"""

from Common.Utilities import*
from GUI.Dialogs.Register import Register
import UsConfig as Config
import Common.Constants.Singal as Signal
import Common.Constants.DataField as DataField
from DataModel.Exceptions import*
import logging
import GUI.MessageDialog as md


from abc import ABCMeta, abstractmethod


class AddCategoryControllerI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def addView(self, view):
        "Add view to the controller"
        pass
       
    @abstractmethod
    def okPress(self):
        pass
    
    @abstractmethod
    def cancelPress(self):
        pass
    
    @abstractmethod
    def sendSingnal(self, data):
        """
        Send signal about adding a new category
        @type data: dict
        @param data: dictionary of parameters provided by user
        """
        pass
      
    
    
class AddCategoryController(AddCategoryControllerI):
    '''
    Controller for the add new category dialog
    '''
    def __init__(self, dbManager, notifier, localization):
        self.__dbManager = dbManager 
        self.__notifier = notifier
        self.__localization = localization
        self._view = None
        
        
    def addView(self, view):
        self._view = view
        
        
    def okPress(self):
        #get data from entries
        name = self._view.getName()
        comments = self._view.getComments()
        #check the provided data
        data = {}
        data[DataField.NAME] = name
        data[DataField.COMMENTS] = comments
        self._doFieldsCheck(**data)
        #if all is OK
        data = {}
        data[DataField.NAME] = name
        data[DataField.COMMENTS] = comments
        #send data to the main app controller
        self._view.destroy()
        self.sendSingnal(data)
        
        
    def cancelPress(self):
        self._view.destroy()
        
        
    def _doFieldsCheck(self, name, comments):
        if not self.__dbManager.checkEntryData(name, DataField.NAME):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('name'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
        
        if not self.__dbManager.checkEntryData(comments, DataField.COMMENTS):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('comments'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False   
        
        return True 
    
    def sendSingnal(self, data):
        self.__notifier.sendSignal(Signal.ADD_NEW_CATEGORY, data)    
        
        
    
