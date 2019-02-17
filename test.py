from distutils.core import setup
import py2exe
#from _functools import partial
import os,  shutil




class FileGetter():
    fouldersToRemove = ['build', 'dist']
    #relatively to the root dir
    ignoreFiles = ['exe.py', 'test.py'] 
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
    
    
    def getSourceFiles(self, path):
        res = []
        for root, dirs, files in os.walk(path):
            for file in files:
                fullPath = os.path.join(root, file)
                relPath = os.path.relpath(fullPath, path)
                #if file.endswith(".py") and file not in ignoreFilesFullPath:
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
    
    





g = FileGetter()
g.clean()
#res = g.getDataFilesOfRelativeDir("")
res = g.getSourceFiles(os.getcwd())
a = g.getPackages()
res = res + a
#res = g.getDataFilesOfRelativeDir("Resources/Icons")
for r in res:
    print r


        
        
            
