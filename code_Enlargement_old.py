import form_Enlargement
import code_Filter
import datetime

import os
from math import floor

import piexif

from PyQt5.QtGui import (
    QPixmap,
    QPainter,
    QCursor
    )
    
from PyQt5.QtCore import (
    Qt,
    pyqtSignal,
    QTimer
    )
    
from PyQt5.QtWidgets import (
    QApplication, 
    QMdiSubWindow,
    QGraphicsView,
    QGraphicsScene,
    QMessageBox,
    QMenu,
    QLabel,
    QGroupBox,
    QHBoxLayout
    )
   

class Enlargement(QMdiSubWindow, form_Enlargement.Ui_frmEnlargement):
    
    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal() 
    
    class MyGraphicsView(QGraphicsView):
        
        def __init__(self):
            QGraphicsView.__init__(self)
            self.setRenderHints(QPainter.Antialiasing|QPainter.SmoothPixmapTransform)
            self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.mdiParent = "" 
            
            
        def wheelEvent(self,event):        
            adj = 1 + event.angleDelta().y()/120 * 0.1
            self.scale(adj, adj)

        # we need a keepress event handler here in case the user clicks on the photo.
        # when user clicks on the photo, the keypress handler is this GraphicsView, not the Englargement class.
        def keyPressEvent(self, e):
            
            # F key is pressed. Re-display the currentEnlargement to fit the screen
            if e.key() == Qt.Key_F:   
                self.mdiParent.fitEnlargement()
                
            # Backspace key is pressed, so show previous image as enlargement     
            if e.key() == Qt.Key_Backspace:
                self.mdiParent.showPreviousPhoto()
    
            # Space bar is pressed, so show next image as enlargement     
            if e.key() == Qt.Key_Space:
                self.mdiParent.showNextPhoto()

            # F7 is pressed, so toggle display of cursor
            if e.key() == Qt.Key_F7:
                self.mdiParent.toggleHideCursor()          
    
            # F9 is pressed, so toggle display of camera details 
            if e.key() == Qt.Key_F9:
                self.mdiParent.toggleCameraDetails()
    
            # F11 is pressed, so toggle display of camera details 
            if e.key() == Qt.Key_F11:
                self.mdiParent.toggleFullScreen()
    
            # Esc is pressed, so exit full screen mode, if we're in it 
            if e.key() == Qt.Key_Escape and self.mdiParent.mdiParent.mdiParent.statusBar.isVisible() is False:
                self.mdiParent.toggleFullScreen()
    
            # 1-5 pressed, so rate the photo 
            if e.key() in [Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5]:
                self.mdiParent.ratePhoto(e.key())
    
            # Right is pressed: show next photo            
            if e.key() == Qt.Key_Right:   
                self.mdiParent.showNextPhoto()               
    
            # Left is pressed: show previous photo
            if e.key() == Qt.Key_Left:   
                self.mdiParent.showPreviousPhoto()           

            
        def contextMenuEvent(self, event):
    
            QApplication.restoreOverrideCursor()           

            menu = QMenu(self)
            menu.setStyleSheet("color:silver; background-color: #343333;")
            
            actionFitToWindow = menu.addAction("Fit to window (F)")
            menu.addSeparator()
            actionShowNextPhoto = menu.addAction("Next photo (Right arrow)")
            actionShowPreviousPhoto = menu.addAction("Previous photo (Left arrow)")
            menu.addSeparator()
            if self.mdiParent.isMaximized() is True:
                actionToggleHideCursor = menu.addAction("Toggle hide cursor (F7)")
            actionToggleCameraDetails = menu.addAction("Show/Hide details (F9)")
            actionToggleFullScreen = menu.addAction("Toggle full screen (F11)")
            menu.addSeparator()
            actionDetachFile = menu.addAction("Detach photo from Yearbird")
            menu.addSeparator()
            actionDeleteFile = menu.addAction("Delete photo from file system")
            
            action = menu.exec_(self.mapToGlobal(event.pos()))

            if action == actionFitToWindow:
                self.parent().fitEnlargement()

            if action == actionShowNextPhoto:
                self.parent().showNextPhoto()
            
            if action == actionShowPreviousPhoto:
                self.parent().showPreviousPhoto()

            if action == actionToggleCameraDetails:
                self.parent().toggleCameraDetails()
                
            if action == actionToggleFullScreen:
                self.parent().toggleFullScreen()

            if action == actionDeleteFile:
                self.parent().deleteFile()
                
            if action == actionDetachFile:
                self.parent().detachFile() 

            if self.mdiParent.isMaximized() is True:                
                if action == actionToggleHideCursor:
                    self.parent().toggleHideCursor() 
                
                                                 
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.resized.connect(self.resizeMe)        
        self.mdiParent = ""
        self.photoList = []
        self.currentIndex = 0
        self.pixmapEnlargement = QPixmap()
        self.cameraDetails = QLabel()
        self.layout().addWidget(self.cameraDetails)
        self.layout().setDirection(1)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.cursorIsVisible = True

        self.cameraDetails.setStyleSheet("color:silver; background-color: #343333; padding: 3px")                
        self.cameraDetails.setVisible(False)

