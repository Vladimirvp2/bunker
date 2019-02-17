'''
Containes some settings(like pathes) needed for running the tests
'''

#Directory where all the temporary files will be created. This dir is
#created by user, not automatically   
TEMP_DIR = r"D:/"
#DB file name. Should be in TEST_DIR
SQLITE_DB_PATH =  r"D:/example5.db"
SQLITE_USER_CONFIG_DB_PATH =  r"D:/userConfigTest.db"
#Path than doesn't exist on file system. Used to check wrong path exceptions
NO_EXISTING_PATH = r"D:/BadPath/"
NO_EXISTING_FILE = r"D:/bedfile.db"


DB_NAME = "Test database"
DB_PASSWORD = "Test password"
DB_COMMENTS = "Test comments"
#id of the first DB object 
DB_OBJECT_ID1 = '1'