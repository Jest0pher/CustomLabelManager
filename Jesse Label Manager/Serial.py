from GlobalImport import *
from Custom import CustomLabel

class SerialLabel(CustomLabel):
    class CSVExporter:
        frame : Frame
        filename : StringVar
        array = []
        listVar : StringVar
        listBox : Listbox
        record : bool = False
        recordButton : Button
        note : StringVar
        noteEntry : Entry
        clearNote : BooleanVar
        
        def CSVStartRecord(self):
            if self.record == True:
                self.record = False
                self.recordButton.configure(text="Start Record")
            else:
                self.record = True
                self.recordButton.configure(text="Stop Record")
        
        def CSVExport(self):
            if self.array.count == 0:
                print("No entries to save")
                return
            
            ok = ".-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            for i in self.filename.get():
                if i in ok:
                    continue
                else:
                    print("Bad Filename")
                    return
            print("Export " + self.filename.get())

            filePath = os.path.join(directory, self.filename.get()+".csv")
            csvFile = open(filePath, "w")
            csvFile.write("PO;Prefix;Serials;Model;Notes\n")
            for i in self.array:
                csvFile.write(str(i) + "\n")       
            csvFile.close()
        
        def CSVImport(self):
            filePath = os.path.join(directory, self.filename.get()+".csv")
            if os.path.exists(filePath):
                with open(filePath, 'r') as loadFile:
                    try:
                        counter : int = 0
                        valid : bool = False
                        for i in loadFile:
                            if counter == 0:
                                if i.__contains__("PO;Prefix;Serials;Model;Notes"):
                                    valid = True
                                    self.array.clear()
                                else:
                                    print("Format error")
                                    break
                            elif valid == True:
                                toAdd : str = ""
                                if i.endswith("\n"):
                                    toAdd = i.split('\n')[0]
                                else:
                                    toAdd = i
                                self.array.append(toAdd)
                            counter += 1
                        self.listVar.set(self.array)
                        self.listBox.see(self.listBox.size()-1)
                    except Exception as e:
                        print(e)
                        pass

        def CSVDeleteLast(self):
            self.array.pop()
            self.listVar.set(self.array)
            
        def CSVDeleteSelected(self):
            index = self.listBox.curselection()
            if len(index) > 0:
                self.array.pop(index[0])
                self.listVar.set(self.array)
            
        def CSVClearList(self):
            self.array.clear()
            self.listVar.set(self.array)

        def ConstructWindow(self, parentFrame :ttk.Frame, startColumn : int, startRow : int):
            self.frame = Frame(parentFrame)
            self.frame.grid(column=startColumn,row=startRow)
            ttk.Label(self.frame, text="Record to CSV file").grid(column=0, row=0)
            self.filename = StringVar(value="CSVExport")
            ttk.Label(self.frame,text="CSV Filename: ").grid(column=0, row=1)
            ttk.Entry(self.frame, textvariable=self.filename).grid(column=1,row=1)
            ttk.Label(self.frame,text="Printed Serials").grid(column=0, row=2)
            self.listVar = StringVar(value=self.array)
            listBoxFrame = Frame(self.frame)
            listBoxFrame.grid(column=0,row=2)
            self.listBox = Listbox(listBoxFrame, listvariable=self.listVar, selectmode=BROWSE, width=75)
            self.listBox.grid(column=0,row=0)
            vscrollBar = ttk.Scrollbar(listBoxFrame, orient=VERTICAL, command=self.listBox.yview)
            hscrollBar = ttk.Scrollbar(listBoxFrame, orient=HORIZONTAL, command=self.listBox.xview)
            self.listBox.configure(yscrollcommand=vscrollBar.set, xscrollcommand=hscrollBar.set)
            vscrollBar.grid(column=1, row=0, sticky="ns")
            hscrollBar.grid(column=0,row=1,sticky="ew")
            

            buttonFrame = Frame(self.frame)
            buttonFrame.grid(column=1,row=2)

            self.recordButton = ttk.Button(buttonFrame,text="Start Record", command=self.CSVStartRecord)
            self.recordButton.grid(column=startColumn, row=startRow)
            ttk.Button(buttonFrame,text="Import CSV", command=self.CSVImport).grid(column=startColumn, row=startRow+1)
            ttk.Button(buttonFrame,text="Export CSV", command=self.CSVExport).grid(column=startColumn, row=startRow+2)
            ttk.Button(buttonFrame,text="Delete Previous Entry",command=self.CSVDeleteLast).grid(column=startColumn, row=startRow+3)
            ttk.Button(buttonFrame,text="Delete Selected Entry",command=self.CSVDeleteSelected).grid(column=startColumn, row=startRow+4)
            ttk.Button(buttonFrame,text="Clear List",command=self.CSVClearList).grid(column=startColumn, row=startRow+5)

            #Add notes entry box
            noteFrame = Frame(self.frame)
            noteFrame.grid(column=0, row=3)
            ttk.Label(noteFrame, text="Additional Notes: ").grid(column=0, row=0)
            self.csvNote = StringVar()
            ttk.Entry(noteFrame, textvariable=self.csvNote).grid(column=1, row=0)
            self.clearNote = BooleanVar(value=True)
            ttk.Checkbutton(noteFrame, variable=self.clearNote, text="Clear Note").grid(column=2, row=0)
            
            self.Load()
            pass

        def DestroyWindow(self):
            self.record = False
            self.Save()
            for i in self.frame.winfo_children():
                i.destroy()
            self.frame.destroy()
        
        def CSVNewEntry(self, po : str, prefix : str, id : str, model : str):
            if self.record:
                entryString : str = po+','+prefix+','+id+','+model+','+self.csvNote.get()
                self.array.append(entryString)
                self.listVar.set(self.array)
                #Once note entry and variable set up
                if self.clearNote.get() == True:
                    self.csvNote.set("")
        
        def Save(self):
            #Save directly to file
            saveDict : dict =  {"list" : self.array, "filename" : self.filename.get(), "note" : self.csvNote.get(), "clearnote" : self.clearNote.get()}
            filePath = os.path.join(directory, "CSVExporter.txt")
            saveFile = open(filePath, "w")
            json.dump(saveDict,saveFile)
            saveFile.close()
            pass
        
        def Load(self):
            #Load directly from file
            filePath = os.path.join(directory, "CSVExporter.txt")
            if os.path.exists(filePath):
                with open(filePath, 'r') as loadFile:
                    try:
                        loadDict : dict = json.load(loadFile)
                        keys = loadDict.keys()
                        if "list" in keys:
                            self.array = loadDict["list"]
                            self.listVar.set(self.array)
                            self.listBox.see(self.listBox.size()-1)
                        if "filename" in keys:
                            self.filename.set(loadDict["filename"])
                        if "note" in keys:
                            self.csvNote.set(loadDict["note"])
                        if "clearnote" in keys:
                            self.clearNote.set(loadDict["clearnote"])
                    except json.JSONDecodeError as jsonError:
                        print("Corrupt File")
                        os.remove(filePath)
            pass

    initials : StringVar
    po : StringVar
    sn : StringVar
    prefix : StringVar

    radioNone : Radiobutton
    radioIMEI : Radiobutton
    radioSN : Radiobutton
    radioCustom : Radiobutton

    radioEntry : ttk.Entry
    radioEntryVar : StringVar

    model : StringVar

    serialLabel : ttk.Label
    serialEntry : ttk.Entry
    clearSN : BooleanVar
    clearButton : Checkbutton

    hideText : BooleanVar
    hideBar : BooleanVar
    hidePo : BooleanVar
    hideIni : BooleanVar
    hideModel : BooleanVar

    hideTextButton : Button
    hideBarButton : Button
    hidePoButton : Button
    hideIni : Button
    hideModelButton : Button

    previousSerial : StringVar
    prevSerialLabel : ttk.Label

    csvButton : Button
    csvBool : bool = False
    csvExporter : CSVExporter

    normalFrame : Frame

    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, mm=mm, height=height, startColumn=startColumn, startRow=startRow)
        self.initials = StringVar(value=initials)
        self.po = StringVar(value=po)

        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def WindowFocused(self,event):
        if event.widget in [self.radioNone, self.radioIMEI, self.radioSN, self.root, self.clearButton, self.hideTextButton, self.hideBarButton, self.hidePoButton, self.hideIniButton]:
            self.serialEntry.focus_set()
        elif event.widget == self.radioCustom:
            self.radioEntry.focus_set()
    
    def LabelClosed(self):
        try:
            self.csvExporter.DestroyWindow()
        except:
            pass
        super().LabelClosed()

    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        self.normalFrame = Frame(self.frame)
        self.normalFrame.grid(column=startColumn, row=startRow)
        self.prefix = StringVar(value="IMEI")
        ttk.Label(self.normalFrame, text="Prefix:").grid(column=startColumn,row=startRow)
        self.radioNone = ttk.Radiobutton(self.normalFrame, text="None", value="None", variable=self.prefix,command=self.RadioChanged)
        self.radioNone.grid(column=startColumn+1,row=startRow)
        self.radioIMEI = ttk.Radiobutton(self.normalFrame, text="IMEI", value="IMEI", variable=self.prefix,command=self.RadioChanged)
        self.radioIMEI.grid(column=startColumn+2,row=startRow)
        self.radioSN = ttk.Radiobutton(self.normalFrame, text="S/N", value="S/N", variable=self.prefix,command=self.RadioChanged)
        self.radioSN.grid(column=startColumn+3,row=startRow)
        self.radioCustom = ttk.Radiobutton(self.normalFrame, text="Custom", value="Custom", variable=self.prefix,command=self.RadioChanged)
        self.radioCustom.grid(column=startColumn+4,row=startRow)
        self.radioEntryVar = StringVar(value="")
        self.radioEntry = ttk.Entry(self.normalFrame,textvariable=self.radioEntryVar, state="disabled")
        self.radioEntry.grid(column=startColumn+5,row=startRow)

        ttk.Label(self.normalFrame,text="PO").grid(column=startColumn,row=startRow+1)
        ttk.Entry(self.normalFrame,textvariable=self.po).grid(column=startColumn+1,row=startRow+1)
        ttk.Label(self.normalFrame,text="Initials").grid(column=startColumn+3,row=startRow+1)
        ttk.Entry(self.normalFrame,textvariable=self.initials).grid(column=startColumn+4,row=startRow+1)

        ttk.Label(self.normalFrame, text="").grid(column=startColumn,row=startRow+2)

        ttk.Label(self.normalFrame, text="Model:").grid(column=startColumn, row=startRow+3)
        self.model = StringVar()
        modelEntry = ttk.Entry(self.normalFrame, textvariable=self.model)
        modelEntry.grid(column=startColumn+1, row=startRow+3)
        self.serialLabel = ttk.Label(self.normalFrame,text=self.prefix.get())
        self.serialLabel.grid(column=startColumn+2, row=startRow+3)
        self.sn = StringVar()
        self.serialEntry = ttk.Entry(self.normalFrame, textvariable=self.sn)
        self.serialEntry.grid(column=startColumn+3,row=startRow+3)
        self.root.protocol("WM_TAKE_FOCUS", self.WindowFocused)
        self.clearSN = BooleanVar()
        ttk.Label(self.normalFrame, text="Clear After Print").grid(column=startColumn+4, row=startRow+3)
        self.clearButton = ttk.Checkbutton(self.normalFrame, variable=self.clearSN)
        self.clearButton.grid(column=startColumn+4, row=startRow+4)
        self.previousSerial = StringVar()
        ttk.Label(self.normalFrame, text="Previous:").grid(column=startColumn+2, row=startRow+4)
        self.prevSerialLabel = ttk.Label(self.normalFrame, textvariable=self.previousSerial)
        self.prevSerialLabel.grid(column=startColumn+3,row=startRow+4)
        ttk.Button(self.normalFrame, text="Paste Previous Entry", command=self.PastePreviousPressed).grid(column=startColumn+3, row=startRow+5)

        ttk.Label(self.normalFrame, text="Hide Text").grid(column=startColumn+1,row=startRow+6)
        ttk.Label(self.normalFrame, text="Hide Barcode").grid(column=startColumn+2,row=startRow+6)
        ttk.Label(self.normalFrame, text="Hide PO").grid(column=startColumn+3,row=startRow+6)
        ttk.Label(self.normalFrame, text="Hide Initials").grid(column=startColumn+4,row=startRow+6)
        ttk.Label(self.normalFrame, text="Hide Model").grid(column=startColumn+5, row=startRow+6)
        self.hideText = BooleanVar()
        self.hideTextButton = ttk.Checkbutton(self.normalFrame,variable=self.hideText)
        self.hideTextButton.grid(column=startColumn+1,row=startRow+7)
        self.hideBar = BooleanVar()
        self.hideBarButton = ttk.Checkbutton(self.normalFrame,variable=self.hideBar)
        self.hideBarButton.grid(column=startColumn+2,row=startRow+7)
        self.hidePo = BooleanVar()
        self.hidePoButton = ttk.Checkbutton(self.normalFrame,variable=self.hidePo)
        self.hidePoButton.grid(column=startColumn+3,row=startRow+7)
        self.hideIni = BooleanVar()
        self.hideIniButton = ttk.Checkbutton(self.normalFrame,variable=self.hideIni)
        self.hideIniButton.grid(column=startColumn+4,row=startRow+7)
        self.hideModel = BooleanVar()
        self.hideModelButton = ttk.Checkbutton(self.normalFrame, variable=self.hideModel)
        self.hideModelButton.grid(column=startColumn+5,row=startRow+7)

        self.csvButton = Button(self.normalFrame, text="CSV Exporter", command=self.ToggleCSV)
        self.csvButton.grid(column=startColumn+6, row=startRow)

        self.csvExporter = self.CSVExporter()

        self.DisplayPrintButton(startColumn+3, startRow+8, self.normalFrame)
        
        self.Load()
    
    def RadioChanged(self):
        if self.prefix.get() == "Custom":
            self.radioEntry.configure(state="normal")
        else:
            self.radioEntry.configure(state="disabled")
        
        self.UpdateSerialLabel()
    
    def UpdateSerialLabel(self):
        labelText = ""
        if self.prefix.get() == "None" or self.prefix.get() == "Custom":
            labelText = "Identifier"
        else:
            labelText = self.prefix.get()
        
        self.serialLabel.configure(text=labelText)

    def SetLabelData(self):
        self.l = zpl.Label(self.height,self.width, 11.8)
        self.l.origin(1,4)
        self.sn.set(self.sn.get().upper())
        
        if self.hideText.get() == False:
            concat = self.sn.get()
            if self.prefix.get() != "None":
                if self.prefix.get() == "Custom":
                    concat = self.radioEntryVar.get() + ": " + self.sn.get()
                else:
                    concat = self.prefix.get() + ": " + self.sn.get()
            #self.l.write_text(concat, char_height=4.2, char_width=4, line_width=45, justification='L')
            TextBoxResize(self.l, concat, self.width, self.height)
            self.l.endorigin()

        if self.hideBar.get() == False:
            self.l.origin(3, 8)
            self.l.zpl_raw("^BY2")
            self.l.barcode('C', self.sn.get(), height=60, mode='A')
            self.l.endorigin()

        if self.hidePo.get() == False:
            self.l.origin(4,21)
            self.l.write_text("PO: " + self.po.get(), char_height=3, char_width=3, line_width=30, justification='L')
            self.l.endorigin()

        if self.hideIni.get() == False:
            self.l.origin(37,21)
            self.l.write_text(self.initials.get().upper(), char_height=4, char_width=4, line_width=30, justification='L')
            self.l.endorigin()
        
        if self.hideModel.get() == False:
            self.l.origin(4,17)
            self.l.write_text("Model: " + self.model.get(), char_height=3, char_width=3, line_width=30, justification='L')
            self.l.endorigin()

    def PastePreviousPressed(self):
        self.sn.set(self.previousSerial.get())

    def ToggleCSV(self):
        self.csvBool = not self.csvBool
        if self.csvBool == True:
            self.csvExporter.ConstructWindow(self.frame, 7, 0)
        else:
            self.csvExporter.DestroyWindow()
            pass

    def GetPrintData(self, setData :bool = True) -> str:
        super()
        if setData:
            self.SetLabelData()
        return self.l.dumpZPL()
    
    def PrintTrigger(self):
        super().PrintTrigger()
        self.csvExporter.CSVNewEntry(self.po.get(), self.prefix.get(), self.sn.get(), self.model.get())
        self.previousSerial.set(self.sn.get())
        if self.clearSN.get() == True:
            self.sn.set("")
        self.serialEntry.focus_set()
    
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
            if "prefix" in keys:
                self.prefix.set(loadDict["prefix"])
                self.RadioChanged()
            if "radiocustom" in keys:
                self.radioEntryVar.set(loadDict["radiocustom"])
            if "po" in keys:
                self.po.set(loadDict["po"])
            if "initials" in keys:
                self.initials.set(loadDict["initials"])
            if "serial" in keys:
                self.sn.set(loadDict["serial"])
            if "clear" in keys:
                self.clearSN.set(loadDict["clear"])
            if "hidetext" in keys:
                self.hideText.set(loadDict["hidetext"])
            if "hidebar" in keys:
                self.hideBar.set(loadDict["hidebar"])
            if "hidepo" in keys:
                self.hidePo.set(loadDict["hidepo"])
            if "hideini" in keys:
                self.hideIni.set(loadDict["hideini"])
            if "model" in keys:
                self.model.set(loadDict["model"])
            if "hidemodel" in keys:
                self.hideModel.set(loadDict["hidemodel"])
            if "prevserial" in keys:
                self.previousSerial.set(loadDict["prevserial"])
        return
    
    def Save(self) -> dict:
        saveDict : dict = super().Save()
        saveDict["prefix"] = self.prefix.get()
        saveDict["radiocustom"] = self.radioEntryVar.get()
        saveDict["po"] = self.po.get()
        saveDict["initials"] = self.initials.get()
        saveDict["serial"] = self.sn.get()
        saveDict["clear"] = self.clearSN.get()
        saveDict["hidetext"] = self.hideText.get()
        saveDict["hidebar"] = self.hideBar.get()
        saveDict["hidepo"] = self.hidePo.get()
        saveDict["hideini"] = self.hideIni.get()
        saveDict["model"] = self.model.get()
        saveDict["hidemodel"] = self.hideModel.get()
        saveDict["prevserial"] = self.previousSerial.get()
        return saveDict