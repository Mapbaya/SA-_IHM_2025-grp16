"""
Interface de création d'un nouveau projet de magasin.

Cette interface collecte :
- Le nom du projet
- Le nom du magasin
- Le nom de l'auteur
- Le fichier du plan
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                           QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from controleurs.gestion_projet import GestionProjet
from styles import (DIALOG_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        INPUT_STYLE, FIELD_LABEL_STYLE)

class DialogueCreationProjet(QDialog):
    """
    Interface de dialogue pour la création d'un nouveau projet.
    
    Collecte et valide l'ensemble des informations nécessaires
    à l'initialisation d'un nouveau projet de magasin.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nouveau projet")
        
        # Application du style
        self.setStyleSheet(DIALOG_STYLE)
        
        # Initialisation du gestionnaire
        self.mon_projet = GestionProjet()
        
        # Configuration de l'interface
        self.initialiser_interface()
        
    def initialiser_interface(self):
        """
        Configure l'interface utilisateur avec les champs de saisie
        et les boutons de validation.
        """
        # Configuration de la mise en page
        mon_layout = QVBoxLayout(self)
        mon_layout.setSpacing(15)
        
        # Configuration des champs
        self.configurer_champ_nom(mon_layout)
        self.configurer_champ_magasin(mon_layout)
        self.configurer_champ_auteur(mon_layout)
        self.configurer_champ_plan(mon_layout)
        
        # Configuration des boutons
        self.configurer_boutons(mon_layout)
        
    def configurer_champ_nom(self, mon_layout):
        """
        Configure le champ de saisie du nom du projet.
        """
        mon_label = QLabel("Nom du projet :")
        mon_label.setStyleSheet(FIELD_LABEL_STYLE)
        mon_layout.addWidget(mon_label)
        
        self.mon_nom = QLineEdit()
        self.mon_nom.setStyleSheet(INPUT_STYLE)
        self.mon_nom.setPlaceholderText("Par exemple : Magasin Centre-ville")
        mon_layout.addWidget(self.mon_nom)
        
    def configurer_champ_magasin(self, mon_layout):
        """
        Configure le champ de saisie du nom du magasin.
        """
        mon_label = QLabel("Nom du magasin :")
        mon_label.setStyleSheet(FIELD_LABEL_STYLE)
        mon_layout.addWidget(mon_label)
        
        self.mon_magasin = QLineEdit()
        self.mon_magasin.setStyleSheet(INPUT_STYLE)
        self.mon_magasin.setPlaceholderText("Par exemple : Carrefour")
        mon_layout.addWidget(self.mon_magasin)
        
    def configurer_champ_auteur(self, mon_layout):
        """
        Configure le champ de saisie du nom de l'auteur.
        """
        mon_label = QLabel("Votre nom :")
        mon_label.setStyleSheet(FIELD_LABEL_STYLE)
        mon_layout.addWidget(mon_label)
        
        self.mon_auteur = QLineEdit()
        self.mon_auteur.setStyleSheet(INPUT_STYLE)
        self.mon_auteur.setPlaceholderText("Par exemple : Marie")
        mon_layout.addWidget(self.mon_auteur)
        
    def configurer_champ_plan(self, mon_layout):
        """
        Configure le champ de sélection du fichier plan.
        """
        mon_label = QLabel("Plan du magasin :")
        mon_label.setStyleSheet(FIELD_LABEL_STYLE)
        mon_layout.addWidget(mon_label)
        
        # Configuration du layout horizontal
        layout_plan = QHBoxLayout()
        
        self.mon_plan = QLineEdit()
        self.mon_plan.setStyleSheet(INPUT_STYLE)
        self.mon_plan.setPlaceholderText("Choisissez une image PNG ou JPEG")
        self.mon_plan.setReadOnly(True)
        layout_plan.addWidget(self.mon_plan)
        
        mon_bouton_plan = QPushButton("Parcourir...")
        mon_bouton_plan.setStyleSheet(BUTTON_SECONDARY_STYLE)
        mon_bouton_plan.clicked.connect(self.selectionner_plan)
        layout_plan.addWidget(mon_bouton_plan)
        
        mon_layout.addLayout(layout_plan)
        
    def configurer_boutons(self, mon_layout):
        """
        Configure les boutons de validation et d'annulation.
        """
        layout_boutons = QHBoxLayout()
        
        mon_bouton_creer = QPushButton("Créer le projet")
        mon_bouton_creer.setStyleSheet(BUTTON_STYLE)
        mon_bouton_creer.clicked.connect(self.creer_projet)
        layout_boutons.addWidget(mon_bouton_creer)
        
        mon_bouton_annuler = QPushButton("Annuler")
        mon_bouton_annuler.setStyleSheet(BUTTON_SECONDARY_STYLE)
        mon_bouton_annuler.clicked.connect(self.reject)
        layout_boutons.addWidget(mon_bouton_annuler)
        
        mon_layout.addLayout(layout_boutons)
        
    def selectionner_plan(self):
        """
        Ouvre une boîte de dialogue pour sélectionner le fichier plan.
        Accepte les formats PNG et JPEG.
        """
        mon_fichier, _ = QFileDialog.getOpenFileName(
            self,
            "Choisir le plan du magasin",
            "",
            "Images (*.png *.jpg *.jpeg);;Tous les fichiers (*.*)"
        )
        if mon_fichier:
            self.mon_plan.setText(mon_fichier)
            
    def creer_projet(self):
        """
        Valide les informations saisies et crée le nouveau projet.
        """
        # Récupération des données
        nom = self.mon_nom.text().strip()
        magasin = self.mon_magasin.text().strip()
        auteur = self.mon_auteur.text().strip()
        plan = self.mon_plan.text().strip()
        
        # Validation des champs requis
        if not all([nom, magasin, auteur, plan]):
            QMessageBox.warning(
                self,
                "Erreur de saisie",
                "Tous les champs sont obligatoires."
            )
            return
            
        # Création du projet
        try:
            self.mon_projet.creer_projet(
                nom, magasin, auteur, plan
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible de créer le projet : {str(e)}"
            ) 