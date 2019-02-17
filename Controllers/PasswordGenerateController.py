"""Classes of controller for password generation dialog"""

from Common.Utilities import*
from GUI.Dialogs.Register import Register
import UsConfig as Config
import Common.Constants.Singal as Signal
import Common.Constants.DataField as DataField
from DataModel.Exceptions import*
import logging
import Services.PasswordGenerator as pswg
from GUI.MessageDialog import showError 
from Common.Notifier import Observer


from abc import ABCMeta, abstractmethod


class PasswordGenerateControllerI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def addView(self, view):
        "Add view to the controller"
        pass
       
    @abstractmethod
    def generatePasswordPress(self):
        pass
    
    @abstractmethod
    def cancelPress(self):
        pass
    
    @abstractmethod
    def getSelectedPasswordPress(self):
        pass
    
    
        
    
class PasswordGenerateController(PasswordGenerateControllerI):
    '''
    Controller for the add new category dialog
    '''
    def __init__(self, passGenService, notifier, localization):
        self.__passGenService = passGenService 
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        self.__notifier.register(self)
        
        
    def addView(self, view):
        self.__view = view
        
        

    def generatePasswordPress(self):
        #if entropy collected clear it
        self.__passGenService.clearEntropy()
        
        self.__view.clearPasswordPreview()
        data = pswg.PasswordSpecification()
        #initialize password generator with specified parameters
        passwordLength = self.__view.getPasswordLength()
        data.setPasswordLength(passwordLength)
         
        #general tab
        if self.__view.getUpperCase():
            data.setUpperCase(True)
        if self.__view.getLowerCase():
            data.setLowerCase(True)
        if self.__view.getDigit():
            data.setDigit(True)
        if self.__view.getMinus():
            data.setMinus(True)
        if self.__view.getSpace():
            data.setSpace(True)
        if self.__view.getUnderline():
            data.setUnderline(True)
        if self.__view.getDot():
            data.setDot(True)
             
        additChars = self.__view.getAdditionalSymbols()
        data.setAdditionalSymbols(additChars) 
 
        #advanced tab
        if self.__view.getEachCaracterAtMostOne():
            data.setEachCaracterAtMostOne(True)
        if self.__view.getExcludeLookLikeSymbols():
            data.setExcludeLookLikeSymbols(True)
             
        excludeChars = self.__view.getExcludedSymbols()
        data.setExcludedSymbols(excludeChars)
             
        #generate passwords
        psws = []
        try:
            p = self.__passGenService.generatePasswordRange(data, 1)
            #if collect entropy show dialog
            if self.__view.getCollectEntropy():
                dialog = Config.ASSEMBLER.assemble("CollectEntropyView")
                centerTopLevel(dialog)
                setWaitForClose(dialog)
                
            psws = self.__passGenService.generatePasswordRange(data, Config.AUTO_PASSWORD_GENERATION_SAMPLE_NUMBER)
        except pswg.ZeroPasswordException:
            showError(self.__view, title = 'Error', text="Password length can't be 0!", buttonsText=['Ok'])
            return
        except pswg.FewSymbolsProvidedException:
            showError(self.__view, title = 'Error', text="Not enough symbols provided for password generation!", buttonsText=['Ok'])
            return
            
        #insert them into preview
        for psw in psws:
            self.__view.insertIntoPasswordPreview(psw)
             
        #open preview tab
        self.__view.openPreviewTab()
    

    def getSelectedPasswordPress(self):
        sel = self.__view.getSelectedPassword()
        #if a few passwords selected show error    
        for c in sel:
            if c == '\n':
                showError(self.__view, title = 'Error', text='Select only one password!', buttonsText=['Ok'])
                return
             
        #if not the hole password selected but only part show error
        passwordLength = self.__view.getPasswordLength()
        if len(sel) < passwordLength:
            showError(self.__view, title = 'Error', text='Select the hole password!', buttonsText=['Ok'])
            return            
        
        logging.debug("Password selected: {}".format(sel))         
        #send signal and close dialog
        self.__view.destroy()
        self.__notifier.unregister(self)
        
        
    def cancelPress(self):
        self.__view.destroy()
        self.__notifier.unregister(self)
        
        
    def update(self, signal, data=None):
        if signal == Signal.ENTROPY_COLLECTED:
            #set entropy
            for e in data:
                self.__passGenService.addEntropy(e[0], e[1]) 
                
        elif signal == Signal.ENTROPY_COLLECT_CANCEL:
            self.__passGenService.clearEntropy()
        
                  
        
 
 
class CollectEntropyControllerI(object):
    """
    Login view interface 
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def addView(self, view):
        "Add view to the controller"
        pass
        
    @abstractmethod
    def cancelPress(self):
        pass
    
    @abstractmethod
    def okPress(self):
        pass
    
    @abstractmethod    
    def mouseClick(self, x, y):
        """Called if the entropy image clicked"""
        pass 
 
        
        
        
class CollectEntropyController(CollectEntropyControllerI):
    '''
    Controller for the add new category dialog
    '''
    
    PERCENTAGE_MAX = 100
    
    def __init__(self, notifier, localization): 
        self.__notifier = notifier
        self.__localization = localization
        self.__view = None
        self.__entropyValues = []
        self.__addProcentage = self.PERCENTAGE_MAX / Config.AUTO_PASSWORD_GENERATION_COLLECT_ENTROPY_NUMBER
        
        
    def addView(self, view):
        self.__view = view
        
        
    def cancelPress(self):
        self.__notifier.sendSignal(Signal.ENTROPY_COLLECT_CANCEL, None)
        self.__view.destroy()
    

    def okPress(self):
        self.__ready()
    
   
    def mouseClick(self, x, y):
        progress = self.__view.getProgress()   
        if progress < self.PERCENTAGE_MAX:
            self.__entropyValues.append((x, y))
            progress+=self.__addProcentage
            self.__view.setProgress(progress) 
        else:
            self.__ready()
        
        
    def __ready(self):
        self.__view.destroy()
        self.__notifier.sendSignal(Signal.ENTROPY_COLLECTED, self.__entropyValues)
        for a in self.__entropyValues:
            print a
        
        
        
        
        
   
        
        
   
