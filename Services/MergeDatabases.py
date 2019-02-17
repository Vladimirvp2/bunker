'''
Classes to merge databases
'''


import sqlite3, logging
from DataModel.SQLConnectProvider import SQLiteConnectProvider
import Common.Constants.DataField as DataField
import Common.Constants.DBObjectType as DBObjectType
import Common.Constants.Table as Table
from DataModel.SQLqueries import *
from DataModel.DataEntries import DBEntryFactory
import UsConfig
from Tkinter import *
import Common.Constants.DatabaseMerge as DatabaseMerge
from Common.Notifier import *
import Common.Constants.Singal as Signal
import time

notify = Notifier()


class DBTreeCreator(object):
    """Parse a given DB and create tree structure of Categories and Records.
    dbID are default, id - real ids in DB
    """
    def __init__(self, sqlProvider):
        self.__SQLConnectProvider = sqlProvider
        self.__recordsDataAll = []
        self.__categoriesDataAll = []
        
        
    def getDBTree(self, file):
        #parse DB and create DB tree
        self.__loadCategoriesDataAll(file)
        self.__loadRecordsDataAll(file)
        #create root Category
        data = {DataField.DB_ID : None}
        root = DBEntryFactory.createEntry(DBObjectType.CATEGORY, id = None, **data)
        self.__builtLevel(root)
        
        return root
                
        
    def __builtLevel(self, parentObject):
        #add records
        data = self.__findRecordDataByParentID(parentObject.id)
        for d in data:
            id = d[DataField.DB_ID]
            del d[DataField.DB_ID]
            c = DBEntryFactory.createEntry(DBObjectType.RECORD, id, **d)
            parentObject.addnewEntry(c)
        
        #add child categories
        data = self.__findCategoryDataByParentID(parentObject.id)
        for d in data:
            id = d[DataField.DB_ID]
            del d[DataField.DB_ID]
            c = DBEntryFactory.createEntry(DBObjectType.CATEGORY, id, **d)
            parentObject.addnewEntry(c)
            
        for c in parentObject.entries:
            if c.type == DBObjectType.CATEGORY:     
                self.__builtLevel(c)
    
    
    def __loadCategoriesDataAll(self, file):
        #clean categories list
        self.__categoriesDataAll = []
        self.__SQLConnectProvider.open(file)
        data = self.__SQLConnectProvider.executeFetch(SQLQuery.SELECT_ALL_CATEGORIES)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        for d in data:
            self.__categoriesDataAll.append(d)
            logging.debug("category data added: {}".format(d))
            
            
    def __loadRecordsDataAll(self, file):
        #clean categories list
        self.__recordsDataAll = []
        self.__SQLConnectProvider.open(file)
        data = self.__SQLConnectProvider.executeFetch(SQLQuery.SELECT_ALL_RECORDS)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        for d in data:
            self.__recordsDataAll.append(d)
            logging.debug("record data added: {}".format(d))
            
            
    def __findCategoryDataByParentID(self, parentID):
        res = []
        for c in self.__categoriesDataAll:
            if c[DataField.PARENT] == parentID:
                res.append(c)
                
        return res
    
    
    def __findRecordDataByParentID(self, parentID):
        res = []
        for c in self.__recordsDataAll:
            if c[DataField.PARENT] == parentID:
                res.append(c)
                
        return res
    
    
    
    
