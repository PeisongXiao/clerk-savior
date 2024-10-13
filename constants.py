from configparser import ConfigParser
import os
import glob

# Load the Tesseract model path from the configuration file if it exists.
# Otherwise, use the default model path.
if os.path.exists("clerk.cfg"):
    config = ConfigParser()
    config.read("clerk.cfg")
    MODELS_PATH = config["DEFAULT"]["path"]
    traineddataFiles = glob.glob(os.path.join(MODELS_PATH, "*.traineddata"))
    if not traineddataFiles:
        MODELS_PATH = '/usr/share/tessdata/'
else:
    MODELS_PATH = '/usr/share/tessdata/' # default for linux system

# Sane values for scaling
SCALE_MIN     = 0.2          # Minimum scaling factor for images
SCALE_MAX     = 5.0          # Maximum scaling factor for images
SCALE_DEFAULT = 1.0          # Default scaling factor
SCALE_DELTA   = 8 * 360 * 1  # Amount to scale

# Sane values for text recognition
WIDTH_MIN  = 10              # Minimum width for text recognition
HEIGHT_MIN = 10              # Minimum height for text recognition

# Table info
TABLE_COL_CNT        = 4     # Total number of columns in the table
TABLE_COL_ADD        = 0     # Column index for "Add Col"
TABLE_COL_DEL        = 1     # Column index for "DEL"
TABLE_COL_FILE_NAME  = 2     # Column index for "File Name"
TABLE_COL_ITEM_START = 3     # start index for new column names
# Last column is reserved for generated file name
TABLE_HEADERS = ["Add Col", "  Del  ", "File Name", "New File Name"]
