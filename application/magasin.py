import sys
import os
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QListWidget,
    QPushButton, QMessageBox
)

class ListeMagasins(QWidget):
    def __init__(self, dossier_magasins, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Liste des Magasins")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.setLayout(layout)

        titre = QLabel("Fichiers magasins (.json) disponibles :")
        self.liste = QListWidget()

        layout.addWidget(titre)
        layout.addWidget(self.liste)

        self.ajouter_magasins(dossier_magasins)

        # Bouton Ouvrir
        self.bouton_ouvrir = QPushButton("Ouvrir")
        self.bouton_ouvrir.clicked.connect(self.ouvrir_selection)
        layout.addWidget(self.bouton_ouvrir)

        # Bouton Annuler
        self.bouton_annuler = QPushButton("Annuler")
        self.bouton_annuler.clicked.connect(self.revenir_en_arriere)
        layout.addWidget(self.bouton_annuler)

        self.liste.itemDoubleClicked.connect(self.ouvrir_json)

        self.dossier_magasins = dossier_magasins

    def ajouter_magasins(self, dossier):
        self.liste.clear()
        if not os.path.exists(dossier):
            QMessageBox.warning(self, "Erreur", "Le dossier des magasins n'existe pas.")
            return
        for nom in os.listdir(dossier):
            if nom.endswith(".json"):
                self.liste.addItem(nom)

    def ouvrir_selection(self):
        item = self.liste.currentItem()
        if item:
            self.ouvrir_json(item)
        else:
            QMessageBox.warning(self, "Aucun fichier sélectionné", "Veuillez sélectionner un fichier à ouvrir.")

    def ouvrir_json(self, item):
        chemin = os.path.join(self.dossier_magasins, item.text())
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                contenu = json.load(f)
            QMessageBox.information(self, "Contenu du JSON", json.dumps(contenu, indent=2, ensure_ascii=False))
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir le fichier : {e}")

    def revenir_en_arriere(self):
        # Ici tu peux rouvrir la fenêtre précédente ou faire ce que tu veux
        QMessageBox.information(self, "Retour", "Retour à la page précédente (à adapter selon ton application).")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dossier_magasins = "./magasins"  # le dossier contenant les magasins
    fenetre = ListeMagasins(dossier_magasins)
    fenetre.show()
    sys.exit(app.exec())