from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QMainWindow, QCheckBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys

from Donnees import Donnees
from styles import FIELD_LABEL_STYLE


class ProduitWidget(QWidget):

    def __init__(self, name : str, list_prod_checked : list):
        super().__init__()

        self.nomProduit = name

        self.setFixedSize(100, 100)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet("""
                            color: #000000;
                            font-weight: bold;
                            font-size: 12px;
                            
                            """)
      
        image = QLabel()
        pixmap = QPixmap("./Images/" + name + ".png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        image.setPixmap(pixmap)
        image.setFixedSize(60, 40)

        label = QLabel(name)
        checkbox = QCheckBox()
        checkbox.stateChanged.connect(self.retourCheck)
        checkbox.setFixedSize(20, 20)

        self.list_elt_checked = list_prod_checked

        line = QHBoxLayout()
        line.addWidget(label)
        line.addWidget(checkbox)
        layout.addWidget(image)
        layout.addLayout(line)
        self.checkbox = checkbox
        self.setLayout(layout)


        self.show()
        
    def retourCheck(self, etat) -> str:
        if etat == 2 : self.list_elt_checked.append(self.nomProduit)
        else : self.list_elt_checked.remove(self.nomProduit)
        print(self.list_elt_checked)
        


if __name__ == '__main__' :
    
    
    app : QApplication = QApplication(sys.argv)

    data = Donnees()
    
    f : ProduitWidget = ProduitWidget("Ail", data.list_prod_checked)
    f2 : ProduitWidget = ProduitWidget("Champignon", data.list_prod_checked)

    app.exit(app.exec())

    print(data.list_prod_checked)