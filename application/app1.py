import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QComboBox, QMessageBox,
    QVBoxLayout, QHBoxLayout, QCheckBox, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt


class Categories(QWidget):
    def __init__(self):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.label_title = QLabel("CRÉATION D’UNE LISTE DE COURSES")
        self.combo = QComboBox()
        self.combo.addItems(["TOUT", "Légumes", "Poissons", "Viandes", "Épicerie", "Épicerie sucrée"])
        self.check_all = QCheckBox("Tout sélectionner")

        layout.addWidget(self.label_title)
        layout.addStretch()
        layout.addWidget(self.combo)
        layout.addWidget(self.check_all)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)


class ZoneGrise(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.setContentsMargins(0, 0, 0, 0)
        cadre = QFrame()
        cadre.setStyleSheet("background-color: #d3d3d3; border: 1px solid #999;")
        cadre.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(cadre)


class Selection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        label = QLabel("Sélection")
        layout.addWidget(label)
        zone = ZoneGrise()
        layout.addWidget(zone)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)


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
        self.cancel_btn.clicked.connect(self.cancel)

    def cancel(self):
        annuler = QMessageBox()
        annuler.setWindowTitle("Annuler")
        annuler.setText("Êtes-vous sûr d’annuler ?\nToutes modifications ne seront pas enregistrées.")
        annuler.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        annuler.setDefaultButton(QMessageBox.StandardButton.No)

        annuler.button(QMessageBox.StandardButton.Yes).setText("Oui")
        annuler.button(QMessageBox.StandardButton.No).setText("Non")

        res = annuler.exec()
        if res == QMessageBox.StandardButton.Yes:
            QApplication.quit()


class ShoppingListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Création d’une liste de courses")
        self.setMinimumSize(950, 650)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.categories = Categories()
        main_layout.addWidget(self.categories)

        centre_layout = QHBoxLayout()
        centre_layout.setSpacing(20)
        self.zone_gauche = ZoneGrise()
        self.zone_droite = Selection()

        centre_layout.addWidget(self.zone_gauche, 3)  
        centre_layout.addWidget(self.zone_droite, 1)  
        main_layout.addLayout(centre_layout)

        self.boutons = Boutons()
        main_layout.addWidget(self.boutons)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShoppingListApp()
    window.show()
    sys.exit(app.exec())
