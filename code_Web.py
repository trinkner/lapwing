# import the GUI forms that we create with Qt Creator
import form_Web
import code_MapHtml

# import the Qt components we'll use
# do this so later we won't have to clutter our code with references to parent Qt classes 

from PyQt5.QtGui import (
    QCursor,
    QIcon,
    QPixmap
    )
    
from PyQt5.QtCore import (
    Qt,
    QUrl,
    pyqtSignal,
    QIODevice,
    QByteArray,
    QBuffer
    )    
    
from PyQt5.QtWidgets import (
    QApplication,  
    QMdiSubWindow
    )

from math import (
    floor
    )

from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
    QWebEngineSettings,
    )

from collections import (
    defaultdict
    )

import base64


class Web(QMdiSubWindow, form_Web.Ui_frmWeb):
    
    resized = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""
        self.setWindowIcon(QIcon(QPixmap(1,1)))
        self.contentType = "Web Page"
        self.resized.connect(self.resizeMe)   
        self.webView = QWebEngineView(self)
        self.webView.setObjectName("webView")
        self.webView.loadFinished.connect(self.LoadFinished)
        self.webView.loadProgress.connect(self.showLoadProgress)
        self.title = ""


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
            
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)
        self.webView.setGeometry(5, 27, windowWidth - 10, windowHeight-35)
        if self.contentType == "Map":
            self.webView.adjustSize()
            self.LoadLocationsMap(self.filter)
   
   
    def html(self):
    
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        html = """
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <body>
            """
        
        myPixmap = self.webView.grab()
        myPixmap = myPixmap.scaledToWidth(600, Qt.SmoothTransformation)

        myByteArray = QByteArray()
        myBuffer = QBuffer(myByteArray)
        myBuffer.open(QIODevice.WriteOnly)
        myPixmap.save(myBuffer, "PNG")

        encodedImage = base64.b64encode(myByteArray)
        
        html = html + ("""
        <img src="data:image/png;base64, 
        """)
        
        html = html + str(encodedImage)[1:]
        
        html = html + ("""
            <font size>
            </body>
            </html>
            """)
        
        QApplication.restoreOverrideCursor()   
        
        return(html)
        
       
    def scaleMe(self):
       
        fontSize = self.mdiParent.fontSize
        settings = QWebEngineSettings.globalSettings()
        settings.setFontSize(QWebEngineSettings.DefaultFontSize, floor(fontSize * 1.6))        
        
        scaleFactor = self.mdiParent.scaleFactor
        windowWidth =  800 * scaleFactor
        windowHeight = 580 * scaleFactor            
        self.resize(windowWidth, windowHeight)


    def loadAboutLapwing(self):
        
        self.title= "About Lapwing"
        
        self.contentType = "About"
                    
        html = """

            <!DOCTYPE html>
            <html>
            <head>
            <title>About Lapwing</title>
            <meta charset="utf-8">
            <style>
            * {
                font-family: "Times New Roman", Times, serif;
                }
            </style>
            </head>
            <body>
            <h1>
            Lapwing
            </h1>
            """
        
        html = html + "<h3>Version: " + self.mdiParent.versionNumber + "</h3>"
        html = html + "<h3>Date: " + self.mdiParent.versionDate+ "</h3>"
        
        html = html + """
            <font size='4'>            
            <b>
            Lapwing is a free, open-source application to analyze personal eBird sightings. 
            <br><br>
            Created by Richard Trinkner.             
            </b>
            <h3>
            Licenses
            </h3>
            <p>
            <ul>
            <li>
            Lapwing is licensed under the GNU General Public License, version 3.
            </li>
            <li>
            PyQt, by Riverbank Computing, is licensed under the GNU General Public License.
            </li>
            <li>
            Map base layers are retrieved from Google.
            </li>            
            <li>
            Map layers that include points and location labels are generated using OpenLayers. OpenLayers is free, Open Source JavaScript, released under the 2-clause BSD License (also known as the FreeBSD).
            </li>
            <li>
            PyInstaller, by the PyInstaller Development Team, Giovanni Bajo and McMillan Enterprise, is licensed under the GPL General Public License.
            </li>
            </ul>
            </font size>
            </body>
            </html>        
            """
        
        self.webView.setHtml(html)
                
        self.setWindowTitle("About Lapwing")

        return(True)


    def LoadWebPage(self,  url):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.webView.load(QUrl(url))
        self.resizeMe()
        self.scaleMe()
        
        
    def LoadFinished(self):
        QApplication.restoreOverrideCursor()

        
    def LoadLocationsMap(self, filter):
        
        self.title= "Location Map"
        
        coordinatesDict = defaultdict()
        mapWidth =  self.frameGeometry().width() -10
        mapHeight = self.frameGeometry().height() -35
        self.scrollArea.setGeometry(5, 27, mapWidth + 2, mapHeight + 2)
        self.webView.setGeometry(5, 27, mapWidth + 2, mapHeight + 2)        
        self.contentType = "Map"
        self.filter = filter
        
        locations = self.mdiParent.db.GetLocations(filter)
        
        if len(locations) == 0:
            return(False)
        
        for l in locations:
            coordinates = self.mdiParent.db.GetLocationCoordinates(l)
            coordinatesDict[l] = coordinates

        thisMap = code_MapHtml.MapHtml()
        thisMap.mapHeight = mapHeight
        thisMap.mapWidth = mapWidth
        thisMap.coordinatesDict = coordinatesDict
        
        html = thisMap.html()
        
        self.webView.setHtml(html)
        
        # set window title to descriptive map name
        
        locationName = filter.getLocationName()                         # str   name of region or location  or ""
        locationType = filter.getLocationType()
        startDate = filter.getStartDate()                                           # str   format yyyy-mm-dd  or ""
        endDate = filter.getEndDate()                                               # str   format yyyy-mm-dd  or ""
        startSeasonalMonth = filter.getStartSeasonalMonth() # str   format mm
        startSeasonalDay = filter.getStartSeasonalDay()            # str   format dd
        endSeasonalMonth  = filter.getEndSeasonalMonth()    # str   format  dd
        endSeasonalDay  = filter.getEndSeasonalDay()               # str   format dd
        speciesName = filter.getSpeciesName()                           # str   speciesName
        family = filter.getFamily()                                                         # str family name
        
        # set main location label, using "All Locations" if none others are selected
        
        windowTitle = speciesName
        
        if locationName != "":
            if locationType == "Country":
                locationName = self.mdiParent.db.GetCountryName(locationName)
            if locationType == "State":
                locationName = self.mdiParent.db.GetStateName(locationName)
            windowTitle = windowTitle + "; " + locationName
        
        if startDate != "":
            dateTitle = startDate + " to " + endDate
            if startDate == endDate:
                dateTitle = startDate
            windowTitle = windowTitle + "; " + dateTitle

        # set main seasonal range label, if specified
        if not ((startSeasonalMonth == "") or (endSeasonalMonth == "")):
            monthRange = ["Jan",  "Feb",  "Mar",  "Apr", "May",   "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec"]
            rangeTitle = monthRange[int(startSeasonalMonth)-1] + "-" + startSeasonalDay + " to " + monthRange[int(endSeasonalMonth)-1] + "-" + endSeasonalDay
            windowTitle = windowTitle + "; " + rangeTitle
        
        if family != "":
            family = family[0:family.index("(") - 1]
            windowTitle = windowTitle + "; " + family
            
        if windowTitle  == "":
            windowTitle  = "All species, locations, dates and families"
            
        #remove leading "; " if needed
        if windowTitle[0:2] == "; ":
            windowTitle = windowTitle [2:]
            
        # add location count to window title
        windowTitle = "Map: " + windowTitle + " (" + str(len(coordinatesDict.keys())) + ")"
        
        self.setWindowTitle(windowTitle) 
        self.title = windowTitle
       
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_map.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon) 
                
        return(True)


    def showLoadProgress(self, percent):
        
        if percent < 100:
            self.setWindowTitle(self.title + ": " + str(percent) + "%")
        else:
            self.setWindowTitle(self.title)

