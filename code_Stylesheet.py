from PyQt5.QtGui import QColor 

baseColor = "rgb(225, 225, 225)"
tableColor = "rgb(240, 240, 240)"
mdiAreaColor = QColor(67, 129, 168)
textColor = "black"
speciesColor = QColor(12, 114, 179)

stylesheetBase = (
    "QWidget {" +
    "background:" + baseColor + ";" +
    "color:" + textColor + ";" +
    "}"

    "QTableWidget {" +
    "background:" + tableColor + ";" +
    "color:" + textColor + ";" +
    "}"

    "QListWidget {" +
    "background:" + tableColor + ";" +
    "color:" + textColor + ";" +
    "}"

    "QLineEdit {" +
    "background:" + tableColor + ";" +
    "color:" + textColor + ";" +
    "}"

    "QPlainTextEdit {" +
    "background:" + tableColor + ";" +
    "color:" + textColor + ";" +
    "}"
    )
# 
#     QComboBox {
#         border: 2px;
#         outline: 2px;
#         border-radius: 2px;
#         padding: 1px 18px 1px 3px;
#         min-width: 3em;
#         color: rgb(223, 228, 235)
#     }            
# 
#     QListWidget:item:selected {
#         background: rgb(56,114,189)
#     }
# 
#     QListWidget:item:!active {
#         color: silver
#     }
# 
#     QPushButton {
#         background-color: rgb(80,80,80);
#         border-radius: 1px;
#         padding: 5px;
#         min-width: 5em;
#         outline: 1px
#     }
#     """