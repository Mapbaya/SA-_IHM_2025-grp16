from PyQt6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QSize

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

