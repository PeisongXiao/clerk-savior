import cv2, os, sys
import numpy
from PIL import Image
import PyQt6
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
from PyQt6 import QtCore, QtGui, QtWidgets
import glob
from constants import *
import tess
import gc
from pdf2image import convert_from_path
from io import BytesIO

class ClerkGUI(QtWidgets.QMainWindow):
    # initialization 
    # requires: modelNames must be valid and not empty
    def __init__(self, modelNames):
        print("Initializing GUI...")

        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('clerk.ui', self)

        # connect buttons in the UI to functions
        self.ui.openImage.clicked.connect(self.openImageFile) # "Open Image" button
        self.ui.openPDF.clicked.connect(self.openPDFFile) # "Open PDF" button
        self.ui.nextPage.clicked.connect(self.nextImage) # "Next Page" button
        self.ui.batchProcess.clicked.connect(self.process) # "Process file names" button
        self.ui.batchRename.clicked.connect(self.rename) # "Rename all files" button

        # Rubber Band and Mouse tracking 
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self) 
        self.ui.viewPanel.setMouseTracking(True)
        self.ui.viewPanel.installEventFilter(self)
        self.ui.viewPanel.setAlignment(PyQt6.QtCore.Qt.AlignmentFlag.AlignTop)

        if len(modelNames) == 0:
            print("[ERR] No tesseract model(s) given to ClerkGUI!",
                  file=sys.stderr)
            sys.exit(1)

        # Tersseract Model initialization 
        self.modelNames = modelNames
        self.updateModel(self.modelNames[0])
        self.models.addItems(self.modelNames)
        self.models.currentTextChanged.connect(self.updateModel)
        self.models.setCurrentIndex(self.modelNames.index(self.model))

        # Set up for image and display 
        self.imageList  = []
        self.pixmapList = []
        self.imageIndex = 0
        self.imageScale = SCALE_DEFAULT
        
        # Set up for table 
        self.items = QStandardItemModel()
        self.itemsTable.setModel(self.items)
        self.items.setColumnCount(TABLE_COL_CNT)

        self.setTableHeader()
        print("Initialized new table!")

    #  openImageFile(): prompts to open an image, if an error occurrs, the
    #  image within the photo view will not be updated, otherwise, the
    #  image will be updated and stored in self.pixmapList
    def openImageFile(self):
        self.imageList  = []
        self.imageIndex = 0
        self.pixmapList = []
        self.imageScale = SCALE_DEFAULT
        gc.collect()      # free up large chucks of memory
        
        filename = QFileDialog.getOpenFileName(self, 'Select File',
                                               filter="Images (*.jpeg *.jpg *.png)")
            
        if filename[0] == "":
            print("No file was selected or opened!")
            return None

        print("Opening file: ", filename[0])
        self.imageList.append(cv2.imread(str(filename[0])))

        if self.imageList[0] is None:
            print("Error: image is empty!", file=sys.stderr)
            print("No file was opened!")
            return None
        
        # Convert the image for display 
        frame = cv2.cvtColor(self.imageList[0], cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0],
                       frame.strides[0], QImage.Format.Format_RGB888)
        
        # add to pixmap list and update view 
        self.pixmapList.append(QPixmap.fromImage(image))
        self.imageScale = SCALE_DEFAULT
        self.updateView()

        self.statusBar().showMessage("Opened file: " + filename[0])

        self.newRow(self.items.rowCount(), filename[0])
        
        return None
    
    # openPDFFile(): Prompts the user to open a PDF file. if an error occurs exists, 
    # image within the photo view will not be updated. Otherwise, each page of the PDF is converted to
    # an image and stored in self.pixmapList, the first page will be  displayed.
    def openPDFFile(self):
        self.imageList  = []
        self.imageIndex = 0
        self.pixmapList = []
        self.imageScale = SCALE_DEFAULT
        gc.collect()      # free up large chucks of memory
        
        filename = QFileDialog.getOpenFileName(self, 'Select File',
                                               filter="PDF (*.pdf)")
        if filename[0] == "":
            print("No file was selected or opened!")
            return None

        print("Opening file: ", filename[0])
        pages = convert_from_path(filename[0], fmt="jpeg")

        # convert each page to an image 
        for page in pages:
            with BytesIO() as ftmp:
                page.save(ftmp, format="JPEG")
                ftmp.seek(0)
                frame = numpy.array(Image.open(ftmp))
                image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                self.imageList.append(image)
                image = QImage(frame, frame.shape[1], frame.shape[0],
                               frame.strides[0], QImage.Format.Format_RGB888)
                self.pixmapList.append(QPixmap.fromImage(image))
  
        del pages
        gc.collect()

        self.imageScale = SCALE_DEFAULT
        self.updateView()

        self.statusBar().showMessage("Opened file: " + filename[0])
        
        self.newRow(self.items.rowCount(), filename[0])

        return None

    # setTableHeader(): sets the headers and create the "Add" button in the table
    # for adding new columns
    def setTableHeader(self):
        for i in range(TABLE_COL_CNT):
            item = QStandardItem(TABLE_HEADERS[i])
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setEditable(False)
            self.items.setItem(0, i, item)

        addButton = QPushButton("Add Col")
        self.itemsTable.setIndexWidget(self.items.index(0, 0), addButton)
        addButton.clicked.connect(self.addCol)

        self.itemsTable.resizeColumnsToContents()

    # updateView(): update the current image with the new scale
    # requires: The image is loaded into the pixmapList
    def updateView(self):
        self.ui.viewPanel.setPixmap(self.pixmapList[self.imageIndex].scaled(
            int(self.imageScale * self.pixmapList[self.imageIndex].width()),
            int(self.imageScale * self.pixmapList[self.imageIndex].height())))

        print("Photo scale set to:", self.imageScale)
        self.statusBar().showMessage("Photo scale set to: " + str(self.imageScale))

    # delRow(): delete the row where the "Del" button was clicked
    def delRow(self):
        button = self.sender()
        index  = self.itemsTable.indexAt(button.pos())
        self.items.removeRow(index.row())
        print("Removed row", index.row())
        self.statusBar().showMessage("Removed row " + str(index.row()))

    # addRow(): add a row under the row where the button was clicked
    def addRow(self):
        button = self.sender()
        index  = self.itemsTable.indexAt(button.pos())
        self.newRow(index.row() + 1, "")

    # newRow(): creates a new row in the table with the filenames and buttons.
    def newRow(self, row, fileName):
       
        items = [QStandardItem("") for i in range(self.items.columnCount())]
        self.items.insertRow(row, items)
        self.items.setItem(row, TABLE_COL_FILE_NAME, QStandardItem(fileName))
        self.populateButtons(row)
        print("Added new row", row)
        self.statusBar().showMessage("Added new row " + str(row))

    # nameRow(): creates a new file name based on the pattern from the patternBox and
    # and data from multiple columns
    # example: the pattern in patternBox is file_$0$_$1$.jpg
    # And the first two columns have "image" and "01",
    # the generated file name will be "file_image_01.jpg".
    def nameRow(self, row):
        fileName = str(self.patternBox.text())
        for i in range(self.items.columnCount() - TABLE_COL_CNT):
            fileName = fileName.replace("$" + str(i) + "$",
                                        self.items.item(row,
                                                        TABLE_COL_ITEM_START + i).
                                        text())
        self.items.setItem(row, self.items.columnCount() - 1,
                           QStandardItem(fileName))

    # process(): generates a new file name for each row 
    def process(self):
        for i in range(1, self.items.rowCount()):
            self.nameRow(i)
        return None

    # rename(): iterates through each row in the table, and renames the files
    def rename(self):
        for i in range(1, self.items.rowCount()):
            originalPath = self.items.item(i, TABLE_COL_FILE_NAME).text()
            newPath      = os.path.join(os.path.dirname(originalPath),
                                        self.items.item(
                                            i, self.items.columnCount() - 1).text())
            # for windows system only
            if os.name == 'nt':  
                newPath= newPath.replace("\\",'/')
                
            os.rename(originalPath, newPath)
        return None
    
    # addCol(): Adds a new column to the table
    def addCol(self):
        item = QStandardItem(str(self.items.columnCount() - TABLE_COL_CNT))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        items = [item]
        items.extend([QStandardItem("") for i in range(self.items.rowCount() - 1)])
        self.items.insertColumn(self.items.columnCount() - 1, items)

    # populateButtons(): put buttons on the table when creating a new row
    # with "Del" button linked to delRow() and "Add Row" linked to addRow() function
    def populateButtons(self, row):
        delButton  = QPushButton("Del")
        self.itemsTable.setIndexWidget(
            self.items.index(row, TABLE_COL_DEL),
            delButton)
        delButton.clicked.connect(self.delRow)

        addButton = QPushButton("Add Row")
        self.itemsTable.setIndexWidget(
            self.items.index(row, TABLE_COL_ADD),
            addButton)
        addButton.clicked.connect(self.addRow)

    # updateModel(): update self.model to the one selected
    def updateModel(self, value):
        self.model = value
        print("Model selected as:", self.model)

    # eventFilter(source, event): Handles different types of events occurs 
    # in the view panel. And depending on the type of event, different functions are called to 
    # handle it
    # return type: bool
    # -  True if the event has been handled
    # -  False if the evenet cannot be processed 
    def eventFilter(self, source, event):
        # 1: press mouse over the view panel
        if (event.type() == QEvent.Type.MouseButtonPress and
            source is self.ui.viewPanel):
            self.rubberBandShow(event) # draw the rubber band
            return True
        # 2: move the mouse over the view panel
        elif (event.type() == QEvent.Type.MouseMove and
              source is self.ui.viewPanel and self.rubberBand.isVisible()):
            self.rubberBandRedraw(event) #adjust the size of rubber band
            return True
        # 3: release the mouse 
        elif (event.type() == QEvent.Type.MouseButtonRelease and
              source is self.ui.viewPanel and self.rubberBand.isVisible()):
            return self.rubberBandSelect(event)# finalize and process the selected area
        # 4: Wheel: rezie the image 
        elif (event.type() == QEvent.Type.Wheel and
              self.imageList is not [] and source is self.ui.viewPanel and
              QApplication.keyboardModifiers() ==
              Qt.KeyboardModifier.ControlModifier): # zoom in/out the image
            self.imageResize(event)
            return True
        # 5: open a new image when double click on the view panel
        elif (event.type() == QEvent.Type.MouseButtonDblClick and
              source is self.ui.viewPanel):
            self.openImageFile() # open a new image file
            return True
        return False

    # rubberBandShow(event): shows the rubber band for selection
    def rubberBandShow(self, event):
        self.org = self.mapFromGlobal(event.globalPosition())
        self.top_left = event.position()
        self.rubberBand.setGeometry(QRect(self.org.toPoint(), QSize()))
        self.rubberBand.show()

    # rubberBandRedraw(event): resizes the rubber band for selection
    def rubberBandRedraw(self, event):
        pos = self.mapFromGlobal(event.globalPosition()).toPoint()
        pos = QPoint(int(max(pos.x(), 0)), int(max(pos.y(), 0)))
        self.rubberBand.setGeometry(QRect(self.org.toPoint(), pos).normalized())

    # rubberBandSelect(event): finalize the rubber band selection. This function processes 
    # the selected area
    # Returns type: bool
    # - True if a valid area is selected and text extraction is successful.
    # - False if no valid area is selected or if the selection dimensions is too small
    def rubberBandSelect(self, event):
        pos = event.position()
        self.top_left = QPoint(int(max(min(pos.x(), self.top_left.x()), 0)),
                               int(max(min(pos.y(), self.top_left.y()), 0)))

        self.rubberBand.hide()
        
        # caculates the selected area 
        rect = self.rubberBand.geometry()
        self.x1 = int(self.top_left.x() / self.imageScale)
        self.y1 = int(self.top_left.y() / self.imageScale)
        width = rect.width() / self.imageScale
        height = rect.height() / self.imageScale
        self.x2 = int(self.x1 + width)
        self.y2 = int(self.y1 + height)

        if (width >= WIDTH_MIN and height >= HEIGHT_MIN and
            self.imageList is not []):
            print("Cropped image:", self.x1, self.y1, self.x2, self.y2)
            crop = self.imageList[self.imageIndex][self.y1:self.y2, self.x1:self.x2] 

            # extract the text from the selected area 
            text = tess.image2Text(self.model, crop)
            print("Text selected:", text)
            self.statusBar().showMessage("Text selected: " + text)
            self.addText(text)
            return True

        return False

    # addText(text): adds the extracted text to the selected cell in the table.
    # inserts the given text into the selected table cell.  If no valid cell is selected, or
    # multiple cell selected, display error message
    def addText(self, text):
        indexes = self.itemsTable.selectionModel().selectedIndexes()
        for idx in indexes:
            if idx.row() == 0:
                indexes.remove(idx)

        if indexes == []:
            self.statusBar().showMessage("You must select a valid tile!")
            return None

        if len(indexes) != 1:
            self.statusBar().showMessage("You must select only one valid tile!")
            return None

        self.items.setItem(indexes[0].row(), indexes[0].column(),
                           QStandardItem(text))
        return None

    # imageResize(event): resize the image when scrolling with Ctrl
    def imageResize(self, event):
        self.imageScale = self.imageScale + event.angleDelta().y() / SCALE_DELTA

        if self.imageScale < SCALE_MIN:
            self.imageScale = SCALE_MIN
        
        if self.imageScale > SCALE_MAX:
            self.imageScale = SCALE_MAX
            
        self.updateView()

    # nextImage(): loop to the next image in imageList
    def nextImage(self):
        self.imageScale = SCALE_DEFAULT
        self.imageIndex = (self.imageIndex + 1) % len(self.imageList)
        self.updateView()
        return None
