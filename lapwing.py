# import the GUI forms that we create with Qt Creator
import code_MainWindow 

# import basic Python libraries
import sys

from PyQt5.QtWidgets import (
    QApplication, 
    QStyleFactory    
    )
    

def main():
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create( "Fusion"))    
    form = code_MainWindow.MainWindow()
    form.show()                     
    app.exec_()                         


if __name__ == '__main__':              
    main()                              
