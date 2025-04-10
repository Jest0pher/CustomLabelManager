from GlobalImport import *
from Custom import CustomLabel
from zebrafy import ZebrafyZPL
from PIL import Image

class ZebraPrinter:
    z : Zebra
    label : CustomLabel

    def __init__(self):
        self.z = Zebra()

    def SetCurrentPrinter(self,var):
        self.z.setqueue(var)

    def SetLabel(self, label : CustomLabel):
        self.label = label
        self.label.testObserve.SetFunc(self.Print)

    def Print(self):
        data = self.label.GetPrintData()
        print(data)
        self.z.output(data)