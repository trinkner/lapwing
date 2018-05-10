# import the GUI forms that we create with Qt Creator
import code_DataBase
import code_BigReport
import code_Filter
import code_Find 
import code_Lists
import code_Web
import code_Families
import code_Compare
import code_LocationTotals
import code_DateTotals
import form_MDIMain

# import basic Python libraries
import sys
import os
import subprocess
import datetime

from math import (
    floor, 
    modf
    )

# import the Qt components we'll use
# do this so later we won't have to clutter our code with references to parent Qt classes 

from PyQt5.QtGui import (
    QCursor,
    QFont,
    QTextDocument
    )
    
from PyQt5.QtCore import (
    Qt,
    QDate
    )
    
from PyQt5.QtWidgets import (
    QApplication, 
    QMessageBox, 
    QMainWindow,
    QFileDialog,
    QSlider,
    QLabel,
    )

from PyQt5.QtPrintSupport import (
    QPrintDialog, 
    QPrinter
    )

class MainWindow(QMainWindow, form_MDIMain.Ui_MainWindow):

    # initialize main database that will be used throughout program
    db = code_DataBase.DataBase()
    fontSize = 11
    scaleFactor = 1
    versionNumber = "0.1"
    versionDate = "May 10, 2018"    

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
        
        sub = code_Find.Find()
        
        # save the MDI window as the parent for future use in the child            
        sub.mdiParent = self
        
        # add and position the child to our MDI area        
        self.mdiArea.addSubWindow(sub)
        sub.setGeometry(self.dckFilter.width() * 2, self.dckFilter.height() * .25, sub.width(), sub.height())
        
        sub.scaleMe()
        sub.resizeMe()
        
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
        sub = code_BigReport.BigReport()
        
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
        sub = code_Lists.Lists()
        
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
        sub = code_Lists.Lists()
        
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
        sub = code_LocationTotals.LocationTotals()

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
        
        sub = code_Web.Web()

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
        sub = code_Web.Web()

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
        sub = code_DateTotals.DateTotals()

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
        sub = code_Families.Families()
        
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
            sub.scaleMe()
            sub.resizeMe()
            
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
        sub = code_Compare.Compare()
        
        # save the MDI window as the parent for future use in the child
        sub.mdiParent = self

        # call the child's routine to fill it with data
        if sub.FillListChoices() is True:

            # add and position the child to our MDI area        
            self.mdiArea.addSubWindow(sub)
            self.PositionChildWindow(sub,  self)
            sub.scaleMe()
            sub.resizeMe()
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
        sub = code_Lists.Lists()
        
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
        newFilter = code_Filter.Filter()
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
                if self.cboOrders.currentText() == "**All Orders**":
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
        
