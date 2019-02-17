'''
Classes of controllers for add new record dialog
'''

from tkMessageBox import *
import logging
import Common.Constants.Singal as Signal
from abc import ABCMeta, abstractmethod
import Common.Constants.DataField as DataField
import GUI.MessageDialog as md



class AddRecordContollerI(object):
    """
    Add Record Controller interface 
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
    
    
class AddRecordController(AddRecordContollerI):
    '''
    Controller for the Add new record dialog
    '''
    def __init__(self, dbManager, notifier, localization):
        self.__dbManager = dbManager 
        self.__notifier = notifier
        self.__localization = localization
        self._view = None
        
    def addView(self, view):
        self._view = view 
        
         
    def okPress(self):    
        if self._checkData():
            logging.debug("Checking data OK")    
            #get the values from entries
            data = {}
            data[DataField.SITE] = self._view.getSite()
            data[DataField.USERNAME] = self._view.getUserName()
            data[DataField.EMAIL] = self._view.getEmail() 
            data[DataField.PASSWORD] = self._view.getPassword()
            data[DataField.COMMENTS] = self._view.getComments()
            #send data to the main app controller
            self.__notifier.sendSignal(Signal.ADD_NEW_RECORD, data)
            self._view.destroy()
               
               
    def cancelPress(self):
        self._view.destroy() 
       
        
    def _checkData(self):
        """Check if the user provided valid data"""
        #get the values from entries
        site = self._view.getSite()
        if len(site) == 0:
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = self.__localization.getWord('site_empty'), 
                            buttonsText=[self.__localization.getWord('ok')])

            return False
            
        if not self.__dbManager.checkEntryData(site, DataField.SITE):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('site'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
                           
        username = self._view.getSite() 
        if not self.__dbManager.checkEntryData(username, DataField.USERNAME):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('username'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
                   
        email = self._view.getEmail()
        if not self.__dbManager.checkEntryData(email, DataField.EMAIL):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('email'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False
                 
        password = self._view.getPassword()
        if not self.__dbManager.checkEntryData(password, DataField.PASSWORD):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('password'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False   
            
        comments = self._view.getComments()
        if not self.__dbManager.checkEntryData(comments, DataField.COMMENTS):
            md.showError(self._view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = "{} {}".format(self.__localization.getWord('comments'), self.__localization.getWord('contains_invalid_value')), 
                            buttonsText=[self.__localization.getWord('ok')])
            return False 
        
        return True       