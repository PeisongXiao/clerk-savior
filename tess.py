############################################################
### Project: coin
### File: tess.py
### Description: handles all pytesseract-related operations
### Version: 1.0
############################################################
import sys, os, glob
import cv2
from PIL import Image
import pytesseract
from constants import *

# getTessModelNames(modelsPath): automatically finds all available
#  language models in modelsPath
def getTessModelNames(modelsPath=MODELS_PATH):
    models_list = glob.glob(modelsPath + "*.traineddata")
    model_names = []
    for path in models_list:
        base_name = os.path.basename(path)
        base_name = os.path.splitext(base_name)[0]
        model_names.append(base_name)
    return model_names

# image2Text(model, croppedImage): use the model with the name
#  model to try to recognize the text in croppedImage
def image2Text(model, croppedImage):
    gray = cv2.cvtColor(croppedImage, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 1)
    crop = Image.fromarray(gray)
    text = pytesseract.image_to_string(crop, lang=model).strip()
    return text
