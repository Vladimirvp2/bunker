'''
Contains SQL queries used in the app
'''

from Common.Utilities import SuperEnum
import Common.Constants.Table as Table
import Common.Constants.DataField as DataField

class SQLQuery(SuperEnum):
    
    FOREIGN_KEY_ON = '''PRAGMA foreign_keys = ON;'''
    
    ROOT_CATEGORIES = '''SELECT {}, {}, {} FROM {} where {} is NULL'''.format(DataField.NAME, DataField.COMMENTS, DataField.ID,
                                                                      Table.CATEGORY_TABLE, DataField.PARENT)
    
    ROOT_RECORDS = '''SELECT {}, {}, {}, {}, {}, {} FROM {} where {} is NULL'''.format(DataField.ID, DataField.SITE, DataField.USERNAME,
                                                                           DataField.EMAIL, DataField.PASSWORD,
                                                                           DataField.COMMENTS,
                                                                           Table.RECORD_TABLE,
                                                                           DataField.PARENT) 
    
    SUB_CATEGORIES = '''SELECT {}, {}, {} FROM {} where {} = {} '''.format(DataField.NAME, DataField.COMMENTS, DataField.ID,
                                                                      Table.CATEGORY_TABLE, DataField.PARENT, '{}') 
    
    SELECT_ALL_CATEGORIES = '''SELECT {}, {}, {}, {} FROM {} '''.format(DataField.NAME, DataField.COMMENTS, DataField.ID, DataField.PARENT,
                                                                      Table.CATEGORY_TABLE)
    
    SELECT_ALL_RECORDS = '''SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM {} '''.format(DataField.ID, DataField.PARENT, DataField.SITE, DataField.USERNAME,
                                                                           DataField.EMAIL, DataField.PASSWORD, DataField.COMMENTS, DataField.TIME,
                                                                           Table.RECORD_TABLE
                                                                           ) 

       
    
    SUB_RECORDS = '''SELECT {}, {}, {}, {}, {}, {} FROM {} where {} = {}'''.format(DataField.ID, DataField.SITE, DataField.USERNAME,
                                                                           DataField.EMAIL, DataField.PASSWORD,
                                                                           DataField.COMMENTS,
                                                                           Table.RECORD_TABLE,
                                                                           DataField.PARENT,
                                                                           '{}') 
                
    INSERT_NEW_ROOT_RECORD = '''INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES (NULL, '{}', '{}', '{}', '{}', '{}' )
                               '''.format(Table.RECORD_TABLE,
                                          DataField.PARENT,
                                          DataField.SITE,
                                          DataField.USERNAME,
                                          DataField.EMAIL, 
                                          DataField.PASSWORD,
                                          DataField.COMMENTS,
                                          '{}', '{}', '{}', '{}', '{}') 
                               
                               
    INSERT_NEW_NOROOT_RECORD = '''INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES ({}, '{}', '{}', '{}', '{}', '{}' )
                             '''.format(Table.RECORD_TABLE,
                                        DataField.PARENT,
                                        DataField.SITE,
                                        DataField.USERNAME,
                                        DataField.EMAIL,
                                        DataField.PASSWORD,
                                        DataField.COMMENTS,
                                        '{}', '{}', '{}', '{}', '{}', '{}')                               
                               
                               
    UPDATE_RECORD = '''UPDATE {} SET {}='{}', {}='{}', {}='{}', {}='{}', {}='{}', {}=CURRENT_TIMESTAMP WHERE {} = {}
                    '''.format(Table.RECORD_TABLE,
                               DataField.SITE, '{}',
                               DataField.USERNAME, '{}',
                               DataField.EMAIL, '{}',
                               DataField.PASSWORD, '{}',
                               DataField.COMMENTS, '{}',
                               DataField.TIME,
                               DataField.ID, '{}' )                               
                                
            
                     
    INSERT_NEW_ROOT_CATEGORY = '''INSERT INTO {} ({}, {}, {}) VALUES (NULL, '{}', '{}' )
                               '''.format(Table.CATEGORY_TABLE,
                                          DataField.PARENT,
                                          DataField.NAME,
                                          DataField.COMMENTS,
                                          '{}', '{}' )
                               
    INSERT_NEW_NOROOT_CATEGORY = '''INSERT INTO {} ({}, {}, {}) VALUES ({}, '{}', '{}' )
                                 '''.format(Table.CATEGORY_TABLE,
                                            DataField.PARENT,
                                            DataField.NAME,
                                            DataField.COMMENTS,
                                            '{}', '{}', '{}' )                               
                   
    UPDATE_CATEGORY = '''UPDATE {} SET {}='{}', {}='{}' WHERE {} = {}
                      '''.format(Table.CATEGORY_TABLE,
                                 DataField.NAME, '{}',
                                 DataField.COMMENTS, '{}',
                                 DataField.ID, '{}' )                     
                               
                               
    REMOVE_RECORD = '''DELETE FROM {} WHERE {}={}
                    '''.format(Table.RECORD_TABLE,
                               DataField.ID,
                               '{}')
                    
    REMOVE_CATEGORY = '''DELETE FROM {} WHERE {}={}
                      '''.format(Table.CATEGORY_TABLE,
                               DataField.ID,
                               '{}')
               
    CREATE_METADATA_TABLE = '''CREATE TABLE {} ({} text, {} text, {} text )
                            '''.format(Table.METADATA_TABLE,
                                       DataField.NAME,
                                       DataField.PASSWORD,
                                       DataField.COMMENTS)                        
                               
    INSERT_INTO_METADATA_TABLE = '''INSERT INTO {} VALUES ('{}', '{}', '{}' )
                                 '''.format(Table.METADATA_TABLE,
                                            '{}', '{}', '{}' )
                                 
    CREATE_RECORD_TABLE = '''CREATE TABLE {} ({} INTEGER PRIMARY KEY   AUTOINCREMENT,
                                    {} INTEGER,
                                    {} text,
                                    {} text,
                                    {} text,
                                    {} text,
                                    {} text,
                                    {} TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                                    FOREIGN KEY({}) REFERENCES {}({}) ON DELETE CASCADE
                                    )
                '''.format(Table.RECORD_TABLE,
                           DataField.ID,
                           DataField.PARENT,
                           DataField.SITE,
                           DataField.USERNAME,
                           DataField.EMAIL,
                           DataField.PASSWORD,
                           DataField.COMMENTS,
                           DataField.TIME,
                           
                           DataField.PARENT,
                           Table.CATEGORY_TABLE,
                           DataField.ID)
                
                
    CREATE_CATEGORY_TABLE = '''CREATE TABLE {} ({} INTEGER PRIMARY KEY  AUTOINCREMENT,
                                    {} INTEGER,
                                    {} text,
                                    {} text,
                                    FOREIGN KEY({}) REFERENCES {}({}) ON DELETE CASCADE
                )
                '''.format(Table.CATEGORY_TABLE,
                           DataField.ID,
                           DataField.PARENT,
                           DataField.NAME,
                           DataField.COMMENTS,
                           
                           DataField.PARENT,
                           Table.CATEGORY_TABLE,
                           DataField.ID
                           )
                
    ADD_FOREIGN_KEY_FOR_RECORD_TABLE = '''ALTER TABLE {} ADD FOREIGN KEY ({}) REFERENCES {}({})
                                       '''.format(Table.RECORD_TABLE,
                                                  DataField.PARENT,
                                                  Table.CATEGORY_TABLE,
                                                  DataField.ID) 
    
    SELECT_FROM_METADATA = '''SELECT* FROM {}'''.format(Table.METADATA_TABLE)   
    
    
