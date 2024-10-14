from GlobalImport import *
from Custom import CustomLabel

class SwitchLabel(CustomLabel):
    initials : StringVar
    po : StringVar
    switchType : StringVar
    
    radioNormal : Radiobutton
    radioOLED : Radiobutton
    radioLite : Radiobutton

    model : StringVar
    storageSize : StringVar
    storageModelLabel : Label
    
    color : StringVar
    colorEntry : Entry

    sn : StringVar
    serialEntry : Entry
    clearSN : BooleanVar
    clearButton : Checkbutton

    switchL : zpl.Label

    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, height=height, mm=mm,startColumn=startColumn, startRow=startRow)
        self.initials = StringVar(value=initials)
        self.po = StringVar(value=po)

        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def WindowFocused(self,event):
        if event.widget in [self.radioNormal, self.radioOLED, self.radioLite, self.root, self.clearButton]:
            self.serialEntry.focus_set()
    
    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        self.switchType = StringVar(value="Normal")
        ttk.Label(self.frame, text="Type:").grid(column=startColumn,row=startRow)
        self.radioNormal = ttk.Radiobutton(self.frame, text="Normal", value="Normal", variable=self.switchType,command=self.RadioChanged)
        self.radioNormal.grid(column=startColumn+1,row=startRow)
        self.radioOLED = ttk.Radiobutton(self.frame, text="OLED", value="OLED", variable=self.switchType,command=self.RadioChanged)
        self.radioOLED.grid(column=startColumn+2,row=startRow)
        self.radioLite = ttk.Radiobutton(self.frame, text="Lite", value="Lite", variable=self.switchType,command=self.RadioChanged)
        self.radioLite.grid(column=startColumn+3,row=startRow)
        self.storageSize = StringVar(value="32 GB")
        self.model = StringVar(value="HAC-001(-01)")
        self.storageLabel = ttk.Label(self.frame, text="Storage: 32 GB")
        self.RadioChanged()
        self.storageLabel.grid(column=startColumn+4, row=startRow)

        ttk.Label(self.frame,text="PO").grid(column=startColumn,row=startRow+1)
        ttk.Entry(self.frame,textvariable=self.po).grid(column=startColumn+1,row=startRow+1)
        ttk.Label(self.frame,text="Initials").grid(column=startColumn+3,row=startRow+1)
        ttk.Entry(self.frame,textvariable=self.initials).grid(column=startColumn+4,row=startRow+1)

        ttk.Label(self.frame, text="").grid(column=startColumn,row=startRow+2)

        ttk.Label(self.frame, text="Color").grid(column=startColumn+1, row=startRow+3)
        self.color = StringVar(value="Black")
        self.colorEntry = ttk.Entry(self.frame, textvariable=self.color)
        self.colorEntry.grid(column=startColumn+1, row=startRow+4)
        ttk.Label(self.frame,text="S/N:").grid(column=startColumn+2, row=startRow+3)
        self.sn = StringVar()
        self.serialEntry = ttk.Entry(self.frame, textvariable=self.sn)
        self.serialEntry.grid(column=startColumn+3,row=startRow+3)
        self.root.protocol("WM_TAKE_FOCUS", self.WindowFocused)
        self.clearSN = BooleanVar()
        ttk.Label(self.frame, text="Clear After Print").grid(column=startColumn+4, row=startRow+3)
        self.clearButton = ttk.Checkbutton(self.frame, variable=self.clearSN)
        self.clearButton.grid(column=startColumn+4, row=startRow+4)

        self.DisplayPrintButton(startColumn+3, startRow+8)
        
        self.Load()
    
    def RadioChanged(self):
        if self.switchType.get() == "Normal":
            self.storageSize.set("32 GB")
            self.model.set("HAC-001(-01)")
        elif self.switchType.get() == "Lite":
            self.storageSize.set("32 GB")
            self.model.set("HDH-001")
        else:
            self.storageSize.set("64 GB")
            self.model.set("HEG-001")

        self.storageLabel.configure(text="Storage: " + self.storageSize.get() + '\n' + "Model: " + self.model.get())
    
    def SetLabelData(self):
        self.l = zpl.Label(self.height,self.width, 11.8)
        self.l.origin(1,4)
        #self.l.write_text(concat, char_height=4.2, char_width=4, line_width=45, justification='L')
        TextBoxResize(self.l, "S/N: " + self.sn.get(), self.width, self.height)
        self.l.endorigin()
        self.l.origin(1, 8)
        self.l.zpl_raw("^BY2")
        self.l.barcode('C', self.sn.get(), height=60, mode='A')
        self.l.endorigin()
        self.l.origin(4,19)
        self.l.write_text("PO: " + self.po.get(), char_height=3, char_width=3, line_width=30, justification='L')
        self.l.endorigin()
        self.l.origin(37,19)
        self.l.write_text(self.initials.get().upper(), char_height=4, char_width=4, line_width=30, justification='L')
        self.l.endorigin()
    
    def SetSwitchData(self):
        self.switchL = zpl.Label(self.height,self.width, 11.8)
        self.switchL.origin(1,4)
        self.switchL.write_text("Initials: " + self.initials.get().upper(), char_height=3, char_width=3, line_width=60, justification='L')
        self.switchL.endorigin()
        self.switchL.origin(1,7)
        self.switchL.write_text("PO: " + self.po.get(), char_height=3, char_width=3, line_width=30, justification='L')
        self.switchL.endorigin()
        self.switchL.origin(1,10)
        self.switchL.write_text("Storage: " + self.storageSize.get(), char_height=3, char_width=3, line_width=30, justification='L')
        self.switchL.endorigin()
        self.switchL.origin(1,13)
        self.switchL.write_text("Model: " + self.model.get(), char_height=3, char_width=3, line_width=30, justification='L')
        self.switchL.endorigin()
        self.switchL.origin(1,16)
        self.switchL.write_text("Color: " + self.color.get(), char_height=3, char_width=3, line_width=30, justification='L')
        self.switchL.endorigin()

    def GetPrintData(self, setData :bool = True) -> str:
        super()
        if setData:
            self.SetLabelData()
            self.SetSwitchData()
        data = self.switchL.dumpZPL()
        #print(data)
        return self.l.dumpZPL() + self.switchL.dumpZPL()
    
    def PrintTrigger(self):
        super().PrintTrigger()
        if self.clearSN.get() == True:
            self.sn.set("")
    
    def Load(self, loadOverride : dict = None):
        super().Load(loadOverride=loadOverride)
        loadDict : dict = {}
        if loadOverride:
            loadDict = loadOverride
        else:
            if self.hasSave:
                loadDict = self.saveData

        if len(loadDict.items()) > 0:
            keys = loadDict.keys()
            if "switchType" in keys:
                self.switchType.set(loadDict["switchType"])
                self.RadioChanged()
            if "color" in keys:
                self.color.set(loadDict["color"])
            if "po" in keys:
                self.po.set(loadDict["po"])
            if "initials" in keys:
                self.initials.set(loadDict["initials"])
            if "serial" in keys:
                self.sn.set(loadDict["serial"])
            if "clear" in keys:
                self.clearSN.set(loadDict["clear"])
        return
    
    def Save(self) -> dict:
        saveDict : dict = super().Save()
        saveDict["switchType"] = self.switchType.get()
        saveDict["color"] = self.color.get()
        saveDict["po"] = self.po.get()
        saveDict["initials"] = self.initials.get()
        saveDict["serial"] = self.sn.get()
        saveDict["clear"] = self.clearSN.get()
        return saveDict