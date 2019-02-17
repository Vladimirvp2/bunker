'''
Classes of auto generate password dialog
'''
 
import string, logging
import Tkinter as tk
import ttk
import UsConfig as Config
from abc import ABCMeta, abstractmethod
import tkFont



class PasswordGenerateI(object):
    """
    Generate password view interface 
    """
    __metaclass__ = ABCMeta
    @abstractmethod
    def getUpperCase(self):
        pass
    
    @abstractmethod
    def getLowerCase(self):
        pass
    
    @abstractmethod
    def getDigit(self):
        pass
    
    @abstractmethod
    def getMinus(self):
        pass
    
    @abstractmethod
    def getDot(self):
        pass
    
    @abstractmethod
    def getUnderline(self):
        pass
    
    @abstractmethod
    def getSpace(self):
        pass
    
    @abstractmethod
    def getEachCaracterAtMostOne(self):
        pass
    
    @abstractmethod
    def getExcludeLookLikeSymbols(self):
        pass
    
    @abstractmethod
    def getExcludedSymbols(self):
        pass
    
    @abstractmethod
    def getAdditionalSymbols(self):
        pass
    
    @abstractmethod
    def getCollectEntropy(self):
        pass
    
    @abstractmethod
    def getPasswordLength(self):
        pass  
    
    @abstractmethod
    def insertIntoPasswordPreview(self, text):
        pass
           
    @abstractmethod
    def clearPasswordPreview(self): 
        pass
    
    @abstractmethod
    def openPreviewTab(self): 
        pass
    
    @abstractmethod
    def getSelectedPassword(self):
        pass      
    
    
 
 
