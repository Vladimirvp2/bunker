'''
UnitTests for User config  manager(SQLite)
'''

import unittest, os
import Common.Constants.Table as Table
from Tests import TestConfig as TestConfig
from DataModel.UserConfigManager import UserConfigManager
import Common.Constants.DataField as DataField
from Common.Crypt import *
from DataModel.SQLConnectProvider import SQLiteConnectProvider
import DataModel.Exceptions as Exceptions
import DataModel.SQLqueries as SQLqueries
import Common.Constants.Default as Default


#Get info about a particular table in SQLite        
SELECT_TABLE_INFO = '''PRAGMA table_info({});'''


class TestUserConfigManager(unittest.TestCase):
        
    @classmethod
    def setUpClass(self):    
        self.__SQLConnectProvider = SQLiteConnectProvider()  
        self.crypt = CryptAES()
        
    
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
        if os.path.isfile(TestConfig.SQLITE_USER_CONFIG_DB_PATH):
            os.remove(TestConfig.SQLITE_USER_CONFIG_DB_PATH)         
    
    
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
    

    def test_01_createEmptyConfig(self):
        """Test structure of newly created user config"""
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig()
        
        query = SELECT_TABLE_INFO.format(Table.DATABASES_TABLE)
        self.__SQLConnectProvider.open(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(query)
        #Data bases table check
        fields = [{'name' : DataField.ID, 'type' : 'INTEGER'}, {'name' : DataField.PATH, 'type' : 'text'}]
        res = self.checkFieldInTable(data, fields)    
        self.assertTrue(res)
        
        #Users table check
        query = SELECT_TABLE_INFO.format(Table.USERS_TABLE)         
        data = self.__SQLConnectProvider.executeFetch(query)    
        fields = [{'name' : DataField.ID, 'type' : 'INTEGER'}, {'name' : DataField.USERNAME, 'type' : 'text'},
                           {'name' : DataField.PASSWORD, 'type' : 'text'}, {'name' : DataField.FONT, 'type' : 'text'},
                           {'name' : DataField.FONT_SIZE, 'type' : 'INTEGER'}, {'name' : DataField.FONT_COLOR, 'type' : 'text'},
                           {'name' : DataField.PANEL_COLOR, 'type' : 'text'}]
        
        res = self.checkFieldInTable(data, fields)    
        self.assertTrue(res)
        
        #Database-user table check
        query = SELECT_TABLE_INFO.format(Table.USER_DATABASES_TABLE)          
        data = self.__SQLConnectProvider.executeFetch(query)      
        fields = [{'name' : DataField.ID, 'type' : 'INTEGER'}, {'name' : DataField.DB_ID, 'type' : 'INTEGER'},
                  {'name' : DataField.USER_ID, 'type' : 'INTEGER'}, {'name' : DataField.PASSWORD, 'type' : 'blob'}]
        res = self.checkFieldInTable(data, fields)    
        self.assertTrue(res)
        self.__SQLConnectProvider.closeConnection()
        
    
    def test_02_addNewUser(self):
        userName = 'user'
        password = 'password' 
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig() 
        c.addNewUser(userName, password) 
        #check if added
        query = '''SELECT * FROM {}'''.format(Table.USERS_TABLE)
        self.__SQLConnectProvider.open(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(query)
        self.__SQLConnectProvider.closeConnection() 
        
          
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][DataField.USERNAME], userName) 
        self.assertEqual(data[0][DataField.PASSWORD], self.crypt.hashSHA1(password))
          
        #Check exceptions
        #Second try to add the same user
        self.assertRaises(Exceptions.NotUniqueValueException, c.addNewUser, userName, password )
        
        
        
    def test_03_removeCurrentUser(self):
        #Fill the config DB
        userName = 'user'
        password = 'password' 
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig() 
        c.addNewUser(userName, password)    
        #Check   
        query = '''SELECT * FROM {}'''.format(Table.USERS_TABLE)
        self.__SQLConnectProvider.open(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(query)
        self.assertEqual(len(data), 1)
        c.removeCurrentUser()
        
        query = '''SELECT * FROM {}'''.format(Table.USERS_TABLE)  
        data = self.__SQLConnectProvider.executeFetch(query)   
        self.__SQLConnectProvider.closeConnection() 
        self.assertEqual(len(data), 0) 
        
        
    def test_04_addDBForCurrentUser(self):
        #Fill the config DB
        userName = 'user'
        password = 'password' 
        dbPath = 'path'
        dbPassword = 'pass'
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig() 
        c.addNewUser(userName, password)  
        
        c.addDBForCurrentUser(dbPath, dbPassword)
        
        self.__SQLConnectProvider.open(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(SQLqueries.SELECT_CONFIG_DBS_FOR_USER.format(userName))
        self.__SQLConnectProvider.closeConnection()
        
        self.assertEqual(len(data), 1)
        #self.assertEqual(data[0][DataField.USERNAME], userName)
        self.assertEqual(data[0][DataField.PATH], dbPath)     
        self.assertEqual(dbPassword, self.crypt.decipher(data[0][DataField.PASSWORD], password)) 
        
        #Check exceptions
        #Second try to add the same db
        self.assertRaises(Exceptions.DataBaseException, c.addDBForCurrentUser, dbPath, dbPassword ) 
        
        

    def test_05_removeDBFromUser(self):
        #Fill the config DB
        userName = 'user'
        password = 'password' 
        dbPath = 'path'
        dbPassword = 'pass'
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig() 
        c.addNewUser(userName, password)  
        #add and remove DB
        c.addDBForCurrentUser(dbPath, dbPassword)
        c.removeDBFromCurrentUser(dbPath)
        #get data from config DB
        self.__SQLConnectProvider.open(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        data = self.__SQLConnectProvider.executeFetch(SQLqueries.SELECT_CONFIG_DBS_FOR_USER.format(userName))
        self.__SQLConnectProvider.closeConnection()
         
        self.assertEqual(len(data), 0)
        
        
    def test_06_loadUserConfig(self):
        #Fill the config DB
        userName = 'user'
        password = 'password' 
        dbPath = 'path'
        dbPassword = 'pass'
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig() 
        c.addNewUser(userName, password)
        
        c2 = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c2.loadUserConfig(userName, password)
        #Check username and password
        self.assertEqual(c2.currentUserName, userName)
        self.assertEqual(c2.currentMasterPassword, password)
        
        
    def test_07_getCurrentUserConfig(self):
        #Fill the config DB
        userName = 'user'
        password = 'password' 
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig() 
        c.addNewUser(userName, password) 
        
        #Check data  
        data = c.getCurrentUserConfig()
        self.assertEqual(data[DataField.USERNAME], userName)
        self.assertEqual(data[DataField.PASSWORD], password)
        self.assertEqual(data[DataField.PANEL_COLOR], Default.DAFAULT_PANEL_COLOR)
        self.assertEqual(data[DataField.FONT], Default.DEFAULT_FONT)
        self.assertEqual(data[DataField.FONT_SIZE], Default.DEFAULT_FONT_SIZE)
        self.assertEqual(data[DataField.FONT_COLOR], Default.DEFAULT_FONT_COLOR)
        
        
    def test_08_getCurrentUserDBs(self):
        #Fill the config DB
        userName = 'user'
        password = 'password' 
        dbPath1 = 'path1'
        dbPassword1 = 'pass1'
        dbPath2 = 'path2'
        dbPassword2 = 'pass2'
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig()
         
        c.addNewUser(userName, password)                    

        c.addDBForCurrentUser(dbPath1, dbPassword1)  
        c.addDBForCurrentUser(dbPath2, dbPassword2) 
        
        data = c.getCurrentUserDBs() 
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0][DataField.PATH], dbPath1)
        self.assertEqual(data[0][DataField.PASSWORD], dbPassword1)
        self.assertEqual(data[1][DataField.PATH], dbPath2)
        self.assertEqual(data[1][DataField.PASSWORD], dbPassword2)
        
        
        
    def test_09_userExist(self):
        #Fill the config DB
        userName1 = 'user1'
        password1 = 'password1'
        userName2 = 'user2'
        password2 = 'password2'
        #not added
        userName3 = 'user3'
        password3 = 'password3'  
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig()
         
        c.addNewUser(userName1, password1)
        c.addNewUser(userName2, password2)
        
        self.assertTrue(c.userExist(userName1))
        self.assertTrue(c.userExist(userName2))
        self.assertFalse(c.userExist(userName3)) 
        
        
    def test_10_setCurrentUserSettings(self):
        #Fill the config DB
        userName1 = 'user1'
        password1 = 'password1'  
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig()
         
        c.addNewUser(userName1, password1)
        settings = {DataField.FONT : 'font1', DataField.FONT_COLOR : 'color1', DataField.FONT_SIZE : 20, DataField.PANEL_COLOR : 'color2'} 
        c.setCurrentUserSettings(**settings)
        
        #Check data  
        data = c.getCurrentUserConfig()
        self.assertEqual(data[DataField.PANEL_COLOR], settings[DataField.PANEL_COLOR])
        self.assertEqual(data[DataField.FONT], settings[DataField.FONT])
        self.assertEqual(data[DataField.FONT_SIZE], settings[DataField.FONT_SIZE])
        self.assertEqual(data[DataField.FONT_COLOR], settings[DataField.FONT_COLOR])
        
        
    def test_11_getCurrentUserSetting(self):
        #Fill the config DB
        userName1 = 'user1'
        password1 = 'password1'  
        c = UserConfigManager(TestConfig.SQLITE_USER_CONFIG_DB_PATH)
        c.createEmptyConfig()
         
        c.addNewUser(userName1, password1)
        data = c.getCurrentUserSetting(DataField.FONT)
        self.assertEqual(data, Default.DEFAULT_FONT)
        data = c.getCurrentUserSetting(DataField.FONT_SIZE)
        self.assertEqual(data, Default.DEFAULT_FONT_SIZE)
        data = c.getCurrentUserSetting(DataField.FONT_COLOR)
        self.assertEqual(data, Default.DEFAULT_FONT_COLOR)
        data = c.getCurrentUserSetting(DataField.PANEL_COLOR)
        self.assertEqual(data, Default.DAFAULT_PANEL_COLOR)          
        
        #Check exceptions
        #No existing settings key
        self.assertRaises(Exceptions.NoneObjectException, c.getCurrentUserSetting, DataField.EMAIL )                                        
        
    
if __name__ == '__main__':
    unittest.main()
    