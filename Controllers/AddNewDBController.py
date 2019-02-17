'''
Classes for add new DB dialog
'''

import Common.Constants.Singal as Signal
import Common.Constants.DataField as DataField
from tkMessageBox import *
import logging
import GUI.MessageDialog as md


from abc import ABCMeta, abstractmethod


class AddNewDBControllerI(object):
    """
    Controller interface 
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

    
    
    
    
class AddNewDBController(AddNewDBControllerI):
    '''
    Controller for the add new database dialog
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
        name = self.__view.getNameEntry().get().encode('utf8')
        password = self.__view.getPasswordEntry().get()
        comments = self.__view.getCommentsEntry().get("1.0",'end-1c').encode('utf8') 
        
        
        if self.checkUserValues(path, name, password, comments):
            data = {}
            data[DataField.PATH] = path
            data[DataField.PASSWORD] = password
            data[DataField.NAME] = name
            data[DataField.COMMENTS] = comments    
            self.__view.destroy()      
            self.__notifier.sendSignal(Signal.DB_ADD_NEW, data)
    
    def cancelPress(self):
        self.__view.destroy() 
        
        
    def checkUserValues(self, path, name, password, comments):
        if not self.__dbManager.checkEntryData(path, DataField.PATH):
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('path'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
        
        if not self.__dbManager.checkEntryData(name, DataField.NAME):
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('db_name'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
        
        if not self.__dbManager.checkEntryData(password, DataField.PASSWORD):
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('password'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
        
        if not self.__dbManager.checkEntryData(comments, DataField.COMMENTS):
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('comments'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False   
        
        return True    
