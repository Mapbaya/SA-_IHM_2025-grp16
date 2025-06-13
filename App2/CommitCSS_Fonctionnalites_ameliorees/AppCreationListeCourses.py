import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QMainWindow, QApplication, QCheckBox, QGridLayout, QPushButton
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize
from Donnees import Donnees

class Categories(QWidget):
    def __init__(self, liste_produits : list, liste_elt_checked : list) -> None:
        super().__init__()

        # Titre
        self.label_title: QLabel = QLabel("CRÉATION D’UNE LISTE DE COURSES")

        # Filtrage
        self.combo = QComboBox()
        for categorie in liste_produits:
            self.combo.addItem(categorie)
        self.filterButton : QPushButton = QPushButton("Filtrer")

        self.check_all = QCheckBox("Tout sélectionner")

        self.layout_top_bottom : QHBoxLayout = QHBoxLayout()
        self.layout_top_bottom.addWidget(self.combo)
        self.layout_top_bottom.addWidget(self.filterButton)
        self.layout_top_bottom.addWidget(self.check_all)

        # Layout du haut
        self.layout_top: QVBoxLayout = QVBoxLayout()
        self.layout_top.addWidget(self.label_title)
        self.layout_top.addLayout(self.layout_top_bottom)
        self.layout_top.setContentsMargins(10, 10, 10, 10)

        # Layout principal
        self.main_layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addLayout(self.layout_top)

        # Widget conteneur pour le tableau
        self.produits_widget = QWidget()
        self.produits_widget.setFixedSize(QSize(600, 400))  # Taille définie

        # Couleur de fond du layout grid
        palette = self.produits_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))  # Gris clair
        self.produits_widget.setAutoFillBackground(True)
        self.produits_widget.setPalette(palette)

        # Layout sous forme de tableau
        self.layoutListeProduits: QGridLayout = QGridLayout()
        self.layoutListeProduits.setSpacing(10)

        self.produits_widget.setLayout(self.layoutListeProduits)
        self.main_layout.addWidget(self.produits_widget)


class Selection(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        label = QLabel("Sélection")

        self.main_layout.addWidget(label)

        # Widget conteneur pour le tableau
        self.produits_widget = QWidget()
        self.produits_widget.setFixedSize(QSize(200, 400))  # Taille définie

        # Couleur de fond du layout grid
        palette = self.produits_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))  # Gris clair
        self.produits_widget.setAutoFillBackground(True)
        self.produits_widget.setPalette(palette)

        # Layout sous forme de tableau
        self.layoutListeProduits: QGridLayout = QGridLayout()
        self.layoutListeProduits.setSpacing(10)

        self.produits_widget.setLayout(self.layoutListeProduits)
        self.main_layout.addWidget(self.produits_widget)


class Boutons(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.cancel_btn = QPushButton("Annuler")
        self.create_btn = QPushButton("Créer la liste")
        layout.addStretch()
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.create_btn)
        layout.addStretch()
        layout.setContentsMargins(0, 20, 0, 20)



class MainWindow(QMainWindow):

    def __init__(self) -> None:

        super().__init__()

        self.data_app : Donnees = Donnees()

        list_produits_checked : list = []

        self.setWindowTitle("Création d’une liste de courses")
        self.setMinimumSize(950, 650)

        layout_top : QHBoxLayout = QHBoxLayout()

        central : QWidget = QWidget()
        self.setCentralWidget(central)
        main_layout : QVBoxLayout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.categories : Categories = Categories(self.data_app.listProduitsTotal, list_produits_checked)
        layout_top.addWidget(self.categories)

        self.selection : Selection = Selection()
        layout_top.addWidget(self.selection)

        main_layout.addLayout(layout_top)

        self.boutons : Boutons = Boutons()
        main_layout.addWidget(self.boutons)


        self.show()

if __name__ == "__main__":

    app : QApplication = QApplication(sys.argv)

    window : MainWindow = MainWindow()
   
    sys.exit(app.exec())
