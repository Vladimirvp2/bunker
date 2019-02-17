'''
GUI classes for merge databases dialog 
'''

import Tkinter as tk
import ttk, logging
from Common.Utilities import AutoScrollbar
from GUI.MessageDialog import*
import UsConfig as Config 
import Common.Constants.LabelType as LabelType
from abc import ABCMeta, abstractmethod
import Common.Constants.DataField as DataField
from tkFileDialog   import asksaveasfilename

        
        

class MergeDatabasesI(object): 
    """Interface for Merge database dialog view"""   
    
    __metaclass__ = ABCMeta
    
    
    @abstractmethod
    def getDBAllSelected(self):
        """Get index of the selected object in the list of all databases"""
        pass
    
    @abstractmethod
    def insertIntoDBAllList(self, value):
        """Insert value into the list of all databases"""
        pass
    
    @abstractmethod
    def getDBChoosenSelected(self):
        """Get index of the selected object in the list of the chosen databases"""
        pass 
    
    @abstractmethod
    def insertIntoDBChoosenList(self, value):
        """Insert value into the list of the chosen databases"""
        pass
    
    @abstractmethod
    def removeFromDBChoosenList(self, index):
        """Remove row by index from the list of the chosen databases"""
        pass
      
    
    @abstractmethod
    def getMergeModeRadiobuttonValue(self):
        pass
    
    
    @abstractmethod  
    def clearDBPriorityList(self):
        pass
    
    @abstractmethod    
    def setPrioritySelectedInPriorityList(self, priority):
        pass
            
    @abstractmethod             
    def addDataInPriorityList(self, priority, dbname):
        pass
    
    @abstractmethod       
    def getSelectedInPriorittyList(self):
        """
        Get the data of selected row from priority tree
        @return: index
        """
           


