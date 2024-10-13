#!/usr/bin/python
import sys, os, glob
from constants import *
from configparser import ConfigParser
import PyQt6
import gui
import tess

def main():

    if os.path.exists(CONFIG_FILE_PATH ):
        config = ConfigParser()
        config.read(CONFIG_FILE_PATH )
        MODELS_PATH = config["DEFAULT"]["path"]
        
    modelNames = tess.getTessModelNames()

    if len(modelNames) == 0:
        print("[ERR] No tesseract model found at", MODELS_PATH, file=sys.stderr)
        sys.exit(1)

    print("Available models:\n", modelNames)
    
    app = PyQt6.QtWidgets.QApplication(sys.argv)
    mainWindow = gui.ClerkGUI(modelNames)
    mainWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
