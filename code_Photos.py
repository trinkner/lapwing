# import project files
import form_Photos
import code_Enlargement

import piexif
import datetime

# import basic Python libraries
from math import floor

from functools import partial

from PyQt5.QtGui import (
    QPixmap,
    QFont,
    QIcon,
    QImage,
    QTransform
    )
    
from PyQt5.QtCore import (
    pyqtSignal,
    QSize, 
    Qt
    )
    
from PyQt5.QtWidgets import (
    QMdiSubWindow,
    QLabel,
    QPushButton, 
    QApplication,
    qApp
    )
   

class Photos(QMdiSubWindow, form_Photos.Ui_frmPhotos):
    
    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()                         
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose,True)
        self.mdiParent = ""
        self.resized.connect(self.resizeMe)        
        self.currentSpeciesList = []
        self.lblDetails.setVisible(False)
        self.filter = ()
        self.photoList = []
        self.gridPhotos.setContentsMargins(2,2,2,2)
        self.gridPhotos.setSpacing(2)
        

    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
            
    def resizeMe(self):

        windowWidth = self.width()-10
        windowHeight = self.height()     
        self.scrollArea.setGeometry(5, 27, windowWidth-5, windowHeight-35)
        self.layLists.setGeometry(0, 0, windowWidth-5, windowHeight-40)

   
    def scaleMe(self):
       
        fontSize = self.mdiParent.fontSize
        scaleFactor = self.mdiParent.scaleFactor    
        
        self.lblLocation.setFont(QFont("Helvetica", fontSize))    
        metrics = self.lblLocation.fontMetrics()                
        cboText = self.lblLocation.text()
        if cboText == "":
            cboText = "Dummy Text"
        itemTextWidth = metrics.boundingRect(cboText).width()
        itemTextHeight = metrics.boundingRect(cboText).height()
        #scale the font for all widgets in window
        for w in self.children():
            try:
                w.setFont(QFont("Helvetica", fontSize))
            except:
                pass

        self.lblLocation.setFont(QFont("Helvetica", floor(fontSize * 1.4 )))
        self.lblLocation.setStyleSheet("QLabel { font: bold }");
        self.lblLocation.setMaximumHeight(itemTextHeight)
        self.lblDateRange.setFont(QFont("Helvetica", floor(fontSize * 1.2 )))
        self.lblDateRange.setStyleSheet("QLabel { font: bold }");
        self.lblDateRange.setMaximumHeight(itemTextHeight)        
        self.lblDetails.setFont(QFont("Helvetica", floor(fontSize * 1.2 )))
        self.lblDetails.setStyleSheet("QLabel { font: bold }");
        self.lblDetails.setMaximumHeight(itemTextHeight)        
        self.lblSpecies.setFont(QFont("Helvetica", fontSize))
        self.lblSpecies.setMaximumHeight(itemTextHeight)
        
        for c in self.layLists.children():
            if "QLabel" in str(c):
                c.setFont(QFont("Helvetica", fontSize))
         
        windowWidth =  800  * scaleFactor
        if len(self.photoList) == 1:
            windowHeight = 400 * scaleFactor
        else:  
            windowHeight = 800 * scaleFactor
            
        self.resize(windowWidth, windowHeight)

                                  
    def FillPhotos(self, filter): 

        self.scaleMe()
        self.resizeMe()        
        
        # clear the grdPhotos layout, in case there was anything in there to start
        # there could be photos in there if we're doing a refresh here
        for i in reversed(range(self.gridPhotos.count())): 
            self.gridPhotos.itemAt(i).widget().setParent(None)
        
        # save the filter settings passed to this routine to the form for future use
        self.filter = filter
        
        photoSightings = self.mdiParent.db.GetSightingsWithPhotos(filter)

        if len(photoSightings) == 0:
            return False
        
        # for each sighting, iterate through attached photos and add them as a 
        # label with photo to the gridPhotos
        species = set()
        row = 0
        
        # count photos for message display
        photoCount = 0
        for s in photoSightings:
            for p in s["photos"]:
                if self.mdiParent.db.TestIndividualPhoto(p, filter):
                    photoCount += 1
                    species.add(s["commonName"])
        photoCount = str(photoCount)

        speciesCount = len(species)
        
        self.lblSpecies.setText("Species: " + str(speciesCount) + ". Photos: " + str(photoCount))
        
        self.mdiParent.SetChildDetailsLabels(self, filter)

        for s in photoSightings:

            for p in s["photos"]:
                            
                if self.mdiParent.db.TestIndividualPhoto(p, filter):
                    
                    self.mdiParent.lblStatusBarMessage.setVisible(True)
                    self.mdiParent.lblStatusBarMessage.setText("Processing photo " + str(row + 1) + " of " + photoCount)
                    
                    # p is a filename. Use it to add the image to the label as a pixmap
                    
                    # save both the photo file name and the sighting data to the photoList 
                    # enlargements will use this data in the details display
                    self.photoList.append([p, s])
                    buttonPhoto = QPushButton()
                    buttonPhoto.setMinimumHeight(281)
                    buttonPhoto.setMinimumWidth(500)
                    
                    pixMap = self.GetPixmapForThumbnail(p["fileName"])
                    
                    buttonPhoto.setIcon(QIcon(pixMap))
                    
                    buttonPhoto.setIconSize(QSize(500,281))    
                    buttonPhoto.setStyleSheet("QPushButton:pressed{ background-color: #343333; }")
                    buttonPhoto.setStyleSheet("QPushButton:hover{ background-color: #343333; }")
                    buttonPhoto.setStyleSheet("QPushButton:flat{ background-color: #343333; }")
                    buttonPhoto.setStyleSheet("QPushButton{ background-color: #343333; border:none }")
                    # set up behavior when button is clicked, passing the photo file name as p
                    buttonPhoto.clicked.connect(partial( self.showEnlargement, row))
    
                    photoWeekday = datetime.datetime(int(s["date"] [0:4]), int(s["date"] [5:7]), int(s["date"] [8:10]))
                    photoWeekday = photoWeekday.strftime("%A")
                    
                    
                    labelCaption = QLabel()
                    labelCaption.setText(
                        s["commonName"] + "\n" +
                        s["scientificName"] + "\n\n" +
                        s["location"] + "\n" +
                        photoWeekday + ", " + s["date"] + " " + s["time"] + "\n\n" +
                        "Rating: " + p["rating"]
                        )
                    labelCaption.setStyleSheet("QLabel { background-color: #343333; color: silver; padding: 3px; }")
                    
                    self.gridPhotos.addWidget(buttonPhoto, row, 0)
                    self.gridPhotos.addWidget(labelCaption, row, 1)
                    
                    # add species to species set so we can count them
                    species.add(s["commonName"])
                    
                    row = row + 1
                    
                    maxValue = self.scrollArea.verticalScrollBar().maximum()
                    self.scrollArea.verticalScrollBar().setValue(maxValue)
                    
                    qApp.processEvents()

        self.mdiParent.lblStatusBarMessage.setText("")
        self.mdiParent.lblStatusBarMessage.setVisible(False)
        
        QApplication.processEvents()

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_camera.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        
        self.scrollArea.verticalScrollBar().setValue(0)

        # don't show if we don't have any photos to show
        if len(self.photoList) == 0:
            # close our window
            self.close()

        # resie to a smaller window if we only have one photo to show
        if len(self.photoList) == 1:
            self.scaleMe()
        
        # tell MainWindow that we succeeded filling the list
        return(True)


    def GetPixmapForThumbnail(self, photoFile):
        
        photoExif = piexif.load(photoFile)
        
        try:
            pmOrientation = int(photoExif["0th"][piexif.ImageIFD.Orientation] )
        except:
            pmOrientation = 1
            
        try:
            thumbimg = photoExif["thumbnail"]
        except:
            thumbimg = None

        if thumbimg is None:
            qimage = QImage(photoFile)
        else:
            qimage = QImage()
            qimage.loadFromData(thumbimg, format='JPG')
        if pmOrientation == 2: qimage = qimage.mirrored(True,  False)
        if pmOrientation == 3: qimage = qimage.transformed(QTransform().rotate(180))
        if pmOrientation == 4: qimage = qimage.mirrored(False,  True)
        if pmOrientation == 5: 
            qimage = qimage.mirrored(True,  False)
            qimage = qimage.transformed(QTransform().rotate(270))
        if pmOrientation == 6: qimage = qimage.transformed(QTransform().rotate(90))
        if pmOrientation == 7:          
            qimage = qimage.mirrored(True,  False)
            qimage = qimage.transformed(QTransform().rotate(90))
        if pmOrientation == 8: qimage = qimage.transformed(QTransform().rotate(270))
        
        pm = QPixmap()
        pm.convertFromImage(qimage)
            
        if pm.height() > pm.width():
            pm = pm.scaledToHeight(281)
        else:
            pm = pm.scaledToWidth(500)
        return pm


    def showEnlargement(self, row):
        
        sub = code_Enlargement.Enlargement()

        # save the MDI window as the parent for future use in the child        
        sub.mdiParent = self
        sub.photoList = self.photoList
        sub.currentIndex = row
       
        # add and position the child to our MDI area
        self.mdiParent.mdiArea.addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self.mdiParent)
        sub.show()

        # call the child's routine to fill it with data
        sub.fillEnlargement()
        