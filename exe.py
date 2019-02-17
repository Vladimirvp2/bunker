from distutils.core import setup
import py2exe
import os,  shutil


class FileGetter():
    buildPath = "Build"
    fouldersToRemove = ['build', 'dist']
    #relatively to the root dir
    ignoreFiles = ['exe.py', 'test.py']
    ignoreFolders = ['Tests']
    #without relation to current directory
    ignoreRelativeFiles = ['__init__.py'] 
    includeSourceExt = [".py"]
    includeDataExt = [".gif", ".xml"]
    #packages are added to source files
    packages = ["aglyph"]
    
    def __init__(self):
        self.cwd = os.getcwd()
        
        
    def clean(self):
        for folder in self.fouldersToRemove:
            folderFullPath = os.path.join(self.cwd, folder)
            if os.path.isdir(folderFullPath):
                shutil.rmtree(folderFullPath)
        #remove previous build        
        buildFullPath = os.path.join(self.cwd, self.buildPath)
        if os.path.isdir(buildFullPath):
            shutil.rmtree(buildFullPath)
    
    
    def getSourceFiles(self, path):
        res = []
        for root, dirs, files in os.walk(path):
            for file in files:
                fullPath = os.path.join(root, file)
                relPath = os.path.relpath(fullPath, path)
                relPathList = self.__splitall(relPath)
                #check if the folder should be ignored
                if not self.__checkSourceFolderInclude(relPathList):
                    continue
                if self.__checkSourceFileInclude(relPath):
                    relPathWithoutExt = os.path.splitext(relPath)[0]
                    #fullPath = os.path.relpath(fullPath, cwd)
                    relPathWithoutExtList = self.__splitall(relPathWithoutExt)
                    dotFile = self.__joinByDot(relPathWithoutExtList)
                    res.append(dotFile)
        return res
    
    
    def getPackages(self):
        return self.packages
    
    
    def getDataFilesOfRelativeDir(self, relPath):
        res = []
        fullPath = os.path.join(self.cwd, relPath)
        dirs = os.listdir(fullPath)
        for file in os.listdir(fullPath):
            fullFile = os.path.join(fullPath, file)
            relFile = os.path.relpath(fullFile, self.cwd)
            if os.path.isfile(fullFile) and self.__checkDataFileInclude(relFile): 
                #relFile = os.path.relpath(fullFile, self.cwd)
                res.append(relFile)
                
        return res
                
    
    def __getDataFilesAll(self, path):
        res = []
        for root, dirs, files in os.walk(path):
            for file in files:
                fullPath = os.path.join(root, file)
                relPath = os.path.relpath(fullPath, path)
                if self.__checkDataFileInclude(relPath):
                    res.append(relPath)
        return res    
    
    
    
    def __splitall(self, path):
        allparts = []
        while 1:
            parts = os.path.split(path)
            if parts[0] == path:  # sentinel for absolute paths
                allparts.insert(0, parts[0])
                break
            elif parts[1] == path: # sentinel for relative paths
                allparts.insert(0, parts[1])
                break
            else:
                path = parts[0]
                allparts.insert(0, parts[1])
        return allparts 
    
    
    def __joinByDot(self, pathList):
        res = ""
        for part in pathList:
            if res == "":   #for first component
                res = part
            else:
                res = res + "." + part
            
        return res
    
    
    def __checkSourceFileInclude(self, file):
        #check if the file is in the ignore list
        if file in self.ignoreFiles:
            return False
        
        for ignore in self.ignoreRelativeFiles:
            if ignore in file:
                return False
            
        #check if the file has the allowed extension
        filename, file_extension = os.path.splitext(file)
        if file_extension not in self.includeSourceExt:
            return False
        
        return True
    
    
    def __checkDataFileInclude(self, file):
        #check if the file is in the ignore list
        if file in self.ignoreFiles:
            return False
        
        #check if the file has the allowed extension
        filename, file_extension = os.path.splitext(file)
        if file_extension not in self.includeDataExt:
            return False
        
        return True
    
    
    def __checkSourceFolderInclude(self, dirs):
        if len(dirs) > 0 and dirs[0] in self.ignoreFolders:
            return False
        
        return True



g = FileGetter()
g.clean()

#get list of source files and packages
source =  g.getSourceFiles(os.getcwd())
packages = g.getPackages()
includes = source + packages



#get list of data files
dataFiles = [("Resources", g.getDataFilesOfRelativeDir("Resources")), 
                  ("Resources/Localization", g.getDataFilesOfRelativeDir("Resources/Localization")),
                  ("Resources/Icons", g.getDataFilesOfRelativeDir("Resources/Icons")),
                   g.getDataFilesOfRelativeDir("")]
   
setup(
      windows=['App.py'],
      options={"py2exe": {"includes": includes ,  'dist_dir': FileGetter.buildPath}},
      #options={"py2exe": {"includes":["sip","qad","dialog","sys","PyQt4"]}},
      data_files=[("Resources", g.getDataFilesOfRelativeDir("Resources")), 
                   ("Resources/Localization", g.getDataFilesOfRelativeDir("Resources/Localization")),
                   ("Resources/Icons", g.getDataFilesOfRelativeDir("Resources/Icons")),
                   ("", g.getDataFilesOfRelativeDir(""))
                   ]
      )



 
# setup(
#       windows=['App.py'],
#       options={"py2exe": {"includes":["aglyph", 'Common.Localization', 'Common.ResourceManager', 'Common.Notifier', 'Common.Utilities',
#                                       'Common.Crypt', 'Common.Constants.Colors', 'Common.Constants.DatabaseMerge',
#                                       'Common.Constants.DataField', 'Common.Constants.DBObjectType', 
#                                       'Common.Constants.DBStatus', 'Common.Constants.Default', 
#                                       'Common.Constants.EntryStatus', 'Common.Constants.PasswordStrength',
#                                       'Common.Constants.Singal', 'Common.Constants.Table', 
#                                       'Common.Constants.LabelType',
#                                        
#                                         
#                                        'GUI.AppMainWin',
#                                        'GUI.Dialogs.Login',
#                                         
#                                        'Controllers.MainWinController',
#                                        'Controllers.LoginController',
#                                         
#                                        'DataModel.DataBaseManager',
#                                        'DataModel.UserConfigManager',
#                                         
#                                        'GUI.MessageDialog'
#                                         
#                                        ]}},
#       #options={"py2exe": {"includes":["sip","qad","dialog","sys","PyQt4"]}},
#       data_files=[("Resources",["Resources/resourceConfig.xml"]), 
#                   ("Resources/Localization",["Resources/Localization/l_EN.xml"]), 'app_context.xml']
#       #             ["bm/large.gif", "bm/small.gif"]),
#       #            ("fonts",
#        #            )]
#       )