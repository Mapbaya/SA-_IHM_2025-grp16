"""
Cette fenêtre permet de créer un nouveau projet de magasin.
Elle demande à l'utilisateur toutes les infos nécessaires comme
le nom du projet, le magasin concerné, qui fait le projet, etc.
"""

# On importe tout ce qu'il faut pour faire une belle interface graphique ^^
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                           QLabel, QLineEdit, QPushButton, QFileDialog,
                           QMessageBox, QSpinBox)
from PyQt6.QtCore import Qt
import os
# On va chercher le dossier où tous les projets sont rangés
from config import DOSSIER_PROJETS
# On importe notre gestionnaire de projets 
from app1.controleurs.gestion_projet import GestionProjet
from app1.styles import (WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        INPUT_STYLE, FIELD_LABEL_STYLE)

class DialogueCreationProjet(QDialog):
    """
    La fenêtre principale pour créer un nouveau projet.
    C'est ici que l'utilisateur va remplir toutes les infos.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau Projet")
        self.setModal(True)  # On force l'utilisateur à finir cette fenêtre avant de faire autre chose
        self.gestion_projet = GestionProjet()
        
        # Applique le style global
        self.setStyleSheet(WINDOW_STYLE)
        
        self.init_ui()
        
    def init_ui(self):
        """
        Crée toute l'interface graphique avec les champs à remplir.
        Organisé propremement avec des layouts.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Zone pour le nom du projet ---
        layout_nom = QHBoxLayout()
        label_nom = QLabel("Nom du projet:")
        label_nom.setStyleSheet(FIELD_LABEL_STYLE)
        self.input_nom = QLineEdit()
        self.input_nom.setStyleSheet(INPUT_STYLE)
        layout_nom.addWidget(label_nom)
        layout_nom.addWidget(self.input_nom)
        layout.addLayout(layout_nom)
        
        # --- Zone pour le nom du magasin ---
        layout_magasin = QHBoxLayout()
        label_magasin = QLabel("Magasin:")
        label_magasin.setStyleSheet(FIELD_LABEL_STYLE)
        self.input_magasin = QLineEdit()
        self.input_magasin.setStyleSheet(INPUT_STYLE)
        layout_magasin.addWidget(label_magasin)
        layout_magasin.addWidget(self.input_magasin)
        layout.addLayout(layout_magasin)
        
        # --- Zone pour l'auteur du projet ---
        layout_auteur = QHBoxLayout()
        label_auteur = QLabel("Auteur:")
        label_auteur.setStyleSheet(FIELD_LABEL_STYLE)
        self.input_auteur = QLineEdit()
        self.input_auteur.setStyleSheet(INPUT_STYLE)
        layout_auteur.addWidget(label_auteur)
        layout_auteur.addWidget(self.input_auteur)
        layout.addLayout(layout_auteur)
        
        # --- Zone pour choisir le plan du magasin ---
        layout_plan = QHBoxLayout()
        label_plan = QLabel("Plan:")
        label_plan.setStyleSheet(FIELD_LABEL_STYLE)
        self.input_plan = QLineEdit()
        self.input_plan.setStyleSheet(INPUT_STYLE)
        self.input_plan.setReadOnly(True)  # L'utilisateur ne peut pas écrire directement, il doit utiliser le bouton
        btn_parcourir = QPushButton("Parcourir...")
        btn_parcourir.setStyleSheet(BUTTON_STYLE)
        btn_parcourir.clicked.connect(self.selectionner_plan)
        layout_plan.addWidget(label_plan)
        layout_plan.addWidget(self.input_plan)
        layout_plan.addWidget(btn_parcourir)
        layout.addLayout(layout_plan)
        
        # --- Zone pour définir la taille du quadrillage ---
        layout_quadrillage = QHBoxLayout()
        label_quadrillage = QLabel("Taille du quadrillage (pixels):")
        label_quadrillage.setStyleSheet(FIELD_LABEL_STYLE)
        self.input_quadrillage = QSpinBox()
        # On limite entre 50 et 200 pixels pour rester raisonnable
        self.input_quadrillage.setRange(50, 200)
        self.input_quadrillage.setValue(100)  # Valeur par défaut qui marche bien
        self.input_quadrillage.setSingleStep(10)  # On avance de 10 en 10
        self.input_quadrillage.setStyleSheet(INPUT_STYLE)
        layout_quadrillage.addWidget(label_quadrillage)
        layout_quadrillage.addWidget(self.input_quadrillage)
        layout.addLayout(layout_quadrillage)
        
        # --- Les boutons en bas de la fenêtre ---
        layout_boutons = QHBoxLayout()
        layout_boutons.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout_boutons.setSpacing(10)
        
        # Bouton pour annuler et fermer la fenêtre
        btn_annuler = QPushButton("Annuler")
        btn_annuler.setStyleSheet(BUTTON_SECONDARY_STYLE)
        btn_annuler.clicked.connect(self.reject)
        
        # Bouton pour créer le projet une fois qu'on a tout rempli
        btn_creer = QPushButton("Créer")
        btn_creer.setStyleSheet(BUTTON_STYLE)
        btn_creer.clicked.connect(self.creer_projet)
        btn_creer.setDefault(True)  # C'est le bouton par défaut quand on appuie sur Entrée
        
        layout_boutons.addWidget(btn_annuler)
        layout_boutons.addWidget(btn_creer)
        layout.addLayout(layout_boutons)
        
        # On s'assure que la fenêtre est assez large pour tout afficher
        self.setMinimumWidth(600)
        
    def selectionner_plan(self):
        """
        Ouvre une fenêtre pour choisir le fichier du plan du magasin.
        On accepte les images PNG et JPEG..
        """
        fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner le plan du magasin",
            "",
            "Images (*.png *.jpg *.jpeg);;Tous les fichiers (*.*)"
        )
        if fichier:
            self.input_plan.setText(fichier)
            
    def creer_projet(self):
        """
        On récupère toutes les infos
        saisies par l'utilisateur et on crée le projet.
        """
        # On récupère tout ce que l'utilisateur a saisi
        nom = self.input_nom.text().strip()
        magasin = self.input_magasin.text().strip()
        auteur = self.input_auteur.text().strip()
        plan = self.input_plan.text().strip()
        taille_quadrillage = self.input_quadrillage.value()
        
        # On vérifie que l'utilisateur n'a rien oublié
        if not all([nom, magasin, auteur, plan]):
            QMessageBox.warning(
                self,
                "Champs manquants",
                "Tous les champs sont obligatoires."
            )
            return
            
        # On essaie de créer le projet
        try:
            self.gestion_projet.creer_projet(
                nom, magasin, auteur, plan, taille_quadrillage
            )
            self.accept()  # Tout s'est bien passé, on ferme la fenêtre
        except Exception as e:
            # Ou uelque chose s'est mal passé, on prévient l'utilisateur
            QMessageBox.critical(self, "Erreur", str(e)) 