# import basic Python libraries
import sys
import random
import os
import subprocess
import datetime
import csv
import zipfile
import io
from copy import deepcopy
from collections import defaultdict
from math import floor, modf
import base64

# import the GUI forms that we create with Qt Creator
import MDIMain
import Lists
import Individual
import DateTotals
import LocationTotals
import Compare
import Location
import BigReport
import Families
import Web
import Find

# import the Qt components we'll use
# do this so later we won't have to clutter our code with references to parent Qt classes 

from PyQt5.QtGui import (
    QCursor,
    QIcon,
    QPixmap,
    QColor,
    QFont,
    QTextDocument
    )
    
from PyQt5.QtCore import (
    Qt,
    QVariant,
    QSize,
    QUrl,
    pyqtSignal,
    QIODevice,
    QByteArray,
    QBuffer,
    QDate
    )
    
from PyQt5.QtWidgets import (
    QApplication, 
    QMessageBox, 
    QTableWidgetItem, 
    QHeaderView,
    QMainWindow,
    QFileDialog,
    QMdiSubWindow,
    QGraphicsScene,
    QTreeWidgetItem,
    QGraphicsEllipseItem,
    QStyleFactory,
    QSlider,
    QLabel,
    QItemDelegate
    )
    
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView,
    QWebEngineSettings,
)

from PyQt5.QtPrintSupport import (
    QPrintDialog, 
    QPrinter
    )

class DataBase():

    # this is the class that will store all our data and the data-seeking logic 
    
    def __init__(self):
        self.allSpeciesList = []
        self.familyList = []
        self.orderList = []
        self.masterFamilyOrderList = []
        self.masterLocationList = []
        self.countryList = []
        self.stateList = []
        self.countyList = []
        self.locationList = []
        self.sightingList = []
        self.eBirdFileOpenFlag = False
        self.countryStateCodeFileFound = False
        self.speciesDict = defaultdict()
        self.yearDict = defaultdict()
        self.monthDict = defaultdict()
        self.dateDict = defaultdict()
        self.countryDict = defaultdict()
        self.stateDict = defaultdict()
        self.countyDict = defaultdict()
        self.locationDict = defaultdict()
        self.checklistDict = defaultdict()
        self.familySpeciesDict = defaultdict()
        self.orderSpeciesDict = defaultdict()
        self.monthNameDict = ({
            "01":"Jan",  
            "02":"Feb",  
            "03":"Mar",  
            "04":"Apr",  
            "05":"May",  
            "06":"Jun",  
            "07":"Jul",  
            "08":"Aug",  
            "09":"Sep",  
            "10":"Oct",  
            "11":"Nov",  
            "12":"Dec"
            })
        self.monthNumberDict = ({
            "Jan":"01", 
            "Feb":"02",  
            "Mar":"03", 
            "Apr":"04", 
            "May":"05", 
            "Jun":"06", 
            "Jul":"07", 
            "Aug":"08", 
            "Sep":"09", 
            "Oct":"10", 
            "Nov":"11", 
            "Dec":"12"
            })            
        
    def ReadCountryStateCodeFile(self,  dataFile):
        
        # initialize variable used to store CSV file's data
        countryCodeData = []
        
        # open the country and stae code data file
        # and read its lines into a list for future searching
        with open(dataFile, 'r',  errors='replace') as csvfile:
            csvdata = csv.reader(csvfile, delimiter=',', quotechar='"')
            for line in csvdata:
                countryCodeData.append(line)
        csvfile.close()
        
        # clear the countryList and stateList because we'll use longer names
        self.countryList = []
        self.stateList = []
        
        # search through each location in the master location file
        # append the long country and state names when found in the country state code data
        for l in self.masterLocationList:
            
            # append two place holders in the masterLocationList for long country and state names
            l.append("")
            l.append("")
            
            for c in countryCodeData:
                
                # find the long country name by looking for a perfect match of "cc-" for the state code
                # this match is actually for the country because states have characters
                # after the - character
                if l[0] + "-" == c[1]:
                    
                    # when found, save the long country name to the masterLocationList
                    l[4] = c[2]
                    self.countryList.append(c[2])
                
                # look for a perfect match for the state code
                if l[1] == c[1]:
                    
                    # when found, save the long state name to the masterLocationList
                    l[5] = c[2]
                    self.stateList.append(c[2])
                    
                    # no need to keep searching. We've found our long names.
                    break
                    
            # get rid of duplicates in master country and state lists using the set command
            self.countryList = list(set(self.countryList))
            self.stateList = list(set(self.stateList))
            
            # sort the master country and state lists
            self.countryList.sort()
            self.stateList.sort()                
            
            self.countryStateCodeFileFound = True            


    def ReadDataFile(self, DataFile):
        
        if os.path.splitext(DataFile[0])[1] == ".zip":   
            
            filehandle = open(DataFile[0], 'rb')
            zfile = zipfile.ZipFile(filehandle)
            try:
                csvfile = io.StringIO(zfile.read("MyEBirdData.csv").decode('utf-8'))
            except (KeyError):
                QApplication.restoreOverrideCursor()
                self.eBirdFileOpenFlag = False
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("The file failed to load.\n\nPlease check that it is a valid eBird data file.\n")
                msg.setWindowTitle("File failed to load")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()   
                return
                
        if os.path.splitext(DataFile[0])[1] == ".csv":        
            csvfile = open(DataFile[0], 'r')
        
        # try to process it's CSV values. Go to except if we have problems
        try:
            csvdata = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            # initialize temporary list variable to hold location data 
            thisMasterLocationEntry = []
            
            for line in csvdata:
                                
                # convert date format from mm-dd-yyyy to yyyy-mm-dd for international standard and sorting ability
                line[10] = line[10][6:]+ "-" + line[10][0:2] + "-" + line[10][3:5]
                
                # append state name in parentheses to county name to differentiate between
                # counties that have the same name but are in different states
                if line[6] != "":
                    line[6] =  line[6] + " (" + line[5] + ")" 
                
                # add blank elements to list so we can later add family and order names if taxonomic file exists
                # also add blank line for subspecies name
                while len(line) < 24:
                    line.append("")
                
                # store full name (maybe a subspecies) in sighting
                subspeciesName = deepcopy(line[1])
                line[23]= subspeciesName
                
                # remove any subspecies data in parentheses in species name
                if "(" in line[1]:
                    line[1] = line[1][:line[1].index("(")-1]    
                 
                # convert 12-hour time format to 24-hour format for easier sorting and display
                time = line[11]
                if "AM" in time:
                    time = line[11][0:5]
                if "PM" in time:
                    time = line[11][0:5]
                    hour = int(line[11][0:2])
                    hour = str(hour + 12)
                    if hour == "24":
                        hour = "12"
                    time = hour + line[11][2:5]  
                line[11] = time
                
                # add sighting to the main database for use by later searches etc.
                # this sightingList will be used in nearly every search performed by user
                self.sightingList.append(line)

                #add sighting to checklistDict, even if it's a sp or / species
                if line[0] not in self.checklistDict.keys():
                    self.checklistDict[line[0]] = [line]
                else:
                    self.checklistDict[line[0]].append(line)  

                #add sighting to other dicts only if it's a full species, not a / or sp.
                if ("/" not in line[1]) and ("sp." not in line[1]):
                    if line[1] not in self.speciesDict.keys():
                        self.speciesDict[line[1]] = [line]
                    else:
                        self.speciesDict[line[1]].append(line)                                
                
                    # also add subspecies as key to speciesDict 
                    # to faciliate lookup
                    if line[23] not in self.speciesDict.keys():
                        self.speciesDict[line[23]] = [line]
                    else:
                        self.speciesDict[line[23]].append(line) 
                    
                    #add sighting to yearDict
                    if line[10][0:4] not in self.yearDict.keys():
                        self.yearDict[line[10][0:4]] = [line]
                    else:
                        self.yearDict[line[10][0:4]].append(line)
                        
                    #add sighting to monthDict
                    if line[10][5:7] not in self.monthDict.keys():
                        self.monthDict[line[10][5:7]] = [line]
                    else:
                        self.monthDict[line[10][5:7]].append(line)      
                        
                    #add sighting to dateDict
                    if line[10] not in self.dateDict.keys():
                        self.dateDict[line[10]] = [line]
                    else:
                        self.dateDict[line[10]].append(line)                                        
                        
                    #add sighting to countryDict
                    if line[5][0:2] not in self.countryDict.keys():
                        self.countryDict[line[5][0:2]] = [line]
                    else:
                        self.countryDict[line[5][0:2]].append(line)                                
                        
                    #add sighting to stateDict
                    if line[5] not in self.stateDict.keys():
                        self.stateDict[line[5]] = [line]
                    else:
                        self.stateDict[line[5]].append(line)                                

                    #add sighting to countyDict
                    if line[6] != "":
                        if line[6] not in self.countyDict.keys():
                            self.countyDict[line[6]] = [line]
                        else:
                            self.countyDict[line[6]].append(line)                                
                        
                    #add sighting to locationDict
                    if line[7] not in self.locationDict.keys():
                        self.locationDict[line[7]] = [line]
                    else:
                        self.locationDict[line[7]].append(line)          
                
                # get just the location data from this particular sighting
                thisMasterLocationEntry = [line[5][0:2],  line[5],  line[6],  line[7]]
                
                # if this location isn't already in the cache, save it for future use
                if thisMasterLocationEntry not in self.masterLocationList:
                    self.masterLocationList.append(thisMasterLocationEntry)
                    self.allSpeciesList.append(line[1])
                    self.countryList.append(line[5][0:2])
                    self.stateList.append(line[5])
                    if line[6] != "":
                        self.countyList.append(line[6])
                    self.locationList.append(line[7])
            
        except (IndexError,  RuntimeError, TypeError, NameError, KeyError):
            self.allSpeciesList = []
            self.currentSpeciesList = []
            self.masterLocationList = []
            self.countryList = []
            self.stateList = []
            self.countyList = []
            self.locationList = []
            self.sightingList = []
            self.eBirdFileOpenFlag = False
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("The file failed to load.\n\nPlease check that it is a valid eBird data file.\n")
            msg.setWindowTitle("File failed to load")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()   
            csvfile.close()                 
            return
        
        csvfile.close()
        
        # remove csv header row from list
        self.allSpeciesList.pop(0) 
        self.locationList.pop(0) 
        self.sightingList.pop(0) 
        self.countryList.pop(0)
        self.stateList.pop(0)
        
        # use set function to remove duplicates and then return to a list
        self.allSpeciesList = list(set(self.allSpeciesList))
        self.countryList = list(set(self.countryList))
        self.stateList = list(set(self.stateList))
        self.locationList = list(set(self.locationList))

        # sort 'em 
        self.locationList.sort()
        self.countryList.sort()
        self.stateList.sort()
        self.masterLocationList.sort()
        
        # remove parenthetical state names from counties, unless needed to 
        # differentiate counties with same name in different states
        countyNamesWithoutParens = []
        countyKeyChanges = []
        for cdk in self.countyDict.keys():
            if cdk != "":
                countyNamesWithoutParens.append(cdk.split(" (")[0])
        
        for cdk in self.countyDict.keys():
            if cdk != "":
                if countyNamesWithoutParens.count((cdk.split(" (")[0])) == 1:
                    for s in self.countyDict[cdk]:
                        s[6] = cdk.split(" (")[0]
                    countyKeyChanges.append([cdk,  cdk.split(" (")[0]])
        
        for ckc in countyKeyChanges:
            self.countyDict[str(ckc[1])] = self.countyDict.pop(str(ckc[0]))
            for ml in self.masterLocationList:
                if ml[2] == str(ckc[0]):
                    ml[2] = str(ckc[1])
            
        self.countyList = list(self.countyDict.keys())
        self.countyList.sort()
        
        # set flat indicating that a data file is now open
        self.eBirdFileOpenFlag = True


    def ReadTaxonomyDataFile(self, taxonomyDataFile):
        
        # initialize variable to hold the csv data from the taxonomy file
        taxonomyData = []
        # open the CSV taxonomy file, using "replace" for any problematic characters
        with open(taxonomyDataFile,  "r",  errors='replace') as csvfile:
            csvdata = csv.reader(csvfile, delimiter=',', quotechar='"')
            # store the csv data in a list for easier searching later on
            for row in csvdata:
                taxonomyData.append(row)

        # initialize variables that will save the family and order names for faster lookup
        thisSciName = ""
        thisOrder = ""
        thisFamily = ""

        # loop through sighting list to get each species, compare it, and add order and family
        for s in self.sightingList:

            # if this species already has a order/family found, no need to search database again.
            # But if species does not have order/family found, we need to get search the database
            if thisSciName != s[2]:

                for line in taxonomyData:

                    # if species matches, save the order and family names for the next time we find the species
                    # species will be found in the sighting file in taxonomic order, so each species will be chunked together
                    if s[2] == line[4]:  # sci names match                   
                        
                        thisSciName = line[4]
                        thisOrder= line[5]
                        thisFamily = line[6]   
   
                        if thisFamily not in self.familyList:
                            self.familyList.append(thisFamily)                        

                        if thisOrder not in self.orderList:
                            self.orderList.append(thisOrder)  
                            
                        if [thisFamily, thisOrder] not in self.masterFamilyOrderList:
                            self.masterFamilyOrderList.append([thisFamily, thisOrder])

                        #add species to orderSpeciesDict:
                        if thisOrder not in self.orderSpeciesDict.keys():
                            self.orderSpeciesDict[thisOrder] = [s[1]]
                        else:
                            self.orderSpeciesDict[thisOrder].append(s[1]) 
                            
                        #add species to familySpeciesDict:
                        if thisFamily not in self.familySpeciesDict.keys():
                            self.familySpeciesDict[thisFamily] = [s[1]]
                        else:
                            self.familySpeciesDict[thisFamily].append(s[1]) 
                                    
                        break

            # append the order and family names to the species in the sighting list.
            s[21] = thisOrder
            s[22] = thisFamily

        csvfile.close()


    def GetFamilies(self,  filter,  filteredSightingList = []):
        familiesList = []
        
        # set filteredSightingList to master list if no filteredSightingList specified
        if filteredSightingList == []:
            filteredSightingList = self.GetMinimalFilteredSightingsList(filter)
        
        # for each sighting, test date if necessary. Append new dates to return list.
        # don't consider spuh or slash species
        for s in filteredSightingList:
            if "sp." not in s[1] and "/" not in s[1]:
                if self.TestSighting(s,  filter) is True:
                    if s[22] not in familiesList:
                        familiesList.append(s[22])
        
        return(familiesList)


    def GetSightings(self,  filter):
        returnList = []
        
        filteredSightingList = self.GetMinimalFilteredSightingsList(filter)

        for s in filteredSightingList:
            # this is not a single checklist, so remove spuh and slash sightings
            if filter.getChecklistID() == "":
                if "/" not in s[1] and "sp." not in s[1]:
                    if self.TestSighting(s,  filter) is True:
                        returnList.append(s)
            else:
                # this is a single checklist, so allow spuh and slash sightings
                if self.TestSighting(s,  filter) is True:
                    returnList.append(s)        
        
        return(returnList)


    def GetSpecies(self,  filter,  filteredSightingList = []):
        speciesList = []
        
        # set filteredSightingList to master list if no filteredSightingList specified
        if filteredSightingList == []:
            filteredSightingList = self.GetMinimalFilteredSightingsList(filter)
        
        # for each sighting, test date if necessary. Append new dates to return list.
        for s in filteredSightingList:
            if self.TestSighting(s,  filter) is True:
                if s[1] not in speciesList:
                    speciesList.append(s[1])
        
        return(speciesList)


    def GetMinimalFilteredSightingsList(self,  filter):

        returnList = []
        speciesName = filter.getSpeciesName()
        speciesList = filter.getSpeciesList()
        startDate = filter.getStartDate()
        endDate= filter.getEndDate()
        locationType = filter.getLocationType()
        locationName = filter.getLocationName()
        checklistID = filter.getChecklistID()
        
        # if no filteredSightingList is specified, create one.
        # use narrowest subset possible, according to filter            
        if checklistID != "":
            returnList = self.checklistDict[checklistID]
        elif speciesName != "":
            returnList = self.speciesDict[speciesName]
        elif speciesList != []:
            for sp in speciesList:
                for s in self.speciesDict[sp]:
                    returnList. append(s)
        elif startDate !="" and startDate == endDate:
            if startDate in self.dateDict.keys():
                returnList = self.dateDict[startDate]
            else:
                returnList = []
        elif locationType == "Country":
            returnList = self.countryDict[locationName]
        elif locationType == "State":
            returnList = self.stateDict[locationName]
        elif locationType == "County":
            returnList = self.countyDict[locationName]
        elif locationType == "Location":
            returnList = self.locationDict[locationName]                
        else:
            returnList = self.sightingList  
        
        return(returnList)


    def GetSpeciesWithData(self, filter,  filteredSightingList = [],  includeSpecies = "Species"):
        filteredDictWithDates = {}
        checklistIDs = {}
        returnList = []
        allChecklists = set()
        
        # if no filteredSightingList is specified, create one.
        # use narrowest subset possible, according to filter            
        if filteredSightingList == []:
            filteredSightingList = self.GetMinimalFilteredSightingsList(filter)
            
        # loop through sightingList and check each sighting for the filtered list criteria
        for sighting in filteredSightingList:
            
            if self.TestSighting(sighting,  filter) is True:
                
                # store the sighting date so we can get first and last later
                # include the taxonomy entry so we can sort the list by taxonomy later
                # include the main species name so we can store it in SpeciesList hidden data
                # include the checklist number so we can count checklists for each species
                thisDateTaxSpecies = [sighting[10],  sighting[3],  sighting[1], sighting[0]]
                
                # decide whether we're returning only species or also subspecies
                if includeSpecies == "Species":
                    key = sighting[1]
                if includeSpecies == "Subspecies":
                    key = sighting[23]
                
                # add the date and taxonomy number to a temp dictionary 
                # we'll use this dictionary later to find the first and last dates
                if key not in filteredDictWithDates.keys():
                    filteredDictWithDates[key] = [thisDateTaxSpecies]
                else:
                    filteredDictWithDates[key].append(thisDateTaxSpecies)
                    
                # add the checklist ID to a temp dictionary 
                # we'll use this dictionary later to sum the checklists per species
                if key not in checklistIDs.keys():
                    checklistIDs[key] = [thisDateTaxSpecies[3]]
                else:
                    checklistIDs[key].append(thisDateTaxSpecies[3])       
       
                # add checklistID to allChecklist set so we can count all the checklists later
                allChecklists.add(sighting[0])
    
        # get the total number of checklists so we can compute percentages 
        # of checklists for each species
        allChecklistCount = len(allChecklists)
        
        if len(filteredDictWithDates) > 0:            
            
            # initiate currentSpeciesIndex with data from first element in filteredListWithDates
            for s in filteredDictWithDates.keys():
                tempSpeciesList = filteredDictWithDates[s]
                tempSpeciesList.sort()
                thisCommonName = s
                thisFirstDate = tempSpeciesList[0][0]
                thisLastDate = tempSpeciesList[len(tempSpeciesList)-1][0]
                thisTaxNumber = float(tempSpeciesList[0][1])
                thisTopLevelSpeciesName = tempSpeciesList[0][2]
                thisChecklistCount = len(checklistIDs[s])
                percentageOfChecklists = round(100 * thisChecklistCount / allChecklistCount, 2)
                
                returnList.append([
                    thisCommonName, 
                    thisFirstDate,  
                    thisLastDate, 
                    thisTaxNumber,  
                    thisTopLevelSpeciesName, 
                    thisChecklistCount, 
                    percentageOfChecklists
                    ])
        
        returnList = sorted(returnList,  key=lambda x: (x[3]))
        
        return(returnList)


    def GetUniqueSpeciesForLocation(self,  filter,  location,  speciesList,  filteredSightingList = [],):
        uniqueSpeciesList = []
        
        # set filteredSightingList to master list if no filteredSightingList specified
        if filteredSightingList == []:
            filteredSightingList = self.GetMinimalFilteredSightings(filter)
        
        # for each sighting, test date if necessary. Append new dates to return list.
        for species in speciesList:
            isSeenNowhereElse = True
            for s in filteredSightingList:
                if self.TestSighting(s,  filter) is True:
                    if s[1] == species and s[7] != location:
                        isSeenNowhereElse = False
                        break
                
            if isSeenNowhereElse == True:
               if species not in uniqueSpeciesList:
                    uniqueSpeciesList.append(species)
                    
        return(uniqueSpeciesList)


    def TestSighting(self, sighting,  filter):
        locationType = filter.getLocationType()                             # str   choices are Country, County, State, Location, or ""
        locationName = filter.getLocationName()                         # str   name of region or location  or ""
        startDate = filter.getStartDate()                                           # str   format yyyy-mm-dd  or ""
        endDate = filter.getEndDate()                                               # str   format yyyy-mm-dd  or ""
        startSeasonalMonth = filter.getStartSeasonalMonth() # str   format mm
        startSeasonalDay = filter.getStartSeasonalDay()            # str   format dd
        endSeasonalMonth  = filter.getEndSeasonalMonth()    # str   format  dd
        endSeasonalDay  = filter.getEndSeasonalDay()               # str   format dd
        checklistID = filter.getChecklistID()                                     # str   checklistID
        sightingDate = sighting[10]                                                    # str   format yyyy-mm-dd
        speciesName = filter.getSpeciesName()                            # str   species Name
        speciesList = filter.getSpeciesList()                                      # list of species names
        order = filter.getOrder()                                                         # str   order name
        family = filter.getFamily()                                                         # str   family name
        time = filter.getTime()                                                               # str format HH:DD in 24-hour format
        
        # Check every filter setting. Return False immediately if sighting fails.
        # If sighting survives the filter, return True

        # if a checklistID has been specified, check if sighting matches
        if checklistID != "":
            if checklistID != sighting[0]:
                return(False)

        # if speciesName has been specified, check it
        if speciesName != "":
            if speciesName != sighting[1] and speciesName != sighting[23]:
                return(False)

        # if order  has been specified, check it
        if order != "":
            if order != sighting[21]:
                return(False)

        # if family  has been specified, check it
        if family != "":
            if family != sighting[22]:
                return(False)
                
        # if speciesList has been specified, check it
        if speciesList != []:
            if sighting[1] not in speciesList:
                return(False)                    

        # if family  has been specified, check it
        if time != "":
            if time != sighting[11]:
                return(False)
                
        # check if location matches for sighting; flag species that fit the location
        # no need to check if locationType is ""
        if not locationType == "":
            if locationType == "Country":
                if not locationName == sighting[5][0:2]:
                    return(False)
            if locationType == "State":
                if not locationName == sighting[5]:
                    return(False)   
            if locationType == "County":
                if not locationName == sighting[6]:
                    return(False)
            if locationType == "Location":
                if not locationName == sighting[7]:
                    return(False)                    
        
        # check date for matches for sighting range or seasonal range; disqualify sighting if date doesn't fit specific date range
        if not ((startDate == "") or (endDate == "")):
            # if sightingDate is before start date
            if sightingDate < startDate:
                return(False)
            # if sightingDate is after end date
            if sightingDate > endDate: 
                return(False)
        
        # check for seasonal range using month and date parts; disqualify sighting if date doesn't fit in seasonal range
        if not ((startSeasonalMonth == "") or (endSeasonalMonth== "")):
            sightingMonth = sightingDate[5:7]
            sightingDay = sightingDate[8:]
            # if startSeasonalMonth is earlier than endSeasonalMonth (e.g., July to October)
            if startSeasonalMonth < endSeasonalMonth:
                if sightingMonth < startSeasonalMonth:
                    return(False)
                if sightingMonth > endSeasonalMonth:
                    return(False)
                if sightingMonth == startSeasonalMonth:
                    if sightingDay < startSeasonalDay:
                        return(False)
                if sightingMonth == endSeasonalMonth:
                    if sightingDay > endSeasonalDay:
                        return(False)
            # if endSeasonalMonth is earlier than startSeasonalMonth (e.g., October to February)                                        
            if startSeasonalMonth > endSeasonalMonth:
                if sightingMonth < startSeasonalMonth:
                    if sightingMonth > endSeasonalMonth:
                        return(False)
                if sightingMonth == startSeasonalMonth:
                    if sightingDay < startSeasonalDay:
                        return(False)
                if sightingMonth == endSeasonalMonth:
                    if sightingDay > endSeasonalDay:
                        return(False)
            # if endSeasonalMonth is same as startSeasonalMonth (e.g., October and October)
            if startSeasonalMonth == endSeasonalMonth:
                if startSeasonalDay < endSeasonalDay:
                    if not sightingMonth == startSeasonalMonth:
                        return(False)
                    if sightingDay < startSeasonalDay:
                        return(False)
                    if sightingDay > endSeasonalDay:
                        return(False)
                if startSeasonalDay > endSeasonalDay:
                    if sightingMonth < startSeasonalMonth:
                        if sightingMonth > endSeasonalMonth:
                            return(False)
                    if sightingMonth == startSeasonalMonth:
                        if sightingDay > startSeasonalDay:
                            if sightingDay < endSeasonalDay:
                                return(False)
                if startSeasonalDay == endSeasonalDay:
                    if not sightingDay == startSeasonalDay:
                        return(False)
                    if not sightingMonth == startSeasonalMonth:
                        return(False)
        
        # if we've arrived here, the sighting passes the filter. 
        return(True)


    def GetDates(self, filter,  filteredSightingList=[]):
        dateList = set()
        needToCheckFilter = False
                
        # set filteredSightingList to master list if no filteredSightingList specified
        if filteredSightingList == []:
            filteredSightingList = self.GetMinimalFilteredSightingsList(filter)
            needToCheckFilter = True
                
        # for each sighting, test date if necessary. Append new dates to return list.
        for s in filteredSightingList:
            if needToCheckFilter is True:
                if self.TestSighting(s,  filter) is True:
                    dateList.add(s[10])
            else:
                dateList.add(s[10])
        
        # convert the set to a list and sort it. 
        dateList = list(dateList)
        dateList.sort()
        
        return(dateList)


    def ClearDatabase(self):
        
        self.eBirdFileOpenFlag = False
        self.countryStateCodeFileFound = False
        self.allSpeciesList = []
        self.familyList = []
        self.masterLocationList = []
        self.countryList = []
        self.stateList = []
        self.countyList = []
        self.locationList = []
        self.sightingList = []
        self.speciesDict = defaultdict()
        self.yearDict = defaultdict()
        self.monthDict = defaultdict()
        self.dateDict = defaultdict()
        self.countryDict = defaultdict()
        self.stateDict = defaultdict()
        self.countyDict = defaultdict()
        self.locationDict = defaultdict()
        self.checklistDict = defaultdict()
        

    def CountSpecies(self,  speciesList):
        
        # method to count true species in a list. Entries with parens, /, or sp. should not be counted,
        # unless no non-paren entries exist for that species.append
        speciesSet = set()
        
        # use a set (which deletes duplicates) to hold species names
        # remove parens from species names if they exist
        for s in speciesList:
            if "(" in s:
                speciesSet.add(s.split(" (")[0])
            elif "sp." in s:
                pass
            elif "/" in s:
                pass
            else:
                speciesSet.add(s)
        
        # count the species, including species whose parens have been removed
        count = len(speciesSet)
        
        return(count)

    def GetChecklists(self,  filter):
        returnList = []
        checklistIDs = set()
        
        # speed retreaval by choosing minimal set of sightings to search
        minimalSightingList = self.GetMinimalFilteredSightingsList(filter)
        
        # gather the IDs of checklists that match the filter
        for s in minimalSightingList:
            if self.TestSighting(s,  filter) is True:
                checklistIDs .add(s[0])
        
        # get all the sightings that match these checklistIDs
        for c in checklistIDs:
            
            # set up blank list to hold species names
            checklistSpecies = []
            
            # use the checklistDict to return sightings that match checklist ID
            for sighting in self.checklistDict[c]:
                
                # append species common name to list, so we can count the species
                checklistSpecies.append(sighting[1])
                
            # count the species, discarding superflous subspecies, spuhs and slashes when necessary
            speciesCount = MainWindow.db.CountSpecies(checklistSpecies)
            
            # compile data for checklist (id, country, county, location, date, time, speciesCount)
            checklistData= [sighting[0],  sighting[5],  sighting[6], sighting[7], sighting[10], sighting[11],  speciesCount]
            
            returnList.append(checklistData)    
            
        # sort by country, county, location, date, time
        returnList=  sorted(returnList, key=lambda x: (x[1],  x[2],  x[3],  x[4],  x[5]))

        return(returnList)


    def GetFindResults(self,  searchString, checkedBoxes):
        
        foundSet = set()
        
        for s in self.sightingList:
            for c in checkedBoxes:
                if c == "chkCommonName":
                    if searchString.lower() in s[1].lower():
                        foundSet.add(("Common Name",  s[0], s[7],  s[10], s[1]))
                if c == "chkScientificName":
                    if searchString.lower() in s[2].lower():
                        foundSet.add(("Scientific Name",  s[0], s[7],  s[10], s[2]))                    
                if c == "chkCountryName":
                    if searchString.lower() in self.GetCountryName(s[5][0:2]).lower():
                        foundSet.add(("Country",  s[0], s[7],  s[10],  self.GetCountryName(s[5][0:2])))
                if c == "chkStateName":
                    if searchString.lower() in self.GetStateName(s[5]).lower():
                        foundSet.add(("State",  s[0], s[7],  s[10],  self.GetStateName(s[5])))
                if c == "chkCountyName":
                    if searchString.lower() in s[6].lower():
                        foundSet.add(("County",  s[0], s[7],  s[10],  s[6]))
                if c == "chkLocationName":
                    if searchString.lower() in s[7].lower():
                        foundSet.add(("Location",  s[0], s[7],  s[10],  s[7]))
                if c == "chkSpeciesComments":
                    if searchString.lower() in s[19].lower():
                        foundSet.add(("Species Comments",  s[0], s[7],  s[10],  s[19]))
                if c == "chkChecklistComments":                    
                    if searchString.lower() in s[20].lower():
                        foundSet.add(("Checklist Comments",  s[0], s[7],  s[10],  s[20]))
                
            foundList = list(foundSet)
            foundList.sort()
                
        return(foundList)

    def GetLastDayOfMonth(self,  month):
                
        # find last day of the specified month
        if month in ["01",  "1",  "03",  "3",  "05",  "5",  "07",  "7",  "08",  "8",  "10",  "12"]:
            lastDayOfThisMonth = "31"
        if month in ["04",  "4",  "06",  "6",  "09",  "9",  "11"]:
            lastDayOfThisMonth = "30"
        if month in ["02",  "2"]:
            lastDayOfThisMonth = "29"
        return(lastDayOfThisMonth)


    def GetLocationCoordinates(self,  location):
        coordinates = []
        s = self.locationDict[location][0]
        coordinates.append(s[8])
        coordinates.append(s[9])

        return(coordinates)


    def GetLocations(self, filter, queryType="OnlyLocations",  filteredSightingList=[]):
        # queryType specifies which data fields to return in the returnList
        # "OnlyLocations" returns just the location names
        # "Checklist"returns  locationName, count, checklistID, and time
        # "LocationHierarchy" returns country, county, and location (country includes the state code)
        
        returnList = []
        
        if queryType == "Dates":
            tempDateDict = {}
        
        speciesName = filter.getSpeciesName()
        
        # set filteredSightingList to master list if no filteredSightingList specified
        if filteredSightingList == []:
            filteredSightingList = self.GetMinimalFilteredSightingsList(filter)
            
        sightingFound = False
        
        # for each sighting, test date if necessary. Append new dates to return list.
        for s in filteredSightingList:
            
            # If a single species is specified:
            # since the file is ordered by species taxonomically, we can stop for loop when we've 
            # found a species, processed all its entries, and then moved on to a different species
            # this prevents us from needlessly checking all sightings in the whole database
            if speciesName != "":
                if sightingFound is True:
                    if s[1] != speciesName and speciesName != s[23]:
                        break
                    
            if self.TestSighting(s,  filter) is True:
                
                sightingFound = True
                                    
                if queryType == "OnlyLocations":
                    thisLocationList = s[7]
                
                if queryType == "Checklist":
                    thisLocationList = [s[7],  s[4],  s[0],  s[8]]

                if queryType == "LocationHierarchy":
                    thisLocationList = [s[5],  s[6],  s[7]]

                # if we're getting first and last dates, too, we need to 
                # store all dates in a dictionary keyed by location
                # so later we can sort them and return the first and last dates, too
                if queryType == "Dates":
                    
                    keyName = s[7]
                    
                    if keyName not in tempDateDict.keys():
                        tempDateDict[keyName] = [s[10] + " " + s[11]]
                    else:
                        tempDateDict[keyName].append(s[10] + " " + s[11])
                
                if queryType != "Dates":
                    # add entry to returnList if it's not a duplicate
                    if thisLocationList not in returnList:
                        returnList.append(thisLocationList)
        
        # if we're returning dates, find the first and last dates from dictionary
        # loop through all keys (location names) and append the name and dates
        # to the return list
        if queryType == "Dates":
            for k in tempDateDict.keys():
                tempDateList = tempDateDict[k]
                tempDateList.sort()
                tempFirstDate = tempDateList[0]
                tempLastDate = tempDateList[len(tempDateList)-1]
                thisLocationList = [k,  tempFirstDate,  tempLastDate]
                returnList.append(thisLocationList)
        
        # sort the list and return it
        returnList.sort()
        return(returnList)


    def GetNewCountrySpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset,  speciesList):
        
        countries = set()
        countrySpecies = []
        tempFilter = deepcopy(filter)
        
        # loop through sightingListForSpeciesSubset to gather relevant country names
        for s in sightingListForSpeciesSubset:
            if self.TestSighting(s,  tempFilter) is True:
                countries.add(s[5][0:2])
        countries = list(countries)
        countries.sort()
        
        # loop through countries to gather first-time species sightings
        for country in countries:
            
            # get list of species with first/last dates for specific country filter
            tempFilter.setLocationType("Country")
            tempFilter.setLocationName(country)
            
            speciesWithFirstLastDates = self.GetSpeciesWithData(tempFilter,  filteredSightingList)
            
            # use dictionary created when data file was first loaded to get all sightings from 
            # the selected country
            thisCountrySightings = self.countryDict[country]
            
            # create temporary dictionary of sightings in selected country
            # keyed by species name
            tempSpeciesDict = {}
            for tcs in thisCountrySightings:

                keyName = tcs[1]
                
                if tcs[1] not in tempSpeciesDict.keys():
                    tempSpeciesDict[keyName] = [tcs]
                else:
                    tempSpeciesDict[keyName].append(tcs)

            # loop through species with dates to see if any sightings are the 
            # first for the country
            for species in speciesWithFirstLastDates:
                tempSpeciesSightings = tempSpeciesDict[species[0]]
                tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
                if species[1] <= tempSpeciesSightings[0][10]:
                    countrySpecies.append([country,  species[0]])
        
        return(countrySpecies)


    def GetNewCountySpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset,  speciesList):
        
        # find which years are in the filtered sightingsfor the species in question
        counties = set()
        countySpecies = []
        tempFilter = deepcopy(filter)

        # loop through speciesWithFirstLastDates to gather county names for sightings subset
        for s in sightingListForSpeciesSubset:
            if self.TestSighting(s,  tempFilter) is True:
                if s[6] != "":
                    counties.add(s[6])
        counties = list(counties)
        counties.sort()
        
        # loop through counties, keeping species that are new sightings
        for county in counties:
            
            # get list of species with first/last dates for filter in selected county
            tempFilter.setLocationType("County")
            tempFilter.setLocationName(county)
            speciesWithFirstLastDates = self.GetSpeciesWithData(tempFilter,  filteredSightingList)
            
            thisCountySightings = self.countyDict[county]
            
            # create temporary dictionary of sightings in selected county
            # keyed by species name            
            tempSpeciesDict = {}
            for tms in thisCountySightings:
                if tms[1] not in tempSpeciesDict.keys():
                    tempSpeciesDict[tms[1]] = [tms]
                else:
                    tempSpeciesDict[tms[1]].append(tms)

            # loop through species with dates to see if any sightings are the 
            # first for the county
            for species in speciesWithFirstLastDates:
                tempSpeciesSightings = tempSpeciesDict[species[0]]
                tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
                if species[1] <= tempSpeciesSightings[0][10]:
                    countySpecies.append([county,  species[0]])                    
        
        return(countySpecies)


    def GetNewLifeSpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset):
        
        # find which years are in the filtered sightingsfor the species in question
        # DON'T use a SET here, because we want to keep the species taxonomic order 
        lifeSpecies = []
        
        # get list of species with first/last dates for filter
        speciesWithFirstLastDates = self.GetSpeciesWithData(filter,  filteredSightingList)

        for species in speciesWithFirstLastDates:
            tempSpeciesSightings = self.speciesDict[species[0]]
            tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
            if species[1] <= tempSpeciesSightings[0][10]:
                lifeSpecies.append(species[0])        
                        
        return(lifeSpecies)


    def GetNewLocationSpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset,  speciesList):
        
        # find which years are in the filtered sightingsfor the species in question
        locations = set()
        locationSpecies = []
        tempFilter = deepcopy(filter)
        
        for s in sightingListForSpeciesSubset:
            if self.TestSighting(s,  filter) is True:
                locations.add(s[7])
        locations = list(locations)
        locations.sort()
        
        # loop through speciesWithFirstLastDates for each state, keeping species that are new
        for location in locations:
            # get list of species with first/last dates for filter                
            tempFilter.setLocationType("Location")
            tempFilter.setLocationName(location)
            
            speciesWithFirstLastDates = self.GetSpeciesWithData(tempFilter,  filteredSightingList)
            
            thisLocationSightings = self.locationDict[location]
                        
            tempSpeciesDict = {}
            for tms in thisLocationSightings:
                if tms[1] not in tempSpeciesDict.keys():
                    tempSpeciesDict[tms[1]] = [tms]
                else:
                    tempSpeciesDict[tms[1]].append(tms)

            for species in speciesWithFirstLastDates:
                tempSpeciesSightings = tempSpeciesDict[species[0]]
                tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
                if species[1] <= tempSpeciesSightings[0][10]:
                    locationSpecies.append([location,  species[0]])         
                        
        return(locationSpecies)            


    def GetNewMonthSpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset):
        
        # find which months are in the filtered sightingsfor the species in question
        months = set()
        monthSpecies = []
        
        for s in sightingListForSpeciesSubset:
            if self.TestSighting(s,  filter) is True:
                months.add(s[10][5:7])
        months = list(months)
        months.sort()
        
        # get list of species with first/last dates for filter
        for month in months:
            # set temporary filter with each month in loop in filter
            tempFilter = deepcopy(filter)
            tempFilter.setStartSeasonalMonth(month)
            tempFilter.setStartSeasonalDay("01")
            tempFilter.setEndSeasonalMonth(month)
            
            lastDayOfThisMonth = self.GetLastDayOfMonth(month)
            
            tempFilter.setEndSeasonalDay(lastDayOfThisMonth)
            
            speciesWithFirstLastDates = self.GetSpeciesWithData(tempFilter,  filteredSightingList)
            
            thisMonthSightings = self.monthDict[month]
            
            tempSpeciesDict = {}
            for tms in thisMonthSightings:
                if tms[1] not in tempSpeciesDict.keys():
                    tempSpeciesDict[tms[1]] = [tms]
                else:
                    tempSpeciesDict[tms[1]].append(tms)

            for species in speciesWithFirstLastDates:
                tempSpeciesSightings = tempSpeciesDict[species[0]]
                tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
                if species[1] <= tempSpeciesSightings[0][10]:
                    monthRange = ["Jan",  "Feb",  "Mar",  "Apr", "May",   "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec"]
                    monthName = monthRange[int(month)-1]
                    monthSpecies.append([monthName,  species[0]])                       
        
        return(monthSpecies)


    def GetNewStateSpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset,  speciesList):
        
        # find which years are in the filtered sightingsfor the species in question
        states = set()
        stateSpecies = []
        tempFilter = deepcopy(filter)
        
        for s in sightingListForSpeciesSubset:
            if self.TestSighting(s,  tempFilter) is True:
                states.add(s[5])
        states = list(states)
        states.sort()
        
        # loop through speciesWithFirstLastDates for each state, keeping species that are new
        for state in states:
            # get list of species with first/last dates for filter
            tempFilter.setLocationType("State")
            tempFilter.setLocationName(state)
            
            speciesWithDates = self.GetSpeciesWithData(tempFilter,  filteredSightingList)
            thisStateSightings = self.stateDict[state]
            
            tempSpeciesDict = {}
            for tms in thisStateSightings:
                if tms[1] not in tempSpeciesDict.keys():
                    tempSpeciesDict[tms[1]] = [tms]
                else:
                    tempSpeciesDict[tms[1]].append(tms)

            for species in speciesWithDates:
                tempSpeciesSightings = tempSpeciesDict[species[0]]
                tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
                if species[1] <= tempSpeciesSightings[0][10]:
                    stateSpecies.append([state,  species[0]])            
                        
        return(stateSpecies)


    def GetNewYearSpecies(self,  filter,  filteredSightingList,  sightingListForSpeciesSubset):
        
        # find which years are in the filtered sightingsfor the species in question
        years = set()
        yearSpecies = []
        thisFilter = deepcopy(filter)
        
        for s in sightingListForSpeciesSubset:
            if self.TestSighting(s,  filter) is True:
                years.add(s[10][0:4])
        years = list(years)
        years.sort()
        
        for year in years:
            thisYearSightings = self.yearDict[year]

            # get list of species with first/last dates for filter
            startDate = year + "-01-01"
            endDate = year + "-12-31"
            thisFilter.setStartDate(startDate)
            thisFilter.setEndDate(endDate)
            speciesWithDates = self.GetSpeciesWithData(thisFilter,  filteredSightingList)

            tempSpeciesDict = {}
            for tms in thisYearSightings:
                if tms[1] not in tempSpeciesDict.keys():
                    tempSpeciesDict[tms[1]] = [tms]
                else:
                    tempSpeciesDict[tms[1]].append(tms)

            for species in speciesWithDates:
                tempSpeciesSightings = tempSpeciesDict[species[0]]
                tempSpeciesSightings = sorted(tempSpeciesSightings, key=lambda x: (x[10]))
                if species[1] <= tempSpeciesSightings[0][10]:
                    yearSpecies.append([year,  species[0]])   
                        
        return(yearSpecies)


    def GetFamilyName(self,  species):
        
        filteredSightingList = self.speciesDict[species]
        
        familyName = filteredSightingList[0][22]
        
        return(familyName)

    
    def GetOrderName(self,  species):
        
        filteredSightingList = self.speciesDict[species]
        
        orderName = filteredSightingList[0][21]
        
        return(orderName)        

    
    def GetScientificName(self,  species):

        filteredSightingList = self.speciesDict[species]
        
        scientificName = filteredSightingList[0][2]
        
        return(scientificName)


    def GetCountryCode(self,  longName):
        
        if longName == "**All Countries**":
            return("**All Countries**")
        
        if self.countryStateCodeFileFound is True:
            for l in self.masterLocationList:
                if l[4] == longName:
                    return(l[0])
        else:
            return(longName)                    

                
    def GetStateCode(self,  longName):
        
        if longName == "**All States**":
            return("**All States**")
            
        if self.countryStateCodeFileFound is True:
            for l in self.masterLocationList:
                if l[5] == longName:
                    return(l[1])
        else:
            return(longName)


    def GetCountryName(self,  shortCode):
        
        if shortCode == "**All Countries**":
            return("**All Countries**")
            
        if self.countryStateCodeFileFound is True:
            for l in self.masterLocationList:
                if l[0] == shortCode:
                    return(l[4])
        else:
            return(shortCode)


    def GetMonthName(self,  monthNumberString):
        
        monthName = self.monthNameDict[monthNumberString]
        return(monthName)


    def GetStateName(self,  shortCode):

        if shortCode == "**All States**":
            return("**All States**")            
        
        if self.countryStateCodeFileFound is True:            
            for l in self.masterLocationList:
                if l[1] == shortCode:
                    return(l[5])                    
        else:
            return(shortCode)


