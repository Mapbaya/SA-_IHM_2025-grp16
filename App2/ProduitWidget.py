from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QApplication, QMainWindow, QCheckBox, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
import sys, os

from .Donnees import Donnees
from .styles import FIELD_LABEL_STYLE


class ProduitWidget(QWidget):

    def __init__(self, name : str, list_prod_checked : list, selection_widget):
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
      
        self.selection_widget = selection_widget
        self.selection_widget.widgets_produits[self.nomProduit] = self


        # chemin absolu du dossier Images
        script_dir = os.path.dirname(os.path.abspath(__file__))
        chemin_image = os.path.join(script_dir, "Images", name + ".png")
        chemin_image = os.path.normpath(chemin_image)
        
        
        image = QLabel()
        pixmap = QPixmap(chemin_image).scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        
        
        
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
        if etat == Qt.CheckState.Checked.value:
            if self.nomProduit not in self.list_elt_checked:
                self.list_elt_checked.append(self.nomProduit)
                self.selection_widget.ajouter_produit(self.nomProduit)
        else:
            if self.nomProduit in self.list_elt_checked:
                self.list_elt_checked.remove(self.nomProduit)
                self.selection_widget.retirer_produit(self.nomProduit)
        


if __name__ == '__main__' :
    
    
    app : QApplication = QApplication(sys.argv)

    data = Donnees()
    
    f : ProduitWidget = ProduitWidget("Ail", data.list_prod_checked)
    f2 : ProduitWidget = ProduitWidget("Champignon", data.list_prod_checked)

    app.exit(app.exec())

    print(data.list_prod_checked)