CREATE_CONFIG_DB_TABLE = '''CREATE TABLE {} ({} INTEGER PRIMARY KEY   AUTOINCREMENT,
                                             {} text UNIQUE NOT NULL
                                             )
                          '''.format(Table.DATABASES_TABLE,
                                     DataField.ID,
                                     DataField.PATH
                                     )
                                             
CREATE_CONFIG_USERS_TABLE = '''CREATE TABLE {} ({} INTEGER PRIMARY KEY   AUTOINCREMENT,
                                             {} text UNIQUE NOT NULL,
                                             {} text,
                                             {} text,
                                             {} INTEGER,
                                             {} text,
                                             {} text
                                              )
                            '''.format(Table.USERS_TABLE,
                                       DataField.ID,
                                       DataField.USERNAME,
                                       DataField.PASSWORD,
                                       DataField.FONT,
                                       DataField.FONT_SIZE,
                                       DataField.FONT_COLOR,
                                       DataField.PANEL_COLOR
                                     )
                            
CREATE_CONFIG_USER_DATABASES_TABLE = '''CREATE TABLE {} ({} INTEGER PRIMARY KEY   AUTOINCREMENT,
                                    {} INTEGER NOT NULL,
                                    {} INTEGER NOT NULL,
                                    {} BLOB,
                                    FOREIGN KEY({}) REFERENCES {}({}) ON DELETE CASCADE,
                                    FOREIGN KEY({}) REFERENCES {}({}) ON DELETE CASCADE,
                                    unique ({}, {})
                                    ) 
                                    '''.format(Table.USER_DATABASES_TABLE,
                                               DataField.ID,
                                               DataField.DB_ID,
                                               DataField.USER_ID,
                                               DataField.PASSWORD,
                                               
                                               DataField.DB_ID,
                                               Table.DATABASES_TABLE,
                                               DataField.ID,
                                               
                                               DataField.USER_ID,
                                               Table.USERS_TABLE,
                                               DataField.ID,
                                               
                                               DataField.DB_ID,
                                               DataField.USER_ID
                                               )   
                                    
                                    