class PasswordGenerate(tk.Toplevel, PasswordGenerateI):
    """Dialog for password auto generation"""
     
    CHECKBOX_VALUE_ON = '1'
    CHECKBOX_VALUE_OFF = '0'
     
    #constants for widgets. Use them to get values of check boxes
    CHECKBOX_UPPERCASE_KEY = 'upper_case'
    CHECKBOX_LOWERCASE_KEY = 'lower_case'
    CHECKBOX_DIGITS_KEY = 'digits'
    CHECKBOX_MINUS_KEY = 'minus'
    CHECKBOX_UNDERLINE_KEY = 'underline'
    CHECKBOX_SPACE_KEY = 'space'
    CHECKBOX_DOT_KEY = 'dot'
     
    CHECKBOX_OCCUR_ONCE_KEY = 'occur_only_once'
    CHECKBOX_EXCLUDE_ALIKE_KEY = 'exclude_look_alike'
    CHECKBOX_COLLECT_ENTROPY_KEY = 'collect_entropy'
     
    SPINNER_PASSWORD_LENGTH_KEY = 'password_length_spinner'
    ENTRY_INCLUDE_CHARACRETS_KEY = 'include_characters_entry'
    ENTRY_ECXLUDE_CHARACRETS_KEY = 'exclude_characters_entry'
    TEXT_PASSWORD_PREVIEW_KEY = 'password_preview_text'
     
    #useful structures
    generalCheckboxKeys = [CHECKBOX_UPPERCASE_KEY, CHECKBOX_LOWERCASE_KEY, CHECKBOX_DIGITS_KEY, CHECKBOX_MINUS_KEY,
                            CHECKBOX_UNDERLINE_KEY, CHECKBOX_SPACE_KEY, CHECKBOX_DOT_KEY]
    advancedCheckboxKeys = [CHECKBOX_OCCUR_ONCE_KEY, CHECKBOX_EXCLUDE_ALIKE_KEY, CHECKBOX_COLLECT_ENTROPY_KEY]
    #text for check boxes
    generalCheckboxText = {generalCheckboxKeys[0]: 'Upper case',
                    generalCheckboxKeys[1] : 'Lower case',
                    generalCheckboxKeys[2] : 'Digits',
                    generalCheckboxKeys[3] : 'Minus',
                    generalCheckboxKeys[4] : 'Underline',
                    generalCheckboxKeys[5] : 'Space',
                    generalCheckboxKeys[6] : 'Dot'}
     
    advancedCheckboxText = {advancedCheckboxKeys[0] : 'Each character must occur only once',
                            advancedCheckboxKeys[1] : 'Exclude look-alike characters(O0, lI|)',
                            advancedCheckboxKeys[2] : 'Collect additional entropy'}
     
    #UI setting constants
    CELL_PADDING_X = 10
    CELL_PADDING_Y = 2
    SPINNBOX_LENGTH = 14
     
    BUTTONS_FRAME_PADDDING_X = 12
    BUTTONS_FRAME_PADDDING_Y = 5
    BUTTONS_SPACE_X = 5
     
    SEPARATOR_HEIGHT = 5
    ENTRY_WIDTH = 35
    LABEL_FRAME_PADDING_Y = 3
    LABEL_FRAME_PADDING_X = 1 
     
    PREVIEW_TAB_ID = 2   
     
     
    def __init__(self, controller, localization):    
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        self.__controller.addView(self)
        #values of all the check boxes. To address a certain check box use a key from  generalCheckboxKeys or advancedCheckboxKeys
        self.__GeneralCheckBoxValue = {}
        #references of all the widgets of which the information is needed
        self.__widgetsRef = {}
        self.__nb = None
        self.__currRow = 0
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.init()
         
         
    def init(self):
        self.__initStartCheckBoxValues()
         
        self.title('Generate password') 
          
        self.__nb = ttk.Notebook(self, name='nb') # create Notebook in "master"
        self.__nb.pack(fill=tk.BOTH, padx=2, pady=3) # fill "master" but pad sides
         
        self.addGeneralTab(self.__nb)
        self.addAdvancedTab(self.__nb)
        self.addPreviewTab(self.__nb)
             
             
    def addGeneralTab(self, parent):
        #create new tab
        mainFrame = ttk.Frame(parent)
        parent.add(mainFrame, text="General")
        genSettingsTab = ttk.LabelFrame(mainFrame, name='master-foo', text='Current settings')
        genSettingsTab.pack(fill=tk.X, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
        #add label and spin box for password length
        ttk.Label(genSettingsTab, text="Length of password ").grid(row=self.__getRow(False), column=0, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)
        varS = tk.StringVar()
        varS.set(Config.AUTO_PASSWORD_GENERATION_DEFAULT_LENGTH)
        self.sp = tk.Spinbox(genSettingsTab, 
                        from_=Config.AUTO_PASSWORD_GENERATION_MIN_LENGTH,
                        to=Config.AUTO_PASSWORD_GENERATION_MAX_LENGTH,
                        textvariable=varS )
        self.sp.config(width = self.SPINNBOX_LENGTH)
        self.sp.grid(row=self.__getRow(False), column=1, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)
        self.sp.bind('<KeyPress>', self.ignore)
        self.__widgetsRef[self.SPINNER_PASSWORD_LENGTH_KEY] = self.sp 
         
        #add separator
        self.__addSeparator(genSettingsTab, row=self.__getRow(True))
         
        #add check boxes for password specification       
        startCheckBoxRow = self.__getRow(False) + 1
        currColn = 0
        currRow = startCheckBoxRow
        for name in self.generalCheckboxKeys:
            c = ttk.Checkbutton(genSettingsTab, text=self.generalCheckboxText[name], variable=self.__GeneralCheckBoxValue[name],
                                onvalue=self.CHECKBOX_VALUE_ON,
                                offvalue=self.CHECKBOX_VALUE_OFF)
            self.__widgetsRef[name] = c
 
            #change column on the middle element
            if name == 'underline':
                currRow = startCheckBoxRow
                currColn = 1            
 
            if (currColn == 0):
                row = self.__getRow(True)
            else:
                row = currRow
                currRow+=1
                                
            c.grid(row=row, column=currColn, sticky=tk.W, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)
 
        #add separator
        self.__addSeparator(genSettingsTab, row=self.__getRow(True))         
                 
        #include characters label and entry
        ttk.Label(genSettingsTab, text="Include the following characters:").grid(row=self.__getRow(True), column=0, columnspan=2, 
                                                                             pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                                                                             sticky=tk.W)
        includeEnt = ttk.Entry(genSettingsTab, width=self.ENTRY_WIDTH)
        includeEnt.grid(row=self.__getRow(True), column=0, columnspan=2, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                 sticky=tk.E+tk.W)
        includeEnt.bind('<KeyPress>', self.printableOnly)
        self.__widgetsRef[self.ENTRY_INCLUDE_CHARACRETS_KEY] = includeEnt
         
        #add ok/cancel buttons
        self.__addOkCancelButtons(mainFrame, ok=self.generatePassword, cancel=self.cancel)
        
         
    def addAdvancedTab(self, parent):
        mainFrame = ttk.Frame(parent)
        parent.add(mainFrame, text="Advanced")
        advancedTab = ttk.LabelFrame(mainFrame, name='advanced', text='Advanced settings')
        advancedTab.pack(fill=tk.X, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
         
        #clean after the first general tab
        self.__setRowTo(0)
            
        for name in self.advancedCheckboxKeys:
            c = ttk.Checkbutton(advancedTab, text=self.advancedCheckboxText[name], variable=self.__GeneralCheckBoxValue[name],
                                onvalue=self.CHECKBOX_VALUE_ON,
                                offvalue=self.CHECKBOX_VALUE_OFF) 
             
            c.grid(row=self.__getRow(True), column=0, sticky=tk.W, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X)
            self.__widgetsRef[name] = c
             
        #include characters label and entry
        ttk.Label(advancedTab, text="Exclude the following characters:").grid(row=self.__getRow(True), column=0, columnspan=2, 
                                                                             pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                                                                             sticky=tk.W)
        excludeEnt = ttk.Entry(advancedTab, width=self.ENTRY_WIDTH)
        excludeEnt.grid(row=self.__getRow(True), column=0, columnspan=2, pady=self.CELL_PADDING_Y, padx = self.CELL_PADDING_X,
                 sticky=tk.E+tk.W)
        excludeEnt.bind('<KeyPress>', self.printableOnly)
        self.__widgetsRef[self.ENTRY_ECXLUDE_CHARACRETS_KEY] = excludeEnt        
                  
        self.__addOkCancelButtons(mainFrame, ok=self.generatePassword, cancel=self.cancel)
        
         
    def addPreviewTab(self, parent):
        mainFrame = ttk.Frame(parent)
        parent.add(mainFrame, text="Preview")
        previewTab = ttk.LabelFrame(mainFrame, name='preview', text='Sample passwords')
        previewTab.pack(fill=tk.BOTH, pady=self.LABEL_FRAME_PADDING_Y, padx=self.LABEL_FRAME_PADDING_X)
        
        #include characters label and entry
        ttk.Label(previewTab, text="Select one of the generated passwords:").pack(anchor=tk.W, side = tk.TOP)
         
        #add text area for passwords
        self.ent = tk.Text(previewTab, height=Config.AUTO_PASSWORD_GENERATION_SAMPLE_NUMBER, width=35 )
        ysb = tk.Scrollbar(previewTab, orient='vertical', command=self.ent.yview)
        self.ent.configure(yscroll=ysb.set)
        self.__widgetsRef[self.TEXT_PASSWORD_PREVIEW_KEY] = self.ent
                             
        self.ent.config(state=tk.DISABLED)
        ysb.pack(fill=tk.Y, side=tk.RIGHT, anchor=tk.E)
        self.ent.pack(fill=tk.X)  
        
        self.__addOkCancelButtons(mainFrame, ok=self.getSelectedPasswordPress, cancel=self.cancel)        
         
               
    def cancel(self):
        self.__controller.cancelPress()
        
        
    def getSelectedPasswordPress(self):
        self.__controller.getSelectedPasswordPress() 
        
             
    def generatePassword(self):
        self.__controller.generatePasswordPress()

                     
    def getSelectedPassword(self):
        textW = self.__widgetsRef[self.TEXT_PASSWORD_PREVIEW_KEY]
        sel = ""
        if textW.tag_ranges(tk.SEL):
            sel = textW.get(tk.SEL_FIRST, tk.SEL_LAST)
        return sel
             
             
    def ignore(self, event):
        if event.keysym not in ('Alt_r', 'Alt_L', 'F4'):
            return 'break'  
         
         
    def printableOnly(self, event):
        if event.char in string.printable:
            pass
        elif event.keysym not in ('Alt_r', 'Alt_L', 'F4', 'BackSpace', 'Delete'):
            return 'break'
        
        
    def getUpperCase(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_UPPERCASE_KEY)
    

    def getLowerCase(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_LOWERCASE_KEY)
    

    def getDigit(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_DIGITS_KEY)
    

    def getMinus(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_MINUS_KEY)
    

    def getDot(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_DOT_KEY)
    

    def getUnderline(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_UNDERLINE_KEY)
    

    def getSpace(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_SPACE_KEY)
    

    def getEachCaracterAtMostOne(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_OCCUR_ONCE_KEY)
    

    def getExcludeLookLikeSymbols(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_EXCLUDE_ALIKE_KEY)
    
    
    def getCollectEntropy(self):
        return self.__getIfCheckBoxChecked(self.CHECKBOX_COLLECT_ENTROPY_KEY)
    

    def getExcludedSymbols(self):
        return self.__widgetsRef[self.ENTRY_ECXLUDE_CHARACRETS_KEY].get().encode('utf8')
    

    def getAdditionalSymbols(self):
        return self.__widgetsRef[self.ENTRY_INCLUDE_CHARACRETS_KEY].get().encode('utf8')
    

    def getPasswordLength(self):
        return int(self.__widgetsRef[self.SPINNER_PASSWORD_LENGTH_KEY].get())   
    

    def insertIntoPasswordPreview(self, text):
        w = self.__widgetsRef[self.TEXT_PASSWORD_PREVIEW_KEY]
        w.config(state=tk.NORMAL)
        w.insert(tk.END, text)
        w.insert(tk.END, "\n") 
        w.config(state=tk.DISABLED) 
            
 
    def clearPasswordPreview(self): 
        w = self.__widgetsRef[self.TEXT_PASSWORD_PREVIEW_KEY]
        w.config(state=tk.NORMAL)
        w.delete('1.0', tk.END)  
        w.config(state=tk.DISABLED)
        
        
    def openPreviewTab(self): 
        self.__nb.select(self.PREVIEW_TAB_ID) 
                                 
             
    def __initStartCheckBoxValues(self):
        for c in self.generalCheckboxText.keys():
            self.__GeneralCheckBoxValue[c] = tk.StringVar()
             
        for c in self.advancedCheckboxText.keys():
            self.__GeneralCheckBoxValue[c] = tk.StringVar()
             
             
    def __getRow(self, increase=False):
        if increase: 
            self.__currRow+=1
         
        return self.__currRow 
     
     
    def __setRowTo(self, value):
        self.__currRow = value
         
     
    def __addSeparator(self, parent, row):
        ttk.Frame(parent, height = self.SEPARATOR_HEIGHT).grid(row=row, columnspan=2, sticky=tk.E+tk.W)        
         
     
    def __addOkCancelButtons(self, parent, ok, cancel):
        buttonsFrame = ttk.Frame(parent, name='master') # create Frame in "root"
        buttonsFrame.pack(side=tk.RIGHT, anchor = tk.SE, padx=self.BUTTONS_FRAME_PADDDING_X,
                                        pady=self.BUTTONS_FRAME_PADDDING_Y)       
                         
        btn = ttk.Button(buttonsFrame, text="Cancel", command=cancel)
        btn.pack(side=tk.RIGHT, padx=self.BUTTONS_SPACE_X)
        
        btn = ttk.Button(buttonsFrame, text="Ok", command=ok)
        btn.pack(side=tk.RIGHT) 
        
                  
    def __getIfCheckBoxChecked(self, key):
        value =  self.__GeneralCheckBoxValue[key].get()
        if value == self.CHECKBOX_VALUE_ON: 
            return True
        return False
       




class CollectEntropyI(object):
    """
    Collect entropy view interface 
    """
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def getProgress(self):
        """Get value of progress as percentage"""
        pass
    
    @abstractmethod
    def setProgress(self, value):
        """Get value of progress as percentage"""
        pass
    



class CollectEntropy(tk.Toplevel, CollectEntropyI):
    """Dialog for collecting additional entropy for password generation"""
    BUTTONS_FRAME_PADDDING_X = 12
    BUTTONS_FRAME_PADDDING_Y = 5
    BUTTONS_SPACE_X = 5
    PERCENTAGE_MAX = 100
    
    
    def __init__(self, controller, localization):
        tk.Toplevel.__init__(self)
        self.__controller = controller
        self.__localization = localization
        self.__controller.addView(self)
        self.__currRow = 0
        #0-100
        self.__currProgress = 0
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.resizable(0,0)
        self.__fontLabel = tkFont.Font(size = 20, family='Arial')
        self.init()
        
        
    def init(self):
        #set dialog title
        self.title("Collect entropy")
        #w = ttk.Label(self, text="Random mouse input", font = Config.LABEL_FONT_TABFRAME)
        #fr = ttk.LabelFrame(self, name='preview', text='Random mouse input', labelwidget = w)
        fr = ttk.LabelFrame(self, name='preview', text='Random mouse input')
        fr.pack()
        ttk.Label(fr, text="Click a few times the image and press Ok").grid(row=self.__getRow(False), column = 0, columnspan=2, sticky = tk.W)
        
        self._image = tk.PhotoImage(file=r"D:/grained_texture.gif")
        #self.__image = PhotoImage(file=r"Icons/error_dialog.gif")
        self.im = tk.Label(fr, image = self._image, padx=5)
        self.im.grid(row=self.__getRow(True), column = 0, columnspan=2, sticky = tk.W)
        self.im.bind('<ButtonRelease-1>', self.__imageClicked)
        
        #s.configure("yellow.Horizontal.TProgressbar", foreground='yellow', background='yellow')
        
        ttk.Label(fr, text="Generated random values: ").grid(row=self.__getRow(True), column = 0, columnspan=2, sticky = tk.W)
        
        progressFrame = ttk.Frame(fr)
        progressFrame.grid(row=self.__getRow(True), column=0, columnspan=2, sticky=tk.W+tk.E)
        
        #tk.Label(progressFrame, text="Generated random values: ").pack(side=tk.LEFT, anchor=tk.W)
        
        s = ttk.Style()
        #s.theme_use('clam')
        s.configure("red.Horizontal.TProgressbar", foreground='red', background='red')
        
        self.__pb = ttk.Progressbar(progressFrame, orient='horizontal', mode='determinate', style="red.Horizontal.TProgressbar")
        self.__pb.pack(side=tk.LEFT, anchor=tk.W, expand=1, fill=tk.X)
        self.__pb["value"] = 0
        self.__pb["maximum"] = self.PERCENTAGE_MAX
        
        self.__pl = ttk.Label(progressFrame, text="0%")
        self.__pl.pack(side=tk.RIGHT, anchor=tk.E, padx=5)
        
        self.__addOkCancelButtons(self, self.ok, self.cancel)
        

    def getProgress(self):
        return self.__currProgress
    

    def setProgress(self, value):
        self.__currProgress = value
        self.__pb["value"] = value
        self.__pl.config(text="{}%".format(value))
        
            
    def cancel(self):
        self.__controller.cancelPress()  
        
                
    def ok(self):
        self.__controller.okPress() 
        
        
    def __addOkCancelButtons(self, parent, ok, cancel):
        buttonsFrame = tk.Frame(parent, name='master') # create Frame in "root"
        buttonsFrame.pack(side=tk.RIGHT, anchor = tk.SE, padx=self.BUTTONS_FRAME_PADDDING_X,
                                        pady=self.BUTTONS_FRAME_PADDDING_Y)       
                         
        btn = ttk.Button(buttonsFrame, text="Cancel", command=cancel)
        btn.pack(side=tk.RIGHT, padx=self.BUTTONS_SPACE_X)
        
        btn = ttk.Button(buttonsFrame, text="Ok", command=ok)
        btn.pack(side=tk.RIGHT) 
        
        
    def __getRow(self, increase=False):
        if increase: 
            self.__currRow+=1
         
        return self.__currRow 
    
    
    def __imageClicked(self, event):
        self.__controller.mouseClick(event.x, event.y)                  
                             
 
 
if __name__ == "__main__":
    #g = pswg.PasswordGenerator()
    #w = PasswordGenerate(g)
    #w.mainloop()
    
    d = CollectEntropy(1, 1)
    d.mainloop()



