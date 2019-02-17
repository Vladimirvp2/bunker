"""Classes controllers for Login dialog"""

from Common.Utilities import*
from GUI.Dialogs.Register import Register
import UsConfig as Config
import Common.Constants.Singal as Signal
from DataModel.Exceptions import*
import logging
import GUI.MessageDialog as md


from abc import ABCMeta, abstractmethod


class LoginContollerI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def addView(self, view):
        "Add view to the controller"
        pass
       
    @abstractmethod
    def loginPress(self):
        "Call if login button pressed"
        pass
    
    @abstractmethod
    def cancelPress(self):
        "Call if cancel button pressed or dialog corner close button"
        pass
    
    @abstractmethod
    def registerPress(self):
        "Call if registration button pressed"
        pass
    
    
    
    
class LoginController(LoginContollerI):
    '''
    Controller for the login dialog
    If login button pressed the controller should check whether such combination
    of user name and password exists in the UsConfig. If not, show a message about the mismatch
    of either user name or password 
    '''
    def __init__(self, userConf, notifier, localization):
        #self.__loginDialog = loginDialog
        #self.__parent = parentLogin
        #self.__app = mainApp
        self.__userConfig = userConf 
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        
    def addView(self, view):
        self.__view = view
        
    def loginPress(self):
        #check the match of user name and password
        login = self.__view.getLogin().encode('utf8')
        password = self.__view.getPassword().encode('utf8')
        logging.debug("Login %s, Password %s ", login, password)
        
        try:
            self.__userConfig.loadUserConfig(login, password)
        except WrongUserException: 
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = self.__localization.getWord('you_entered_wrong_login'), 
                            buttonsText=[self.__localization.getWord('ok')])
            return        
        except WrongPasswordException:
            md.showError(self.__view, 
                            title = self.__localization.getWord('invalid_value'),
                            text = self.__localization.getWord('you_entered_wrong_password'), 
                            buttonsText=[self.__localization.getWord('ok')])
            return 
        
        #send signal about successful logging and pass login and password
        self.__view.destroy()  
        self.__notifier.sendSignal(Signal.LOGIN_OK, [login, password])

    
    def cancelPress(self):
        #send signal about quitting app
        self.__notifier.sendSignal(Signal.APP_QUIT, False)
    

    def registerPress(self):
        #show register dialog it the center of the screen
        registerDialog = Config.ASSEMBLER.assemble("RegisterView")
        centerTopLevel(registerDialog)
        self.__view.destroy()
                           
        
        