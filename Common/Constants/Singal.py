'''
Signals used in the app
'''


#ADD_NEW_CAREGORY = 0
ADD_NEW_RECORD = 1
UPDATE_CATEGORY = 2
UPDATE_RECORD = 3
REMOVE_CATEGORY = 4
REMOVE_RECORD = 5

LOGIN_OK = 6                #data [login, password]
APP_QUIT = 7                #data True - if needed confirmation, False if not needed
NEW_USER_REGISTER_OK = 8    #data [login, password] if a new user is registered in Register dialog
NOT_YET_AVAILABLE = 9       #data None, if the feature is not implemented yet
CATEGORY_RIGHT_CLICK = 10   #data event, if right click on the category panel in the main window
RECORD_RIGHT_CLICK = 11     #data event, if right click on the record panel in the main window
CATEGORY_SINGLE_CLICK = 12 
CATEGORY_DOUBLE_CLICK = 13
RECORD_CLICK = 14
EDIT_RECORD = 15
REMOVE_RECORD = 16
SHOW_ADD_NEW_RECORD_DIALOG = 17
SAVE_CURR_DB = 18
SHOW_EDIT_RECORD_DIALOG = 19

#Category panel
SHOW_ADD_NEW_CATEGORY_DIALOG = 20  #data None
ADD_NEW_CATEGORY = 21              #data dict of fields
SHOW_EDIT_CATEGORY_DIALOG = 22     #data None
EDIT_CATEGORY = 23                 #data dict of fields
REMOVE_CATEGORY = 24               #data None

#Connect
DB_CONNECT = 25
DB_DISCONNECT = 26
DB_REMOVE_FROM_CONFIG = 27
DB_REMOVE_FROM_FILE_SYSTEM = 28
DB_ADD_NEW = 29
DB_ADD_EXISTING_SHOW_DIALOG = 30
DB_ADD_EXISTING = 31

DB_ADD_NEW_SHOW_DIALOG = 32

DB_SELECTED_CHANGED = 33
CATEGORY_SELECTED_CHANGED = 34
RECORD_SELECTED_CHANGED = 35

#Settings
SHOW_SETTINGS_DIALOG = 36

#Info
SHOW_INFO_DIALOG = 37
SHOW_MANUAL = 38

#Auto password generate
SHOW_AUTO_GEN_DIALOG = 39
ENTROPY_COLLECTED = 40          #data [(x, y), (x, y)..]
ENTROPY_COLLECT_CANCEL = 41 

MEGRE_DB_SHOW_DIALOG = 42
MERGE_DB_ASK_USER = 43
MERGE_DB_USER_ANSWER = 44







