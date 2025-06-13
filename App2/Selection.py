from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QScrollArea

from PyQt6.QtCore import Qt

class Selection(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        label = QLabel("Sélection")
        self.main_layout.addWidget(label)

        # Zone scrollable
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_content.setStyleSheet("background-color: #2c2c2c;")

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.labels = {}  # nom -> QLabel
        self.widgets_produits = {}  # nom -> ProduitWidget (sera rempli depuis ProduitWidget)

    def ajouter_produit(self, nom: str):
        if nom not in self.labels:
            # Crée le nouveau label
            label = QLabel(nom)
            label.setStyleSheet("color: white; padding: 5px;")
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            label.mousePressEvent = lambda event, n=nom: self.retirer_depuis_label(n)

            self.labels[nom] = label

            # Réordonner les labels dans le layout
            self._reordonner_labels()

    def retirer_depuis_label(self, nom: str):
        if nom in self.widgets_produits:
            self.widgets_produits[nom].checkbox.setChecked(False)

        label = self.labels.pop(nom, None)
        if label:
            self.scroll_layout.removeWidget(label)
            label.deleteLater()
        
        self.widgets_produits.pop(nom, None)

    def retirer_produit(self, nom: str):
        if nom in self.labels:
            label = self.labels.pop(nom)
            self.scroll_layout.removeWidget(label)
            label.deleteLater()

    def _reordonner_labels(self):
        # Supprimer tous les widgets du layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                self.scroll_layout.removeWidget(widget)

        # Réinsérer les labels triés par ordre alphabétique
        for nom in sorted(self.labels.keys(), key=lambda x: x.lower()):
            self.scroll_layout.addWidget(self.labels[nom])