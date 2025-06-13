from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QMainWindow, QCheckBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys

class ProduitWidget(QWidget):

    def __init__(self, nomProduit : str, liste_element_checked : list):
        super().__init__()

        self.liste_elt_checked : list = liste_element_checked

        self.setWindowTitle("Afficher une image")

        self.nomProduit : str = nomProduit

        self.setStyleSheet("""
                           background-color : #D9D9D9;
                           border-radius : 25px;
                           text-transform : uppercase;
                           font-weight : bold;
                           font-size : 20px;
                           color : black;
                           """)
        

        # Créer un QLabel pour contenir l'image
        self.image_label = QLabel(self)
        pixmap = QPixmap("./Images/" + self.nomProduit + ".png").scaled(156, 156, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

        self.labelNomProduit : QLabel = QLabel(self.nomProduit)

        self.checkBox_selectionProduit : QCheckBox = QCheckBox()
        self.checkBox_selectionProduit.stateChanged.connect(self.retourCheck)
        self.checkBox_selectionProduit.setStyleSheet("""
                                                    QCheckBox::indicator {
                                                    border : 1px solid black;
                                                    }
                                                    QCheckBox::indicator:checked {
                                                    background-color : green;
                                                    }
                                                    """)
        
    

        top_layout : QVBoxLayout = QVBoxLayout()
        top_layout.addWidget(self.image_label)

        # Layout bas de page
        bottom_layout : QHBoxLayout = QHBoxLayout()
        bottom_layout.addWidget(self.labelNomProduit)
        bottom_layout.addWidget(self.checkBox_selectionProduit)

        #Création du layout principal
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)
        self.setLayout(main_layout)


        self.show()

    def retourCheck(self, etat) -> str:
        if etat == 2 : self.liste_elt_checked.append(self.nomProduit)
        else : self.liste_elt_checked.remove(self.nomProduit)
        print(f"La liste est \n{self.liste_elt_checked}")


if __name__ == '__main__' :
    
    liste_elt_checked : list = []
    app : QApplication = QApplication(sys.argv)

    f : ProduitWidget = ProduitWidget("Ail", liste_elt_checked)
    f2 : ProduitWidget = ProduitWidget("Champignon", liste_element_checked=liste_elt_checked)

    app.exit(app.exec())