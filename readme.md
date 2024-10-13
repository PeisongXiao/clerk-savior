# 🌟 Clerk-Savior

Clerk Savior is a desktop application written in Python that helps you manage your images and PDFs files with Tesseract.

## Features

- 📂 **Open Image and PDF Files**: open your img/pdf files for processing.
- 📄 **Navigate Through Pages**: Move through pages in PDFs and images.
- ✏️ **Extract Text**: Select specific areas to extract text.
- 📝 **Rename Files**: Use customizable patterns to rename files.
- 👩‍💻 **User-Friendly Interface**: Designed for ease of use.
- 📊 **Manage File Names**: View and manage file names in a table format.

## Requirements

Before you install Clerk Savior, ensure that you have the following software installed on your system:

- **Python**: Clerk Savior is written using Python. You can download it from [python.org](https://www.python.org/downloads/).

- **Tesseract OCR**: Language models (`.traineddata` files) are necessary for Tesseract to recognize text in different languages. You can find these files in the tessdata repository: [tessdata repository](https://github.com/tesseract-ocr/tessdata).

  To ensure Tesseract is installed correctly, run the following command in your terminal or command prompt:

  ```bash
  tesseract --version
  ```
- Choose the language(s) you wish to use:
For example, if you only want to recognize English in your files, download eng.traineddata only.
- **Poppler**: Poppler is required to convert PDF files into images (used by the pdf2image library).
You can download Poppler from https://github.com/oschwartz10612/poppler-windows
To ensure Tesseract is installed correctly, run the following command in your terminal or command prompt:

```bash
pdftoppm -v
```

Set Environment Variables (if needed):
After installation, ensure that the Tesseract executable and Poppler are in your system's PATH.

## Dependencies
Clerk Savior requires several Python packages to function correctly. These can be installed using `pip`. The necessary packages are:

- **PyQt6**: For the graphical user interface.
- **NumPy**: For handling  data and image processing.
- **Pillow**: For image manipulation.
- **OpenCV**: For advanced image processing.
- **pdf2image**: To convert PDF files into images.
- **ConfigParser**: For handling configuration files.

To install the required packages, run the following command in your terminal or command prompt:

```bash
pip install opencv-python pillow pytesseract pdf2image
```
## Usage
To launch the application, run the following command in your terminal or command prompt:
```bash
python clerk-savior.py
```

## Instructions

1. **Launch the Application**:
   - Open the Clerk Savior application by running `python clerk-savior.py`.

2. **Open a PDF or Image**:
   - Double click on the display panel to select and open a file.
   - Or click on the "Open Image" button to open image file, or click the "Open PDF" button to open a PDF document.

3. **Set the Renaming Pattern**:
   - In the **Pattern Box**, enter the expected naming pattern for the files. Use placeholders like `$0$, $1$, $2$, etc., to represent different elements from the file.


4. **Extract Text from the Image**:
   - !!! Make sure the language selected at the top right corner is the language in the file
   - Click on the cell where you want the extracted text to appear.
   - Click on the display panel to select the area containing the text.
   - Release the mouse button to extract and display the text in the selected cell.

5. **Zoom In and Out**:
   - Use the scroll wheel while holding down the `Ctrl` key to zoom in and out of the image displayed in the panel.

6. **Rename Files**:
   - Make sure the new File names are filled, then click the "Rename All Files" button to rename all the files

7. **Navigate PDF Pages (if applicable)**:
   - If you opened a PDF, use the "Next Page" button to navigate through the pages of the document.
