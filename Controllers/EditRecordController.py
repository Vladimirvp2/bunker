'''
Classes of edit record controller
'''

from AddRecordController import*


class EditRecordController(AddRecordController):
    '''
    Controller for the Add new record dialog
    '''
    def __init__(self, dbManager, notifier, localization):
        self.__dbManager = dbManager 
        self.__notifier = notifier
        self.__localization = localization
        AddRecordController.__init__(self, dbManager, notifier, localization)
        
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
            self.__notifier.sendSignal(Signal.EDIT_RECORD, data)
            self._view.destroy()
