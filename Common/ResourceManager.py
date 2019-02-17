'''
Manager of graphic resources
'''

import xml.etree.ElementTree
import os

import UsConfig as Config
import DataModel.Exceptions as Exceptions

class ResourceManager(object):
    '''Manager of graphic resources'''
    def __init__(self):
        self.__data = {}
        self.__loadResourceData()   
  
    
    def getResource(self, key):
        if key in self.__data:
            return self.__data[key]
        else:
            raise Exceptions.WrongValueException("No value", "No value for key {} found".format(key)) 
    
            
    def __loadResourceData(self):
        print os.getcwd()
        self.__data = {}
        root = xml.etree.ElementTree.parse(Config.RESOURCES_CONFIG_PATH).getroot()
        for atype in root.findall('res'):
            #print(atype.get('key') , atype.get('val').encode('utf8')) 
            self.__data[str(atype.get('key'))] = str(atype.get('val').encode('utf8'))        
 
        

if __name__ == '__main__':
    r = ResourceManager()
    a = r.getResource('app_name')
    print a
