"""Classes controllers for Register dialog"""


from abc import ABCMeta, abstractmethod
import Common.Constants.Singal as Signal
import Common.Constants.PasswordStrength as PasswordStrength
import Common.Constants.Colors as Colors
#from tkMessageBox import *
import DataModel.Exceptions as Exceptions
import GUI.MessageDialog as md



class RegisterControllerI(object):
    """
    Login view intergace 
    """
    
    __metaclass__ = ABCMeta
    @abstractmethod
    def addView(self, view):
        """Add view to the controller"""
        pass
       
           
    @abstractmethod
    def cancelPress(self):
        """Call if cancel button pressed or dialog corner close button"""
        pass
    
    @abstractmethod
    def registerPress(self):
        """Call if registration button pressed"""
        pass
    
    @abstractmethod
    def loginEntryChanged(self):
        """Call if a character added or removed from ligin entry
           used do define whether such username alreagy exist 
        """
        pass     
    
    
    @abstractmethod
    def passwordEntryChanged(self):
        """Call if a character added or removed from password entry
           used do define strength of the password 
        """
        pass 
    
    @abstractmethod
    def passwordConfirmEntryChanged(self):
        """
        Call if a character added or removed from password confirm entry
        used do define the match in password entry and confirm password entry
        """
        pass
    
    
    
    
class RegisterController(RegisterControllerI):
    '''
    Controller for the Register dialog
    The controller checks if the provided data is correct, creates a new user
    and sends a signal about successful registration
    '''
    def __init__(self, userConf, notifier, localization):
        self.__userConfig = userConf 
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        
    def addView(self, view):
        self.__view = view
        
   
    def cancelPress(self):
        #send signal about quitting app
        self.__notifier.sendSignal(Signal.APP_QUIT, False)
        self.__view.destroy()
    
    
    def registerPress(self):
        #get entered information
        login = self.__view.getLoginEntry().get()
        password = self.__view.getPasswordEntry().get()
        confirmPassword = self.__view.getConfirmPasswordEntry().get()
        #check if not 0 in length
        if len(login) == 0:
            #showerror(self.__localization.getWord('invalid_login'), 
            #          self.__localization.getWord('login_at_least_1_symbol'))
            
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = self.__localization.getWord('login_at_least_1_symbol'), 
                buttonsText=[self.__localization.getWord('ok')])
            return 
        #check if user doesn't contains correct symbols
        if not self.__userConfig.checkNewLogin(login):
#             showerror(self.__localization.getWord('invalid_symbols'), 
#                       "{}. \n{} {}".format(
#                                            self.__localization.getWord('login_contains_invalid_symbols'),
#                                            self.__localization.getWord('should_be_only'),
#                                            self.__localization.getWord('login_valid_symbols')
#                                            ))
            
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_value'),
                text = "{} {}. \n{} {}".format(
                                               self.__localization.getWord('login'),
                                               self.__localization.getWord('contains_invalid_value'),
                                               self.__localization.getWord('should_be_only'),
                                               self.__localization.getWord('login_valid_symbols')
                                               ), 
                buttonsText=[self.__localization.getWord('ok')])        
            return             
        #check if there is no such user in the config DB
        if self.__userConfig.userExist(login):
            #showerror(self.__localization.getWord('duplicate_login'), 
            #          self.__localization.getWord('user_exist')) 
            md.showError(self.__view, 
                title = self.__localization.getWord('duplicate_login'),
                text = self.__localization.getWord('user_exist'), 
                buttonsText=[self.__localization.getWord('ok')])
            return 
        
        #check length of the password               
        if len(password) == 0:
            #showerror(self.__localization.getWord('invalid_password'),
            #          self.__localization.getWord('password_at_least_1_symbol'))
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_password'),
                text = self.__localization.getWord('password_at_least_1_symbol'), 
                buttonsText=[self.__localization.getWord('ok')])
            return
        
        #check if the password contains correct symbols            
        if not self.__userConfig.checkNewPassword(password):
