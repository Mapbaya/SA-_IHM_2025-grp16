"""
Interface de gestion des projets de magasin.

Cette interface permet de gérer l'ensemble de vos projets de magasin de manière
intuitive et efficace. Elle offre les fonctionnalités suivantes :
- Création de nouveaux projets
- Ouverture et modification de projets existants
- Suppression sécurisée de projets

L'interface utilise un design moderne avec une palette de couleurs bleue
et une mise en page claire et intuitive.
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QPushButton, QListWidget,
                           QMessageBox, QHBoxLayout)
from PyQt6.QtCore import Qt
import os
from app1.controleurs.gestion_projet import GestionProjet
from app1.vues.creation_projet import DialogueCreationProjet
from app1.vues.vue_projet import VueProjet
from config import DOSSIER_PROJETS
from app1.styles import (WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        BUTTON_WARNING_STYLE, LIST_STYLE, TITLE_LABEL_STYLE)

class MainApp1(QMainWindow):
    """
    Interface principale de gestion des projets de magasin.
    
    Cette fenêtre offre une vue d'ensemble de tous vos projets et permet
    de les gérer facilement. Elle intègre une liste interactive des projets
    et des boutons d'action pour créer, ouvrir ou supprimer des projets.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Création de projet magasin")
        self.parent = parent
        
        # Application du thème global
        self.setStyleSheet(WINDOW_STYLE)
        
        # Initialisation du gestionnaire de projets
        self.gestion_projet = GestionProjet()
        
        # Configuration de l'interface utilisateur
        self._setup_interface()
        
    def _setup_interface(self):
        """
        Configure l'interface utilisateur avec une mise en page élégante
        et des éléments visuels cohérents.
        """
        # Création du widget principal
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Configuration de la mise en page
        layout = QVBoxLayout(widget_central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # En-tête de l'application
        self._setup_header(layout)
        
        # Barre d'actions
        self._setup_action_buttons(layout)
        
        # Liste des projets
        self._setup_project_list(layout)
        
        # Bouton de retour
        self._setup_back_button(layout)
        
        # État initial des boutons
        self._update_button_states()
        
        # Affichage en plein écran
        self.showMaximized()
        
    def _setup_header(self, layout):
        """
        Configure l'en-tête de l'application avec un titre élégant.
        """
        titre = QLabel("Gestion des projets")
        titre.setStyleSheet(TITLE_LABEL_STYLE)
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titre)
        
    def _setup_action_buttons(self, layout):
        """
        Configure la barre d'actions avec les boutons principaux.
        """
        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(15)
        
        # Bouton de création
        btn_nouveau = QPushButton("Nouveau Projet")
        btn_nouveau.setStyleSheet(BUTTON_STYLE)
        btn_nouveau.clicked.connect(self.nouveau_projet)
        layout_boutons.addWidget(btn_nouveau)
        
        # Bouton d'ouverture
        self.btn_ouvrir = QPushButton("Ouvrir Projet")
        self.btn_ouvrir.setStyleSheet(BUTTON_STYLE)
        self.btn_ouvrir.clicked.connect(self.ouvrir_projet_selectionne)
        layout_boutons.addWidget(self.btn_ouvrir)
        
        # Bouton de suppression
        self.btn_supprimer = QPushButton("Supprimer Projet")
        self.btn_supprimer.setStyleSheet(BUTTON_WARNING_STYLE)
        self.btn_supprimer.clicked.connect(self.supprimer_projet_selectionne)
        layout_boutons.addWidget(self.btn_supprimer)
        
        layout.addLayout(layout_boutons)
        
    def _setup_project_list(self, layout):
        """
        Configure la liste interactive des projets.
        """
        self.liste_projets = QListWidget()
        self.liste_projets.setStyleSheet(LIST_STYLE)
        self.liste_projets.itemSelectionChanged.connect(self.selection_changee)
        layout.addWidget(self.liste_projets)
        
        # Chargement initial des projets
        self.maj_liste_projets()
        
    def _setup_back_button(self, layout):
        """
        Ajoute le bouton de retour au menu principal.
        """
        btn_retour = QPushButton("Retour au menu principal")
        btn_retour.setStyleSheet(BUTTON_SECONDARY_STYLE)
        btn_retour.clicked.connect(self.retour_menu)
        layout.addWidget(btn_retour)
        
    def _update_button_states(self):
        """
        Met à jour l'état des boutons en fonction de la sélection.
        """
        self.btn_ouvrir.setEnabled(False)
        self.btn_supprimer.setEnabled(False)
                    
    def maj_liste_projets(self):
        """
        Actualise la liste des projets disponibles depuis le dossier des projets.
        """
        self.liste_projets.clear()
        if os.path.exists(DOSSIER_PROJETS):
            for projet in os.listdir(DOSSIER_PROJETS):
                if os.path.isdir(os.path.join(DOSSIER_PROJETS, projet)):
                    self.liste_projets.addItem(projet)
                    
    def selection_changee(self):
        """
        Réagit au changement de sélection dans la liste des projets
        en activant ou désactivant les boutons appropriés.
        """
        a_selection = bool(self.liste_projets.selectedItems())
        self.btn_ouvrir.setEnabled(a_selection)
        self.btn_supprimer.setEnabled(a_selection)
                    
    def nouveau_projet(self):
        """
        Ouvre l'interface de création d'un nouveau projet et actualise
        la liste si un projet est créé.
        """
        dialogue = DialogueCreationProjet(self)
        if dialogue.exec():
            self.maj_liste_projets()
            
    def ouvrir_projet_selectionne(self):
        """
        Ouvre l'interface du projet sélectionné avec gestion des erreurs
        pour une meilleure expérience utilisateur.
        """
        item = self.liste_projets.currentItem()
        if item:
            try:
                projet = self.gestion_projet.charger_projet(item.text())
                if not os.path.exists(projet['chemin_plan']):
                    raise ValueError(f"Le fichier du plan est introuvable : {projet['chemin_plan']}")
                self.vue_projet = VueProjet(projet, self)
                self.vue_projet.show()
                self.hide()
            except Exception as e:
                QMessageBox.warning(
                    self, 
                    "Erreur d'ouverture",
                    f"Impossible d'ouvrir le projet : {str(e)}"
                )
                
    def supprimer_projet_selectionne(self):
        """
        Supprime le projet sélectionné après confirmation de l'utilisateur,
        avec gestion des erreurs pour une suppression sécurisée.
        """
        item = self.liste_projets.currentItem()
        if item:
            reponse = QMessageBox.question(
                self,
                "Confirmation de suppression",
                f"Êtes-vous sûr de vouloir supprimer le projet '{item.text()}' ?\n"
                "Cette action est irréversible.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reponse == QMessageBox.StandardButton.Yes:
                try:
                    self.gestion_projet.supprimer_projet(item.text())
                    self.maj_liste_projets()
                except Exception as e:
                    QMessageBox.warning(
                        self, 
                        "Erreur de suppression",
                        f"Impossible de supprimer le projet : {str(e)}"
                    )
            
    def retour_menu(self):
        """
        Retourne au menu principal de l'application.
        """
        if self.parent:
            self.parent.show()
        self.close() 