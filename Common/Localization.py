'''
Localization class for support of many languages
'''

import xml.etree.ElementTree
import Common.Constants.Language as Language
import UsConfig as Config
import os

class Localization(object):
    def __init__(self, language):
        self.__data = {}
        self.__currLanguage = language
        self.__loadLanguage(self.__currLanguage)   

       
    def setLanguage(self, language):
        self.__currLanguage = language
        self.__loadLanguage(language)    
    
    
    def getWord(self, key):
        if key in self.__data:
            return self.__data[key]
        else:
            return Language.DEFAULT_TEXT_IF_KEY_NOT_FOUND 
    
            
    def __loadLanguage(self, language):
        self.__data = {}
        lzFile = self.__getFileByLanguage(language)
        root = xml.etree.ElementTree.parse(lzFile).getroot()
        for atype in root.findall('word'):
            #print(atype.get('key') , atype.get('val').encode('utf8')) 
            self.__data[str(atype.get('key'))] = str(atype.get('val').encode('utf8'))        
 
        
    def __getFileByLanguage(self, language):
        if language == Language.EN:
            return os.path.join(Config.LOCALIZATION_FILES_PATH, 'l_EN.xml' )#Config.LOCALIZATION_FILES_PATH + 'l_EN.xml'
        elif language == Language.RU:
            return os.path.join(Config.LOCALIZATION_FILES_PATH, 'l_RU.xml' )#Config.LOCALIZATION_FILES_PATH + 'l_RU.xml'
        elif language == Language.UA:
            return os.path.join(Config.LOCALIZATION_FILES_PATH, 'l_UA.xml' )#Config.LOCALIZATION_FILES_PATH + 'l_UA.xml'
        elif language == Language.DE:
            return os.path.join(Config.LOCALIZATION_FILES_PATH, 'l_DE.xml' )#Config.LOCALIZATION_FILES_PATH + 'l_DE.xml' 
        #default language - English
        else:                            
            return os.path.join(Config.LOCALIZATION_FILES_PATH, 'l_EN.xml' )#Config.LOCALIZATION_FILES_PATH + 'l_EN.xml'

    
    
l = Localization(1)

w1 = l.getWord('app_name')
print w1
    