#         # create horizontal layout to show rating stars
#         self.horizontalGroupBox = QGroupBox("Rating")
#         self.layout().addWidget(self.horizontalGroupBox)
#         ratingLayout = QHBoxLayout()
#         
#         star1 = QLabel()
#         star1.setPixmap(QPixmap(":/icon_star.png"))
#         # star1.clicked.connect(self.on_click)
#         ratingLayout.addWidget(star1)
#         
#         star2 = QLabel()
#         star2.setPixmap(QPixmap(":/icon_star.png"))
#         # star1.clicked.connect(self.on_click)
#         ratingLayout.addWidget(star2)

        
#         self.horizontalGroupBox.setLayout(ratingLayout)
        


    def resizeEvent(self, event):
        #routine to handle window resize event        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
            
    def resizeMe(self):
        
        QTimer.singleShot(5, self.fitEnlargement)
        
        
    def scaleMe(self):
        
        return
        

    def keyPressEvent(self, e):

        # F key is pressed. Re-display the currentEnlargement to fit the screen
        if e.key() == Qt.Key_F:   
            self.fitEnlargement()
            
        # Backspace key is pressed, so show previous image as enlargement     
        if e.key() == Qt.Key_Backspace:
            self.showPreviousPhoto()

        # Space bar is pressed, so show next image as enlargement     
        if e.key() == Qt.Key_Space:
            self.showNextPhoto()

        # F7 is pressed, so toggle display of cursor
        if e.key() == Qt.Key_F7:
            self.toggleHideCursor()       

        # F9 is pressed, so toggle display of camera details 
        if e.key() == Qt.Key_F9:
            self.toggleCameraDetails()

        # F11 is pressed, so toggle display of camera details 
        if e.key() == Qt.Key_F11:
            self.toggleFullScreen()

        # Esc is pressed, so exit full screen mode, if we're in it 
        if e.key() == Qt.Key_Escape and self.mdiParent.mdiParent.statusBar.isVisible() is False:
            self.toggleFullScreen()

        # 1-5 pressed, so rate the photo 
        if e.key() in [Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4, Qt.Key_5]:
            self.ratePhoto(e.key())

        # Right is pressed: show next photo            
        if e.key() == Qt.Key_Right:   
            self.showNextPhoto()               

        # Left is pressed: show previous photo
        if e.key() == Qt.Key_Left:   
            self.showPreviousPhoto()               
             

            
    def ratePhoto(self, ratingKey):
                
        if ratingKey == Qt.Key_0:
            self.photoList[self.currentIndex][0]["rating"] = "0"
        if ratingKey == Qt.Key_1:
            self.photoList[self.currentIndex][0]["rating"] = "1"
        if ratingKey == Qt.Key_2:
            self.photoList[self.currentIndex][0]["rating"] = "2"
        if ratingKey == Qt.Key_3:
            self.photoList[self.currentIndex][0]["rating"] = "3"
        if ratingKey == Qt.Key_4:
            self.photoList[self.currentIndex][0]["rating"] = "4"
        if ratingKey == Qt.Key_5:
            self.photoList[self.currentIndex][0]["rating"] = "5"
            
        self.setCameraDetails()
        self.cameraDetails.setVisible(True)
        self.mdiParent.mdiParent.db.photosNeedSaving = True
                                                

    def showPreviousPhoto(self):
            
        if self.currentIndex > 0:
            self.currentIndex = self.currentIndex - 1            
        
        if self.currentIndex >= 0:                
            self.changeEnlargement()   
    
    
    def showNextPhoto(self):
                
        if self.currentIndex < len(self.photoList) - 1:            
            self.currentIndex += 1            
            self.changeEnlargement()
            
                                  
    def fillEnlargement(self): 
        
        # routine uses self.currentIndex to fill the right photo
        self.pixmapEnlargement = QPixmap(self.photoList[self.currentIndex][0]["fileName"])                 
            
        self.sceneEnlargement= QGraphicsScene()
        # save the item ID of the pixmap so we can replace the pixmap photo easily later
        self.itemPixmap = self.sceneEnlargement.addPixmap(self.pixmapEnlargement)

        self.viewEnlargement = self.MyGraphicsView() 
        self.viewEnlargement.mdiParent = self               
        self.viewEnlargement.setScene(self.sceneEnlargement)
        self.viewEnlargement.setStyleSheet("QWidget{ background-color: #343333;}")
        
        # add viewEnlargementto the default layout of the form
        self.layout().addWidget(self.viewEnlargement)
        
        self.setCameraDetails()               
                       
        self.setPhotoTitle()  
                   
        QTimer.singleShot(10, self.fitEnlargement) 
        

    def changeEnlargement(self):
        
        self.pixmapEnlargement = QPixmap(self.photoList[self.currentIndex][0]["fileName"])                 

        self.itemPixmap.setPixmap(self.pixmapEnlargement)
        
        self.setCameraDetails()
        
        self.setPhotoTitle()
        
        QTimer.singleShot(10, self.fitEnlargement)   
                

    def fitEnlargement(self):
        
        # scale the view to fit the photo, edge to edge
        self.viewEnlargement.setSceneRect(0, 0, self.pixmapEnlargement.width(), self.pixmapEnlargement.height())
        self.viewEnlargement.fitInView(self.viewEnlargement.sceneRect(), Qt.KeepAspectRatio)
                
        
    def setPhotoTitle(self):
        
        # display the file name in the window title bar
        basename = os.path.basename(self.photoList[self.currentIndex][0]["fileName"])
        self.setWindowTitle(basename) 
        
        
    def toggleCameraDetails(self):
        
        # toggle visibility of cameraDetails
        if self.cameraDetails.isVisible():
            self.cameraDetails.setVisible(False)
        else:
            self.cameraDetails.setVisible(True)
            
        QTimer.singleShot(10, self.fitEnlargement)   


    def toggleHideCursor(self):
        
        # toggle visibility of the cursor
        if self.cursorIsVisible is True:
            QApplication.setOverrideCursor(QCursor(Qt.BlankCursor))
            self.cursorIsVisible = False
        else:
            QApplication.restoreOverrideCursor()
            self.cursorIsVisible = True   
        

    def detachFile(self):
        
        # remove photo from database, but don't delete it from file system
        msgText = "Detach \n\n" + self.photoList[self.currentIndex][0]["fileName"] + "\n\n from Yearbird?"
        msgText = msgText + "\n\n(File will NOT be deleted from file system)"
        
        msg = QMessageBox()
        msg.setText(msgText)
        msg.setWindowTitle("Detach photo?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        buttonClicked = msg.exec_()
        
        if buttonClicked == QMessageBox.Yes:
                
            # remove photo from database
            currentPhoto = self.photoList[self.currentIndex][0]["fileName"]
            photoCommonName = self.photoList[self.currentIndex][1]["commonName"]
            photoLocation = self.photoList[self.currentIndex][1]["location"] 
            
            self.mdiParent.mdiParent.db.removePhotoFromDatabase(photoLocation, "", "", photoCommonName, currentPhoto)             
            
            # remove photo from current window's photo list
            self.photoList.remove(self.photoList[self.currentIndex])

            # refresh display of parent photo list
            self.mdiParent.FillPhotos(self.mdiParent.filter)
            
            # advance display to next photo
            if len(self.photoList) == 0:
                self.close()
                
            if self.currentIndex < len(self.photoList):                        
                self.changeEnlargement()            
            
            else:
                self.currentIndex -= 1
                self.changeEnlargement()
                                        
            # set flag for requiring photo file save
            self.mdiParent.mdiParent.db.photosNeedSaving = True

            
    def deleteFile(self):
        
        # remove photo from database, but don't delete it from file system
        msgText = "Permanently delete \n\n" + self.photoList[self.currentIndex][0]["fileName"] + "\n\n from Yearbird and the file system?"
        
        msg = QMessageBox()
        msg.setText(msgText)
        msg.setWindowTitle("Permanently delete photo?")
        msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        buttonClicked = msg.exec_()
        
        if buttonClicked == QMessageBox.Yes:
                
            # remove photo from database
            currentPhoto = self.photoList[self.currentIndex][0]["fileName"]
            photoCommonName = self.photoList[self.currentIndex][1]["commonName"]
            photoLocation = self.photoList[self.currentIndex][1]["location"] 
            
            self.mdiParent.mdiParent.db.removePhotoFromDatabase(photoLocation, "", "", photoCommonName, currentPhoto)             
            
            # remove photo from current window's photo list
            self.photoList.remove(self.photoList[self.currentIndex])

            # advance display to next photo
            if len(self.photoList) == 0:
                self.close()
                
            if self.currentIndex < len(self.photoList):                        
                self.changeEnlargement()            
            
            else:
                self.currentIndex -= 1
                self.changeEnlargement()
                                        
            # set flag for requiring photo file save
            self.mdiParent.mdiParent.db.photosNeedSaving = True  
            
            # delete file from file system
            if os.path.isfile(currentPhoto):
                try:
                    os.remove(currentPhoto)
                except:
                    pass

            # refresh display of parent photo list
            self.mdiParent.FillPhotos(self.mdiParent.filter)
                          
            
    def toggleFullScreen(self):
        
        
        # toggle visibility of filter and menu bar
        if self.mdiParent.mdiParent.dckFilter.isVisible() is True:
            
            self.mdiParent.mdiParent.dckFilter.setVisible(False)
            self.mdiParent.mdiParent.dckPhotoFilter.setVisible(False)
            self.mdiParent.mdiParent.menuBar.setVisible(False)
            self.mdiParent.mdiParent.toolBar.setVisible(False)
            self.mdiParent.mdiParent.statusBar.setVisible(False)
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.mdiParent.mdiParent.showFullScreen()
            self.showMaximized()
            
            
        else:
            
            self.mdiParent.mdiParent.dckFilter.setVisible(True)
            self.mdiParent.mdiParent.dckPhotoFilter.setVisible(True)
            self.mdiParent.mdiParent.menuBar.setVisible(True)
            self.mdiParent.mdiParent.toolBar.setVisible(True)
            self.mdiParent.mdiParent.statusBar.setVisible(True)
            self.mdiParent.mdiParent.showNormal()
            self.mdiParent.mdiParent.showMaximized()
            self.setWindowFlags(Qt.SubWindow)
            self.showNormal()
            QApplication.restoreOverrideCursor()           
            

        QTimer.singleShot(10, self.fitEnlargement)   

            
    def setCameraDetails(self):
        
        currentPhoto = self.photoList[self.currentIndex][0]["fileName"]
        photoRating = self.photoList[self.currentIndex][0]["rating"]
        
        photoCommonName = self.photoList[self.currentIndex][1]["commonName"]
        photoScientificName = self.photoList[self.currentIndex][1]["scientificName"]
        photoLocation = self.photoList[self.currentIndex][1]["location"]
        
        # get EXIF data
        
        try:
            exif_dict = piexif.load(currentPhoto)
        except:
            exif_dict = ""
        
        # get photo date from EXIF
        try:
            photoDateTime = exif_dict["Exif"][piexif.ExifIFD.DateTimeOriginal].decode("utf-8")
            
            #parse EXIF data for date/time components
            photoExifDate = photoDateTime[0:4] + "-" + photoDateTime[5:7] + "-" + photoDateTime[8:10]
            photoExifTime = photoDateTime[11:13] + ":" + photoDateTime[14:16]
            
            photoWeekday = datetime.datetime(int(photoDateTime[0:4]), int(photoDateTime[5:7]), int(photoDateTime[8:10]))
            photoWeekday = photoWeekday.strftime("%A") + ", "
            
        except:
            photoExifDate = "Date unknown"
            photoExifTime = "Time unknown"
            photoWeekday = ""
            
        try:
            photoExifModel = exif_dict["0th"][piexif.ImageIFD.Model].decode("utf-8")
        except:
            photoExifModel = ""
        try:
            photoExifLensModel = exif_dict["Exif"][piexif.ExifIFD.LensModel].decode("utf-8")
        except:
            photoExifLensModel = ""
        
        try:        
            photoExifExposureTime = exif_dict["Exif"][piexif.ExifIFD.ExposureTime]
            photoExifExposureTime = "1/" + str(floor(photoExifExposureTime[1] / photoExifExposureTime[0])) + " sec"
        except:
            photoExifExposureTime = ""

        try:
            photoExifAperture = exif_dict["Exif"][piexif.ExifIFD.FNumber]
            photoExifAperture = round(photoExifAperture[0] / photoExifAperture[1], 1)
        except:
            photoExifAperture = ""
            
        try:
            photoExifISO = exif_dict["Exif"][piexif.ExifIFD.ISOSpeedRatings]
        except:
            photoExifISO = ""
        
        try:
            photoExifFocalLength = exif_dict["Exif"][piexif.ExifIFD.FocalLength]
            photoExifFocalLength = floor(photoExifFocalLength[0] / photoExifFocalLength[1])
            photoExifFocalLength = str(photoExifFocalLength) + " mm"
            
        except:
            photoExifFocalLength = ""
            
        detailsText = photoCommonName + "\n"
        detailsText = detailsText + photoScientificName + "\n"
        detailsText = detailsText + "\n"
        detailsText = detailsText + photoLocation + "\n"
        detailsText = detailsText + "Date: " + photoWeekday + photoExifDate + "\n"
        detailsText = detailsText + "Time: " + photoExifTime + "\n"
        detailsText = detailsText + "\n"
        detailsText = detailsText + "Camera: " + photoExifModel + "\n"
        detailsText = detailsText + "Lens: " + photoExifLensModel + "\n"
        detailsText = detailsText + "Focal Length: " + str(photoExifFocalLength) + "\n"
        detailsText = detailsText + "Exposure: " + str(photoExifExposureTime) + "\n"
        detailsText = detailsText + "Aperture: " + str(photoExifAperture) + "\n"
        detailsText = detailsText + "ISO: " + str(photoExifISO) + "\n\n"
        detailsText = detailsText + "Rating: " + photoRating

        self.cameraDetails.setText(detailsText)
        
        