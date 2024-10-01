#!/usr/bin/python
import sys, os, glob
import PyQt6
import gui
import tess

def main():
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
