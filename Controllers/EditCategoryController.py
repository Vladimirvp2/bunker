'''
Classes of controller for edit category dialog
'''

from AddCategoryController import*

class EditCategoryController(AddCategoryController):
    '''
    Controller for the edit category dialog
    '''
    def __init__(self, dbManager, notifier, localization):
        self.__notifier = notifier
        AddCategoryController.__init__(self, dbManager, notifier, localization)
        
        
    def sendSingnal(self, data):
        self.__notifier.sendSignal(Signal.EDIT_CATEGORY, data) 