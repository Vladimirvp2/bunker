'''
Databases module. Contains database base class, databases implementations
'''

from DataEntries import Category, Record
from SQLqueries import SQLQuery
import logging, os
import Exceptions
from SQLConnectProvider import SQLiteConnectProvider

import Common.Constants.EntryStatus as EntryStatus
import Common.Constants.DBObjectType as DBObjectType
import Common.Constants.DBStatus as DBStatus
import Common.Constants.DataField as DataField
import Common.Constants.Default as Default
from Common.Utilities import *


class DataBase(object): 
    """
    Database base class
    """
    def __init__(self, id, path, name=Default.DEFAULT_DB_NAME, password=Default.DEFAULT_DB_PASSWORD, comments = Default.DEFAULT_DB_COMMENT):
        self.__id = id
        self.__path = path
        self.__name = name
        self.__comments = comments
        self.__password = password
        self.__status = DBStatus.DISCONNECTED
        #container for categories and records
        self.__content = []

        
    def __str__(self):
        return 'DB-> id: {}'.format(self.__id)
        #return 'DB-> id: {}, path: {}, name: {}, password: {}, comments: {}'.format(self.__id, self.__path,
        #                                                              self.__name, self.__password, self.__comments) 
               
        
    def info(self):
        '''Info about DB current field values
        @rtype: string
        @return: field values
        '''
        return self.__str__()    
        
    def removeEntry(self, type, entryID):   
        """
        Removes an entry by a given id. The method doesn't deletes the entry from the database. It only sets its status
        and the statuses of its children(in case of a category) to REMOVED.
        The deleteRemoded method deletes the entries with the status REMOVED entirely from the DB and its objects
        @type  type: DBObjectType
        @param type: DBObjectType, see Settings.Constants
        @type  entryID: string
        @param entryID: id of the entry to remove       
        @type  args: dict of strings
        @param args(site, username, email, password, comments): data for a new record.
               args(name, comments): data for a new category.  
        @raise NoneObjectException: if the entry is with such id doesn't exist or is None 
        """
        
    def createDB(self):    
        """
        Creates a new database with the provided(constructor) metadata
        @raise WrongPathException: if the given path doesn't exist
        @raise ExistFileException: if the file with such name already exists         
        """
        pass
    
    def connect(self):
        """
        Connects to the DB, load DB metadata (name, comments)   
        @raise NoFileException: if the DB file doesn't exist 
        @raise DataBaseException: if the DB is corrupted        
        """
        pass
    
    
    def disconnect(self):
        """
        Disconnect a database  
        @raise DataBaseException: if the DB already disconnected           
        """
        
        if self.status == DBStatus.DISCONNECTED:
            raise Exceptions.DataBaseException(self.info(), "The DB already disconnected")
        
        logging.debug('Disonnecting from the DB: {}'.format(self.info))
        self.status = DBStatus.DISCONNECTED
        #remove DB content without deleting entries from DB file
        self.__content = []
        
        
    def save(self):
        """
        Save changed and inserted entries to DB file
        @raise NoFileException: if no file of the DB exist 
        """
        pass
    
    
    def editMetadata(self, **args):
        """
        Set new metadata info(DB name, comments)
        Password is unchangeable
        """
           
        if DataField.NAME in args.keys():
            self.__name = args[DataField.NAME]
        if DataField.COMMENTS in args.keys():
            self.__comments = args[DataField.COMMENTS]
        #if DataField.PASSWORD in args.keys():
        #    raise Exceptions.DataBaseException("{}".format(args[DataField.PASSWORD]), "Password of the DB can't be changed!") 
        # let change the password if the current one is default. Otherwise raise exception DataBaseException
        #if DataField.PASSWORD in args.keys():
        #    pass
            #if self.__password == Default.DEFAULT_DB_PASSWORD:
            #self.__password = args[DataField.PASSWORD]
            #else:
            #    if self.status == DBStatus.CONNECTED:
            #        raise Exceptions.DataBaseException("", "Password of the DB can't be changed more than 1 time!")        
    
    
    def addNewEntry(self, type, parentEntryID, **args):
        """
        Create and add a new entry(category/record) to data tree(not to DB)      
        @type  type: DBObjectType
        @param type: DBObjectType, see Settings.Constants
        @type  parentEntryID: string
        @param parentEntryID: id of the parent category. If added to root, provide None        
        @type  args: dect of strings
        @param args(site, username, email, password, comments): data for a new record.
               args(name, comments): data for a new category.                       
        @rtype: string
        @return: unique id of the added entry
        @raise NoneObjectException: if the parent with such id doesn't exist 
        @raise EntryException: if try to add to the record. New entries can be added only to categories        
        """  
        pass               
 
    def editEntry(self, type, entryID, **args):
        """
        Edit existing entry
        @type  type: DBObjectType
        @param type: DBObjectType, see Settings.Constants
        @type  entryID: string
        @param entryID: id of the entry to change
        @type  args: dict of parameters that need to be changed
        @param args: for a category(name, comments). For a record(site, username, email, password, comments)
        @raise NoneObjectException: if the object with the given id doesn't exist                
        """  
        pass  

    
    def getEntriesOfCategory(self, catID):
        """
        Return the list of entries(categories and records) of
        the given category by it's id        
        @type  catID: string
        @param catID: unique id of the given category.
                      None if the root category of DB         
        @rtype: list of Entry
        @return: list of entries
        @raise NoneObjectException: if no entry object with given id found. catID = None is ok - root category         
        """   
        
        pass
        
    
    def findEntryByID(self, entryID, type):
        """
        Find the entry object in a given database
        @type  catID: string
        @param catID: unique id of the entry
        @type type: DBObjectType
        @param type: type of the object
        @return: Entry object. None if no entry found. If type is None find all types of entries                                    
        """
        
        if not entryID:
            raise Exception.EntryException(entryID, "Entry with such id doesn't exist")
        
        res =  self.__findEntry(entryID, self, type)  
        return res
    
    
    def getIfChanged(self):
        return self.__findChangedEntry(self)
     
        
    def addnewEntry(self, entry):
        """
        @type  entry: Entry
        @param entry: entry to add 
        """        
        self.__content.append(entry)      
    
    
    def _loadEntriesOfCategory(self, cat):
        """
        load and put entries from a given database to data tree
        @type  cat: Category
        @param cat: category object. None if parent category         
        @raise EntryException: if the cat object doesn't exist                           
        """ 
        
        pass
 
    def _getNextEntryID(self):
        """
        Generate the next unique record/category id
        @rtype: string
        @return: next unique id for BD        
        """        
 
        return generateUniqueID()
    
    
    def _removeCategory(self, parentEntry ):
        """
        Recursively removes current category and it's entities(sets status to REMOVED)
        """
        if (parentEntry):
            logging.debug( "Recursive removing category {}".format(parentEntry.info()))
            parentEntry.status = EntryStatus.REMOVED  
            
        for child in parentEntry.entries:
            self._removeCategory(child)
    
        return 
 
 
    def __findEntry(self, entryID, parentEntry, type):
        """
        Recursively finds the entry by provided id and type
        """
        #if no type given find all types of entries except database type
        if not type:
            if parentEntry.id == entryID and parentEntry.type != DBObjectType.DATABASE:
                return parentEntry
        elif ( (parentEntry.id == entryID) and (parentEntry.type == type) ):
            return parentEntry
            
        res = None
        for child in parentEntry.entries:
            res = self.__findEntry(entryID, child, type)
            if res:
                return res     
        return res   
    
    
    def __findChangedEntry(self, parentEntry):                 
        if  parentEntry and (parentEntry.type != DBObjectType.DATABASE): 
            if parentEntry.status != EntryStatus.SAVED:
                return True
            
        if (parentEntry.type == DBObjectType.CATEGORY) or (parentEntry.type == DBObjectType.DATABASE):
            for entry in parentEntry.entries:
                res = self.__findChangedEntry(entry)
                if res:
                    return True
        return False 
    
           
    @property
    def id(self):
        return self.__id
    
    @property
    def path(self):
        return self.__path           
        
    @property
    def name(self):
        return self.__name
        
    @property
    def comments(self):
        return self.__comments
       
    @property
    def password(self):
        return self.__password
        
    @property
    def status(self):
        return self.__status
    
    @status.setter
    def status(self, value):
        self.__status = value   
    
        
    @property
    def entries(self):
        return self.__content
    
    @property
    def type(self):
        return DBObjectType.DATABASE                                
  