ADD_CONFIG_USER = '''INSERT INTO {} ({}, {}, {}, {}, {}, {}) VALUES ('{}', '{}', '{}', {}, '{}', '{}' )
                               '''.format(Table.USERS_TABLE,
                                          DataField.USERNAME,
                                          DataField.PASSWORD,
                                          DataField.FONT,
                                          DataField.FONT_SIZE,
                                          DataField.FONT_COLOR,
                                          DataField.PANEL_COLOR,
                                          '{}', '{}', '{}', '{}', '{}', '{}') 
                               
                               
REMOVE_CONFIG_USER = '''DELETE FROM {} WHERE {}={}
                      '''.format(Table.USERS_TABLE,
                               DataField.ID,
                               '{}')
                      
SELECT_CONFIG_USER_BY_NAME = '''SELECT * from {} WHERE {} = '{}' '''.format(Table.USERS_TABLE,
                                                                 DataField.USERNAME,
                                                                 '{}'
                                                                   ) 


ADD_CONFIG_DB = '''INSERT INTO {} ({}) VALUES ('{}' )
                               '''.format(Table.DATABASES_TABLE,
                                          DataField.PATH,
                                          '{}')
                               
                           
                        
                           
ADD_CONFIG_DB_TO_USER = '''INSERT INTO {}({}, {}, {}) 
                              SELECT {}, (SELECT {} FROM {} WHERE {}={}), {} from {} WHERE {}={} 
                           '''.format(Table.USER_DATABASES_TABLE, 
                                      DataField.DB_ID,
                                      DataField.USER_ID,
                                      DataField.PASSWORD,
                                      
                                      DataField.ID,
                                      DataField.ID,
                                      Table.USERS_TABLE,
                                      DataField.USERNAME,
                                      '?',
                                      '?',
                                      Table.DATABASES_TABLE,
                                      DataField.PATH,
                                      '?' )                           
                           
                           
                                                       
