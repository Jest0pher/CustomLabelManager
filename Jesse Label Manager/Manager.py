from GlobalImport import *
from IndividualLabels import *
from Printers import ZebraPrinter

class LabelManager:
    root : Tk
    frame : ttk.Frame
    labelPrinter : ZebraPrinter
    queues = []
    currentPrinter : StringVar
    currentButton : StringVar
    previousButtonID : int = -1
    widthLabel : ttk.Label
    heightLabel : ttk.Label
    wEntry : StringVar
    hEntry : StringVar
    labelWidth : float = 50.8 #Always in mm
    labelHeight : float = 25.4 #Always in mm
    units : StringVar
    radioInch : Radiobutton
    radioMM : Radiobutton
    filename :  str

    def __init__(self):
        self.root = Tk()
        self.labelPrinter = ZebraPrinter()
        self.root.title("Custom Print Manager")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.CloseWindow)
        self.frame = Frame(self.root,padx=10, pady=10)
        self.frame.grid()
        ttk.Label(self.frame, text="").grid(row=0, column=0)
        self.queues = self.labelPrinter.z.getqueues()
        self.currentPrinter = StringVar(self.root, self.queues[0])
        self.labelPrinter.SetCurrentPrinter(self.currentPrinter.get())
        ttk.Label(self.frame, text="Selected Printer:").grid(column=0,row=1)
        ttk.OptionMenu(self.frame, self.currentPrinter, self.queues[0], *self.queues, command=self.labelPrinter.SetCurrentPrinter).grid(column=0,row=2)
        ttk.Label(self.frame, text="Label Size:").grid(column=0,row=3)
        sizeFrame = Frame(self.frame)
        sizeFrame.grid(column=0,row=4)
        self.widthLabel = ttk.Label(sizeFrame, text="Width(mm)")
        self.widthLabel.grid(column=0,row=0)
        self.wEntry = StringVar(value=str(self.labelWidth))
        ttk.Entry(sizeFrame, textvariable=self.wEntry).grid(column=1, row=0)
        self.heightLabel = ttk.Label(sizeFrame, text="Height(mm)")
        self.heightLabel.grid(column=0,row=1)
        self.hEntry = StringVar(value=str(self.labelHeight))
        ttk.Entry(sizeFrame, textvariable=self.hEntry).grid(column=1, row=1)
        ttk.Button(self.frame, text="Update Label Size", command=self.UpdateLabelSize).grid(column=0, row=5)
        unitFrame = Frame(self.frame)
        unitFrame.grid(column=0, row=6)
        self.units = StringVar(value="mm")
        self.radioMM = ttk.Radiobutton(unitFrame, text = "mm", value="mm", variable=self.units, command=self.UnitsPressed)
        self.radioMM.grid(column=0,row=0)
        self.radioInch = ttk.Radiobutton(unitFrame, text = "in", value="in", variable=self.units, command=self.UnitsPressed)
        self.radioInch.grid(column=1,row=0)
        
        currentRow = 7
        ttk.Label(self.frame, text="                  ").grid(column=0, row=currentRow) #Spacer
        ttk.Label(self.frame, text="Label Types:").grid(column=0, row=currentRow+1) #Spacer
        ttk.Label(self.frame, text="                  ").grid(column=0, row=currentRow+2) #Spacer
        
        currentRow += 3
        #Button ID
        #0-Serial
        #1-QTY
        #2-Switch
        #3-Text

        self.currentButton = StringVar(value='-1')
        serialButton = Radiobutton(self.frame, text="Serial Label", value='0', variable=self.currentButton, command=self.CreateSerialLabel)
        serialButton.grid(column=0,row=currentRow)
        #test = Radiobutton(self.frame, text="Test", value='1', variable=self.currentButton, command=self.TestFunc)
        #test.grid(column=0,row=currentRow+1)

        qtyButton = Radiobutton(self.frame, text="Quantity", value='1', variable=self.currentButton, command=self.CreateQTYLabel)
        qtyButton.grid(column=0,row=currentRow+1)

        switchButton = Radiobutton(self.frame, text="Switch", value='2', variable=self.currentButton, command=self.CreateSwitchLabel)
        switchButton.grid(column=0,row=currentRow+2)

        watchButton = Radiobutton(self.frame, text="Watch", value='3', variable=self.currentButton, command=self.CreateWatchLabel)
        watchButton.grid(column=0,row=currentRow+3)
        
        switchButton = Radiobutton(self.frame, text="Text", value='4', variable=self.currentButton, command=self.CreateTextLabel)
        switchButton.grid(column=0,row=currentRow+4)

        #self.buttons = [serialButton, qtyButton]


        self.filename = "LabelManager.json"
        saveData : dict = {}
        try:
            os.makedirs(directory, exist_ok=True)
            #print("Created Directory")
        except OSError as error:
            print("Failed to create directory")
        
        filePath = os.path.join(directory, self.filename)
        if os.path.exists(filePath):
            with open(filePath, 'r') as loadFile:
                try:
                    saveData = json.load(loadFile)
                except json.JSONDecodeError as jsonError:
                    print("Corrupt File")
                    os.remove(filePath)
        self.Load(saveData)
        self.root.mainloop()

    def CreateSerialLabel(self):
        self.UpdateLabelSize()
        if self.ToggleButton(0):
            serialLabel = SerialLabel(self.root, width=self.labelWidth, height=self.labelHeight, mm=self.units.get(), startRow=0, startColumn=2)
            self.labelPrinter.SetLabel(serialLabel)
    
    def CreateQTYLabel(self):
        self.UpdateLabelSize
        if self.ToggleButton(1):
            qtyLabel = QTYLabel(self.root, width=self.labelWidth, height=self.labelHeight, mm=self.units.get(),startRow=0, startColumn=2)
            self.labelPrinter.SetLabel(qtyLabel)
        
    def CreateSwitchLabel(self):
        self.UpdateLabelSize()
        if self.ToggleButton(2):
            switchLabel = SwitchLabel(self.root, width=self.labelWidth, height=self.labelHeight, mm=self.units.get(),startRow=0, startColumn=2)
            self.labelPrinter.SetLabel(switchLabel)
    
    def CreateWatchLabel(self):
        self.UpdateLabelSize()
        if self.ToggleButton(3):
            watchLabel = WatchLabel(self.root, width=self.labelWidth, height=self.labelHeight, mm=self.units.get(),startRow=0, startColumn=2)
            self.labelPrinter.SetLabel(watchLabel)

    def CreateTextLabel(self):
        self.UpdateLabelSize()
        if self.ToggleButton(4):
            textLabel = TextLabel(self.root, width=self.labelWidth, height=self.labelHeight, mm=self.units.get(), startRow=0, startColumn=2)
            self.labelPrinter.SetLabel(textLabel)
    #def TestFunc(self):
    #    if self.ToggleButton(1):
    #        print("test")
    
    def UpdateLabelSize(self): #Updates float value using entry values. Make sure always updated. Or convert from string every time its used?
        try:
            self.labelWidth = float(self.wEntry.get())
            self.labelHeight = float(self.hEntry.get())
            self.widthLabel.configure(text="Width(" + self.units.get() + ')')
            self.heightLabel.configure(text="Height(" + self.units.get() + ')')
            if self.units.get() == "in":
                self.labelWidth *= 25.4
                self.labelHeight *= 25.4
            else:
                pass
            self.labelPrinter.label.SetWidth(self.labelWidth)
            self.labelPrinter.label.SetHeight(self.labelHeight)
            self.labelPrinter.label.SetUnit(self.units.get())
        except ValueError:
            print("ERROR: Check your input")
        except AttributeError:
            print("Size updated. No label initialized")
        except Exception as err:
            print(str(type(err)))

    def UnitsPressed(self):
        self.UpdateLabelSize()

    def RemoveCurrentLabel(self):
        try:
            self.labelPrinter.label.LabelClosed()
            self.labelPrinter.label = None
        except:
            print("Closing error")

    def ToggleButton(self, buttonID : int) -> bool:
        if buttonID == self.previousButtonID:
            return False

        self.RemoveCurrentLabel()
        self.previousButtonID = buttonID
        return True

    def CloseWindow(self):
        self.UpdateLabelSize()
        filePath = os.path.join(directory, self.filename)
        saveFile = open(filePath, "w")
        saveDict : dict = self.Save()
        json.dump(saveDict,saveFile)
        saveFile.close()

        try:
            self.labelPrinter.label.LabelClosed()
        except:
            pass
        self.frame.destroy()
        self.root.destroy()
    
    def Save(self) -> dict:
        return {"labelw" : self.labelWidth, "labelh" : self.labelHeight, "units" : self.units.get()}
    
    def Load(self,loadDict : dict):
        keys = loadDict.keys()
        if "units" in keys:
            self.units.set(loadDict["units"])
        if "labelw" in keys:
            self.labelWidth = loadDict["labelw"]
            if self.units.get() == "in":
                self.wEntry.set(str(self.labelWidth/25.4))
            else:
                self.wEntry.set(str(self.labelWidth))
        if "labelh" in keys:
            self.labelHeight = loadDict["labelh"]
            if self.units.get() == "in":
                self.hEntry.set(str(self.labelHeight/25.4))
            else:
                self.hEntry.set(str(self.labelHeight))
        self.UpdateLabelSize()