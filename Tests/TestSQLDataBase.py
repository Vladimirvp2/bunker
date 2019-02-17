'''
UnitTests for SQLite database
'''

import unittest, os
from DataModel.DataBase import SQLDataBase
from DataModel.SQLConnectProvider import SQLiteConnectProvider
from DataModel.SQLqueries import SQLQuery
import DataModel.Exceptions as Exceptions
from DataModel.DataEntries import Category, Record

import Common.Constants.Table as Table
import Common.Constants.DataField as DataField
import Common.Constants.DBStatus as DBStatus
import Common.Constants.Default as Default
import Common.Constants.DBObjectType as DBObjectType
import Common.Constants.EntryStatus as EntryStatus

from Tests import TestConfig as TestConfig



argsCat1 = {DataField.DB_ID : '1', DataField.NAME : 'name1', DataField.COMMENTS : 'comments1'}
argsRec1 = {DataField.DB_ID : '1', DataField.SITE : 'site1', DataField.USERNAME : 'username1', DataField.EMAIL : 'email1',
                    DataField.PASSWORD : 'password1', DataField.COMMENTS : 'comments1' } 
argsCat2 = {DataField.DB_ID : '2', DataField.NAME : 'name2', DataField.COMMENTS : 'comments2'}
argsRec2 = {DataField.DB_ID : '2', DataField.SITE : 'site2', DataField.USERNAME : 'username2', DataField.EMAIL : 'email2',
                    DataField.PASSWORD : 'password2', DataField.COMMENTS : 'comments2' } 
argsCat3 = {DataField.DB_ID : '3', DataField.NAME : 'name3', DataField.COMMENTS : 'comments3'}
argsRec3 = {DataField.DB_ID : '3', DataField.SITE : 'site3', DataField.USERNAME : 'username3', DataField.EMAIL : 'email3',
                    DataField.PASSWORD : 'password3', DataField.COMMENTS : 'comments3' } 

ARGS_DB = {DataField.PATH : TestConfig.SQLITE_DB_PATH, DataField.NAME : TestConfig.DB_NAME, DataField.PASSWORD : TestConfig.DB_PASSWORD, 
                DataField.COMMENTS : TestConfig.DB_COMMENTS}
        
idCat1 = '1'
idRec1 = '2'
idCat2 = '3'
idRec2 = '4' 
idCat3 = '5'
idRec3 = '6' 
noExistID = '10'



