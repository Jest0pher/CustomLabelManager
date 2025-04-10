class PrintPassing:
    printFunc = None

    def __init__(self):
        return
    
    def SetFunc(self, func):
        self.printFunc = func
    
    def CallFunc(self):
        self.printFunc()
   