import subprocess
import os
import time
import win32api
import win32print

command = "^XA^PW599^LL299^FO11,47^A0N,41,41^FB599,1,0,L,0^FDS/N: GFJC37VGLKKT^FS^FO35,94^BY2^BCN,60,Y,N,N,A^FDGFJC37VGLKKT^FS^FO47,247^A0N,35,35^FB354,1,0,L,0^FDPO: 3609^FS^FO436,247^A0N,47,47^FB354,1,0,L,0^FDJRF^FS^FO47,200^A0N,35,35^FB354,1,0,L,0^FDModel: A2190^FS^XZ^XA^PW599^LL299^FO11,47^A0N,41,41^FB599,1,0,L,0^FDS/N: GX8C4JZYJQH4^FS^FO35,94^BY2^BCN,60,Y,N,N,A^FDGX8C4JZYJQH4^FS^FO47,247^A0N,35,35^FB354,1,0,L,0^FDPO: 3609^FS^FO436,247^A0N,47,47^FB354,1,0,L,0^FDJRF^FS^FO47,200^A0N,35,35^FB354,1,0,L,0^FDModel: A2084^FS^XZ^XA^PW599^LL299^FO11,47^A0N,41,41^FB599,1,0,L,0^FDS/N: GFJC1R2EJQH3^FS^FO35,94^BY2^BCN,60,Y,N,N,A^FDGFJC1R2EJQH3^FS^FO47,247^A0N,35,35^FB354,1,0,L,0^FDPO: 3609^FS^FO436,247^A0N,47,47^FB354,1,0,L,0^FDJRF^FS^FO47,200^A0N,35,35^FB354,1,0,L,0^FDModel: A2083^FS^XZ"
output = subprocess.run(["ZPL2PDF","-z", command,"-o","Jesse Label Manager/ZPL2PDF/output/","-n","mylabel.pdf"], executable="Jesse Label Manager/ZPL2PDF/ZPL2PDF.exe")



pdf_path = "C:/Users/jesse/Documents/GitHub/CustomLabelManager/Jesse Label Manager/ZPL2PDF/output/mylabel.pdf"
printer_name = "Brother QL-710W Wireless"

original_printer = win32print.GetDefaultPrinter()

# Set the target printer as default temporarily
win32print.SetDefaultPrinter(printer_name)
        
# Execute the print command via Windows Shell
win32api.ShellExecute(0, "print", pdf_path, None, ".", 0)
        
time.sleep(5)

win32print.SetDefaultPrinter(original_printer)
