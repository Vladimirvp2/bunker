'''
Describe classes that are just containers for data base: category and record
'''

import Common.Constants.EntryStatus as EntryStatus
import Common.Constants.DBObjectType as DBObjectType
import Common.Constants.DBStatus as DBStatus
import Common.Constants.DataField as DataField
import Common.Constants.Default as Default


class Entry(object):
    """
    Base class for both records and categories
    """ 
    def __init__(self, id, dbID=Default.DEFAULT_NEW_ENTRY_DB_ID, comment=Default.DEFAULT_ENTRY_COMMENT):
        """
        @type  id: string
        @param id: id of a new entry 
        """
        self._id = id
        # set type of the new entry to record by default
        self._type = DBObjectType.RECORD
        self._comments = comment
        self._status = EntryStatus.NEW
        #self._dbID = str(dbID) 
        self._dbID = dbID 
        
    def edit(self, **args):
        """
        Edit entry fields(without saving in base)
        """ 
        pass 
    
    def info(self):
        """
        For printing data on the current entry
        @rtype: string
        @return: field values
        """ 
        pass 
        
        
    @property
    def id(self):
        return self._id
      
    @property
    def type(self):
        return self._type
    
    @property
    def comments(self):
        return self._comments
        
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        
    @property
    def dbID(self):
        return self._dbID
                

    @dbID.setter
    def dbID(self, value):
        # let set only for new records
        if self._dbID == Default.DEFAULT_NEW_ENTRY_DB_ID:
            self._dbID = str(value)
                      
        
        
#==============================================================================

class Category(Entry):
    """
    Container for categories of records
    """   
    def __init__(self, id, dbID=Default.DEFAULT_NEW_ENTRY_DB_ID, **args):
        Entry.__init__(self, id, dbID)
        
        self.__name = Default.DEFAULT_CATEGORY_NAME
        self._comments = Default.DEFAULT_ENTRY_COMMENT
        self._type = DBObjectType.CATEGORY
        #container for another potential categories and records
        self.__container = []    
        self.__assignData(**args)
        
    def __str__(self):
        return "Category" 
        #return 'Category-> id: {},  name: {}, comments: {}, db_ID: {}, status: {}, type: {}'.format(self._id, self.__name, self._comments, self._dbID, 
        #                                                                                  self._status, self._type)
        
    def info(self):
        return self.__str__()                                     

    def addnewEntry(self, entry):
        """
        @type  entry: Entry
        @param entry: entry to add 
        """        
        self.__container.append(entry)
            
        
    
    def __assignData(self, **args):
        if DataField.NAME in args.keys():
            self.__name = args[DataField.NAME]         
        if DataField.COMMENTS in args.keys():
            self._comments = args[DataField.COMMENTS]                       
    
    def edit(self, **args):
        #if removed, ignore edit
        if self._status == EntryStatus.REMOVED:
            return           
        self.__assignData(**args)
        if  self._status != EntryStatus.NEW:
            self._status = EntryStatus.CHANGED
            
    def getData(self):
        """
        Return dict of all category data
        """
        data = {}
        data[DataField.NAME] = self.name
        data[DataField.COMMENTS] = self.comments
        
        return data            
        
    @property
    def entries(self):
        return self.__container
    
    @property
    def name(self):
        return self.__name        
  
#==============================================================================
 
class Record(Entry): 
    """
    Container for a record
    """   
    def __init__(self, id, dbID=Default.DEFAULT_NEW_ENTRY_DB_ID, **args):
        Entry.__init__(self, id, dbID)        
        self._type = DBObjectType.RECORD   
        #set default values
        self.__site = Default.DEFAULT_RECORD_SITE
        self.__username = Default.DEFAULT_RECORD_USERNAME
        self.__password = Default.DEFAULT_RECORD_PASSWORD
        self.__email = Default.DEFAULT_RECORD_EMAIL
        self.__time = 0
        #check passes arguments
        self.__assignData(**args)                                    
           
    def __str__(self):
        return 'Record-> id: {},  site: {}, username: {}, comments: {}, db_ID: {}, status: {}, type: {}'.format(self._id, self.__site, self.__username,
                                                                                          self._comments, self._dbID, self._status, self._type)   
        
    def info(self):
        return self.__str__()               
    
    def __assignData(self, **args):
        if DataField.SITE in args.keys():
            self.__site = args[DataField.SITE]
        if DataField.USERNAME in args.keys():
            self.__username = args[DataField.USERNAME]
        if DataField.PASSWORD in args.keys():
            self.__password = args[DataField.PASSWORD]
        if DataField.EMAIL in args.keys():
            self.__email = args[DataField.EMAIL]  
        if DataField.COMMENTS in args.keys():
            self._comments = args[DataField.COMMENTS]
        if DataField.TIME in args.keys():
            self.__time = args[DataField.TIME]                  
    
    
    def edit(self, **args):
        #if removed, ignore edit
        if self._status == EntryStatus.REMOVED:
            return
        #do not change time
        if DataField.TIME in args.keys():
            return        
        self.__assignData(**args)
        if  self._status != EntryStatus.NEW:
            self._status = EntryStatus.CHANGED
            
    def getData(self):
        """
        Return dict of all record data
        """
        data = {}
        data[DataField.SITE] = self.site
        data[DataField.USERNAME] = self.username
        data[DataField.PASSWORD] = self.password
        data[DataField.EMAIL] = self.email
        data[DataField.COMMENTS] = self.comments
        
        return data
              
    @property
    def site(self):
        return self.__site
        
    @property
    def username(self):
        return self.__username
     
    @property
    def password(self):
        return self.__password

        
    @property
    def email(self):
        return self.__email

        
    @property
    def entries(self):
        return [] 
    
    
    @property
    def timestamp(self):
        return self.__time 
    
    
    
class DBEntryFactory(object):
    """Fabric for cteating DB entry objects(Categories, Records)"""
    @staticmethod
    def createEntry(entryType, id, **data):
        """
        @type entryType: DBobjectType
        @param entryType: type of the object to create
        @type data: dict
        @param data: data for entry creation
        @param id: id of the entry to create  
        @return Entry object
        """  
        
        if  entryType == DBObjectType.RECORD:
            return Record(id, **data)
        elif  entryType == DBObjectType.CATEGORY:
            return Category(id, **data)      
                                  