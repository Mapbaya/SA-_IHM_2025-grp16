from PyQt6.QtWidgets import QCheckBox, QComboBox, QGridLayout, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QScrollArea, QMessageBox, QApplication, QSplashScreen
from PyQt6.QtGui import QPalette, QColor, QPixmap
from PyQt6.QtCore import Qt

from Donnees import Donnees
from ProduitWidget import ProduitWidget
from styles import TITLE_LABEL_STYLE, BUTTON_FILTRE_STYLE

class Categories(QWidget):
    def __init__(self, liste_categories : list, list_prod_checked : list, data : Donnees) -> None:
        super().__init__()

        # Titre
        self.label_title: QLabel = QLabel("CRÉATION D’UNE LISTE DE COURSES")
        self.label_title.setStyleSheet(TITLE_LABEL_STYLE)

        # Filtrage
        self.combo = QComboBox()
        
        self.combo.addItems(liste_categories)
        self.filterButton : QPushButton = QPushButton("Filtrer")
        self.filterButton.setStyleSheet(BUTTON_FILTRE_STYLE)
        self.filterButton.clicked.connect(self.filtrer)

        self.check_all = QCheckBox("Tout sélectionner")
        self.check_all.setStyleSheet("""
                                    color : #000000;
                                    font-size = 12px
                                    """)
        self.check_all.stateChanged.connect(self.selectAll)

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

        # Couleur de fond du layout grid
        palette = self.produits_widget.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#f0f0f0"))  # Gris clair
        self.produits_widget.setAutoFillBackground(True)
        self.produits_widget.setPalette(palette)

        # Layout sous forme de tableau
        self.layoutListeProduits: QGridLayout = QGridLayout()
        self.layoutListeProduits.setSpacing(10)
        self.produits_widget.setLayout(self.layoutListeProduits)

        self.data_list_prod: list = data.listProduitsTotal
        self.products = []
        self.list_prod_checked = data.list_prod_checked

        self.load_products(self.combo.currentText())

        # Création de la QScrollArea
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.produits_widget)

        # Ajout de la scroll area dans le layout principal
        self.main_layout.addWidget(scroll_area)


    def filtrer(self):
        # Splash
        splash_pix = QPixmap(950, 650)
        splash_pix.fill(QColor("white"))
        splash = QSplashScreen(splash_pix)
        splash.showMessage("Chargement des produits...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
        splash.show()
        QApplication.processEvents()

        self.load_products(self.combo.currentText())

        splash.close()
        return self.combo.currentText()
    
    def selectAll(self, state):
        is_checked = state == Qt.CheckState.Checked.value  # <-- Ajout `.value`
        for produit in self.products:
            produit.checkbox.setChecked(is_checked)
   
    def clear_grid_layout(self, layout: QGridLayout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.setParent(None)

            else:
                # Si c'est un layout imbriqué
                sub_layout = item.layout()
                if sub_layout is not None:
                    self.clear_grid_layout(sub_layout)

    def load_products(self, category: str):
        self.products.clear()
        self.clear_grid_layout(self.layoutListeProduits)

        produits = self.data_list_prod[category]
        indice_elt: int = 0

        for i in range((len(produits) + 3) // 4):
            for j in range(4):
                if indice_elt >= len(produits):
                    break
                name = produits[indice_elt]
                widget = ProduitWidget(name, self.list_prod_checked)
                self.layoutListeProduits.addWidget(widget, i, j)
                self.products.append(widget)
                indice_elt += 1

                QApplication.processEvents()

