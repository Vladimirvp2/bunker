'''
Classes for providing common interface for SQL database connection  
'''

from abc import ABCMeta, abstractmethod
import sqlite3
import Common.Constants.DataField as DataField
import SQLqueries as SQLqueries
import Exceptions


class SQLConnectProviderI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def open(self, path):
        "Open current connection and cursor"
        pass
       
    @abstractmethod
    def execute(self, query):
        """Execute given SQL query"""
        pass
    
    
    @abstractmethod
    def executeParams(self, query, fields):
        """
        Execute given SQL query with params
        @type query: string 
        @type fields: tuple
        """
        pass
    
    
    @abstractmethod
    def getBirary(self, field):
        """
        Binary transformation
        @type field: string
        @rtype: binary
        """
        pass    
    
    
    @abstractmethod    
    def getLastRowID(self):
        """Return id of the last inserted row"""
        pass
    
    @abstractmethod
    def executeFetch(self, query):
        """
        Execute the given SQL and return fetch result
        @type query: string
        @param query: SQL query
        @return: list of dicts. Each key of the dict corresponds to select query fields  
        """
        pass
    
    @abstractmethod
    def commit(self):
        """Commit the current connection"""
        pass
    
    @abstractmethod
    def closeConnection(self):
        """Close current connection"""
        pass
    
    
class SQLiteConnectProvider(SQLConnectProviderI):
    """Provide connection to SQLite databases"""
    
    #if support foreign keys constraint
    FK_ENABLED = True
    #to be able to insert and read encoded information
    TEXT_FACTOTY_ENABLED = True
    #make select query ad dict 
    ROW_FACTORY_ENABLED = True 
    
    def __init__(self):
        self.__cursor = None
        self.__conn = None
        
        
    def open(self, path):
        if self.__conn:
            self.commit()
            self.closeConnection()
            
        self.__conn = self.__getConnection(path)
        self.__cursor = self.__getCursorWithFK(self.__conn)  
       

    def execute(self, query):
        #try:
        self.__cursor.execute(query)           
        #except sqlite3.OperationalError as e:
        #    raise Exceptions.DataBaseException("Can't connect. Data base corrupted", "{}".format(e)) 
        #except sqlite3.DatabaseError as e:
        #    raise Exceptions.DataBaseException("Can't connect. Data base corrupted", "{}".format(e))
        #except sqlite3.IntegrityError as e:
        #    raise Exceptions.NotUniqueValueException("Value already exist or constrains limitation!", "{}".format(e)) 
        
        
    def executeParams(self, query, fields):
        self.__cursor.execute(query, fields)  
        
        
    def getBirary(self, field):
        return sqlite3.Binary(field)
  
        
        
    def getLastRowID(self):
        return self.__cursor.lastrowid 
    

    def executeFetch(self, query):
        #try:
        self.__cursor.execute(query)
        data = self.__cursor.fetchall()
        return data       
        #except sqlite3.OperationalError as e:
        #    raise Exceptions.DataBaseException("Can't connect. Data base corrupted", "{}".format(e))  
        #except sqlite3.DatabaseError as e:
        #    raise Exceptions.DataBaseException("Can't connect. Data base corrupted", "{}".format(e))
        #except sqlite3.IntegrityError as e:
        #    raise Exceptions.NotUniqueValueException("Value already exist or constrains limitation!", "{}".format(e))  

    
    
    def commit(self):
        self.__conn.commit() 
    

    def closeConnection(self):
        self.__conn.close()
        self.__cursor = None
        self.__conn = None
                
        
    def __getConnection(self, path):
        conn = sqlite3.connect(path)
        if self.ROW_FACTORY_ENABLED:
            conn.row_factory = self.__dict_factory
        if self.TEXT_FACTOTY_ENABLED:
            conn.text_factory = str 
            
        return conn
    
    def __getCursorWithFK(self, conn):
        c = conn.cursor() 
        c.execute(SQLqueries.SQLQuery.FOREIGN_KEY_ON)
        return c
    
    def __getCursorWithoutFK(self, conn):
        c = conn.cursor()                
        return c            
        
        
    def __dict_factory(self, cursor, row):
        '''Used in SQL select queries to create dictionary from result. Keys are fields in DB tables.
           The only exception - id field in DB. In the app it's called dbID to distinguish from local unique id
        '''
        d = {}
        for idx, col in enumerate(cursor.description):
            key =  DataField.DB_ID if col[0] == DataField.ID else col[0]  
            d[key] = row[idx]  
             
        return d  

