import csv

from GlobalImport import *
from Custom import CustomLabel
from playsound import playsound

class ManifestChecker(CustomLabel):
    
    headers = []
    caseFunctionality = []
    caseSerials = []
    caseDefects = []
    leftFunctionality = []
    leftSerials = []
    leftDefects = []
    rightFunctionality = []
    rightSerials = []
    rightDefects = []

    
    importFrame : ttk.Frame
    checkerFrame : ttk.Frame
    checkerControlsFrame : ttk.Frame
    checkerListFrame : ttk.Frame
    checkerOutputFrame : ttk.Frame
    checkerCurrentFrame : ttk.Frame
    listFrame : ttk.Frame

    importButton : ttk.Button
    importString : StringVar
    importEntry : ttk.Entry
    importLabelStatus : ttk.Label
    
    listCaseFuncString : StringVar
    listCaseSerialString : StringVar
    listCaseDefectString : StringVar
    listLeftFuncString : StringVar
    listLeftSerialString : StringVar
    listLeftDefectString : StringVar
    listRightFuncString : StringVar
    listRightSerialString : StringVar
    listRightDefectString : StringVar
    listCaseFuncLabel : ttk.Label
    listCaseSerialLabel : ttk.Label
    listCaseDefectLabel : ttk.Label
    listLeftFuncLabel : ttk.Label
    listLeftSerialLabel : ttk.Label
    listLeftDefectLabel : ttk.Label
    listRightFuncLabel : ttk.Label
    listRightSerialLabel : ttk.Label
    listRightDefectLabel : ttk.Label

    FUNCTIONALITY_OPTIONS = ["Fully Functional", "Good Case", "Good Left Bud", "Good Right Bud", "Bad Case", "Bad Left Bud", "Bad Right Bud"]
    functionalityString = StringVar
    functionalityOption = ttk.OptionMenu
    searchButton : ttk.Button
    searchString : StringVar
    searchEntry : ttk.Entry
    resultFrame : ttk.Frame
    resultLabel : ttk.Label
    icloudFrame : ttk.Frame
    icloudLabel : ttk.Label
    #dropdown for functionalities
    #box to color green or red whether scanned serial matches selected functionality
    #text to display defects over green/red box
    #blue box to display if serial is marked with icloud locked
    #text to display icloud lock text over blue box

    currentCountLabel : ttk.Label
    currentCountValue : IntVar
    removePreviousButton : ttk.Button
    removeSelectedButton : ttk.Button
    clearListButton : ttk.Button
    currentListSerials : list
    currentListVar : StringVar
    currentListBox : Listbox

    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, mm=mm, height=height, startColumn=startColumn, startRow=startRow)
        self.initials = StringVar(value=initials)
        self.po = StringVar(value=po)
        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        self.importFrame = ttk.Frame(self.frame,height=self.frame.winfo_height()*0.2)
        self.importFrame.grid(column=startColumn, row=startRow)
        self.checkerFrame = ttk.Frame(self.frame,height=self.frame.winfo_height()*0.8)
        self.checkerFrame.grid(column=startColumn, row=startRow+1)

        self.importString = StringVar()
        self.importButton = ttk.Button(self.importFrame, text="Import", command=lambda: self.ImportManifestData(self.importString.get()))
        self.importButton.grid(column=0, row=0)
        self.importEntry = ttk.Entry(self.importFrame, textvariable=self.importString)
        self.importEntry.grid(column=1, row=0)
        self.importLabelStatus = ttk.Label(self.importFrame, text="")
        self.importLabelStatus.grid(column=2, row=0)

        self.checkerControlsFrame = ttk.Frame(self.checkerFrame)
        self.checkerControlsFrame.grid(column=0, row=0)
        self.functionalityString = StringVar(value=self.FUNCTIONALITY_OPTIONS[0])
        self.functionalityOption = ttk.OptionMenu(self.checkerControlsFrame, self.functionalityString, self.functionalityString.get(), *self.FUNCTIONALITY_OPTIONS)
        self.functionalityOption.grid(column=0, row=0)
        self.searchString = StringVar()
        self.searchButton = ttk.Button(self.checkerControlsFrame, text="Search", command=lambda: self.SearchManifest())
        self.searchButton.grid(column=1, row=0)
        self.searchEntry = ttk.Entry(self.checkerControlsFrame, textvariable=self.searchString)
        self.searchEntry.grid(column=2, row=0)


        style = ttk.Style().configure("CustomBackground.TFrame", background="red")
        self.listCaseFuncString = StringVar(value="Fully Functional")
        self.listCaseSerialString = StringVar(value="XXXXXXXXXXXX")
        self.listCaseDefectString = StringVar(value="Case Defect")
        self.listLeftFuncString = StringVar(value="Fully Functional")
        self.listLeftSerialString = StringVar(value="XXXXXXXXXXXX")
        self.listLeftDefectString = StringVar(value="Left Bud Defect")
        self.listRightFuncString = StringVar(value="Fully Functional")
        self.listRightSerialString = StringVar(value="XXXXXXXXXXXX")
        self.listRightDefectString = StringVar(value="Right Bud Defect")
        self.checkerListFrame = ttk.Frame(self.checkerFrame)
        self.checkerListFrame.grid(column=0, row=1)
        self.checkerOutputFrame = ttk.Frame(self.checkerListFrame)
        self.checkerOutputFrame.grid(column=0, row=0)
        self.checkerCurrentFrame = ttk.Frame(self.checkerOutputFrame)
        self.checkerCurrentFrame.grid(column=0, row=0)
        ttk.Label(self.checkerCurrentFrame, text="Case").grid(column=0, row=0)
        ttk.Label(self.checkerCurrentFrame, text="Left Bud").grid(column=1, row=0)
        ttk.Label(self.checkerCurrentFrame, text="Right Bud").grid(column=2, row=0)
        self.listCaseFuncLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listCaseFuncString)
        self.listCaseFuncLabel.grid(column=0, row=1)
        self.listCaseSerialLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listCaseSerialString)
        self.listCaseSerialLabel.grid(column=0, row=2)
        self.listCaseDefectLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listCaseDefectString)
        self.listCaseDefectLabel.grid(column=0, row=3)
        self.listLeftFuncLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listLeftFuncString)
        self.listLeftFuncLabel.grid(column=1, row=1)
        self.listLeftSerialLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listLeftSerialString)
        self.listLeftSerialLabel.grid(column=1, row=2)
        self.listLeftDefectLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listLeftDefectString)
        self.listLeftDefectLabel.grid(column=1, row=3)
        self.listRightFuncLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listRightFuncString)
        self.listRightFuncLabel.grid(column=2, row=1)
        self.listRightSerialLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listRightSerialString)
        self.listRightSerialLabel.grid(column=2, row=2)
        self.listRightDefectLabel = ttk.Label(self.checkerCurrentFrame, textvariable=self.listRightDefectString)
        self.listRightDefectLabel.grid(column=2, row=3)
        self.resultFrame = ttk.Frame(self.checkerOutputFrame)
        self.resultFrame.grid(column=0, row=1)
        self.resultLabel = ttk.Label(self.resultFrame, text="Result", background="green", foreground="black")
        self.resultLabel.grid(column=0, row=0)
        self.icloudFrame = ttk.Frame(self.checkerOutputFrame)
        self.icloudFrame.grid(column=0, row=2)
        self.icloudLabel = ttk.Label(self.icloudFrame, text="iCloud Status", background="blue", foreground="black")
        self.icloudLabel.grid(column=0, row=0)

        self.listFrame = ttk.Frame(self.checkerListFrame)
        self.listFrame.grid(column=1, row=0, rowspan=2)
        self.currentCountValue = IntVar(value=0)
        self.currentCountLabel = ttk.Label(self.listFrame, text="Current Count: " + str(self.currentCountValue.get()))
        self.currentCountLabel.grid(column=0, row=0)
        self.removePreviousButton = ttk.Button(self.listFrame, text="Remove Previous", command=lambda: self.RemovePrevious())
        self.removePreviousButton.grid(column=0, row=1)
        self.removeSelectedButton = ttk.Button(self.listFrame, text="Remove Selected", command=lambda: self.RemoveSelected())
        self.removeSelectedButton.grid(column=0, row=2)
        self.clearListButton = ttk.Button(self.listFrame, text="Clear List", command=lambda: self.ClearList())
        self.clearListButton.grid(column=0, row=3)
        self.currentListSerials = []
        self.currentListVar = StringVar(value=self.currentListSerials)
        self.currentListBox = Listbox(self.listFrame, listvariable=self.currentListVar, selectmode=BROWSE, width=35)
        self.currentListBox.grid(column=0, row=4)

        self.Load()

    def ImportManifestData(self, tsvFilePath : str):
        tsvFilePath = os.path.join(directory, tsvFilePath)
        with open(tsvFilePath, 'r') as tsvFile:
            reader = csv.reader(tsvFile, delimiter='\t')
            rowCount = 0
            for row in reader:
                if rowCount == 0:
                    self.headers = row
                else:
                    if row[self.headers.index("Inspector Initials:")] != "":
                        self.caseFunctionality.append(row[self.headers.index("Functionality Status Case")])
                        self.caseSerials.append(row[self.headers.index("Case Serial Number")])
                        self.caseDefects.append(row[self.headers.index("Case Defect Reason")])
                        self.leftFunctionality.append(row[self.headers.index("Functionality Status Left Bud")])
                        self.leftSerials.append(row[self.headers.index("Left Bud Serial Number")])
                        self.leftDefects.append(row[self.headers.index("Left Bud Defect Reason")])
                        self.rightFunctionality.append(row[self.headers.index("Functionality Status Right Bud")])
                        self.rightSerials.append(row[self.headers.index("Right Bud Serial Number")])
                        self.rightDefects.append(row[self.headers.index("Right Bud Defect Reason")])
                rowCount += 1
        self.importLabelStatus.config(text="Import Complete")
    
    def SearchManifest(self):
        #uses current string in serialEntry
        #clear serial entry after search
        index = -1
        serialToSearch = self.searchString.get().upper()
        match self.functionalityString.get():
            case "Fully Functional":
                if serialToSearch in self.caseSerials:
                    index = self.caseSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.caseFunctionality[index] != "Fully Functional" or self.leftFunctionality[index] != "Fully Functional" or self.rightFunctionality[index] != "Fully Functional":
                        self.SetResult(False, "Not Fully Functional")
                        return
                    else:
                        self.SetResult(True, "Fully Functional")
            case "Good Case":
                if serialToSearch in self.caseSerials:
                    index = self.caseSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.caseFunctionality[index] == "Fully Functional":
                        if self.caseFunctionality[index] == "Fully Functional" and self.leftFunctionality[index] == "Fully Functional" and self.rightFunctionality[index] == "Fully Functional":
                            self.SetResult(False, "Fully Functional")
                            return
                        else:
                            self.SetResult(True, self.caseDefects[index])
                    else:
                        self.SetResult(False, self.caseDefects[index])
                        return
            case "Good Left Bud":
                if serialToSearch in self.leftSerials:
                    index = self.leftSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.leftFunctionality[index] == "Fully Functional":
                        self.SetResult(True, self.leftDefects[index])
                    else:
                        self.SetResult(False, self.leftDefects[index])
                        return
            case "Good Right Bud":
                if serialToSearch in self.rightSerials:
                    index = self.rightSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.rightFunctionality[index] == "Fully Functional":
                        self.SetResult(True, self.rightDefects[index])
                    else:
                        self.SetResult(False, self.rightDefects[index])
                        return
            case "Bad Case":
                if serialToSearch in self.caseSerials:
                    index = self.caseSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.caseFunctionality[index] == "Defective":
                        self.SetResult(True, self.caseDefects[index])
                    else:
                        self.SetResult(False, "Not Bad Case")
                        return
            case "Bad Left Bud":
                if serialToSearch in self.leftSerials:
                    index = self.leftSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.leftFunctionality[index] == "Defective":
                        self.SetResult(True, self.leftDefects[index])
                    else:
                        self.SetResult(False, "Not Bad Left Bud")
                        return
            case "Bad Right Bud":
                if serialToSearch in self.rightSerials:
                    index = self.rightSerials.index(serialToSearch)
                    self.SetCurrentSet(index)
                    if self.rightFunctionality[index] == "Defective":
                        self.SetResult(True, self.rightDefects[index])
                    else:
                        self.SetResult(False, "Not Bad Right Bud")
                        return
        if index != -1:
            self.UpdateList(serialToSearch)
        else:
            if serialToSearch in self.caseSerials or serialToSearch in self.leftSerials or serialToSearch in self.rightSerials:
                self.SetResult(False, "Incorrect Category")
            self.SetResult(False, "Serial not found")
        pass
    
    def SetCurrentSet(self, index : int):
        self.listCaseFuncString.set(self.caseFunctionality[index])
        self.listCaseSerialString.set(self.caseSerials[index])
        self.listCaseDefectString.set(self.caseDefects[index])
        self.listLeftFuncString.set(self.leftFunctionality[index])
        self.listLeftSerialString.set(self.leftSerials[index])
        self.listLeftDefectString.set(self.leftDefects[index])
        self.listRightFuncString.set(self.rightFunctionality[index])
        self.listRightSerialString.set(self.rightSerials[index])
        self.listRightDefectString.set(self.rightDefects[index])
    
    def UpdateList(self, serial : str) -> bool:
        if serial in self.currentListSerials:
            playsound(resource_path("Sounds/bonk.mp3"))
            return False
        self.currentListSerials.insert(0, serial)
        self.currentCountValue.set(len(self.currentListSerials))
        self.currentCountLabel.config(text="Current Count: " + str(self.currentCountValue.get()))
        self.currentListVar.set(self.currentListSerials)
        return True
    
    def RemovePrevious(self):
        self.currentListSerials.pop(0)
        self.currentCountValue.set(len(self.currentListSerials))
        self.currentCountLabel.config(text="Current Count: " + str(self.currentCountValue.get()))
        self.currentListVar.set(self.currentListSerials)
    def RemoveSelected(self):
        index = self.currentListBox.curselection()
        if len(index) > 0:
            self.currentListSerials.pop(index[0])
            self.currentCountValue.set(len(self.currentListSerials))
            self.currentCountLabel.config(text="Current Count: " + str(self.currentCountValue.get()))
            self.currentListVar.set(self.currentListSerials)
    
    def ClearList(self):
        self.currentListSerials.clear()
        self.currentCountValue.set(len(self.currentListSerials))
        self.currentCountLabel.config(text="Current Count: " + str(self.currentCountValue.get()))
        self.currentListVar.set(self.currentListSerials)

    def SetResult(self, good : bool, defects : str = ""):
        if good:
            self.resultLabel.config(text=defects, background="green")
            playsound(resource_path("Sounds/correct.mp3"),False)
        else:
            self.resultLabel.config(text=defects, background="red")
            playsound(resource_path("Sounds/wrong.mp3"), False)
        if "iCloud" in defects:
            self.icloudFrame.grid()
        else:
            self.icloudFrame.grid_remove()

    def WindowFocused(self,event):
        pass

    def EnteredPressed(self, event):
        self.SearchManifest()
        self.searchString.set("")

    def Load(self, loadOverride = None):
        super().Load(loadOverride)
        loadDict : dict = {}
        if loadOverride:
            loadDict = loadOverride
        else:
            if self.hasSave:
                loadDict = self.saveData
        
        if len(loadDict.items()) > 0:
            keys = loadDict.keys()
            if "filename" in keys:
                self.importString.set(loadDict["filename"])

    def Save(self) -> dict:
        saveDict : dict = {}
        saveDict["filename"] = self.importString.get()
        return saveDict