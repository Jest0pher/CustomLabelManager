from GlobalImport import *
from Custom import CustomLabel

class QTYLabel(CustomLabel):
    qty : StringVar
    qtyBox : ttk.Entry

    clearSN : BooleanVar
    clearButton : Checkbutton

    def __init__(self, master, width : float, height : float, mm : str, startColumn : int=0, startRow : int=0, initials = "", po = "") -> None:
        super().__init__(master=master, width=width, mm=mm, height=height, startColumn=startColumn, startRow=startRow)

        self.ConstructWindow(startColumn=startColumn, startRow=startRow)

    def ConstructWindow(self, startColumn : int=0, startRow : int=0):
        self.qty = StringVar()
        ttk.Label(self.frame,text="QTY").grid(column=startColumn,row=startRow+1)
        self.qtyBox = ttk.Entry(self.frame,textvariable=self.qty)
        self.qtyBox.grid(column=startColumn+1,row=startRow+1)
        
        self.clearSN = BooleanVar()
        ttk.Label(self.frame, text="Clear After Print").grid(column=startColumn+2, row=startRow)
        self.clearButton = ttk.Checkbutton(self.frame, variable=self.clearSN)
        self.clearButton.grid(column=startColumn+2, row=startRow+1)
        self.root.protocol("WM_TAKE_FOCUS", self.WindowFocused)
        self.DisplayPrintButton(startColumn+1, startRow+2)

    def WindowFocused(self, event):
        if event.widget in [self.root, self.clearButton]:
            self.qtyBox.focus_set()

    def SetLabelData(self):
        self.l = zpl.Label(self.height,self.width, 11.8)
        self.l.origin(2, 7)
        self.l.write_text("QTY:" + self.qty.get(), char_height=16, char_width=10, line_width=50, justification='L')
        self.l.endorigin()

    def GetPrintData(self, setData :bool = True) -> str:
        super()
        if setData:
            self.SetLabelData()
        return self.l.dumpZPL()
    
    def PrintTrigger(self):
        super().PrintTrigger()
        if self.clearSN.get() == True:
            self.qty.set("")