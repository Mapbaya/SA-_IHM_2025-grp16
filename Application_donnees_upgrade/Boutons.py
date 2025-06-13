import json
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from Donnees import Donnees
from styles import BUTTON_SECONDARY_STYLE, BUTTON_WARNING_STYLE

class Boutons(QWidget):
    def __init__(self, donnees : Donnees):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setStyleSheet(BUTTON_WARNING_STYLE)
        self.create_btn = QPushButton("Créer la liste")
        self.create_btn.setStyleSheet(BUTTON_SECONDARY_STYLE)
        self.create_btn.clicked.connect(self.printliste)
        layout.addStretch()
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.create_btn)
        layout.addStretch()
        layout.setContentsMargins(0, 20, 0, 20)
        self.listDonnees : list = donnees.list_prod_checked
    
    def printliste(self):
        liste_finale = {}

        # On parcourt chaque catégorie
        for categorie, produits in self.donnees.listProduitsTotal.items():
            # On filtre les produits sélectionnés dans cette catégorie
            produits_selectionnes = [prod for prod in produits if prod in self.donnees.list_prod_checked]

            # On ajoute seulement s'il y a au moins un produit sélectionné
            if produits_selectionnes:
                liste_finale[categorie] = produits_selectionnes

        # Écriture dans un fichier JSON
        with open("liste_finale.json", "w", encoding="utf-8") as f:
            json.dump(liste_finale, f, ensure_ascii=False, indent=4)

        print("✅ Liste enregistrée dans 'liste_finale.json'")

        