class MainWindow(QMainWindow, MDIMain.Ui_MainWindow):

    # initialize main database that will be used throughout program
    db = DataBase()
    fontSize = 11
    scaleFactor = 1
    versionNumber = "0.1"
    versionDate = "March 8, 2018"    

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.setCentralWidget(self.mdiArea)
        self.actionOpen.triggered.connect(self.OpenDataFile)
        self.actionAboutLapwing.triggered.connect(self.CreateAboutLapwing)        
        self.actionExit.triggered.connect(self.ExitApp)
        self.actionShowFilter.triggered.connect(self.showFilter)
        self.actionHideFilter.triggered.connect(self.hideFilter)
        self.actionClearFilter.triggered.connect(self.clearFilter)
        self.actionDateTotals.triggered.connect(self.CreateDateTotals)
        self.actionLocationTotals.triggered.connect(self.CreateLocationTotals)
        self.actionCompareLists.triggered.connect(self.CreateCompareLists)
        self.actionTileWindows.triggered.connect(self.TileWindows)
        self.actionCascade.triggered.connect(self.CascadeWindows)
        self.actionCloseAllWindows.triggered.connect(self.CloseAllWindows)
        self.actionSpecies.triggered.connect(self.CreateSpeciesList)
        self.actionChecklists.triggered.connect(self.CreateChecklistsList)
        self.actionLocations.triggered.connect(self.CreateLocationsList)
        self.actionPrint.triggered.connect(self.printMe)
        self.actionCreatePDF.triggered.connect(self.CreatePDF)
        self.actionFamilies.triggered.connect(self.CreateFamiliesReport)
        self.actionBigReport.triggered.connect(self.CreateBigReport)
        self.actionMap.triggered.connect(self.CreateMap)
        self.actionFind.triggered.connect(self.CreateFind)
        self.cboStartSeasonalRangeMonth.addItems(["Jan",  "Feb",  "Mar",  "Apr",  "May", "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec"])
        self.cboEndSeasonalRangeMonth.addItems(["Jan",  "Feb",  "Mar",  "Apr",  "May", "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec"])
        for d in range(1,  32):
            self.cboStartSeasonalRangeDate.addItem(str(d))
            self.cboEndSeasonalRangeDate.addItem(str(d))
        self.cboDateOptions.addItems(["No Date Filter",  "Use Calendars Below",  "This Year",  "This Month",  "Today",  "Yesterday"])            
        self.cboSeasonalRangeOptions.addItems(["No Seasonal Range",  "Use Range Below",  "Spring",  "Summer",  "Fall",  "Winter",  "This Month", "Year to Date"])                    
        self.cboCountries.currentIndexChanged.connect(self.ComboCountriesChanged)
        self.cboStates.currentIndexChanged.connect(self.ComboStatesChanged)
        self.cboCounties.currentIndexChanged.connect(self.ComboCountiesChanged)
        self.cboLocations.currentIndexChanged.connect(self.ComboLocationsChanged)
        self.cboOrders.currentIndexChanged.connect(self.ComboOrdersChanged)
        self.cboFamilies.currentIndexChanged.connect(self.ComboFamiliesChanged)
        self.cboSpecies.currentIndexChanged.connect(self.ComboSpeciesChanged)
        self.cboDateOptions.currentIndexChanged.connect(self.ComboDateOptionsChanged)
        self.cboSeasonalRangeOptions.currentIndexChanged.connect(self.ComboSeasonalRangeOptionsChanged)
        self.calStartDate.dateChanged.connect(self.CalendarClicked)
        self.calEndDate.dateChanged.connect(self.CalendarClicked)
        self.cboStartSeasonalRangeMonth.currentIndexChanged.connect(self.SeasonalRangeClicked)
        self.cboStartSeasonalRangeDate.currentIndexChanged.connect(self.SeasonalRangeClicked)
        self.cboEndSeasonalRangeMonth.currentIndexChanged.connect(self.SeasonalRangeClicked)
        self.cboEndSeasonalRangeDate.currentIndexChanged.connect(self.SeasonalRangeClicked)
        self.fillingLocationComboBoxesFlag = False  
        self.calStartDate.setDate(datetime.datetime.now())
        self.calEndDate.setDate(datetime.datetime.now())
        
        self.lblSlider = QLabel(self.statusBar)
        self.lblSlider.setText("Display Size")
        self.sldFontSize = QSlider(self.statusBar)
        self.sldFontSize.setSingleStep(10)
        self.sldFontSize.setProperty("value", 50)
        self.sldFontSize.setOrientation(Qt.Horizontal)
        self.sldFontSize.setObjectName("sldFontSize")
        self.sldFontSize.valueChanged.connect(self.ScaleDisplay)    
        self.statusBar.addWidget(self.lblSlider)
        self.statusBar.addWidget(self.sldFontSize)
        
        self.setWindowTitle("Lapwing v. " + self.versionNumber)

        self.HideMainWindowOptions()

        self.showMaximized()
        self.ScaleDisplay()
        
        
    def ScaleDisplay(self):
        self.scaleFactor = self.sldFontSize.value()/50
        if self.scaleFactor > 1:
            self.scaleFactor = 1 + modf(self.scaleFactor)[0] * 3
        if self.scaleFactor < 1:
            self.scaleFactor = (1 + self.scaleFactor) / 2
        self.fontSize = floor(11 * self.scaleFactor)
        MainWindow.fontSize = self.fontSize
        MainWindow.scaleFactor = self.scaleFactor
        
        self.menuBar.setFont(QFont("Helvetica", self.fontSize))     
                        
        for a in self.toolBar.actions():
            a.setFont(QFont("Helvetica", self.fontSize))                    
        
        # scale the main filter dock
        for w in self.frmFilter.children():
         
            if w.objectName()[0:3] == "cbo":
                styleSheet = w.styleSheet()
                w.setStyleSheet("")
                w.setFont(QFont("Helvetica", self.fontSize))                    
                metrics = w.fontMetrics()
                cboText = w.currentText()
                if cboText == "":
                    cboText = "Dummy Text"
                itemTextWidth = metrics.boundingRect(cboText).width()
                itemTextHeight = metrics.boundingRect(cboText).height()
                w.setMinimumWidth(floor(1.1 * itemTextWidth))
                w.setMinimumHeight(floor(1.1 * itemTextHeight))
                w.setMaximumHeight(floor(1.1 * itemTextHeight))
                w.resize(1.1 * itemTextHeight, 1.1 * itemTextWidth)
                w.setStyleSheet(styleSheet)
       
            if w.objectName()[0:3] == "lbl":
                w.setFont(QFont("Helvetica", self.fontSize))    
                metrics = w.fontMetrics()
                labelText = w.text()
                itemTextWidth = metrics.boundingRect(labelText).width()
                itemTextHeight = metrics.boundingRect(labelText).height()
                w.setMinimumWidth(floor(itemTextWidth))
                w.setMinimumHeight(floor(itemTextHeight))
                w.setMaximumHeight(floor(itemTextHeight))
                w.resize(itemTextHeight, itemTextWidth)  
                w.setStyleSheet("QLabel { font: bold }");
                                      
            if w.objectName()[0:3] == "cal":
                styleSheet = w.styleSheet()
                w.setStyleSheet("")
                w.setFont(QFont("Helvetica", self.fontSize))  
                metrics = w.fontMetrics()
                startDate = (
                               str(self.calStartDate.date().year()) 
                            + "-" 
                            + str(self.calStartDate.date().month()) 
                            + "-" 
                            + str(self.calStartDate.date().day()))
                itemTextWidth = metrics.boundingRect(startDate).width()
                itemTextHeight = metrics.boundingRect(startDate).height()
                w.setMinimumWidth(floor(1.1 * itemTextWidth))
                w.setMinimumHeight(floor(1.1 * itemTextHeight))
                w.setMaximumHeight(floor(1.1 * itemTextHeight))
                w.resize(1.1 * itemTextHeight, 1.1 * itemTextWidth)                     
                w.setStyleSheet(styleSheet)
        
        for w in self.frmStartSeasonalRange.children():
        
            if w.objectName()[0:3] == "cbo":
                styleSheet = w.styleSheet()
                w.setStyleSheet("")
                w.setFont(QFont("Helvetica", self.fontSize))    
                metrics = w.fontMetrics()
                cboText = w.currentText()
                itemTextWidth = metrics.boundingRect(cboText).width()
                itemTextHeight = metrics.boundingRect(cboText).height()
                w.setMinimumWidth(floor(1.1 * itemTextWidth))
                w.setMinimumHeight(floor(1.1 * itemTextHeight))
                w.setMaximumHeight(floor(1.1 * itemTextHeight))
                w.resize(1.1 * itemTextHeight, 1.1 * itemTextWidth)                   
                w.setStyleSheet(styleSheet)   

        for w in self.frmEndSeasonalRange.children():
        
            if w.objectName()[0:3] == "cbo":
                styleSheet = w.styleSheet()
                w.setStyleSheet("")
                w.setFont(QFont("Helvetica", self.fontSize))    
                metrics = w.fontMetrics()
                cboText = w.currentText()
                itemTextWidth = metrics.boundingRect(cboText).width()
                itemTextHeight = metrics.boundingRect(cboText).height()
                w.setMinimumWidth(floor(1.1 * itemTextWidth))
                w.setMinimumHeight(floor(1.1 * itemTextHeight))
                w.setMaximumHeight(floor(1.1 * itemTextHeight))
                w.resize(1.1 * itemTextHeight, 1.1 * itemTextWidth)                   
                w.setStyleSheet(styleSheet)   

        self.frmStartSeasonalRange.setMinimumWidth(floor(1.5 * itemTextWidth))
        self.frmStartSeasonalRange.setMinimumHeight(floor(1.5* itemTextHeight))
        self.frmStartSeasonalRange.setMaximumHeight(floor(1.5 * itemTextHeight))
        self.frmStartSeasonalRange.resize(1.5 * itemTextHeight, 1.5 * itemTextWidth) 
        self.frmStartSeasonalRange.adjustSize()
        
        self.frmEndSeasonalRange.setMinimumWidth(floor(1.5 * itemTextWidth))
        self.frmEndSeasonalRange.setMinimumHeight(floor(1.5* itemTextHeight))
        self.frmEndSeasonalRange.setMaximumHeight(floor(1.5 * itemTextHeight))
        self.frmEndSeasonalRange.resize(1.5 * itemTextHeight, 1.5 * itemTextWidth)  
        self.frmEndSeasonalRange.adjustSize()
                
        # scale open children windows
        for w in self.mdiArea.subWindowList():        
            w.scaleMe()
        
    
    def clearFilter(self):
        self.cboCountries.setCurrentIndex(0)
        self.cboStates.setCurrentIndex(0)
        self.cboCounties.setCurrentIndex(0)
        self.cboLocations.setCurrentIndex(0)
        self.cboOrders.setCurrentIndex(0)
        self.cboFamilies.setCurrentIndex(0)
        self.cboSpecies.setCurrentIndex(0)
        self.cboDateOptions.setCurrentIndex(0)
        self.cboSeasonalRangeOptions.setCurrentIndex(0)
        
        
    def hideFilter(self):
        self.dckFilter.hide()


    def setCountryFilter(self, country):
        index = self.cboCountries.findText(country)
        if index >= 0:
             self.cboCountries.setCurrentIndex(index)

             
    def setCountyFilter(self, county):
        self.cboCountries.setCurrentIndex(0)
        self.cboStates.setCurrentIndex(0)
        index = self.cboCounties.findText(county)
        if index >= 0:
             self.cboCounties.setCurrentIndex(index)

             
    def setStateFilter(self, state):
        self.cboCountries.setCurrentIndex(0)
        index = self.cboStates.findText(state)
        if index >= 0:
             self.cboStates.setCurrentIndex(index)


    def setLocationFilter(self, location):
        self.cboCountries.setCurrentIndex(0)
        self.cboStates.setCurrentIndex(0)
        self.cboCounties.setCurrentIndex(0)
        index = self.cboLocations.findText(location)
        if index >= 0:
             self.cboLocations.setCurrentIndex(index)


    def setSpeciesFilter(self, species):
        index = self.cboSpecies.findText(species)
        if index >= 0:
             self.cboSpecies.setCurrentIndex(index)


    def setDateFilter(self, startDate, endDate = ""):
        
        # if only one date is specified, use that date for both start and end dates
        if endDate == "":
            endDate = startDate
            
        startYear = int(startDate[0:4])
        startMonth = int(startDate[5:7])
        startDay = int(startDate[8:])
        myStartDate = QDate()
        myStartDate.setDate(startYear, startMonth, startDay)
        
        endYear = int(endDate[0:4])
        endMonth = int(endDate[5:7])
        endDay = int(endDate[8:])
        myEndDate = QDate()
        myEndDate.setDate(endYear, endMonth, endDay)        
        
        self.calStartDate.setDate(myStartDate)
        self.calEndDate.setDate(myEndDate)


    def setSeasonalRangeFilter(self, month):
        index = self.cboStartSeasonalRangeMonth.findText(month)
        if index >= 0:
             self.cboStartSeasonalRangeMonth.setCurrentIndex(index)
             self.cboEndSeasonalRangeMonth.setCurrentIndex(index)
             self.cboStartSeasonalRangeDate.setCurrentIndex(0)
             self.cboEndSeasonalRangeDate.setCurrentIndex(30)

             
    def showFilter(self):
        self.dckFilter.show()
        
        
    def keyPressEvent(self, e):
        # open file dalog routine if user presses Crtl-O
        if e.key() == Qt.Key_O and e.modifiers() & Qt.ControlModifier:
            self.OpenDataFile()

        # open file dalog routine if user presses Crtl-O
        if e.key() == Qt.Key_F and e.modifiers() & Qt.ControlModifier:
            self.CreateFind()

                
    def CalendarClicked(self):
        if MainWindow.db.eBirdFileOpenFlag is True:
            self.cboDateOptions.setCurrentIndex(1)


    def CreateFind(self):
        
        # if no data file is currently open, abort
        if MainWindow.db.eBirdFileOpenFlag is False:
            self.CreateMessageNoFile()   
            return
        
        sub = Find()
        
        # save the MDI window as the parent for future use in the child            
        sub.mdiParent = self
        
        # add and position the child to our MDI area        
        self.mdiArea.addSubWindow(sub)
        sub.setGeometry(self.dckFilter.width() * 2, self.dckFilter.height() * .25, sub.width(), sub.height())

        sub.show()
        
        
    def CreateMessageNoFile(self):
        QApplication.restoreOverrideCursor() 
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("No ebird data is currently loaded.\n\nPlease open an eBird data file.")
        msg.setWindowTitle("No Data")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def CreateMessageNoResults(self):
        
        QApplication.restoreOverrideCursor() 
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("No sightings match the current filter settings.")
        msg.setWindowTitle("No Sightings")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        
        
    def PositionChildWindow(self, child,  creatingWindow):
        
        # if creatingWindow is the maind MDI window, center the new child window
        if creatingWindow.objectName() == "MainWindow":
            childWindowCoordinates = []
            for window in self.mdiArea.subWindowList():        
                if window.isVisible() == True:
                    childWindowCoordinates.append([window.x(),  window.y()])
            # try to place child window, but check if that would exactly overlap another window
            x = 10
            y = 10
            # if x, y is already the top left coordinate of a child window, add 20 to x and y and retry
            while [x, y] in childWindowCoordinates:
                x = x + 25
                y = y + 25
            child.setGeometry(x, y, child.width(), child.height())
        
        # if creatingWindow is a child window, place new child window cascaded down from calling creatingWindow
        else:
            x = creatingWindow.x() + 25
            y = creatingWindow.y() + 25
        child.setGeometry(x, y, child.width(), child.height())
        
        child.setFocus()

    def OpenDataFile(self):  
        # clear and close any data if a file is already open

        self.ResetMainWindow()
        self.db.ClearDatabase()
        self.clearFilter()

        fname = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileNames()", "","eBird Data Files (*.csv *.zip)")
                
        if fname[0] != "":
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
            
            self.fillingLocationComboBoxesFlag = True
            
            MainWindow.db.ReadDataFile(fname)            
            
            # now try to open a taxonomy file, if one exists in the same directory as the python script
            # get the directory path leading to the file in an OS-neutral way
            
            # look for a taxonomy file. It must be in the same directory as the script directory
            # and be a csv file named "eBird_Taxonomy.csv"
            if getattr(sys, 'frozen', False):
                # frozen
                scriptDirectory = os.path.dirname(sys.executable)
            else:
                # unfrozen
                scriptDirectory = os.path.dirname(os.path.realpath(__file__))
                               
            # scriptDirectory = os.path.dirname(__file__)
            taxonomyFile = os.path.join(scriptDirectory, "eBird_Taxonomy.csv")
            
            if os.path.isfile(taxonomyFile) is True:
                MainWindow.db.ReadTaxonomyDataFile(taxonomyFile)
                
            # try to open the country-state code file , if one exists in the same directory as python script
            # this file lists all the country and state codes, and their longer names for better legibility
            # It must be named "ebird_api_ref_location_eBird_list_subnational1.csv".
            countryStateCodeFile = os.path.join(scriptDirectory, "ebird_api_ref_location_eBird_list_subnational1.csv")
            if os.path.isfile(countryStateCodeFile) is True:
                MainWindow.db.ReadCountryStateCodeFile(countryStateCodeFile)                

            if MainWindow.db.eBirdFileOpenFlag is True:
                self.FillMainComboBoxes()
                self.CreateSpeciesList()
                
            # we're done filling the comboboxes, so set the flag to false
            # the flag, when True, prevents this method from being called 
            # every time the program adds a location to the combo boxes.
            self.fillingLocationComboBoxesFlag = False
            
            self.ShowMainWindowOptions()
            
        QApplication.restoreOverrideCursor()


    def CreateBigReport(self): 
        # the Create Analysis Report button was clicked
        # spawn a new ChildAnalysis window and fill it
        
        # if no data file is currently open, abort
        if MainWindow.db.eBirdFileOpenFlag is False:
            self.CreateMessageNoFile()   
            return
            
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))            
        
        # get the current filter settings in a list to pass to new child
        filter = self.GetFilter()
        
        # create new Analysis child window
        sub = BigReport()
        
        # set the mdiParent variable in the child so it can know the 
        # object that called it (for later use in the child)
        sub.mdiParent = self
        
        # call the child's routine to fill it with data
        if sub.FillAnalysisReport(filter) is False:
            self.CreateMessageNoResults()
            sub.close()
            
        else:
        
            # add child to MDI area and position it
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.show() 
        
        QApplication.restoreOverrideCursor() 
        
                       
    def CreateChecklistsList(self): 
        # Create Filtered List button was clicked
        # create filtered species list child
        
        # if no data file is currently open, abort
        if MainWindow.db.eBirdFileOpenFlag is False:
            self.CreateMessageNoFile()   
            return
            
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))            
        
        # get the current filter settings in a list to pass to child
        filter = self.GetFilter()
        
        # create child window 
        sub = Lists()
        
        # save the MDI window as the parent for future use in the child
        sub.mdiParent = self
        
        # call the child's fill routine, passing the filter settings list
        if sub.FillChecklists(filter) is True:
            
            # add and position the child to our MDI area
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.show() 

        else:
            
            self.CreateMessageNoResults()
            sub.close()
        
        QApplication.restoreOverrideCursor()                        
                    
                 
    def CreatePDF(self):
        
        activeWindow = self.mdiArea.activeSubWindow()

        if activeWindow is None:
            return

        if activeWindow.objectName() in ([
            "frmSpeciesList", 
            "frmFamilies", 
            "frmCompare", 
            "frmDateTotals", 
            "frmLocationTotals", 
            "frmWeb", 
            "frmIndividual", 
            "frmLocation",
            "frmBigReport"
            ]):

            # create a QTextDocument in memory to hold and render our content
            document = QTextDocument()

            # create a QPrinter object for the printer the user later selects
            printer = QPrinter()
            
            # set printer to PDF output, Letter size
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setPaperSize(QPrinter.Letter);
            printer.setPageMargins(20, 10, 10, 10, QPrinter.Millimeter)

            # set the document to the printer's page size
            pageSize = printer.paperSize(QPrinter.Point)
            document.setPageSize(pageSize)
            
            filename = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileNames()", "","PDF Files (*.pdf)")
            
            if filename[0] != "":
                
                # set output file name
                printer.setOutputFileName(filename[0])
            
                # get html content from child window
                html = activeWindow.html()

                # load the html into the document
                document.setHtml(html)

                # create the PDF file by printing to the "printer" (which is set to PDF)
                document.print_(printer)  

                if sys.platform == "win32":
                    os.startfile(filename[0])
                else:
                    opener ="open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, filename[0]])
                                
              
    def CreateSpeciesList(self): 
        # Create Filtered List button was clicked
        # create filtered species list child
        
        # if no data file is currently open, abort
        if MainWindow.db.eBirdFileOpenFlag is False:
            self.CreateMessageNoFile()   
            return
            
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))            
        
        # get the current filter settings in a list to pass to child
        filter = self.GetFilter()
        
        # create child window 
        sub = Lists()
        
        # save the MDI window as the parent for future use in the child
        sub.mdiParent = self
        
        # call the child's fill routine, passing the filter settings list
        if sub.FillSpecies(filter) is True:
            
            # add and position the child to our MDI area
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.show() 
        
        else:
            
            self.CreateMessageNoResults()
            sub.close()
        
        QApplication.restoreOverrideCursor() 
        
        
    def CreateLocationTotals(self):   

        # if no data file is currently open, abort        
        if MainWindow.db.eBirdFileOpenFlag is not True:
            self.CreateMessageNoFile()   
            return
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        filter = self.GetFilter()
        # create new Location Totals child window        
        sub = LocationTotals()

        # save the MDI window as the parent for future use in the child        
        sub.mdiParent = self        

        # call the child's routine to fill it with data        
        # procede if the child successfully filled with data
        if sub.FillLocationTotals(filter) is True:

            # add and position the child to our MDI area
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.show()
            
        else:

            # abort if filter found no sightings for child
            self.CreateMessageNoResults()
            sub.close()
        
        QApplication.restoreOverrideCursor() 


    def CreateAboutLapwing(self):   
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        sub = Web()

        # save the MDI window as the parent for future use in the child        
        sub.mdiParent = self        

        # call the child's routine to fill it with data        
        sub.loadAboutLapwing()
            
        # add and position the child to our MDI area
        self.mdiArea.addSubWindow(sub)
        self.PositionChildWindow(sub,  self)
        sub.show()
            
        QApplication.restoreOverrideCursor() 


    def CreateMap(self):   

        # if no data file is currently open, abort        
        if MainWindow.db.eBirdFileOpenFlag is not True:
            self.CreateMessageNoFile()   
            return
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        filter = self.GetFilter()
        # create new Location Totals child window        
        sub = Web()

        # save the MDI window as the parent for future use in the child        
        sub.mdiParent = self        

        # call the child's routine to fill it with data        
        if sub.LoadLocationsMap(filter) is True:
            
            # add and position the child to our MDI area
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.show()

        else:
            # abort if filter found no sightings for map
            self.CreateMessageNoResults()
            sub.close()
            
        QApplication.restoreOverrideCursor() 

        
    def CreateDateTotals(self):  

        # if no data file is currently open, abort        
        if MainWindow.db.eBirdFileOpenFlag is not True:
            self.CreateMessageNoFile()   
            return
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        # create new Date Totals child window        
        sub = DateTotals()

        # save the MDI window as the parent for future use in the child        
        sub.mdiParent = self 
        
        # call the child's routine to fill it with data
        if sub.FillDateTotals(self.GetFilter()) is True:

            # add and position the child to our MDI area
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.show()            
        
        else:
                    
            # abort since filter found no sightings for child
            self.CreateMessageNoResults()
            sub.close()

        QApplication.restoreOverrideCursor() 


    def CreateFamiliesReport(self):      

        # if no data file is currently open, abort        
        if MainWindow.db.eBirdFileOpenFlag is not True:
            self.CreateMessageNoFile()   
            return
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        # create Families Report child window
        sub = Families()
        
        # save the MDI window as the parent for future use in the child        
        sub.mdiParent = self
        
        # get filter 
        filter = self.GetFilter()
        
        # call the child's routine to fill it with data
        if sub.FillFamilies(filter) is True:

            # add and position the child to our MDI area        
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)        
            sub.show()
            
        else:
            
            # abort if no families matched the filter
            self.CreateMessageNoResults()
            sub.close()
        
        QApplication.restoreOverrideCursor()   
           
           
    def CreateCompareLists(self):    

        # if no data file is currently open, abort        
        if MainWindow.db.eBirdFileOpenFlag is not True:
            self.CreateMessageNoFile()   
            return
        
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        # create new Compare child window
        sub = Compare()
        
        # save the MDI window as the parent for future use in the child
        sub.mdiParent = self

        # call the child's routine to fill it with data
        if sub.FillListChoices() is True:

            # add and position the child to our MDI area        
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)        
            sub.show()

        else:
            
            QApplication.restoreOverrideCursor() 
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Fewer than two lists are available to compare. \n\nCreate two or more species lists before trying to compare them.")
            msg.setWindowTitle("No Species Lists")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()            
            sub.close()

        QApplication.restoreOverrideCursor()   


    def CreateLocationsList(self):      
        
        # if no data file is currently open, abort        
        if MainWindow.db.eBirdFileOpenFlag is not True:
            self.CreateMessageNoFile()   
            return

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        filter = self.GetFilter()
                
        # create a new list child window
        sub = Lists()
        
        # save the MDI window as the parent for future use in the child            
        sub.mdiParent = self

        # call the child's routine to fill it with data
        if sub.FillLocations(filter) is True:
        
            # add and position the child to our MDI area        
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)        
            sub.show()
        
        else:
            
            self.CreateMessageNoResults()
            sub.close
            
        QApplication.restoreOverrideCursor()   
        
        
    def GetFilter(self):
        startDate = ""
        endDate= ""
        startSeasonalMonth = ""
        startSeasonalDay = ""
        endSeasonalMonth = ""
        endSeasonalDay = ""
        locationType = ""
        locationName = "" 
        speciesName = ""
        family = ""
        order = ""
        
        # check whether calendar widgets are used
        if self.cboDateOptions.currentText() == "Use Calendars Below":
            
            # get yyyy-mm-dd start date string from widget
            startDate = (
                                   str(self.calStartDate.date().year()) 
                                + "-" 
                                + str(self.calStartDate.date().month()) 
                                + "-" 
                                + str(self.calStartDate.date().day()))
            
            # get yyyy-mm-dd end date string from widget
            endDate = (
                                   str(self.calEndDate.date().year()) 
                                + "-" 
                                + str(self.calEndDate.date().month()) 
                                + "-" 
                                + str(self.calEndDate.date().day())
                                )
                                
        # Check if Today radio button is checked.
        # If so, just create yyyy-mm-dd for today.
        if self.cboDateOptions.currentText() == "Today":

            now = datetime.datetime.now()

            startDate = (
                                      str(now.year) 
                                   + "-" 
                                   + str(now.month) 
                                   + "-" 
                                   + str(now.day)
                                   )
            
            # since this is a single day, startDate and endDate are the same
            endDate = startDate    
            
        if self.cboDateOptions.currentText() == "Yesterday":
            now = datetime.datetime.now()
           
           # subtract a day from today to get yesterday
            yesterday = now + datetime.timedelta(days=-1)
            
            # convert to yyyy-mm-dd string
            startDate = (
                                      str(yesterday.year) 
                                   + "-" 
                                   + str(yesterday.month) 
                                   + "-" 
                                   + str(yesterday.day)
                                   )
            
            # since this is a single day, startDate and endDate are the same
            endDate = startDate

        # Check if This Year radio button is checked.
        # if so, create yyyy-01-01 and yyyy-12-31 start and end dates
        if self.cboDateOptions.currentText() == "This Year":

            now = datetime.datetime.now()
            
            # set startDate to January 1 of this year
            startDate = str(now.year) + "-01-01"
            
            # set endDate to December 31 of this year
            endDate = str(now.year) + "-12-31"

        
        # Check if This Month radio button is checked
        # if so, create yyyy-mm-01 and yyyy-mm-31 dates
        # We'll need to get the correct number fo the last day of the month
        if self.cboDateOptions.currentText() == "This Month":
            
            now = datetime.datetime.now()

            # startDate should be first day of this month
            # convert to yyyy-mm-dd string
            startDate = (
                                      str(now.year) 
                                   + "-" 
                                   + str(now.month) 
                                   + "-" 
                                   + "01"
                                   )
            
            # lastDate is trickier. Need the last day of month, which varies numerically by month.
            # set day to 28 and then add 4 days. This guarantees finding a date in next month
            dayInNextMonth= now.replace(day=28) + datetime.timedelta(days=4)
            
             # Now set the date to 1 so we're at the first day of next month
            firstOfNextMonth = dayInNextMonth.replace(day=1)
            
            # Now subtract a day from the  first of next month, which back into the last day of this month
            lastDayOfThisMonth = firstOfNextMonth + datetime.timedelta(days = -1)
            # convert to yyyy-mm-dd string
            endDate = (
                                     str(lastDayOfThisMonth.year) 
                                  + "-" 
                                  + str(lastDayOfThisMonth.month) 
                                  + "-" 
                                  + str(lastDayOfThisMonth.day)
                                  )

        # add leading 0 to date digit strings if less than two digits
        # only take action if startDate has a value
        if not startDate == "":
           
            # get the date digit(s) from the yyyy-mm-d(d) string
            # they might be only 1 digit long, hence the need to pad
            startDateDigits = startDate.split("-")[2]
            endDateDigits = endDate.split("-")[2]
            
            if len(startDateDigits) < 2:
                
                # pad with 0, because date is only one digit
                startDateDigits = "0" + startDateDigits
            
            if len(endDateDigits) < 2:
                
                # pad with 0, because date is only one digit
                endDateDigits = "0" + endDateDigits
                
            # add leading 0 to month digit strings if less than two digits
           
            # get the month digit(s) from the yyyy-m(m)-dd string
            # they might be only 1 digit long, hence the need to pad
            startMonthDigits = startDate.split("-")[1]
            endMonthDigits = endDate.split("-")[1]
            
            if len(startMonthDigits) < 2:

                # pad with 0, because month is only one digit                
                startMonthDigits = "0" + startMonthDigits
            
            if len(endMonthDigits) < 2:
                
                # pad with 0, because month is only one digit                
                endMonthDigits = "0" + endMonthDigits 
                
            # reassemble padded Start and End Dates in yyyy-mm-dd string
            startDate = (
                                     startDate[0:4]   # year digits yyyy
                                     + "-" 
                                     + startMonthDigits 
                                     + "-" 
                                     + startDateDigits
                                    )
            
            endDate = (
                                     endDate[0:4]  # year digits yyyy
                                     + "-" 
                                     + endMonthDigits 
                                     + "-" 
                                     + endDateDigits
                                    )

        if self.cboSeasonalRangeOptions.currentText() == "Use Range Below":
           
            # read date month number from combobox, and add one to convert from
           # zero-based to one-based month 
            startSeasonalMonth = str(self.cboStartSeasonalRangeMonth.currentIndex()+1)
           
            # read startSeasonalDay from combobox
            startSeasonalDay = self.cboStartSeasonalRangeDate.currentText()
            
            # read date month number from combobox, and add one to convert from
            # zero-based to one-based month 
            endSeasonalMonth  = str(self.cboEndSeasonalRangeMonth.currentIndex()+1)
            
            # read endSeasonalDay from combobox
            endSeasonalDay  = self.cboEndSeasonalRangeDate.currentText()      
      
            # add leading 0 to seasonal month and date strings if less than two digits
            if len(startSeasonalMonth) < 2:
                startSeasonalMonth = "0" + startSeasonalMonth
            
            if len(startSeasonalDay) < 2:
                startSeasonalDay = "0" + startSeasonalDay    
            
            if len(endSeasonalMonth) < 2:
                endSeasonalMonth = "0" + endSeasonalMonth
            
            if len(endSeasonalDay) < 2:
                endSeasonalDay = "0" + endSeasonalDay                    

        if self.cboSeasonalRangeOptions.currentText() == "Spring":
            startSeasonalMonth = "03"
            startSeasonalDay = "21"
            endSeasonalMonth = "06"
            endSeasonalDay = "21"

        if self.cboSeasonalRangeOptions.currentText() == "Summer":
            startSeasonalMonth = "06"
            startSeasonalDay = "21"
            endSeasonalMonth = "09"
            endSeasonalDay = "21"

        if self.cboSeasonalRangeOptions.currentText() == "Fall":
            startSeasonalMonth = "09"
            startSeasonalDay = "21"
            endSeasonalMonth = "12"
            endSeasonalDay = "21"

        if self.cboSeasonalRangeOptions.currentText() == "Winter":
            startSeasonalMonth = "12"
            startSeasonalDay = "21"
            endSeasonalMonth = "03"
            endSeasonalDay = "21"         
         
        if self.cboSeasonalRangeOptions.currentText() == "This Month":
            now = datetime.datetime.now()
            startSeasonalMonth = str(now.month)
            if len(startSeasonalMonth) == 1:
                startSeasonalMonth = "0" + startSeasonalMonth
            endSeasonalMonth = startSeasonalMonth
            startSeasonalDay = "01"
            endSeasonalDay = MainWindow.db.GetLastDayOfMonth(startSeasonalMonth)

        if self.cboSeasonalRangeOptions.currentText() == "Year to Date":
            now = datetime.datetime.now()
            startSeasonalMonth = "01"
            startSeasonalDay = "01"
            endSeasonalMonth = str(now.month)
            endSeasonalDay = str(now.day)
            # add leading 0 to seasonal month and date strings if less than two digits
            if len(endSeasonalMonth) < 2:
                endSeasonalMonth = "0" + endSeasonalMonth
            
            if len(endSeasonalDay) < 2:
                endSeasonalDay = "0" + endSeasonalDay  

            
        # check location comboboxes to learn location type and name
        # Only get location information if user has selected one
        if self.cboCountries.currentText() != None:
            
            if self.cboCountries.currentText() != "**All Countries**":
                
                # for country name, get the short code,which the db uses for searches
                locationName = MainWindow.db.GetCountryCode(self.cboCountries.currentText())
                locationType = "Country"
       
        if self.cboStates.currentText() != None:
            
            if self.cboStates.currentText() != "**All States**":
                
                # for state name, get the short code, which the db uses for searches
                locationName = MainWindow.db.GetStateCode(self.cboStates.currentText())
                locationType = "State"
      
        if self.cboCounties.currentText() != None:
            
            if self.cboCounties.currentText() != "**All Counties**":
                
                locationName = self.cboCounties.currentText()
                locationType = "County"
        
        if self.cboLocations.currentText() != None:
            
            if self.cboLocations.currentText() != "**All Locations**":
                
                locationName = self.cboLocations.currentText()
                locationType = "Location"

        # check species combobox to learn species name
        if self.cboSpecies.currentText() != None:
            
            if self.cboSpecies.currentText() != "**All Species**":
                
                speciesName = self.cboSpecies.currentText()

        # check order combobox to learn family
        if self.cboOrders.currentText() != None:
            
            if self.cboOrders.currentText() != "**All Orders**":
                
                order = self.cboOrders.currentText()

        # check family combobox to learn family
        if self.cboFamilies.currentText() != None:
            
            if self.cboFamilies.currentText() != "**All Families**":
                
                family = self.cboFamilies.currentText()

        # package up the filter list and return it
        newFilter = Filter()
        newFilter.setLocationType(locationType)
        newFilter.setLocationName(locationName)
        newFilter.setStartDate(startDate)
        newFilter.setEndDate(endDate)
        newFilter.setStartSeasonalMonth(startSeasonalMonth)
        newFilter.setEndSeasonalMonth(endSeasonalMonth)
        newFilter.setStartSeasonalDay(startSeasonalDay)
        newFilter.setEndSeasonalDay(endSeasonalDay)
        newFilter.setSpeciesName(speciesName)
        newFilter.setFamily(family)
        newFilter.setOrder(order)
        
        return(newFilter)
                                      
        
    def SeasonalRangeClicked(self):
        self.cboSeasonalRangeOptions.setCurrentIndex(1)
        
    def TileWindows(self):
        self.mdiArea.tileSubWindows()
        
    def CascadeWindows(self):
        # scale every window to its default size
        # save those dimensions as minimum size 
        # if we don't, cascading the windows will shrink them
        # too too tiny
        for w in self.mdiArea.subWindowList():        
            w.scaleMe()
            w.setMinimumHeight(w.height())
            w.setMinimumWidth(w.width())
        
        self.mdiArea.cascadeSubWindows()
        
        # set the minimum sizes back to 0, 0
        for w in self.mdiArea.subWindowList():        
            w.setMinimumHeight(0)
            w.setMinimumWidth(0)        
        
    def CloseAllWindows(self):
        self.mdiArea.closeAllSubWindows()


    def HideMainWindowOptions(self):
        self.clearFilter()
        self.dckFilter.setVisible(False)
        

    def ShowMainWindowOptions(self):
        self.dckFilter.setVisible(True)


    def SetChildDetailsLabels(self,  sub,  filter):
        locationType = filter.getLocationType()                             # str   choices are Country, County, State, Location, or ""
        locationName = filter.getLocationName()                         # str   name of region or location  or ""
        startDate = filter.getStartDate()                                           # str   format yyyy-mm-dd  or ""
        endDate = filter.getEndDate()                                               # str   format yyyy-mm-dd  or ""
        startSeasonalMonth = filter.getStartSeasonalMonth() # str   format mm
        startSeasonalDay = filter.getStartSeasonalDay()            # str   format dd
        endSeasonalMonth  = filter.getEndSeasonalMonth()    # str   format  dd
        endSeasonalDay  = filter.getEndSeasonalDay()               # str   format dd
        checklistID = filter.getChecklistID()                                     # str   checklistID
        speciesName = filter.getSpeciesName()                           # str   speciesName
        family = filter.getFamily()                                                         # str family name
        order = filter.getOrder()                                                   #str order name
        
        # set main location label, using "All Locations" if none others are selected
        if locationName is "":   
            sub.lblLocation.setText("All Locations")
        else:
            if locationType == "Country":
                sub.lblLocation.setText(MainWindow.db.GetCountryName(locationName))
            elif locationType == "State":
                sub.lblLocation.setText(MainWindow.db.GetStateName(locationName))       
            else:
                sub.lblLocation.setText(locationName)
        
        if speciesName != "":
            sub.lblLocation.setText(speciesName +": " + sub.lblLocation.text())
            
        # set main date range label, using "AllDates" if none others are selected
        detailsText = ""
        dateText = ""
        
        if startDate == "":
            dateText = "; All Dates"
        else:
            dateTitle = startDate + " to " + endDate
            if startDate == endDate:
                dateTitle = startDate
            if checklistID != "":
                dateTitle = dateTitle + ": Checklist #" + checklistID
            dateText = "; " + dateTitle

        # set main seasonal range label, if specified
        if not ((startSeasonalMonth == "") or (endSeasonalMonth == "")):
            monthRange = ["Jan",  "Feb",  "Mar",  "Apr", "May",   "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec"]
            rangeTitle = monthRange[int(startSeasonalMonth)-1] + "-" + startSeasonalDay + " to " + monthRange[int(endSeasonalMonth)-1] + "-" + endSeasonalDay
            dateText = dateText + "; " + rangeTitle
       
        if checklistID != "":
            detailsText = "; Checklist " + checklistID

        if order != "":
            detailsText = detailsText + "; " + order
        
        if family != "":
            detailsText = detailsText + "; " + family
            
        #remove leading "; "
        dateText = dateText[2:]
        detailsText = detailsText[2:]
        
        sub.lblDateRange.setText(dateText)
        if dateText =="":
            sub.lblDateRange.setVisible(False)
        else:
            sub.lblDateRange.setVisible(True)
            
        sub.lblDetails.setText(detailsText)
        if detailsText =="":
            sub.lblDetails.setVisible(False)
        else:
            sub.lblDetails.setVisible(True)      
            
        sub.setWindowTitle(sub.lblLocation.text() + ": " + sub.lblDateRange.text())   
       
    
    def FillMainComboBoxes(self):
        
        # use the master lists in db to populate the 4 location comboboxes
        # for each, first add the "**All...**" item. 
        # It's starred to appear at the top of the sorted comboboxes
        self.cboCountries.clear()
        self.cboCountries.addItem("**All Countries**")
        self.cboCountries.addItems(MainWindow.db.countryList)        
        
        self.cboStates.clear()
        self.cboStates.addItem("**All States**")
        self.cboStates.addItems(MainWindow.db.stateList)        
        
        self.cboCounties.clear()
        self.cboCounties.addItem("**All Counties**")
        self.cboCounties.addItems(MainWindow.db.countyList)
        
        self.cboLocations.clear()
        self.cboLocations.addItem("**All Locations**")
        self.cboLocations.addItems(MainWindow.db.locationList)
        
        self.cboSpecies.clear()
        self.cboSpecies.addItem("**All Species**")
        self.cboSpecies.addItems(MainWindow.db.speciesDict.keys())  
        self.cboSpecies.model().sort(0)
        
        self.cboFamilies.clear()
        self.cboFamilies.addItem("**All Families**")
        self.cboFamilies.addItems(MainWindow.db.familyList)

        self.cboOrders.clear()
        self.cboOrders.addItem("**All Orders**")
        self.cboOrders.addItems(MainWindow.db.orderList)
        

    def printMe(self):

        activeWindow = self.mdiArea.activeSubWindow()            

        if activeWindow is None:
            return

        if activeWindow.objectName() in ([
            "frmSpeciesList", 
            "frmFamilies", 
            "frmCompare", 
            "frmDateTotals", 
            "frmLocationTotals", 
            "frmWeb", 
            "frmIndividual", 
            "frmLocation",
            "frmBigReport"
            ]):

            # create a QTextDocument in memory to hold and render our content
            document = QTextDocument()

            # create a QPrinter object for the printer the user later selects
            printer = QPrinter()
        
            # get html content from child window
            html = activeWindow.html()

            # load the html into the document
            document.setHtml(html)

            # let user select and configure a printer
            dialog = QPrintDialog(printer, self) 

            # execute the print if the user clicked "Print"
            if dialog.exec_():

                # send the html to the physical printer
                document.print_(printer)            


    def ResetMainWindow(self):
        
        self.CloseAllWindows()
        MainWindow.db.eBirdFileOpenFlag = False
        self.fillingLocationComboBoxesFlag = True
        self.cboCountries.clear()
        self.cboStates.clear()
        self.cboCounties.clear()
        self.cboLocations.clear()
        self.cboSpecies.clear()
        self.cboFamilies.clear()
        self.fillingLocationComboBoxesFlag = False        

        
    def ComboCountriesChanged(self):
        
        # Check whether the program is adding locations while reading the data file
        # if so, abort. If not, the user has clicked the combobox and we should proceed
        if self.fillingLocationComboBoxesFlag is False:  
                  
            # set the flag to True so the state, county, and location cbos won't trigger
            self.fillingLocationComboBoxesFlag = True    
            
            # clear the color coding for selected filter components
            self.cboCountries.setStyleSheet("");                
            self.cboStates.setStyleSheet("");                
            self.cboCounties.setStyleSheet("");                
            self.cboLocations.setStyleSheet("");                            
       
            # use the selected country to filter the masterLocationList
            # clear the subsidiary comboboxes and populat them anew with filtered locations
            thisCountry = MainWindow.db.GetCountryCode(self.cboCountries.currentText())
            self.cboStates.clear()
            self.cboCounties.clear()
            self.cboLocations.clear()
            
            # if "all countries" is chosen, fill subsidiary cbos with all locations
            # e.g., remove the country filter, if one had existed for the cbos
            if thisCountry == "**All Countries**":
                self.cboCountries.setStyleSheet("");                
                self.cboStates.addItem("**All States**")
                self.cboCounties.addItem("**All Counties**")
                self.cboLocations.addItem("**All Locations**")
                self.cboStates.addItems(MainWindow.db.stateList)
                self.cboCounties.addItems(MainWindow.db.countyList)
                self.cboLocations.addItems(MainWindow.db.locationList)
                self.cboCountries.setStyleSheet("");
            
            else:
                
                self.cboCountries.setStyleSheet("QComboBox { background-color: rgb(110, 115, 202)}");
                
                # initialize lists to store the subsidiary locations
                thisCountryStates = set()
                thisCountryCounties = set()
                thisCountryLocations = set()
                
                # loop through masterLocationList to find locations filtered for the chose country
                for l in MainWindow.db.masterLocationList:
                    
                    if l[0] == thisCountry:
                        
                        if l[1] != "": thisCountryStates.add(MainWindow.db.GetStateName(l[1]))
                        if l[2] != "": thisCountryCounties.add(l[2])
                        if l[3] != "": thisCountryLocations.add(l[3])
                
                # remove duplicates using the set command, then return to list format
                thisCountryStates = list(thisCountryStates)
                thisCountryCounties = list(thisCountryCounties)
                thisCountryLocations = list(thisCountryLocations)
                
                # sort them
                thisCountryStates.sort()
                thisCountryCounties.sort()
                thisCountryLocations.sort()
                
                # add filtered locations to comboboxes
                self.cboStates.addItem("**All States**")
                self.cboStates.addItems(thisCountryStates)
                self.cboCounties.addItem("**All Counties**")
                self.cboCounties.addItems(thisCountryCounties)
                self.cboLocations.addItem("**All Locations**")
                self.cboLocations.addItems(thisCountryLocations)
            
            # we're done, so reset flag to false to allow future triggers
            self.fillingLocationComboBoxesFlag = False


    def ComboDateOptionsChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            
            thisOption = self.cboDateOptions.currentText()
            
            if thisOption == "No Date Filter":
                self.cboDateOptions.setStyleSheet("");  
                self.calStartDate.setStyleSheet("")
                self.calEndDate.setStyleSheet("")

            elif thisOption == "Use Calendars Below":
                self.cboDateOptions.setStyleSheet("QComboBox { background-color: blue}");
                self.calStartDate.setStyleSheet("QDateTimeEdit { background-color: blue; color: white}")
                self.calEndDate.setStyleSheet("QDateTimeEdit { background-color: blue; color: white}")                
                
            else:
                self.cboDateOptions.setStyleSheet("QComboBox { background-color: blue}")
                self.calStartDate.setStyleSheet("");                
                self.calEndDate.setStyleSheet("")                


    def ComboFamiliesChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            
            self.fillingLocationComboBoxesFlag = True
            thisFamily = self.cboFamilies.currentText()
            
            # clear any color coding for selected filter components 
            self.cboSpecies.setStyleSheet("")
            self.cboSpecies.clear()
            
            if thisFamily == "**All Families**":
                self.cboFamilies.setStyleSheet("");                
                self.cboSpecies.addItem("**All Species**")
                if self.cboOrders.currentText() == "All Orders":
                    speciesList = MainWindow.db.speciesDict.keys()
                    speciesList = list(speciesList)
                else:
                    speciesList = MainWindow.db.orderSpeciesDict[self.cboOrders.currentText()]
                speciesList.sort()                
                self.cboSpecies.addItems(speciesList)
                
            else:
                self.cboFamilies.setStyleSheet("QComboBox { background-color: blue}");
                self.cboSpecies.addItem("**All Species**")
                self.cboSpecies.addItems(MainWindow.db.familySpeciesDict[thisFamily])                
            
            self.fillingLocationComboBoxesFlag = False


    def ComboLocationsChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            
            thisLocation = self.cboLocations.currentText()
            
            if thisLocation == "**All Locations**":
                self.cboLocations.setStyleSheet("");                
            else:
                self.cboLocations.setStyleSheet("QComboBox { background-color: blue}");
            
            self.cboStartSeasonalRangeMonth.adjustSize()


    def ComboOrdersChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            self.fillingLocationComboBoxesFlag = True
            thisOrder = self.cboOrders.currentText()
            
            # clear any color coding for selected filter components 
            self.cboFamilies.setStyleSheet("")   
            self.cboSpecies.setStyleSheet("")
            self.cboFamilies.clear()
            self.cboSpecies.clear()
            
            if thisOrder == "**All Orders**":
                self.cboOrders.setStyleSheet("");                
                self.cboFamilies.addItem("**All Families**")
                self.cboFamilies.addItems(MainWindow.db.familyList)
                self.cboSpecies.addItem("**All Species**")
                speciesList = MainWindow.db.speciesDict.keys()
                speciesList = list(speciesList)
                speciesList.sort()
                self.cboSpecies.addItems(speciesList)
                
            else:
                thisFamilies = []
                self.cboOrders.setStyleSheet("QComboBox { background-color: blue}");
                for l in MainWindow.db.masterFamilyOrderList:
                    if l[1] == thisOrder:
                        if l[0] not in thisFamilies:
                            thisFamilies.append(l[0])
                self.cboFamilies.addItem("**All Families**")
                self.cboFamilies.addItems(thisFamilies)
                self.cboSpecies.addItem("**All Species**")
                self.cboSpecies.addItems(MainWindow.db.orderSpeciesDict[thisOrder])                
            self.fillingLocationComboBoxesFlag = False
                
        
    def ComboSeasonalRangeOptionsChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            
            thisOption = self.cboSeasonalRangeOptions.currentText()
            
            if thisOption == "No Seasonal Range":
                self.cboSeasonalRangeOptions.setStyleSheet("");  
                self.cboStartSeasonalRangeMonth.setStyleSheet("")
                self.cboStartSeasonalRangeDate.setStyleSheet("")
                self.cboEndSeasonalRangeMonth.setStyleSheet("")
                self.cboEndSeasonalRangeDate.setStyleSheet("")
                
            elif thisOption == "Use Range Below":
                self.cboSeasonalRangeOptions.setStyleSheet("QComboBox { background-color: blue}");
                self.cboStartSeasonalRangeMonth.setStyleSheet("QComboBox { background-color: blue}")
                self.cboStartSeasonalRangeDate.setStyleSheet("QComboBox { background-color: blue}")
                self.cboEndSeasonalRangeMonth.setStyleSheet("QComboBox { background-color: blue}")
                self.cboEndSeasonalRangeDate.setStyleSheet("QComboBox { background-color: blue}")            
                
            else:
                self.cboSeasonalRangeOptions.setStyleSheet("QComboBox { background-color: blue}");
                self.cboStartSeasonalRangeMonth.setStyleSheet("")
                self.cboStartSeasonalRangeDate.setStyleSheet("")
                self.cboEndSeasonalRangeMonth.setStyleSheet("")
                self.cboEndSeasonalRangeDate.setStyleSheet("")   


    def ComboSpeciesChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            
            thisSpecies = self.cboSpecies.currentText()
            
            if thisSpecies == "**All Species**":
                self.cboSpecies.setStyleSheet("");                
            else:
                self.cboSpecies.setStyleSheet("QComboBox { background-color: blue}");

                     
    def ComboStatesChanged(self):
        if self.fillingLocationComboBoxesFlag is False:        
            self.fillingLocationComboBoxesFlag = True
            
            # clear any color coding for selected filter components
            self.cboCounties.setStyleSheet("");                
            self.cboLocations.setStyleSheet("");          
            
            thisState = MainWindow.db.GetStateCode(self.cboStates.currentText())
            self.cboCounties.clear()
            self.cboLocations.clear()
            if thisState == "**All States**":
                self.cboStates.setStyleSheet("");                                
                self.cboCounties.addItem("**All Counties**")
                self.cboLocations.addItem("**All Locations**")
                self.cboCounties.addItems(MainWindow.db.countyList)
                self.cboLocations.addItems(MainWindow.db.locationList)
            else:
                self.cboStates.setStyleSheet("QComboBox { background-color: blue}");                
                thisStateCounties = set()
                thisStateLocations = set()
                for l in MainWindow.db.masterLocationList:
                    if l[1] == thisState:
                        if l[2] != "": thisStateCounties.add(l[2])
                        if l[3] != "": thisStateLocations.add(l[3])
                
                thisStateCounties = list(thisStateCounties)
                thisStateLocations = list(thisStateLocations)
                
                thisStateCounties.sort()
                thisStateLocations.sort()
                
                self.cboCounties.addItem("**All Counties**")
                self.cboCounties.addItems(thisStateCounties)
                self.cboLocations.addItem("**All Locations**")
                self.cboLocations.addItems(thisStateLocations)  
            self.fillingLocationComboBoxesFlag = False
            
    def ComboCountiesChanged(self):
        if self.fillingLocationComboBoxesFlag is False:
            self.fillingLocationComboBoxesFlag = True
            thisCounty = self.cboCounties.currentText()
            
            # clear any color coding for selected filter components 
            self.cboLocations.setStyleSheet("");          
            
            self.cboLocations.clear()
            if thisCounty == "**All Counties**":
                self.cboCounties.setStyleSheet("");                
                self.cboLocations.addItem("**All Locations**")
                self.cboLocations.addItems(MainWindow.db.locationList)
            else:
                self.cboCounties.setStyleSheet("QComboBox { background-color: blue}");
                thisCountyLocations = set()
                for l in MainWindow.db.masterLocationList:
                    if l[2] == thisCounty:
                        if l[3] != "": thisCountyLocations.add(l[3])
                thisCountyLocations = list(thisCountyLocations)
                thisCountyLocations.sort()
                self.cboLocations.addItem("**All Locations**")
                self.cboLocations.addItems(thisCountyLocations)
            self.fillingLocationComboBoxesFlag = False
            
    def ExitApp(self):
        sys.exit()
                                       

