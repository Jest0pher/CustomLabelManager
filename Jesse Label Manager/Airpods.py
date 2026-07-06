from GlobalImport import *
from Custom import CustomLabel

class AirpodsLabel(CustomLabel):

    po : StringVar
    initials : StringVar

    caseModel : StringVar
    caseOptions : OptionMenu
    leftModel : StringVar
    leftOptions : OptionMenu
    rightModel : StringVar
    rightOptions : OptionMenu

    scpoBuds : BooleanVar
    printType : StringVar
    radioIndividual : Radiobutton
    radioComplete : Radiobutton
    radioPrint : Radiobutton

    allSN : StringVar
    prevAllSN : StringVar
    allSNEntry : ttk.Entry
    allSNLabel : ttk.Label
    allSNPrevLabel : ttk.Label
    allSNNoteLabel : ttk.Label
    allSNErrorLabel : ttk.Label
    prevAllSNLabel : ttk.Label
    prevAllSNButton : Button
    allFormat : StringVar
    allFormatLabel : ttk.Label
    allFormatCLR : Radiobutton
    allFormatCL : Radiobutton
    allFormatCR : Radiobutton
    allFormatLR : Radiobutton
    caseSN : StringVar
    prevCaseSN : StringVar
    caseSNEntry : ttk.Entry
    prevCaseSNLabel : ttk.Label
    prevCaseSNButton : Button
    leftSN : StringVar
    prevLeftSN : StringVar
    leftSNEntry : ttk.Entry
    prevLeftSNLabel : ttk.Entry
    prevLeftSNButton : Button
    rightSN : StringVar
    prevRightSN : StringVar
    rightSNEntry : ttk.Entry
    prevRightSNLabel : ttk.Entry
    prevRightSNButton : Button
    serialEntryStartCol : int
    serialEntryStartRow : int
    leftL : zpl.Label
    rightL : zpl.Label
    parseError : bool = False
    snLabels = []
    printLabelsZPL : str = ""
    ffLabel : ttk.Label
    goodCaseLabel : ttk.Label
    goodLLabel : ttk.Label
    goodRLabel : ttk.Label
    badCaseLabel : ttk.Label
    badLLabel : ttk.Label
    badRLabel : ttk.Label
    ffStr : StringVar
    goodCaseStr : StringVar
    goodMagCaseStr : StringVar
    goodLStr : StringVar
    goodRStr : StringVar
    badCaseStr : StringVar
    badMagCaseStr : StringVar
    badLStr : StringVar
    badRStr : StringVar
    ffEntry : ttk.Entry
    goodCaseEntry : ttk.Entry
    goodMagCaseEntry : ttk.Entry
    goodLEntry : ttk.Entry
    goodREntry : ttk.Entry
    badCaseEntry : ttk.Entry
    badMagCaseEntry : ttk.Entry
    badLEntry : ttk.Entry
    badREntry : ttk.Entry
    icloudBool : BooleanVar
    icloudCheck : ttk.Checkbutton
    engravedButton : ttk.Button
    printEngravedQueued : bool = False
    engravedZPL : str = "^XA^PW599^LL299^FO23,35^A0N,41,41^FB599,1,0,L,0^FD^FS^FO23,94^A0N,41,41^FB599,1,0,L,0^FDEngraved^FS^FO23,153^A0N,41,41^FB599,1,0,L,0^FD^FS^FO23,212^A0N,41,41^FB599,1,0,L,0^FD^FS^FO23,271^A0N,41,41^FB599,1,0,L,0^FD^FS^XZ"
    printMismatchedQueued : bool = False
    mismatchedZPL : str = "^XA^PW599^LL299^FO23,35^A0N,41,41^FB599,1,0,L,0^FD^FS^FO23,94^A0N,41,41^FB599,1,0,L,0^FDMismatched^FS^FO23,153^A0N,41,41^FB599,1,0,L,0^FD^FS^FO23,212^A0N,41,41^FB599,1,0,L,0^FD^FS^FO23,271^A0N,41,41^FB599,1,0,L,0^FD^FS^XZ"

    caseModels = ["A1602", "A1938", "A2190", "A2566", "A2700", "A2897", "A2968","A3058","A3059", "A3122"]
    budsModels = [[("A2031","A2032"),("A1722","A1523")], [("A1722","A1523"),("A2031","A2032")], [("A2084", "A2083")], [("A2564", "A2565")], [("A2699","A2698")], [("A2564", "A2565")], [("A3048", "A3047"), ("A3049", "A3049")],[("A3053","A3050")],[("A3056","A3055")],[("A3064","A3063")]]
    currentLBuds : list[str] = ["1","3"]
    currentRBuds : list[str] = ["2","4"]
    
    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, mm=mm, height=height, startColumn=startColumn, startRow=startRow)
        self.initials = StringVar(value=initials)
        self.po = StringVar(value=po)

        self.currentLBuds.append('1')
        self.currentRBuds.append('1')
        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def WindowFocused(self,event):
        if event.widget in [self.root, self.radioIndividual, self.radioComplete]:
            if self.printType.get() == "Individual":
                self.caseSNEntry.focus_set()
            else:
                self.allSNEntry.focus_set()

    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        ttk.Label(self.frame, text="PO").grid(column=startColumn,row=startRow)
        ttk.Entry(self.frame, textvariable=self.po).grid(column=startColumn+1,row=startRow)
        ttk.Label(self.frame, text="").grid(column=startColumn+2,row=startRow)
        ttk.Label(self.frame, text="").grid(column=startColumn+3,row=startRow)
        ttk.Label(self.frame, text="Initials").grid(column=startColumn+4,row=startRow)
        ttk.Entry(self.frame, textvariable=self.initials).grid(column=startColumn+5, row=startRow)

        ttk.Label(self.frame, text="Case Model").grid(column=startColumn,row=startRow+1)
        self.caseModel = StringVar(value=self.caseModels[0])
        copiedCases = self.caseModels.copy()
        copiedCases.pop(0)
        self.caseOptions = OptionMenu(self.frame, self.caseModel,self.caseModel.get(), *copiedCases,command=self.CaseModelChanged)
        self.caseOptions.grid(column=startColumn+1, row=startRow+1)
        ttk.Label(self.frame, text="Left Model").grid(column=startColumn+2,row=startRow+1)
        self.leftModel = StringVar(value=self.currentLBuds[0])
        self.currentLBuds.pop(0)
        self.leftOptions = OptionMenu(self.frame, self.leftModel,self.leftModel.get(), *self.currentLBuds)
        self.leftOptions.grid(column=startColumn+3, row=startRow+1)
        ttk.Label(self.frame, text="Right Model").grid(column=startColumn+4,row=startRow+1)
        self.rightModel = StringVar(value=self.currentRBuds[0])
        self.currentRBuds.pop(0)
        self.rightOptions = OptionMenu(self.frame, self.rightModel,self.rightModel.get(), *self.currentRBuds)
        self.rightOptions.grid(column=startColumn+5, row=startRow+1)

        ttk.Label(self.frame, text=" ").grid(column=startColumn,row=startRow+2)

        self.scpoBuds = BooleanVar(value=False)
        Checkbutton(self.frame, text="SCPO Buds", variable=self.scpoBuds).grid(column=startColumn, row=startRow+3)
        self.printType = StringVar(value="Individual")
        self.radioIndividual = Radiobutton(self.frame, text="Individual", value='Individual', variable=self.printType, command=self.PrintTypeChanged)
        self.radioIndividual.grid(column=startColumn+2, row=startRow+3)
        self.radioComplete = Radiobutton(self.frame, text="Complete", value='Complete', variable=self.printType, command=self.PrintTypeChanged)
        self.radioComplete.grid(column=startColumn+3, row=startRow+3)
        self.radioPrint = Radiobutton(self.frame, text="Print", value='Print', variable=self.printType, command=self.PrintTypeChanged)
        self.radioPrint.grid(column=startColumn+4, row=startRow+3)
        
        ttk.Label(self.frame, text=" ").grid(column=startColumn,row=startRow+4)

        self.serialEntryStartCol=startColumn
        self.serialEntryStartRow=startRow+5

        self.ffStr = StringVar()
        self.goodCaseStr = StringVar()
        self.goodMagCaseStr = StringVar()
        self.goodLStr = StringVar()
        self.goodRStr = StringVar()
        self.badCaseStr = StringVar()
        self.badMagCaseStr = StringVar()
        self.badLStr = StringVar()
        self.badRStr = StringVar()
        self.icloudBool = BooleanVar(value=True)
        self.ffLabel = ttk.Label(self.frame, text="Fully Functional:")
        self.ffLabel.grid(column=startColumn+1, row=self.serialEntryStartRow)
        self.ffEntry = ttk.Entry(self.frame, textvariable=self.ffStr)
        self.ffEntry.grid(column=startColumn+2, row=self.serialEntryStartRow)
        self.goodCaseLabel = ttk.Label(self.frame, text="Good Case:")
        self.goodCaseLabel.grid(column=startColumn+1, row=self.serialEntryStartRow+1)
        self.goodCaseEntry = ttk.Entry(self.frame, textvariable=self.goodCaseStr)
        self.goodCaseEntry.grid(column=startColumn+2, row=self.serialEntryStartRow+1)
        self.goodMagCaseLabel = ttk.Label(self.frame, text="Good Magsafe Case:")
        self.goodMagCaseLabel.grid(column=startColumn+1, row=self.serialEntryStartRow+2)
        self.goodMagCaseEntry = ttk.Entry(self.frame, textvariable=self.goodMagCaseStr)
        self.goodMagCaseEntry.grid(column=startColumn+2, row=self.serialEntryStartRow+2)
        self.goodLLabel = ttk.Label(self.frame, text="Good L Bud:")
        self.goodLLabel.grid(column=startColumn+1, row=self.serialEntryStartRow+3)
        self.goodLEntry = ttk.Entry(self.frame, textvariable=self.goodLStr)
        self.goodLEntry.grid(column=startColumn+2, row=self.serialEntryStartRow+3)
        self.goodRLabel = ttk.Label(self.frame, text="Good R Bud:")
        self.goodRLabel.grid(column=startColumn+1, row=self.serialEntryStartRow+4)
        self.goodREntry = ttk.Entry(self.frame, textvariable=self.goodRStr)
        self.goodREntry.grid(column=startColumn+2, row=self.serialEntryStartRow+4)

        self.icloudCheck = ttk.Checkbutton(self.frame, text="iCloud Locked", variable=self.icloudBool)
        self.icloudCheck.grid(column=startColumn+4, row=self.serialEntryStartRow)
        self.badCaseLabel = ttk.Label(self.frame, text="Bad Case:")
        self.badCaseLabel.grid(column=startColumn+3, row=self.serialEntryStartRow+1)
        self.badCaseEntry = ttk.Entry(self.frame, textvariable=self.badCaseStr)
        self.badCaseEntry.grid(column=startColumn+4, row=self.serialEntryStartRow+1)
        self.badMagCaseLabel = ttk.Label(self.frame, text="Bad Magsafe Case:")
        self.badMagCaseLabel.grid(column=startColumn+3, row=self.serialEntryStartRow+2)
        self.badMagCaseEntry = ttk.Entry(self.frame, textvariable=self.badMagCaseStr)
        self.badMagCaseEntry.grid(column=startColumn+4, row=self.serialEntryStartRow+2)
        self.badLLabel = ttk.Label(self.frame, text="Bad L Bud:")
        self.badLLabel.grid(column=startColumn+3, row=self.serialEntryStartRow+3)
        self.badLEntry = ttk.Entry(self.frame, textvariable=self.badLStr)
        self.badLEntry.grid(column=startColumn+4, row=self.serialEntryStartRow+3)
        self.badRLabel = ttk.Label(self.frame, text="Bad R Bud:")
        self.badRLabel.grid(column=startColumn+3, row=self.serialEntryStartRow+4)
        self.badREntry = ttk.Entry(self.frame, textvariable=self.badRStr)
        self.badREntry.grid(column=startColumn+4, row=self.serialEntryStartRow+4)

        self.HidePrint()

        self.allSN = StringVar(value="")
        self.allSNLabel = ttk.Label(self.frame, text="Serial Numbers")
        self.allSNLabel.grid(column=startColumn+2, row=self.serialEntryStartRow)
        self.allSNNoteLabel = ttk.Label(self.frame, text="Tab or Comma Separated")
        self.allSNNoteLabel.grid(column=startColumn+3, row=self.serialEntryStartRow-1)
        self.allSNEntry = ttk.Entry(self.frame, textvariable=self.allSN)
        self.allSNEntry.grid(column=startColumn+3, row=self.serialEntryStartRow)
        self.allSNErrorLabel = ttk.Label(self.frame, text="")
        self.allSNErrorLabel.grid(column=startColumn+4, row=self.serialEntryStartRow)
        self.prevAllSN = StringVar(value="")
        self.allSNPrevLabel = ttk.Label(self.frame, text="Previous Serials")
        self.allSNPrevLabel.grid(column=startColumn+2, row=self.serialEntryStartRow+1)
        self.prevAllSNLabel = ttk.Label(self.frame, textvariable=self.prevAllSN)
        self.prevAllSNLabel.grid(column=startColumn+3, row=self.serialEntryStartRow+1)
        self.prevAllSNButton = ttk.Button(self.frame, text="Paste Previous", command=self.PastePrevAll)
        self.prevAllSNButton.grid(column=startColumn+3, row=self.serialEntryStartRow+2)

        self.allFormat = StringVar(value="CLR")
        self.allFormatLabel = ttk.Label(self.frame, text="Format")
        self.allFormatLabel.grid(column=startColumn, row=self.serialEntryStartRow-1)
        self.allFormatCLR = Radiobutton(self.frame, text="Case Left Right", value="CLR", variable=self.allFormat)
        self.allFormatCLR.grid(column=startColumn, row=self.serialEntryStartRow)
        self.allFormatCL = Radiobutton(self.frame, text="Case Left", value="CL", variable=self.allFormat)
        self.allFormatCL.grid(column=startColumn, row=self.serialEntryStartRow+1)
        self.allFormatCR = Radiobutton(self.frame, text="Case Right", value="CR", variable=self.allFormat)
        self.allFormatCR.grid(column=startColumn, row=self.serialEntryStartRow+2)
        self.allFormatLR = Radiobutton(self.frame, text="Left Right", value="LR", variable=self.allFormat)
        self.allFormatLR.grid(column=startColumn, row=self.serialEntryStartRow+3)

        self.HideComplete()
        
        self.snLabels.clear()
        self.snLabels.append(ttk.Label(self.frame, text="Case SN"))
        self.snLabels[0].grid(column=startColumn, row=self.serialEntryStartRow)
        self.snLabels.append(ttk.Label(self.frame, text="Left SN"))
        self.snLabels[1].grid(column=startColumn+2, row=self.serialEntryStartRow)
        self.snLabels.append(ttk.Label(self.frame, text="Right SN"))
        self.snLabels[2].grid(column=startColumn+4, row=self.serialEntryStartRow)
        self.caseSN = StringVar(value="")
        self.caseSNEntry = ttk.Entry(self.frame, textvariable=self.caseSN)
        self.caseSNEntry.grid(column=startColumn+1, row=self.serialEntryStartRow)
        self.leftSN = StringVar(value="")
        self.leftSNEntry = ttk.Entry(self.frame, textvariable=self.leftSN)
        self.leftSNEntry.grid(column=startColumn+3, row=self.serialEntryStartRow)
        self.rightSN = StringVar(value="")
        self.rightSNEntry = ttk.Entry(self.frame, textvariable=self.rightSN)
        self.rightSNEntry.grid(column=startColumn+5, row=self.serialEntryStartRow)
        self.prevCaseSN = StringVar(value="")
        self.snLabels.append(ttk.Label(self.frame,text="Prev SN"))
        self.snLabels[3].grid(column=startColumn,row=self.serialEntryStartRow+1)
        self.prevCaseSNLabel = ttk.Label(self.frame, textvariable=self.prevCaseSN)
        self.prevCaseSNLabel.grid(column=startColumn+1,row=self.serialEntryStartRow+1)
        self.prevLeftSN = StringVar(value="")
        self.prevLeftSNLabel = ttk.Label(self.frame, textvariable=self.prevLeftSN)
        self.prevLeftSNLabel.grid(column=startColumn+3,row=self.serialEntryStartRow+1)
        self.prevRightSN = StringVar(value="")
        self.prevRightSNLabel = ttk.Label(self.frame, textvariable=self.prevRightSN)
        self.prevRightSNLabel.grid(column=startColumn+5,row=self.serialEntryStartRow+1)
        self.prevCaseSNButton = Button(self.frame, text="Paste Previous Case", command=self.PastePrevCase)
        self.prevCaseSNButton.grid(column=startColumn+1, row=self.serialEntryStartRow+2)
        self.prevLeftSNButton = Button(self.frame, text="Paste Previous Left", command=self.PastePrevLeft)
        self.prevLeftSNButton.grid(column=startColumn+3, row=self.serialEntryStartRow+2)
        self.prevRightSNButton = Button(self.frame, text="Paste Previous Right", command=self.PastePrevRight)
        self.prevRightSNButton.grid(column=startColumn+5, row=self.serialEntryStartRow+2)

        self.HideIndividual()

        ttk.Label(self.frame, text=" ").grid(column=startColumn+1,row=self.serialEntryStartRow+3)

        self.engravedButton = Button(self.frame, text="Print Engraved", command=self.PrintEngravedLabel)
        self.engravedButton.grid(column=startColumn+3, row=self.serialEntryStartRow+6)
        self.engravedButton = Button(self.frame, text="Print Mismatched", command=self.PrintMismatchedLabel)
        self.engravedButton.grid(column=startColumn+3, row=self.serialEntryStartRow+7)
        self.DisplayPrintButton(startColumn+3, self.serialEntryStartRow+8)

        self.Load()

    def PrintEngravedLabel(self):
        self.printEngravedQueued = True
        self.testObserve.CallFunc()
    
    def PrintMismatchedLabel(self):
        self.printMismatchedQueued = True
        self.testObserve.CallFunc()

    def CaseModelChanged(self, *args):
        index : int = self.caseModels.index(args[0])
        self.currentLBuds.clear()
        self.currentRBuds.clear()
        for i in range(self.budsModels[index].__len__()):
            self.currentLBuds.append(self.budsModels[index][i][0])
            self.currentRBuds.append(self.budsModels[index][i][1])
        tempColumn : int = self.leftOptions.grid_info()["column"]
        tempRow : int = self.leftOptions.grid_info()["row"]
        self.leftOptions.destroy()
        self.rightOptions.destroy()
        if not self.leftModel.get() in self.currentLBuds:
            self.leftModel.set(self.currentLBuds[0])
        self.currentLBuds.pop(self.currentLBuds.index(self.leftModel.get()))
        self.leftOptions = OptionMenu(self.frame, self.leftModel,self.leftModel.get(), *self.currentLBuds)
        self.leftOptions.grid(column=tempColumn, row=tempRow)
        if not self.rightModel.get() in self.currentRBuds:
            self.rightModel.set(self.currentRBuds[0])
        self.currentRBuds.pop(self.currentRBuds.index(self.rightModel.get()))
        self.rightOptions = OptionMenu(self.frame, self.rightModel,self.rightModel.get(), *self.currentRBuds)
        self.rightOptions.grid(column=tempColumn+2, row=tempRow)

        if self.printType.get() == "Print":
            self.HidePrint()
            self.ShowPrint()
        pass
    
    def PrintTypeChanged(self):
        print(self.printType.get())
        if self.printType.get() == "Individual":
            self.HideComplete()
            self.HidePrint()
            self.ShowIndividual()
            self.caseSNEntry.focus_set()
        elif self.printType.get() == "Print":
            self.HideIndividual()
            self.HideComplete()
            self.ShowPrint()
        else:
            self.HideIndividual()
            self.HidePrint()
            self.ShowComplete()
            self.allSNEntry.focus_set()
    
    def PastePrevCase(self):
        self.caseSN.set(self.prevCaseSN.get())
    def PastePrevLeft(self):
        self.leftSN.set(self.prevLeftSN.get())
    def PastePrevRight(self):
        self.rightSN.set(self.prevRightSN.get())
    def PastePrevAll(self):
        self.allSN.set(self.prevAllSN.get())
    
    def HideIndividual(self):
        for i in self.snLabels:
            i.grid_remove()
        self.caseSNEntry.grid_remove()
        self.prevCaseSNLabel.grid_remove()
        self.prevCaseSNButton.grid_remove()
        self.leftSNEntry.grid_remove()
        self.prevLeftSNLabel.grid_remove()
        self.prevLeftSNButton.grid_remove()
        self.rightSNEntry.grid_remove()
        self.prevRightSNLabel.grid_remove()
        self.prevRightSNButton.grid_remove()
    
    def ShowIndividual(self):
        for i in self.snLabels:
            i.grid()
        self.caseSNEntry.grid()
        self.prevCaseSNLabel.grid()
        self.prevCaseSNButton.grid()
        self.leftSNEntry.grid()
        self.prevLeftSNLabel.grid()
        self.prevLeftSNButton.grid()
        self.rightSNEntry.grid()
        self.prevRightSNLabel.grid()
        self.prevRightSNButton.grid()
    
    def HideComplete(self):
        self.allSNEntry.grid_remove()
        self.allSNLabel.grid_remove()
        self.allSNNoteLabel.grid_remove()
        self.allSNErrorLabel.grid_remove()
        self.allSNPrevLabel.grid_remove()
        self.prevAllSNLabel.grid_remove()
        self.prevAllSNButton.grid_remove()
        self.prevAllSNButton.grid_remove()
        self.allFormatLabel.grid_remove()
        self.allFormatCLR.grid_remove()
        self.allFormatCL.grid_remove()
        self.allFormatCR.grid_remove()
        self.allFormatLR.grid_remove()

    def ShowComplete(self):
        self.allSNEntry.grid()
        self.allSNLabel.grid()
        self.allSNNoteLabel.grid()
        self.allSNErrorLabel.grid()
        self.allSNPrevLabel.grid()
        self.prevAllSNLabel.grid()
        self.prevAllSNButton.grid()
        self.prevAllSNButton.grid()
        self.allFormatLabel.grid()
        self.allFormatCLR.grid()
        self.allFormatCL.grid()
        self.allFormatCR.grid()
        self.allFormatLR.grid()
    
    def HidePrint(self):
        self.ffLabel.grid_remove()
        self.ffEntry.grid_remove()
        self.goodCaseLabel.grid_remove()
        self.goodCaseEntry.grid_remove()
        self.goodMagCaseLabel.grid_remove()
        self.goodMagCaseEntry.grid_remove()
        self.goodLLabel.grid_remove()
        self.goodLEntry.grid_remove()
        self.goodRLabel.grid_remove()
        self.goodREntry.grid_remove()
        self.badCaseLabel.grid_remove()
        self.badCaseEntry.grid_remove()
        self.badMagCaseLabel.grid_remove()
        self.badMagCaseEntry.grid_remove()
        self.badLLabel.grid_remove()
        self.badLEntry.grid_remove()
        self.badRLabel.grid_remove()
        self.badREntry.grid_remove()
        self.icloudCheck.grid_remove()

    def ShowPrint(self):
        self.ffLabel.grid()
        self.ffEntry.grid()
        self.goodCaseLabel.grid()
        self.goodCaseEntry.grid()
        self.goodLLabel.grid()
        self.goodLEntry.grid()
        self.goodRLabel.grid()
        self.goodREntry.grid()
        self.badCaseLabel.grid()
        self.badCaseEntry.grid()
        self.badLLabel.grid()
        self.badLEntry.grid()
        self.badRLabel.grid()
        self.badREntry.grid()
        self.icloudCheck.grid()
        if self.caseModel.get() == "A2190":
            self.goodMagCaseLabel.grid()
            self.goodMagCaseEntry.grid()
            self.badMagCaseLabel.grid()
            self.badMagCaseEntry.grid()

    def PrintBagLabels(self):
        self.printLabelsZPL = ""
        arraySize = 8
        texts = ["Fully Functional",self.caseModel.get(),f"QTY: {self.ffStr.get()}",f"PO:{self.po.get()}","",
                 "Good Case",self.caseModel.get(),f"QTY: {self.goodCaseStr.get()}",f"PO:{self.po.get()}","",
                 "Good L Bud",self.leftModel.get(),f"QTY: {self.goodLStr.get()}",f"PO:{self.po.get()}","",
                 "Good R Bud",self.rightModel.get(),f"QTY: {self.goodRStr.get()}",f"PO:{self.po.get()}","",
                 "Bad Case",self.caseModel.get(),f"QTY: {self.badCaseStr.get()}",f"PO:{self.po.get()}","",
                 "Bad L Bud",self.leftModel.get(),f"QTY: {self.badLStr.get()}",f"PO:{self.po.get()}","",
                 "Bad R Bud",self.rightModel.get(),f"QTY: {self.badRStr.get()}",f"PO:{self.po.get()}","",
                 "ICloud Locked","Mixed Defective/Functional",self.leftModel.get() + "/" + self.rightModel.get(),f"PO:{self.po.get()}","",
                 "Good Case(Magsafe)",self.caseModel.get(),f"QTY: {self.goodMagCaseStr.get()}",f"PO:{self.po.get()}","",
                 "Bad Case(Magsafe)",self.caseModel.get(),f"QTY: {self.badMagCaseStr.get()}",f"PO:{self.po.get()}","",]
        if self.caseModel.get() == "A2190":
            texts[5] = "Good Case(Non-magsafe)"
            texts[20] = "Bad Case(Non-magsafe)"
            arraySize = 10
            
        for offset in range(arraySize):
            label = zpl.Label(self.height,self.width, 11.8)
            originY = 3
            skipped = False
            if offset == 7:
                if self.icloudBool.get() == False:
                    continue
            for i in range(5):
                index = 5*offset + i
                if texts[index] == "QTY: ":
                    skipped = True
                    break
                if index >= texts.__len__():
                    break
                label.origin(2, originY)
                TextBoxResize(label, texts[index],self.width, self.height)
                label.endorigin()
                originY += 5
            if skipped == False:
                self.printLabelsZPL += label.dumpZPL()
        

    def ParseCompleteSerials(self) -> list[str]:
        serials : list[str] = self.allSN.get().split('\t')
        if serials.__len__() == self.allFormat.get().__len__():
            self.parseError = False
            return serials

        self.parseError = True
        return []
    
    def SetLabelData(self):
        caseStr : str = ""
        leftStr : str = ""
        rightStr : str = ""
        if self.printType.get() == "Individual":
            self.parseError = False
            caseStr = self.caseSN.get().upper()
            leftStr = self.leftSN.get().upper()
            rightStr = self.rightSN.get().upper()
        elif self.printType.get() == "Print":
            self.l = self.PrintBagLabels()
            return
        else:
            serials : list[str] = self.ParseCompleteSerials()
            if self.parseError == False:
                match(self.allFormat.get()):
                    case "CLR":
                        caseStr = serials[0]
                        leftStr = serials[1]
                        rightStr = serials[2]
                    case "CL":
                        caseStr = serials[0]
                        leftStr = serials[1]
                    case "CR":
                        caseStr = serials[0]
                        rightStr = serials[1]
                    case "LR":
                        leftStr = serials[0]
                        rightStr = serials[1]
        if self.parseError == False:
            self.l = self.FillData(caseStr, self.caseModel.get())
            self.leftL = self.FillData(leftStr, self.leftModel.get(), isBud=True)
            self.rightL = self.FillData(rightStr, self.rightModel.get(), isBud=True)
        pass

    def FillData(self, serial : str, model : str, isBud : bool = False) -> zpl.Label:
        label = zpl.Label(self.height,self.width, 11.8)
        label.origin(1,4)
        
        concat = serial
        concat = "S/N: " + serial
        #self.l.write_text(concat, char_height=4.2, char_width=4, line_width=45, justification='L')
        TextBoxResize(label, concat, self.width, self.height)
        label.endorigin()

        label.origin(3, 8)
        label.zpl_raw("^BY2")
        label.barcode('C', serial, height=60, mode='A')
        label.endorigin()

        if isBud and self.scpoBuds.get():
            label.origin(4,21)
            label.write_text("PO: SCPO", char_height=3, char_width=3, line_width=30, justification='L')
            label.endorigin()
        else:
            label.origin(4,21)
            label.write_text("PO: " + self.po.get(), char_height=3, char_width=3, line_width=30, justification='L')
            label.endorigin()

        label.origin(37,21)
        label.write_text(self.initials.get().upper(), char_height=4, char_width=4, line_width=30, justification='L')
        label.endorigin()
    
        label.origin(4,17)
        label.write_text("Model: " + model, char_height=3, char_width=3, line_width=30, justification='L')
        label.endorigin()

        return label

    def PrintTrigger(self):
        super().PrintTrigger()
        if self.parseError == True:
            self.allSNErrorLabel.configure(text="Parsing Error")
            return
        self.allSNErrorLabel.configure(text="")
        if self.printType.get() == "Individual":
            self.prevCaseSN.set(self.caseSN.get())
            self.caseSN.set("")
            self.prevLeftSN.set(self.leftSN.get())
            self.leftSN.set("")
            self.prevRightSN.set(self.rightSN.get())
            self.rightSN.set("")
            self.caseSNEntry.focus_set()
        elif self.printType.get() == "Print":
            pass
        else:
            self.prevAllSN.set(self.allSN.get())
            self.allSN.set("")
            self.allSNEntry.focus_set()

    def GetPrintData(self, setData = True):
        if self.printEngravedQueued:
            self.printEngravedQueued = False
            return self.engravedZPL
        elif self.printMismatchedQueued:
            self.printMismatchedQueued = False
            return self.mismatchedZPL
        super()
        if setData:
            self.SetLabelData()
        if self.parseError == False and self.printType.get() == "Complete":
            match(self.allFormat.get()):
                case "CLR":
                    return self.l.dumpZPL() + self.leftL.dumpZPL() + self.rightL.dumpZPL()
                case "CL":
                    return self.l.dumpZPL() + self.leftL.dumpZPL()
                case "CR":
                    return self.l.dumpZPL() + self.rightL.dumpZPL()
                case "LR":
                    return self.leftL.dumpZPL() + self.rightL.dumpZPL()
        elif self.printType.get() == "Print":
            return self.printLabelsZPL
        else:
            return self.EmptyCheck("case") + self.EmptyCheck("left") + self.EmptyCheck("right")
        return ""

    def EmptyCheck(self, item : str)->str:
        match(item):
            case "case":
                if self.caseSN.get() != "":
                    return self.l.dumpZPL()
            case "left":
                if self.leftSN.get() != "":
                    return self.leftL.dumpZPL()
            case "right":
                if self.rightSN.get() != "":
                    return self.rightL.dumpZPL()
        return ""

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
            if "po" in keys:
                self.po.set(loadDict["po"])
            if "initials" in keys:
                self.initials.set(loadDict["initials"])
            if "caseModel" in keys:
                self.caseModel.set(loadDict["caseModel"])
            if "caseSerial" in keys:
                self.caseSN.set(loadDict["caseSerial"])
            if "prevCaseSerial" in keys:
                self.prevCaseSN.set(loadDict["prevCaseSerial"])
            if "leftModel" in keys:
                self.leftModel.set(loadDict["leftModel"])
            if "leftSerial" in keys:
                self.leftSN.set(loadDict["leftSerial"])
            if "prevLeftSerial" in keys:
                self.prevLeftSN.set(loadDict["prevLeftSerial"])
            if "rightModel" in keys:
                self.rightModel.set(loadDict["rightModel"])
            if "rightSerial" in keys:
                self.rightSN.set(loadDict["rightSerial"])
            if "prevRightSerial" in keys:
                self.prevRightSN.set(loadDict["prevRightSerial"])
            if "printType" in keys:
                self.printType.set(loadDict["printType"])
            if "allSerial" in keys:
                self.allSN.set(loadDict["allSerial"])
            if "prevAllSerial" in keys:
                self.prevAllSN.set(loadDict["prevAllSerial"])
            if "allFormat" in keys:
                self.allFormat.set(loadDict["allFormat"])
            if "scpoBuds" in keys:
                self.scpoBuds.set(loadDict["scpoBuds"])
        
        self.CaseModelChanged(self.caseModel.get())
        if self.printType.get() == "Complete":
            self.HideIndividual()
            self.ShowComplete()
            self.allSNEntry.focus_set()
        elif self.printType.get() == "Print":
            self.HideIndividual()
            self.HideComplete()
            self.ShowPrint()
        else:
            self.caseSNEntry.focus_set()

    def Save(self) -> dict:
        saveDict : dict = super().Save()
        saveDict["po"] = self.po.get()
        saveDict["initials"] = self.initials.get()
        saveDict["caseModel"] = self.caseModel.get()
        saveDict["caseSerial"] = self.caseSN.get()
        saveDict["prevCaseSerial"] = self.prevCaseSN.get()
        saveDict["leftModel"] = self.leftModel.get()
        saveDict["leftSerial"] = self.leftSN.get()
        saveDict["prevLeftSerial"] = self.prevLeftSN.get()
        saveDict["rightModel"] = self.rightModel.get()
        saveDict["rightSerial"] = self.rightSN.get()
        saveDict["prevRightSerial"] = self.prevRightSN.get()
        saveDict["printType"] = self.printType.get()
        saveDict["allSerial"] = self.allSN.get()
        saveDict["prevAllSerial"] = self.prevAllSN.get()
        saveDict["allFormat"] = self.allFormat.get()
        saveDict["scpoBuds"] = self.scpoBuds.get()
        return saveDict
