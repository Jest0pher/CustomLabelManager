from GlobalImport import *
from Custom import CustomLabel

class TextLabel(CustomLabel):
    texts = []
    clears = []
    textHeight = 3.5
    characterLimit = 28
    labels = []
    saveStartColumn = 2
    lineNum = []
    entries = []
    checkBoxes = []
    removeButtons = []
    reg = None
    entryFrame : Frame
    clearFrame : Frame
    reversePrint : BooleanVar
    
    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, mm=mm, height=height, startColumn=startColumn, startRow=startRow)
        self.saveStartColumn = startColumn
        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def EntryValidate(self, stringVar : str) -> bool:
        if stringVar.__len__() > self.characterLimit:
            return False
        return True

    def ConstructWindow(self, startColumn : int=saveStartColumn, startRow : int=0):
        self.frame = Frame(self.root)
        self.frame.grid(row=startRow, column=startColumn)
        self.reg = self.frame.register(self.EntryValidate)
        buttonFrame = Frame(self.frame)
        buttonFrame.grid(row=startRow, column=startColumn)
        ttk.Button(buttonFrame, text="Add Line", command=self.AddLine).grid(row=startRow, column=startColumn)
        ttk.Button(buttonFrame, text="Remove Last", command=self.RemoveLastLine).grid(row=startRow, column=startColumn+1)
        ttk.Button(buttonFrame, text="Clear All", command=self.ClearAllLines).grid(row=startRow, column=startColumn+2)
        ttk.Button(buttonFrame, text="Reset", command=self.Reset).grid(row=startRow, column=startColumn+3)
        startRow += 1
        self.entryFrame = Frame(self.frame)
        self.entryFrame.grid(row=startRow+1, column=startColumn)
        ttk.Label(self.entryFrame, text="#").grid(row=0, column=0)
        ttk.Label(self.entryFrame, text="Text Line").grid(row=0, column=1)
        ttk.Button(self.entryFrame, text="Toggle Clear", command=self.ToggleClears).grid(row=0, column=2)
        ttk.Label(self.entryFrame, text="Remove").grid(row=0, column=3)
        for i in range(5):
            self.AddLine()
        reverseFrame = Frame(self.frame)
        reverseFrame.grid(row=startRow+self.entries.__len__()+1, column=startColumn)
        self.reversePrint = BooleanVar(value=False)
        ttk.Checkbutton(reverseFrame, text="Reverse Label Order", variable=self.reversePrint).grid(row=0, column=0)
        ttk.Label(self.frame,text="").grid(row=startRow+self.entries.__len__()+2,column=startColumn)
        self.DisplayPrintButton(startColumn, startRow+self.entries.__len__()+3)

        self.Load()

    def AddLine(self):
        rowOffset = 1 #Manually set because of header line
        lineID = ttk.Label(self.entryFrame, text=self.lineNum.__len__()+1)
        lineID.grid(row=rowOffset+self.lineNum.__len__(), column=0)
        self.lineNum.append(lineID)

        self.texts.append(StringVar(value=""))
        entry = ttk.Entry(self.entryFrame, textvariable=self.texts[self.texts.__len__()-1],width=28, validate="key", validatecommand=(self.reg, '%P'))
        entry.grid(row=self.entries.__len__()+rowOffset, column=1)
        self.entries.append(entry)
        
        self.clears.append(BooleanVar(value=False))
        checkBox = ttk.Checkbutton(self.entryFrame, variable=self.clears[self.clears.__len__()-1])
        checkBox.grid(row=self.checkBoxes.__len__()+rowOffset, column=2)
        self.checkBoxes.append(checkBox)
        
        index = self.removeButtons.__len__()
        button = ttk.Button(self.entryFrame, text="Remove " + str(self.removeButtons.__len__()+1), command=lambda: self.RemoveLine(index))
        button.grid(row=self.removeButtons.__len__()+rowOffset, column=3)
        self.removeButtons.append(button)

        for i in self.entries:
            i.lift()
        for i in self.checkBoxes:
            i.lift()
        for i in self.removeButtons:
            i.lift()

    def RemoveLastLine(self):
        self.RemoveLine(-1)

    def ClearAllLines(self):
        for i in self.texts:
            i.set("")

    def RemoveLine(self, index : int):
        if self.lineNum.__len__() > 1:
            self.lineNum[index].destroy()
            self.lineNum.pop(index)
            self.entries[index].destroy()
            self.entries.pop(index)
            self.checkBoxes[index].destroy()
            self.checkBoxes.pop(index)
            self.removeButtons[index].destroy()
            self.removeButtons.pop(index)

            self.texts.pop(index)
            self.clears.pop(index)

            for i in range(self.lineNum.__len__()):
                self.lineNum[i].configure(text=str(i+1))
                if i >= index and index != -1:
                    self.lineNum[i].grid_configure(row=self.lineNum[i].grid_info()['row']-1)

            for i in range(self.entries.__len__()):
                if i >= index and index != -1:
                    self.entries[i].grid_configure(row=self.entries[i].grid_info()['row']-1)
            
            for i in range(self.checkBoxes.__len__()):
                if i >= index and index != -1:
                    self.checkBoxes[i].grid_configure(row=self.checkBoxes[i].grid_info()['row']-1)
                
            for i in range(self.removeButtons.__len__()):
                self.removeButtons[i].configure(text="Remove " + str(i+1), command=lambda: self.RemoveLine(i))
                if i >= index and index != -1:
                    self.removeButtons[i].grid_configure(row=self.removeButtons[i].grid_info()['row']-1)
            

    def ClearAll(self):
        self.texts.clear()
        self.clears.clear()
        for i in self.entries:
            i.destroy()
        self.entries.clear()
        for i in self.checkBoxes:
            i.destroy()
        self.checkBoxes.clear()
        for i in self.lineNum:
            i.destroy()
        self.lineNum.clear()
        for i in self.removeButtons:
            i.destroy()
        self.removeButtons.clear()
        self.labels.clear()

        self.reversePrint.set(False)

    def Reset(self):
        self.ClearAll()
        for i in range(5):
            self.AddLine()
    
    def ToggleClears(self):
        hasFalse : bool = False
        hasTrue : bool = False
        for i in self.clears:
            if i.get() == True:
                hasTrue = True
            elif i.get() == False:
                hasFalse = True
            
            if hasFalse == True and hasTrue == True:
                for j in self.clears:
                    j.set(False)
                return
        if hasFalse == True and hasTrue == False:
            for i in self.clears:
                i.set(True)
        elif hasTrue == True and hasFalse == False:
            for i in self.clears:
                i.set(False)

    def LabelClosed(self):
        super().LabelClosed()
        self.ClearAll()

    def SetLabelData(self):
        #self.l = zpl.Label(self.height,self.width, 11.8)
        self.labels.clear()
        numLabels = int(self.texts.__len__()/5)
        try:
            numLabels += (self.texts.__len__() % 5) / (self.texts.__len__() % 5)
        except:
            pass
        for offset in range(int(numLabels)):
            label = zpl.Label(self.height,self.width, 11.8)
            originY = 3
            for i in range(5):
                index = 5*offset + i
                if index >= self.texts.__len__():
                    break
                label.origin(2, originY)
                TextBoxResize(label, self.texts[index].get(),self.width, self.height)
                label.endorigin()
                originY += 5
            self.labels.append(label)

    def GetPrintData(self, setData :bool = True) -> str:
        super()
        if setData:
            self.SetLabelData()
        
        returnZPL = ""
        labelsIndicies = range(self.labels.__len__())
        if self.reversePrint.get() == False:
            labelsIndicies = labelsIndicies.__reversed__()
        for i in labelsIndicies:
            returnZPL += self.labels[i].dumpZPL()
        return returnZPL
    
    def PrintTrigger(self):
        super().PrintTrigger()
        for i in range(self.clears.__len__()):
            if self.clears[i].get():
                self.texts[i].set("")

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
            if "lines" in keys and "clear" in keys:
                if loadDict["lines"].__len__() > 0:
                    while self.texts.__len__() != loadDict["lines"].__len__():
                        if self.texts.__len__() < loadDict["lines"].__len__():
                            self.AddLine()
                        else:
                            self.RemoveLastLine()

                    for i in range(loadDict["lines"].__len__()):
                        self.texts[i].set(loadDict["lines"][i])
                        self.clears[i].set(loadDict["clear"][i])
            if "reverse" in keys:
                self.reversePrint.set(loadDict["reverse"])
        return
    
    def Save(self) -> dict:
        saveDict : dict = {}
        clearArr = []
        stringArr = []
        for i in range(self.texts.__len__()):
            stringArr.append(self.texts[i].get())
            if i < self.clears.__len__():
                clearArr.append(self.clears[i].get())
        saveDict["lines"] = stringArr
        saveDict["clear"] = clearArr
        saveDict["reverse"] = self.reversePrint.get()
        return saveDict