from GlobalImport import *
from Custom import CustomLabel

class WatchLabel(CustomLabel):
    po : StringVar
    brand : StringVar
    model : StringVar
    devColor : StringVar
    bandColor : StringVar
    screenSize : StringVar

    connectType : StringVar
    radioLTE : Radiobutton
    radioWifi : Radiobutton

    prefix : StringVar

    printSerial : BooleanVar

    serialLabel : ttk.Label
    sn : StringVar
    serialEntry : ttk.Entry
    initials : StringVar
    clearSN : BooleanVar
    previousSerial : StringVar
    prevSerialLabel : ttk.Label

    serialFrame : Frame
    watchFrame : Frame
    countFrame : Frame
    watchL : zpl.Label
    serialL : zpl.Label

    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, height=height, mm=mm,startColumn=startColumn, startRow=startRow)
        self.initials = StringVar(value=initials)
        self.po = StringVar(value=po)

        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        self.serialFrame = Frame(self.frame)
        self.serialFrame.grid(row=startRow, column=startColumn)
        self.prefix = StringVar(value="S/N")

        ttk.Label(self.serialFrame,text="PO").grid(column=startColumn,row=startRow+1)
        ttk.Entry(self.serialFrame,textvariable=self.po).grid(column=startColumn+1,row=startRow+1)
        ttk.Label(self.serialFrame,text="Initials").grid(column=startColumn+3,row=startRow+1)
        ttk.Entry(self.serialFrame,textvariable=self.initials).grid(column=startColumn+4,row=startRow+1)

        ttk.Label(self.serialFrame, text="").grid(column=startColumn,row=startRow+2)

        ttk.Label(self.serialFrame, text="Model:").grid(column=startColumn, row=startRow+3)
        self.model = StringVar()
        modelEntry = ttk.Entry(self.serialFrame, textvariable=self.model)
        modelEntry.grid(column=startColumn+1, row=startRow+3)
        self.serialLabel = ttk.Label(self.serialFrame,text=self.prefix.get())
        self.serialLabel.grid(column=startColumn+2, row=startRow+3)
        self.sn = StringVar()
        self.serialEntry = ttk.Entry(self.serialFrame, textvariable=self.sn)
        self.serialEntry.grid(column=startColumn+3,row=startRow+3)
        self.root.protocol("WM_TAKE_FOCUS", self.WindowFocused)
        self.clearSN = BooleanVar()
        ttk.Label(self.serialFrame, text="Clear After Print").grid(column=startColumn+4, row=startRow+3)
        self.clearButton = ttk.Checkbutton(self.serialFrame, variable=self.clearSN)
        self.clearButton.grid(column=startColumn+4, row=startRow+4)
        self.previousSerial = StringVar()
        ttk.Label(self.serialFrame, text="Previous:").grid(column=startColumn+2, row=startRow+4)
        self.prevSerialLabel = ttk.Label(self.serialFrame, textvariable=self.previousSerial)
        self.prevSerialLabel.grid(column=startColumn+3,row=startRow+4)
        ttk.Button(self.serialFrame, text="Paste Previous Entry", command=self.PastePreviousPressed).grid(column=startColumn+3, row=startRow+5)
        ttk.Label(self.serialFrame, text="Print Serial").grid(row=startRow+6, column=startColumn+2)
        self.printSerial = BooleanVar(value=True)
        ttk.Checkbutton(self.serialFrame, variable=self.printSerial).grid(row=startRow+6, column=startColumn+3)
        ttk.Label(self.serialFrame, text="").grid(column=startColumn,row=startRow+6)
        
        self.watchFrame = Frame(self.frame)
        self.watchFrame.grid(row=startRow+1, column=startColumn)
        self.connectType = StringVar(value="Wifi")
        self.radioLTE = ttk.Radiobutton(self.watchFrame, text="LTE", value="LTE", variable=self.connectType,command=self.RadioChanged)
        self.radioLTE.grid(row=startRow, column=startColumn)
        self.radioWifi = ttk.Radiobutton(self.watchFrame, text="Wifi", value="Wifi", variable=self.connectType, command=self.RadioChanged)
        self.radioWifi.grid(row=startRow+1, column=startColumn)
        ttk.Label(self.watchFrame, text="   |   ").grid(row=startRow, column=startColumn+1)
        ttk.Label(self.watchFrame, text="   |   ").grid(row=startRow+1, column=startColumn+1)
        ttk.Label(self.watchFrame, text="Brand").grid(row=startRow, column=startColumn+2)
        ttk.Label(self.watchFrame, text="Screen Size").grid(row=startRow+1, column=startColumn+2)
        self.brand = StringVar()
        self.screenSize = StringVar()
        ttk.Entry(self.watchFrame, textvariable=self.brand).grid(row=startRow, column=startColumn+3)
        ttk.Entry(self.watchFrame, textvariable=self.screenSize).grid(row=startRow+1, column=startColumn+3)
        ttk.Label(self.watchFrame, text="   |   ").grid(row=startRow, column=startColumn+4)
        ttk.Label(self.watchFrame, text="   |   ").grid(row=startRow+1, column=startColumn+4)
        ttk.Label(self.watchFrame, text="Device Color").grid(row=startRow, column=startColumn+5)
        ttk.Label(self.watchFrame, text="Band Color").grid(row=startRow+1, column=startColumn+5)
        self.devColor = StringVar()
        self.bandColor = StringVar()
        ttk.Entry(self.watchFrame, textvariable=self.devColor).grid(row=startRow, column=startColumn+6)
        ttk.Entry(self.watchFrame, textvariable=self.bandColor).grid(row=startRow+1, column=startColumn+6)

        self.countFrame = Frame(self.frame)
        self.countFrame.grid(row=startRow+2, column=startColumn)

        self.DisplayPrintButton(startColumn, startRow, self.countFrame)

        self.Load()
    
    def RadioChanged(self):
        if self.connectType.get() == "LTE":
            self.prefix.set(value="IMEI")
        else:
            self.prefix.set(value="S/N")
        self.serialLabel.configure(text=self.prefix.get())

    def PastePreviousPressed(self):
        self.sn.set(self.previousSerial.get())

    def SetLabelData(self):
        self.serialL = zpl.Label(self.height,self.width, 11.8)
        self.serialL.origin(1,4)
        #self.l.write_text(concat, char_height=4.2, char_width=4, line_width=45, justification='L')
        TextBoxResize(self.serialL, "S/N: " + self.sn.get(), self.width, self.height)
        self.serialL.endorigin()
        self.serialL.origin(3, 8)
        self.serialL.zpl_raw("^BY2")
        self.serialL.barcode('C', self.sn.get(), height=60, mode='A')
        self.serialL.endorigin()
        self.serialL.origin(4,19)
        self.serialL.write_text("PO: " + self.po.get(), char_height=3, char_width=3, line_width=30, justification='L')
        self.serialL.endorigin()
        self.serialL.origin(37,19)
        self.serialL.write_text(self.initials.get().upper(), char_height=4, char_width=4, line_width=30, justification='L')
        self.serialL.endorigin()

    def SetWatchData(self):
        self.watchL = zpl.Label(self.height, self.width, 11.8)
        self.watchL.origin(1,4)
        self.watchL.write_text("PO: " + self.po.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()
        self.watchL.origin(1,7)
        self.watchL.write_text("Brand: " + self.brand.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()
        self.watchL.origin(1,10)
        self.watchL.write_text("Model: " + self.model.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()
        self.watchL.origin(1,13)
        self.watchL.write_text("Device Color: " + self.devColor.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()
        self.watchL.origin(1,16)
        self.watchL.write_text("Band Color: " + self.bandColor.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()
        self.watchL.origin(1,19)
        self.watchL.write_text("Carrier: " + self.connectType.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()
        self.watchL.origin(1,22)
        self.watchL.write_text("Screen Size: " + self.screenSize.get(), char_height=3, char_width=3, line_width=60, justification='L')
        self.watchL.endorigin()

    def GetPrintData(self, setData = True):
        super().GetPrintData(setData)
        if setData:
            self.SetLabelData()
            self.SetWatchData()
        if self.printSerial.get():
            return self.serialL.dumpZPL() + self.watchL.dumpZPL()
        else:
            return self.watchL.dumpZPL()
    
    def PrintTrigger(self):
        super().PrintTrigger()
        self.previousSerial.set(self.sn.get())
        if self.clearSN.get() == True:
            self.sn.set("")
        self.serialEntry.focus_set()
    
    def Load(self, loadOverride = None):
        super().Load(loadOverride=loadOverride)
        loadDict : dict = {}
        if loadOverride:
            loadDict = loadOverride
        else:
            if self.hasSave:
                loadDict = self.saveData

        if len(loadDict.items()) > 0:
            keys = loadDict.keys()
            if "serial" in keys:
                self.sn.set(value=loadDict["serial"])
            if "po" in keys:
                self.po.set(value=loadDict["po"])
            if "model" in keys:
                self.model.set(value=loadDict["model"])
            if "initials" in keys:
                self.initials.set(value=loadDict["initials"])
            if "brand" in keys:
                self.brand.set(value=loadDict["brand"])
            if "screenSize" in keys:
                self.screenSize.set(value=loadDict["screenSize"])
            if "devColor" in keys:
                self.devColor.set(value=loadDict["devColor"])
            if "bandColor" in keys:
                self.bandColor.set(value=loadDict["bandColor"])
            if "clearSN" in keys:
                self.clearSN.set(value=loadDict["clearSN"])
            if "printSerial" in keys:
                self.printSerial.set(value=loadDict["printSerial"])
            if "carrier" in keys:
                self.connectType.set(value=loadDict["carrier"])
                self.RadioChanged()
            if "previous" in keys:
                self.previousSerial.set(value=loadDict["previous"])
            
    
    def Save(self):
        saveDict : dict = super().Save()
        saveDict["serial"] = self.sn.get()
        saveDict["po"] = self.po.get()
        saveDict["brand"] = self.brand.get()
        saveDict["model"] = self.model.get()
        saveDict["devColor"] = self.devColor.get()
        saveDict["bandColor"] = self.bandColor.get()
        saveDict["carrier"] = self.connectType.get()
        saveDict["screenSize"] = self.screenSize.get()
        saveDict["clearSN"] = self.clearSN.get()
        saveDict["printSerial"] = self.printSerial.get()
        saveDict["initials"] = self.initials.get()
        saveDict["previous"] = self.previousSerial.get()
        return saveDict