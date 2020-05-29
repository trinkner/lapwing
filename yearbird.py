import code_MainWindow 
import sys
 
from PyQt5.QtWidgets import (
    QApplication, 
    QStyleFactory,
    )

def main():
    app = QApplication(sys.argv)
    
    app.setStyle(QStyleFactory.create( "Fusion"))    
    
    form = code_MainWindow.MainWindow()
    form.show()

    form.processPreferences()
            
    app.exec_()
 

if __name__ == '__main__':              
    main()                              