class TestSQLDataBase(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):    
        self.__SQLConnectProvider = SQLiteConnectProvider()     
    
    def setUp(self):
        '''
        Called before each test
        '''   
        self.removeDB()
            
    def tearDown(self):
        '''
        Called after each test
        '''   
        self.removeDB()  
            
                         
    @classmethod  
    def removeDB(self):
        '''
        Remove database file if exist
        '''   
        if os.path.isfile(TestConfig.SQLITE_DB_PATH):
            os.remove(TestConfig.SQLITE_DB_PATH) 
            
        if os.path.isfile(TestConfig.NO_EXISTING_FILE):
            os.remove(TestConfig.NO_EXISTING_FILE)                              
    
    
    @classmethod
    def checkFieldInTable(self, dataToCheck, fieldsData):
        '''
        Used to check if a table contains all the necessary fields(names and types)
        @type  dataToCheck: [{'name' : '', 'type' : '',}, ] - list of dicts
        @param dataToCheck: field data of a particularly table
        @type  fieldsData: [{'name' : '', 'type' : ''}, ] - list of dicts
        @param fieldsData: description of the fields that should be checked matched dataToCheck
        @rtype: boolean
        @return: if the check is passed or not 
        '''
        columnNum = len(fieldsData)
        counter = 0
        for data in dataToCheck:
            for field in fieldsData:
                if data['name'] == field['name']:
                    if data['type'] == field['type'].lower() or data['type'] == field['type'].upper():
                        counter+=1   
        
        if counter == columnNum:
            return True
        
        return False   
    
    @classmethod
    def createCleanDB(self, **args):
        '''
        Creates in tmp dir(see test config) clean DB(only structure and meta info) 
        '''
        #enable foreign key  
        self.__SQLConnectProvider.open(args[DataField.PATH])
        self.__SQLConnectProvider.execute(SQLQuery.FOREIGN_KEY_ON)
                
        #Create metadata table
        query = SQLQuery.CREATE_METADATA_TABLE       
        self.__SQLConnectProvider.execute(query)
        
        #Insert start info inside the metadata table
        query = SQLQuery.INSERT_INTO_METADATA_TABLE.format( args[DataField.NAME], args[DataField.PASSWORD], args[DataField.COMMENTS])     
        self.__SQLConnectProvider.execute(query)        
        
        #Create category table
        query = SQLQuery.CREATE_CATEGORY_TABLE 
        self.__SQLConnectProvider.execute(query)  
        
        #Create record table
        query = SQLQuery.CREATE_RECORD_TABLE       
        self.__SQLConnectProvider.execute(query)
                                
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
    
    @classmethod
    def createDBfileWithEntries(self):
        """
        Create clean DB file, fill in with basic 3 level structure of entries(6 entries, 2 on each level)
        """
        args = {DataField.PATH : TestConfig.SQLITE_DB_PATH, DataField.NAME : TestConfig.DB_NAME, DataField.PASSWORD : TestConfig.DB_PASSWORD, 
                DataField.COMMENTS : TestConfig.DB_COMMENTS}
        self.createCleanDB(**args)
        
        self.__SQLConnectProvider.open(args[DataField.PATH])
                
        #Add root category and record
        query = SQLQuery.INSERT_NEW_ROOT_CATEGORY.format(argsCat1[DataField.NAME], argsCat1[DataField.COMMENTS]) 
        self.__SQLConnectProvider.execute(query)     
        catDBID1 = self.__SQLConnectProvider.getLastRowID()
        query = SQLQuery.INSERT_NEW_ROOT_RECORD.format(argsRec1[DataField.SITE], argsRec1[DataField.USERNAME], argsRec1[DataField.EMAIL],
                                                           argsRec1[DataField.PASSWORD], argsRec1[DataField.COMMENTS])      
        self.__SQLConnectProvider.execute(query) 
        
        #Add new category and record to the level 1
        query = SQLQuery.INSERT_NEW_NOROOT_CATEGORY.format(catDBID1, argsCat2[DataField.NAME], argsCat2[DataField.COMMENTS])      
        self.__SQLConnectProvider.execute(query)  
        catDBID2 = self.__SQLConnectProvider.getLastRowID()#c.lastrowid  
        query = SQLQuery.INSERT_NEW_NOROOT_RECORD.format(catDBID1, argsRec2[DataField.SITE], argsRec2[DataField.USERNAME], argsRec2[DataField.EMAIL],
                                                           argsRec2[DataField.PASSWORD], argsRec2[DataField.COMMENTS])      
        self.__SQLConnectProvider.execute(query) 
        
        #Add new category and record to the level 2
        query = SQLQuery.INSERT_NEW_NOROOT_CATEGORY.format(catDBID2, argsCat3[DataField.NAME], argsCat3[DataField.COMMENTS])       
        self.__SQLConnectProvider.execute(query) 
        catDBID3 = self.__SQLConnectProvider.getLastRowID() 
        query = SQLQuery.INSERT_NEW_NOROOT_RECORD.format(catDBID2, argsRec3[DataField.SITE], argsRec3[DataField.USERNAME], argsRec3[DataField.EMAIL],
                                                           argsRec3[DataField.PASSWORD], argsRec3[DataField.COMMENTS])      
        self.__SQLConnectProvider.execute(query)
        
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
       
    @classmethod
    def createDBObjectWithEntries(self):
        """
        Create some categories and records and add it to the given DB
        @rtype: [ SQLDataBase, [catObject1, recObject1], [catObject2, recObject2], [catObject3, recObject3] ]
        @return: SQLDataBase object containing entries two on each level(1 category, 1 record), 3 lebels - 6 objects
                 And entry objects itself separately
        """
        #create DB
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH )
    
        #create hierarchy of entry objects
        catObj1 = Category(id=idCat1,  **argsCat1)
        recObj1 = Record(id=idRec1,  **argsRec1)
        catObj2 = Category(id=idCat2,  **argsCat2)
        recObj2 = Record(id=idRec2,  **argsRec2)
        catObj3 = Category(id=idCat3,  **argsCat3)
        recObj3 = Record(id=idRec3,  **argsRec3)
        #add category2 and record2 to the root category 
        catObj2.entries.append(catObj3)
        catObj2.entries.append(recObj3)
        catObj1.entries.append(catObj2)
        catObj1.entries.append(recObj2)
        #add root category and record to database
        db.entries.append(catObj1)
        db.entries.append(recObj1)        
        
        return [db, [catObj1, recObj1], [catObj2, recObj2], [catObj3, recObj3] ]        
                                                    
        
        
    @classmethod
    def findEntryByID(self, id, entryList):
        '''
        Finds all entry objects with the given id. If there are 2, 3.. objects with such id, return them all
        If no objects found, return empty list
        @type  id: string
        @param id: object id
        @type  entryList: list
        @param entryList: list of Entries       
        @rtype: list
        @return: list of Entry objects with the given id  
        '''
        res = []
        for obj in entryList:
            if obj.id == id:
                res.append(obj)
        return res           
                
    
    def test_01_createDB(self):
        '''
        Check the structure of newly created DB and it's metadata(name, password, comments)
        '''  
        #Check exceptions
        #================================================================================
        #Check file already exist exception
        db1 = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH, TestConfig.DB_NAME, 
                              TestConfig.DB_PASSWORD, TestConfig.DB_COMMENTS)
        db1.createDB() 
        db2 = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH, TestConfig.DB_NAME, 
                              TestConfig.DB_PASSWORD, TestConfig.DB_COMMENTS)
        self.assertRaises(Exceptions.ExistFileException, db2.createDB)
        
        #Check bad path exception
        self.setUp()
        db1 = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.NO_EXISTING_PATH, TestConfig.DB_NAME, 
                              TestConfig.DB_PASSWORD, TestConfig.DB_COMMENTS)
        self.assertRaises(Exceptions.WrongPathException, db1.createDB)
            
                     
        #check table structure
        #================================================================================        
        self.setUp()
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH, TestConfig.DB_NAME,
                              TestConfig.DB_PASSWORD, TestConfig.DB_COMMENTS)
        db.createDB()
        
        #Check metadata table
        fields = [{'name' : DataField.NAME, 'type' : 'text'}, {'name' : DataField.PASSWORD, 'type' : 'text'},
                  {'name' : DataField.COMMENTS, 'type' : 'text'}]         
        query = '''SELECT* FROM {}'''.format(Table.METADATA_TABLE)
        self.__SQLConnectProvider.open(TestConfig.SQLITE_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #check if meatdata table has only 1 record
        self.assertEqual(1, len(data))
        
        #check if all the columns in the category table exist 
        query = '''PRAGMA table_info({});'''.format(Table.METADATA_TABLE)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #check number of columns
        self.assertEqual(len(fields), len(data))
        #check field names and types                     
        res = self.checkFieldInTable(data, fields)    
        self.assertTrue(res)
        
        #Category table check
        fields = [{'name' : DataField.ID, 'type' : 'INTEGER'}, {'name' : DataField.PARENT, 'type' : 'INTEGER'},
                  {'name' : DataField.NAME, 'type' : 'text'}, {'name' : DataField.COMMENTS, 'type' : 'text'}]        
        #check if all the columns in the category table exist 
        query = '''PRAGMA table_info({});'''.format(Table.CATEGORY_TABLE)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #check number of columns
        self.assertEqual(len(fields), len(data))
        #check field names and types                     
        res = self.checkFieldInTable(data, fields)    
        
        self.assertTrue(res)
        
        #Check if the category table is empty
        query = '''SELECT* FROM {}'''.format(Table.CATEGORY_TABLE) 
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        self.assertEqual(0, len(data))                                                    
                    
        #Records table check
        fields = [{'name' : DataField.ID, 'type' : 'INTEGER'}, {'name' : DataField.PARENT, 'type' : 'INTEGER'},
                  {'name' : DataField.EMAIL, 'type' : 'text'}, {'name' : DataField.USERNAME, 'type' : 'text'}, 
                  {'name' : DataField.PASSWORD, 'type' : 'text'}, {'name' : DataField.SITE, 'type' : 'text'},
                  {'name' : DataField.COMMENTS, 'type' : 'text'}, {'name' : DataField.TIME, 'type' : 'TIMESTAMP'}]        
        #check if all the columns in the category table exist 
        query = '''PRAGMA table_info({});'''.format(Table.RECORD_TABLE)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #check number of columns
        self.assertEqual(len(fields), len(data))
        #check field names and types                     
        res = self.checkFieldInTable(data, fields)    
        
        self.assertTrue(res)
        
        #Check if the category table is empty
        query = '''SELECT* FROM {}'''.format(Table.RECORD_TABLE) 
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        self.assertEqual(0, len(data))
        
        self.__SQLConnectProvider.closeConnection()          
        
    
    def test_02_connect(self):
        '''
        Create a new empty DB, load it and check if the matadata is correctly loaded
        '''
        self.createCleanDB(**ARGS_DB)
        #load the newly created DB file 
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, **ARGS_DB)
        db.connect()
        #check if the metadata is loaded
        self.assertEqual(db.name, TestConfig.DB_NAME)
        self.assertEqual(db.password, TestConfig.DB_PASSWORD) 
        self.assertEqual(db.comments, TestConfig.DB_COMMENTS) 
        
        #Check if status of the DB is connected
        self.assertEqual(db.status, DBStatus.CONNECTED)
        
        #Check exceptions
        #================================================================================
                   
        #Check wrong path exception
        #delete temp db
        self.setUp()
        self.createCleanDB(**ARGS_DB) 
        #set wrong file
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.NO_EXISTING_PATH )
        self.assertRaises(Exceptions.NoFileException, db.connect)    
    
    
    def test_03_disconnect(self):
        #Create new clean DB and connect to it
        self.createCleanDB(**ARGS_DB)
        #load the newly created DB file 
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, **ARGS_DB)
        db.connect() 
        db.disconnect()
        #check status
        self.assertEqual(db.status, DBStatus.DISCONNECTED)
        #Check exceptions
        #================================================================================
        #If DB already disconnected throw exception
        self.assertRaises(Exceptions.DataBaseException, db.disconnect)
        
        
    def test_04_editMetadata(self):    
        args = {DataField.NAME : TestConfig.DB_NAME, DataField.PASSWORD : '1', 
                 DataField.COMMENTS : TestConfig.DB_COMMENTS}
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, path = ARGS_DB[DataField.PATH]) 
        #check if default is ok
        self.assertEqual(db.name, Default.DEFAULT_DB_NAME)
        self.assertEqual(db.password, Default.DEFAULT_DB_PASSWORD)
        self.assertEqual(db.comments, Default.DEFAULT_DB_COMMENT)
        
        #edit and check values
        db.editMetadata(**args)
        self.assertEqual(db.name, args[DataField.NAME])
        self.assertEqual(db.password, args[DataField.PASSWORD])
        self.assertEqual(db.comments, args[DataField.COMMENTS])   
        
        #Check exceptions
        #================================================================================
        #If not possible to change db password that is not default(was changed once)
        #self.assertRaises(Exceptions.DataBaseException, db.editMetadata, **args)   
    
    
    def test_05_findEntryByID(self):
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH )
        argsCat = {DataField.DB_ID : '1', DataField.NAME : 'name'}
        argsRec = {DataField.DB_ID : '1' }
        #add some entries(Categories and Records) to the root
        #ids have to be unique
        idCat1 = '1'
        idCat2 = '2'
        idCat3 = '3'  
        idRec1 = '4'
        idRec2 = '5'
        idRec3 = '6'
        #id on no existing object(entry)
        idNoExistObj = '7'
        #create entry objects
        catObj1 = Category(id=idCat1,  **argsCat)
        catObj2 = Category(id=idCat2,  **argsCat)
        catObj3 = Category(id=idCat3,  **argsCat)
        recObj1 = Record(idRec1, **argsRec)
        recObj2 = Record(idRec2, **argsRec)
        recObj3 = Record(idRec3, **argsRec)
        #arrange the entries hierarchically
        # catObj1, recObj1 - in root(directly in db); catObj2, recRec2 - in catObj1; catObj3, recObj3 - in catObj2
        catObj1.entries.append(catObj2)
        catObj1.entries.append(recObj2)
        catObj2.entries.append(catObj3)
        catObj2.entries.append(recObj3)
        #add to root(direct to db)
        db.entries.append(catObj1)
        db.entries.append(recObj1)
        
        #find each of the entries in the DB        
        #================================================================================
        #in root
        obCat1 = db.findEntryByID(idCat1, DBObjectType.CATEGORY)
        obRec1 = db.findEntryByID(idRec1, DBObjectType.RECORD)
        self.assertEqual(obCat1, catObj1)
        self.assertEqual(obRec1, recObj1)
        #in 1 level depth
        obCat2 = db.findEntryByID(idCat2, DBObjectType.CATEGORY)
        obRec2 = db.findEntryByID(idRec2, DBObjectType.RECORD)
        self.assertEqual(obCat2, catObj2)
        self.assertEqual(obRec2, recObj2)
        #in 2 level depth
        obRec3 = db.findEntryByID(idRec3, DBObjectType.RECORD)
        self.assertEqual(obRec3, recObj3)   
        
        #wrong type find check
        #================================================================================
        #in root
        obCat1_w = db.findEntryByID(idCat1, DBObjectType.RECORD)
        obRec1_w = db.findEntryByID(idRec1, DBObjectType.CATEGORY)
        self.assertFalse(obCat1_w)
        self.assertFalse(obRec1_w) 
        #depth, level 1        
        obCat2_w = db.findEntryByID(idCat2, DBObjectType.RECORD)
        obRec2_w = db.findEntryByID(idRec2, DBObjectType.CATEGORY) 
        self.assertFalse(obCat2_w)
        self.assertFalse(obRec2_w) 
        #level 2              
        obRec3_w = db.findEntryByID(idRec3, DBObjectType.CATEGORY)
        self.assertFalse(obRec3_w)   
        
        #check if type None returns all types of entries        
        #================================================================================
        #in root
        obCat1_notype = db.findEntryByID(idCat1, None)
        obRec1_notype = db.findEntryByID(idRec1, None)
        self.assertEqual(obCat1_notype, catObj1)
        self.assertEqual(obRec1_notype, recObj1)        
        #in 1 level depth
        obCat2_notype = db.findEntryByID(idCat2, None)
        obRec2_notype = db.findEntryByID(idRec2, None)
        self.assertEqual(obCat2_notype, catObj2)
        self.assertEqual(obRec2_notype, recObj2)                  
        #in 2 level depth
        obRec3_notype = db.findEntryByID(idRec3, None)
        self.assertEqual(obRec3_notype, recObj3)
        
        #check if None return if no object with such id exist without type(all types)         
        #================================================================================
        noObj = db.findEntryByID(idNoExistObj, None)    
        self.assertFalse(noObj)        
        
    
    def test_06_addNewEntry(self):
        #create DB
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH )
        #create hierarchy with created categories and records using addNewEntry method
        argsCat1 = {DataField.NAME : 'name1', DataField.COMMENTS : 'comments1'}
        argsRec1 = {DataField.SITE : 'site1', DataField.USERNAME : 'username1', DataField.EMAIL : 'email1',
                    DataField.PASSWORD : 'password1', DataField.COMMENTS : 'comments1' }  
        #Check adding to root
        #================================================================================      
        idCat1 = db.addNewEntry(DBObjectType.CATEGORY, None, **argsCat1)
        idRec1 = db.addNewEntry(DBObjectType.RECORD, None, **argsRec1) 
        #find the added entries
        objsCat1 = self.findEntryByID(idCat1, db.entries)
        #there should be only one object with such id
        self.assertEqual(1, len(objsCat1))
        #check fields of the object
        self.assertEqual(objsCat1[0].name, argsCat1[DataField.NAME])
        self.assertEqual(objsCat1[0].comments, argsCat1[DataField.COMMENTS])
        
        objsRec1 = self.findEntryByID(idRec1, db.entries)
        #there should be only one object with such id
        self.assertEqual(1, len(objsRec1))
        #check fields of the object
        self.assertEqual(objsRec1[0].site, argsRec1[DataField.SITE])
        self.assertEqual(objsRec1[0].username, argsRec1[DataField.USERNAME])
        self.assertEqual(objsRec1[0].email, argsRec1[DataField.EMAIL])  
        self.assertEqual(objsRec1[0].password, argsRec1[DataField.PASSWORD])
        self.assertEqual(objsRec1[0].comments, argsRec1[DataField.COMMENTS])           
      
        #Check adding to categories
        #================================================================================
        argsCat2 = {DataField.NAME : 'name2', DataField.COMMENTS : 'comments2'}
        argsRec2 = {DataField.SITE : 'site2', DataField.USERNAME : 'username2', DataField.EMAIL : 'email2',
                    DataField.PASSWORD : 'password2', DataField.COMMENTS : 'comments2' }       
        #add new entries to the category 1
        idCat2 = db.addNewEntry(DBObjectType.CATEGORY, idCat1, **argsCat2)
        idRec2 = db.addNewEntry(DBObjectType.RECORD, idCat1, **argsRec2)    
        
        #find the added category
        objsCat2 = self.findEntryByID(idCat2, objsCat1[0].entries)
        #there should be only one object with such id
        self.assertEqual(1, len(objsCat2))
        #check fields of the object
        self.assertEqual(objsCat2[0].name, argsCat2[DataField.NAME])
        self.assertEqual(objsCat2[0].comments, argsCat2[DataField.COMMENTS]) 
        #find the added record
        objsRec2 = self.findEntryByID(idRec2, objsCat1[0].entries)
        #there should be only one object with such id
        self.assertEqual(1, len(objsRec2))
        #check fields of the object
        self.assertEqual(objsRec2[0].site, argsRec2[DataField.SITE])
        self.assertEqual(objsRec2[0].username, argsRec2[DataField.USERNAME])
        self.assertEqual(objsRec2[0].email, argsRec2[DataField.EMAIL])  
        self.assertEqual(objsRec2[0].password, argsRec2[DataField.PASSWORD])
        self.assertEqual(objsRec2[0].comments, argsRec2[DataField.COMMENTS]) 
        
        #Check exceptions
        #================================================================================
        #Check add to None parent object  
        noExistID = '10'
        self.assertRaises(Exceptions.NoneObjectException, db.addNewEntry, DBObjectType.CATEGORY, noExistID, **argsCat2 )  
        #Check add to record entry
        self.assertRaises(Exceptions.EntryException, db.addNewEntry, DBObjectType.RECORD, idRec2, **argsRec2 )                         
        
    
    def test_07_editEntry(self):
        #create DB
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, TestConfig.SQLITE_DB_PATH )
        #category and record arguments
        argsCat = {DataField.DB_ID : '1', DataField.NAME : 'name1', DataField.COMMENTS : 'comments1'}
        argsRec = {DataField.DB_ID : '1', DataField.SITE : 'site1', DataField.USERNAME : 'username1', DataField.EMAIL : 'email1',
                    DataField.PASSWORD : 'password1', DataField.COMMENTS : 'comments1' }
        
        argsCatEdit = {DataField.DB_ID : '1', DataField.NAME : 'name1edit', DataField.COMMENTS : 'comments1edit'}
        argsRecEdit = {DataField.DB_ID : '1', DataField.SITE : 'site1edit', DataField.USERNAME : 'username1edit', DataField.EMAIL : 'email1edit',
                    DataField.PASSWORD : 'password1edit', DataField.COMMENTS : 'comments1edit' }        
        
        idCat1 = '1'
        idRec1 = '2'
        idCat2 = '3'
        idRec2 = '4'
        idCat3 = '5'
        idRec3 = '6'        
        #create hierarchy of entry objects
        catObj1 = Category(id=idCat1,  **argsCat)
        recObj1 = Record(id=idRec1,  **argsRec)
        catObj2 = Category(id=idCat2,  **argsCat)
        recObj2 = Record(id=idRec2,  **argsRec)
        #add category2 and record2 to the root category 
        catObj1.entries.append(catObj2)
        catObj1.entries.append(recObj2)
        #add root category and record to database
        db.entries.append(catObj1)
        db.entries.append(recObj1) 
        
        #Change each of these entries
        #Change root category
        db.editEntry(DBObjectType.CATEGORY, idCat1, **argsCatEdit)
        self.assertEqual(catObj1.name, argsCatEdit[DataField.NAME])
        self.assertEqual(catObj1.comments, argsCatEdit[DataField.COMMENTS])  
        #Change root record
        db.editEntry(DBObjectType.RECORD, idRec1, **argsRecEdit)
        self.assertEqual(recObj1.site, argsRecEdit[DataField.SITE])
        self.assertEqual(recObj1.email, argsRecEdit[DataField.EMAIL])
        self.assertEqual(recObj1.username, argsRecEdit[DataField.USERNAME])
        self.assertEqual(recObj1.password, argsRecEdit[DataField.PASSWORD])
        self.assertEqual(recObj1.comments, argsRecEdit[DataField.COMMENTS])
        
        #Check if ignore edit if the entry is removed(marked with status REMOVED)
        #================================================================================        
        catObj3 = Category(id=idCat3,  **argsCat)
        recObj3 = Record(id=idRec3,  **argsRec)
        #Set removed status to entries
        catObj3.status = EntryStatus.REMOVED
        recObj3.status = EntryStatus.REMOVED
        #Add root category and record to database
        db.entries.append(catObj3)
        db.entries.append(recObj3)
        #Edit added entries and check their status. It(removed) shouln't change
        #Category
        db.editEntry(DBObjectType.CATEGORY, idCat3, **argsCatEdit)        
        self.assertEqual(catObj3.status, EntryStatus.REMOVED)
        #Record
        db.editEntry(DBObjectType.RECORD, idRec3, **argsRecEdit)
        self.assertEqual(recObj3.status, EntryStatus.REMOVED)
        
        #Check if edit doesn't change entry status from NEW to CHANGED. It should be NEW even after editing
        catObj3.status = EntryStatus.NEW
        recObj3.status = EntryStatus.NEW
        #Category
        db.editEntry(DBObjectType.CATEGORY, idCat3, **argsCatEdit)        
        self.assertEqual(catObj3.status, EntryStatus.NEW)        
        #Record
        db.editEntry(DBObjectType.RECORD, idRec3, **argsRecEdit)
        self.assertEqual(recObj3.status, EntryStatus.NEW)      
         
        #Check exceptions
        #================================================================================    
        #Check edit entry with no existing id  
        noExistIDCat = '10'
        noExistIDRec = '20'
        #Category
        self.assertRaises(Exceptions.NoneObjectException, db.editEntry, DBObjectType.CATEGORY, noExistIDCat, **argsCatEdit ) 
        #Record
        self.assertRaises(Exceptions.NoneObjectException, db.editEntry, DBObjectType.RECORD, noExistIDRec, **argsRecEdit )        
          
        
    
    def test_08_removeEntry(self):
        """Check whether the removed entry and it's children are set the REMOVED status""" 
        
        objectsDB = self.createDBObjectWithEntries()
        #get DB with entries
        db = objectsDB[0]
        #get entry objects
        catObj1 = objectsDB[1][0]
        recObj1 = objectsDB[1][1]
        catObj2 = objectsDB[2][0]
        recObj2 = objectsDB[2][1]
        catObj3 = objectsDB[3][0]
        recObj3 = objectsDB[3][1]
        #remove category and record of each level and check status of children
        db.removeEntry(DBObjectType.CATEGORY, catObj1.id)
        #Check status of entries
        #root
        self.assertEqual(recObj1.status, EntryStatus.NEW)
        self.assertEqual(catObj1.status, EntryStatus.REMOVED) 
        #level 1
        self.assertEqual(catObj2.status, EntryStatus.REMOVED)
        self.assertEqual(recObj2.status, EntryStatus.REMOVED)         
        #level 2
        self.assertEqual(catObj3.status, EntryStatus.REMOVED)
        self.assertEqual(recObj3.status, EntryStatus.REMOVED) 
        
        #remove record
        db.removeEntry(DBObjectType.RECORD, recObj1.id)
        self.assertEqual(recObj1.status, EntryStatus.REMOVED)   
              
        #Check exceptions
        #================================================================================
        #if non existing id
        self.assertRaises(Exceptions.NoneObjectException, db.removeEntry, DBObjectType.CATEGORY, noExistID )
        self.assertRaises(Exceptions.NoneObjectException, db.removeEntry, DBObjectType.RECORD, noExistID )           
        #None id
        self.assertRaises(Exceptions.NoneObjectException, db.removeEntry, DBObjectType.CATEGORY, None)
        self.assertRaises(Exceptions.NoneObjectException, db.removeEntry, DBObjectType.RECORD, None)        
                     
                           
            
    def test_09_getEntriesOfCategory(self):
        """Check loading of entries of each level""" 
        #Creates a DB with 2 entries on each level(root, level 1, level 2)        
        self.createDBfileWithEntries()
        
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, **ARGS_DB)
        db.connect()

        #None loaded categories
        self.assertEqual(0, len(db.entries))
        
        #Load root level
        res1 = db.getEntriesOfCategory(None)
        #should be 2 entries now in the root: 1 category and 1 record 
        self.assertEqual(2, len(db.entries))
        self.assertEqual(2, len(res1))  
        cat1 = db.entries[0] if db.entries[0].type == DBObjectType.CATEGORY else db.entries[1]
        #Category 1 should be empty
        self.assertEqual(0, len(cat1.entries))
        #Load level 1
        res2 = db.getEntriesOfCategory(cat1.id)
        self.assertEqual(2, len(cat1.entries))
        self.assertEqual(2, len(res2))
        
        cat2 = cat1.entries[0] if cat1.entries[0].type == DBObjectType.CATEGORY else cat1.entries[1]
        #Category 2 should be empty
        self.assertEqual(0, len(cat2.entries))
        #Load level 2
        res3 = db.getEntriesOfCategory(cat2.id)
        self.assertEqual(2, len(cat2.entries))
        self.assertEqual(2, len(res3))
        
        #check second call
        #root
        res1_sec = db.getEntriesOfCategory(None)
        #should be 2 entries now in the root: 1 category and 1 record 
        self.assertEqual(2, len(db.entries))
        self.assertEqual(2, len(res1_sec))  
       
        #level1
        res2_sec = db.getEntriesOfCategory(cat1.id)
        self.assertEqual(2, len(cat1.entries))
        self.assertEqual(2, len(res2_sec))    
        
        #level2
        res3_sec = db.getEntriesOfCategory(cat2.id)
        self.assertEqual(2, len(cat2.entries))
        self.assertEqual(2, len(res3_sec)) 
        
        #Check exceptions
        #================================================================================
        #If wrong id provided throw exception
        self.assertRaises(Exceptions.NoneObjectException, db.getEntriesOfCategory, noExistID )                   

    
    def test_10_save(self):
        """
        Create clean DB file, create DB object, add some Categories and records, save and check whether all entries
        have been saved correctly
        """
        #Create clean DB file
        self.createCleanDB(**ARGS_DB)
        #Create DB object than is points at the file than was just created
        objectsDB = self.createDBObjectWithEntries()
        #get DB with entries
        db = objectsDB[0]
        #get entry objects
        catObj1 = objectsDB[1][0]
        recObj1 = objectsDB[1][1]
        catObj2 = objectsDB[2][0]
        recObj2 = objectsDB[2][1]
        catObj3 = objectsDB[3][0]
        recObj3 = objectsDB[3][1]
         
        db.save()
        #check whether all entries are saved correctly
        #conn = sqlite3.connect(TestConfig.SQLITE_DB_PATH)
        #conn.row_factory = self.dict_factory
        #c = conn.cursor()

        #Select all the categories
        query = SQLQuery.SELECT_ALL_CATEGORIES 
        self.__SQLConnectProvider.open(TestConfig.SQLITE_DB_PATH)      
        #c.execute(query)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #number of checked categories
        counter = 0
        for cat in data:
            #if root
            if cat[DataField.PARENT] == None:
                self.assertEqual(cat[DataField.NAME], catObj1.name)
                self.assertEqual(cat[DataField.COMMENTS], catObj1.comments) 
                counter+=1
            # level 1 category
            elif str(cat[DataField.PARENT]) == catObj1.dbID:
                self.assertEqual(str(cat[DataField.NAME]), catObj2.name)
                self.assertEqual(str(cat[DataField.COMMENTS]), catObj2.comments)
                counter+=1
            # level 2 category
            elif str(cat[DataField.PARENT]) == catObj2.dbID:
                self.assertEqual(str(cat[DataField.NAME]), catObj3.name)
                self.assertEqual(str(cat[DataField.COMMENTS]), catObj3.comments) 
                counter+=1  
                
        #should be 3 categories
        self.assertEqual(3, counter)                     
          
        #Select all the records
        query = SQLQuery.SELECT_ALL_RECORDS 
        #c.execute(query)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #number of checked categories
        counter = 0
        for rec in data:
            #if root
            if rec[DataField.PARENT] == None:
                self.assertEqual(rec[DataField.COMMENTS], recObj1.comments)
                self.assertEqual(rec[DataField.SITE], recObj1.site)
                self.assertEqual(rec[DataField.EMAIL], recObj1.email)
                self.assertEqual(rec[DataField.USERNAME], recObj1.username) 
                self.assertEqual(rec[DataField.PASSWORD], recObj1.password)
                counter+=1 
            #level 1 record
            elif str(rec[DataField.PARENT]) == catObj1.dbID:
                self.assertEqual(rec[DataField.COMMENTS], recObj2.comments)
                self.assertEqual(rec[DataField.SITE], recObj2.site)
                self.assertEqual(rec[DataField.EMAIL], recObj2.email)
                self.assertEqual(rec[DataField.USERNAME], recObj2.username) 
                self.assertEqual(rec[DataField.PASSWORD], recObj2.password)
                counter+=1 
            #level 2 record
            elif str(rec[DataField.PARENT]) == catObj2.dbID:
                self.assertEqual(rec[DataField.COMMENTS], recObj3.comments)
                self.assertEqual(rec[DataField.SITE], recObj3.site)
                self.assertEqual(rec[DataField.EMAIL], recObj3.email)
                self.assertEqual(rec[DataField.USERNAME], recObj3.username) 
                self.assertEqual(rec[DataField.PASSWORD], recObj3.password) 
                counter+=1                                                       
                  
        #should be 3 categories
        self.assertEqual(3, counter)                 
        
        self.__SQLConnectProvider.closeConnection()
        #conn.commit()
        #conn.close() 
        
        
    
    def test_11_deleteRemoved(self):
        """Create DB file with basic fill. Load then configuration and delete"""
        
        #Test delete of root category
        #================================================================================
        #Create DB file
        self.createDBfileWithEntries()
        
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, **ARGS_DB)
        db.connect()
        entriesRoot = db.getEntriesOfCategory(None)
        for entry in entriesRoot:
            #remove root category
            if entry.type == DBObjectType.CATEGORY:
                db.removeEntry(entry.type, entry.id)
                db.deleteRemoved()
                break
        #check if all sub categories and sub records of the first root category have been deleted from DB file
        query = SQLQuery.SELECT_ALL_CATEGORIES
        self.__SQLConnectProvider.open(TestConfig.SQLITE_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(query)
        self.assertEqual(0, len(data))
        
        #Check records(should be 1 - root)
        query = SQLQuery.SELECT_ALL_RECORDS
        data = self.__SQLConnectProvider.executeFetch(query)
        self.assertEqual(1, len(data))
        
        #Check whether entry objects were removed from parent entries
        entriesDB = db.entries
        self.assertEqual(1, len(entriesDB))
        self.assertEqual(DBObjectType.RECORD, entriesDB[0].type)        
        
        self.__SQLConnectProvider.closeConnection()
        
        #Test delete not root category
        #================================================================================        
        self.setUp()
        #Create DB file
        self.createDBfileWithEntries()
        
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, **ARGS_DB )
        db.connect()
        entriesRoot = db.getEntriesOfCategory(None) 
        catEntriesLevel1 = None       
        for entry in entriesRoot:
            #remove root category
            if entry.type == DBObjectType.CATEGORY:
                catEntriesLevel1 = db.getEntriesOfCategory(entry.id) 
                break       
        
        for entry in catEntriesLevel1:
            #remove category of level 1
            if entry.type == DBObjectType.CATEGORY:
                db.removeEntry(entry.type, entry.id)
                db.deleteRemoved()
                break
            
        #check if all sub categories and sub records of the category level 1 have been removed
        query = SQLQuery.SELECT_ALL_CATEGORIES
        self.__SQLConnectProvider.open(TestConfig.SQLITE_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        #1 - root should stay
        self.assertEqual(1, len(data)) 
        
        #Check records(should be 2 - 1 in root and 1 of the level 1 )
        query = SQLQuery.SELECT_ALL_RECORDS
        data = self.__SQLConnectProvider.executeFetch(query)
        self.assertEqual(2, len(data))                   
            
        self.__SQLConnectProvider.closeConnection()                   
        
        #Check whether entry objects were removed from parent entries
        entriesDB = db.entries
        #All(2) should stay in the root 
        self.assertEqual(2, len(entriesDB))   
        #only 1 in the level 1
        self.assertEqual(1, len(catEntriesLevel1)) 
        

    def test_12_getIfChanged(self):
        self.createCleanDB(**ARGS_DB)
        #load the newly created DB file 
        db = SQLDataBase(TestConfig.DB_OBJECT_ID1, **ARGS_DB)
        db.connect()
        
        self.assertFalse(db.getIfChanged())
        #add root categories
        idCatRoot1 = db.addNewEntry(DBObjectType.CATEGORY, None, **argsCat1)
        db.addNewEntry(DBObjectType.CATEGORY, None, **argsCat2)
        self.assertTrue(db.getIfChanged())
        db.save()
        self.assertFalse(db.getIfChanged())  
        #add 1 level category
        catLevel1 = db.addNewEntry(DBObjectType.CATEGORY, idCatRoot1, **argsCat2) 
        self.assertTrue(db.getIfChanged()) 
        db.save()
        self.assertFalse(db.getIfChanged()) 
        #add record to the level 1
        db.addNewEntry(DBObjectType.RECORD, catLevel1, **argsRec1) 
        self.assertTrue(db.getIfChanged())   
                                    


if __name__ == '__main__':
    unittest.main()       
          