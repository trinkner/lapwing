# import basic Python libraries
import os
import csv
import zipfile
import io
from copy import deepcopy
from collections import defaultdict

from PyQt5.QtWidgets import (
    QApplication, 
    QMessageBox
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
            speciesCount = self.CountSpecies(checklistSpecies)
            
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