class BigReport(QMdiSubWindow, BigReport.Ui_frmBigReport):

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
        self.filter = Filter()
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
        sub = Location()
        sub.FillLocation(locationName)
        sub.mdiParent = self.mdiParent
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
        sub = Individual()
        sub.FillIndividual(species)
        sub.mdiParent = self.mdiParent
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        sub.resizeMe()
        QApplication.restoreOverrideCursor()     
    
    def CreateSpeciesList(self,  callingWidget):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        if callingWidget.objectName() == "lstDates":
            date = callingWidget.currentItem().text()
        
        filter = Filter()
        filter.setStartDate(date)
        filter.setEndDate(date)
        
        sub = Lists()
        sub.FillSpecies(filter)
        sub.mdiParent = self.mdiParent
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        QApplication.restoreOverrideCursor()          
        
    def FillAnalysisReport(self, filter):
        # save filter for later use
        self.filter = filter
        
        # create subset of master sightings list for this filter
        self.filteredSightingList = deepcopy(MainWindow.db.GetSightings(filter))
        filteredSightingList = self.filteredSightingList
        
        # ****Setup Species page****
        # get species and first/last date data from db 
        speciesListWithDates = MainWindow.db.GetSpeciesWithData(filter,  self.filteredSightingList,  "Subspecies")
       
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
        listDates = MainWindow.db.GetDates(filter,  filteredSightingList)
        self.lstDates.addItems(listDates)
        self.lstDates.setSpacing(2)
        if len(listDates) > 0:
            self.lstDates.setCurrentRow(0)
            self.FillSpeciesForDate()

        # ****Setup Locations page****
        listLocations = MainWindow.db.GetLocations(filter, "OnlyLocations",   filteredSightingList)
        for l in listLocations:
            self.lstLocations.addItem(l)
        self.lstLocations.setSpacing(2)
        if len(listLocations) > 0:
            self.lstLocations.setCurrentRow(0)
            self.FillSpeciesForLocation()
            self.lblLocations.setText("Locations (" + str(len(listLocations)) + ")")

        # ****Setup New Species for Dates page****
        speciesListFilter = Filter()
        speciesListFilter.setSpeciesList(self.speciesList)
        sightingListForSpeciesSubset = MainWindow.db.GetSightings(speciesListFilter)
        
        yearSpecies = MainWindow.db.GetNewYearSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset)
        lifeSpecies=  MainWindow.db.GetNewLifeSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset)
        monthSpecies = MainWindow.db.GetNewMonthSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset)
        
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
        countrySpecies = MainWindow.db.GetNewCountrySpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        stateSpecies = MainWindow.db.GetNewStateSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        countySpecies = MainWindow.db.GetNewCountySpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        locationSpecies = MainWindow.db.GetNewLocationSpecies(filter,  filteredSightingList,  sightingListForSpeciesSubset,  self.speciesList)
        
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
                countryItem.setText(MainWindow.db.GetCountryName(ms[0]))
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
                stateItem.setText(MainWindow.db.GetStateName(ms[0]))
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
        count = MainWindow.db.CountSpecies(self.speciesList)
        
        self.lblTopSpeciesSeen.setText("Species seen: " + str(count))
        
        # set main location label, using "All Locations" if none others are selected
        MainWindow.SetChildDetailsLabels(self,  self,  filter)

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
        
        tempFilter = Filter()
        
        tempFilter.setStartDate(date)
        tempFilter.setEndDate(date)
        
        speciesList = MainWindow.db.GetSpecies(tempFilter,  self.filteredSightingList)
        
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
            coordinates = MainWindow.db.GetLocationCoordinates(locationName)
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
        
        tempFilter = Filter()
        tempFilter.setLocationType("Location")
        tempFilter.setLocationName(location)

        speciesList = MainWindow.db.GetSpecies(tempFilter,  self.filteredSightingList)
        
        self.lstLocationSpecies.clear()
        self.lstLocationSpecies.addItems(speciesList)
        self.lstLocationSpecies.setSpacing(2)
        
        uniqueSpecies = MainWindow.db.GetUniqueSpeciesForLocation(
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
            sub = Individual()
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
            
            sub = Lists()
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
            
            species = MainWindow.db.GetSpecies(filter)

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
                        
            species = MainWindow.db.GetSpecies(filter)

            uniqueSpecies = MainWindow.db.GetUniqueSpeciesForLocation(
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
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  1100  * scaleFactor
        windowHeight = 625 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
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


class Lists(QMdiSubWindow, Lists.Ui_frmSpeciesList):
    
    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()
    
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""
        self.tblList.doubleClicked.connect(self.tblListClicked)
        self.btnShowLocation.clicked.connect(self.CreateLocation)
        self.txtFind.textChanged.connect(self.ChangedFindText)
        self.resized.connect(self.resizeMe)        
        self.currentSpeciesList = []
        self.btnShowLocation.setVisible(False)
        self.lblDetails.setVisible(False)
        self.filter = ()
        self.listType = ""
        
        self.actionSetDateFilter.triggered.connect(self.setDateFilter)
        self.actionSetFirstDateFilter.triggered.connect(self.setFirstDateFilter)
        self.actionSetLastDateFilter.triggered.connect(self.setLastDateFilter)
        self.actionSetSpeciesFilter.triggered.connect(self.setSpeciesFilter)
        self.actionSetCountryFilter.triggered.connect(self.setCountryFilter)
        self.actionSetStateFilter.triggered.connect(self.setStateFilter)
        self.actionSetCountyFilter.triggered.connect(self.setCountyFilter)
        self.actionSetLocationFilter.triggered.connect(self.setLocationFilter)


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
            
    def resizeMe(self):

        windowWidth = self.width()-10
        windowHeight = self.height()     
        self.scrollArea.setGeometry(5, 27, windowWidth-5, windowHeight-35)
        self.layLists.setGeometry(0, 0, windowWidth-5, windowHeight-40)
        self.txtChecklistComments.setMaximumHeight(floor(.15 * windowHeight))  
    
   
    def setCountyFilter(self):
        if self.listType in ["Checklists"]:
            if self.listType == "Checklists":
                countyName= self.tblList.item(self.tblList.currentRow(), 2).text()
            self.mdiParent.setCountyFilter(countyName)
   
   
    def setCountryFilter(self):
        if self.listType in ["Checklists"]:
            if self.listType == "Checklists":
                countryName= self.tblList.item(self.tblList.currentRow(), 0).text()
                self.mdiParent.setCountryFilter(countryName)


    def setDateFilter(self):        
        if self.listType in ["Checklists", "Single Checklist"]:
            if self.listType == "Checklists":
                date = self.tblList.item(self.tblList.currentRow(), 4).text()
            if self.listType == "Single Checklist":
                date = self.filter.getStartDate()
            self.mdiParent.setDateFilter(date)
   
   
    def setFirstDateFilter(self):
        if self.listType in ["Species", "Locations"]:
            if self.listType == "Species":
                date = self.tblList.item(self.tblList.currentRow(), 2).text()
            if self.listType == "Locations":
                date = self.tblList.item(self.tblList.currentRow(), 1).text()                
            self.mdiParent.setDateFilter(date)


    def setLastDateFilter(self):
        
        if self.listType in ["Species", "Locations"]:
            if self.listType == "Species":
                date = self.tblList.item(self.tblList.currentRow(), 3).text()
            if self.listType == "Locations":
                date = self.tblList.item(self.tblList.currentRow(), 2).text()    
            self.mdiParent.setDateFilter(date)


    def setLocationFilter(self):
        if self.listType in ["Locations", "Single Checklist", "Checklists"]:
            if self.listType == "Locations":
                locationName= self.tblList.item(self.tblList.currentRow(), 0).text()
            if self.listType == "Single Checklist":
                locationName= self.lblLocation.text()
            if self.listType == "Checklists":
                locationName= self.tblList.item(self.tblList.currentRow(), 3).text()
            self.mdiParent.setLocationFilter(locationName)
                 
   
    def setSpeciesFilter(self):
        if self.listType in ["Species", "Single Checklist"]:
            speciesName = self.tblList.item(self.tblList.currentRow(), 1).text()
            self.mdiParent.setSpeciesFilter(speciesName)
            
   
    def setStateFilter(self):
        if self.listType in ["Checklists"]:
            if self.listType == "Checklists":
                stateName= self.tblList.item(self.tblList.currentRow(), 1).text()
            self.mdiParent.setStateFilter(stateName)
            
   
    def scaleMe(self):
       
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
        #scale the font for all widgets in window
        for w in self.children():
            try:
                w.setFont(QFont("Helvetica", fontSize))
            except:
                pass
          
        # scale the find text box and show location button
        metrics = self.btnShowLocation.fontMetrics()
        buttonWidth = metrics.boundingRect(self.btnShowLocation.text()).width() * 1.25
        buttonHeight = metrics.boundingRect(self.btnShowLocation.text()).height() * 1.25
        self.btnShowLocation.setMinimumWidth(buttonWidth)
        self.btnShowLocation.setMaximumWidth(buttonWidth)
        self.btnShowLocation.setMinimumHeight(buttonHeight)
        self.btnShowLocation.setMaximumHeight(buttonHeight)
        self.txtFind.setMinimumWidth(buttonWidth)
        self.txtFind.setMaximumWidth(buttonWidth)
        self.txtFind.setMinimumHeight(buttonHeight)
        self.txtFind.setMaximumHeight(buttonHeight)        
        
        # scale the main window table   
        header = self.tblList.horizontalHeader()
        metrics = self.tblList.fontMetrics()

        if self.listType == "Species":
            dateTextWidth = metrics.boundingRect("2222-22-22").width()
            dateTextHeight = metrics.boundingRect("2222-22-22").height()
            taxTextWidth = metrics.boundingRect("Tax").width()
            header.resizeSection(0,  floor(1.75 * taxTextWidth))
            header.resizeSection(2,  floor(1.3 * dateTextWidth))
            header.resizeSection(3,  floor(1.3 * dateTextWidth))                
            header.resizeSection(4,  floor(1.3 * dateTextWidth))                
            header.resizeSection(5,  floor(1.7 * dateTextWidth))                
            for R in range(self.tblList.rowCount()):
                self.tblList.setRowHeight(R, dateTextHeight * 1.1)
        
        if self.listType == "Single Checklist":
            taxTextWidth = metrics.boundingRect("Tax").width()
            header.resizeSection(0,  floor(1.75 * taxTextWidth))
            countWidth = metrics.boundingRect("Count").width()
            header.resizeSection(2,  floor(1.6 * countWidth))
            commentWidth = metrics.boundingRect("Suitble comments column").width()
            header.resizeSection(3,  floor(1.15 * commentWidth))
            # only limit row height if there aren't comments. If there are comments, we want word wrap
            # to have unlimited height
            thisRowHeight= metrics.boundingRect("222").height()
            for R in range(self.tblList.rowCount()):
                if self.tblList.item(R,3).data(Qt.DisplayRole) == "":
                    self.tblList.setRowHeight(R, thisRowHeight * 1.1) 
            self.tblList.resizeRowsToContents()
        
        if self.listType == "Locations":
            dateTextWidth = metrics.boundingRect("2222-22-22 22:22").width()
            dateTextHeight = metrics.boundingRect("2222-22-22 22:22").height()            
            header.resizeSection(1,  floor(1.25 * dateTextWidth))
            header.resizeSection(2,  floor(1.25 * dateTextWidth))                
            for R in range(self.tblList.rowCount()):
                self.tblList.setRowHeight(R, dateTextHeight * 1.1)        

        if self.listType == "Checklists":

            thisColumnWidth = metrics.boundingRect("Some Country").width()
            header.resizeSection(0,  floor(1.15 * thisColumnWidth))                

            thisColumnWidth = metrics.boundingRect("Some State").width()
            header.resizeSection(1,  floor(1.15 * thisColumnWidth))                
            header.resizeSection(2,  floor(1.15 * thisColumnWidth))                
            
            # Don't set Location width. It stretches to fill remaining vacant width

            dateTextWidth = metrics.boundingRect("2222-22-22 22:22").width()
            header.resizeSection(4,  floor(1.1 * dateTextWidth))

            timeTextWidth = metrics.boundingRect("22:22").width()
            header.resizeSection(5,  floor(1.45 * timeTextWidth))
            
            speciesColumnWidth = metrics.boundingRect("Species").width()
            header.resizeSection(6,  floor(1.45 * speciesColumnWidth))                
            
            textHeight= metrics.boundingRect("2222").height()
            for R in range(self.tblList.rowCount()):
                self.tblList.setRowHeight(R, textHeight * 1.1)  
        
        if self.listType == "Find Results":

            # I chose to measure the size of "United States" becuase it's long, not for nationalistic reasons. 
            thisColumnWidth = metrics.boundingRect("Checklist Comments").width()
            header.resizeSection(0,  floor(1.15 * thisColumnWidth))                

            thisColumnWidth = metrics.boundingRect("Some Location's Long Name").width()
            header.resizeSection(1,  floor(1.15 * thisColumnWidth))               

            dateTextWidth = metrics.boundingRect("2222-22-22").width()
            header.resizeSection(2,  floor(1.25 * dateTextWidth))

            # Don't set Comments width. It stretches to fill remaining vacant width

            textHeight= metrics.boundingRect("2222").height()
            for R in range(self.tblList.rowCount()):
                self.tblList.setRowHeight(R, textHeight * 1.1)        
        
        self.lblLocation.setFont(QFont("Helvetica", floor(fontSize * 1.4 )))
        self.lblLocation.setStyleSheet("QLabel { font: bold }");
        self.lblDateRange.setFont(QFont("Helvetica", floor(fontSize * 1.2 )))
        self.lblDateRange.setStyleSheet("QLabel { font: bold }");
        self.lblDetails.setFont(QFont("Helvetica", floor(fontSize * 1.2 )))
        self.lblDetails.setStyleSheet("QLabel { font: bold }");
        self.lblSpecies.setFont(QFont("Helvetica", fontSize))
        self.lblFind.setFont(QFont("Helvetica", fontSize))
        self.btnShowLocation.setFont(QFont("Helvetica", fontSize))
        self.btnShowLocation.setStyleSheet("QLabel { font: bold }");
         
        windowWidth =  800  * scaleFactor
        windowHeight = 580 * scaleFactor  
        self.resize(windowWidth, windowHeight)
           
        
    def ChangedFindText(self):
        searchString = self.txtFind.text().lower()
        rowCount = self.tblList.rowCount()
        columnCount = self.tblList.columnCount()
        
        for r in range(rowCount):
            wholeRowText = ""
            
            for c in range(columnCount):

                wholeRowText = wholeRowText + self.tblList.item(r,  c).text().lower() + " "
            
            if searchString in wholeRowText:
                self.tblList.setRowHidden(r,  False)
            
            else:
                self.tblList.setRowHidden(r,  True)


    def CreateLocation(self):
        location = self.lblLocation.text()
        sub = Location()
        sub.mdiParent = self.mdiParent
        sub.FillLocation(location)  
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()        


    def html(self):
    
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
                padding: 1px;
            }
            th {
                text-align: left;
            }
            </style>
            <body>
            """
            
        html = html + (
            "<H1>" + 
            self.lblLocation.text() + 
            "</H1>"
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
            self.lblSpecies.text() + 
            "</H3>"
            )        
        
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
            
        # add table content depending on type of list we're displaying
        
        if self.listType == "Species":
            html=html + (    
                "<th>Species</th>" +
                "<th>First</th> " +
                "<th>       </th> " +
                "<th>Latest</th>" +
                "<th>Checklists</th>" +
                "</tr>"
                )
                
            for r in range(self.tblList.rowCount()):
                html = html + (
                "<tr>" +
                "<td>" +
                self.tblList.item(r, 1).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 2).text() +
                "</td>" +
                "<td>" +
                "  " +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 3).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 4).text() +
                "</td>" +
                "</tr>"
                )
            html = html + "</table>"

        if self.listType == "Locations":
            html=html + (    
                "<th>Location</th>" +
                "<th>First</th> " +
                "<th>Latest</th>" +
                "</tr>"
                )
                
            for r in range(self.tblList.rowCount()):
                html = html + (
                "<tr>" +
                "<td>" +
                self.tblList.item(r, 0).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 1).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 2).text() +
                "</td>" +
                "</tr>"
                )
            html = html + "</table>"

        if self.listType == "Single Checklist":
            html=html + (    
                "<th>Taxa</th>" +
                "<th>Count</th> " +
                "<th>Comments</th>" +
                "</tr>"
                )
                
            for r in range(self.tblList.rowCount()):
                html = html + (
                "<tr>" +
                "<td>" +
                self.tblList.item(r, 1).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 2).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 3).text() +
                "</td>" +
                "</tr>"
                )
            html = html + (
                "</table>" +
                "<h2>" +
                self.txtChecklistComments.toPlainText() +
                "</h2>"
            )

        if self.listType == "Checklists":
            html=html + (    
                "<th>Country</th>" +
                "<th>State</th> " +
                "<th>County</th>" +
                "<th>Location</th>" +
                "<th>Date</th>" +
                "<th>Time</th>" +
                "<th>Species</th>" +
                "</tr>"
                )
                
            for r in range(self.tblList.rowCount()):
                html = html + (
                "<tr>" +
                "<td>" +
                self.tblList.item(r, 0).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 1).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 2).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 3).text() +
                "</td>" +
                "<td>" +            
                self.tblList.item(r, 4).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 5).text() +
                "</td>" +
                "<td>" +
                self.tblList.item(r, 6).text() +
                "</td>" +
                "</tr>"
                )
            html = html + "</table>"                

        html = html + (
            "<font size>" +            
            "</body>" +
            "</html>"
            )
            
        return(html)
        

    def FillSpecies(self, filter): 
        
        self.filter = filter
        self.listType = "Species"
        checklistDetails = ""

        # set up a bold font to use in columns as needed
        font = QFont()
        font.setBold(True)        
       
        if filter.getLocationType() == "Location":
           self.btnShowLocation.setVisible(True)
                  
       # set up tblList column headers and widths
        self.tblList.setShowGrid(False)        
        header = self.tblList.horizontalHeader()
        header.setVisible(True)   
        
        # if this is a species list (not a single checklist), get data and set 4 columns
        if filter.getChecklistID() == "":
                        
            thisWindowList = MainWindow.db.GetSpeciesWithData(filter,  [], "Subspecies")
            thisCleanedWindowList = []
            
            # clean out spuh and slash entries
            for s in range(len(thisWindowList)):
                if not("sp." in thisWindowList[s][0] or "/" in thisWindowList[s][0]):
                    thisCleanedWindowList.append(thisWindowList[s])
            thisWindowList = thisCleanedWindowList
                    
            if len(thisWindowList) == 0:
                return(False)                    
                    
            self.tblList.setRowCount(len(thisWindowList))
            self.tblList.setColumnCount(6)
            self.tblList.setHorizontalHeaderLabels(['Tax', 'Species', 'First',  'Last', 'Checklists', '% of Checklists'])
            header.setSectionResizeMode(1, QHeaderView.Stretch)   
            self.tblList.setItemDelegateForColumn(5, FloatDelegate(2))

            # add species and dates to table row by row        
            R = 0
            for species in thisWindowList:   
                taxItem = QTableWidgetItem()
                taxItem.setData(Qt.DisplayRole, R+1)
                speciesItem = QTableWidgetItem()
                speciesItem.setText(species[0])
                speciesItem.setData(Qt.UserRole,  QVariant(species[4]))                
                firstItem = QTableWidgetItem()
                firstItem.setData(Qt.DisplayRole, species[1])
                lastItem = QTableWidgetItem()
                lastItem.setData(Qt.DisplayRole, species[2])
                self.tblList.setItem(R, 0, taxItem)    
                checklistCountItem = QTableWidgetItem()
                checklistCountItem.setData(Qt.DisplayRole, species[5])
                checklistCountItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
                
                percentageItem = QTableWidgetItem()
                percentageItem.setData(Qt.DisplayRole, species[6])
                
                self.tblList.setItem(R, 1, speciesItem)
                self.tblList.item(R, 1).setFont(font)
                self.tblList.item(R, 1).setForeground(Qt.blue)

                self.tblList.setItem(R, 2, firstItem)
                self.tblList.setItem(R, 3, lastItem)
                self.tblList.setItem(R, 4, checklistCountItem)
                self.tblList.setItem(R, 5, percentageItem)
                self.currentSpeciesList.append(species[0])
                R = R + 1    
                
            # hide the checklist comments box, since  we're not showing a single checklist
            self.txtChecklistComments.setVisible(False)
                            
            self.tblList.addAction(self.actionSetFirstDateFilter)
            self.tblList.addAction(self.actionSetLastDateFilter)
            self.tblList.addAction(self.actionSetSpeciesFilter)
                
        # if this is limited to a checklist, set 3 columns
        else:
            
            self.listType = "Single Checklist"

            thisWindowList = MainWindow.db.GetSightings(filter)  
            self.tblList.setRowCount(len(thisWindowList))            
            self.tblList.setColumnCount(4)
            self.tblList.setHorizontalHeaderLabels(['Tax', 'Species', 'Count',  "Comment"])    
            header.setSectionResizeMode(1, QHeaderView.Stretch)        
            self.tblList.setWordWrap(True)
            
            # add species and dates to table row by row        
            R = 0
            for s in thisWindowList:    
                
                taxItem = QTableWidgetItem()
                taxItem.setData(Qt.DisplayRole, R+1)
                
                speciesItem = QTableWidgetItem()
                speciesItem.setText(s[23])
                speciesItem.setData(Qt.UserRole,  QVariant(s[1]))
                
                countItem = QTableWidgetItem()
                count = s[4]
                if count != "X":
                    count = int(count)
                countItem.setData(Qt.DisplayRole, count)
                countItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)

                commentItem = QTableWidgetItem()
                commentItem.setText(s[19])                
                
                self.tblList.setItem(R, 0, taxItem)    
                self.tblList.setItem(R, 1, speciesItem)
                self.tblList.item(R, 1).setFont(font)
                self.tblList.item(R, 1).setForeground(Qt.blue)  
                self.tblList.setItem(R, 2, countItem)
                self.tblList.setItem(R,  3,  commentItem)
        
                self.currentSpeciesList.append(s[1])
                
                R = R + 1     
            
            # resize all rows as necessary to show full comments
            # without this call, Qt sometimes truncates the comments
             
            # shorten  the height of tblList to create room for checklist comments box
            self.txtChecklistComments.setVisible(True)
            
            # fill checklist comments text
            checklistComments = thisWindowList[0][20]
            if checklistComments == "":
                checklistComments = "No checklist comments."
            self.txtChecklistComments.appendPlainText(checklistComments)
            
            #fill checklist details of time, distance, and checklist protoccol
            time = thisWindowList[0][11]        
            protocol = thisWindowList[0][12]
            duration = thisWindowList[0][13]
            distance = thisWindowList[0][15]
            observerCount = thisWindowList[0][17]
            
            if time != "":
                time = time + ",  "
                
            if duration != "0":
                duration = duration + " min,  "
            else:
                duration = ""
                
            if distance != "":
                distance = distance + " km,  "
                
            if observerCount != "":
                observerCount = observerCount + " obs,  "
            
            if "Traveling" in protocol:
                protocol ="Traveling"
            if "Stationary" in protocol:
                protocol ="Stationary"
            if "Casual" in protocol:
                protocol ="Casual"
                
            checklistDetails = (
                time + 
                duration +
                distance +
                observerCount  +
                protocol
                )
                
            self.tblList.addAction(self.actionSetDateFilter)
            self.tblList.addAction(self.actionSetSpeciesFilter)
            self.tblList.addAction(self.actionSetLocationFilter)
                            
        speciesCount = MainWindow.db.CountSpecies(self.currentSpeciesList)
        
        self.lblSpecies.setText("Species: " + str(speciesCount))
        
        if speciesCount != self.tblList.rowCount():
            self.lblSpecies.setText(
                "Species: " + 
                str(speciesCount) + 
                " plus " + 
                str(self.tblList.rowCount() - speciesCount) + 
                " other taxa"
                )

        MainWindow.SetChildDetailsLabels(self,  self,  filter)
        
        if checklistDetails != "":
            self.lblDetails.setText(checklistDetails)        

        location = filter.getLocationName()
        if location != "":
            if filter.getLocationType() == "Country":
                location = MainWindow.db.GetCountryName(location)
            if filter.getLocationType() == "State":
                location = MainWindow.db.GetStateName(location)                
            location = location + ": "
            
        dateRange= self.lblDateRange.text()
        
        family = filter.getFamily()
        if family != "":
            family = family.split(" (")[0]
            family = " (" + family + ")"        

        order = filter.getOrder()
        if order != "":
            order = order + ":"
            
        windowTitle = location + dateRange + order + family
        self.setWindowTitle(windowTitle)
        
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_bird.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)      
        
        self.scaleMe()
        self.resizeMe()
        
        # tell MainWindow that we succeeded filling the list
        return(True)


    def FillChecklists(self, filter): 

        self.filter = filter
        self.listType = "Checklists"
        
        # get species data from db 
        checklists = MainWindow.db.GetChecklists(filter)
        
        # abort if no checklists matched filter
        if len(checklists) == 0:
            return(False)
       
       # set up tblList column headers and widths
        self.tblList.setColumnCount(7)
        self.tblList.setRowCount(len(checklists))
        self.tblList.horizontalHeader().setVisible(True)
        self.tblList.setHorizontalHeaderLabels(['Country', 'State', 'County',  'Location', 'Date', 'Time',  'Species'])
        header = self.tblList.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.Stretch)        
        self.tblList.setShowGrid(False)

        # add species and dates to table row by row        
        R = 0
        for c in checklists:    
            countryItem = QTableWidgetItem()
            countryItem.setData(Qt.UserRole, QVariant(c[0]))  #store checklistID for future retreaval                     
            countryName = MainWindow.db.GetCountryName(c[1][0:2])
            countryItem.setText(countryName)            
            
            stateItem = QTableWidgetItem()
            stateName = MainWindow.db.GetStateName(c[1])
            stateItem.setText(stateName)
            
            countyItem = QTableWidgetItem()
            countyItem.setText(c[2])
            
            locationItem = QTableWidgetItem()
            locationItem.setText(c[3])
            
            dateItem = QTableWidgetItem()
            dateItem.setText(c[4])

            timeItem = QTableWidgetItem()
            timeItem.setText(c[5])
            
            speciesCountItem = QTableWidgetItem()
            speciesCountItem.setData(Qt.DisplayRole, c[6])  
            speciesCountItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
            
            self.tblList.setItem(R, 0, countryItem)    
            self.tblList.setItem(R, 1, stateItem)
            self.tblList.setItem(R, 2, countyItem)
            self.tblList.setItem(R, 3, locationItem)
            self.tblList.setItem(R, 4, dateItem)
            self.tblList.setItem(R, 5, timeItem)
            self.tblList.setItem(R, 6, speciesCountItem)
            R = R + 1
        
        self.lblSpecies.setText("Checklists: " + str(self.tblList.rowCount()))

        MainWindow.SetChildDetailsLabels(self,  self,  filter)

        self.setWindowTitle(self.lblLocation.text() + ": " + self.lblDateRange.text())
        
        self.txtChecklistComments.setVisible(False)

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_checklists.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)  
        
        self.tblList.addAction(self.actionSetDateFilter)
        self.tblList.addAction(self.actionSetCountryFilter)
        self.tblList.addAction(self.actionSetStateFilter)
        self.tblList.addAction(self.actionSetCountyFilter)
        self.tblList.addAction(self.actionSetLocationFilter)

        self.scaleMe()
        self.resizeMe()
        
        # alert MainWindow that we finished fill data successfully
        return(True)


    def FillFindChecklists(self,  foundList):
        
        self.filter = filter
        self.listType = "Find Results"        
                      
       # set up tblList column headers and widths
        self.tblList.setColumnCount(4)
        self.tblList.setRowCount(len(foundList))
        self.tblList.horizontalHeader().setVisible(True)
        self.tblList.setHorizontalHeaderLabels(['Type', 'Location', 'Date', 'Found'])
        header = self.tblList.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.Stretch)        

        self.tblList.setShowGrid(False)
        self.tblList.setWordWrap(True)

        # add checklists and fount term to table row by row        
        R = 0
        for c in foundList:  
            typeItem = QTableWidgetItem()
            typeItem.setData(Qt.UserRole, QVariant(c[1]))  #store checklistID for future retreaval                     
            typeItem.setText(c[0])
            
            locationItem = QTableWidgetItem()
            locationItem.setText(c[2])
            
            dateItem = QTableWidgetItem()
            dateItem.setText(c[3])

            foundTextItem = QTableWidgetItem()
            foundTextItem.setText(c[4])

            self.tblList.setItem(R, 0, typeItem)                
            self.tblList.setItem(R, 1, locationItem)
            self.tblList.setItem(R, 2, dateItem)
            self.tblList.setItem(R, 3, foundTextItem)
            R = R + 1
        
        self.setWindowTitle("Find Results")        
        self.lblLocation.setVisible(False)
        self.lblDateRange.setVisible(False)
        
        if self.lblDetails.text() != "":
            self.lblDetails.setVisible(True)
        else:
            self.lblDetails.setVisible(False)
            
        self.lblSpecies.setText("Checklists: " + str(self.tblList.rowCount()))
        self.txtChecklistComments.setVisible(False)
        
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_find.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)          

        self.scaleMe()
        self.resizeMe()


    def FillLocations(self, filter): 
        
        self.filter = filter
        self.listType = "Locations"
       
        self.btnShowLocation.setVisible(False)
        self.lblDetails.setVisible(False)
                  
       # set up tblList column headers and widths
        self.tblList.setShowGrid(False)        
        header = self.tblList.horizontalHeader()
        header.setVisible(True)   
        
        thisWindowList = MainWindow.db.GetLocations(filter,  "Dates")
        
        if len(thisWindowList) == 0:
            return(False)

        # set 3 columns and header titles
        self.tblList.setRowCount(len(thisWindowList))
        self.tblList.setColumnCount(3)
        self.tblList.setHorizontalHeaderLabels(['Location', 'First',  'Last'])
        header.setSectionResizeMode(0, QHeaderView.Stretch)        

        # add locations and dates to table row by row        
        R = 0
        for loc in thisWindowList:    
            locationItem = QTableWidgetItem()
            locationItem.setText(loc[0])
            firstItem = QTableWidgetItem()
            firstItem.setData(Qt.DisplayRole, loc[1])
            lastItem = QTableWidgetItem()
            lastItem.setData(Qt.DisplayRole, loc[2])
            self.tblList.setItem(R, 0, locationItem)
            self.tblList.setItem(R, 1, firstItem)
            self.tblList.setItem(R, 2, lastItem)
            R = R + 1    
            
            # hide the checklist comments box, since  we're not showing a single checklist
            self.txtChecklistComments.setVisible(False)
            
            # hide the checklist details label, since  we're not showing a single checklist                
            self.lblDetails.setText("")
            
        locationCount = self.tblList.rowCount()
        
        self.lblSpecies.setText("Locations: " + str(locationCount))
        
        MainWindow.SetChildDetailsLabels(self,  self,  filter)

        self.setWindowTitle(self.lblLocation.text() + ": " + self.lblDateRange.text())

        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_location.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)  

        self.tblList.addAction(self.actionSetLocationFilter)
        self.tblList.addAction(self.actionSetFirstDateFilter)
        self.tblList.addAction(self.actionSetLastDateFilter)
        
        self.scaleMe()
        self.resizeMe()
        
        return(True)


    def tblListClicked(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        currentRow = self.tblList.currentRow()
        currentColumn = self.tblList.currentColumn()
        
        if self.listType in ["Species", "Single Checklist"]:
            if currentColumn in [0, 5]:
                # the taxonomy order or percentage column was clicked, so abort. We won't create a report.
                # turn off the hourglass cursor before exiting
                QApplication.restoreOverrideCursor()     
                return
                
            if currentColumn== 1:
                # species column has been clicked so create individual window for that species
                speciesName = self.tblList.item(currentRow,  1).text()
                
                # abort if a spuh or slash species was clicked (we can't show an individual for this)
                if "sp." in speciesName or "/" in speciesName:
                    QApplication.restoreOverrideCursor()     
                    return                    
                
                sub = Individual()
                sub.FillIndividual(speciesName)
                
            if currentColumn in [2, 3]:
                # If list is already a checklist, we abort
                if self.filter.getChecklistID() != "":
                    QApplication.restoreOverrideCursor()  
                    return
                    
                # date column has been clicked so create species list frame for that dateArray
                date = self.tblList.item(currentRow,  self.tblList.currentColumn()).text()
                speciesName = self.tblList.item(currentRow,  1).data(Qt.UserRole)

                filter = Filter()
                filter.setSpeciesName(speciesName)
                filter.setStartDate(date)
                filter.setEndDate(date)
                
                # get all checklists that have this date and species
                checklists = MainWindow.db.GetChecklists(filter)
                
                # see if only one checklist meets filter
                # create a SpeciesList window to display a checklist if only one is found
                # create a checklists list window if more than one if found
                if len(checklists) == 1:
                    filter.setSpeciesName("")
                    filter.setChecklistID(checklists[0][0])
                    filter.setLocationType("Location")
                    filter.setLocationName(checklists[0][3])
                    sub = Lists()
                    sub.FillSpecies(filter) 
                if len(checklists) > 1:
                    sub = Lists()
                    sub.FillChecklists(filter)

            if currentColumn == 4:
                # If list is already a checklist, we abort
                if self.filter.getChecklistID() != "":
                    QApplication.restoreOverrideCursor()  
                    return
                    
                # checklist count column has been clicked so create checklist list for widget's filter and species
                speciesName = self.tblList.item(currentRow,  1).text()

                filter = deepcopy(self.filter)
                filter.setSpeciesName(speciesName)
                
                # get all checklists that have this date and species
                checklists = MainWindow.db.GetChecklists(filter)
                
                if len(checklists) > 0:
                    sub = Lists()
                    sub.FillChecklists(filter)

        if self.listType == "Locations":
                
            if currentColumn == 0:
                # species column has been clicked so create individual window for that species
                locationName = self.tblList.item(currentRow,  0).text()
                
                sub = Location()
                sub.FillLocation(locationName)
                
            if currentColumn > 0:

                # date column has been clicked so create species list frame for that dateArray
                clickedText = self.tblList.item(currentRow,  self.tblList.currentColumn()).text()
                date = clickedText.split(" ")[0]
                time = clickedText.split(" ")[1]
                locationName = self.tblList.item(currentRow,  0).text()

                filter = Filter()
                filter.setLocationName(locationName)
                filter.setLocationType("Location")
                filter.setStartDate(date)
                filter.setEndDate(date)
                filter.setTime(time)
                
                # get all checklists that have this date and location
                checklists = MainWindow.db.GetChecklists(filter)
                
                # see if only one checklist meets filter
                # create a SpeciesList window to display a checklist if only one is found
                # create a checklists list window if more than one if found
                if len(checklists) == 1:
                    filter.setSpeciesName("")
                    filter.setChecklistID(checklists[0][0])
                    filter.setLocationType("Location")
                    filter.setLocationName(checklists[0][3])
                    sub = Lists()
                    sub.FillSpecies(filter) 
                if len(checklists) > 1:
                    sub = Lists()
                    sub.FillChecklists(filter)

        if self.listType in ["Checklists", "Find Results"]:

            checklistID = self.tblList.item(currentRow, 0).data(Qt.UserRole)
            
            filter = Filter()
            filter.setChecklistID(checklistID)
            
            location = MainWindow.db.GetLocations(filter)[0]
            date = MainWindow.db.GetDates(filter)[0]

            filter = Filter()
            filter.setChecklistID(checklistID)
            filter.setLocationName(location)
            filter.setLocationType("Location")
            filter.setStartDate(date)
            filter.setEndDate(date)

            sub = Lists()
            sub.FillSpecies(filter)
            
        sub.mdiParent = self.mdiParent
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show() 
        sub.resizeMe()
        QApplication.restoreOverrideCursor()     
        

class DateTotals(QMdiSubWindow, DateTotals.Ui_frmDateTotals):
            
    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()            
    
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""        
        self.tblYearTotals.itemDoubleClicked.connect(self.YearTableClicked)
        self.tblMonthTotals.itemDoubleClicked.connect(self.MonthTableClicked)
        self.tblDateTotals.itemDoubleClicked.connect(self.DateTableClicked)        
        self.tblYearTotals.setShowGrid(False)
        self.tblDateTotals.setShowGrid(False)
        self.tblMonthTotals.setShowGrid(False)
        self.resized.connect(self.resizeMe) 
        self.tabDateTotals.setCurrentIndex(0)
        self.filter = Filter()

        self.tblDateTotals.addAction(self.actionSetDateFilter)
        self.tblMonthTotals.addAction(self.actionSetDateFilterToMonth)
        self.tblYearTotals.addAction(self.actionSetDateFilterToYear)
        
        self.actionSetDateFilter.triggered.connect(self.setDateFilter)
        self.actionSetDateFilterToMonth.triggered.connect(self.setSeasonalRangeFilterToMonth)
        self.actionSetDateFilterToYear.triggered.connect(self.setDateFilterToYear)
        
        self.scaleMe()
        self.resizeMe()


    def DateTableClicked(self):
        sub = Lists()
        sub.mdiParent = self.mdiParent 
        
        date = self.tblDateTotals.item(self.tblDateTotals.currentRow(),  1).text()        
        tempFilter = deepcopy(self.filter)
        tempFilter.setStartDate(date)
        tempFilter.setEndDate(date)

        if self.tblDateTotals.currentColumn() in [0, 1, 2]:
            sub.FillSpecies(tempFilter)

        if self.tblDateTotals.currentColumn() == 3:
            sub.FillChecklists(tempFilter)
            
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)                
        sub.show()   


    def MonthTableClicked(self):
        month = self.tblMonthTotals.item(self.tblMonthTotals.currentRow(),  1).text() 
        monthRange = ["Jan",  "Feb",  "Mar",  "Apr", "May",   "Jun",  "Jul",  "Aug",  "Sep",  "Oct",  "Nov",  "Dec"]
        monthNumberStrings = ["01",  "02",  "03",  "04",  "05",  "06",  "07",  "08",  "09",  "10",  "11",  "12"]
        monthNumber = monthRange.index(month)
        # find last day of the selected month
        if month in ["Apr", "Jun",  "Sep",  "Nov"]: lastDay = "30"
        if month in ["Jan",  "Mar", "May",  "Jul",  "Aug", "Oct",  "Dec"]: lastDay = "31"
        if month == "Feb": lastDay = "29"
        
        sub = Lists()
        
        tempFilter = deepcopy(self.filter)
        tempFilter.setStartSeasonalMonth(monthNumberStrings[monthNumber])
        tempFilter.setStartSeasonalDay("01")
        tempFilter.setEndSeasonalMonth(monthNumberStrings[monthNumber])
        tempFilter.setEndSeasonalDay(lastDay)
        
        if self.tblMonthTotals.currentColumn() in [0, 1, 2]:
            sub.FillSpecies(tempFilter)

        if self.tblMonthTotals.currentColumn() == 3:
            sub.FillChecklists(tempFilter)
    
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)                
        sub.show()   


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
            "Date Totals" + 
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
            "Year Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>Year</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblYearTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblYearTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblYearTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblYearTotals.item(r, 2).text() +
            "</td>" +
            "<td>" +
            self.tblYearTotals.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
            
        html = html + (
            "</table>"
            "</font size>"
            )

        html = html + (
            "<H3>" + 
            "Month Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>Month</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblMonthTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblMonthTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblMonthTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblMonthTotals.item(r, 2).text() +
            "</td>" +
            "<td>" +
            self.tblMonthTotals.item(r, 3).text() +
            "</td>" +
            "</tr>"
            )
            
        html = html + (
            "</table>"
            "</font size>"
            )

        html = html + (
            "<H3>" + 
            "Date Totals" + 
            "</H3>"
            )        
            
        html=html + (
            "<font size='2'>" +
            "<table width='100%'>" +
            " <tr>"
            )
                    
        html=html + (    
            "<th>Rank</th>" +
            "<th>Date</th> " +
            "<th>Species</th>" +
            "<th>Checklists</th>" +
            "</tr>"
            )
            
        for r in range(self.tblDateTotals.rowCount()):
            html = html + (
            "<tr>" +
            "<td>" +
            self.tblDateTotals.item(r, 0).text() +
            "</td>" +
            "<td>" +
            self.tblDateTotals.item(r, 1).text() +
            "</td>" +
            "<td>" +
            self.tblDateTotals.item(r, 2).text() +
            "</td>" +
            "<td>" +
            self.tblDateTotals.item(r, 3).text() +
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


    def YearTableClicked(self):

        sub = Lists()
        sub.mdiParent = self.mdiParent

        year = self.tblYearTotals.item(self.tblYearTotals.currentRow(),  1).text()                
        startDate = year + "-01-01"
        endDate = year + "-12-31"
        
        tempFilter = deepcopy(self.filter)
        tempFilter.setStartDate(startDate)
        tempFilter.setEndDate(endDate)
        
        if self.tblYearTotals.currentColumn() in [0, 1, 2]:
            sub.FillSpecies(tempFilter)

        if self.tblYearTotals.currentColumn() == 3:
            sub.FillChecklists(tempFilter)
            
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)                
        sub.show()   
    
    
    def FillDateTotals(self,  filter):
        
        self.filter = filter
        
        # find all years, months, and dates in db
        dbYears = set()
        dbMonths = set()
        dbDates = set()   
        dbFilteredSightings = []
        yearDict = defaultdict()
        monthDict = defaultdict()
        dateDict = defaultdict()
        
        minimalSightingList = MainWindow.db.GetMinimalFilteredSightingsList(filter)
        
        for sighting in minimalSightingList:
            
            # Consider only full species, not slash or spuh entries
            if ("/" not in sighting[1]) and ("sp." not in sighting[1]):
            
                if MainWindow.db.TestSighting(sighting,  filter) is True:
                    dbYears.add(sighting[10][0:4])
                    dbMonths.add(sighting[10][5:7])
                    dbDates.add(sighting[10])
                    dbFilteredSightings.append(sighting)
                    
                    if sighting[10][0:4] not in yearDict.keys():
                        yearDict[sighting[10][0:4]] = [sighting]
                    else:
                        yearDict[sighting[10][0:4]].append(sighting)
                    
                    if sighting[10][5:7] not in monthDict.keys():
                        monthDict[sighting[10][5:7]] = [sighting]
                    else:
                        monthDict[sighting[10][5:7]].append(sighting)
                    
                    if sighting[10] not in dateDict.keys():
                        dateDict[sighting[10]] = [sighting]
                    else:
                        dateDict[sighting[10]].append(sighting)

        # check that we have at least one sighting to work with
        # otherwise, abort so MainWindow can post message to user
        if len(yearDict) == 0:
            return(False)
        
        # set numbers of rows for each tab's grid (years, months, dates)
        self.tblYearTotals.setRowCount(len(dbYears)+1)
        self.tblYearTotals.setColumnCount(4)
        self.tblMonthTotals.setRowCount(len(dbMonths)+1)
        self.tblMonthTotals.setColumnCount(4)
        self.tblDateTotals.setRowCount(len(dbDates)+1)
        self.tblDateTotals.setColumnCount(4)

#        # sort dbFilteredSightings on date
#        dbFilteredSightings.sort(key=lambda x: x[10])

        yearArray = []

        for year in dbYears:
            yearSpecies = set()
            yearChecklists = set()
            for s in yearDict[year]:
                yearSpecies.add(s[1])
                yearChecklists.add(s[0])
            yearArray.append([len(yearSpecies),  year, len(yearChecklists)])
        yearArray.sort(reverse=True)
        R = 0
        for year in yearArray:            
            rankItem = QTableWidgetItem()
            rankItem.setData(Qt.DisplayRole, R+1)
            yearItem = QTableWidgetItem()
            yearItem.setText(year[1])
            yearTotalItem = QTableWidgetItem()
            yearTotalItem.setData(Qt.DisplayRole, year[0])
            yearTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
            yearChecklistTotalItem = QTableWidgetItem()
            yearChecklistTotalItem.setData(Qt.DisplayRole, year[2])
            yearChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)
            self.tblYearTotals.setItem(R, 0, rankItem)    
            self.tblYearTotals.setItem(R, 1, yearItem)
            self.tblYearTotals.setItem(R, 2, yearTotalItem)
            self.tblYearTotals.setItem(R, 3, yearChecklistTotalItem)
            R = R + 1

        monthArray = []
        for month in dbMonths:
            monthSpecies = set()
            monthChecklists = set()
            monthChecklists.add(s[0])
            for s in monthDict[month]:
                monthSpecies.add(s[1])
                monthChecklists.add(s[0])
            monthArray.append([len(monthSpecies),  month, len(monthChecklists)])
        monthArray.sort(reverse=True)
        R = 0
        for month in monthArray:
            if month[1] == "01":
                month[1] = "Jan"
            if month[1] == "02":
                month[1] = "Feb"
            if month[1] == "03":
                month[1] = "Mar"
            if month[1] == "04":
                month[1] = "Apr"
            if month[1] == "05":
                month[1] = "May"
            if month[1] == "06":
                month[1] = "Jun"
            if month[1] == "07":
                month[1] = "Jul"
            if month[1] == "08":
                month[1] = "Aug"
            if month[1] == "09":
                month[1] = "Sep"
            if month[1] == "10":
                month[1] = "Oct"
            if month[1] == "11":
                month[1] = "Nov"
            if month[1] == "12":
                month[1] = "Dec"        
            rankItem = QTableWidgetItem()
            rankItem.setData(Qt.DisplayRole, R+1)
            monthItem= QTableWidgetItem()
            monthItem.setText(month[1])
            monthTotalItem = QTableWidgetItem()
            monthTotalItem.setData(Qt.DisplayRole, month[0])
            monthTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)         
            monthChecklistTotalItem = QTableWidgetItem()
            monthChecklistTotalItem.setData(Qt.DisplayRole, month[2])   
            monthChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)         
            self.tblMonthTotals.setItem(R, 0, rankItem)    
            self.tblMonthTotals.setItem(R, 1, monthItem)
            self.tblMonthTotals.setItem(R, 2, monthTotalItem)
            self.tblMonthTotals.setItem(R, 3, monthChecklistTotalItem)
            R = R + 1
        R = -1
        
        dateArray = []
                
        for date in dbDates:
            dateSpecies = set()
            dateChecklists = set()
            for s in dateDict[date]:
                dateSpecies.add(s[1])
                dateChecklists.add(s[0])
            dateArray.append([len(dateSpecies),  date, len(dateChecklists)])
                        
        dateArray.sort(reverse=True)
        R = 0
        rank = 1
        lastDateTotal = 0
        for date in dateArray:            
            dateItem = QTableWidgetItem()
            dateItem.setText(date[1][0:4] + "-" + date[1][5:7] + "-" + date[1][8:])
            dateTotalItem = QTableWidgetItem()
            dateTotalItem.setData(Qt.DisplayRole, date[0])
            dateTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                     
            if date[0] != lastDateTotal:
                rank = R+1
            rankItem = QTableWidgetItem()
            rankItem.setData(Qt.DisplayRole, rank)
            dateChecklistTotalItem = QTableWidgetItem()
            dateChecklistTotalItem.setData(Qt.DisplayRole, date[2])    
            dateChecklistTotalItem.setTextAlignment(Qt.AlignCenter|Qt.AlignVCenter)                     
            self.tblDateTotals.setItem(R, 0, rankItem)    
            self.tblDateTotals.setItem(R, 1, dateItem)
            self.tblDateTotals.setItem(R, 2, dateTotalItem)
            self.tblDateTotals.setItem(R, 3, dateChecklistTotalItem)
            lastDateTotal = date[0]
            
            R = R + 1
    
        self.tblYearTotals.horizontalHeader().setVisible(True)
        self.tblMonthTotals.horizontalHeader().setVisible(True)
        self.tblDateTotals.horizontalHeader().setVisible(True)
        self.tblYearTotals.setHorizontalHeaderLabels(['Rank', 'Year', 'Species', 'Checklists'])
        self.tblYearTotals.setSortingEnabled(True)
        self.tblYearTotals.sortItems(0,0)
        self.tblMonthTotals.setHorizontalHeaderLabels(['Rank', 'Month', 'Species', 'Checklists'])
        self.tblMonthTotals.setSortingEnabled(True)
        self.tblMonthTotals.sortItems(0,0)
        self.tblDateTotals.setHorizontalHeaderLabels(['Rank', 'Date', 'Species', 'Checklists'])
        self.tblDateTotals.setSortingEnabled(True)
        self.tblDateTotals.sortItems(0,0)
        self.tblYearTotals.removeRow(self.tblYearTotals.rowCount()-1)
        self.tblMonthTotals.removeRow(self.tblMonthTotals.rowCount()-1)
        self.tblDateTotals.removeRow(self.tblDateTotals.rowCount()-1)
        header = self.tblYearTotals.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header = self.tblMonthTotals.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header = self.tblDateTotals.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        MainWindow.SetChildDetailsLabels(self,  self,  self.filter)

        self.setWindowTitle("Date Totals: " + str(self.tblDateTotals.rowCount()) + " dates" )   

        if self.lblDetails.text() != "":
            self.lblDetails.setVisible(True)
        else:
            self.lblDetails.setVisible(False)
        
        self.scaleMe()
        
        # tell MainWindow that all is OK
        return(True)
        
        
    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)
   
   
    def setDateFilter(self):        
        currentRow = self.tblDateTotals.currentRow()
        date = self.tblDateTotals.item(currentRow, 1).text()
        self.mdiParent.setDateFilter(date)


    def setSeasonalRangeFilterToMonth(self):        
        currentRow = self.tblMonthTotals.currentRow()
        month = self.tblMonthTotals.item(currentRow, 1).text()
        self.mdiParent.setSeasonalRangeFilter(month)  # month is in format three-letter English abbreviation


    def setDateFilterToYear(self):        
        currentRow = self.tblYearTotals.currentRow()
        year = self.tblYearTotals.item(currentRow, 1).text()
        startDate = year + "-01-01"
        endDate = year + "-12-31"
        self.mdiParent.setDateFilter(startDate, endDate)
        
         
    def scaleMe(self):
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  600  * scaleFactor
        windowHeight = 580 * scaleFactor    
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
        #scale the font for all widgets in window
        for w in self.layLists.children():
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

        metrics = self.tblYearTotals.fontMetrics()
        textHeight = metrics.boundingRect("A").height()        
        rankTextWidth = metrics.boundingRect("Rank").width()
        
        for t in [self.tblYearTotals, self.tblMonthTotals, self.tblDateTotals]:
            header = t.horizontalHeader()
            header.resizeSection(0,  floor(2 * rankTextWidth))
            header.resizeSection(2,  floor(2.5 * rankTextWidth))
            header.resizeSection(3,  floor(2.5 * rankTextWidth))
            for r in range(t.rowCount()):
                t.setRowHeight(r, textHeight * 1.1) 
 
        
class Families(QMdiSubWindow, Families.Ui_frmFamilies):

    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()   
            
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""        
        self.lstFamilies.currentRowChanged.connect(self.FillSpecies)
        self.lstFamilies.itemDoubleClicked.connect(self.ClickedLstFamilies)  
        self.lstSpecies.itemDoubleClicked.connect(self.ClickedLstSpecies)          
        self.lstFamilies.setSpacing(2)
        self.lstSpecies.setSpacing(2)
        self.resized.connect(self.resizeMe)  
        self.tabFamilies.setCurrentIndex(0)        
        self.filter = Filter()
        self.filteredSpeciesList = []
        self.filteredSpeciesListWithFamilies = []
        self.familiesList = []
        self.scaleMe()
        self.resizeMe()
    
    
    def ClickedLstSpecies(self):
        species = self.lstSpecies.currentItem().text()
        self.CreateIndividual(species)    


    def ClickedLstFamilies(self):
        family = self.lstFamilies.currentItem().text()
        self.CreateFamilyList(family)
        

    def CreateFamilyList(self,  family):
        
        tempFilter = deepcopy(self.filter)
        tempFilter.setFamily(family)
        
        sub = Lists()
        sub.FillSpecies(tempFilter)
        
        sub.mdiParent = self.mdiParent        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()

    
    def CreateIndividual(self,  species):
        sub = Individual()
        sub.mdiParent = self.mdiParent
        sub.FillIndividual(species)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()
        sub.resizeMe()


    def FillSpecies(self):
        self.lstSpecies.clear()
        if self.lstFamilies.currentIndex() is not None:
            selectedFamily = self.lstFamilies.currentItem().text()
            familySpecies = []
            # check if we've already added each species' family to list
            if len(self.filteredSpeciesListWithFamilies) == 0:
                # need to add species' families to list               
                for s in self.filteredSpeciesList:
                    thisFamily = MainWindow.db.GetFamilyName(s)
                    self.filteredSpeciesListWithFamilies.append([s,  thisFamily])
            for sf in self.filteredSpeciesListWithFamilies:               
                if sf[1]== selectedFamily:
                    familySpecies.append(sf[0])
            self.lstSpecies.addItems(familySpecies)
            self.lstSpecies.setSpacing(2)
            
            count = MainWindow.db.CountSpecies(familySpecies)
            self.lblSpecies.setText("Species for selected family (" + str(count) + ")")
            
        
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
            self.lblLocation.text() + 
            "</H1>"
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
        
        html=html + (
            "<font size='2'>"
            )
            
        # add family names and the species under them
        
        for r in range(self.lstFamilies.count()):
            html = html + (
                "<h3>" +
                self.lstFamilies.item(r).text() +
                "</h3>"
                )
            self.filter.setFamily(self.lstFamilies.item(r).text())
            for s in MainWindow.db.GetSpecies(self.filter):
                html = html + (
                    s +
                    "<br>"
                    )                

        html = html + (
            "<font size>" +            
            "</body>" +
            "</html>"
            )
            
        QApplication.restoreOverrideCursor()   
        
        return(html)
        
    
    def FillFamilies(self, filter):
        self.filter = deepcopy(filter)
        
        self.familiesList = MainWindow.db.GetFamilies(self.filter)
        self.filteredSpeciesList = MainWindow.db.GetSpecies(self.filter)
        cleanedFilteredSpeciesList = []
        for s in self.filteredSpeciesList:
            if ("sp." not in s) and ("/" not in s):
                cleanedFilteredSpeciesList.append(s)
        self.filteredSpeciesList = cleanedFilteredSpeciesList
        
        self.lblFamilies.setText("Families (" + str(len(self.familiesList )) + "):")
        self.lstFamilies.addItems(self.familiesList )
        if len(self.familiesList ) > 0:
            self.lstFamilies.setCurrentRow(0)
            self.FillSpecies()
            self.FillPieChart()
            self.lstFamilies.setSpacing(2)
        
        else:
            # no families were found matching filter, so report failure back to MainWindow
            return(False)
            
        MainWindow.SetChildDetailsLabels(self,  self,  self.filter)

        self.setWindowTitle("Families: "+ self.lblLocation.text() + ": " + self.lblDateRange.text())
        
        # report success back to MainWindow
        return(True)
        

    def FillPieChart(self):
        self.tblPieChartLegend.clear()
        
        scene = QGraphicsScene()
        self.tblPieChartLegend.setColumnCount(3)       
        self.tblPieChartLegend.setRowCount(len(self.familiesList))        
        self.tblPieChartLegend.horizontalHeader().setVisible(False)
        header = self.tblPieChartLegend.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)     
        self.tblPieChartLegend.setShowGrid(False)
        total = 0
        colours = []
        familiesCount = []
        set_angle = 0
        R = 0
        
        for f in self.familiesList:
            familiesCount.append(sum(x.count(str(f)) for x in self.filteredSpeciesListWithFamilies))
        total = sum(familiesCount)
        
        for fl in range(len(self.familiesList)):
            number = []
            # randomly create three color values (rgb)
            for rgb in range(3):
                number.append(random.randrange(0, 255))
            colours.append(QColor(number[0],number[1],number[2]))

        if self.gvPieChart.width() < self.gvPieChart.height():
            shorterSide = self.gvPieChart.width()
        else:
            shorterSide = self.gvPieChart.height()
            
        pieChartRadius = floor(.9 * shorterSide)
        for family in familiesCount:  
            # create the angle of each wedge according to its perecent of 360
            angle = round(family/total*16*360)
            # set size of circle and create wedge
            ellipse = QGraphicsEllipseItem(0, 0, pieChartRadius, pieChartRadius)
            # set center of circle, like an axle
            ellipse.setPos(0,0)
            # rotate through the wedge
            ellipse.setStartAngle(set_angle)
            ellipse.setSpanAngle(angle)
            # assign color
            ellipse.setBrush(colours[R])
            # create set_angle for next time around
            set_angle = angle + set_angle
            # add the actual wedge to the scene object
            scene.addItem(ellipse) 
            # add entry to legend table and set proper color
            colorItem = QTableWidgetItem()
            colorItem.setBackground(QColor(colours[R]))
            familyNameItem = QTableWidgetItem()
            familyNameItem.setData(Qt.DisplayRole, self.familiesList[R])
            familyCountItem = QTableWidgetItem()
            familyCountItem.setData(Qt.DisplayRole, family)            
            self.tblPieChartLegend.setItem(R, 0, colorItem) 
            self.tblPieChartLegend.setItem(R, 1, familyNameItem)
            self.tblPieChartLegend.setItem(R, 2, familyCountItem)
            
            R = R + 1 
#        self.tblPieChartLegend.removeRow(len(self.familiesList)-1)
        self.gvPieChart.setScene(scene)
        

    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)
        self.FillPieChart()
   
   
    def scaleMe(self):
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  780  * scaleFactor
        windowHeight = 500 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
        #scale the font for all widgets in window
        for w in self.children():
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

        metrics = self.tblPieChartLegend.fontMetrics()
        textHeight = metrics.boundingRect("A").height()        
        textWidth = metrics.boundingRect("Rank").width()
        
        for t in [self.tblPieChartLegend]:
            header = t.horizontalHeader()
            header.resizeSection(0,  floor(.75 * textWidth))
            header.resizeSection(2,  floor(.75 * textWidth))
            for r in range(t.rowCount()):
                t.setRowHeight(r, textHeight * 1.1) 
    

class Individual(QMdiSubWindow, Individual.Ui_frmIndividual):

    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()
   
   
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""        
        self.resized.connect(self.resizeMe)                    
        self.trLocations.currentItemChanged.connect(self.FillDates)
        self.trLocations.itemDoubleClicked.connect(self.CreateLocation)
        self.trDates.currentItemChanged.connect(lambda: self.FillLocations(self.trDates))   
        self.trMonthDates.currentItemChanged.connect(lambda: self.FillLocations(self.trMonthDates))           
        self.lstDates.itemDoubleClicked.connect(lambda: self.CreateSpeciesList(self.lstDates))   
        self.tblYearLocations.itemDoubleClicked.connect(lambda: self.CreateSpeciesList(self.tblYearLocations))
        self.tblMonthLocations.itemDoubleClicked.connect(lambda: self.CreateSpeciesList(self.tblMonthLocations))
        self.buttonMacaulay.clicked.connect(self.CreateWebPageForPhotos)
        self.buttonWikipedia.clicked.connect(self.CreateWebPageForWikipedia)
        self.buttonAllAboutBirds.clicked.connect(self.CreateWebPageForAllAboutBirds)
        self.buttonAudubon.clicked.connect(self.CreateWebPageForAudubon)
        self.buttonMap.clicked.connect(self.CreateMap)
        self.buttonChecklists.clicked.connect(self.CreateChecklists)
        self.tabIndividual.setCurrentIndex(0)

 
    def FillIndividual(self, Species): 
        self.setWindowTitle(Species)
        self.lblCommonName.setText(Species)
        self.lblCommonName.setStyleSheet('QLabel {color: blue;}')
        self.lblScientificName.setText(MainWindow.db.GetScientificName(Species))
        orderAndFamilyText = MainWindow.db.GetOrderName(Species)
        # check if taxonomy data has been loaded. If so, add a semi-colon and the family name
        if orderAndFamilyText != "":
            orderAndFamilyText = orderAndFamilyText + "; " + MainWindow.db.GetFamilyName(Species)
        self.lblOrderName.setText(orderAndFamilyText)
        # find list of dates for species, to find oldest and newest
        filter = Filter()
        filter.setSpeciesName(Species)
        dbDates = MainWindow.db.GetDates(filter)
        firstDate = dbDates[0]
        lastDate = dbDates[len(dbDates)-1]
        
        # create filter to find the first location seen
        filter = Filter()
        filter.setStartDate(firstDate)
        filter.setEndDate(firstDate)
        filter.setSpeciesName(Species)
        firstDateLocations = MainWindow.db.GetLocations(filter, "Checklist")
        firstDateLocations =  sorted(firstDateLocations, key=lambda x: (x[3]))
        firstLocation = firstDateLocations[0][0]
        
        # create filter to find the last location seen
        filter = Filter()
        filter.setStartDate(lastDate)
        filter.setEndDate(lastDate)
        filter.setSpeciesName(Species)
        lastDateLocations = MainWindow.db.GetLocations(filter, "Checklist")
        lastDateLocations =  sorted(lastDateLocations, key=lambda x: (x[3]))
        lastLocation = lastDateLocations[len(lastDateLocations) - 1][0]
        
        self.lblFirstSeen.setText(
            "First seen: " 
            + dbDates[0] 
            + " at " 
            + firstLocation
            )
                                                       
        self.lblMostRecentlySeen.setText(
            "Most recently seen: " 
            + dbDates[len(dbDates ) - 1] 
            + " at " 
            + lastLocation
            )
            
        # display all locations for the species
        filter = Filter()
        filter.setSpeciesName(Species)
        locationList = MainWindow.db.GetLocations(filter,  "LocationHierarchy")
        dateList = MainWindow.db.GetDates(filter)

        # fill treeview Locations widget
        self.trLocations.setColumnCount(1)
        theseCountries = set()
        
        sortedLocationList = sorted(locationList, key=lambda x: (x[0], x[1], x[2]))
        
        # add the top-level country tree items
        for l in sortedLocationList:
            theseCountries.add(l[0][0:2])
        
        locationCount = 0
        theseCountries = list(theseCountries)
        theseCountries.sort()
        
        for c in theseCountries:
            thisCountryItem = QTreeWidgetItem()
            thisCountry = MainWindow.db.GetCountryName(c)
            thisCountryItem.setText(0,  thisCountry)   
            self.trLocations.addTopLevelItem(thisCountryItem)
            thisCountryItem.setSizeHint(0,  QSize(20,  20))
            
            theseStates = set()
            for l in sortedLocationList:
                if l[0][0:2] == c:
                    theseStates.add(l[0])
            theseStates = list(theseStates)
            theseStates.sort()
            
            for s in theseStates:
                thisState = MainWindow.db.GetStateName(s)
                stateTreeItem = QTreeWidgetItem()
                stateTreeItem.setText(0, thisState)
                thisCountryItem.addChild(stateTreeItem)
                stateTreeItem.setSizeHint(0, QSize(20,  20))

                theseCounties = set()
                for l in sortedLocationList:
                    if l[0] == s:
                        theseCounties.add(l[1])
                theseCounties = list(theseCounties)
                theseCounties.sort()
                
                for co in theseCounties:
                    countyTreeItem= QTreeWidgetItem()                    
                    if co == "":
                        countyTreeItem.setText(0, "No County Name")
                    else:
                        countyTreeItem.setText(0, co)                    
                    stateTreeItem.addChild(countyTreeItem)
                    countyTreeItem.setSizeHint(0, QSize(20,  20))
        
                    theseLocations= []
                    for l in sortedLocationList:
                        if l[0] == s and l[1] == co:
                            theseLocations.append(l[2])
                    theseLocations.sort()
                    
                    for lo in theseLocations:
                        locationTreeItem = QTreeWidgetItem()
                        locationTreeItem.setText(0, lo)
                        countyTreeItem.addChild(locationTreeItem)
                        locationTreeItem.setSizeHint(0, QSize(20,  20))                        
                        
                    locationCount = locationCount + len(theseLocations)
        
        # Fill Year Tree widget
        theseYears = []
        
        theseYears = set()
        for d in dateList:
            theseYears.add(d[0:4])
        
        theseYears = list(theseYears)
        theseYears.sort()
        
        dateCount = 0
        for y in theseYears:
            thisYearItem = QTreeWidgetItem()
            thisYearItem.setText(0, str(y))   
            self.trDates.addTopLevelItem(thisYearItem)
            thisYearItem.setSizeHint(0, QSize(20,  20))
            
            theseMonths = set()
            for d in dateList:
                if y == d[0:4]:
                    theseMonths.add(d[5:7])
            
            theseMonths = list(theseMonths)
            theseMonths.sort()
            
            for m in theseMonths:
                monthName = MainWindow.db.GetMonthName(m)
                monthTreeItem = QTreeWidgetItem()
                monthTreeItem.setText(0, str(monthName))
                thisYearItem.addChild(monthTreeItem)
                monthTreeItem.setSizeHint(0, QSize(20,  20))

                theseDates = set()
                for da in dateList:
                    if da[0:4] == y:
                        if da[5:7] == m:
                            theseDates.add(da)
                                
                theseDates = list(theseDates)
                theseDates.sort()
                
                for td in theseDates:
                    dateTreeItem= QTreeWidgetItem()                    
                    dateTreeItem.setText(0, str(td))                    
                    monthTreeItem.addChild(dateTreeItem)
                    dateTreeItem.setSizeHint(0, QSize(20,  20))                       

                dateCount = dateCount + len(theseDates)

        # Fill Month Tree widget
        theseMonths = []
        
        theseMonths = set()
        for d in dateList:
            theseMonths.add(d[5:7])
        
        theseMonths = list(theseMonths)
        theseMonths.sort()
        
        dateCount = 0
        for m in theseMonths:
            monthName = MainWindow.db.GetMonthName(m)
            thisMonthItem = QTreeWidgetItem()
            thisMonthItem.setText(0, monthName)   
            self.trMonthDates.addTopLevelItem(thisMonthItem)
            thisMonthItem.setSizeHint(0, QSize(20,  20))
            
            theseYears = set()
            for d in dateList:
                if m == d[5:7]:
                    theseYears.add(d[0:4])
            
            theseYears = list(theseYears)
            theseYears.sort()
            
            for y in theseYears:
                yearTreeItem = QTreeWidgetItem()
                yearTreeItem.setText(0, y)
                thisMonthItem.addChild(yearTreeItem)
                yearTreeItem.setSizeHint(0, QSize(20,  20))

                theseDates = set()
                for da in dateList:
                    if da[0:4] == y:
                        if da[5:7] == m:
                            theseDates.add(da)
                                
                theseDates = list(theseDates)
                theseDates.sort()
                
                for td in theseDates:
                    dateTreeItem= QTreeWidgetItem()                    
                    dateTreeItem.setText(0, str(td))                    
                    yearTreeItem.addChild(dateTreeItem)
                    dateTreeItem.setSizeHint(0, QSize(20,  20))                       

                dateCount = dateCount + len(theseDates)

        if locationCount == 1:
            self.lblLocations.setText("Location (1)")
        else:
            self.lblLocations.setText("Locations (" + str(locationCount) + ")")   

        self.scaleMe()
        self.resizeMe()            

        
    def FillDates(self):

        currentItem = self.trLocations.currentItem()        
        species = self.lblCommonName.text()
        location = currentItem.text(0)
        self.lstDates.clear()
        
        filter = Filter()
        filter.setSpeciesName(species)
        
        # check if top-level country is currentItem
        if currentItem.parent() is None:
            filter.setLocationType("Country")
            filter.setLocationName(MainWindow.db.GetCountryCode(location))

        # check if second-level state is currentItem        
        elif currentItem.parent().parent() is None:
            filter.setLocationType("State")
            filter.setLocationName(MainWindow.db.GetStateCode(location))            
            
        # check if third-level county is currentItem
        elif currentItem.parent().parent().parent() is None:
            filter.setLocationType("County") 
            filter.setLocationName(location)            
        
        # check if fourth-level location is currentItem
        else:
            filter.setLocationType("Location")
            filter.setLocationName(location)            
            
        dates = MainWindow.db.GetDates(filter)
        
        self.lstDates.addItems(dates)
        self.lstDates.setCurrentRow(0)
        self.lstDates.setSpacing(2)
        self.lblDatesForLocation.setText("Dates for selected location (" + str(self.lstDates.count()) + ")")


    def FillLocations(self,  callingWidget):
        
        species = self.lblCommonName.text()
        currentItem = callingWidget.currentItem()
        
        filter = Filter()
        filter.setSpeciesName(species)
        
        if callingWidget.objectName() == "trDates":
            locationWidget = self.tblYearLocations
            
            # check if currentItem is a year
            if currentItem.parent() is None:
                filter.setStartDate(currentItem.text(0) + "-01-01")
                filter.setEndDate(currentItem.text(0) + "-12-31")                
            
            # check if currentItem is a month
            elif currentItem.parent().parent() is None:
                month = currentItem.text(0)
                monthNumberString =  MainWindow.db.monthNumberDict[month]
                lastDayOfThisMonth = MainWindow.db.GetLastDayOfMonth(monthNumberString)
                year = currentItem.parent().text(0)
                filter.setStartDate(year + "-" + monthNumberString + "-01")
                filter.setEndDate(year + "-" + monthNumberString + "-" + lastDayOfThisMonth)
            
            # item is a just a single date
            else:
                filter.setStartDate(currentItem.text(0))
                filter.setEndDate(currentItem.text(0))                

        if callingWidget.objectName() == "trMonthDates":

            locationWidget = self.tblMonthLocations
                        
            # check if currentItem is a month
            if currentItem.parent() is None:
                monthNumberString = MainWindow.db.monthNumberDict[currentItem.text(0)]
                lastDayOfThisMonth = MainWindow.db.GetLastDayOfMonth(monthNumberString)
                filter.setStartSeasonalMonth(monthNumberString)
                filter.setStartSeasonalDay("01")
                filter.setEndSeasonalMonth(monthNumberString)
                filter.setEndSeasonalDay(lastDayOfThisMonth)
           
            # check if currentItem is a year
            elif currentItem.parent().parent() is None:
                year = currentItem.text(0)
                monthString = currentItem.parent().text(0)
                monthNumberString = MainWindow.db.monthNumberDict[monthString]
                filter.setStartDate(year + "-" + monthNumberString + "-01")
                filter.setEndDate(year + "-" + monthNumberString + "-31")
            
            # item is a just a single date
            else:
                filter.setStartDate(currentItem.text(0))
                filter.setEndDate(currentItem.text(0))    
        
        locations = MainWindow.db.GetLocations(filter, "Checklist")          
        
        locationWidget.clear()        
        locationWidget.setColumnCount(2)       
        locationWidget.setRowCount(len(locations))        
        locationWidget.horizontalHeader().setVisible(False)
        locationWidget.verticalHeader().setVisible(False)
        header = locationWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        locationWidget.setShowGrid(False)

        metrics = locationWidget.fontMetrics()
        textHeight = metrics.boundingRect("A").height()            
        
        R = 0
        for l in locations:
            locationItem = QTableWidgetItem()
            locationItem.setText(l[0])
            # store checklist ID in hidden data component of item
            locationItem.setData(Qt.UserRole,  QVariant(l[2]))
            speciesCountItem = QTableWidgetItem()
            speciesCountItem.setData(Qt.DisplayRole, l[1])
            locationWidget.setItem(R, 0, locationItem)  
            locationWidget.setItem(R, 1, speciesCountItem)
            locationWidget.setRowHeight(R, textHeight * 1.1)                 
            R = R + 1
            
        self.lblLocationsForDate.setText("Checklists (" + str(locationWidget.rowCount()) + ")")


    def CreateChecklists(self):
        species = self.lblCommonName.text()
        
        filter = Filter()
        filter.setSpeciesName(species)
        
        sub = Lists()
        sub.mdiParent = self.mdiParent
        sub.FillChecklists(filter)  
        sub.lblLocation.setText("Checklists: " + species)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()   
        

    def CreateLocation(self):
        if self.trLocations.currentItem().childCount() == 0:
            location = self.trLocations.currentItem().text(0)
            sub = Location()
            sub.mdiParent = self.mdiParent
            sub.FillLocation(location)  
            self.parent().parent().addSubWindow(sub)
            self.mdiParent.PositionChildWindow(sub, self)        
            sub.show()        


    def CreateLocationAndSetDate(self):
        location = self.trLocations.currentItem().text(0)
        date = self.lstDates.currentItem().text()
        sub = Location()
        sub.mdiParent = self.mdiParent
        sub.FillLocation(location) 
        sub.SetDate(date)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)                
        sub.show()     
        
        
    def CreateMap(self):
        species = self.lblCommonName.text()
        
        filter = Filter()
        filter.setSpeciesName(species)
        
        sub = Web()
        sub.mdiParent = self.mdiParent
        
        sub.LoadLocationsMap(filter)  
        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()   
        

    def CreateSpeciesList(self, callingWidget):

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        filter = Filter()
        filter.setSpeciesName(self.lblCommonName.text())
        
        # Get checklistID(s) and location, depending on the calling widget
        if callingWidget.objectName() in ["tblYearLocations",  "tblMonthLocations"]:
            currentRow = callingWidget.currentRow()
            checklistID = callingWidget.item(currentRow,  0).data(Qt.UserRole)
            filter.setChecklistID(checklistID)
            filter.setLocationType ("Location")
            filter.setLocationName(callingWidget.item(currentRow,  0).text())
            date = MainWindow.db.GetDates(filter)[0]
            # even though there is only one checklist here, we need a list to we can
            # loop it later
            checklists = [[checklistID]]

        if callingWidget.objectName() in ["lstDates"]:
            date = str(callingWidget.currentItem().text())
            currentItem = self.trLocations.currentItem()
            locationName = currentItem.text(0)
            #need to get the location type based on the tree hierarchy
            if currentItem.parent() is None:
                filter.setLocationType("Country")
                locationName = MainWindow.db.GetCountryCode(locationName)
            elif currentItem.parent().parent() is None:
                filter.setLocationType("State")
                locationName = MainWindow.db.GetStateCode(locationName)                
            elif currentItem.parent().parent().parent() is None:
                filter.setLocationType("County")
            else:
                filter.setLocationType("Location")
            
            filter.setLocationName(locationName)
            filter.setStartDate(date)
            filter.setEndDate(date)
                        
            checklists= MainWindow.db.GetChecklists(filter)
                    
        for c in checklists:
            cFilter = Filter()
            cFilter.setChecklistID(c[0])
            cLocation = MainWindow.db.GetLocations(cFilter,  "OnlyLocations")[0]          
            cFilter.setStartDate(date)
            cFilter.setEndDate(date)
            cFilter.setLocationType("Location")
            cFilter.setLocationName(cLocation)

            sub = Lists()
            sub.FillSpecies(cFilter)
            sub.mdiParent = self.mdiParent
            self.parent().parent().addSubWindow(sub)

            self.mdiParent.PositionChildWindow(sub, self)        
            sub.show() 

        QApplication.restoreOverrideCursor()   


    def CreateWebPageForAllAboutBirds(self):
        
        speciesCommonName = self.lblCommonName.text()

        if "(" in speciesCommonName:
            speciesCommonName = speciesCommonName.split(" (")[0]
            
        speciesCommonName = speciesCommonName.replace(" ",  "_")
        speciesCommonName = speciesCommonName.replace("'",  "")
        
        sub = Web()
        sub.mdiParent = self.mdiParent
        sub.title = "All About Birds: " + speciesCommonName        
        url = ("https://www.allaboutbirds.org/guide/"
                  + speciesCommonName
                  + "/id"
                  )
        sub.LoadWebPage(url)        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()   


    def CreateWebPageForAudubon(self):
        speciesCommonName = self.lblCommonName.text()
        
        if "(" in speciesCommonName:
            speciesCommonName = speciesCommonName.split(" (")[0]
            
        speciesCommonName = speciesCommonName.replace(" ",  "-")
        speciesCommonName = speciesCommonName.replace("'",  "")
        
        sub = Web()
        sub.mdiParent = self.mdiParent
        sub.title = "Audubon: " + speciesCommonName        
        url = ("http://www.audubon.org/field-guide/bird/"
                  + speciesCommonName                
                  )
        sub.LoadWebPage(url)        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()   


    def CreateWebPageForPhotos(self):
        
        speciesScientificName = self.lblScientificName.text()
        speciesCommonName = self.lblCommonName.text()
        
        sub = Web()
        sub.mdiParent = self.mdiParent
        sub.title = "Macaulay Library Photos: " + speciesCommonName        
        url = ("https://search.macaulaylibrary.org/catalog?searchField=species&q="
                  + speciesScientificName.split(" ")[0] 
                  +"+" 
                  + speciesScientificName.split(" ")[1]
                  )
                  
        if speciesScientificName.count(" ") == 2:
            url = url + "%20" + speciesScientificName.split(" ")[2]
                        
        sub.LoadWebPage(url)        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()      


    def CreateWebPageForWikipedia(self):
        
        speciesScientificName = self.lblScientificName.text()
        speciesCommonName = self.lblCommonName.text()

        if "(" in speciesCommonName:
            speciesCommonName = speciesCommonName.split(" (")[0]        

        sub = Web()
        sub.title = "Wikipedia: " + speciesCommonName        
        url = ("https://en.wikipedia.org/wiki/"
                 + speciesScientificName.split(" ")[0] 
                 +"_" 
                 + speciesScientificName.split(" ")[1]
                 )
        sub.LoadWebPage(url)        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show() 


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
            self.lblCommonName.text() + 
            "</H1>"
            )
        
        html = html + (
            "<H2>" + 
            self.lblScientificName.text() + 
            "</H2>"
            )        

        html = html + (
            "<H4>" + 
            self.lblOrderName.text() + 
            "</H4>"
            )               

        html = html + (
            "<H4>" + 
            self.lblFirstSeen.text() + 
            "</H4>"
            )    
    
        html = html + (
            "<H4>" + 
            self.lblMostRecentlySeen.text() + 
            "</H4>"
            )    
            
        html = html + (
            "<br>" +
            "<H4>" + 
            "Locations"
            "</H4>"
            )    

        html=html + (
            "<font size='2'>"
            )
            
        root = self.trLocations.invisibleRootItem()
        for i in range(root.childCount()):
            for ii in range(root.child(i).childCount()):
                for iii in range(root.child(i).child(ii).childCount()):
                    for iv in range(root.child(i).child(ii).child(iii).childCount()):
                        html = html + (
                            "<b>" + 
                            root.child(i).text(0) + ", " + 
                            root.child(i).child(ii).text(0) + ", " + 
                            root.child(i).child(ii).child(iii).text(0) + ", " + 
                            root.child(i).child(ii).child(iii).child(iv).text(0)
                            )
                            
                        filter = Filter()
                        filter.setSpeciesName = self.lblCommonName.text()
                        filter.setLocationType("Location")
                        filter.setLocationName(root.child(i).child(ii).child(iii).child(iv).text(0))            
            
                        dates = MainWindow.db.GetDates(filter)
                        
                        html= html + (
                            " (" + str(len(dates))
                            )
                        
                        if len(dates) > 1:
                            html = html + " dates)"
                        else:
                            html = html + " date)"
                            
                        html = html + (    
                            "</b>"
                            "<br>"                        
                            "<table width='100%'>"
                            "<tr>"
                            )
                            
                        R = 1
                        for d in dates:
                            html = html + (
                                "<td>" +
                                d + 
                                "</td>"
                                )
                            if R == 5:
                                html = html + (
                                    "</tr>"
                                    "<tr>"
                                    )
                                R = 0
                            R = R + 1

                        html= html + (
                            "<br>" +
                            "<br>" +
                            "<br>" +
                            "</table>"
                            )

        html = html + (

            "<font size>" +            
            "</body>" +
            "</html>"
            )
            

        QApplication.restoreOverrideCursor()   
        
        return(html)


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)


    def scaleMe(self):
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  780  * scaleFactor
        windowHeight = 500 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
        #scale the font for all widgets in window
        for w in self.children():
            try:
                w.setFont(QFont("Helvetica", fontSize))
            except:
                pass 
        
        baseFont = QFont(QFont("Helvetica", fontSize))
        commonFont = QFont(QFont("Helvetica", floor(fontSize * 1.4)))
        commonFont.setBold(True)
        scientificFont=  QFont(QFont("Helvetica", floor(fontSize * 1.2)))
        scientificFont.setItalic(True)
        self.lblCommonName.setFont(commonFont)
        self.lblScientificName.setFont(scientificFont)
        self.lblOrderName.setFont(baseFont)

        metrics = self.trDates.fontMetrics()
        textHeight = metrics.boundingRect("2222-22-22").height()            
        textWidth= metrics.boundingRect("2222-22-22").width()  

        self.buttonMacaulay.resize(self.buttonMacaulay.x(), textHeight)
        self.buttonWikipedia.resize(self.buttonMacaulay.x(), textHeight)
        self.buttonAudubon.resize(self.buttonMacaulay.x(), textHeight)
        self.buttonAllAboutBirds.resize(self.buttonMacaulay.x(), textHeight)
        self.buttonChecklists.resize(self.buttonMacaulay.x(), textHeight)
        self.buttonMap.resize(self.buttonMacaulay.x(), textHeight)

        root = self.trLocations.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1))
            for ii in range(root.child(i).childCount()):
                root.child(i).child(ii).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1))
                for iii in range(root.child(i).child(ii).childCount()):
                    root.child(i).child(ii).child(iii).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1)) 
                    for iv in range(root.child(i).child(ii).child(iii).childCount()):
                        root.child(i).child(ii).child(iii).child(iv).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1)) 
        
        root = self.trDates.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1))
            for ii in range(root.child(i).childCount()):
                root.child(i).child(ii).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1))
                for iii in range(root.child(i).child(ii).childCount()):
                    root.child(i).child(ii).child(iii).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1)) 
 
        root = self.trMonthDates.invisibleRootItem()
        for i in range(root.childCount()):
            root.child(i).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1))
            for ii in range(root.child(i).childCount()):
                root.child(i).child(ii).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1))
                for iii in range(root.child(i).child(ii).childCount()):
                    root.child(i).child(ii).child(iii).setSizeHint(0, QSize(textWidth * 1.1, textHeight * 1.1)) 

        metrics = self.tblYearLocations.fontMetrics()
        textHeight = metrics.boundingRect("A").height()            
        for r in range(self.tblYearLocations.rowCount()):
            self.tblYearLocations.setRowHeight(r, textHeight * 1.1)
        for r in range(self.tblMonthLocations.rowCount()):
            self.tblMonthLocations.setRowHeight(r, textHeight * 1.1)            
            
            
class Location(QMdiSubWindow, Location.Ui_frmLocation):
    
    resized = pyqtSignal()    
    
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""        
        self.resized.connect(self.resizeMe)                      
        self.tblDates.currentItemChanged.connect(self.FillSpeciesForDate)
        self.lstSpecies.doubleClicked.connect(self.ClickedLstSpecies)       
        self.tblDates.doubleClicked.connect(self.ClickedTblDates)               
        self.tblSpecies.doubleClicked.connect(self.ClickedTblSpecies)               
        self.tblDates.setShowGrid(False)
        
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.horizontalLayout_2.setSpacing(4)
        self.webMap = QWebEngineView(self.tabMap)
        self.webMap.setUrl(QUrl("about:blank"))
        self.webMap.setObjectName("webMap")
        self.horizontalLayout_2.addWidget(self.webMap)  
        self.tabLocation.setCurrentIndex(0)
        
        self.scaleMe()
        self.resizeMe()


    def ClickedLstSpecies(self):
        species = self.lstSpecies.currentItem().text()
        self.CreateIndividual(species)


    def ClickedTblDates(self):
        thisDate = self.tblDates.item(self.tblDates.currentRow(),  1).text()
        thisLocation = self.lblLocation.text()
        
        tempFilter = Filter()
        
        tempFilter.setLocationType("Location")
        tempFilter.setLocationName(thisLocation)
        tempFilter.setStartDate(thisDate)
        tempFilter.setEndDate(thisDate)
        
        self.CreateSpeciesList(tempFilter)


    def ClickedTblSpecies(self):

        selectedRow = self.tblSpecies.currentRow()
        selectedColumn = self.tblSpecies.currentColumn()        

        if selectedColumn > 1:
            thisDate = self.tblSpecies.item(selectedRow, selectedColumn).text()
            thisLocation = self.lblLocation.text()
            
            tempFilter = Filter()

            tempFilter.setLocationType("Location")
            tempFilter.setLocationName(thisLocation)
            tempFilter.setStartDate(thisDate)
            tempFilter.setEndDate(thisDate)

            self.CreateSpeciesList(tempFilter)
        
        else:
            thisSpecies = self.tblSpecies.item(selectedRow,  1).text()
            self.CreateIndividual(thisSpecies)


    def CreateIndividual(self,  species):
        sub = Individual()
        sub.mdiParent = self.mdiParent
        sub.FillIndividual(species)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()
        sub.resizeMe()


    def CreateSpeciesList(self,  filter):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        sub = Lists()
        sub.FillSpecies(filter)
        sub.mdiParent = self.mdiParent
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow( sub, self)        
        sub.show() 
        
        QApplication.restoreOverrideCursor()  


    def FillLocation(self, location):
        thisLocationDates= []
        
        filter = Filter()
        filter.setLocationType("Location")
        filter.setLocationName(location)
        
        thisLocationDates = MainWindow.db.GetDates(filter)
        thisLocationDates.sort()
        
        self.tblDates.setColumnCount(4)       
        self.tblDates.setRowCount(len(thisLocationDates))        
        self.tblDates.horizontalHeader().setVisible(True)
        self.tblDates.setHorizontalHeaderLabels(['Rank', 'Date', 'Species', 'Checklists'])
        header = self.tblDates.horizontalHeader()
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.lblLocation.setText(location)
        self.lblFirstVisited.setText("First visited: " + thisLocationDates[0])
        self.lblMostRecentlyVisited.setText("Most recently visited: " + thisLocationDates[len(thisLocationDates)-1])
        
        dateArray = []
        for d in thisLocationDates:
            if d != "":
                dSpecies = set()
                checklistCount = set()
                for sighting in MainWindow.db.locationDict[location]:
                    if d == sighting[10]:
                        dSpecies.add(sighting[1])
                        checklistCount.add(sighting[0])
                dateArray.append([len(dSpecies),  d, len(checklistCount)])
        dateArray.sort(reverse=True)
        
        rank = 0
        lastDateTotal = 0
        R = 0
        for date in dateArray:            
            rankItem = QTableWidgetItem()
            if date[0] != lastDateTotal:
                rank = R + 1
            rankItem.setData(Qt.DisplayRole, rank)
            dateItem = QTableWidgetItem()
            dateItem.setText(date[1])
            totalSpeciesItem = QTableWidgetItem()
            totalSpeciesItem.setData(Qt.DisplayRole, date[0])
            totalChecklistsItem = QTableWidgetItem()
            totalChecklistsItem.setData(Qt.DisplayRole, date[2])
            self.tblDates.setItem(R, 0, rankItem)  
            self.tblDates.setItem(R, 1, dateItem)
            self.tblDates.setItem(R, 2, totalSpeciesItem)
            self.tblDates.setItem(R, 3, totalChecklistsItem)
            lastDateTotal = date[0]
            R = R + 1
        
        self.tblDates.selectRow(0)
        
        if self.tblDates.rowCount() == 1:
            self.lblDatesSeen.setText("Date (1)")
        else:
            self.lblDatesSeen.setText("Dates (" + str(self.tblDates.rowCount()) + ")")
        # display all dates for the selected location
        self.tblDates.setSortingEnabled(True)
        self.tblDates.sortItems(0,0)
        self.tblDates.setCurrentCell(0, 1)
            
        coordinates = MainWindow.db.GetLocationCoordinates(location)

        # display the species in the species for date list
        self.FillSpeciesForDate()
        # display the main all-species list
        self.FillSpecies()
        # display the Google map
        self.FillMap(coordinates)
        
        self.scaleMe()
        self.resizeMe()


    def FillMap(self,  coordinates):
        
        # assemble html and javascript to pass to Google Maps
        # using a simple URL would not let us have a clean map without the Google search bar, etc.
        
        html = """<!DOCTYPE html>
                            <html>
                              <head>
                                <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
                                <meta charset="utf-8">
                                <title>Location Map</title>
                                <style>"""
        # we need to add the # character here, so escape it with quotes
        html = html + '#' 
        html = html + """map {
                                    height: 100%;
                                  }
                                  html, body {
                                    height: 100%;
                                    margin: 0;
                                    padding: 0;
                                  }
                                </style>
                              </head>
                              <body>
                                <div id="map"></div>
                                <script>
                                  function initMap() {
                                  
                                    var markerLatLng = {lat: """
                                    
        # set the coordinates for the marker
        html = html + coordinates[0] + ",  lng: " + coordinates[1] + "};"
        html = html + """       

                                    var myLatLngCenter = {lat: """
                                    
        # set the coordinates for the map center 
        #(we adjust because it doesn't seem to center accurately otherwise)
        # we increase the latitude and decrease the longitude to get the correct center
#        html = html + str(float(coordinates[0]) + .02442906) +  ",  lng: " + str(float(coordinates[1]) - .0642) + "};"
        html = html + str(float(coordinates[0])) +  ",  lng: " + str(float(coordinates[1])) + "};"
        html = html + """       
                
                                    var map = new google.maps.Map(document.getElementById('map'), {
                                      zoom: 13,
                                      center: myLatLngCenter
                                    });
                                    var marker = new google.maps.Marker({
                                      position: markerLatLng,
                                      map: map,
                                      title: 'eBird Location!'
                                    });
                                  }
                                </script>
                                <script async defer
                                src="https://maps.googleapis.com/maps/api/js?key="""
                                
        # add the Google Maps API key unique to this project
        html = html + "AIzaSyDjVuwWvZmRlD5n-Jj2Jh_76njXxldDgug"
        
        html = html +"""&callback=initMap">
                                </script>
                              </body>
                            </html>"""
        # pass the html we created to the QWebView widget for display                    
        self.webMap.setHtml(html)


    def FillSpecies(self): 
        location = self.lblLocation.text()
        tempFilter = Filter()
        tempFilter.setLocationType("Location")
        tempFilter.setLocationName(location)
        speciesList = []
       
        # get species data from db 
        thisWindowList = MainWindow.db.GetSpeciesWithData(tempFilter)
       
       # set up tblSpecies column headers and widths
        self.tblSpecies.setColumnCount(6)
        self.tblSpecies.setRowCount(len(thisWindowList)+1)
        self.tblSpecies.horizontalHeader().setVisible(True)
        self.tblSpecies.setHorizontalHeaderLabels(['Tax', 'Species', 'First',  'Last', 'Chlists', '% of Chlists'])
        header = self.tblSpecies.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tblSpecies.setShowGrid(False)

        # add species and dates to table row by row        
        R = 1
        for species in thisWindowList:    
            taxItem = QTableWidgetItem()
            taxItem.setData(Qt.DisplayRole, R)
            speciesItem = QTableWidgetItem()
            speciesItem.setText(species[0])
            firstItem = QTableWidgetItem()
            firstItem.setData(Qt.DisplayRole, species[1])
            lastItem = QTableWidgetItem()
            lastItem.setData(Qt.DisplayRole, species[2])
            checklistsItem = QTableWidgetItem()
            checklistsItem.setData(Qt.DisplayRole, species[5])
            percentageItem = QTableWidgetItem()
            percentageItem.setData(Qt.DisplayRole, species[6])
            
            self.tblSpecies.setItem(R, 0, taxItem)    
            self.tblSpecies.setItem(R, 1, speciesItem)
            self.tblSpecies.setItem(R, 2, firstItem)
            self.tblSpecies.setItem(R, 3, lastItem)
            self.tblSpecies.setItem(R, 4, checklistsItem)
            self.tblSpecies.setItem(R, 5, percentageItem)
            
            speciesList.append(species[0])
            R = R + 1
            
        self.tblSpecies.removeRow(0)
        
        count = MainWindow.db.CountSpecies(speciesList)
        self.lblSpecies.setText("Species (" + str(count) + "):")
        

    def SetDate(self,  date):
        if self.tblDates.rowCount() > 0:
            for d in range(self.tblDates.rowCount()):
                if self.tblDates.item(d,  1).text() == date:
                    self.tblDates.setCurrentCell(d,  1)
                    self.FillSpeciesForDate()
                    self.tabLocation.setCurrentIndex(1)
                    break


    def FillSpeciesForDate(self):
        self.lstSpecies.clear()
        location = self.lblLocation.text()
        if self.tblDates.item(self.tblDates.currentRow(),  1) is not None:
            
            date = self.tblDates.item(self.tblDates.currentRow(),  1).text()      

            tempFilter = Filter()
            tempFilter.setStartDate(date)
            tempFilter.setEndDate(date)
            tempFilter.setLocationName(location)
            tempFilter.setLocationType("Location")

            species = MainWindow.db.GetSpecies(tempFilter)

            self.lstSpecies.addItems(species)
            self.lstSpecies.setCurrentRow(0)
            self.lstSpecies.setSpacing(2)
            
            count = MainWindow.db.CountSpecies(species)
            
            self.lblSpeciesSeen.setText("Species for selected date (" + str(count) + ")")


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
            self.lblFirstVisited.text() + 
            "</H3>"
            )        

        html = html + (
            "<H3>" + 
            self.lblMostRecentlyVisited.text() + 
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
            "Species"
            "</H4>"
            )    

        html=html + (
            "<font size='2'>" +
            "<p>"
            )
       
        # loopthrough the species listed in tblSpecies
        for r in range(self.tblSpecies.rowCount()):
            html= html + (
                self.tblSpecies.item(r, 1).text()
                + "<br>"
                )

        html= html + (
            "<H4>" +
            "Dates" +
            "</H4>"
            )
 
        # create filter set to our current location
        filter = Filter()
        filter.setLocationType = "Location"
        filter.setLocationName =  self.lblLocation.text()

        # for each date in tblDates, find the species and display them in a table
        for r in range(self.tblDates.rowCount()):

            html= html + (
                "<b>" +
                self.tblDates.item(r, 1).text() +
                "</b>"
                )    

            filter.setStartDate(self.tblDates.item(r, 1).text())
            filter.setEndDate(self.tblDates.item(r, 1).text())
            species = MainWindow.db.GetSpecies(filter)

            html = html + (    
                "<br>"                        
                "<table width='100%'>"
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
                        "</tr>"
                        "<tr>"
                        )
                    R = 0
                R = R + 1

            html= html + (
                "<br>" +
                "<br>" +
                "<br>" +
                "</table>"
                )

        html = html + (
            "<font size>" +            
            "</body>" +
            "</html>"
            )
        
        QApplication.restoreOverrideCursor()   
        
        return(html)


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)


    def scaleMe(self):
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  780  * scaleFactor
        windowHeight = 500 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
        #scale the font for all widgets in window
        for w in self.children():
            try:
                w.setFont(QFont("Helvetica", fontSize))
            except:
                pass 
        
        baseFont = QFont(QFont("Helvetica", fontSize))
        locationFont = QFont(QFont("Helvetica", floor(fontSize * 1.4)))
        locationFont.setBold(True)
        self.lblLocation.setFont(locationFont)
        self.lblFirstVisited.setFont(baseFont)
        self.lblMostRecentlyVisited.setFont(baseFont)

        header = self.tblSpecies.horizontalHeader()
        metrics = self.tblSpecies.fontMetrics()

        dateTextWidth = metrics.boundingRect("2222-22-22").width()
        dateTextHeight = metrics.boundingRect("2222-22-22").height()
        taxText = str(self.tblSpecies.rowCount())
        taxTextWidth = metrics.boundingRect(taxText).width()
        header.resizeSection(0,  floor(1.7 * taxTextWidth))
        header.resizeSection(2,  floor(1.3 * dateTextWidth))
        header.resizeSection(3,  floor(1.3 * dateTextWidth))                
        for R in range(self.tblSpecies.rowCount()):
            self.tblSpecies.setRowHeight(R, dateTextHeight)

        header = self.tblDates.horizontalHeader()         
        textWidth = metrics.boundingRect("Rank").width()
        header.resizeSection(0,  floor(1.5 * textWidth))
        header.resizeSection(1,  floor(1.5 * dateTextWidth))
        for R in range(self.tblDates.rowCount()):
            self.tblDates.setRowHeight(R, dateTextHeight)
        

class LocationTotals(QMdiSubWindow, LocationTotals.Ui_frmLocationTotals):

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
        self.filter = Filter()
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
            locationName = MainWindow.db.GetCountryCode(self.tblCountryTotals.item(self.tblCountryTotals.currentRow(),  1).text())
        if locationType == "State":
            locationName = MainWindow.db.GetStateCode(self.tblStateTotals.item(self.tblStateTotals.currentRow(),  1).text())
        if locationType == "County":
            locationName = self.tblCountyTotals.item(self.tblCountyTotals.currentRow(),  1).text()
        if locationType == "Location":
            locationName = self.tblLocationTotals.item(self.tblLocationTotals.currentRow(),  1).text()
        
        sub = Lists()        
        tempFilter.setLocationType(locationType)
        tempFilter.setLocationName(locationName)
        
        if self.focusWidget().currentColumn() in [0, 1, 2]:
            sub.FillSpecies(tempFilter)

        if self.focusWidget().currentColumn() == 3:
            sub.FillChecklists(tempFilter)

        sub.mdiParent = self.mdiParent
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
        
        minimalSightingList = MainWindow.db.GetMinimalFilteredSightingsList(filter)
        
        for s in minimalSightingList:
            
            # Consider only full species, not slash or spuh entries
            if ("/" not in s[1]) and ("sp." not in s[1]):
                
                if MainWindow.db.TestSighting(s,  filter) is True:
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
            countryItem.setText(MainWindow.db.GetCountryName(country[1]))
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
            stateItem.setText(MainWindow.db.GetStateName(state[1]))
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
        MainWindow.SetChildDetailsLabels(self,  self,  self.filter)

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
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  600  * scaleFactor
        windowHeight = 580 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
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
            


class Compare(QMdiSubWindow, Compare.Ui_frmCompare):

    # create "resized" as a signal that the window can emit
    # we respond to this signal with the form's resizeMe method below
    resized = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""
        self.resized.connect(self.resizeMe)                      
        self.btnCompare.clicked.connect(self.CompareLists)
        self.lstLeftOnly.itemDoubleClicked.connect(self.ListLeftClicked)
        self.lstRightOnly.itemDoubleClicked.connect(self.ListRightClicked)
        self.lstBoth.itemDoubleClicked.connect(self.ListBothClicked)
        self.webView = QWebEngineView()
        self.myPrinter = QPrinter(QPrinter.HighResolution)
        
        self.scaleMe()
        self.resizeMe()


    def html(self):
    
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
            
        html = html + """
            <H1>  
            List Comparison  
            </H1>
            """
        
        html = html + (
            "<H2>" + 
            "Species only on " + self.cboListsLeft.currentText() + 
            "</H2>"
            )        

        html=html + (
            "<font size='2'>"
            )
        
        for r in range(self.lstLeftOnly.count()):
            html = html + (
                "<br>" +
                self.lstLeftOnly.item(r).text() +
                "</br>"
                )
        
        html=html + (
            "</font size='2'>"
            )
        
        html = html + (
            "<H2>" + 
            "Species only on " + self.cboListsRight.currentText() + 
            "</H2>"
            )        

        html=html + (
            "<font size='2'>"
            )
            
        # add family names and the species under them
        
        for r in range(self.lstRightOnly.count()):
            html = html + (
                "<br>" +
                self.lstRightOnly.item(r).text() +
                "</br>"
                )
        
        html=html + (
            "</font size='2'>"
            )        
        
        html = html + """
            <H2>  
            Species on Both Lists  
            </H2>
            """    

        html=html + (
            "<font size='2'>"
            )
                    
        for r in range(self.lstBoth.count()):
            html = html + (
                "<br>" +                
                self.lstBoth.item(r).text() +
                "</br>"
                )
        
        html=html + (
            "</font size='2'>"
            )        
             
        html = html + """
            <font size>           
            </body>
            </html>
            """
        return(html)


    def ListLeftClicked(self):
        self.CreateNewIndividual(self.lstLeftOnly.currentItem().text())


    def ListRightClicked(self):
        self.CreateNewIndividual(self.lstRightOnly.currentItem().text())


    def ListBothClicked(self):
        self.CreateNewIndividual(self.lstBoth.currentItem().text())        


    def FillListChoices(self): 
        self.lstLeftOnly.clear()
        self.lstRightOnly.clear()
        self.lstBoth.clear()
        self.cboListsLeft.clear()
        self.cboListsRight.clear()
        thisWindowList = []
        for window in self.mdiParent.mdiArea.subWindowList():        
            if window.objectName() == "frmSpeciesList":
                if window.isVisible() == True:
                    thisWindowList.append(window.windowTitle())
        thisWindowList.sort()
        self.cboListsLeft.addItems(thisWindowList)
        self.cboListsRight.addItems(thisWindowList)
        
        if len(thisWindowList) < 2:
            return(False)
        else:
            return(True)
              
    def CompareLists(self):
        self.lstLeftOnly.clear()
        self.lstBoth.clear()
        self.lstRightOnly.clear()
        
        # get left list species
        leftListSpecies = []
        leftTitle = self.cboListsLeft.currentText()
        for window in self.mdiParent.mdiArea.subWindowList():        
            if window.objectName() == "frmSpeciesList":
                if window.windowTitle() == leftTitle:
                    for s in window.currentSpeciesList:
                        if "(" in s:
                            s = s.split(" (")[0]
                        leftListSpecies.append(s)
                        
        # get right list species
        rightListSpecies = []
        rightTitle = self.cboListsRight.currentText()
        for window in self.mdiParent.mdiArea.subWindowList():        
            if window.objectName() == "frmSpeciesList":
                if window.windowTitle() == rightTitle:
                    for s in window.currentSpeciesList:
                        if "(" in s:
                            s = s.split(" (")[0]
                        rightListSpecies.append(s)
        
        bothLists = []
        leftListOnly = []
        rightListOnly = []
        
        for ls in leftListSpecies:
          
            if ls in rightListSpecies:
                if ls not in bothLists:
                    bothLists.append(ls)
            
            else:
                
                if ls not in leftListOnly:
                    leftListOnly.append(ls)
        
        for rs in rightListSpecies:
          
            if rs in leftListSpecies:
                
                if rs not in bothLists:
                    bothLists.append(rs)
            
            else:
                
                if rs not in rightListOnly:
                    rightListOnly.append(rs)
                    
        self.lstLeftOnly.addItems(leftListOnly)
        self.lstLeftOnly.setSpacing(2)
        self.lstBoth.addItems(bothLists)
        self.lstBoth.setSpacing(2)
        self.lstRightOnly.addItems(rightListOnly)
        self.lstRightOnly.setSpacing(2)        
        self.lblLeftListOnly.setText("Species only on This List (" + str(self.lstLeftOnly.count())+")")
        self.lblBothLists.setText("Species on Both Lists (" + str(self.lstBoth.count()) + ")")
        self.lblRightListOnly.setText("Species only on This List (" + str(self.lstRightOnly.count()) + ")")
        
        
    def CreateNewIndividual(self,  speciesName):      
        sub = Individual()
        sub.mdiParent = self.mdiParent
        sub.FillIndividual(speciesName)
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()
        sub.resizeMe()


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
        
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth -10 , windowHeight-35)
   
   
    def scaleMe(self):
               
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  800  * scaleFactor
        windowHeight = 500 * scaleFactor            
        self.resize(windowWidth, windowHeight)
        
        fontSize = MainWindow.fontSize
        scaleFactor = MainWindow.scaleFactor     
        #scale the font for all widgets in window
        for w in self.children():
            try:
                w.setFont(QFont("Helvetica", fontSize))
            except:
                pass        


