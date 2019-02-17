'''
Hold users databases and settings
'''

import sqlite3, os, re, logging
import Exceptions
#import UsConfig as Config
from Common.Crypt import*
import SQLqueries as SQLqueries
from Common.Constants import DataField
from Common.Constants.Default import*
import Common.Constants.Table as Table
import Common.Constants.PasswordStrength as PasswordStrength
import Common.Constants.DataField as DataField
import Common.Constants.LabelType as LabelType
#from SQLconnection import SQLiteConnector
from SQLConnectProvider import SQLiteConnectProvider

#MASTER_PASSWORD = "password"
USER_NAME = "Vova2"



class UserConfigManager(object):
    
    
    def __init__(self, path = Config.CONFIG_FILE_PATH):
        self.crypt = CryptAES()
        self.__userSettings = {}
        self.__userDatabases = []
        self.__Users = []
        self.__masterPassword = DEFAULT_USER_MASTER_PASSWORD
        self.__userName = DEFAULT_USER_NAME
        #path to config file
        self.__path = path
        #Cached values
        self.__basesChanged = True
        self.__settingsChanged = True
        self.__usersChagned = True
        #if set True all operations(adding/removing DBs, config data for the current user) will be ignored 
        self.__currentUserRemoved = False  
        
        self.__initDefaultUserSettings() 
        #should be injected
        self.__SQLConnectProvider = SQLiteConnectProvider()  
        
        
    @property
    def currentUserName(self):
        return self.__userName
    
    @property
    def currentMasterPassword(self):
        return self.__masterPassword
        
    
    def createEmptyConfig(self):
        """Create a new db config file with table structure. Tables are empty"""
        logging.debug("Creating empty config DB with file {}".format(self.__path))
        
        #remove DB file if exist
        if os.path.isfile(self.__path):
            os.remove(self.__path) 

        #create DB structure
        self.__SQLConnectProvider.open(self.__path)
        
        queries = [SQLqueries.SQLQuery.FOREIGN_KEY_ON, SQLqueries.CREATE_CONFIG_DB_TABLE,
                   SQLqueries.CREATE_CONFIG_USERS_TABLE, SQLqueries.CREATE_CONFIG_USER_DATABASES_TABLE]
        #create DB structure
        for query in queries:
            #c.execute(query) 
            self.__SQLConnectProvider.execute(query)                 
        
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
        logging.debug("Empty config DB with file {} successfully created".format(self.__path))
        
    
    def addNewUser(self, userName, password):
        """
        Add new user while registration
        @type  userName: string
        @param userName: name of the user
        @type  password: string
        @param password: user's password
        @raise NotUniqueValueException: if the user with such name already exist(should be unique)     
        """
        
        logging.debug("Adding a new user with username: {}, password: {}".format(userName, password))
        
        self.__createEmpryConfigIfNotExist()           

        self.__SQLConnectProvider.open(self.__path)
        #check whether a user with such username already exist. If so raise exception
        query = SQLqueries.SELECT_CONFIG_USER_BY_NAME.format(userName)
        data = self.__SQLConnectProvider.executeFetch(query)
        if len(data) > 0:
            self.__SQLConnectProvider.commit()
            self.__SQLConnectProvider.closeConnection()
            raise Exceptions.NotUniqueValueException(userName, "Such username already exist!") 
        
        #if there is no such user add it
        query = SQLqueries.ADD_CONFIG_USER.format(userName, self.crypt.hashSHA1(password), DEFAULT_FONT, DEFAULT_FONT_SIZE, 
                                              DEFAULT_FONT_COLOR, DAFAULT_PANEL_COLOR)
        self.__SQLConnectProvider.execute(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
            
        #renew master password
        self.__masterPassword = password
        self.__userName = userName
        self.__usersChagned = True
        self.__currentUserRemoved = False    
        logging.debug("New user with username:{}, password:{} successfully added".format(userName, password))
        
        
    def checkNewLogin(self, login):
        """
        Checks if the provided login contains valid values
        @type login: string
        @return: boolean 
        """
        return self.__checkValidUserCredentials(login)
    
    
    def checkNewPassword(self, password):
        """
        Checks if the provided password contains valid values
        @type password: string
        @return: boolean 
        """
        return self.__checkValidUserCredentials(password)
        
        
    def defineStrengthOfPassword(self, password):
        """
        Determine the level of strength of the provided password
        @type password: string
        @param password: password which strength should be defined
        @return PasswordStrength
        """
        
        #strong if the length is more than 8, and it contains digits, lower and  capital letters
        #middle if the length is 5-8
        #weak if the length is 1-5 exclusive
        #==================================================== TO DO!!!!!!!!!!!!! =========================================================
        passwordLen = len(password)
        if passwordLen > 8:
            return PasswordStrength.STRONG
        elif passwordLen >5:
            return PasswordStrength.MIDDLE
        else:
            return PasswordStrength.WEAK     
    
        
    def addDBForCurrentUser(self, path, password):
        """
        Add new database info to the current user config
        @type  path: string
        @param path: full path of the DB file to be added
        @type  password: string
        @param password: user's password
        @raise WrongPasswordException: if can't write encrypted password to DB. The user should change the password
        @raise UserRemovedException: if the user removed itself from config and tries to perform some operations with config data
        @raise DataBaseException: if the same DB added to the user twice or if no current user exist in the config DB 
        """
        logging.debug("Adding a DB to the user path: {}, password: {}".format(path, password)) 
        
        self.__currenUserRemovedCheck()      
        self.__createEmpryConfigIfNotExist()  
        
        self.__SQLConnectProvider.open(self.__path)
        #check whether such DB already exist in databases table
        query = SQLqueries.SELECT_CONFIG_DB_BY_PATH.format(path)
        data = self.__SQLConnectProvider.executeFetch(query)
        #if the db with such path doesn't exist add it
        if len(data) == 0:
            query = SQLqueries.ADD_CONFIG_DB.format(path)
            self.__SQLConnectProvider.execute(query)
            self.__SQLConnectProvider.commit()
             
        #check if the db already added to the user
        query = SQLqueries.SELECT_CONFIG_DBS_FOR_USER.format(self.__userName)
        data = self.__SQLConnectProvider.executeFetch(query)
        for d in data:
            #if a db with such path already added to the user raise exception
            if d[DataField.PATH] == path:
                self.__SQLConnectProvider.commit()
                self.__SQLConnectProvider.closeConnection()
                raise Exceptions.DataBaseException("Integrity Error", "Database already added to the user {}".format(self.__userName))
        
        #add new DB data        
        query = SQLqueries.ADD_CONFIG_DB_TO_USER
        self.__SQLConnectProvider.executeParams(query, (self.__userName,
                          self.__SQLConnectProvider.getBirary(self.crypt.cipher(password, self.__masterPassword)),
                           path))
        
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
            
        self.__basesChanged = True
        logging.debug("DB with path: {}, password: {} successfully added to the user {}".format(path, password, self.__userName))  
        
        
        
    def removeDBFromCurrentUser(self, path):
        """
        Remove DB from the current user config
        @type  path: string
        @param path: full path of the DB file to be added  
        @raise UserRemovedException: if the user removed itself from config and rties to perform some operations with config data                       
        """
        
        logging.debug("Removing database with path {} from the current user {}".format(path, self.__userName)) 
        self.__currenUserRemovedCheck()       
        self.__createEmpryConfigIfNotExist()  
        
        #conn = self.__SQLConnector.getConnection(self.__path)
        #c = self.__SQLConnector.getCursorWithFK(conn)
        self.__SQLConnectProvider.open(self.__path)
         
        query = SQLqueries.DELETE_CONFIG_DB_FROM_USER.format(path, self.__userName)
        #c.execute(query)
        self.__SQLConnectProvider.execute(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
                                               
        #self.__SQLConnector.closeConnection(conn) 
        self.__basesChanged = True        
        logging.debug("database with path {} successfully removed from the current user {}".format(path, self.__userName))                  
        
    
    def loadUserConfig(self, userName, password):
        """
        Load config info for the given user if log in
        @type  userName: string
        @param userName: name of the user
        @type  password: string
        @param password: user's password
        @raise WrongUserException: if no user with such userName and password found
        @raise WrongPasswordException: if the password fora particular user is wrong                      
        """
        logging.debug("Loading user config info with username: {}, password: {}".format(userName, password))
        #check if config file exist
        self.__createEmpryConfigIfNotExist()  
        
        self.__SQLConnectProvider.open(self.__path)
        #check if user exist
        query = SQLqueries.SELECT_CONFIG_USER_BY_NAME.format(userName) 
        data = self.__SQLConnectProvider.executeFetch(query)#c.fetchall()
        if len(data) == 0:
            self.__SQLConnectProvider.commit()
            self.__SQLConnectProvider.closeConnection()
            raise Exceptions.WrongUserException(userName, "Can't load config of the user. No such user in config file")
        else:
            #check if password match
            passwordDB = str(data[0][DataField.PASSWORD])
            if (passwordDB != self.crypt.hashSHA1(password)):
                self.__SQLConnectProvider.commit()
                self.__SQLConnectProvider.closeConnection()
                raise Exceptions.WrongPasswordException(password, "Password doesn't match the username {}".format(userName))
            #renew master password and username
            logging.debug("User and password match OK. Loading data...")
            #close connection
            self.__SQLConnectProvider.commit()
            self.__SQLConnectProvider.closeConnection()
            #assign user's data
            self.__userName = userName    
            self.__masterPassword = password 
            self.__currentUserRemoved = False
            #load user settings data
            self.__userSettings = data[0]
            
            # ================================ TO DO =================================================
            self.__userSettings[DataField.CHANGE_DB_PATH_TO_NAME_AFTER_CONN] = DEFAULT_CHANGE_DB_PATH_TO_NAME_AFTER_CONN
            # ================================ TO DO =================================================            
            
            #get user databases
            self.__loadUserDBs(userName)
             
    
    def getCurrentUserConfig(self):    
    #def getCurrentUserSettings(self):
        """
        @return: list
        @raise UserRemovedException: if the user removed itself from config and rties to perform some operations with config data
        @raise NoUserException: if the is no current user in DB config 
        """
        logging.debug("Getting current user settings")
        self.__currenUserRemovedCheck()  
        if self.__settingsChanged:
            self.__loadUserConfig(self.__userName)
        self.__settingsChanged = False     
        return self.__userSettings
    
    
    def getCurrentUserSetting(self, key):
        """
        @type key: string
        @param key: key of setting. See DataField file 
        @return: value of the key
        @raise UserRemovedException: if the user removed itself from config and rties to perform some operations with config data
        @raise NoneObjectException: if the is no given key 
        """
        logging.debug("Getting current user setting {}".format(key))
        settings = self.getCurrentUserConfig()
        if key in settings.keys():
            return self.__userSettings[key]
        raise Exceptions.NoneObjectException(key, "No such key in current user settings")    
    
    
    def getCurrentUserDBs(self):
        """
        @return: list of dict - {'path', 'password'}
        @raise UserRemovedException: if the user removed itself from config and rties to perform some operations with config data
        """
        logging.debug("Getting current user DBs")
        self.__currenUserRemovedCheck()  
        if self.__basesChanged:
            self.__loadUserDBs(self.__userName)
        self.__basesChanged = False    
        return self.__userDatabases
    
    
    def setCurrentUserSettings(self, **args):
        """
        Update current user settings
        @type  args: dict
        @param args: config values to be changed     
        """
        logging.debug("Updating current user settings {}".format(args.values()))
        #assign provided values to settings
        for arg in args.keys():
            self.__userSettings[arg] = args[arg]
            
        #save in config DB
        self.__createEmpryConfigIfNotExist() 

        self.__SQLConnectProvider.open(self.__path) 
        query = SQLqueries.UPDATE_CONFIG_SETTINGS_FOR_CURRENT_USER.format(self.__userSettings[DataField.FONT], 
                                                                          self.__userSettings[DataField.FONT_SIZE],
                                                                          self.__userSettings[DataField.FONT_COLOR],
                                                                          self.__userSettings[DataField.PANEL_COLOR],   
                                                                          self.__userName)
        self.__SQLConnectProvider.execute(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()        
        
        self.__settingsChanged = True
        
        logging.debug("Settings update of the current user successfully finished {}".format(args.values()))
             
    
    def removeCurrentUser(self):
        """
        Remove current user from DB config
        @raise UserRemovedException: if the user already removed
        """
        logging.debug("Removing current user {} from DB config".format(self.__userName))
        self.__currenUserRemovedCheck()
        
        self.__usersChagned = True
        self.__currentUserRemoved = True
        
        self.__createEmpryConfigIfNotExist()   
                  
        self.__SQLConnectProvider.open(self.__path) 
        query = SQLqueries.REMOVE_CONFIG_CURRENT_USER.format(self.__userName)         
        self.__SQLConnectProvider.execute(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
        logging.debug("Current user {} successfully removed from DB config".format(self.__userName))     
    
   
    def userExist(self, userName):
        """
        Check whether a user with the given name already exist. Cached method. 
        If no user added or removed it uses previously loaded data
        Otherwise loads it from DB config
        @type  userName: string
        @param userName: name of the user to check
        @rtype: boolean
        @return: True if exist, otherwise False        
        """
        logging.debug("User exist check method")
        #if some user was added or removed load users from DB config
        if self.__usersChagned:
            self.__loadAllUsers()
        #find provided user
        if userName in self.__Users:
            return True
        return False 
         
    
    
    def __checkValidUserCredentials(self, value):
        """
        Checks if the provided string contains valid symbols
        @type value: string
        @param value: string to check
        @return: boolean. True if match, otherwise False  
        """
        pattern = re.compile('[-0-9a-zA-Z_\.]+')
        result = pattern.findall(value)
        if len(result) == 1 and len(result[0]) == len(value):
            return True        
        
        return False       
     
                
    def __loadUserDBs(self, userName): 
        #check if config file exist
        logging.debug("Loading DBs for the current user")
        self.__createEmpryConfigIfNotExist()  
                              
        self.__SQLConnectProvider.open(self.__path)    
        
        query = SQLqueries.SELECT_CONFIG_DBS_FOR_USER.format(userName) 
        data = self.__SQLConnectProvider.executeFetch(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
         
        self.__userDatabases = data
        #decrypt database password
        for db in self.__userDatabases:
            if DataField.PASSWORD in db.keys():
                db[DataField.PASSWORD] = self.crypt.decipher(db[DataField.PASSWORD], self.__masterPassword)                                
    
    
    def __loadUserConfig(self, userName):
        logging.debug("Loading settings for the current user")
        #check if config file exist
        self.__createEmpryConfigIfNotExist()
                               
        self.__SQLConnectProvider.open(self.__path) 
              
        query = SQLqueries.SELECT_CONFIG_USER_BY_NAME.format(userName) 
        data =  self.__SQLConnectProvider.executeFetch(query)
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection()
        
        if len(data) == 0:
            raise Exceptions.NoUserException("userName", "Can't load settings for user {}. No such user in config".format(userName))
        else:
            self.__userSettings = data[0]
            self.__userSettings[DataField.PASSWORD] = self.__masterPassword
            # ================================ TO DO =================================================
            self.__userSettings[DataField.CHANGE_DB_PATH_TO_NAME_AFTER_CONN] = DEFAULT_CHANGE_DB_PATH_TO_NAME_AFTER_CONN
            # ================================ TO DO ================================================= 
                                
    
    def __loadAllUsers(self):
        """
        Load all users from DB config if a new user was added or removed
        """
        logging.debug("Loading all users from DB cinfig")
        self.__Users = []
        self.__createEmpryConfigIfNotExist()    
                        
        self.__SQLConnectProvider.open(self.__path)  
        query = SQLqueries.SELECT_CONFIG_ALL_USERS
        usersData = self.__SQLConnectProvider.executeFetch(query) #c.fetchall()
        self.__SQLConnectProvider.commit()
        self.__SQLConnectProvider.closeConnection() 
        
        for userData in usersData:
            self.__Users.append(userData[DataField.USERNAME])
            
        self.__usersChagned = False    
                                     
    
    def __currenUserRemovedCheck(self):
        """Check whether the current user was removed from the config DB.
          The method is used in all the config operations with the Db config
        """
        if self.__currentUserRemoved:
            raise Exceptions.UserRemovedException(self.__userName, "User removed!")
             
        
    def __createEmpryConfigIfNotExist(self):
        if not os.path.isfile(self.__path):
            self.createEmptyConfig()       
        
    def __initDefaultUserSettings(self):
        self.__userSettings[DataField.FONT] = DEFAULT_FONT
        self.__userSettings[DataField.FONT_SIZE] = DEFAULT_FONT_SIZE
        self.__userSettings[DataField.FONT_COLOR] = DEFAULT_FONT_COLOR
        self.__userSettings[DataField.PANEL_COLOR] = DAFAULT_PANEL_COLOR
        
if __name__ == '__main__':        
    c = UserConfigManager(r"D:/fff.db")
    #c.loadUserConfig('Vova4', '1')
    #c.loadUserConfig('Vova5', '12345F2')
    c.createEmptyConfig()
    #c.loadUserConfig('Vova5', '12345F2')
    c.addNewUser('Vova5', '12345F2')
    #c.addNewUser('Vova5', '1')

    
    
    
    #print ADD_CONFIG_DB_TO_USER_TTT
    c.addDBForCurrentUser(r"D:/basa5.db", 'pass6')
    
    
    data = c.getCurrentUserDBs()
    for d in data:
        print d    
    