DELETE_CONFIG_DB_FROM_USER = '''DELETE FROM {} where {} = (SELECT {} FROM {} WHERE {}='{}')
                                AND {}=(SELECT {} FROM {} WHERE {} = '{}' )
                            '''.format(Table.USER_DATABASES_TABLE,
                                       DataField.DB_ID,
                                       DataField.ID,
                                       Table.DATABASES_TABLE,
                                       DataField.PATH,
                                       '{}',
                                       DataField.USER_ID,
                                       DataField.ID,
                                       Table.USERS_TABLE,
                                       DataField.USERNAME,
                                       '{}'
                                       )
                            
SELECT_CONFIG_DBS_FOR_USER = '''SELECT {}, {}.{} FROM {} 
                                INNER JOIN 
                                {} 
                                ON {}.{} = {}.{} 
                                WHERE {}.{} = (SELECT {} FROM {} WHERE {}='{}')
                            '''.format(DataField.PATH,
                                       Table.USER_DATABASES_TABLE,
                                       DataField.PASSWORD,
                                       Table.DATABASES_TABLE,
                                       Table.USER_DATABASES_TABLE,
                                       Table.DATABASES_TABLE,
                                       DataField.ID,
                                       Table.USER_DATABASES_TABLE,
                                       DataField.DB_ID,
                                       Table.USER_DATABASES_TABLE,
                                       DataField.USER_ID,
                                       DataField.ID,
                                       Table.USERS_TABLE,
                                       DataField.USERNAME,
                                       '{}' )
                            
SELECT_CONFIG_ALL_USERS = '''SELECT {} FROM {}
                          '''.format(DataField.USERNAME,
                                     Table.USERS_TABLE )
                          
REMOVE_CONFIG_CURRENT_USER = '''DELETE FROM {} WHERE {} = '{}' 
                             '''.format(Table.USERS_TABLE,
                                        DataField.USERNAME,
                                        '{}'
                                        )
                             
UPDATE_CONFIG_SETTINGS_FOR_CURRENT_USER = '''UPDATE {} SET {} = '{}', {} = {}, {} = '{}', {} = '{}' 
                                            WHERE {} = '{}'
                                          '''.format(Table.USERS_TABLE,
                                                    DataField.FONT, '{}',
                                                    DataField.FONT_SIZE, '{}',
                                                    DataField.FONT_COLOR, '{}',
                                                    DataField.PANEL_COLOR, '{}',
                                                    DataField.USERNAME, '{}'
                                                    )
                                          

SELECT_CONFIG_DB_BY_PATH = """
                            SELECT * FROM {} WHERE {} = '{}' 
                            """.format(Table.DATABASES_TABLE,
                                       DataField.PATH,
                                       '{}') 
                            
                                           

                                          
TABLE_INFO = """PRAGMA table_info({})"""  



SELECT_NOROOT_RECORDS_BY_SITE = """SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM {} WHERE {}='{}' AND {}='{}'""".format(DataField.ID, DataField.PARENT, DataField.SITE, DataField.USERNAME,
                                                                           DataField.EMAIL, DataField.PASSWORD, DataField.COMMENTS, DataField.TIME,
                                                                           Table.RECORD_TABLE,
                                                                           DataField.SITE,
                                                                           '{}',
                                                                           DataField.PARENT,
                                                                           '{}'
                                                                           )
    
SELECT_ROOT_RECORDS_BY_SITE = """SELECT {}, {}, {}, {}, {}, {}, {}, {} FROM {} WHERE {}='{}' AND {} is NULL""".format(DataField.ID, DataField.PARENT, DataField.SITE, DataField.USERNAME,
                                                                           DataField.EMAIL, DataField.PASSWORD, DataField.COMMENTS, DataField.TIME,
                                                                           Table.RECORD_TABLE,
                                                                           DataField.SITE,
                                                                           '{}',
                                                                           DataField.PARENT
                                                                           ) 


