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
