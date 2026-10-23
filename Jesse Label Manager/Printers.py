from GlobalImport import *
from Custom import CustomLabel
from zebrafy import ZebrafyZPL
from PIL import Image

import os
import shutil
import subprocess
import time
from pathlib import Path


class PrinterManager:
    z : Zebra
    label : CustomLabel
    isZebra : bool = True


    def __init__(self):
        self.z = Zebra()

    def SetCurrentPrinter(self,var):
        self.z.setqueue(var)

    def SetIsZebra(self, isZebra: bool):
        self.isZebra = isZebra
        print(f"SetIsZebra called with value: {isZebra}")

    def SetLabel(self, label : CustomLabel):
        self.label = label
        self.label.testObserve.SetFunc(self.Print)

    def Print(self):
        data = self.label.GetPrintData()
        print(data)
        if self.isZebra:
            self.z.output(data)
        else:
            self.CreateAndPrintPDF(data)

    def CreateAndPrintPDF(self, zpl_data: str):
        # Convert ZPL to PDF using the bundled ZPL2PDF app.
        script_dir = Path(sys.executable).resolve().parent
        output_dir = directory
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf_path = output_dir / "outputLabel.pdf"
        exe_path = script_dir / "ZPL2PDF" / "ZPL2PDF"

        subprocess.run(["chmod", "+x", str(exe_path)], check=True)

        if not exe_path.exists():
            raise FileNotFoundError(f"ZPL2PDF executable not found: {exe_path}")

        tempW = self.label.width
        tempH = self.label.height
        if self.label.mm == "in":
            tempW = tempW / 25.4
            tempH = tempH / 25.4
        subprocess.run(
            [
                str(exe_path),
                "-z",
                zpl_data,
                "-w",
                tempW.__str__(),
                "-h",
                tempH.__str__(),
                "-u",
                self.label.mm,
                "-o",
                str(output_dir),
                "-d",
                "300",
                "-n",
                pdf_path.name,
            ],
            check=True,
        )

        print(f"PDF saved to: {pdf_path}")

        # Print the PDF to the default printer
        if os.name == "nt":
            import win32api
            import win32print

            original_printer = win32print.GetDefaultPrinter()
            win32print.SetDefaultPrinter(self.z.getqueues()[0])
            win32api.ShellExecute(0, "print", str(pdf_path), None, ".", 0)
            win32print.SetDefaultPrinter(original_printer)
            print(f"Sent {pdf_path} to printer: {self.z.getqueues()[0]}")
        lp_cmd = shutil.which("lp")
        lpr_cmd = shutil.which("lpr")
        if not lp_cmd and not lpr_cmd:
            print(
                f"Printer '{self.z.getqueues()[0]}' is not available on this system. "
                f"PDF was still generated at {pdf_path}."
            )
        media_option = f"Custom.{tempW}x{tempH}{self.label.mm}"
        for command_args in (
            [
                lp_cmd or "lp",
                "-d",
                self.z.getqueues()[0],
                "-o",
                f"media={media_option}",
                "-o",
                "fit-to-page",
                "-o",
                "outputorder=reverse",
                "-o",
                "CutMedia=EndOfJob",
                "-o",
                "page-left=12",
                str(pdf_path),
            ]
            if lp_cmd
            else None,
            [
                lpr_cmd or "lpr",
                "-P",
                self.z.getqueues()[0],
                "-o",
                f"media={media_option}",
                "-o",
                "fit-to-page",
                "-o",
                "outputorder=reverse",
                "-o",
                "CutMedia=EndOfJob",
                "-o",
                "page-left=12",
                str(pdf_path),
            ]
            if lpr_cmd
            else None,
        ):
            if not command_args:
                continue

            result = subprocess.run(command_args, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Sent {pdf_path} to printer: {self.z.getqueues()[0]}")
                return

        print(
            f"Printer '{self.z.getqueues()[0]}' was not found or is not configured. "
            f"PDF remains available at {pdf_path}."
        )