# import GUI form for this class
import form_LocationTotals

# import classes from other project files
import code_Filter
import code_Lists

# import basic Python libraries
from copy import deepcopy
from math import floor

from PyQt5.QtGui import (
    QCursor,
    QFont
    )
    
from PyQt5.QtCore import (
    Qt,
    pyqtSignal
    )
    
from collections import (
    defaultdict
)    
from PyQt5.QtWidgets import (
    QApplication, 
    QTableWidgetItem, 
    QHeaderView,
    QMdiSubWindow,
    )




class LocationTotals(QMdiSubWindow, form_LocationTotals.Ui_frmLocationTotals):

    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()       
    
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""        
        self.resized.connect(self.resizeMe)                            
        self.tblCountryTotals.itemDoubleClicked.connect(lambda: self.CreateListForLocation("Country"))
        self.tblStateTotals.itemDoubleClicked.connect(lambda: self.CreateListForLocation("State"))
        self.tblCountyTotals.itemDoubleClicked.connect(lambda: self.CreateListForLocation("County"))
        self.tblLocationTotals.itemDoubleClicked.connect(lambda: self.CreateListForLocation("Location"))
        self.filter = code_Filter.Filter()
        self.tabLocationTotals.setCurrentIndex(0)

        self.tblCountryTotals.addAction(self.actionSetCountryFilter)
        self.tblStateTotals.addAction(self.actionSetStateFilter)
        self.tblCountyTotals.addAction(self.actionSetCountyFilter)
        self.tblLocationTotals.addAction(self.actionSetLocationFilter)
        
        self.actionSetCountryFilter.triggered.connect(self.setCountryFilter)
        self.actionSetStateFilter.triggered.connect(self.setStateFilter)
        self.actionSetCountyFilter.triggered.connect(self.setCountyFilter)
        self.actionSetLocationFilter.triggered.connect(self.setLocationFilter)


    def CreateListForLocation(self,  locationType):
        tempFilter = deepcopy(self.filter)
        
        if locationType == "Country":
            locationName = self.mdiParent.db.GetCountryCode(self.tblCountryTotals.item(self.tblCountryTotals.currentRow(),  1).text())
        if locationType == "State":
            locationName = self.mdiParent.db.GetStateCode(self.tblStateTotals.item(self.tblStateTotals.currentRow(),  1).text())
        if locationType == "County":
            locationName = self.tblCountyTotals.item(self.tblCountyTotals.currentRow(),  1).text()
        if locationType == "Location":
            locationName = self.tblLocationTotals.item(self.tblLocationTotals.currentRow(),  1).text()
        
        sub = code_Lists.Lists()        
        sub.mdiParent = self.mdiParent
        tempFilter.setLocationType(locationType)
        tempFilter.setLocationName(locationName)
        
        if self.focusWidget().currentColumn() in [0, 1, 2]:
            sub.FillSpecies(tempFilter)

        if self.focusWidget().currentColumn() == 3:
            sub.FillChecklists(tempFilter)

        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        QApplication.restoreOverrideCursor()       


    def html(self):
    
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

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
            table, th, td {
                border-collapse: collapse;
            }
            th, td {
                padding: 5px;
            }
            th {
                text-align: left;
            }
            </style>
            <body>
            """
            
        html = html + (
            "<H1>" + 
            "Location Totals" + 
            "</H1>"
            )
        
        html = html + (
            "<H2>" + 
            self.lblLocation.text() + 
            "</H2>"
            )        

        html = html + (
            "<H2>" + 
            self.lblDateRange.text() + 
            "</H2>"
            )        

        html = html + (
            "<H2>" + 
            self.lblDetails.text() + 
            "</H2>"
            )        

        html = html + (
            "<H3>" + 
            "Country Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>Country</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblCountryTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblCountryTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblCountryTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblCountryTotals.item(r, 2).text() +
            "</td>" +
            "<td>" +
            self.tblCountryTotals.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
            
        html = html + (
            "</table>"
            "</font size>"
            )

        html = html + (
            "<H3>" + 
            "State Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>State</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblStateTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblStateTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblStateTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblStateTotals.item(r, 2).text() +
            "</td>" +           
            "<td>" +
            self.tblStateTotals.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
            
        html = html + (
            "</table>"
            "</font size>"
            )

        html = html + (
            "<H3>" + 
            "County Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>County</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblCountyTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblCountyTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblCountyTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblCountyTotals.item(r, 2).text() +
            "</td>" +
            "<td>" +
            self.tblCountyTotals.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
            
        html = html + (
            "</table>"
            "</font size>"
            )

        html = html + (
            "<H3>" + 
            "Location Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>Location</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblLocationTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblLocationTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblLocationTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblLocationTotals.item(r, 2).text() +
            "</td>" +
            "<td>" +
            self.tblLocationTotals.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
            
        html = html + (
            "</table>"
            "</font size>"
            )
            
        html = html + (
            "</body>" +
            "</html>"
            )
            
        QApplication.restoreOverrideCursor()   
        
        return(html)
        

    def FillLocationTotals(self,  filter):
        self.filter = deepcopy(filter)
        
        # find all years, months, and dates in db
        dbCountries = set()
        dbStates = set()
        dbCounties = set()
        dbLocations = set()
        countryDict = defaultdict()
        stateDict = defaultdict()
        countyDict = defaultdict()
        locationDict = defaultdict()
        
        minimalSightingList = self.mdiParent.db.GetMinimalFilteredSightingsList(filter)
        
        for s in minimalSightingList:
            
            # Consider only full species, not slash or spuh entries
            if ("/" not in s[1]) and ("sp." not in s[1]):
                
                if self.mdiParent.db.TestSighting(s,  filter) is True:
                    dbCountries.add(s[5][0:2])
                    dbStates.add(s[5])
                    if s[6] != "":
                        dbCounties.add(s[6])
                    dbLocations.add(s[7])
                    
                    # create dictionaries of country, state, county, and location sighting for faster lookup
                    if s[5][0:2] not in countryDict.keys():
                        countryDict[s[5][0:2]] = [s]
                    else:
                        countryDict[s[5][0:2]].append(s)                
                    
                    if s[5] not in stateDict.keys():
                        stateDict[s[5]] = [s]
                    else:
                        stateDict[s[5]].append(s)                
                                 
                    if s[6] != "":
                        if s[6] not in countyDict.keys():
                            countyDict[s[6]] = [s]
                        else:
                            countyDict[s[6]].append(s)       
                                 
                    if s[7] not in locationDict.keys():
                        locationDict[s[7]] = [s]
                    else:
                        locationDict[s[7]].append(s)           
        
        # check if no sightings were found. Return false if none found. Abort and display message.
        if len(countryDict) + len(stateDict) + len(countyDict) + len(locationDict) == 0:
            return(False)
        
        # set numbers of rows for each tab's grid (years, months, dates)
        self.tblCountryTotals.setRowCount(len(dbCountries))
        self.tblCountryTotals.setColumnCount(4)
        self.tblStateTotals.setRowCount(len(dbStates))
        self.tblStateTotals.setColumnCount(4)
        self.tblCountyTotals.setRowCount(len(dbCounties))
        self.tblCountyTotals.setColumnCount(4)
        self.tblLocationTotals.setRowCount(len(dbLocations))
        self.tblLocationTotals.setColumnCount(4)     
        
        self.tblCountryTotals.setShowGrid(False)        
        self.tblStateTotals.setShowGrid(False)        
        self.tblCountyTotals.setShowGrid(False)        
        self.tblLocationTotals.setShowGrid(False)        
        
        countryArray = []
        for country in dbCountries:
            countrySpecies = set()
            countryChecklists = set()
            for s in countryDict[country]:
                countrySpecies.add(s[1])
                countryChecklists.add(s[0])
            countryArray.append([len(countrySpecies),  country, len(countryChecklists)])
        countryArray.sort(reverse=True)
        R = 0
        for country in countryArray:            
            rankItem = QTableWidgetItem()
            rankItem.setData(Qt.DisplayRole, R+1)
            countryItem = QTableWidgetItem()
            countryItem.setText(self.mdiParent.db.GetCountryName(country[1]))
            countryTotalItem = QTableWidgetItem()
            countryTotalItem.setData(Qt.DisplayRole, country[0])
            countryTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                     
            countryChecklistTotalItem = QTableWidgetItem()
            countryChecklistTotalItem.setData(Qt.DisplayRole, country[2])
            countryChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                     
            self.tblCountryTotals.setItem(R, 0, rankItem)    
            self.tblCountryTotals.setItem(R, 1, countryItem)
            self.tblCountryTotals.setItem(R, 2, countryTotalItem)
            self.tblCountryTotals.setItem(R, 3, countryChecklistTotalItem)

            R = R + 1

        stateArray = []
        for state in dbStates:
            stateSpecies = set()
            stateChecklists = set()
            for s in stateDict[state]:
                stateSpecies.add(s[1])
                stateChecklists.add(s[0])
            stateArray.append([len(stateSpecies),  state, len(stateChecklists)])
        stateArray.sort(reverse=True)
        R = 0
        for state in stateArray:            
            rankItem = QTableWidgetItem()
            rankItem.setData(Qt.DisplayRole, R+1)
            stateItem = QTableWidgetItem()
            stateItem.setText(self.mdiParent.db.GetStateName(state[1]))
            stateTotalItem = QTableWidgetItem()
            stateTotalItem.setData(Qt.DisplayRole, state[0])
            stateTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                     
            stateChecklistTotalItem = QTableWidgetItem()
            stateChecklistTotalItem.setData(Qt.DisplayRole, state[2])
            stateChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                     
            self.tblStateTotals.setItem(R, 0, rankItem)    
            self.tblStateTotals.setItem(R, 1, stateItem)
            self.tblStateTotals.setItem(R, 2, stateTotalItem)
            self.tblStateTotals.setItem(R, 3, stateChecklistTotalItem)
            R = R + 1

        countyArray = []
        for county in dbCounties:
            if county != "" and county is not None:
                countySpecies = set()
                countyChecklists = set()
                for s in countyDict[county]:
                    countySpecies.add(s[1])
                    countyChecklists.add(s[0])
                countyArray.append([len(countySpecies),  county, len(countyChecklists)])
        countyArray.sort(reverse=True)
        R = 0
        for county in countyArray:            
            rankItem = QTableWidgetItem()
            rankItem.setData(Qt.DisplayRole, R+1)
            countyItem = QTableWidgetItem()
            countyItem.setText(county[1])
            countyTotalItem = QTableWidgetItem()
            countyTotalItem.setData(Qt.DisplayRole, county[0])
            countyTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                                 
            countyChecklistTotalItem = QTableWidgetItem()
            countyChecklistTotalItem.setData(Qt.DisplayRole, county[2])
            countyChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                                 
            self.tblCountyTotals.setItem(R, 0, rankItem)    
            self.tblCountyTotals.setItem(R, 1, countyItem)
            self.tblCountyTotals.setItem(R, 2, countyTotalItem)
            self.tblCountyTotals.setItem(R, 3, countyChecklistTotalItem)
            R = R + 1

        locationArray = []
        for location in dbLocations:
            if location != "":
                locationSpecies = set()
                locationChecklists = set()
                for s in locationDict[location]:
                    locationSpecies.add(s[1])
                    locationChecklists.add(s[0])
                locationArray.append([len(locationSpecies),  location, len(locationChecklists)])
        locationArray.sort(reverse=True)
        rank = 0
        lastLocationTotal = 0
        R = 0
        for location in locationArray:            
            rankItem = QTableWidgetItem()
            if location[0] != lastLocationTotal:
                rank = R+1
            rankItem.setData(Qt.DisplayRole, rank)
            locationItem = QTableWidgetItem()
            locationItem.setText(location[1])
            locationTotalItem = QTableWidgetItem()
            locationTotalItem.setData(Qt.DisplayRole, location[0])
            locationTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                                             
            locationChecklistTotalItem = QTableWidgetItem()
            locationChecklistTotalItem.setData(Qt.DisplayRole, location[2])
            locationChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                                             
            self.tblLocationTotals.setItem(R, 0, rankItem)    
            self.tblLocationTotals.setItem(R, 1, locationItem)
            self.tblLocationTotals.setItem(R, 2, locationTotalItem)
            self.tblLocationTotals.setItem(R, 3, locationChecklistTotalItem)
            lastLocationTotal = location[0]
            R = R + 1

        # set headers and column stretching 
        for t in [self.tblCountryTotals, self.tblStateTotals, self.tblCountyTotals, self.tblLocationTotals]:
            t.setSortingEnabled(True)
            t.sortItems(0,0)
            t.horizontalHeader().setVisible(True)
            # remove first three characters from tbl widget name
            regionType = t.objectName()[3:]
            # remove "Totals" from widget name
            regionType = regionType[:-6]
            t.setHorizontalHeaderLabels(['Rank', regionType, 'Species', 'Checklists'])
            header = t.horizontalHeader()
            header.setSectionResizeMode(1, QHeaderView.Stretch)

        # set location and date range titles
        self.mdiParent.SetChildDetailsLabels(self, self.filter)

        # set window title
        self.setWindowTitle("Location Totals: " + self.lblLocation.text() + ": " + self.lblDateRange.text())

        if self.lblDetails.text() != "":
            self.lblDetails.setVisible(True)
        else:
            self.lblDetails.setVisible(False)
        
        self.scaleMe()
        self.resizeMe()

        return(True)


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)
   
   
    def scaleMe(self):
               
        scaleFactor = self.mdiParent.scaleFactor
        windowWidth =  600  * scaleFactor
        windowHeight = 580 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = self.mdiParent.fontSize
        scaleFactor = self.mdiParent.scaleFactor     
        #scale the font for all widgets in window
        for w in self.scrollAreaWidgetContents.children():
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

        metrics = self.tblCountryTotals.fontMetrics()
        textHeight = metrics.boundingRect("A").height()        
        rankTextWidth = metrics.boundingRect("Rank").width()
        
        for t in [self.tblCountryTotals, self.tblStateTotals, self.tblCountyTotals, self.tblLocationTotals]:
            header = t.horizontalHeader()
            header.resizeSection(0,  floor(1.7 * rankTextWidth))
            header.resizeSection(2,  floor(2 * rankTextWidth))
            header.resizeSection(3,  floor(2.5 * rankTextWidth))
            for r in range(t.rowCount()):
                t.setRowHeight(r, textHeight * 1.1) 


    def setCountryFilter(self):
        countryName= self.tblCountryTotals.item(self.tblCountryTotals.currentRow(), 1).text()
        self.mdiParent.setCountryFilter(countryName)

             
    def setStateFilter(self):
        stateName= self.tblStateTotals.item(self.tblStateTotals.currentRow(), 1).text()
        self.mdiParent.setStateFilter(stateName)
            
            
    def setCountyFilter(self):
        countyName= self.tblCountyTotals.item(self.tblCountyTotals.currentRow(), 1).text()
        self.mdiParent.setCountyFilter(countyName)
   
   
    def setLocationFilter(self):
        locationName= self.tblLocationTotals.item(self.tblLocationTotals.currentRow(), 1).text()
        self.mdiParent.setLocationFilter(locationName)
            
