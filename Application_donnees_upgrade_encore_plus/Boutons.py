import json
import os
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QInputDialog, QMessageBox

from Donnees import Donnees
from styles import BUTTON_SECONDARY_STYLE, BUTTON_WARNING_STYLE

class Boutons(QWidget):
    def __init__(self, donnees: Donnees):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.donnees = donnees  # <- FIX: Ajout de l’attribut manquant

        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.setStyleSheet(BUTTON_WARNING_STYLE)
        self.create_btn = QPushButton("Créer la liste")
        self.create_btn.setStyleSheet(BUTTON_SECONDARY_STYLE)
        self.create_btn.clicked.connect(self.saveListe)
        layout.addStretch()
        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.create_btn)
        layout.addStretch()
        layout.setContentsMargins(0, 20, 0, 20)

    def saveListe(self):
        # Création du dictionnaire à sauvegarder
        liste_finale = {}
        for categorie, produits in self.donnees.listProduitsTotal.items():
            if categorie == "Tout":
                continue  # On ignore la catégorie "Tout"
            selectionnes = [p for p in produits if p in self.donnees.list_prod_checked]
            if selectionnes:
                liste_finale[categorie] = selectionnes

        # Demander le nom du fichier à l'utilisateur
        nom_fichier, ok = QInputDialog.getText(
            self,
            "Choisir le nom de votre liste",
            "Entrez le nom du fichier :"
        )

        if not ok or not nom_fichier.strip():
            QMessageBox.warning(self, "Annulé", "La sauvegarde a été annulée ou le nom est vide.")
            return

        nom_fichier = nom_fichier.strip()
        if not nom_fichier.endswith(".json"):
            nom_fichier += ".json"

        dossier = "sauvegardeListeCourses"
        os.makedirs(dossier, exist_ok=True)
        chemin_complet = os.path.join(dossier, nom_fichier)

        try:
            with open(chemin_complet, "w", encoding="utf-8") as f:
                json.dump(liste_finale, f, ensure_ascii=False, indent=4)

            chemin_absolu = os.path.abspath(chemin_complet)  # <- ligne ajoutée
            QMessageBox.information(
                self,
                "Succès",
                f"Votre liste a été sauvegardée dans :\n{chemin_absolu}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde : {e}")