#=====================================================================================

class SQLDataBase(DataBase):
    '''Database class based on SQLite'''
    def __init__(self, id, path, name=Default.DEFAULT_DB_NAME, password=Default.DEFAULT_DB_PASSWORD, comments = Default.DEFAULT_DB_COMMENT):
        DataBase.__init__(self, id, path, name, password, comments)
        self.__SQLConnectProvider = SQLiteConnectProvider() 
        
        
    def createDB(self):
        #logging.debug('Creating DB with parameters: path:{}, name:{}, password:{}, comments:{} '.format(self.path, self.name, self.password, self.comments))
        
        #check if the given dir of the path is correct
        dir = os.path.dirname(self.path.decode('utf8'))
        if not os.path.exists(dir):
            raise Exceptions.WrongPathException(dir, "Path doesn't exist")
        
        #check if the given file already exist
        if os.path.isfile(self.path.decode('utf8')):
            raise Exceptions.ExistFileException(self.path, "File already exists")
        
        query = SQLQuery.FOREIGN_KEY_ON
        self.__SQLConnectProvider.open(self.path)
        self.__SQLConnectProvider.execute(query)
        
        #Create metadata table
        query = SQLQuery.CREATE_METADATA_TABLE
        logging.debug('Creating metadata table by query: {}'.format(query))
        self.__SQLConnectProvider.execute(query)        
        
        #Insert start info inside the metadata table
        query = SQLQuery.INSERT_INTO_METADATA_TABLE.format( self.name, self.password, self.comments) 
        logging.debug('Inserting metadata by query: {}'.format(query))       
        self.__SQLConnectProvider.execute(query)     
        
        #Create category table
        query = SQLQuery.CREATE_CATEGORY_TABLE
        logging.debug('Creating category table by query: {}'.format(query)) 
        self.__SQLConnectProvider.execute(query)        
        
        #Create record table
        query = SQLQuery.CREATE_RECORD_TABLE
        logging.debug('Creating records table by query: {}'.format(query))         
        self.__SQLConnectProvider.execute(query) 
                            
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()        
        
        logging.debug('''Created DB with data {}'''.format(self.info()))
        
        return self   
    
    
    def connect(self):
        #in already connected ignore
        if self.status == DBStatus.CONNECTED:
            return
            #raise Exceptions.DataBaseException(self.info(), "DB already connected ")
        
        #check path 
        if not os.path.isfile(self.path.decode('utf8')):
            raise Exceptions.NoFileException(self.path, "Can't connect to the DB: Such file in database doesn't exist")
        #connect to the db
        logging.debug('Connecting to the DB with file'.format(self.path)) 
        
        #load it's metadata and put it to DB object
        query = SQLQuery.SELECT_FROM_METADATA 
        self.__SQLConnectProvider.open(self.path)
        data = self.__SQLConnectProvider.executeFetch(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        if not data or len(data) == 0:
            raise Exceptions.DataBaseException(self.info(), "The Database doesn't have metadata") 

        #check password
        if data[0][DataField.PASSWORD] != self.password:
            print "Passwords differ {}, {}".format(data[0][DataField.PASSWORD], self.password)
            raise Exceptions.WrongPasswordException ("Wrong password", "Can't connect to the database. Wrong password" )
        #load DB data
        self.editMetadata(**data[0])
        self.status = DBStatus.CONNECTED
        logging.debug('Connected successfully to the DB {}'.format(self.info())) 
                   
        
    def save(self):
        #check if the DB file exist
        if not os.path.isfile(self.path.decode('utf8')):
            raise Exceptions.NoFileException(file, "The database file doesn't exist") 
        #open db connection
        self.__SQLConnectProvider.open(self.path)
        for entry in self.entries:
            self.__saveEntry(entry, None) 
        
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()          
        
        
    def getEntriesOfCategory(self, catID):   
        #if the category is root
        if not catID:
            logging.debug('Getting entries of a root category')
            #check id root entries are loaded
            #id not loaded load them
            if not self.entries:
                self._loadEntriesOfCategory(catID)
            return self.entries                 
         
        #if normal category with parent
        else:
            #find the category    
            logging.debug('Getting entries of a category with id: {}'.format(catID))
            catObj = self.findEntryByID(catID, DBObjectType.CATEGORY)
            if catObj:
                #if empty load data
                if not len(catObj.entries):
                    self._loadEntriesOfCategory(catObj)    
                return catObj.entries
            else:
                raise Exceptions.NoneObjectException(catID, "Can't load the content. No category with such id found")       
          
        
    def addNewEntry(self, type, parentEntryID, **args):
        logging.debug('Adding a new entry for parent entry with id {}'.format(parentEntryID))
        parentEntryObj = None
        if not parentEntryID:
            pass                  
        else:
            parentEntryObj = self.findEntryByID(parentEntryID, None)  
        
        #if no parent found and not root raise exception
        if parentEntryID and not parentEntryObj:
            raise Exceptions.NoneObjectException(parentEntryID, "Can't add the new entry to None: there is no parent object with such id")
        #if try to add to the record, raise exception
        if parentEntryObj and parentEntryObj.type == DBObjectType.RECORD:
            raise Exceptions.EntryException(parentEntryID, """Can't add the new entry to parent object that is a record. 
            New entries can be added only to categories""")
        #add default new database id for a new record
        args[DataField.DB_ID] = Default.DEFAULT_NEW_ENTRY_DB_ID 
        newEntryID = self._addEntry(type, parentEntryObj, EntryStatus.NEW, **args)
        return newEntryID
        
        
    def editEntry(self, type, entryID, **args):   
        logging.debug('Editing the entry with id {}'.format(entryID) )
        #find category object
        entryObj = self.findEntryByID(entryID, type)
        if not entryObj:
            raise Exceptions.NoneObjectException(entryID, "Entry with such id doesn't exist")
        entryObj.edit(**args)          
        logging.debug('The entry after editing {}'.format(entryObj.info()) )   
        
        
    def removeEntry(self, type, entryID):
        if not entryID:
            raise Exceptions.NoneObjectException(entryID, "Can't remove the entry with such ID")
        
        entryObj = self.findEntryByID(entryID, type)
        if not entryObj:
            raise Exceptions.NoneObjectException(entryID, "Can't remove the entry with such id")        
        
        logging.debug('Removing the entry with id {}'.format(entryID) )
        entryObj.status = EntryStatus.REMOVED
        if type == DBObjectType.CATEGORY:
            #walk through entire entity sub tree of the given category and set status for REMOVED  
            self._removeCategory(entryObj) 
            
            
    def deleteRemoved(self):  
        #open db connection
        sql_query = SQLQuery.FOREIGN_KEY_ON
        self.__SQLConnectProvider.open(self.path)
        self.__SQLConnectProvider.execute(sql_query)
        
        for entry in self.entries:
            self.__deleteRemoved(entry, None) 
        
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
        
    def _addEntry(self, type, parentObj, status, **args):
        logging.debug('Adding an entry with the status {}'.format(status))
        entry = None
        newEntryID = None
        if type == DBObjectType.CATEGORY:
            logging.debug('Adding a category, parent {}'.format(parentObj))
            entry = Category(id=self._getNextEntryID(),  **args)
            newEntryID = entry.id
            entry.status = status
        elif type == DBObjectType.RECORD:
            logging.debug('Adding a record, parent {}'.format(parentObj))
            entry = Record(self._getNextEntryID(), **args) 
            newEntryID = entry.id
            entry.status = status       
        #If root category
        if not parentObj:
            self.addnewEntry(entry)
        else:
            parentObj.addnewEntry(entry) 
            
        return newEntryID 
    
    
    def _loadEntriesOfCategory(self, catObj):
        #if parent category
        #DB none check
        cat_query = rec_query = None
        #if root category(None)
        if not catObj:
            #if already loaded return
            if self.entries:
                return
            logging.debug('Loading root entries ')
            cat_query = SQLQuery.ROOT_CATEGORIES
            rec_query = SQLQuery.ROOT_RECORDS
        #if ordinary category
        else:
            #if already loaded return
            if catObj.entries:
                return
            logging.debug('Loading normal entries ')
            cat_query = SQLQuery.SUB_CATEGORIES.format(catObj.dbID)
            rec_query = SQLQuery.SUB_RECORDS.format(catObj.dbID)
             
        self.__SQLConnectProvider.open(self.path)
        data = self.__SQLConnectProvider.executeFetch(cat_query)#c.fetchall()
        for d in data:
            self._addEntry(DBObjectType.CATEGORY, catObj, EntryStatus.SAVED, **d)           
        #Add records
        data = self.__SQLConnectProvider.executeFetch(rec_query)
        for d in data:
            self._addEntry(DBObjectType.RECORD, catObj, EntryStatus.SAVED, **d)                                  
         
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
        
    def __saveEntry(self, entryObj, parentObj):
        if not entryObj:
            return
            
        #if record
        sql_query = None
        if entryObj.type == DBObjectType.RECORD:
            if entryObj.status == EntryStatus.NEW:
                # insert into root
                if not parentObj:
                    sql_query = SQLQuery.INSERT_NEW_ROOT_RECORD.format(entryObj.site, entryObj.username, entryObj.email, 
                                                                          entryObj.password, entryObj.comments)
                # insert into no root category  
                else:
                    sql_query = SQLQuery.INSERT_NEW_NOROOT_RECORD.format(parentObj.dbID, entryObj.site, entryObj.username, 
                                                                            entryObj.email, entryObj.password, entryObj.comments) 
            elif entryObj.status == EntryStatus.CHANGED:
                sql_query = SQLQuery.UPDATE_RECORD.format(entryObj.site, entryObj.username, entryObj.email,
                                                                      entryObj.password, entryObj.comments, entryObj.dbID)
            #execute query
            if (sql_query):
                logging.debug('Saving {}  by query: {}'.format(entryObj.info(), sql_query)) 
                self.__SQLConnectProvider.execute(sql_query)
                #Set auto id for new record
                if entryObj.status == EntryStatus.NEW:
                    entryObj.dbID = self.__SQLConnectProvider.getLastRowID()    
                
                entryObj.status = EntryStatus.SAVED
                
            return
            
        elif entryObj.type == DBObjectType.CATEGORY:
            if entryObj.status == EntryStatus.NEW:
                # insert into root
                if not parentObj:
                    sql_query = SQLQuery.INSERT_NEW_ROOT_CATEGORY.format(entryObj.name, entryObj.comments)
                #insert into no root   
                else:
                    sql_query = SQLQuery.INSERT_NEW_NOROOT_CATEGORY.format(parentObj.dbID, entryObj.name, entryObj.comments)
            elif entryObj.status == EntryStatus.CHANGED:
                sql_query = SQLQuery.UPDATE_CATEGORY.format(entryObj.name, entryObj.comments, entryObj.dbID)
            #execute query
            if (sql_query):
                logging.debug('Saving {}  by query: {}'.format(entryObj.info(), sql_query)) 
                self.__SQLConnectProvider.execute(sql_query)
                #Set auto id for new record
                if entryObj.status == EntryStatus.NEW:
                    entryObj.dbID = self.__SQLConnectProvider.getLastRowID() 
                entryObj.status = EntryStatus.SAVED
            #save children
            for entry in entryObj.entries: 
                #if (entry.status == EntryStatus.NEW or entry.status == EntryStatus.CHANGED):
                self.__saveEntry(entry, entryObj)      
               
                                           
    def __deleteRemoved(self, entryObj, parentObj):
        if not entryObj:
            return
        
        sql_query = None
        obj_info = entryObj.info()
        #if record
        if entryObj.status == EntryStatus.REMOVED and entryObj.type == DBObjectType.RECORD:
            #execute query
            logging.debug("Delete record {} from db".format(obj_info))
            sql_query = SQLQuery.REMOVE_RECORD.format(entryObj.dbID)
            self.__SQLConnectProvider.execute(sql_query)
            #delete from parent category!
            #if parent None remove from db
            if not parentObj:
                try:
                    self.entries.remove(entryObj) 
                except ValueError:
                    logging.debug("Error while removing record object. DB doesn't contain such object: {}".format(obj_info))
            
            #if not root record
            else:
                try:
                    parentObj.entries.remove(entryObj)
                except ValueError:
                    logging.debug("Error while removing record object. Parent {} doesn't contain such object: {}".format(parentObj.info(), obj_info))
                
            return
        #if category
        elif entryObj.type == DBObjectType.CATEGORY:
            #query remove the current category from database
            if entryObj.status == EntryStatus.REMOVED:
                logging.debug("Delete category {} from db".format(obj_info))
                sql_query = SQLQuery.REMOVE_CATEGORY.format(entryObj.dbID)
                self.__SQLConnectProvider.execute(sql_query)
                #remove the category object from parent!
                #if parent None remove from db
                if not parentObj:                                                                   
                    try:
                        self.entries.remove(entryObj) 
                    except ValueError:
                        logging.debug("Error while removing category object. DB doesn't contain such object: {}".format(obj_info))
                    
                #if not root record
                else:
                    try:
                        parentObj.entries.remove(entryObj)
                    except ValueError:
                        logging.debug("Error while removing category object. Parent {} doesn't contain such object: {}".format(parentObj.info(), obj_info))
  
            else:
                for entry in entryObj.entries: 
                    self.__deleteRemoved(entry, entryObj)    
               

                      
                                    
                                         