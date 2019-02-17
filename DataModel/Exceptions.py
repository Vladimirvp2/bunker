'''
Defined exceptions used in the app
'''

class MyException(Exception):
    '''Base class for all app user exceptions'''
    def __init__(self, value, message):
        self.value = value
        self.message = message
    def __str__(self):
        return repr(' {}, {}'.format(self.value, self.message))   
    

class WrongPathException(MyException):
    '''If path doesn't exist'''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
    
    
    
class NoFileException(MyException):
    '''Used to check the absence of a file'''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        

class ExistFileException(MyException):
    '''Used to check the existence of a file'''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)           


    
class DataBaseException(MyException):
    '''Used for checking if the database is ok'''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        

class EntryException(MyException):
    '''Used for record/category operations'''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        
class NoneObjectException(MyException):
    '''Used to determine None object'''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)                     

class NotUniqueValueException(MyException):
    '''
    Used to alarm the attempt to add value to the DB filed
    that already contains such value
    '''
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        
        
class WrongUserException(MyException): 
    """If there is no such user in config file"""
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        
        
class WrongPasswordException(MyException): 
    """If wrong password for a particular username in config file"""
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        
class NoUserException(MyException): 
    """If there is no given user"""
    def __init__(self, value, message):
        MyException.__init__(self, value, message)          
        
class UserRemovedException(MyException): 
    """If user was removed from config and tyr to to some pperations with the user (add DBs, config info...)"""
    def __init__(self, value, message):
        MyException.__init__(self, value, message)
        
        
class WrongValueException(MyException): 
    """If there is no such value"""
    def __init__(self, value, message):
        MyException.__init__(self, value, message)                                  
    
#raise NotImplementedError()    
 
    
    