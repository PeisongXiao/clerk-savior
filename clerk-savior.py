#!/usr/bin/python
############################################################
### Project: clerk-savior
### File: clerk-savior.py
### Description: serves as the entry point for the Clerk-Savior application
### Version: 1.0
############################################################
import sys, os, glob
from constants import *
import PyQt6
import gui
import tess

def main():

    # retrive avaliable model Names
    modelNames = tess.getTessModelNames()

    # check if any models avaliable
    # Suggest changing the path in clerk.cfg if this error occurs
    if len(modelNames) == 0:
        print("[ERR] No tesseract model found at", MODELS_PATH, file=sys.stderr)
        sys.exit(1)

    print("Available models:\n", modelNames)

    #initialization
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    mainWindow = gui.ClerkGUI(modelNames)
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
