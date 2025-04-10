from GlobalImport import *
from PrintPassing import PrintPassing

class CustomLabel:

    testObserve = PrintPassing
    l : zpl.Label
    width : float
    height : float
    mm : str = "mm"
    dimensionsLabel : ttk.Label
    root : Tk
    frame : Frame
    filename : str
    hasSave : bool = False
    saveData : dict

    printButton : Button
    count : IntVar
    
    def EnteredPressed(self, event):
        self.PrintTrigger()
    
    def WindowFocused(self, event):
        return
    
    def LabelClosed(self):
        saveDict : dict = self.Save()
        filePath = os.path.join(directory, self.filename)
        saveFile = open(filePath, "w")
        json.dump(saveDict,saveFile)
        self.RecursiveDestroyChildren(self.frame)
        saveFile.close()

    def RecursiveDestroyChildren(self, frameToDestroy : Frame):
        for i in frameToDestroy.winfo_children():
            self.RecursiveDestroyChildren(i)
            i.destroy()
        frameToDestroy.destroy()

    def __init__(self, master, width : float, height : float, mm :str, startColumn : int=0, startRow : int=0) -> None:
        self.width = width
        self.height = height
        self.mm = mm
        self.testObserve = PrintPassing()

        self.root = master
        self.frame = Frame(master=master)
        self.frame.grid(row=startRow, column=startColumn)
        #self.frame = frame
        self.root.bind("<Return>", self.EnteredPressed)
        self.root.bind("<FocusIn>", self.WindowFocused)
        #self.root.wm_protocol("WM_DELETE_WINDOW", self.LabelClosed)
        self.filename = str(self.__class__.__name__) + ".json"
        try:
            os.makedirs(directory, exist_ok=True)
            #print("Created Directory")
        except OSError as error:
            print("Failed to create directory")
        
        filePath = os.path.join(directory, self.filename)
        if os.path.exists(filePath):
            self.hasSave = True
            with open(filePath, 'r') as loadFile:
                try:
                    self.saveData = json.load(loadFile)
                except json.JSONDecodeError as jsonError:
                    print("Corrupt File")
                    os.remove(filePath)


    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        self.Load()
        return
    
    def SetLabelData():
        return
    
    def GetPrintData(self,setData :bool = True) -> str:
        return ""

    def SetWidth(self,width):
        self.width = width
    
    def SetHeight(self,height):
        self.height = height

    def SetUnit(self,_mm : str):
        self.mm = _mm
        try:
            self.dimensionsLabel.configure(text=self.DimensionText())
        except:
            pass

    def DisplayPrintButton(self, _column : int = 1, _row : int = 0, frameOverride = None):
        if frameOverride is None:
            frameOverride = self.frame
        self.printButton = Button(frameOverride, text="Print", command=self.PrintTrigger)
        self.printButton.grid(column=_column, row=_row)
        Label(frameOverride, text="Count").grid(column=_column-1, row=_row+1)
        self.count = IntVar(None, 1)
        Entry(frameOverride, textvariable=self.count).grid(column=_column, row=_row+1)
        self.dimensionsLabel = Label(frameOverride, text=self.DimensionText())
        self.dimensionsLabel.grid(column=_column, row=_row+2)
    
    def DimensionText(self) -> str:
        adjustedW : float = self.width
        adjustedH : float = self.height
        if self.mm == "in":
            adjustedW /= 25.4
            adjustedH /= 25.4
        return "Label Size: " + str(adjustedW) + " x " + str(adjustedH) + " " + self.mm

    def PrintTrigger(self):
        for i in range(self.count.get()):
            self.testObserve.CallFunc()

    def Load(self, loadOverride : dict = None):
        loadDict : dict = {}
        if loadOverride:
            loadDict = loadOverride
        else:
            if self.hasSave:
                loadDict = self.saveData
        
        if len(loadDict.items()) > 0:
            keys = loadDict.keys()
            if "width" in keys:
                self.width = loadDict["width"]
            if "height" in keys:
                self.height = loadDict["height"]
            if "unit" in keys:
                self.mm = loadDict["unit"]
        return
    
    def Save(self) -> dict:
        tempDict : dict = {"width" : self.width, "height" : self.height, "unit" : self.mm}
        return tempDict