#             showerror(self.__localization.getWord('invalid_symbols'), 
#                       "{}. \n{} {}".format(
#                                            self.__localization.getWord('password_contains_invalid_symbols'),
#                                            self.__localization.getWord('should_be_only'),
#                                            self.__localization.getWord('password_valid_symbols')
#                                            )) 
            md.showError(self.__view, 
                title = self.__localization.getWord('invalid_symbols'),
                text = "{} {}. \n{} {}".format(
                                               self.__localization.getWord('password'),
                                               self.__localization.getWord('contains_invalid_value'),
                                               self.__localization.getWord('should_be_only'),
                                               self.__localization.getWord('password_valid_symbols')
                                               ), 
                buttonsText=[self.__localization.getWord('ok')])           
            return
                                                    
        #check if password and confirm match
        if password != confirmPassword:
            #showerror(self.__localization.getWord('mismatch'),
            #           self.__localization.getWord('password_confirm_mismatch') )
            md.showError(self.__view, 
                title = self.__localization.getWord('mismatch'),
                text = self.__localization.getWord('password_confirm_mismatch'), 
                buttonsText=[self.__localization.getWord('ok')])
            return
        
                  
        #add new user
        try:
            self.__userConfig.addNewUser(login, password)
        except Exceptions.NotUniqueValueException:
            #showerror(self.__localization.getWord('duplicate_login'),
            #           self.__localization.getWord('user_exist')) 
            md.showError(self.__view, 
                title = self.__localization.getWord('duplicate_login'),
                text = self.__localization.getWord('user_exist'), 
                buttonsText=[self.__localization.getWord('ok')])
            return 
        
        #send signal
        self.__notifier.sendSignal(Signal.NEW_USER_REGISTER_OK, (login, password))
        #close register dialog
        self.__view.destroy()


    def loginEntryChanged(self):
        entry = self.__view.getLoginEntry()
        entryText = entry.get()
        infoLabel = self.__view.getLoginInfoLabel()
        
        if len(entryText) == 0:
            self.__setEntryIfEmpty(entry , infoLabel)
            return             
        
        #if the login contains  not valid symbols
        if not self.__userConfig.checkNewLogin(entryText):
            entry.config(background = Colors.INVALID_VALUE)
            infoLabel.config(text=self.__localization.getWord('wrong_value')) 
            return          
        
        #check if entered user name already exist
        if self.__userConfig.userExist(entryText):
            entry.config(background = Colors.INVALID_VALUE)
            infoLabel.config(text=self.__localization.getWord('taken'))
            return
        
        #if all checks are ok
        entry.config(background = Colors.VALID_VALUE)
        infoLabel.config(text=self.__localization.getWord('free'))
        
            

    def passwordEntryChanged(self):
        entry = self.__view.getPasswordEntry()
        entryText = entry.get()
        infoLabel = self.__view.getPasswordInfoLabel()
        
        self.__recheckConfirmPasswordEntry()
        
        if len(entryText) == 0:
            self.__setEntryIfEmpty(entry, infoLabel)
            return 
        
        #if the password contains  not valid symbols
        if not self.__userConfig.checkNewPassword(entryText):
            entry.config(background = Colors.INVALID_VALUE)
            infoLabel.config(text=self.__localization.getWord('wrong_value')) 
            return
        
        #if checks are ok define password strength
        passStrength = self.__userConfig.defineStrengthOfPassword(entryText)
        if passStrength == PasswordStrength.WEAK:
            entry.config(background = Colors.WEAK_STRENGTH_PASSWORD)
            infoLabel.config(text=self.__localization.getWord('weak'))
        elif passStrength == PasswordStrength.MIDDLE:
            entry.config(background = Colors.MIDDLE_STRENGTH_PASSWORD)
            infoLabel.config(text=self.__localization.getWord('middle'))
        else: 
            entry.config(background = Colors.STRONG__STRENGTH_PASSWORD)
            infoLabel.config(text=self.__localization.getWord('strong'))               
                             
    

    def passwordConfirmEntryChanged(self):
        self.__recheckConfirmPasswordEntry()
        
    
    def __setEntryIfEmpty(self, ent, label):
        ent.config(background = 'white')
        label.config(text='')       
        
        
    def __recheckConfirmPasswordEntry(self):
        entry = self.__view.getConfirmPasswordEntry()
        entryText = entry.get()
        password = self.__view.getPasswordEntry().get()        
        infoLabel = self.__view.getConfirmPasswordInfoLabel()
        
        #if none text entered
        if len(entryText) == 0:
            self.__setEntryIfEmpty(entry , infoLabel)
            return
        
        #check match with the password 
        if entryText == password:
            entry.config(background = Colors.VALID_VALUE)
            infoLabel.config(text=self.__localization.getWord('ok'))              
            return
        
        #if not match 
        entry.config(background = Colors.INVALID_VALUE)
        infoLabel.config(text=self.__localization.getWord('no_match')) 
        