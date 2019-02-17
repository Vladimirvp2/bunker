'''
Start App 
'''

import Tkinter as tk
from tkMessageBox import *
import ttk, tkFont, logging, os
import UsConfig as Config

from GUI.Dialogs.Login import Login
import Common.Constants.Singal as Signal
from Common.Notifier import Observer
from Common.Constants import DBStatus

from Common.Utilities import*

from aglyph.assembler import Assembler
from aglyph.context import XMLContext
from abc import ABCMeta, abstractmethod

from GUI.Dialogs.AddRecord import AddRecord


class MainWinI(object):
    """
    Interface for the main window view 
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod    
    def getCategoryPanel(self):
        "get the reference of the panel containing databases and categories"
        pass
        
    @abstractmethod    
    def getRecordPanel(self):
        "get the reference of the panel containing records"
        pass
    
    @abstractmethod       
    def getTopMenu(self):
        "get the reference of the top Menu"
        pass
    
    @abstractmethod      
    def getToolbar(self):
        "get the reference of the toolbar panel"
        pass 

    
    
class MainWin(tk.Tk, MainWinI):
    """
    Main GUI class of the app 
    """
    def __init__(self, controller, notifier, localization):
        tk.Tk.__init__(self)
        self.__controller = controller
        self.__notifier = notifier
        self.__localization = localization
        self.__controller.addView(self)
        self.__componentsRef = {}
        self.init()
         
         
    def init(self):
        #add menu
        self.addMenu()
        #add data panels
        self.addDataPanels()
        #add bottom tool bar
        self.addToolBar()
         
        self.withdraw()
        login = Config.ASSEMBLER.assemble("LoginView")
        #login = Config.ASSEMBLER.assemble("AddNewDBView")
        centerTopLevel(login)
        #centerTopLevel(Login(self, self))
              
         
    def LoginOk(self):
        self.deiconify()
        print "Login OK!"
         
         
    def addMenu(self):
        self.mainMenu = MenuMain(self, self.__notifier, self.__localization)
        self.__componentsRef['top_menu'] = self.mainMenu
                
         
    def addDataPanels(self):
        """Add two data panels - left for data bases and categories; and right - for the records"""
                 
        #add draggable
        self.panes = tk.PanedWindow(self)
        self.panes.pack(fill="both", expand="yes")
        self.panes.configure(bg="#383838")
     
        #add category panel(left)
        self.categoryPanel = CategoryPanel(self.panes, self.__notifier, path=r"D:/Temp/Foto/")
        self.categoryPanel.pack(expand=YES, fill=tk.BOTH)
        self.panes.add(self.categoryPanel)
         
        #add record panel(right)
        self.recordPanel = RecordPanel(self.panes, self.__notifier)
        self.recordPanel.pack(expand=YES, fill=tk.X)
        self.panes.add(self.recordPanel) 
         
        self.__componentsRef['category_panel'] = self.categoryPanel
        self.__componentsRef['record_panel'] = self.recordPanel  
         
    def addToolBar(self):
        button = ttk.Button(self, text="Save")
        button.pack(side=tk.LEFT, padx=2, pady=2)    
        button1 = ttk.Button(self, text="Save1")
        button1.pack(side=tk.LEFT, padx=2, pady=2) 
         
        self.__componentsRef['toolbar'] = None
         
         
    def getCategoryPanel(self):
        return self.__componentsRef['category_panel']
            
    def getRecordPanel(self):
        return self.__componentsRef['record_panel']
     
    def getTopMenu(self):
        return self.__componentsRef['top_menu'] 
           
    def getToolbar(self):
        return self.__componentsRef['toolbar']
    
    
    
    
class CategoryPanel(tk.Frame):
    """Category data panel(from the left)"""
    def __init__(self, parent, notifier, path):
        tk.Frame.__init__(self, parent)
        self.tree = ttk.Treeview(self)
        ysb = AutoScrollbar(self, orient='vertical', command=self.tree.yview)
        #xsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscroll=ysb.set)
        self.tree.heading('#0', text='Databases', anchor='w')
        
        #ttk.Style().configure("Treeview", background="white",                            
        #    foreground="black", fieldbackground="red", selectforeground='green')   
 
        abspath = os.path.abspath(path)
        #root_node = self.tree.insert('', 'end', text=abspath, open=True)
        #self.process_directory(root_node, abspath)
         
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)      
        self.tree.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        ysb.grid(row=0,column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        #xsb.grid(row=1,column=0, sticky=tk.E+tk.W)
 
        #self.tree.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        #ysb.pack(side=tk.RIGHT, fill=tk.Y, anchor=tk.E)
         
        #Add context menu
        self.tree.bind("<ButtonRelease-3>", lambda event : notifier.sendSignal(Signal.CATEGORY_RIGHT_CLICK, event))
                 
        self.tree.bind("<Double-Button-1>", lambda event : notifier.sendSignal(Signal.CATEGORY_DOUBLE_CLICK, event))
        self.tree.bind("<ButtonRelease-1>", lambda event : notifier.sendSignal(Signal.CATEGORY_SINGLE_CLICK, event))
        self.tree.bind("<Return>", lambda event : notifier.sendSignal(Signal.CATEGORY_DOUBLE_CLICK, event))
         
        #self.tree.bind("<Button-1>", lambda event : notifier.sendSignal(Signal.CATEGORY_SINGLE_CLICK, event))
 
    def process_directory(self, parent, path):
 
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)



class RecordPanel(tk.Frame):
    """Record data panel(from the right)"""
    def __init__(self, parent, notifier):

        tk.Frame.__init__(self, parent)
        self.tree = ttk.Treeview(self)

  
        #ttk.Style().configure("Treeview", background="#EEEEEE",                            
        #    foreground="black", fieldbackground="red", selectforeground='green')              
    
        i = r'D:/uAQrp.gif'
        self.root_pic3 = tk.PhotoImage(file=i)
        #tree = ttk.Treeview(master, height="10")
        self.tree["columns"]=("one","two", "three", "four")
        self.tree.column("one", width=100 )
        self.tree.column("two", width=150)
        self.tree.column("three", width=100 )
        self.tree.column("four", width=150)        
        self.tree.heading('#0', text='Site', anchor='w')
        self.tree.heading('#0', text='Site', anchor='w')
        #self.tree.heading("one", image=self.root_pic3, text="Username", anchor='e')
        self.tree.heading("one", text="Username", anchor='w')
        self.tree.heading("two", text="Email", anchor='w')
        self.tree.heading("three", text="Password", anchor='w')
        self.tree.heading("four", text="Comments", anchor='w')
        self.tree['height'] = 20
        
        style = ttk.Style()
        helv36 = tkFont.Font(family='Helvetica',
                             size=8, weight='bold') 
        style.configure("Treeview.Heading", foreground='black', font=helv36, anchor='w')

        #im = tk.PhotoImage(r'D:/uAQrp.gif')        
        #self.tree.insert("" , 0,  '0',  text="Line", values=("2A","2b", "3f", "5"), image = im)
        i = r'D:/uAQrp.gif'
        self.root_pic = tk.PhotoImage(file=i)
        #root_node = self.tree.insert('', 'end', text='  Work Folder', open=True, image=self.root_pic)
        #root_node2 = self.tree.insert('', 'end', text='  Work Folder2', image=self.root_pic)
    
        self.tree.bind("<ButtonRelease-1>", lambda event : notifier.sendSignal(Signal.RECORD_CLICK, event))
    
    
        helv36 = tkFont.Font(family='Helvetica',
        size=8, weight='bold')     
    
    

        self.tree.bind("<Double-1>", self.on_double_click)  
        #Add context menu
        self.tree.bind("<ButtonRelease-3>", lambda event : notifier.sendSignal(Signal.RECORD_RIGHT_CLICK, event))                 
        #add scrollbar y
        ysb = AutoScrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set) 
        
        tk.Grid.rowconfigure(self, 0, weight=1)
        tk.Grid.columnconfigure(self, 0, weight=1)
        self.tree.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        ysb.grid(row=0,column=1, sticky=tk.N+tk.S+tk.E+tk.W)        
        #ysb.pack(side=tk.RIGHT, fill=tk.Y, anchor=tk.E)
        
        #self.tree.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)   
        
        
    def on_double_click(self, event):
        print "on_double_click"
       
        
               
        
class MenuMain(tk.Menu, Observer):
    """Top menu for the main app window"""
    def __init__(self, parent, notifier, localization):
        tk.Menu.__init__(self)
        self.__parent = parent
        self.__notifier = notifier
        self.__localization = localization
        #references for images
        self.__images = {}
        #references for menus(to change them via signals) 
        self.__menuRef = {}
        self.__resourceManager = Config.ASSEMBLER.assemble("ResourceManager")
        self.__createMenu()
        self.__notifier.register(self)
       
    def __createMenu(self):
        top = tk.Menu(self.__parent)                  
        self.__parent.config(menu=top) 
        #database menu            
        dbMenu = tk.Menu(top, tearoff=False)
        self.__menuRef['database'] = dbMenu
        dbMenu.add_command(label=self.__localization.getWord('create_db'), 
                        command=lambda: self.__notifier.sendSignal(Signal.DB_ADD_NEW_SHOW_DIALOG, None),
                        underline=0,
                        image=self.__getImage('add_new_db_image'), 
                        compound = LEFT)
                  
        dbMenu.add_command(label=self.__localization.getWord('import_db'),
                        command=lambda: self.__notifier.sendSignal(Signal.DB_ADD_EXISTING_SHOW_DIALOG, None),
                        underline=0,
                        image=self.__getImage('add_existing_db_image'), 
                        compound = LEFT)
          
        dbMenu.add_command(label=self.__localization.getWord('connect_db'),
                        command=lambda: self.__notifier.sendSignal(Signal.DB_CONNECT, None),
                        underline=0,
                        image=self.__getImage('connected_image'), 
                        compound = LEFT,
                        state="disabled")
          
        dbMenu.add_command(label=self.__localization.getWord('disconnect_db'),
                        command=lambda: self.__notifier.sendSignal(Signal.DB_DISCONNECT, None),
                        underline=0,
                        image=self.__getImage('disconnected_image'), 
                        compound = LEFT,
                        state="disabled")
          
        dbMenu.add_command(label=self.__localization.getWord('remove_db_from_config'),
                        command=lambda: self.__notifier.sendSignal(Signal.DB_REMOVE_FROM_CONFIG, None),
                        state="disabled")
          
        dbMenu.add_command(label=self.__localization.getWord('remove_db_from_filesystem'),
                        command=lambda: self.__notifier.sendSignal(Signal.DB_REMOVE_FROM_FILE_SYSTEM, None),
                        underline=0, image=self.__getImage('remove_db_from_config_image'),
                        compound = LEFT,
                        state="disabled")
          
        dbMenu.add_command(label=self.__localization.getWord('save'),
                        command=lambda: self.__notifier.sendSignal(Signal.SAVE_CURR_DB, None),
                        image=self.__getImage('save_image'),
                        underline=0,
                        compound = LEFT,
                        state="disabled")
          
        dbMenu.add_command(label=self.__localization.getWord('quit'),
                        command=lambda: self.__notifier.sendSignal(Signal.APP_QUIT, 1),
                        underline=0)
          
        top.add_cascade(label=self.__localization.getWord('main_menu_db'),
                        menu=dbMenu,
                        underline=0)
        
        #Operations menu
        operationsMenu = tk.Menu(top, tearoff=False)
        #Category sub menu
        categorySubmenu = tk.Menu(operationsMenu, tearoff=False)
        categorySubmenu.add_command(label=self.__localization.getWord('add'),
                                    command=lambda : self.__notifier.sendSignal(Signal.SHOW_ADD_NEW_CATEGORY_DIALOG, None),
                                    underline=0,
                                    image=self.__getImage('add'),
                                    compound = LEFT,
                                    state="disabled")    
              
        categorySubmenu.add_command(label=self.__localization.getWord('edit'),
                                    command=lambda : self.__notifier.sendSignal(Signal.SHOW_EDIT_CATEGORY_DIALOG, None), 
                                    underline=0,
                                    image=self.__getImage('edit'),
                                    compound = LEFT,
                                    state="disabled")
          
        categorySubmenu.add_command(label=self.__localization.getWord('delete'), 
                                    command=lambda : self.__notifier.sendSignal(Signal.REMOVE_CATEGORY, None), 
                                    underline=0,
                                    image=self.__getImage('delete'),
                                    compound = LEFT,
                                    state="disabled")
        # Record sub menu 
        recordSubmenu = tk.Menu(operationsMenu, tearoff=False)
        recordSubmenu.add_command(label=self.__localization.getWord('add'), 
                                command=lambda : self.__notifier.sendSignal(Signal.SHOW_ADD_NEW_RECORD_DIALOG, None), 
                                underline=0,
                                image=self.__getImage('add'),
                                compound = LEFT,
                                state="disabled")    
              
        recordSubmenu.add_command(label=self.__localization.getWord('edit'), 
                                command=lambda : self.__notifier.sendSignal(Signal.SHOW_EDIT_RECORD_DIALOG, None), 
                                underline=0,
                                image=self.__getImage('edit'),
                                compound = LEFT,
                                state="disabled")
          
        recordSubmenu.add_command(label=self.__localization.getWord('delete'), 
                                command=lambda : self.__notifier.sendSignal(Signal.REMOVE_RECORD, None), 
                                underline=0,
                                image=self.__getImage('delete'),
                                compound = LEFT,
                                state="disabled")                
          
        operationsMenu.add_cascade(label=self.__localization.getWord('main_menu_caregory'), menu=categorySubmenu, underline=0)
        operationsMenu.add_cascade(label=self.__localization.getWord('main_menu_record'), menu=recordSubmenu, underline=0)  
        top.add_cascade(label=self.__localization.getWord('main_menu_operations'), menu=operationsMenu, underline=0)  
          
          
        self.__menuRef['category'] = categorySubmenu
        self.__menuRef['record'] = recordSubmenu
        
        #settings menu
        settingsMenu = tk.Menu(top, tearoff=False)               
        settingsMenu.add_command(label=self.__localization.getWord('user_settings'),
                        command=lambda: self.__notifier.sendSignal(Signal.SHOW_SETTINGS_DIALOG, None),
                        underline=0)        
  
        top.add_cascade(label=self.__localization.getWord('main_menu_settings'),
                        menu=settingsMenu,
                        underline=0)
         
        #info menu
        infoMenu = tk.Menu(top, tearoff=False)               
        infoMenu.add_command(label=self.__localization.getWord('info'),
                        command=lambda: self.__notifier.sendSignal(Signal.SHOW_INFO_DIALOG, None),
                        underline=0,
                        image=self.__getImage('info_image'),
                        compound = LEFT)
         
        infoMenu.add_command(label=self.__localization.getWord('manual'),
                        command=lambda: self.__notifier.sendSignal(Signal.SHOW_MANUAL, None),
                        underline=0)         
  
        top.add_cascade(label=self.__localization.getWord('main_menu_info'),
                        menu=infoMenu,
                        underline=0)         
        
        
    def update(self, signal, data=None):
        """
        Handler. Called if a signal is fired
        """
        #try:
        if signal == Signal.DB_SELECTED_CHANGED:
            logging.info("DB changed: {}".format(data))
            dbMenu = self.__menuRef['database']
            categoryMenu = self.__menuRef['category']
            recordMenu = self.__menuRef['record']
            if not data: 
                #data base menu
                dbMenu.entryconfig(self.__localization.getWord("connect_db"), state="disabled")
                dbMenu.entryconfig(self.__localization.getWord("disconnect_db"), state="disabled")
                dbMenu.entryconfig(self.__localization.getWord("remove_db_from_config"), state="disabled")
                dbMenu.entryconfig(self.__localization.getWord("remove_db_from_filesystem"), state="disabled")
                dbMenu.entryconfig(self.__localization.getWord("save"), state="disabled")
                
                #operations menu
                categoryMenu.entryconfig(self.__localization.getWord('add'), state="disabled")
                categoryMenu.entryconfig(self.__localization.getWord('edit'), state="disabled")
                categoryMenu.entryconfig(self.__localization.getWord('delete'), state="disabled")
                
                recordMenu.entryconfig(self.__localization.getWord('add'), state="disabled")
                recordMenu.entryconfig(self.__localization.getWord('edit'), state="disabled")
                recordMenu.entryconfig(self.__localization.getWord('delete'), state="disabled")
                
            else:
                if data.status == DBStatus.DISCONNECTED:
                    #data base menu
                    dbMenu.entryconfig(self.__localization.getWord("connect_db"), state="normal")
                    dbMenu.entryconfig(self.__localization.getWord("remove_db_from_config"), state="normal")
                    dbMenu.entryconfig(self.__localization.getWord("remove_db_from_filesystem"), state="normal")
                    dbMenu.entryconfig(self.__localization.getWord("disconnect_db"), state="disabled")
                    dbMenu.entryconfig(self.__localization.getWord("save"), state="disabled")
                    
                    #operations menu
                    categoryMenu.entryconfig(self.__localization.getWord('add'), state="disabled")
                    categoryMenu.entryconfig(self.__localization.getWord('edit'), state="disabled")
                    categoryMenu.entryconfig(self.__localization.getWord('delete'), state="disabled")
                    
                    recordMenu.entryconfig(self.__localization.getWord('add'), state="disabled")
                    recordMenu.entryconfig(self.__localization.getWord('edit'), state="disabled")
                    recordMenu.entryconfig(self.__localization.getWord('delete'), state="disabled")
                #if connected
                else:
                    dbMenu.entryconfig(self.__localization.getWord("connect_db"), state="disabled")
                    dbMenu.entryconfig(self.__localization.getWord("disconnect_db"), state="normal")
                    dbMenu.entryconfig(self.__localization.getWord("remove_db_from_config"), state="normal")
                    dbMenu.entryconfig(self.__localization.getWord("remove_db_from_filesystem"), state="normal")
                    if data.getIfChanged():
                        dbMenu.entryconfig(self.__localization.getWord("save"), state="normal")
                    else:
                        dbMenu.entryconfig(self.__localization.getWord("save"), state="disabled")
                        
                    #operations menu
                    categoryMenu.entryconfig(self.__localization.getWord('add'), state="normal")
                    recordMenu.entryconfig(self.__localization.getWord('add'), state="normal")                            
                                        
                dbMenu.entryconfig(self.__localization.getWord("remove_db_from_config"), state="normal") 

        if signal == Signal.CATEGORY_SELECTED_CHANGED:
            categoryMenu = self.__menuRef['category']
            if not data:
                #operations menu
                categoryMenu.entryconfig(self.__localization.getWord('edit'), state="disabled")
                categoryMenu.entryconfig(self.__localization.getWord('delete'), state="disabled")
            else:
                categoryMenu.entryconfig(self.__localization.getWord('edit'), state="normal")
                categoryMenu.entryconfig(self.__localization.getWord('delete'), state="normal") 
                
        if signal == Signal.RECORD_SELECTED_CHANGED:
            recordMenu = self.__menuRef['record']
            if not data:
                #operations menu
                recordMenu.entryconfig(self.__localization.getWord('edit'), state="disabled")
                recordMenu.entryconfig(self.__localization.getWord('delete'), state="disabled")
            else:
                #operations menu
                recordMenu.entryconfig(self.__localization.getWord('edit'), state="normal")
                recordMenu.entryconfig(self.__localization.getWord('delete'), state="normal")                                                                                 
                
        
        
    def  notdone(self):
        self.__notifier.sendSignal(Signal.NOT_YET_AVAILABLE, None) 


    def __getImage(self, value):
        if not value in self.__images.keys():
            self.__images[value] = PhotoImage(file=self.__resourceManager.getResource(value))
        return self.__images[value]      
    
    
    
    
    
    
    
    
    
                
#     root = Config.ASSEMBLER.assemble("MainApp")
#     #root = MainWin()                   
#     root.title('menu_win')   
#     #root.iconbitmap(default=r'D:/icon.ico')
#     root.title("EasyPass")
#     root.iconbitmap(default=r'D:/logo.ico') 
#     centerRoot(root)
#     
#     #Config.ASSEMBLER.assemble("AddRecordView")
#     
#     root.mainloop()