class MergeDatabase(Observer):
    """Class to merge databases"""
    def __init__(self):
        #database objects
        self.__databases = []
        self.__DBTreeCreator = DBTreeCreator(SQLiteConnectProvider())
        self.__SQLConnectProvider = SQLiteConnectProvider()
        self.__mergeMode = DatabaseMerge.REWRITE_BY_NEWER
        #priority of the current DB than are create by merging
        self.__currPriority = DatabaseMerge.PRIORITY_MIN
        self.__userAnswer = 0
        notify.register(self)
        
        
    def setMergeMode(self, value):
        self.__mergeMode = value
        
        
    def update(self, signal, data):
        if signal == Signal.MERGE_DB_USER_ANSWER:
            self.__userAnswer  = data
        
        
    def merge(self, finishDB, databases, priorities= []):
        """
        Merge databases
        @type finishDB: DataBase
        @param finishDB: db result object 
        @type databases: list of DataBase
        @param databases: list of database objects to merge 
        """
        
        for db in databases:
            treeDB = self.__DBTreeCreator.getDBTree(db.file)
            self.__SQLConnectProvider.open(finishDB.file)
            
            self.__merge(finishDB.file, treeDB)
            
            self.__SQLConnectProvider.commit()
            self.__SQLConnectProvider.closeConnection()
            
            
            
    def mergeTe(self, resFile, dbToAddFile, priority):
        """
        Merge databases
        @type finishDB: DataBase
        @param finishDB: db result object 
        @type databases: list of DataBase
        @param databases: list of database objects to merge 
        """
        
        treeDB = self.__DBTreeCreator.getDBTree(dbToAddFile)
        self.__SQLConnectProvider.open(resFile)
        
        self.__merge(treeDB, priority)
        #renew current priority
        if self.__currPriority < priority:
            self.__currPriority = priority
        
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
        logging.debug("Merge finished successfully")
        
                   
    def __merge(self, parentObject, priority=DatabaseMerge.PRIORITY_MIN):
        """Merge two databases recursively"""
        for entry in parentObject.entries:
            if entry.type == DBObjectType.RECORD:
                self.__mergeRecord(entry, parentObject, priority)
                    
            elif entry.type == DBObjectType.CATEGORY:
                self.__mergeCategory(entry, parentObject, priority)
       
        #go inside each category recursively    
        for entry in parentObject.entries:
            if entry.type == DBObjectType.CATEGORY:
                self.__merge(entry, priority) 
                
                
    def __mergeRecord(self, entry, parentObject, priority=DatabaseMerge.PRIORITY_MIN):  
        query = ""
        if not parentObject.dbID:
            query = SELECT_ROOT_RECORDS_BY_SITE.format(entry.site)
        else:
            query = SELECT_NOROOT_RECORDS_BY_SITE.format(entry.site, parentObject.dbID)
            
        data = self.__SQLConnectProvider.executeFetch(query)
        #check if records are not duplicate
        if len(data) > 0:
            if self.__mergeMode == DatabaseMerge.REWRITE_BY_NEWER:
                query = ""
                if entry.timestamp > data[0][DataField.TIME]:
                    self.__updateRecord(entry, data[0][DataField.DB_ID])
                    logging.debug("Record rewrite by newer one, id: {}, site: {}".format(data[0][DataField.DB_ID],
                                                                                         entry.site))
            elif  self.__mergeMode == DatabaseMerge.REWRITE_BY_PRIORITY:
                if priority > self.__currPriority:
                    self.__updateRecord(entry, data[0][DataField.DB_ID])
                    logging.debug("Record rewrite by one with higher priority, id: {}, site: {}".format(data[0][DataField.DB_ID],
                                                                                         entry.site))
            #show message that duplicate records        
            elif  self.__mergeMode == DatabaseMerge.MANUALLY:
                notify.sendSignal(Signal.MERGE_DB_ASK_USER, []) #data, entry
                logging.debug("User answer: {}".format(self.__userAnswer))
                #if user answered for the new data
                if self.__userAnswer == 1:
                    self.__updateRecord(entry, data[0][DataField.DB_ID])
                    logging.debug("Record rewrite manually, id: {}, site: {}".format(data[0][DataField.DB_ID],
                                                                                         entry.site))
        else:
            #insert record
            #if root record
            if not parentObject.dbID:
                query = SQLQuery.INSERT_NEW_ROOT_RECORD.format(entry.site, entry.username, entry.email, 
                                                                  entry.password, entry.comments) 
            #not root record
            else:
                query = SQLQuery.INSERT_NEW_NOROOT_RECORD.format(parentObject.dbID, entry.site, entry.username, 
                                                                    entry.email, entry.password, entry.comments)
            #insert record
            self.__SQLConnectProvider.execute(query)
            #set new real dbID in result DB 
            entry.dbID = self.__SQLConnectProvider.getLastRowID()
            self.__SQLConnectProvider.commit()
            logging.debug('Add record: {}, dbID {}'.format(entry.site, entry.dbID) )
            
            
    def __mergeCategory(self, entry, parentObject, priority=DatabaseMerge.PRIORITY_MIN):     
        query = ""
        if not parentObject.dbID :
            query = SELECT_ROOT_CATEGORIES_BY_NAME.format(entry.name)
        else:
            query = SELECT_NOROOT_CATEGORIES_BY_NAME.format(entry.name, parentObject.dbID)                    
        data = self.__SQLConnectProvider.executeFetch(query)
        #check if category with such name already exist
        if len(data) > 0:
            logging.debug("Double categories!")
            #merge categories
            entry.dbID = data[0][DataField.DB_ID]
        #if there are no such category add
        else:
            #if root category
            if not parentObject.dbID :
                query = SQLQuery.INSERT_NEW_ROOT_CATEGORY.format(entry.name, entry.comments)
            #not root record
            else:
                query = SQLQuery.INSERT_NEW_NOROOT_CATEGORY.format(parentObject.dbID, entry.name, entry.comments)
            #insert category
            self.__SQLConnectProvider.execute(query)
            self.__SQLConnectProvider.commit()
            #renew it's id
            entry.dbID = self.__SQLConnectProvider.getLastRowID()
            logging.debug('Add category: {}, dbID {}'.format(entry.name, entry.dbID) ) 
                                        
                    
    def __updateRecord(self, entry, dbID):
        query = SQLQuery.UPDATE_RECORD.format(entry.site, entry.username, entry.email, 
                                              entry.password, entry.comments, dbID)
        self.__SQLConnectProvider.execute(query)
        self.__SQLConnectProvider.commit() 
        
                                      

class Listener(Observer):
    def __init__(self):
        notify.register(self)
        
    def update(self, signal, data):
        if signal == Signal.MERGE_DB_ASK_USER:
            time.sleep( 2 )  
            notify.sendSignal(Signal.MERGE_DB_USER_ANSWER, 1)             
        
    
        

if __name__ == "__main__":
    
    #root = Tk()
    #top = Toplevel(root)

    #root.mainloop()
    l = Listener()    
    m = MergeDatabase()
    m.setMergeMode(DatabaseMerge.MANUALLY)
    m.mergeTe( r'D:/Temp/db/mergetest.db', r'D:/Temp/db/mergetest2.db', 1)
    
    
    
#     c = DBTreeCreator(SQLiteConnectProvider())
#     data = c.getDBTree(r"D:/vova1.db")
#     print data.dbID
#     for c in data.entries:
#         print c.id, "Level1"
#         for c2 in c.entries:
#             print c2.dbID, "Level2"
#             for c3 in c2.entries:
#                 print c3.dbID, "Level3"



