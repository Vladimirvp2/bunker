'''
Classes controllers of the main application window
'''

from abc import ABCMeta, abstractmethod
import logging, os
import Common.Constants.Singal as Signal
import Common.Constants.DBStatus as DBStatus
import Common.Constants.DBObjectType as DBObjectType
from tkFileDialog   import askopenfilename  
from Tkinter import *
import DataModel.Exceptions as Exceptions
import UsConfig as Config
import Common.Constants.DataField as DataField
import Common.Constants.DBStatus as DBStatus
import Common.Constants.EntryStatus as EntryStatus
from Common.Utilities import*
from Common.Constants import DataField
from Common.Notifier import Observer
from GUI.Dialogs.PasswordGenerate import PasswordGenerate

import GUI.MessageDialog as md


class MainWinControllerI(object):
    """Interface class for main window controller"""
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def addView(self, view):
        "Add view to the controller"
        pass
       
    
    
class MainWinController(MainWinControllerI, Observer):
    '''
    Controller implementation for the main application window
    '''
    def __init__(self, userConf, DBManager, notifier, localization):
        self.__userConfig = userConf 
        self.__dbManager = DBManager
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        
        self.__notifier.register(self)
        #Cache 
        self.__previousClickedCategory = None
        self.__previousSignal = None
        self.__currentDB = None
        self.__currentCategory = None 
        #image references dict(to keep them)
        self.__images = {}
        self.__resourceManager = Config.ASSEMBLER.assemble("ResourceManager")
        
            
        
    def addView(self, view):
        self.__view = view
        
        
    def update(self, signal, data=None):
        """
        Handler. Called if a signal is fired
        """
        logging.debug("Signal: {}, Data: {}".format(signal, data))
        #try:
        if signal == Signal.LOGIN_OK:
            self.loginOk(data)     
            
        elif signal == Signal.NEW_USER_REGISTER_OK:
            self.newUserRegisterOK(data)             
            
        elif signal == Signal.APP_QUIT:
            self.quitApp(data)
                    
        elif signal == Signal.NOT_YET_AVAILABLE:
            self.notImplementedYet(data)
        
        elif signal == Signal.CATEGORY_RIGHT_CLICK: 
            self.categoryRightClick(data)
        
        elif signal == Signal.RECORD_RIGHT_CLICK:                                
            self.__showRecordContextMenu(data)
        
        elif signal == Signal.RECORD_CLICK:
            self.recordPanelClicked(data)           
        
        elif (signal == Signal.CATEGORY_SINGLE_CLICK) or (signal == Signal.CATEGORY_DOUBLE_CLICK):                                
            self.categoryPanelClicked(signal, data)
                    
        elif signal == Signal.SHOW_ADD_NEW_RECORD_DIALOG: 
            self.showAddNewRecordDialog(data)                             
            
        elif signal == Signal.ADD_NEW_RECORD:                                
            self.addNewRecord(data)
        
        elif signal == Signal.SHOW_EDIT_RECORD_DIALOG:
            self.showEditRecordDialog(data)
        
        elif signal == Signal.EDIT_RECORD: 
            self.editRecord(data)                                       
        
        elif signal == Signal.REMOVE_RECORD:
            self.removeRecord(data)
        
        elif signal == Signal.SAVE_CURR_DB:
            self.saveDB()
                
        elif signal == Signal.DB_CONNECT:
            self.connectDB(data)    
        
        elif signal == Signal.DB_DISCONNECT:
            self.disconnectDB(data)
        
        elif signal == Signal.SHOW_ADD_NEW_CATEGORY_DIALOG:
            self.showAddNewCategoryDialod(data)
            
        elif signal == Signal.ADD_NEW_CATEGORY:
            self.addNewCategory(data)
        
        elif signal == Signal.SHOW_EDIT_CATEGORY_DIALOG:
            self.showEditCategoryDailog(data)
        
        elif signal == Signal.EDIT_CATEGORY:
            self.editCategory(data)
        
        elif signal == Signal.REMOVE_CATEGORY:
            self.removeCategory(data)
        
        elif signal == Signal.DB_ADD_EXISTING_SHOW_DIALOG:
            self.showAddExistingDBDialog(data)
        
        elif signal == Signal.DB_ADD_EXISTING:
            self.addExistingDB(data)
        
        elif signal == Signal.DB_ADD_NEW_SHOW_DIALOG:
            self.showAddNewDBDialog(data)
            
        elif signal == Signal.DB_REMOVE_FROM_FILE_SYSTEM:
            self.removeDBFromFileSystem(data)

        elif signal == Signal.DB_ADD_NEW:
            self.addNewDB(data)

        elif signal == Signal.DB_REMOVE_FROM_CONFIG:
            self.removeDBFromConfig(data)

        elif signal == Signal.DB_REMOVE_FROM_CONFIG:
            self.removeDBFromConfig(data)
            
        elif signal == Signal.SHOW_SETTINGS_DIALOG:
            logging.debug("Show add new DB dialog")
            #dialog = Config.ASSEMBLER.assemble("GenPasswordView")
            dialog = Config.ASSEMBLER.assemble("MergeDatabasesView")
            centerTopLevel(dialog)
            setWaitForClose(dialog)
            
    
            #w = PasswordGenerate()
            #d = md.showYesNo(self.__view, 'Error2', text = "Some text", buttonsText=['Yees', 'Noo'])
            #print d
         

        elif signal == Signal.SHOW_INFO_DIALOG:
            self.notImplementedYet(data)
            
        elif signal == Signal.SHOW_MANUAL:
            self.notImplementedYet(data)
                       
        #except Exception as e:
            #show message about critical error and write to file
            #showerror('Critical error', 'Critical error {}. \n Written to log file'.format(e))
        #    raise e 
        #    pass
        
        
    def loginOk(self, data):
        #show main window
        login = data[0]
        password = data[1] 
        self.__view.deiconify()
        #apply user settings
        self.__applyUserSettring()

        dbs = self.__userConfig.getCurrentUserDBs()
        #register each db by path id DB manager
        for db in dbs:
            try:
                self.__dbManager.registerDB(db[DataField.PATH], db[DataField.PASSWORD]) 
            except Exceptions.DataBaseException:
                pass
            
        #load users DBs and show them in the category panel
        self.__loadUserDBsToPanel()
        
        
    def newUserRegisterOK(self, data):
        logging.debug("New user added")
        login = data[0]
        password = data[1] 
        self.__view.deiconify()
        #apply user settings
        self.__applyUserSettring()
        self.__loadUserDBsToPanel()  
        
        
    def quitApp(self, data):
        logging.debug("Quitting the application")
        if not data:
            self.__view.quit()
        else:
            #show confirmation dialog
            res = md.showYesNo(self.__view, 
                    title = self.__localization.getWord('quit'),
                    text = self.__localization.getWord('do_you_want_to_quit_app'), 
                    buttonsText=[self.__localization.getWord('yes'), self.__localization.getWord('no')])             
            if res:
                self.__view.quit()                              
        
        
    def connectDB(self, data):
        """
        Connect to the given database
        @type data: DataBase
        @param data: reference of the database to which to connect
        """        
        logging.debug("Connecting to DB {}".format(data)) 
        db = self.__getCurrDB()
        #do checks
        if not db:
            return
        if db.status == DBStatus.CONNECTED:
            return
        categoryPanel = self.__view.getCategoryPanel()
        try:
            db.connect()
            #load root content to panels
            self.__loadSubcategoriesToPanel(db.id, None)
            self.__loadRecordsToPanel(db.id, None) 
            #change DB image to connected  
            categoryPanel.tree.item(db.id , open = True, image=self.__getImage('db_connected_image')) 
            #change text to db name if setting
            if (self.__userConfig.getCurrentUserSetting(DataField.CHANGE_DB_PATH_TO_NAME_AFTER_CONN) ):
                categoryPanel.tree.item(db.id , text=db.name) 
                
            self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, db)    
            
        except Exceptions.NoFileException:     
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = "{} {} {}".format(self.__localization.getWord('database_with_file'),
                                         db.path,
                                         self.__localization.getWord('no_exist')
                                         ), 
                buttonsText=[self.__localization.getWord('ok')]) 
             
        except Exceptions.DataBaseException: 
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = "{} {} {}".format(self.__localization.getWord('can_not_connect_to_db'),
                                         db.path,
                                         self.__localization.getWord('corrupted')
                                         ), 
                buttonsText=[self.__localization.getWord('ok')]) 
        except Exceptions.WrongPasswordException:
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = self.__localization.getWord('wrong_password_provided'),
                buttonsText=[self.__localization.getWord('ok')])                       
        
        
    def disconnectDB(self, data):
        """
        Disconnect given DB
        @type data: DataBase
        @param data: reference of the database to be disconnected 
        """
        logging.debug("Disconnecting from DB") 
        db = self.__getCurrDB()
        if not db:
            return
        if db.status == DBStatus.DISCONNECTED:
            return
        categoryPanel = self.__view.getCategoryPanel()
        #remove sub categories from DB
        rootEntries = db.getEntriesOfCategory(None)
        #db = self.__dbManager.findBDByID(rootEntries)
        for entry in rootEntries:
            if entry.type == DBObjectType.CATEGORY:
                if categoryPanel.tree.exists(entry.id):
                    categoryPanel.tree.delete(entry.id)
        
        db.disconnect()
        #clean record panel
        self.__cleanRecordPanel()
        #set disconnected image to DB
        categoryPanel.tree.item(db.id , image=self.__getImage('db_disconnected_image'))
        #change text to db name if setting
        categoryPanel.tree.item(db.id , text=db.path)  
        self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, db)
        
        
    def saveDB(self):
        """Save current DB"""
        logging.debug("Saving current DB")
        db = self.__getCurrDB()    
        if db:
            db.save() 
            db.deleteRemoved()
            logging.debug("Saving current db {} successfully".format(self.__currentDB)) 
            self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, db)
    
            
    def showAddExistingDBDialog(self, data):
        logging.debug("Show add existing DB dialog")
        dialog = Config.ASSEMBLER.assemble("AddExistingDBView")
        centerTopLevel(dialog)
        setWaitForClose(dialog)

        
    def  addExistingDB(self, data):
        logging.debug("Add existing DB with parameters {}".format(data))
        #add to config
        self.__userConfig.addDBForCurrentUser(data[DataField.PATH], data[DataField.PASSWORD])
        try:
            #add to DB manager
            db = self.__dbManager.registerDB(data[DataField.PATH], data[DataField.PASSWORD]) 
            #add to panel
            categoryPanel = self.__view.getCategoryPanel()
            categoryPanel.tree.insert("" , 'end', db.id,  text=db.path, image=self.__getImage('db_disconnected_image'), open=True )
        except Exceptions.DataBaseException:
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = self.__localization.getWord('db_exist'), 
                buttonsText=[self.__localization.getWord('ok')])  
                      
    
        logging.debug("Existing DB {} successfully added".format(data))
        
        
    def showAddNewDBDialog(self, data):
        logging.debug("Show add new DB dialog")
        dialog = Config.ASSEMBLER.assemble("AddNewDBView")
        centerTopLevel(dialog)
        setWaitForClose(dialog)
        
        
    def addNewDB(self, data):
        logging.debug("Add new DB with data {}".format(data)) 
        try:
            #create new DB add add it to DB manager
            #path, name, password, comments='')
            db = self.__dbManager.createDB(**data)
            #add new DB to config
            self.__userConfig.addDBForCurrentUser(data[DataField.PATH], data[DataField.PASSWORD])
            #add to the panel
            categoryPanel = self.__view.getCategoryPanel()
            categoryPanel.tree.insert("" , 'end', db.id,  text=db.path, image=self.__getImage('db_disconnected_image'), open=True )
        except Exceptions.DataBaseException:
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = self.__localization.getWord('db_exist'), 
                buttonsText=[self.__localization.getWord('ok')]) 
            
            
    def removeDBFromConfig(self, data):
        logging.debug("Removing DB from config")
        res = md.showYesNo(self.__view, 
                title = self.__localization.getWord('removing_db'),
                text = self.__localization.getWord('remove_db_from_config_question'), 
                buttonsText=[self.__localization.getWord('yes'), self.__localization.getWord('no')]) 
        if res:
            if self.__currentDB:
                #remove from category panel
                categoryPanel = self.__view.getCategoryPanel()
                categoryPanel.tree.delete(self.__currentDB.id)
                #remove from DB manager
                id = self.__currentDB.id
                path = self.__currentDB.path
                self.__dbManager.deleteDB(id)
                self.__setCurrentDB(None)
                #remove from userConfig            
                self.__userConfig.removeDBFromCurrentUser(path)
                
                logging.debug("Removing DB from config successfully")  
        
    
    def removeDBFromFileSystem(self, data):
        logging.debug("Remove selected DB from file system")
        if not self.__currentDB:
            return
        res = md.showYesNo(self.__view, 
                title = self.__localization.getWord('removing_db'),
                text = self.__localization.getWord('remove_db_from_filesystem_question'), 
                buttonsText=[self.__localization.getWord('yes'), self.__localization.getWord('no')])
        if res:
            if os.path.isfile(self.__currentDB.path.decode('utf8')):
                os.remove(self.__currentDB.path.decode('utf8'))
                #remove from DB manager
                self.__dbManager.deleteDB(self.__currentDB.id)
                #remove from userConfig            
                self.__userConfig.removeDBFromCurrentUser(self.__currentDB.path)
                #remove from panel
                categoryPanel = self.__view.getCategoryPanel()
                categoryPanel.tree.delete(self.__currentDB.id)
                #remove from file system
                #os.remove(self.__currentDB.path.decode('utf8')) 
                self.__setCurrentDB(None)
                 
            else:
                #remove from DB manager
                dbpath = self.__currentDB.path
                self.__dbManager.deleteDB(self.__currentDB.id)
                #remove from userConfig            
                self.__userConfig.removeDBFromCurrentUser(self.__currentDB.path)
                #remove from panel
                categoryPanel = self.__view.getCategoryPanel()
                categoryPanel.tree.delete(self.__currentDB.id)
                #remove from file system
                #os.remove(self.__currentDB.path.decode('utf8')) 
                self.__setCurrentDB(None)
                #show info dialog abot missing database file
                md.showInfo(self.__view, 
                title = self.__localization.getWord('removing_db'),
                text = "{} {}. {}".format(self.__localization.getWord('remove_db_from_filesystem_no_file'),
                                         dbpath,
                                         self.__localization.getWord('db_from_config_remove_ok')
                                         ), 
                buttonsText=[self.__localization.getWord('ok')])
                
            logging.debug("DB removed successfully from file system") 
                    
    
    
    def showAddNewCategoryDialod(self, data):
        logging.debug("Show add new category dialog")
        dialog = Config.ASSEMBLER.assemble("AddCategoryView")
        centerTopLevel(dialog)
        setWaitForClose(dialog)
        
        
    def addNewCategory(self, data):
        """
        Add new category to the data model and category panel
        @type data: dict
        @param data: dict of category fields got from user in the add category dialog 
        """
        logging.debug("Add new category to DB {} and category {}".format(self.__currentDB, self.__currentCategory))
        if self.__currentDB:
            #add category to data manager
            newID = self.__currentDB.addNewEntry(DBObjectType.CATEGORY, self.__currentCategory, **data)
            #add to category to panel
            categoryPanel = self.__view.getCategoryPanel()
            if self.__currentCategory:
                categoryPanel.tree.insert(self.__currentCategory, 'end', newID, text=data[DataField.NAME], image=self.__getImage('category_image'))
            else:
                categoryPanel.tree.insert(self.__currentDB.id, 'end', newID, text=data[DataField.NAME], image=self.__getImage('category_image'))   
                
            self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, self.__currentDB)
            self.__notifier.sendSignal(Signal.CATEGORY_SELECTED_CHANGED, newID)
                                                          
            logging.debug("Category {} successfully added".format(newID))          
        
                
            
    def showEditCategoryDailog(self, data):
        logging.debug("Showing edit category dialog")    
        categoryPanel = self.__view.getCategoryPanel()
        clickedItem = categoryPanel.tree.focus()
        if not clickedItem or not self.__currentDB:
            return            
        dialog = Config.ASSEMBLER.assemble("EditCategoryView")
        #init dialog with clicked category data 
        categoryObj = self.__currentDB.findEntryByID(clickedItem, DBObjectType.CATEGORY)
        data = categoryObj.getData()
        dialog.setEditData(**data) 
        #position dialog and set focus to it           
        centerTopLevel(dialog)
        setWaitForClose(dialog) 
               
        
    def editCategory(self, data):
        logging.debug("Editing category with data {}".format(data))  
                  
        categoryPanel = self.__view.getCategoryPanel()
        clickedItem = categoryPanel.tree.focus()
        if not clickedItem or not self.__currentDB:
            return 
        #edit category object
        categoryObj = self.__currentDB.findEntryByID(clickedItem, DBObjectType.CATEGORY) 
        categoryObj.edit(**data)
        #renew data in category panel
        categoryPanel.tree.item(clickedItem , text=categoryObj.name) 
        self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, self.__currentDB)
        self.__notifier.sendSignal(Signal.CATEGORY_SELECTED_CHANGED, categoryObj.id)
                
        logging.debug("Editing category with data {} successfully".format(data))
        
        for key in data.keys():
            print data[key]
        
        
    def removeCategory(self, data):
        logging.debug("Removing category")
        res = md.showYesNo(self.__view, 
                title = self.__localization.getWord('removing_category'),
                text = self.__localization.getWord('remove_category'), 
                buttonsText=[self.__localization.getWord('yes'), self.__localization.getWord('no')])
        
        if res:
            if self.__currentDB:
                categoryPanel = self.__view.getCategoryPanel()
                clickedItem = categoryPanel.tree.focus()
                if clickedItem:
                    #remove from data structure
                    self.__currentDB.removeEntry(DBObjectType.CATEGORY, clickedItem)
                    #remove from record panel
                    categoryPanel.tree.delete(clickedItem)
                    self.__setCurrentCategory(None)
                    self.__cleanRecordPanel()
                    
                    self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, self.__currentDB)
                    self.__notifier.sendSignal(Signal.CATEGORY_SELECTED_CHANGED, None)
                    
                    logging.debug("Removed category successfully {}".format(clickedItem))
                    
    
    def categoryRightClick(self, data):
        logging.debug("Right click on the category panel")
        
        categoryPanel = self.__view.getCategoryPanel()
        clickedItem = categoryPanel.tree.focus() 
        rootItem = self.__findRootOfPanel(clickedItem, categoryPanel.tree)
        #if click on the DB  
        if rootItem == clickedItem and clickedItem:
            #call DB context menu
            db = self.__dbManager.findBDByID(rootItem)  
            self.__showDBContextMenu(db, data)
        else:                                  
            if self.__currentDB:
                self.__showCategoryContextMenu(data) 
                    
                        
    
    def showAddNewRecordDialog(self, data): 
        logging.debug("Show add new record dialog")   
        
        dialog = Config.ASSEMBLER.assemble("AddRecordView")
        centerTopLevel(dialog)
        setWaitForClose(dialog)
        
        
    def addNewRecord(self, data):
        logging.debug("Add new record to DB {} and category {}".format(self.__currentDB, self.__currentCategory))
        if self.__currentDB:
            #add record to data manager
            newID = self.__currentDB.addNewEntry(DBObjectType.RECORD, self.__currentCategory, **data)
            #add record to panel
            recordPanel = self.__view.getRecordPanel()
            recordPanel.tree.insert("", 'end', newID, text=data[DataField.SITE], 
                                    values=(data[DataField.USERNAME], data[DataField.EMAIL], data[DataField.PASSWORD], data[DataField.COMMENTS])
                                    ) 
            
            self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, self.__currentDB)
            self.__notifier.sendSignal(Signal.RECORD_SELECTED_CHANGED, newID)
            
    def showEditRecordDialog(self, data):
        logging.debug("Show edit record dialog")
        
        recordPanel = self.__view.getRecordPanel()
        clickedItem = recordPanel.tree.focus()
        if not clickedItem or not self.__currentDB:
            return
        dialog = Config.ASSEMBLER.assemble("EditRecordView")
        centerTopLevel(dialog)
        #init dialod with records data 
        recordObj = self.__currentDB.findEntryByID(clickedItem, DBObjectType.RECORD)
        data = recordObj.getData()
        dialog.setEditData(**data)
        setWaitForClose(dialog)
        
    def editRecord(self, data):
        logging.debug("Editing record")     
               
        recordPanel = self.__view.getRecordPanel()
        clickedItem = recordPanel.tree.focus()
        if not clickedItem or not self.__currentDB:
            return 
        #edit record object
        recordObj = self.__currentDB.findEntryByID(clickedItem, DBObjectType.RECORD) 
        recordObj.edit(**data)
        #edit info in record panel
        self.__loadRecordsToPanel(self.__currentDB.id, self.__currentCategory)
          
        self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, self.__currentDB)
        self.__notifier.sendSignal(Signal.RECORD_SELECTED_CHANGED, recordObj.id)
        
        
    def removeRecord(self, data):
        logging.debug("Removing record")
        res = md.showYesNo(self.__view, 
                title = self.__localization.getWord('removing_record'),
                text = self.__localization.getWord('remove_record'), 
                buttonsText=[self.__localization.getWord('yes'), self.__localization.getWord('no')])
        
        if res:
            if self.__currentDB:
                recordPanel = self.__view.getRecordPanel()
                clickedItem = recordPanel.tree.focus()
                if clickedItem:
                    #remove from data structure
                    self.__currentDB.removeEntry(DBObjectType.RECORD, clickedItem)
                    #remove from record panel
                    recordPanel.tree.delete(clickedItem)
                    self.__setCurrentRecord(recordPanel.tree.focus())
                    
                    logging.debug("Removed record successfully {}".format(clickedItem)) 
                    
                    self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, self.__currentDB)
                    self.__notifier.sendSignal(Signal.RECORD_SELECTED_CHANGED, None)
                    
                    
    def recordPanelClicked(self, data):
        recordPanel = self.__view.getRecordPanel()
        clickedItem = recordPanel.tree.focus()
        self.__notifier.sendSignal(Signal.RECORD_SELECTED_CHANGED, clickedItem)                  
                           
                    
    def categoryPanelClicked(self, signal, data):
        categoryPanel = self.__view.getCategoryPanel()
        clickedItem = categoryPanel.tree.focus()
        
        logging.debug("Category item {} clicked. DB {}, parent {}".format(clickedItem, self.__currentDB, self.__currentCategory))
        
        #if no databases and categories selected
        if not clickedItem:
            return
        #cache to prevent from processing the same signal on the same object
        if self.__previousClickedCategory == clickedItem and  self.__previousSignal == signal:
            return
        
        #renew click cache
        self.__previousClickedCategory = clickedItem
        self.__previousSignal = signal
        #get DB            
        rootItem = self.__findRootOfPanel(clickedItem, categoryPanel.tree)
        db = self.__dbManager.findBDByID(rootItem) 
        #refresh current DB and category cache
        self.__setCurrentDB(db)          
        self.__setCurrentCategory(clickedItem)  
        #if DB clicked 
        if rootItem == clickedItem:
            self.__setCurrentCategory(None)
            
            logging.debug("DB with id {} clicked".format(clickedItem))
            #id db not connected yet
            if db.status == DBStatus.DISCONNECTED and signal == Signal.CATEGORY_DOUBLE_CLICK:
                self.connectDB(db)
                return
            
            elif db.status == DBStatus.DISCONNECTED and signal == Signal.CATEGORY_SINGLE_CLICK:
                self.__cleanRecordPanel()
                return
                
            elif db.status == DBStatus.CONNECTED:
                #load root records to the root panel 
                self.__loadRecordsToPanel(db.id, None)
        #if category clicked       
        else:
            #entries = db.getEntriesOfCategory(clickedItem)
            #load sub categories of a clicked category
            #if signal == Signal.CATEGORY_DOUBLE_CLICK:
                #load sub categories id double clicked
            self.__loadSubcategoriesToPanel(db.id, clickedItem)
            #categoryPanel.tree.item(clickedItem , open = True)
            #load records    
            self.__loadRecordsToPanel(db.id, clickedItem)
            
            logging.debug("Category with id {} in DB {} clicked".format(clickedItem, rootItem)) 
            
            
    def notImplementedYet(self, data):
        md.showError(self.__view, 
                title = self.__localization.getWord('not_implemented'),
                text = self.__localization.getWord('not_yet_available'), 
                buttonsText=[self.__localization.getWord('ok')])                            
           
        
    def __loadUserDBsToPanel(self):
            categoryPanel = self.__view.getCategoryPanel()
            dbs = self.__dbManager.getDataBases()
            for db in dbs:
                categoryPanel.tree.insert("" , 'end', db.id,  text=db.path, image=self.__getImage('db_disconnected_image'), open=True )
                
    def __applyUserSettring(self):
        pass
    
    def __findRootOfPanel(self, item, tree):
        p = tree.parent(item) 
        if not p:
            return item
    
        return  self.__findRootOfPanel(p, tree) 
    
                              
    def __loadSubcategoriesToPanel(self, dbID, categoryID):
        categoryPanel = self.__view.getCategoryPanel()
        db = self.__dbManager.findBDByID(dbID) 
        #load categories of DB root
        parent = categoryID
        if not categoryID:
            parent = dbID  
        entries = db.getEntriesOfCategory(categoryID)
        for entry in entries:
            if entry.type == DBObjectType.CATEGORY and entry.status != EntryStatus.REMOVED:
                #check if sub categories already added
                if not categoryPanel.tree.exists(entry.id):
                    #continue
                    categoryPanel.tree.insert(parent , 'end', entry.id,  text=entry.name, image=self.__getImage('category_image'))
                
                entriesLevel2 = db.getEntriesOfCategory(entry.id)
                for entryLevel2 in entriesLevel2:
                    if entryLevel2.type == DBObjectType.CATEGORY and entryLevel2.status != EntryStatus.REMOVED: 
                        if not categoryPanel.tree.exists(entryLevel2.id):
                            #continue
                            categoryPanel.tree.insert(entry.id , 'end', entryLevel2.id,  text=entryLevel2.name, image=self.__getImage('category_image'))                   
                
                #categoryPanel.tree.item(parent , open = True)
               
 
    def __loadRecordsToPanel(self, dbID, categoryID):
        #clean record panel
        recordPanel = self.__view.getRecordPanel()
        self.__cleanRecordPanel()
        #load entries of a given DB and category
        db = self.__dbManager.findBDByID(dbID)
        entries = db.getEntriesOfCategory(categoryID)
        
        for entry in entries:
            if entry.type == DBObjectType.RECORD and entry.status != EntryStatus.REMOVED:
                recordPanel.tree.insert("", 'end', entry.id, text=entry.site, values=(entry.username, entry.email, entry.password, entry.comments))
                 
        self.__notifier.sendSignal(Signal.RECORD_SELECTED_CHANGED, None)
                           
                
                
    def __showRecordContextMenu(self, event):
        recordPanel = self.__view.getRecordPanel()
        clickedItem = recordPanel.tree.focus()
        menu = Menu(self.__view, tearoff=0)
        if self.__currentDB:
            menu.add_command(label=self.__localization.getWord('add'), command=lambda : self.__notifier.sendSignal(Signal.SHOW_ADD_NEW_RECORD_DIALOG, None))
        if clickedItem:
            menu.add_command(label=self.__localization.getWord('edit'), command=lambda : self.__notifier.sendSignal(Signal.SHOW_EDIT_RECORD_DIALOG, None))
            menu.add_command(label=self.__localization.getWord('delete'), command=lambda : self.__notifier.sendSignal(Signal.REMOVE_RECORD, None))
        menu.post(event.x_root, event.y_root)
        
        
    def __showCategoryContextMenu(self, event):
        categoryPanel = self.__view.getCategoryPanel()
        clickedItem = categoryPanel.tree.focus()
        menu = Menu(self.__view, tearoff=0)
        if self.__currentDB and clickedItem:
            menu.add_command(label=self.__localization.getWord('add'), command=lambda : self.__notifier.sendSignal(Signal.SHOW_ADD_NEW_CATEGORY_DIALOG, None))
            menu.add_command(label=self.__localization.getWord('edit'), command=lambda : self.__notifier.sendSignal(Signal.SHOW_EDIT_CATEGORY_DIALOG, None))
            menu.add_command(label=self.__localization.getWord('delete'), command=lambda : self.__notifier.sendSignal(Signal.REMOVE_CATEGORY, None))
        menu.post(event.x_root, event.y_root)
        
        
    def __showDBContextMenu(self, db, event):
        menu = Menu(self.__view, tearoff=0)
        if  db.status == DBStatus.DISCONNECTED:
            menu.add_command(label=self.__localization.getWord('connect_db'), command=lambda : self.__notifier.sendSignal(Signal.DB_CONNECT, db),
                            image=self.__getImage('connected_image'), compound = LEFT)
            menu.add_command(label=self.__localization.getWord('disconnect_db'), state="disabled", command=lambda : self.__notifier.sendSignal(Signal.DB_DISCONNECT, db),
                             image=self.__getImage('disconnected_image'), compound = LEFT)
            menu.add_command(label=self.__localization.getWord('add_category'), state="disabled", command=lambda : self.__notifier.sendSignal(Signal.SHOW_ADD_NEW_CATEGORY_DIALOG, None))             
        else:
            menu.add_command(label=self.__localization.getWord('connect_db'), state="disabled", command=lambda : self.__notifier.sendSignal(Signal.DB_CONNECT, db),
                             image=self.__getImage('add_new_db_image'), compound = LEFT)
            menu.add_command(label=self.__localization.getWord('disconnect_db'), command=lambda : self.__notifier.sendSignal(Signal.DB_DISCONNECT, db),
                             image=self.__getImage('disconnected_image'), compound = LEFT)
            menu.add_command(label=self.__localization.getWord('add_category'), command=lambda : self.__notifier.sendSignal(Signal.SHOW_ADD_NEW_CATEGORY_DIALOG, None)) 
                           
        menu.add_command(label=self.__localization.getWord('remove_db_from_config'), command=lambda : self.__notifier.sendSignal(Signal.DB_REMOVE_FROM_CONFIG, None))
        menu.add_command(label=self.__localization.getWord('remove_db_from_filesystem'), command=lambda : self.__notifier.sendSignal(Signal.DB_REMOVE_FROM_FILE_SYSTEM, None))        
        menu.post(event.x_root, event.y_root) 
                         
        
    def __cleanRecordPanel(self):
        recordPanel = self.__view.getRecordPanel()
        for i in recordPanel.tree.get_children():
            recordPanel.tree.delete(i)
            
            
    def __getImage(self, value):
        if not value in self.__images.keys():
            self.__images[value] = PhotoImage(file=self.__resourceManager.getResource(value))
        return self.__images[value]        
    
    def __getCurrDB(self):
        return self.__currentDB
    
    def __getCurrentCategory(self):
        return self.__currentCategory 
    
    def __setCurrentDB(self, db):
        self.__currentDB = db
        self.__notifier.sendSignal(Signal.DB_SELECTED_CHANGED, db)
        
    def __setCurrentCategory(self, cat):
        self.__currentCategory = cat
        self.__notifier.sendSignal(Signal.CATEGORY_SELECTED_CHANGED, cat)
        
    def __setCurrentRecord(self, rec):
        self.__currentRecord = rec 
        self.__notifier.sendSignal(Signal.RECORD_SELECTED_CHANGED, rec)
        
                                           