class Web(QMdiSubWindow, Web.Ui_frmWeb):
    
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
        
        self.scaleMe()
        self.resizeMe()


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
       
        fontSize = MainWindow.fontSize
        settings = QWebEngineSettings.globalSettings()
        settings.setFontSize(QWebEngineSettings.DefaultFontSize, floor(fontSize * 1.6))        
        
        scaleFactor = MainWindow.scaleFactor
        windowWidth =  900 * scaleFactor
        windowHeight = 600 * scaleFactor            
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
            <body bgcolor="#98FB98">
            <h1>
            Lapwing
            </h1>
            """
        
        html = html + "<h3>Version: " + MainWindow.versionNumber + "</h3>"
        html = html + "<h3>Date: " + MainWindow.versionDate+ "</h3>"
        
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
            Qt, by the Qt Company, is licensed under the (L)GPL Lesser General Public License.
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
        
        locations = MainWindow.db.GetLocations(filter)
        
        if len(locations) == 0:
            return(False)
        
        for l in locations:
            coordinates = MainWindow.db.GetLocationCoordinates(l)
            coordinatesDict[l] = coordinates
            
        html = """

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
        html = html + "height: " + str(mapHeight) + "px;"
        html = html + "width: " + str(mapWidth)  + "px;"
            
        html = html + """
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
            html = html + """
                var marker = new google.maps.Marker({
                """
            html = html + "position: {lat: " + coordinatesDict[c][0] + ", lng: " + coordinatesDict[c][1] + "},"
            
            html = html + """
                    map: map,
                    title: """
            html = html + '"' + c + '"'
            html = html + """
                    }); 
                bounds.extend(marker.getPosition());                    
                
            """    
        html = html + """
            
                map.setCenter(bounds.getCenter());
                
                map.fitBounds(bounds);
            }
            
            </script>
            <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyDjVuwWvZmRlD5n-Jj2Jh_76njXxldDgug&callback=initMap" async defer></script>
            </body>
            </html>        
            """
        
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
                locationName = MainWindow.db.GetCountryName(locationName)
            if locationType == "State":
                locationName = MainWindow.db.GetStateName(locationName)
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
       
        icon = QIcon()
        icon.addPixmap(QPixmap(":/icon_map.png"), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon) 
        
        return(True)


    def showLoadProgress(self, percent):
        
        if percent < 100:
            self.setWindowTitle(self.title + ": " + str(percent) + "%")
        else:
            self.setWindowTitle(self.title)


class Find(QMdiSubWindow, Find.Ui_frmFind):
    
    resized = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.mdiParent = ""
        self.resized.connect(self.resizeMe)    
        self.btnFind.clicked.connect(self.CreateFindResults)
        self.btnCancel.clicked.connect(self.Cancel)
      
        self.txtFind.setFocus()
        
        self.scaleMe()
        self.resizeMe()


    def CreateFindResults(self):

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        
        #The user has accepted the has clicked OK
        searchString = self.txtFind.text()
        
        # get names of which checkboxes are checked
        checkedBoxes = []
        for c in ([
            self.chkCommonName, 
            self.chkScientificName,
            self.chkCountryName,
            self.chkStateName,
            self.chkCountyName,
            self.chkLocationName,
            self.chkSpeciesComments,
            self.chkChecklistComments
            ]):
            if c.isChecked() is True:
                checkedBoxes.append(c.objectName())
                
        # get search results
        found = MainWindow.db.GetFindResults(searchString, checkedBoxes)
    
        # create child window 
        sub = Lists()
        
        # save the MDI window as the parent for future use in the child
        sub.mdiParent = self.mdiParent
        
        # call the child's fill routine, passing the filter settings list
        sub.FillFindChecklists(found)
        
        self.parent().parent().addSubWindow(sub)
        self.mdiParent.PositionChildWindow(sub, self)        
        sub.show()  

        QApplication.restoreOverrideCursor()   
        
        # close the Find child
        self.close()


    def Cancel(self):
        
        self.close()


    def resizeEvent(self, event):
        #routine to handle events on objects, like clicks, lost focus, gained forcus, etc.        
        self.resized.emit()
        return super(self.__class__, self).resizeEvent(event)
        
            
    def resizeMe(self):

        windowWidth =  self.frameGeometry().width()
        windowHeight = self.frameGeometry().height()
        self.scrollArea.setGeometry(5, 27, windowWidth - 10, windowHeight - 32)

   
    def scaleMe(self):
       
        metrics = self.txtFind.fontMetrics()
        textHeight = metrics.boundingRect("ABCD").height()          
        
        self.txtFind.resize(self.txtFind.x(), textHeight)
        self.lblFind.resize(self.txtFind.x(), textHeight)
       
        fontSize = MainWindow.fontSize
        for c in ([
            self.chkCommonName, 
            self.chkScientificName,
            self.chkCountryName,
            self.chkStateName,
            self.chkCountyName,
            self.chkLocationName,
            self.chkSpeciesComments,
            self.chkChecklistComments
            ]):
            c.setFont(QFont("Helvetica", fontSize))  
            c.resize(c.x(), textHeight * 1.1)

        scaleFactor = MainWindow.scaleFactor
        windowWidth =  400 * scaleFactor
        windowHeight = 300 * scaleFactor            
        self.resize(windowWidth, windowHeight)

        baseFont = QFont(QFont("Helvetica", fontSize))
        self.lblFind.setFont(baseFont)
        self.lblWhatToSearch.setFont(baseFont)
        self.txtFind.setFont(baseFont)

        metrics = self.txtFind.fontMetrics()
        textHeight = metrics.boundingRect("2222-22-22").height()          
        
        self.txtFind.resize(self.txtFind.x(), textHeight)
        self.lblFind.resize(self.txtFind.x(), textHeight)
        
                    
class Filter():
    locationType = ""                    # str   choices are Country, County, State, Location, or ""
    locationName = ""                  # str   name of region or location  or ""
    startDate = ""                           # str   format yyyy-mm-dd  or ""
    endDate = ""                             # str   format yyyy-mm-dd  or ""
    startSeasonalMonth = ""      # str   format mm
    startSeasonalDay = ""            # str   format dd
    endSeasonalMonth  = ""       # str   format  mm
    endSeasonalDay  = ""             # str   format dd
    checklistID = ""                         # str   number taken from main sightings CSV file
    speciesName = ""                     # str    species name
    speciesList = []                          # list of species names      
    family = ""                                   #str  family name
    time = ""                                       #str  format HH:MM in 24-hour format
    order = ""                                  #str order name
        
        
    def setLocationType(self,  locationType):
        self.locationType = locationType


    def getLocationType(self):
        return(self.locationType)


    def setLocationName(self,  locationName):
        self.locationName = locationName


    def getLocationName(self):
        return(self.locationName)        

        
    def setStartDate(self,  startDate):
        self.startDate = startDate


    def getStartDate(self):
        return(self.startDate)  


    def setEndDate(self,  endDate):
        self.endDate = endDate


    def getEndDate(self):
        return(self.endDate)   


    def setStartSeasonalMonth(self,  startSeasonalMonth):
        self.startSeasonalMonth = startSeasonalMonth


    def getStartSeasonalMonth(self):
        return(self.startSeasonalMonth)               

        
    def setEndSeasonalMonth(self,  endSeasonalMonth):
        self.endSeasonalMonth = endSeasonalMonth


    def getEndSeasonalMonth(self):
        return(self.endSeasonalMonth)

  
    def setStartSeasonalDay(self,  startSeasonalDay):
        self.startSeasonalDay = startSeasonalDay


    def getStartSeasonalDay(self):
        return(self.startSeasonalDay)


    def setEndSeasonalDay(self,  endSeasonalDay):
        self.endSeasonalDay = endSeasonalDay


    def getEndSeasonalDay(self):
        return(self.endSeasonalDay)

 
    def setChecklistID(self,  checklistID):
        self.checklistID = checklistID


    def getChecklistID(self):
        return(self.checklistID)        


    def setSpeciesName(self,  speciesName):
        self.speciesName = speciesName


    def getSpeciesName(self):
        return(self.speciesName)       


    def setSpeciesList(self,  speciesList):
        self.speciesList = speciesList


    def getSpeciesList(self):
        return(self.speciesList)           

    
    def setFamily(self,  family):
        self.family = family


    def getOrder(self):
        return(self.order)        


    def setOrder(self, order):
        self.order = order


    def getFamily(self):
        return(self.family)  

        
    def setTime(self,  time):
        self.time = time

    
    def getTime(self):
        return(self.time)

    
    def debugAll(self):
        returnString = (
            "locationType: " + self.locationType + '   ' +
            "locationName: " + self.locationName + "   " +
            "startDate: " + self.startDate + "   " +
            "endDate: " + self.endDate + "   " +
            "startSeasonalMonth: " + self.startSeasonalMonth + "   " +
            "startSeasonalDay: " + self.startSeasonalDay + "   " +
            "endSeasonalMonth: " + self.endSeasonalMonth + "   " +
            "endSeasonalDay: " + self.endSeasonalDay + "   " +
            "checklistID: " + self.checklistID + "   " +
            "speciesName: " + self.speciesName + "   " +
            "family:" +self.family + "   " + 
            "speciesList:"
            )
        return(returnString,  self.speciesList)
            
class FloatDelegate(QItemDelegate):
    
    def __init__(self, decimals, parent=None):
        QItemDelegate.__init__(self, parent=parent)
        self.nDecimals = decimals

    def paint(self, painter, option, index):
        value = index.model().data(index, Qt.EditRole)
        try:
            number = float(value)        
            painter.drawText(option.rect, Qt.AlignCenter, "{:.{}f}".format(number, self.nDecimals))
        except :
            QItemDelegate.paint(self, painter, option, index)            

           
def main():
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create( "Fusion"))    
    form = MainWindow()
    form.show()                     
    app.exec_()                         


if __name__ == '__main__':              
    main()                              
