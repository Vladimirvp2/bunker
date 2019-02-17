'''
Database Manager classes 
'''
 
import re, os, logging
from DataEntries import Category, Record
from SQLqueries import SQLQuery 
import Exceptions

import Common.Constants.DataField as DataField
import Common.Constants.EntryStatus as EntryStatus
import Common.Constants.DBObjectType as DBObjectType
import Common.Constants.DBStatus as DBStatus
import Common.Constants.DataField as DataField
from UsConfig import* 
from Common.Utilities import *

from DataBase import SQLDataBase

class DataBaseManager():
    '''Data Manager contains and manages all the user databases'''

    def __init__(self):
        # container for databases
        self._databases = []

        
    @staticmethod    
    def getNextID():
        """
        Generate the next unique BD id
        @rtype: string
        @return: next unique id for BD        
        """    
        return generateUniqueID()    
          
                                  
    
    def createDB(self, path, name, password, comments=''):
        """
        Create a new BD object and add it to the DB-list. Init structure for a new database with the provided metadata
        @type  path: string
        @param path: path to the database file with filename       
        @type  name: string
        @param name: name of the new database
        @type  password: string
        @param password: password the new database        
        @type  comments: string
        @param comments: comments for the new database 
        @return new DB object
        @raise WrongPathException: if the given path doesn't exist
        @raise ExistFileException: if the file with such name already exists                       
        """       
            
        db = SQLDataBase(DataBaseManager.getNextID(), path, name, password, comments)
        db.createDB()
        self._databases.append(db) 
        
        return db      
    
    
    def registerDB(self, file, password):
        """
        Create the database object and add it
        @type  file: string
        @param file: db file
        @type  password: string
        @param password: password of the database
        @return DataBase object                       
        @raise DataBaseException: if a database with such file already registered
        """  
        logging.debug('Registering the DB with file: {}'.format(file)) 
        #check if the file exist
        #if not os.path.isfile(file):
        #    raise Exceptions.NoFileException(file, "Database with such file doesn't exist")        
              
        #check if a database with such file already registered
        for db in self._databases:
            if db.path == file:
                raise Exceptions.DataBaseException(file, "Database with such file already registered")  
        
        #Create db if all is ok and add to the db container
        data = {}
        data[DataField.PASSWORD] = password
        db = SQLDataBase(DataBaseManager.getNextID(), file, **data)
        self._databases.append(db)
        logging.debug('The DB with file: {} and id {} successfully registered'.format(file, db.id))
        
        return db
            
          
    
    def findBDByID(self, dbID):
        """
        Check if the db with the given id added to the data model
        @type  dbID: string
        @param dbID: unique id of the database
        @type: DataBase
        @return: DataBase object          
        @raise DataBaseException: if the DB object with the given id doesn't exist                     
        """
        
        logging.debug("Finding DB object with id {}".format(dbID))    
        #find the DB
        db = None
        for b in self._databases: 
            if b.id == dbID:
                db = b
                break
            
        if not db:
            raise Exceptions.DataBaseException(dbID, "Database with such id doesn't exist in model") 
        
        return db
    
    def checkEntryData(self, value, type):
        """
        Check whether values are valid. Is used by adding new entry to check dates, provided by user
        @type value: string
        @type value: what should be checked
        @type type: DataField
        @type type: type of value 
        @return boolean
        """ 
        if type == DataField.SITE:
            pattern = re.compile(SITE_PATTERN)
            result = pattern.findall(value)
            if len(result) == 1 and len(result[0]) == len(value):
                return True
            return False
        
        return True
    

    def checkDBPassword(self, password):
        """
        Checks if the provided password contains valid values
        @type password: string
        @return: boolean 
        """
        pattern = re.compile('[-0-9a-zA-Z_\.]+')
        result = pattern.findall(password)
        if len(result) == 1 and len(result[0]) == len(password):
            return True        
        
        return False     

        
    def dbPathUniqueCheck(self, path):
        """
        Check if DB with such path already exists
        @type path: string
        @param path: path to the DB file that needs be checked
        @return: boolean. True if not duplicate, otherwise False  
        """ 
        for db in self._databases:
            if db.path == path:
                return False
            
        return True
    
               
    def deleteDB(self, id):
        """
        Delete db from db list
        @type id: string
        @param id: id of the database
        """
        for db in self._databases:
            if db.id == id:
                self._databases.remove(db)
                return
             
            
    def getDataBases(self):
        return self._databases     




if __name__ == '__main__':
    DM = DataBaseManager()
    DM.createDB(r'D:/vova20.db', "moon2", '123', comments='comments')   
    
    argsCat1 = {DataField.DB_ID : '1', DataField.NAME : 'name1', DataField.COMMENTS : 'comments1'}
    argsCat2 = {DataField.DB_ID : '2', DataField.NAME : 'name2', DataField.COMMENTS : 'comments2'}
    argsRec1 = {DataField.DB_ID : '1', DataField.SITE : 'site1', DataField.USERNAME : 'username1', DataField.EMAIL : 'email1',
                         DataField.PASSWORD : 'password1', DataField.COMMENTS : 'comments1' }
#     argsRec2 = {DataField.DB_ID : '2', DataField.SITE : 'site2', DataField.USERNAME : 'username2', DataField.EMAIL : 'email2',
#                         DataField.PASSWORD : 'password2', DataField.COMMENTS : 'comments2' } 
#     
#     DM = DataBaseManager()
#     DM.createDB(r"D:/basa3.db", "basa1", "pass1", "comm")
#     dbdata = [r"D:/basa3.db", ]
#     # dbdata = DM.getDBasesDataFromConfig('file.txt')
#     # print dbdata
#     #DM.registerDB(dbdata[0])
    basa = DM.findBDByID('1')
    print basa
    idCatRoot = basa.addNewEntry(DBObjectType.CATEGORY, None, **argsCat1)
    idCatRoot2 = basa.addNewEntry(DBObjectType.CATEGORY, None, **argsCat2)
    basa.save()
    rec3 = basa.addNewEntry(DBObjectType.CATEGORY, idCatRoot, **argsCat2)
    basa.save()
    basa.addNewEntry(DBObjectType.RECORD, rec3, **argsRec1)
    print basa.getIfChanged()
#     # print 10
#     a = basa.getEntriesOfCategory(None)
#     # 
#     # for entry in a:
#     #     print entry
#     #     
#     idCatRoot = basa.addNewEntry(DBObjectType.CATEGORY, None, **argsCat1)
#     basa.addNewEntry(DBObjectType.RECORD, None, **argsRec1)
#     # 
#     idCatLev1 = basa.addNewEntry(DBObjectType.CATEGORY, idCatRoot, **argsCat2)
#     basa.addNewEntry(DBObjectType.RECORD, idCatRoot, **argsRec2)   
#     # 
#     # a = basa.getEntriesOfCategory(idCatRoot)
#     # 
#     # for entry in a:
#     #     print entry
#     #     
#     #     
#     basa.save()
#     # 
#     # basa.removeEntry(DBObjectType.CATEGORY, idCatLev1)
#     # basa.deleteRemoved()
#     # basa.save()
#            
