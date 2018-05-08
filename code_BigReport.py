# import project files
import form_BigReport
import code_Filter
import code_Location
import code_Individual
import code_Lists

# import basic Python libraries
from copy import deepcopy
from collections import defaultdict
from math import floor
import base64

from PyQt5.QtGui import (
    QCursor,
    QFont,
    )
    
from PyQt5.QtCore import (
    Qt,
    QVariant,
    QUrl,
    pyqtSignal,
    QIODevice,
    QByteArray,
    QBuffer
    )
    
from PyQt5.QtWidgets import (
    QApplication, 
    QTableWidgetItem, 
    QHeaderView,
    QMdiSubWindow,
    )
    
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
)


class BigReport(QMdiSubWindow, form_BigReport.Ui_frmBigReport):

    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()  
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""
        self.myHtml = ""
        self.resized.connect(self.resizeMe)                
        self.lstDates.currentRowChanged.connect(self.FillSpeciesForDate)
        self.lstLocations.currentRowChanged.connect(self.FillSpeciesForLocation)
        self.lstLocations.doubleClicked.connect(lambda: self.CreateLocation(self.lstLocations))
        self.tblNewLocationSpecies.itemDoubleClicked.connect(lambda: self.CreateLocation(self.tblNewLocationSpecies))        
        self.lstDates.doubleClicked.connect(lambda: self.CreateSpeciesList(self.lstDates))
        self.lstSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.lstSpecies))
        self.lstLocationSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.lstLocationSpecies))
        self.lstLocationUniqueSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.lstLocationUniqueSpecies))
        self.lstNewLifeSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.lstNewLifeSpecies))
        self.tblNewYearSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.tblNewYearSpecies))
        self.tblNewMonthSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.tblNewMonthSpecies))
        self.tblNewCountrySpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.tblNewCountrySpecies))
        self.tblNewStateSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.tblNewStateSpecies))
        self.tblNewCountySpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.tblNewCountySpecies))
        self.tblNewLocationSpecies.doubleClicked.connect(lambda: self.CreateIndividual(self.tblNewLocationSpecies))
        self.tblSpecies.doubleClicked.connect(self.TblSpeciesClicked)
        
        # right-click menu actions to widgets as appropriate
        self.tblSpecies.addAction(self.actionSetSpeciesFilter)
        self.tblSpecies.addAction(self.actionSetFirstDateFilter)
        self.tblSpecies.addAction(self.actionSetLastDateFilter)
        self.lstLocations.addAction(self.actionSetLocationFilter)
        self.lstDates.addAction(self.actionSetDateFilter)
        self.lstSpecies.addAction(self.actionSetSpeciesFilter)        
        self.lstLocationSpecies.addAction(self.actionSetSpeciesFilter)
        self.lstLocationUniqueSpecies.addAction(self.actionSetSpeciesFilter)
        self.lstNewLifeSpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewYearSpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewYearSpecies.addAction(self.actionSetDateFilterToYear)
        self.tblNewMonthSpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewMonthSpecies.addAction(self.actionSetDateFilterToMonth)
        self.tblNewCountrySpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewCountrySpecies.addAction(self.actionSetLocationFilter)
        self.tblNewStateSpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewStateSpecies.addAction(self.actionSetLocationFilter)
        self.tblNewCountySpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewCountySpecies.addAction(self.actionSetLocationFilter)
        self.tblNewLocationSpecies.addAction(self.actionSetSpeciesFilter)
        self.tblNewLocationSpecies.addAction(self.actionSetLocationFilter)
        
        # connect right-click actions to methods
        self.actionSetDateFilter.triggered.connect(self.setDateFilter)
        self.actionSetFirstDateFilter.triggered.connect(self.setFirstDateFilter)
        self.actionSetLastDateFilter.triggered.connect(self.setLastDateFilter)
        self.actionSetSpeciesFilter.triggered.connect(self.setSpeciesFilter)
        self.actionSetCountryFilter.triggered.connect(self.setLocationFilter)
        self.actionSetStateFilter.triggered.connect(self.setLocationFilter)
        self.actionSetCountyFilter.triggered.connect(self.setLocationFilter)
        self.actionSetLocationFilter.triggered.connect(self.setLocationFilter)       
        self.actionSetDateFilterToYear.triggered.connect(self.setDateFilter)
        self.actionSetDateFilterToMonth.triggered.connect(self.setDateFilter)

        self.webMap = QWebEngineView(self.tabMap)
        self.webMap.setUrl(QUrl("about:blank"))
        self.webMap.setObjectName("webMap")
        
        self.tabAnalysis.setCurrentIndex(0)
        self.speciesList = []        
        self.filter = code_Filter.Filter()
        self.filteredSightingList = []
        
        
    def CreateLocation(self,  callingWidget):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if callingWidget.objectName() == "lstLocations":
            locationName = callingWidget.currentItem().text()
        if callingWidget.objectName() == "tblNewLocationSpecies":
            locationName = callingWidget.item(callingWidget.currentRow(),  0).text()
            if callingWidget.currentColumn() != 0:
                QApplication.restoreOverrideCursor()     
                return
        sub = code_Location.Location()
        sub.mdiParent = self.mdiParent
        sub.FillLocation(locationName)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        QApplication.restoreOverrideCursor()     
    
    def CreateIndividual(self,  callingWidget):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if callingWidget.objectName() in (["lstSpecies", 
                                                                            "lstLocationSpecies", 
                                                                            "lstLocationUniqueSpecies", 
                                                                            "lstNewLifeSpecies"
                                                                            ]):
            species = callingWidget.currentItem().text()
        if callingWidget.objectName() in (["tblNewYearSpecies", 
                                                                            "tblNewMonthSpecies", 
                                                                            "tblNewCountrySpecies", 
                                                                            "tblNewStateSpecies", 
                                                                            "tblNewCountySpecies", 
                                                                            "tblNewLocationSpecies"
                                                                            ]):
            species = callingWidget.item(callingWidget.currentRow(),  1).text()
            if callingWidget.currentColumn() != 1:
                QApplication.restoreOverrideCursor()     
                return
        sub = code_Individual.Individual()
        sub.mdiParent = self.mdiParent
        sub.FillIndividual(species)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        sub.resizeMe()
        QApplication.restoreOverrideCursor()     
    
    def CreateSpeciesList(self,  callingWidget):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if callingWidget.objectName() == "lstDates":
            date = callingWidget.currentItem().text()
        
        filter = code_Filter.Filter()
        filter.setStartDate(date)
        filter.setEndDate(date)
        
        sub = code_Lists.Lists()
        sub.mdiParent = self.mdiParent
        sub.FillSpecies(filter)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        QApplication.restoreOverrideCursor()          
        
    def FillAnalysisReport(self, filter):
        # save filter for later use
        self.filter = filter
        
        # create subset of master sightings list for this filter
        self.filteredSightingList = deepcopy(self.mdiParent.db.GetSightings(filter))
        filteredSightingList = self.filteredSightingList
        
        # ****Setup Species page****
        # get species and first/last date data from db 
        speciesListWithDates = self.mdiParent.db.GetSpeciesWithData(filter,  self.filteredSightingList,  "Subspecies")
       
       # abort if filter produced no sightings
        if len(speciesListWithDates) == 0:
            return(False)
       
       # set up tblSpecies column headers and widths
        self.tblSpecies.setColumnCount(4)
        self.tblSpecies.setRowCount(len(speciesListWithDates))
        self.tblSpecies.horizontalHeader().setVisible(True)
        self.tblSpecies.setHorizontalHeaderLabels(['Tax', 'Species', 'First',  'Last'])
        header = self.tblSpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblSpecies.setShowGrid(False)

        # add species and dates to table row by row        
        R = 0
        for species in speciesListWithDates:    
            taxItem = QTableWidgetItem()
            taxItem.setData(Qt.DisplayRole, R+1)
            speciesItem = QTableWidgetItem()
            speciesItem.setText(species[0])
            speciesItem.setData(Qt.UserRole,  QVariant(species[4]))                            
            firstDateItem = QTableWidgetItem()
            firstDateItem.setData(Qt.DisplayRole, species[1])
            lastDateItem = QTableWidgetItem()
            lastDateItem.setData(Qt.DisplayRole, species[2])
            self.tblSpecies.setItem(R, 0, taxItem)    
            self.tblSpecies.setItem(R, 1, speciesItem)
            self.tblSpecies.setItem(R, 2, firstDateItem)
            self.tblSpecies.setItem(R, 3, lastDateItem)

            self.speciesList.append(species[4])
            
            R = R + 1

        # ****Setup Dates page****
        listDates = self.mdiParent.db.GetDates(filter,  filteredSightingList)
        self.lstDates.addItems(listDates)
        self.lstDates.setSpacing(2)
        if len(listDates) > 0:
            self.lstDates.setCurrentRow(0)
            self.FillSpeciesForDate()

        # ****Setup Locations page****
        listLocations = self.mdiParent.db.GetLocations(filter, "OnlyLocations",   filteredSightingList)
        for l in listLocations:
            self.lstLocations.addItem(l)
        self.lstLocations.setSpacing(2)
        if len(listLocations) > 0:
            self.lstLocations.setCurrentRow(0)
            self.FillSpeciesForLocation()
            self.lblLocations.setText("Locations (" + str(len(listLocations)) + ")")

        # ****Setup New Species for Dates page****
        speciesListFilter = code_Filter.Filter()
        speciesListFilter.setSpeciesList(self.speciesList)
        sightingListForSpeciesSubset = self.mdiParent.db.GetSightings(speciesListFilter)
        
        yearSpecies = self.mdiParent.db.GetNewYearSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset)
        lifeSpecies=  self.mdiParent.db.GetNewLifeSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset)
        monthSpecies = self.mdiParent.db.GetNewMonthSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset)
        
       # set up tblNewYearSpecies column headers and widths
        self.tblNewYearSpecies.setColumnCount(2)
        self.tblNewYearSpecies.setRowCount(len(yearSpecies)+1)
        self.tblNewYearSpecies.horizontalHeader().setVisible(False)
        header = self.tblNewYearSpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblNewYearSpecies.setShowGrid(False)

        if len(yearSpecies) > 0:
            R = 1
            for ys in yearSpecies:
                yearItem = QTableWidgetItem()
                yearItem.setText(ys[0])
                newYearSpeciesItem = QTableWidgetItem()
                newYearSpeciesItem.setText(ys[1])
                self.tblNewYearSpecies.setItem(R, 0, yearItem)    
                self.tblNewYearSpecies.setItem(R, 1, newYearSpeciesItem)
                R = R + 1
            self.tblNewYearSpecies.removeRow(0)
            
        self.lblNewYearSpecies.setText("New year species (" + str(len(yearSpecies)) + ")")
            
       # set up tblNewMonthSpecies column headers and widths
        self.tblNewMonthSpecies.setColumnCount(2)
        self.tblNewMonthSpecies.setRowCount(len(monthSpecies)+1)
        self.tblNewMonthSpecies.horizontalHeader().setVisible(False)
        header = self.tblNewMonthSpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblNewMonthSpecies.setShowGrid(False)

        if len(monthSpecies) > 0:
            R = 1
            for ms in monthSpecies:
                monthItem = QTableWidgetItem()
                monthItem.setText(ms[0])
                newMonthSpeciesItem = QTableWidgetItem()
                newMonthSpeciesItem.setText(ms[1])
                self.tblNewMonthSpecies.setItem(R, 0, monthItem)    
                self.tblNewMonthSpecies.setItem(R, 1, newMonthSpeciesItem)
                R = R + 1
            self.tblNewMonthSpecies.removeRow(0)
            
        self.lblNewMonthSpecies.setText("New month species (" + str(len(monthSpecies)) + ")")
            
       # set up lstNewLifeSpecies 
        if len(lifeSpecies) > 0:
            self.lstNewLifeSpecies.addItems(lifeSpecies)
            self.lstNewLifeSpecies.setSpacing(2)

        self.lblNewLifeSpecies.setText("New life species (" + str(len(lifeSpecies)) + ")")

        # ****Setup new Location Species page****
        countrySpecies = self.mdiParent.db.GetNewCountrySpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        stateSpecies = self.mdiParent.db.GetNewStateSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        countySpecies = self.mdiParent.db.GetNewCountySpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        locationSpecies = self.mdiParent.db.GetNewLocationSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        
        # set up tblNewCountrySpecies column headers and widths
        self.tblNewCountrySpecies.setColumnCount(2)
        self.tblNewCountrySpecies.setRowCount(len(countrySpecies))
        self.tblNewCountrySpecies.horizontalHeader().setVisible(False)
        header = self.tblNewCountrySpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblNewCountrySpecies.setShowGrid(False)

        if len(countrySpecies) > 0:
            R = 0
            for ms in countrySpecies:
                countryItem = QTableWidgetItem()
                countryItem.setText(self.mdiParent.db.GetCountryName(ms[0]))
                newCountrySpeciesItem = QTableWidgetItem()
                newCountrySpeciesItem.setText(ms[1])
                self.tblNewCountrySpecies.setItem(R, 0, countryItem)    
                self.tblNewCountrySpecies.setItem(R, 1, newCountrySpeciesItem)
                R = R + 1
            
        self.lblNewCountrySpecies.setText("New country species (" + str(len(countrySpecies)) + ")")

        # set up tblNewStateSpecies column headers and widths
        self.tblNewStateSpecies.setColumnCount(2)
        self.tblNewStateSpecies.setRowCount(len(stateSpecies))
        self.tblNewStateSpecies.horizontalHeader().setVisible(False)
        header = self.tblNewStateSpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblNewStateSpecies.setShowGrid(False)

        if len(stateSpecies) > 0:
            R = 0
            for ms in stateSpecies:
                stateItem = QTableWidgetItem()
                stateItem.setText(self.mdiParent.db.GetStateName(ms[0]))
                newStateSpeciesItem = QTableWidgetItem()
                newStateSpeciesItem.setText(ms[1])
                self.tblNewStateSpecies.setItem(R, 0, stateItem)    
                self.tblNewStateSpecies.setItem(R, 1, newStateSpeciesItem)
                R = R + 1
            self.tblNewStateSpecies.sortByColumn(0, Qt.AscendingOrder)
            
        self.lblNewStateSpecies.setText("New state species (" + str(len(stateSpecies)) + ")")

        # set up tblNewCountySpecies column headers and widths
        self.tblNewCountySpecies.setColumnCount(2)
        self.tblNewCountySpecies.setRowCount(len(countySpecies))
        self.tblNewCountySpecies.horizontalHeader().setVisible(False)
        header = self.tblNewCountySpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblNewCountySpecies.setShowGrid(False)

        if len(countySpecies) > 0:
            R = 0
            for ms in countySpecies:
                countyItem = QTableWidgetItem()
                countyItem.setText(ms[0])
                newCountySpeciesItem = QTableWidgetItem()
                newCountySpeciesItem.setText(ms[1])
                self.tblNewCountySpecies.setItem(R, 0, countyItem)    
                self.tblNewCountySpecies.setItem(R, 1, newCountySpeciesItem)
                R = R + 1
            
        self.lblNewCountySpecies.setText("New county species (" + str(len(countySpecies)) + ")")
        
        # set up tblNewLocationSpecies column headers and widths
        self.tblNewLocationSpecies.setColumnCount(2)
        self.tblNewLocationSpecies.setRowCount(len(locationSpecies))
        self.tblNewLocationSpecies.horizontalHeader().setVisible(False)
        header = self.tblNewLocationSpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblNewLocationSpecies.setShowGrid(False)

        if len(locationSpecies) > 0:
            R = 0
            for ms in locationSpecies:
                locationItem = QTableWidgetItem()
                locationItem.setText(ms[0])
                newLocationSpeciesItem = QTableWidgetItem()
                newLocationSpeciesItem.setText(ms[1])
                self.tblNewLocationSpecies.setItem(R, 0, locationItem)    
                self.tblNewLocationSpecies.setItem(R, 1, newLocationSpeciesItem)
                R = R + 1
            
        self.lblNewLocationSpecies.setText("New location species (" + str(len(locationSpecies)) + ")")

        # ****Setup window's main labels****
        # set main species seen lable text
        count = self.mdiParent.db.CountSpecies(self.speciesList)
        
        self.lblTopSpeciesSeen.setText("Species seen: " + str(count))
        
        # set main location label, using "All Locations" if none others are selected
        self.mdiParent.SetChildDetailsLabels(self, filter)

        self.setWindowTitle(self.lblLocation.text() + ": " + self.lblDateRange.text())

        if self.lblDetails.text() != "":
            self.lblDetails.setVisible(True)
        else:
            self.lblDetails.setVisible(False)

        self.resizeMe()        
        self.scaleMe()
 
        return(True)
        

    def FillSpeciesForDate(self):
        # create temporary filter for query with nothing but needed date
        self.lstSpecies.clear()
        date = self.lstDates.currentItem().text()
        
        tempFilter = code_Filter.Filter()
        
        tempFilter.setStartDate(date)
        tempFilter.setEndDate(date)
        
        speciesList = self.mdiParent.db.GetSpecies(tempFilter,  self.filteredSightingList)
        
        self.lstSpecies.addItems(speciesList)
        self.lstSpecies.setSpacing(2)
        
        self.lblSpeciesSeen.setText("Species seen on selected date (" + str(len(speciesList)) + "):")
    

    def FillMap(self):
        
        coordinatesDict = defaultdict()
        mapWidth = self.width() -20
        mapHeight = self.height() - self.lblLocation.height() - (self.lblDateRange.height() * 7.5)
        self.webMap.setGeometry(5, 5, mapWidth, mapHeight)

        for l in range(self.lstLocations.count()):
            locationName = self.lstLocations.item(l).text()
            coordinates = self.mdiParent.db.GetLocationCoordinates(locationName)
            coordinatesDict[locationName] = coordinates
            
        mapHtml = """

            <!DOCTYPE html>
            <html>
            <head>
            <title>Locations Map</title>
            <meta name="viewport" content="initial-scale=1.0">
            <meta charset="utf-8">
            <style>            
            * {
                font-size: 75%;
                font-family: "Times New Roman", Times, serif;
                }
            #map {
                height: 100%;
                }
            html, body {
            """
        mapHtml = mapHtml + "height: " + str(mapHeight -10) + "px;"
        mapHtml = mapHtml + "width: " + str(mapWidth -10)  + "px;"
            
        mapHtml = mapHtml + """
                margin: 0;
                padding: 0;
                }
            </style>
            </head>
            <body>
            <div id="map"></div>
            <script>
            var map;

            function initMap() {
                map = new google.maps.Map(document.getElementById('map'), {
                    zoom: 5
                });
                
                var bounds = new google.maps.LatLngBounds();
                """
        for c in coordinatesDict.keys():
            mapHtml = mapHtml + """
                var marker = new google.maps.Marker({
                """
            mapHtml = mapHtml + "position: {lat: " + coordinatesDict[c][0] + ", lng: " + coordinatesDict[c][1] + "},"
            
            mapHtml = mapHtml + """
                    map: map,
                    title: '"""
            mapHtml = mapHtml + c
            mapHtml = mapHtml + """'
                    }); 
                bounds.extend(marker.getPosition());                    
                
            """    
        mapHtml = mapHtml + """
            
                map.setCenter(bounds.getCenter());
                
                map.fitBounds(bounds);
            }
            
            </script>
            <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDjVuwWvZmRlD5n-Jj2Jh_76njXxldDgug&callback=initMap" async defer></script>
            </body>
            </html>        
            """
        # save mapHtml in object's variable so we can reload it later
        self.mapHtml = mapHtml
                
        # pass the mapHtml we created to the QWebView widget for display                    
        self.webMap.setHtml(self.mapHtml)
        

    
    def FillSpeciesForLocation(self):
        # create temporary filter for query with nothing but needed location
        location = self.lstLocations.currentItem().text()
        
        tempFilter = code_Filter.Filter()
        tempFilter.setLocationType("Location")
        tempFilter.setLocationName(location)

        speciesList = self.mdiParent.db.GetSpecies(tempFilter,  self.filteredSightingList)
        
        self.lstLocationSpecies.clear()
        self.lstLocationSpecies.addItems(speciesList)
        self.lstLocationSpecies.setSpacing(2)
        
        uniqueSpecies = self.mdiParent.db.GetUniqueSpeciesForLocation(
            self.filter,
            location,  
            speciesList,  
            self.filteredSightingList
            )
            
        self.lstLocationUniqueSpecies.clear()
        self.lstLocationUniqueSpecies.addItems(uniqueSpecies)
        self.lstLocationUniqueSpecies.setSpacing(2)
        
        self.lblLocationSpecies.setText("Species at selected location (" + str(len(speciesList)) + ")")
        self.lblLocationUniqueSpecies.setText("Species seen ONLY at selected location (" + str(len(uniqueSpecies)) + ")")


    def TblSpeciesClicked(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        currentColumn = self.tblSpecies.currentColumn()
        currentRow = self.tblSpecies.currentRow()
        
        tempFilter = deepcopy(self.filter)
        
        if currentColumn == 0:
            # the taxonomy order column was clicked, so abort. We won't create a report.
            # turn off the hourglass cursor before exiting
            QApplication.restoreOverrideCursor()     
            return
                        
        if currentColumn == 1:
            # species column has been clicked so create individual window for that species
            species = self.tblSpecies.item(currentRow,  1).data(Qt.UserRole)
            sub = code_Individual.Individual()
            sub.FillIndividual(species)
        
        sub.mdiParent = self.mdiParent
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show() 
        sub.resizeMe()
        
        if currentColumn > 1:
            # date column has been clicked so create species list frame for that dateArray
            # use same start and end date for new filter to show just the single day
            date = self.tblSpecies.item(currentRow,  currentColumn).text()
            tempFilter.setStartDate(date)
            tempFilter.setEndDate(date)
            
            sub = code_Lists.Lists()
            sub.FillSpecies(tempFilter)

        QApplication.restoreOverrideCursor() 
        

    def html(self):
    
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # create start to basic html format
        html = """
            <!DOCTYPE html>
            <html>
            <head>
            </head>
            <style>
            * {
                font-size: 75%;
                font-family: "Times New Roman", Times, serif;
                }
            th {
                text-align: left;
            }
            </style>
            <body>
            """
        
        # add title information
        html = html + (
            "<H1>" + 
            self.lblLocation.text() + 
            "</H1>"
            )
        
        html = html + (
            "<H3>" + 
            self.lblDateRange.text() + 
            "</H3>"
            )        

        html = html + (
            "<H3>" + 
            self.lblDetails.text() + 
            "</H3>"
            )               

        html = html + (
            "<H3>" + 
            self.lblLocationsVisited.text() + 
            "</H3>"
            )   

        html = html + (
            "<H3>" + 
            self.lblTopSpeciesSeen.text() + 
            "</H3>"
            )    
            
        # grab the map image from the map tap
        # process it into a byte array and encode it
        # so we can insert it inline into the html
        myPixmap = self.webMap.grab()
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
        "  />
        """)

        html = html + (
            "<H4>" + 
            "Species" +
            "</H4>"
            )    

        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>" + 
            "Species" +
            "</th>" +
            "<th>" + 
            "First" + 
            "</th> " +
            "<th></th> " +
            "<th>" +
            "Latest" +
            "</th>" +
            "</tr>"
            )
            
        for r in range(self.tblSpecies.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblSpecies.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblSpecies.item(r, 2).text() +
            "</td>" +
            "<td>" +
            "  " +
            "</td>" +
            "<td>" +
            self.tblSpecies.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
        html = html + "</table>"

        html= html + (
            "<H4>" +
            "Dates" +
            "</H4>"
            )

        html=html + (
            "<font size='2'>" +
            "<p>"
            )
       
        # loopthrough the dates listed in lstDates
        # create a filter unique to each date
        # and get species for that date
        for r in range(self.lstDates.count()):
            html= html + (
                "<b>" +
                self.lstDates.item(r).text() +
                "</b>"                
                )
 
            # create filter set to our current location
            filter = deepcopy(self.filter)
            filter.setStartDate(self.lstDates.item(r).text())
            filter.setEndDate(self.lstDates.item(r).text())
            
            species = self.mdiParent.db.GetSpecies(filter)

            html = html + (    
                "<br>" +                   
                "<table width='100%'>" +
                "<tr>"
                )

            # set up counter R to start a new row after listing each 3 species
            R = 1
            for s in species:
                html = html + (
                    "<td>" +
                    s + 
                    "</td>"
                    )
                if R == 3:
                    html = html + (
                        "</tr>" +
                        "<tr>"
                        )
                    R = 0
                R = R + 1

            html= html + (
                "<br>" +
                "<br>" +
                "</table>"
                )

        html= html + (
            "<H4>" +
            "Locations" +
            "</H4>" +
            "<p>" +
            "Asterisks indicate species seen only at listed location."
            )

        # loopthrough the locations listed in lstLocations
        # create a filter unique to each location
        # and get species for that date
        for r in range(self.lstLocations.count()):
            html= html + (
                "<b>" +
                self.lstLocations.item(r).text() +
                "</b>"                
                )
 
            # create filter set to our current location
            filter = deepcopy(self.filter)
            filter.setLocationType("Location")
            filter.setLocationName(self.lstLocations.item(r).text())
                        
            species = self.mdiParent.db.GetSpecies(filter)

            uniqueSpecies = self.mdiParent.db.GetUniqueSpeciesForLocation(
                self.filter,
                self.lstLocations.item(r).text(),  
                species,  
                self.filteredSightingList
                )            

            html = html + (    
                "<br>" +                       
                "<table width='100%'>" +
                "<tr>"
                )

            # set up counter R to start a new row after listing each 3 species
            R = 1
            for s in species:
                
                if s in uniqueSpecies:
                    s = s + "*"
                    
                html = html + (
                    "<td>" +
                    s + 
                    "</td>"
                    )
                if R == 3:
                    html = html + (
                        "</tr>" +
                        "<tr>"
                        )
                    R = 0
                R = R + 1

            html= html + (
                "<br>" +
                "<br>" +
                "</table>"
                )

        html= html + (
            "<p>" +
            "<H4>" +
            "New Life Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>"
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1

        if self.lstNewLifeSpecies.count() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:
            
            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.lstNewLifeSpecies.count()):
                        
                html = html + (
                    "<td>" +
                    self.lstNewLifeSpecies.item(r).text() +
                    "</td>"
                    )
                    
                if R == 3:
                    html = html + (
                        "</tr>" +
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "<br>" +
                "<br>" +
                "</table>"
                    )
                
        # set up New Year Species
        html= html + (
            "<p>" +
            "<H4>" +
            "New Year Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>" +
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1

        if self.tblNewYearSpecies.rowCount() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:
            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.tblNewYearSpecies.rowCount()):
            
                html = html + (
                    "<td>" +
                    self.tblNewYearSpecies.item(r, 1).text() +
                    " (" + self.tblNewYearSpecies.item(r, 0).text() + ")" +
                    "</td>"
                    )
                    
                if R == 3:
                    html = html + (
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "</tr>" +
                "</table>"
                    )

        # set up New Month Species
        html= html + (
            "<p>" +
            "<H4>" +
            "New Month Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>" +
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1

        if self.tblNewMonthSpecies.rowCount() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:
        
            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.tblNewMonthSpecies.rowCount()):
            
                html = html + (
                    "<td>" +
                    self.tblNewMonthSpecies.item(r, 1).text() +
                    " (" + self.tblNewMonthSpecies.item(r, 0).text() + ")" +
                    "</td>"
                    )
                    
                if R == 3:
                    html = html + (
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "</tr>" +
                "</table>"
                    )

        # set up New Country Species
        html= html + (
            "<p>" +
            "<H4>" +
            "New Country Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>" +
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1
        
        if self.tblNewCountrySpecies.rowCount() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:

            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.tblNewCountrySpecies.rowCount()):
            
                html = html + (
                    "<td>" +
                    self.tblNewCountrySpecies.item(r, 1).text() +
                    " (" + self.tblNewCountrySpecies.item(r, 0).text() + ")" +
                    "</td>"
                    )
                    
                if R == 2:
                    html = html + (
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "</tr>" +
                "</table>"
                    )
                
        html = html + (
            "<font size>" +            
            "</body>" +
            "</html>"
            )
        
        # set up New State Species
        html= html + (
            "<p>" +
            "<H4>" +
            "New State Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>" +
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1

        if self.tblNewStateSpecies.rowCount() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:
            
            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.tblNewStateSpecies.rowCount()):
            
                html = html + (
                    "<td>" +
                    self.tblNewStateSpecies.item(r, 1).text() +
                    " (" + self.tblNewStateSpecies.item(r, 0).text() + ")" +
                    "</td>"
                    )
                    
                if R == 2:
                    html = html + (
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "</tr>" +
                "</table>"
                    )

        # set up New County Species
        html= html + (
            "<p>" +
            "<H4>" +
            "New County Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>" +
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1

        if self.tblNewCountySpecies.rowCount() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:
            
            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.tblNewCountySpecies.rowCount()):
            
                html = html + (
                    "<td>" +
                    self.tblNewCountySpecies.item(r, 1).text() +
                    " (" + self.tblNewCountySpecies.item(r, 0).text() + ")" +
                    "</td>"
                    )
                    
                if R == 2:
                    html = html + (
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "</tr>" +
                "</table>"
                    )
     
        # set up New Location Species
        html= html + (
            "<p>" +
            "<H4>" +
            "New Location Species" +
            "</H4>" +
            "<p>" +
            "<table width='100%'>" +
            "<tr>"
            )

        # set up counter R to start a new row after listing each 3 species
        R = 1

        if self.tblNewLocationSpecies.rowCount() == 0:
            html = html + (
                "<td>" +
                "None" +
                "</td>"
                )
                
        else:
            
            # loopthrough the species listed in lstNewLifeSpecies
            for r in range(self.tblNewLocationSpecies.rowCount()):
            
                html = html + (
                    "<td>" +
                    self.tblNewLocationSpecies.item(r, 1).text() +
                    " (" + self.tblNewLocationSpecies.item(r, 0).text() + ")" +
                    "</td>"
                    )
                    
                if R == 2:
                    html = html + (
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                    
                R = R + 1

            html= html + (
                "</tr>" +
                "</table>"
                )
     
        html = html + (
            "<font size>" +            
            "</body>" +
            "</html>"
            )       
            
        QApplication.restoreOverrideCursor()   
        
        return(html)


    def setDateFilter(self):
        # get location name and type from focus widget. Varies for widgets. 
        if self.focusWidget().objectName() == "lstDates":
            date = self.focusWidget().currentItem().text()
            self.mdiParent.setDateFilter(date)

        if self.focusWidget().objectName() == "tblNewYearSpecies":
            date = self.focusWidget().item(self.focusWidget().currentRow(), 0).text()
            startDate = date + "-01-01"
            endDate = date + "-12-31"
            self.mdiParent.setDateFilter(startDate, endDate)

        if self.focusWidget().objectName() == "tblNewMonthSpecies":
            month = self.focusWidget().item(self.focusWidget().currentRow(), 0).text()
            self.mdiParent.setSeasonalRangeFilter(month)


    def setFirstDateFilter(self):
        # get location name and type from focus widget. Varies for tables. 
        if self.focusWidget().objectName() == "tblSpecies":
            date = self.focusWidget().item(self.focusWidget().currentRow(), 2).text()
            self.mdiParent.setDateFilter(date)


    def setLastDateFilter(self):
        # get location name and type from focus widget. Varies for tables. 
        if self.focusWidget().objectName() == "tblSpecies":
            date = self.focusWidget().item(self.focusWidget().currentRow(), 3).text()
            self.mdiParent.setDateFilter(date)
            
            
    def setLocationFilter(self):

        # get location name and type from focus widget. Varies for tables. 
        if self.focusWidget().objectName() == "tblNewCountrySpecies":
            country = self.focusWidget().item(self.focusWidget().currentRow(), 0).text()
            self.mdiParent.setCountryFilter(country)

        if self.focusWidget().objectName() == "tblNewStateSpecies":
            state = self.focusWidget().item(self.focusWidget().currentRow(), 0).text()
            self.mdiParent.setStateFilter(state)

        if self.focusWidget().objectName() == "tblNewCountySpecies":
            county = self.focusWidget().item(self.focusWidget().currentRow(), 0).text()
            self.mdiParent.setCountyFilter(county)

        if self.focusWidget().objectName() == "tblNewLocationSpecies":
            location = self.focusWidget().item(self.focusWidget().currentRow(), 0).text()
            self.mdiParent.setLocationFilter(location)

        if self.focusWidget().objectName() == "lstLocations":
            location = self.focusWidget().currentItem().text()
            self.mdiParent.setLocationFilter(location)


    def setSpeciesFilter(self):

        # get species name from focus widget. Getting the species name is different for tables than for lists.
        if self.focusWidget().objectName() in ([
            "tblSpecies",
            "tblNewYearSpecies", 
            "tblNewMonthSpecies", 
            "tblNewCountrySpecies", 
            "tblNewStateSpecies", 
            "tblNewCountySpecies", 
            "tblNewLocationSpecies"
            ]):
            species = self.focusWidget().item(self.focusWidget().currentRow(), 1).text()

        if self.focusWidget().objectName() in ([
            "lstSpecies",
            "lstLocationSpecies",
            "lstLocationUniqueSpecies",
            "lstNewLifeSpecies"
            ]):
            species = self.focusWidget().currentItem().text()

        self.mdiParent.setSpeciesFilter(species)


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)
        self.FillMap()

   
    def scaleMe(self):
               
        scaleFactor = self.mdiParent.scaleFactor
        windowWidth =  1100  * scaleFactor
        windowHeight = 625 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = self.mdiParent.fontSize
        scaleFactor = self.mdiParent.scaleFactor     
        #scale the font for all widgets in window
        for w in self.scrollArea.children():
            try:
                w.setFont(QFont("Helvetica", fontSize))
            except:
                pass 

        self.lblLocation.setFont(QFont("Helvetica", floor(fontSize * 1.4 )))
        self.lblLocation.setStyleSheet("QLabel { font: bold }");
        self.lblDateRange.setFont(QFont("Helvetica", floor(fontSize * 1.2 )))
        self.lblDateRange.setStyleSheet("QLabel { font: bold }");
        self.lblDetails.setFont(QFont("Helvetica", floor(fontSize * 1.2 )))
        self.lblDetails.setStyleSheet("QLabel { font: bold }");

        metrics = self.tblSpecies.fontMetrics()
        textHeight = metrics.boundingRect("A").height()        
        textWidth = metrics.boundingRect("Dummy Country").width()
        
        for t in ([
            self.tblNewYearSpecies,
            self.tblNewMonthSpecies,
            self.tblNewCountrySpecies,
            self.tblNewStateSpecies,
            self.tblNewCountySpecies
            ]):
            header = t.horizontalHeader()
            header.resizeSection(0,  floor(1.2 * textWidth))
            for r in range(t.rowCount()):
                t.setRowHeight(r, textHeight * 1.1) 
            
        # format tblSpecies, which is laid out differently from the other tables
        dateWidth = metrics.boundingRect("2222-22-22").width()
        header = self.tblSpecies.horizontalHeader()
        header.resizeSection(2,  floor(1.5* dateWidth))
        header.resizeSection(3,  floor(1.5 * dateWidth))
        for r in range(self.tblSpecies.rowCount()):
            self.tblSpecies.setRowHeight(r, textHeight * 1.1)         
        
        # format tblNewLocationSpecies, which needs wider location column
        header = self.tblNewLocationSpecies.horizontalHeader()
        header.resizeSection(0,  floor(4 * textWidth))
        for r in range(self.tblNewLocationSpecies.rowCount()):
            t.setRowHeight(r, textHeight * 1.1)         

