'''
Classes of controller for add existing database dialog
'''

from Common.Utilities import*
from GUI.Dialogs.Register import Register
import UsConfig as Config
import Common.Constants.Singal as Signal
import Common.Constants.DataField as DataField
from DataModel.Exceptions import*
import logging
import GUI.MessageDialog as md


from abc import ABCMeta, abstractmethod


class AddExistingDBControllerI(object):
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
        "Call if login button pressed"
        pass
    
    @abstractmethod
    def cancelPress(self):
        "Call if cancel button pressed or dialog corner close button"
        pass

    
    
    
    
class AddExistingDBController(AddExistingDBControllerI):
    '''
    Controller for the add existing database dialog
    '''
    def __init__(self, dbManager, notifier, localization):
        self.__dbManager = dbManager 
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        
    def addView(self, view):
        self.__view = view
        
    def okPress(self):
        #check user values
        path = self.__view.getPath()
        password = self.__view.getPassword()
        
        if self.checkUserValues(path, password):
            data = {}
            data[DataField.PATH] = path
            data[DataField.PASSWORD] = password    
            self.__view.destroy()      
            self.__notifier.sendSignal(Signal.DB_ADD_EXISTING, data)
    
    def cancelPress(self):
        self.__view.destroy() 
        
        
    def checkUserValues(self, path, password):
        #check path
        if not self.__dbManager.dbPathUniqueCheck(path):
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = self.__localization.getWord('db_exist'), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
        
        #check password
        if not self.__dbManager.checkEntryData(password, DataField.PASSWORD):
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('password'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False 
        
        return True            
