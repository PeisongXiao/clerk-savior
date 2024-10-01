# Change this if tesseract or ClerkGUI can't find any data
MODELS_PATH = '/usr/share/tessdata/'

# Sane values for scaling
SCALE_MIN     = 0.2
SCALE_MAX     = 5.0
SCALE_DEFAULT = 1.0
SCALE_DELTA   = 8 * 360 * 1

# Sane values for text recognition
WIDTH_MIN  = 10
HEIGHT_MIN = 10

# Table info
TABLE_COL_CNT        = 4
TABLE_COL_ADD        = 0
TABLE_COL_DEL        = 1
TABLE_COL_FILE_NAME  = 2
TABLE_COL_ITEM_START = 3
# Last column is reserved for generated file name
TABLE_HEADERS = ["Add Col", "  Del  ", "File Name", "New File Name"]
