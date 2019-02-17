'''
Start App
'''

import UsConfig as Config
from Common.Utilities import centerRoot

  
if __name__ == '__main__':
    root = Config.ASSEMBLER.assemble("MainApp")          
    root.title("EasyPass")
    root.iconbitmap(default=r'D:/logo.ico') 
    centerRoot(root)
    root.mainloop()
    