SELECT_ROOT_CATEGORIES_BY_NAME = """SELECT {}, {}, {}, {} FROM {} WHERE {}='{}' AND {} is NULL""".format(DataField.NAME, DataField.COMMENTS, DataField.ID, DataField.PARENT,
                                                                      Table.CATEGORY_TABLE,
                                                                      DataField.NAME,
                                                                      '{}',
                                                                      DataField.PARENT)
    
SELECT_NOROOT_CATEGORIES_BY_NAME = """SELECT {}, {}, {}, {} FROM {} WHERE {}='{}' AND {} = '{}' """.format(DataField.NAME, DataField.COMMENTS, DataField.ID, DataField.PARENT,
                                                                      Table.CATEGORY_TABLE,
                                                                      DataField.NAME,
                                                                      '{}',
                                                                      DataField.PARENT,
                                                                      '{}')

                                                                                                        
             

if __name__ == "__main__":
    print SQLQuery.ROOT_CATEGORIES
    print "==========================="
    print SQLQuery.ROOT_RECORDS
    print "==========================="
    print SQLQuery.SUB_CATEGORIES
    print "==========================="
    print SQLQuery.SUB_RECORDS
    print "==========================="
    #Insert record
    print SQLQuery.INSERT_NEW_ROOT_RECORD
    print "==========================="    
    print SQLQuery.INSERT_NEW_NOROOT_RECORD
    print "==========================="
    #Update records    
    print SQLQuery.UPDATE_RECORD
    print "==========================="       
    #Insert categories   
    print SQLQuery.INSERT_NEW_ROOT_CATEGORY
    print "==========================="    
    print SQLQuery.INSERT_NEW_NOROOT_CATEGORY 
    print "===========================" 
    #Update categories   
    print SQLQuery.UPDATE_CATEGORY
    print "===========================" 
    #Remove record
    print SQLQuery.REMOVE_RECORD
    print "===========================" 
    #Remove category
    print SQLQuery.REMOVE_CATEGORY 
    print "===========================" 
    # create DB structure queries      
    print SQLQuery.CREATE_METADATA_TABLE 
    print "==========================="  
    print SQLQuery.INSERT_INTO_METADATA_TABLE
    print "==========================="
    print SQLQuery.CREATE_RECORD_TABLE
    print "==========================="
    print SQLQuery.CREATE_CATEGORY_TABLE 
    print "==========================="                     
    print SQLQuery.ADD_FOREIGN_KEY_FOR_RECORD_TABLE
    print "===========================" 
    print SQLQuery.SELECT_FROM_METADATA   
    
    #Config queries
    print "===========================" 
    print CREATE_CONFIG_DB_TABLE
    print "===========================" 
    print CREATE_CONFIG_USERS_TABLE
    print "===========================" 
    print CREATE_CONFIG_USER_DATABASES_TABLE
    print "===========================" 
    print ADD_CONFIG_USER
    print "==========================="     
    print SELECT_CONFIG_USER_BY_NAME
    print "==========================="     
    print ADD_CONFIG_DB
    print "===========================" 
    print ADD_CONFIG_DB_TO_USER
    print "==========================="   
    print DELETE_CONFIG_DB_FROM_USER
    print "==========================="    
    print SELECT_CONFIG_DBS_FOR_USER
    print "===========================" 
    print SELECT_CONFIG_ALL_USERS
    print "===========================" 
    print REMOVE_CONFIG_CURRENT_USER 
    print "===========================" 
    print UPDATE_CONFIG_SETTINGS_FOR_CURRENT_USER  
    print "==========================="     

    
    
    #print SELECT_CONFIG_DBS_FOR_USER 
    print ADD_CONFIG_DB_TO_USER
    
    print SELECT_CONFIG_DBS_FOR_USER
    
    print SELECT_CONFIG_DB_BY_PATH
    
    
    print SELECT_ROOT_RECORDS_BY_SITE
    print "===========================" 
    print SELECT_NOROOT_RECORDS_BY_SITE
    print SELECT_ROOT_CATEGORIES_BY_NAME
    print SELECT_NOROOT_CATEGORIES_BY_NAME
 