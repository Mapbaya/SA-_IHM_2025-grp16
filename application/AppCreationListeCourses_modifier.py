import sys
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QMainWindow, QApplication, QCheckBox, QGridLayout, QPushButton, QMessageBox
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize, Qt
from Donnees import Donnees
from ProduitWidget import ProduitWidget

class Categories(QWidget):
    def __init__(self, liste_produits : list, liste_elt_checked : list) -> None:
        super().__init__()

        # Titre
        self.label_title: QLabel = QLabel("CRÉATION D’UNE LISTE DE COURSES")

        # Filtrage
        self.combo = QComboBox()

        self.combo.setStyleSheet("""
                                background-color :#CEE694 ;
                                 """)

        for categorie in liste_produits:
            self.combo.addItem(categorie)
        self.filterButton : QPushButton = QPushButton("Filtrer")
        self.filterButton.setStyleSheet("""
                                background-color :#E7EEB3 ;""")

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
        palette.setColor(QPalette.ColorRole.Window, QColor("#E3EBF2"))  # Gris clair
        self.produits_widget.setAutoFillBackground(True)
        self.produits_widget.setPalette(palette)

        # Layout sous forme de tableau
        self.layoutListeProduits: QGridLayout = QGridLayout()
        self.layoutListeProduits.setSpacing(10)

        liste : list = []
        self.produits : list = []

        for i in range(3):
            for j in range(2):
                widget : ProduitWidget = ProduitWidget("Champignon", liste)
                self.layoutListeProduits.addWidget(widget, i, j)
                self.produits.append(widget)

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
        palette.setColor(QPalette.ColorRole.Window, QColor("#F6EECF"))  # Gris clair
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
        self.cancel_btn.setStyleSheet("background-color: #BD3434;")
        self.create_btn = QPushButton("Créer la liste")
        self.create_btn.setStyleSheet("background-color: #FFA175;")
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
        self.setFixedSize(950, 650)

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
        self.boutons.cancel_btn.clicked.connect(self.afficher_popup_annulation)



        self.show()

    def afficher_popup_annulation(self):
        message_box = QMessageBox(self)
        message_box.setWindowTitle("Vérification")
        message_box.setText("Êtes-vous sur d’annuler ?\nToutes modifications ne seront pas enregistrées.")
        quitter_btn = message_box.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)
        continuer_btn = message_box.addButton("Continuer", QMessageBox.ButtonRole.AcceptRole)

        quitter_btn.setStyleSheet("background-color: #BD3434; color: white; padding: 5px 10px;")
        continuer_btn.setStyleSheet("background-color: #FFA175; color: black; padding: 5px 10px;")

        message_box.exec()

        if message_box.clickedButton() == quitter_btn:               
            self.close()  


if __name__ == "__main__":

    app : QApplication = QApplication(sys.argv)

    window : MainWindow = MainWindow()
   
    sys.exit(app.exec())
