'''
Classes of controller to merge DB
'''


import logging
from GUI.MessageDialog import*
from abc import ABCMeta, abstractmethod

   
    
class MergeDatabasesControllerI(object):    
    
    __metaclass__ = ABCMeta
    
    
    @abstractmethod
    def addView(self, view):
        self.__view = view
        
    @abstractmethod        
    def addDBPress(self):
        pass
        
    @abstractmethod        
    def removeDBPress(self):
        pass
        
    @abstractmethod        
    def initDBList(self):
        pass
            
    @abstractmethod            
    def cancel(self):
        pass
        
    @abstractmethod        
    def startMerge(self):
        pass
        
    @abstractmethod        
    def showSetPriorityDialog(self):
        """Show dialog to set priority for a clicked item in the database priority list"""
        pass
        
    @abstractmethod        
    def noDBChosen(self):
        """Check whether the user has chosen some databases"""
        pass
        
    @abstractmethod        
    def allPrioritiesProvided(self):
        """Check whether priorities for all the databases are set"""
        pass
    
    @abstractmethod    
    def fillPriorityList(self):
        """Add chosen databases to the priority tree"""
        pass
    
    
    
    
class MergeDatabasesController(MergeDatabasesControllerI):
    
    DEFAULT_PRIORITY = -1
    
    def __init__(self, userConfig, dbManager, notifier, localization):
        self.__userConfig = userConfig
        self.__dbManager = dbManager
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        self.__allDBObject = []
        #list of tuples. first element is db object, second it's priority
        self.__mergeDBObjects = []
        #key is db object, priority is integer
    
    def addView(self, view):
        self.__view = view
        
        
    def addDBPress(self):
        index = self.__view.getDBAllSelected()
        #if no elements selected
        if index == None:
            return

        db = self.__allDBObject[index]
        
        #check whether DB already added
        for data in self.__mergeDBObjects:
            if db == data[0]:
                showWarning(self.__view, 
                title = self.__localization.getWord('warning'),
                text = self.__localization.getWord('db_already_added'), 
                buttonsText=[self.__localization.getWord('ok'),]) 
                return
            
        #add to chosen DBs
        self.__mergeDBObjects.append([db, self.DEFAULT_PRIORITY])
        #add to list widget  
        self.__view.insertIntoDBChoosenList(db.path)      
        
        
    def removeDBPress(self):
        index = self.__view.getDBChoosenSelected()
        #if no elements selected
        if index == None:
            return

        dbData = self.__mergeDBObjects[index]
        db = self.__mergeDBObjects[index][0]
        logging.debug("Remove db with path {}".format(db.path))
        
        #remove from list
        self.__view.removeFromDBChoosenList(index)
        #remove from chosen DB list
        self.__mergeDBObjects.remove(dbData)
        #disable remove button
        self.__view.enableRemoveDBButton(False)
        
        
    def initDBList(self):
        #set DBs
        self.__allDBObject = []
        dbs = self.__dbManager.getDataBases()
        for db in dbs: 
            self.__allDBObject.append(db) 
            self.__view.insertIntoDBAllList(db.path)
            
            
    def cancel(self):
        #show confirmation dialog
        res = showYesNo(self.__view, 
                title = self.__localization.getWord('quit'),
                text = self.__localization.getWord('do_you_want_to_quit_merge_wizard'), 
                buttonsText=[self.__localization.getWord('yes'), self.__localization.getWord('no')])             
        if res:
            self.__view.destroy()          
               
        
    def startMerge(self):
        #check all the provided data
        
        print "Merge Start"
        
        
    def showSetPriorityDialog(self):
        """Show dialog to set priority for a clicked item in the database priority list"""
        index = int(self.__view.getSelectedInPriorittyList())
        data = self.__mergeDBObjects[index]
        priority = showNumber(self.__view, 
                title = self.__localization.getWord('enter_number'),
                text = self.__localization.getWord('enter_priority'), 
                buttonsText=[self.__localization.getWord('ok'),]) 

        #if ask priority dialog canceled
        if priority == NUMBER_DIALOG_DEFAULT_VALUE:
            return

        #check if such priority already set
        if self.__priorityAlreadySet(index, priority):
            #show info dialog
            showError(self.__view, 
                title = self.__localization.getWord('error'),
                text = self.__localization.getWord('such_priority_already_used'), 
                buttonsText=[self.__localization.getWord('ok'),]) 
            return
        
        data[1] = priority
        self.__view.setPrioritySelectedInPriorityList(priority)
        
        
    def noDBChosen(self):
        """Check whether the user has chosen some databases"""
        if len(self.__mergeDBObjects) == 0:
            return True
        
        return False
        
        
    def allPrioritiesProvided(self):
        """Check whether priorities for all the databases are set"""
        for data in self.__mergeDBObjects:
            print "Priority", data[1]
            if data[1] == self.DEFAULT_PRIORITY:
                return False
            
        return True
    
    
    def fillPriorityList(self):
        """Add chosen databases to the priority tree"""
        for data in self.__mergeDBObjects:
            priority = data[1]
            file = data[0].path
            if data[1] == self.DEFAULT_PRIORITY:
                priority = 'not set'             
            self.__view.addDataInPriorityList(priority, file)
        
        
    def __priorityAlreadySet(self, index, value):
        for i in range(0, len(self.__mergeDBObjects)):
            data = self.__mergeDBObjects[i]
            #check if priority set and not the same db
            if value == data[1] and int(index) != i:
                return True
            
        return False   
