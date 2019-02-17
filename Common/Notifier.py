'''
Classes to implement Notify pattern to send signals
'''

from abc import ABCMeta, abstractmethod


class Observer(object):
    """
    Abstract Observer
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, signal, data):
        """
        Getting a new data
        @type  signal: Settings.Constants.Signal
        @param signal: type of signal
        @type  data: 
        @param data: provided data         
        """
        pass

#====================================================================================================

class Observable():
    """
    Abstract observable
    """

    def __init__(self):
        """
        Constructor
        """
        self.observers = []     # init Observers

    def register(self, observer):
        """
        Register a new observer
        """
        self.observers.append(observer)
        
    def unregister(self, observer):
        """
        Unregister an observer
        """
        self.observers.remove(observer)      

    def notifyObservers(self, signal, data):
        """
        Notify all the registered observers
        @type  signal: Settings.Constants.Signal
        @param signal: type of signal
        @type  data: 
        @param data: provided data              
        """
        for observer in self.observers:
            observer.update(signal, data)
                       

#====================================================================================================


def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


#@singleton
class Notifier(Observable):
    """
    Class notifier of objects expecting signals
    """ 
    def __init__(self):
        Observable.__init__(self)
    
    
    def sendSignal(self, singal, data):
        """
        Send signal and data to all registered observers
        @type  signal: Settings.Constants.Signal
        @param signal: type of signal
        @type  data: 
        @param data: provided data          
        """
        self.notifyObservers(singal, data)    
        
 





        
       