class MergeDatabases(tk.Toplevel, MergeDatabasesI):
    """Dialog for merging databases"""
    
    #UI setting constants
    WIN_WIDTH = 470
    WIN_HEIGHT = 330
    
    CELL_PADDING_X = 5
    CELL_PADDING_Y = 2
    CELL_PADDING_RADIOBUTTON_Y = 0
        
    LABEL_FRAME_PADDING_Y = 3
    LABEL_FRAME_PADDING_X = 1 
    
    BUTTONS_FRAME_PADDDING_X = 12
    BUTTONS_FRAME_PADDDING_Y = 5
    BUTTONS_SPACE_X = 5
    
    LIST_WIDTH_CATARTERS = 26
    ADD_REMOVE_BUTTON_PADDING_Y = 4
    
    
    #views in wizard
    VIEW_CHOOSE_DB = 0
    VIEW_SET_MODE = 1
    VIEW_SET_PRIORITY = 2 
    VIEW_FINISH = 3      
    
    #widget ids
    VIEW_CHOOSE_DB_LIST_ALL_DB = 0
    VIEW_CHOOSE_DB_LIST_CHOOSEN_DB = 1
    VIEW_CHOOSE_DB_BUTTON_ADD_DB = 2
    VIEW_CHOOSE_DB_BUTTON_REMOVE_DB = 3
    VIEW_SET_MODE_RADIOBUTTON_VALUE = 4
    VIEW_SET_MODE_TREE = 5
    VIEW_SET_MODE_TREE_FRAME = 6
    
    #Radio button constants
    RADIOBUTTON_REWRITE_OLDER_RECORDS = 4
    RADIOBUTTON_MANUAL = 5
    RADIOBUTTON_REWRITE_BY_PRIORITY = 6
    RADIOBUTTON_DEFAULT = RADIOBUTTON_REWRITE_OLDER_RECORDS
    
    
    #Buttons type
    BUTTON_NEXT = 0
    BUTTON_BACK = 1
    BUTTON_CANCEL = 2
    BUTTON_OK = 3
    
    PRIORITY_ROW_START = -1

    def __init__(self, controller, localization, notifier):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        self.__notifier = notifier
        #add self to controller
        self.__controller.addView(self)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.__widgetsRef = {}
        #list of all DB registered for a current user
        self.__allDBObject = []
        #list of DBs to merge
        self.__mergeDBObjects = []
        self.__images = {}
        self.__resourceManager = Config.ASSEMBLER.assemble("ResourceManager")
        #user by grid manager
        self.__currRow = 0
        #id for tree for setting priority of databases
        self.__priorityRowID = self.PRIORITY_ROW_START
        #references of views to hide and show them
        self.__chooseDBView = None
        self.__mergeModeView = None
        self.__setPriorityView = None
        self.__finishView = None
        
        self.minsize(width=self.WIN_WIDTH, height=self.WIN_HEIGHT)
        self.maxsize(width=self.WIN_WIDTH, height=self.WIN_HEIGHT)

        self.init()
        
        
    def init(self):
        self.title(self.__localization.getWord('merge_databases_dialog_title'))
        self.addChooseDatabasesView()
        self.addMergeModeView()
        self.addSetDBPriorityView()
        
        self.addFinishView()
        self.__controller.initDBList()
        self.showView(self.VIEW_CHOOSE_DB)
        
        
    def addChooseDatabasesView(self):
        self.__setRowTo(0)
        mainFrame = tk.Frame(self)
        mainFrame.pack(expand=1, fill=tk.BOTH)
        self.__chooseDBView = mainFrame
        #parent.add(mainFrame, text="Databases")
        tabL = ttk.Label(mainFrame, text=self.__localization.getWord('databases'), font=Config.getFont(LabelType.LABEL_FRAME_TITLE),
                          foreground=Config.getLabelColor(LabelType.LABEL_FRAME_TITLE))
        labelFrame = ttk.LabelFrame(mainFrame, name='choose_dbs', labelwidget=tabL)
        labelFrame.pack(fill=tk.X, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
        #add label and spin box for password length
        ttk.Label(labelFrame, text=self.__localization.getWord('choose_databases_to_merge'), font=Config.getFont(LabelType.TITEL_TEXT)).grid(row=self.__getRow(False),
                                                                                     column=0, columnspan=2, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                                                                                     sticky = tk.W)
        
        ttk.Label(labelFrame, text=self.__localization.getWord('user_databases'), font=Config.getFont(LabelType.NORMAL_TEXT)).grid(row=self.__getRow(True),
                                                                                     column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)
        
        ttk.Label(labelFrame, text=self.__localization.getWord('chosen_databases'), font=Config.getFont(LabelType.NORMAL_TEXT)).grid(row=self.__getRow(False),
                                                                                     column=1, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)        
        
        dbListRowFrame = self.__getRow(True)
        self.__createDBScrollList(labelFrame, dbListRowFrame, 0, type = self.VIEW_CHOOSE_DB_LIST_ALL_DB)
        self.__createDBScrollList(labelFrame, dbListRowFrame, 1, type = self.VIEW_CHOOSE_DB_LIST_CHOOSEN_DB)
        
        #add Ok/cancel buttons
        self.__addOkCancelButtons(mainFrame, action1=lambda: self.__getButtonAction(self.VIEW_CHOOSE_DB, self.BUTTON_NEXT), text1=self.__localization.getWord('next'), image1 = self.__getImage('next_btn_image'), imageAlign1 = 'right',
                                                    action2=lambda: self.__getButtonAction(self.VIEW_CHOOSE_DB, self.BUTTON_CANCEL), text2 = self.__localization.getWord('cancel'))
        
        
        
    def addMergeModeView(self):
        self.__setRowTo(0)
        mainFrame = tk.Frame(self)
        mainFrame.pack(expand=1, fill=tk.BOTH)
        self.__mergeModeView = mainFrame
        tabL = ttk.Label(mainFrame, text=self.__localization.getWord('merge_mode'), font=Config.getFont(LabelType.LABEL_FRAME_TITLE),
                          foreground=Config.getLabelColor(LabelType.LABEL_FRAME_TITLE))
        labelFrame = ttk.LabelFrame(mainFrame, name='merge_mode', text='Merge modes', labelwidget=tabL)
        labelFrame.pack(fill=tk.X, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
        #add label and spin box for password length
        ttk.Label(labelFrame, text=self.__localization.getWord('choose_merge_mode'), font=Config.getFont(LabelType.TITEL_TEXT), foreground=Config.getLabelColor(LabelType.TITEL_TEXT),
                  ).grid(row=self.__getRow(False), column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X, sticky=tk.W)         

        RadioButtonData = [ (self.RADIOBUTTON_REWRITE_OLDER_RECORDS , self.__localization.getWord('rewrite_olders_mode') ),
                    (self.RADIOBUTTON_MANUAL , self.__localization.getWord('manual_mode') ),
                    (self.RADIOBUTTON_REWRITE_BY_PRIORITY , self.__localization.getWord('database_priority_mode') )] 
        
        self.__widgetsRef[self.VIEW_SET_MODE_RADIOBUTTON_VALUE] = tk.StringVar()
        v = self.__widgetsRef[self.VIEW_SET_MODE_RADIOBUTTON_VALUE] 
        v.set(self.RADIOBUTTON_DEFAULT) 

        for mode, text in RadioButtonData:
            b = Radiobutton(labelFrame, text=text,
                            variable=v, value=mode,
                            font = Config.getFont(LabelType.RADIO_BUTTON), 
                            foreground = Config.getLabelColor(LabelType.RADIO_BUTTON))
            b.grid(row=self.__getRow(True), column=0, pady=self.CELL_PADDING_RADIOBUTTON_Y, padx = self.CELL_PADDING_X, sticky=tk.W)

        self.__addOkCancelButtons(mainFrame, action1=lambda: self.__getButtonAction(self.VIEW_SET_MODE, self.BUTTON_BACK), text1=self.__localization.getWord('back'), image1 = self.__getImage('back_btn_image'), imageAlign1 = 'left',
                                                    action2=lambda: self.__getButtonAction(self.VIEW_SET_MODE, self.BUTTON_NEXT), text2=self.__localization.getWord('next'), image2 = self.__getImage('next_btn_image'), imageAlign2 = 'right',
                                                    action3=lambda: self.__getButtonAction(self.VIEW_SET_MODE, self.BUTTON_CANCEL), text3 = self.__localization.getWord('cancel'))

        
        
    def addSetDBPriorityView(self):
        self.__setRowTo(0)
        mainFrame = tk.Frame(self)
        mainFrame.pack(expand=1, fill=tk.BOTH)
        self.__setPriorityView = mainFrame
        tabL = ttk.Label(mainFrame, text=self.__localization.getWord('database_priorities'), font=Config.getFont(LabelType.LABEL_FRAME_TITLE),
                          foreground=Config.getLabelColor(LabelType.LABEL_FRAME_TITLE))
        labelFrame = ttk.LabelFrame(mainFrame, name='merge_mode', labelwidget=tabL)
        labelFrame.pack(fill=tk.X, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
        #add label and spin box for password length
        ttk.Label(labelFrame, text=self.__localization.getWord('set_db_priorities'), font=Config.getFont(LabelType.TITEL_TEXT)).grid(
                                    row=self.__getRow(False), column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X, sticky=tk.W) 


        frame = tk.Frame(labelFrame)
        treeRow = self.__getRow(True)
        frame.grid(row=treeRow, column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X, sticky=tk.E+tk.W)
        tk.Grid.rowconfigure(labelFrame, treeRow, weight=1)
        tk.Grid.columnconfigure(labelFrame, 0, weight=1)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        
        tree = ttk.Treeview(frame, style=Config.TREEVIEW_DIALOG_STYLE)
        ysb = tk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscroll=ysb.set)
        tree["columns"]=("one")
        tree.heading('#0', text=self.__localization.getWord('priority_title'))
        tree.heading("one", text=self.__localization.getWord('databases_title'))
        tree.column("#0", width=70 )
        tree.column("one", width=330 )
        tree['height'] = 8
        self.__widgetsRef[self.VIEW_SET_MODE_TREE] = tree
        self.__widgetsRef[self.VIEW_SET_MODE_TREE_FRAME] = frame
        tree.bind("<ButtonRelease-3>", lambda event : self.__showPriorityContextMenu(event))
     
        tree.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        ysb.grid(row=0,column=1, sticky=tk.N+tk.S+tk.E+tk.W) 
        
        
        ttk.Label(labelFrame, text=self.__localization.getWord('set_db_priorities_prompt'), font=Config.getFont(LabelType.NORMAL_TEXT)).grid(
                                    row=self.__getRow(True), column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X, sticky=tk.W) 
    
     
        self.__addOkCancelButtons(mainFrame, action1=lambda: self.__getButtonAction(self.VIEW_SET_PRIORITY, self.BUTTON_BACK), text1=self.__localization.getWord('back'), image1 = self.__getImage('back_btn_image'), imageAlign1 = 'left',
                                                    action2=lambda: self.__getButtonAction(self.VIEW_SET_PRIORITY, self.BUTTON_NEXT), text2=self.__localization.getWord('next'), image2 = self.__getImage('next_btn_image'), imageAlign2 = 'right',
                                                    action3=lambda: self.__getButtonAction(self.VIEW_SET_PRIORITY, self.BUTTON_CANCEL), text3 = self.__localization.getWord('cancel'))    
        
        
    def addFinishView(self):
        LABEL_WIDTH = 12
        LABEL_PAD_X = 2
        BUTTON_CHOOSE_DIALOG_WIDTH = 35
        ENTRY_WIDTH = 35
        COMMENT_AREA_HIGHT = 3
        ROW_PAD_Y = 2
        
        self.__setRowTo(0)
        mainFrame = tk.Frame(self)
        mainFrame.pack(expand=1, fill=tk.BOTH)
        self.__finishView = mainFrame
        tabL = ttk.Label(mainFrame, text=self.__localization.getWord('result_database'), font=Config.getFont(LabelType.LABEL_FRAME_TITLE),
                          foreground=Config.getLabelColor(LabelType.LABEL_FRAME_TITLE))
        labelFrame = ttk.LabelFrame(mainFrame, name='merge_mode', labelwidget=tabL)
        labelFrame.pack(fill=tk.X, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
        #add label and spin box for password length
        ttk.Label(labelFrame, text=self.__localization.getWord('provide_info_result_database'), font=Config.getFont(LabelType.TITEL_TEXT)).grid(row=self.__getRow(False), column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                                                         sticky = tk.W) 
         
        
        elFrame = tk.Frame(labelFrame) 
        elFrame.grid(row=self.__getRow(True), column=0, columnspan=2, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)
        #add GUI elements
        fields_data = { DataField.PATH : self.__localization.getWord('path_to_file'),
                   DataField.PASSWORD : self.__localization.getWord('password'),
                   DataField.COMMENTS : self.__localization.getWord('comments'),
                   DataField.NAME : self.__localization.getWord('name')}
        fields = [DataField.PATH, DataField.NAME, DataField.PASSWORD, DataField.COMMENTS]
        
        for field in fields:
            row = tk.Frame(elFrame) 
            lab = ttk.Label(row, width=LABEL_WIDTH, text=fields_data[field], font=Config.getFont(LabelType.NORMAL_TEXT))
            ent = None
            if field == DataField.PATH:             
                ent = ttk.Button(row, text='file', command=self.chooseFile, width=BUTTON_CHOOSE_DIALOG_WIDTH)
                self.__chooseFileButton = ent
            elif field == DataField.PASSWORD:
                ent = tk.Entry(row, show="*", width=ENTRY_WIDTH)
            elif field == DataField.COMMENTS:
                ent = tk.Text(row, height=COMMENT_AREA_HIGHT, width=ENTRY_WIDTH  ) 
            else:
                ent = tk.Entry(row, width=ENTRY_WIDTH)                              
                
            row.pack(side=tk.TOP, fill=tk.X, pady=ROW_PAD_Y)              
            lab.pack(side=tk.LEFT, anchor=tk.W, padx=LABEL_PAD_X )
            ent.pack(side=tk.RIGHT, expand=tk.YES, fill=tk.X)
            
        ttk.Label(labelFrame, text=self.__localization.getWord('press_start_to_begin_merge'), font=Config.getFont(LabelType.NORMAL_TEXT)).grid(row=self.__getRow(True), column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                                                         sticky = tk.W)          
         
         
        self.__addOkCancelButtons(mainFrame, action1=lambda: self.__getButtonAction(self.VIEW_FINISH, self.BUTTON_BACK) , text1=self.__localization.getWord('back'), image1 = self.__getImage('back_btn_image'), imageAlign1 = 'left',
                                                    action2=lambda: self.__getButtonAction(self.VIEW_FINISH, self.BUTTON_OK) , text2=self.__localization.getWord('start'),
                                                    action3=lambda: self.__getButtonAction(self.VIEW_FINISH, self.BUTTON_CANCEL) , text3 = self.__localization.getWord('cancel'))        
                
     
        
    def showView(self, viewType):
        if viewType == self.VIEW_CHOOSE_DB:                
            self.__mergeModeView.pack_forget()
            self.__finishView.pack_forget()
            self.__setPriorityView.pack_forget()
            self.__chooseDBView.pack(expand=1, fill=tk.BOTH, anchor=tk.W)
        elif viewType == self.VIEW_SET_MODE:  
            if self.__controller.noDBChosen():
                showError(self, 
                title = self.__localization.getWord('error'),
                text = self.__localization.getWord('no_db_to_merge'), 
                buttonsText=[self.__localization.getWord('ok'),]) 
                return              
            self.__chooseDBView.pack_forget()
            self.__finishView.pack_forget()
            self.__setPriorityView.pack_forget()
            self.__mergeModeView.pack(expand=1, fill=tk.BOTH)
        elif viewType == self.VIEW_SET_PRIORITY:
            #reload db priorities tree
            self.clearDBPriorityList()
            self.__controller.fillPriorityList()
            
            self.__mergeModeView.pack_forget()
            self.__chooseDBView.pack_forget()
            self.__finishView.pack_forget()
            self.__setPriorityView.pack(expand=1, fill=tk.BOTH)
        elif viewType == self.VIEW_FINISH:
            if self.getMergeModeRadiobuttonValue() == str(self.RADIOBUTTON_REWRITE_BY_PRIORITY):
                if not self.__controller.allPrioritiesProvided():
                    showError(self, 
                              title = self.__localization.getWord('error'),
                              text = self.__localization.getWord('provide_priorities_for_all_db'), 
                              buttonsText=[self.__localization.getWord('ok'),]) 
                    return 
            self.__mergeModeView.pack_forget()
            self.__chooseDBView.pack_forget()
            self.__setPriorityView.pack_forget() 
            self.__finishView.pack(expand=1, fill=tk.BOTH)  
            
    def chooseFile(self):
        ftypes = [('database file', '.db')]
        self.__path = asksaveasfilename(filetypes=ftypes, title=self.__localization.getWord('path_to_file'),
                                     defaultextension='.db') 
        self.__chooseFileButton.config(text=self.__path) 
              
        
    def cancel(self):
        self.__controller.cancel()  
        
    def startMerge(self):
        self.__controller.startMerge() 
                
    
    def onSelectDBAll(self, evt):
        self.enableAddDBButton(True)
        self.enableRemoveDBButton(False)
        
        
    def onSelectDBChoosen(self, evt):
        self.enableRemoveDBButton(True)
        self.enableAddDBButton(False)
        
        
    def addDBPress(self):
        self.__controller.addDBPress()
        
        
    def removeDBPress(self):
        self.__controller.removeDBPress()


    def __createDBScrollList(self, parent, row, column, type):
        tk.Grid.rowconfigure(parent, row, weight=1)
        tk.Grid.columnconfigure(parent, column, weight=1)
        frame = tk.Frame(parent)
        frame.grid(row=row, column=column, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X, sticky=tk.E+tk.W)
        tk.Grid.rowconfigure(frame, 0, weight=1)
        tk.Grid.columnconfigure(frame, 0, weight=1)
        scrollbarY = AutoScrollbar(frame)
        scrollbarX = AutoScrollbar(frame, orient='horizontal')
        scrollbarY.grid(row=0,column=1, sticky=tk.N+tk.S+tk.E)  
        scrollbarX.grid(row=1, column=0, sticky=tk.E+tk.W) 


        mylist = tk.Listbox(frame, font=Config.getFont(LabelType.LISTBOX), foreground=Config.getLabelColor(LabelType.LISTBOX), selectmode=tk.SINGLE, width = self.LIST_WIDTH_CATARTERS, yscrollcommand = scrollbarY.set, xscrollcommand = scrollbarX.set )
        mylist.grid(row=0,column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        scrollbarY.config( command = mylist.yview )
        scrollbarX.config( command = mylist.xview ) 
                
        action = None
        text = ""
        listKey = ""
        btnKey = ""
        selectAction = None
        if type == self.VIEW_CHOOSE_DB_LIST_ALL_DB:
            action = self.addDBPress
            text = self.__localization.getWord('add_btn')
            listKey = self.VIEW_CHOOSE_DB_LIST_ALL_DB
            btnKey = self.VIEW_CHOOSE_DB_BUTTON_ADD_DB
            selectAction = self.onSelectDBAll
        elif type == self.VIEW_CHOOSE_DB_LIST_CHOOSEN_DB:
            action = self.removeDBPress
            text = self.__localization.getWord('remove_btn')
            listKey = self.VIEW_CHOOSE_DB_LIST_CHOOSEN_DB
            btnKey = self.VIEW_CHOOSE_DB_BUTTON_REMOVE_DB
            selectAction = self.onSelectDBChoosen
            
        btn = ttk.Button(frame, text=text, command=action, style=Config.BUTTON_STYLE)
        btn.grid(row=2, column=0, columnspan=2, pady=self.ADD_REMOVE_BUTTON_PADDING_Y) 
        btn.state(["disabled"])
        
        mylist.bind('<<ListboxSelect>>', selectAction)
        
        #add references of list and button
        self.__widgetsRef[listKey] = mylist
        self.__widgetsRef[btnKey] = btn        
        
        
    def __getRow(self, increase=False):
        if increase: 
            self.__currRow+=1
         
        return self.__currRow 
     
     
    def __setRowTo(self, value):
        self.__currRow = value
        
        
    def __addOkCancelButtons(self, parent, action1, text1,  action2=None, text2="", text3="", action3=None, image1=None, imageAlign1="left", image2=None, imageAlign2="left"):
        buttonsFrame = tk.Frame(parent, name='master') 
        buttonsFrame.pack(side=tk.RIGHT, anchor = tk.SE, padx=self.BUTTONS_FRAME_PADDDING_X,
                                        pady=self.BUTTONS_FRAME_PADDDING_Y) 
        
        btn = None
        if action3:
            btn = ttk.Button(buttonsFrame, text=text3, style=Config.BUTTON_STYLE, command=action3)
            btn.pack(side=tk.RIGHT, padx=self.BUTTONS_SPACE_X*2)
        
        if image2:         
            btn = ttk.Button(buttonsFrame, text=text2, style=Config.BUTTON_STYLE, command=action2, image=image2, compound=imageAlign2)
        else:
            btn = ttk.Button(buttonsFrame, text=text2, style=Config.BUTTON_STYLE, command=action2)            
        btn.pack(side=tk.RIGHT)
        
            
        if image1:
            btn = ttk.Button(buttonsFrame, text=text1, style=Config.BUTTON_STYLE, command=action1, image=image1, compound=imageAlign1)
        else:   
            btn = ttk.Button(buttonsFrame, text=text1, style=Config.BUTTON_STYLE, command=action1)
        btn.pack(side=tk.RIGHT, padx=self.BUTTONS_SPACE_X)
        
    
    
    def getDBAllSelected(self):
        listDBAll = self.__widgetsRef[self.VIEW_CHOOSE_DB_LIST_ALL_DB]
        #if no elements selected
        if len(listDBAll.curselection()) == 0:
            return None
        index = int(listDBAll.curselection()[0])
        return index
    

    def getDBChoosenSelected(self):
        listChoosenDBs = self.__widgetsRef[self.VIEW_CHOOSE_DB_LIST_CHOOSEN_DB]
        #if no elements selected
        if len(listChoosenDBs.curselection()) == 0:
            return None
        index = int(listChoosenDBs.curselection()[0]) 
        return index
    

    def insertIntoDBChoosenList(self, value):
        listChoosenDBs = self.__widgetsRef[self.VIEW_CHOOSE_DB_LIST_CHOOSEN_DB]
        listChoosenDBs.insert(tk.END, value)
             

    def insertIntoDBAllList(self, value):
        listAllDBs = self.__widgetsRef[self.VIEW_CHOOSE_DB_LIST_ALL_DB]
        listAllDBs.insert(tk.END, value)
        
        
    def removeFromDBChoosenList(self, index):
        listChoosenDBs = self.__widgetsRef[self.VIEW_CHOOSE_DB_LIST_CHOOSEN_DB]
        listChoosenDBs.delete(index)
        
        
    def enableAddDBButton(self, value):
        state = '!disabled' if value else 'disabled'
        self.__widgetsRef[self.VIEW_CHOOSE_DB_BUTTON_ADD_DB].state([state])
    

    def enableRemoveDBButton(self, value):
        state = '!disabled' if value else 'disabled'
        self.__widgetsRef[self.VIEW_CHOOSE_DB_BUTTON_REMOVE_DB].state([state])
        
        
    def getMergeModeRadiobuttonValue(self):
        mergeModeValue = str(self.RADIOBUTTON_DEFAULT)
        if self.VIEW_SET_MODE_RADIOBUTTON_VALUE in self.__widgetsRef.keys():
            v = self.__widgetsRef[self.VIEW_SET_MODE_RADIOBUTTON_VALUE]
            mergeModeValue = str(v.get())
            
        return mergeModeValue
    
    
    def clearDBPriorityList(self):
        tree = self.__widgetsRef[self.VIEW_SET_MODE_TREE]
        for i in tree.get_children():
            tree.delete(i)
        self.__priorityRowID = self.PRIORITY_ROW_START 
        
            
            
    def addDataInPriorityList(self, priority, dbname):
        tree = self.__widgetsRef[self.VIEW_SET_MODE_TREE]
        tree.insert("", 'end', self.getNextPriorityTreeID(), text=priority, 
                                    values=(dbname) )
        
   
    def setPrioritySelectedInPriorityList(self, priority):
        tree = self.__widgetsRef[self.VIEW_SET_MODE_TREE]
        clickedItem = tree.focus()
        if not clickedItem:
            return 
        item = tree.item(clickedItem)
        tree.item(clickedItem, text=(priority), values=(item['values'][0]))
        
        
    def getNextPriorityTreeID(self):
        self.__priorityRowID +=1
        return str(self.__priorityRowID) 
    
    
    def getSelectedInPriorittyList(self):
        tree = self.__widgetsRef[self.VIEW_SET_MODE_TREE]
        clickedItem = tree.focus()
        if not clickedItem:
            return None
        return clickedItem
    
    
    def __getButtonAction(self, viewType, buttonType):
        mergeMode = self.getMergeModeRadiobuttonValue()
#             print mergeMode
        if viewType == self.VIEW_CHOOSE_DB:
            if buttonType == self.BUTTON_NEXT:
                return self.showView(self.VIEW_SET_MODE)
            elif buttonType == self.BUTTON_CANCEL:
                return self.cancel() 
            
        elif viewType == self.VIEW_SET_MODE:
            if buttonType == self.BUTTON_NEXT:
                if mergeMode == str(self.RADIOBUTTON_REWRITE_BY_PRIORITY):
                    return self.showView(self.VIEW_SET_PRIORITY)
                else:
                    return self.showView(self.VIEW_FINISH)  
            elif buttonType == self.BUTTON_BACK:
                return self.showView(self.VIEW_CHOOSE_DB)                 
            elif buttonType == self.BUTTON_CANCEL:
                return self.cancel() 
            
        elif viewType == self.VIEW_SET_PRIORITY:
            if buttonType == self.BUTTON_NEXT:
                return self.showView(self.VIEW_FINISH) 
            elif buttonType == self.BUTTON_BACK:
                return self.showView(self.VIEW_SET_MODE)                 
            elif buttonType == self.BUTTON_CANCEL:
                return self.cancel() 
            
        elif viewType == self.VIEW_FINISH:
            if buttonType == self.BUTTON_OK:
                return self.startMerge()
            elif buttonType == self.BUTTON_BACK:
                if mergeMode == str(self.RADIOBUTTON_REWRITE_BY_PRIORITY):
                    return self.showView(self.VIEW_SET_PRIORITY)
                else:
                    return self.showView(self.VIEW_SET_MODE)                                 
            elif buttonType == self.BUTTON_CANCEL:
                return self.cancel()
            
        return None 
       

    def __showPriorityContextMenu(self, event):
        tree = self.__widgetsRef[self.VIEW_SET_MODE_TREE]
        clickedItem = tree.focus()
        item = tree.item(clickedItem)
        print clickedItem
        if not clickedItem:
            return 
        menu = Menu(self, tearoff=0)
        menu.add_command(label=self.__localization.getWord('set_priority_menu'), command=lambda : self.__controller.showSetPriorityDialog())
        menu.post(event.x_root, event.y_root)  
        
        
    def __getImage(self, value):
        if not value in self.__images.keys():
            self.__images[value] = PhotoImage(file=self.__resourceManager.getResource(value))
        return self.__images[value]    

    
