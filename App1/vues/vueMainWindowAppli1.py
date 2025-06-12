"""
Interface principale de gestion d'un projet de magasin.

Cette interface présente :
- Une visualisation interactive du plan du magasin
- Un gestionnaire de produits par zone
- Des outils de modification et de sauvegarde
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QLabel, QPushButton, QMessageBox, QGraphicsView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from vues.vueScenePlan import VuePlan, ScenePlan
from vues.selection_produits import SelectionProduits
from styles import (WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        TITLE_LABEL_STYLE)

class MainWindowAppli1(QMainWindow):
    """
    Interface principale de gestion d'un projet de magasin.
    
    Fonctionnalités principales :
    - Visualisation et interaction avec le plan
    - Gestion des produits par zone
    - Sauvegarde des modifications
    """
    
    def __init__(self, gestion_projet, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.gestion_projet = gestion_projet
        
        # Application du style global
        self.setStyleSheet(WINDOW_STYLE)

        # Configuration de l'interface
        self.initialiser_interface()
        
    def initialiser_interface(self):
        """
        Configure l'interface utilisateur avec l'ensemble des composants
        nécessaires à la gestion du projet.
        """
        # Initialisation du widget principal
        mon_widget = QWidget()
        self.setCentralWidget(mon_widget)
        
        # Configuration de la mise en page
        mon_layout = QVBoxLayout(mon_widget)
        mon_layout.setSpacing(20)
        mon_layout.setContentsMargins(20, 20, 20, 20)
        
        # Configuration des composants
        self.configurer_titre(mon_layout)
        self.configurer_contenu(mon_layout)
        self.configurer_boutons(mon_layout)
        
        # Affichage en plein écran
        self.showMaximized()
        
    def configurer_titre(self, mon_layout):
        """
        Configure la section titre avec les informations du projet.
        """
        # Layout horizontal pour le titre et les infos
        titre_layout = QHBoxLayout()
        titre_layout.setSpacing(10)
        
        # Titre principal
        mon_titre = QLabel(f"Projet : {self.gestion_projet.projet_actuel['nom']}")
        mon_titre.setStyleSheet(TITLE_LABEL_STYLE)
        titre_layout.addWidget(mon_titre)
        
        # Informations complémentaires
        mes_infos = QLabel(
            f"Magasin : {self.gestion_projet.projet_actuel['magasin']} | "
            f"Créé par : {self.gestion_projet.projet_actuel['auteur']}"
        )
        mes_infos.setStyleSheet("font-size: 14px; color: #666666;")
        titre_layout.addWidget(mes_infos)
        
        mon_layout.addLayout(titre_layout)
        
    def configurer_contenu(self, mon_layout):
        """
        Configure la zone principale avec le plan interactif
        et le gestionnaire de produits.
        """
        # Layout horizontal pour le plan et les produits
        layout_contenu = QHBoxLayout()
        layout_contenu.setSpacing(20)
        
        # Gestionnaire de produits (partie gauche)
        self.mes_produits = SelectionProduits(self)
        self.mes_produits.selection_changee.connect(self.actualiser_plan)
        layout_contenu.addWidget(self.mes_produits, stretch=1)
        
        # Vue du plan (partie droite)
        self.ma_vue_plan = VuePlan(self.gestion_projet.projet_actuel['chemin_plan'])
        self.ma_vue_plan.scene_plan.case_selectionnee.connect(self.actualiser_selection_case)
        layout_contenu.addWidget(self.ma_vue_plan, stretch=2)
        
        mon_layout.addLayout(layout_contenu)
        
    def configurer_boutons(self, mon_layout):
        """
        Configure la barre d'actions avec les boutons de navigation
        et de sauvegarde.
        """
        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(10)
        
        # Bouton de sauvegarde
        mon_bouton_sauver = QPushButton("Sauvegarder")
        mon_bouton_sauver.setStyleSheet(BUTTON_STYLE)
        mon_bouton_sauver.clicked.connect(self.sauvegarder_projet)
        layout_boutons.addWidget(mon_bouton_sauver)
        
        # Bouton de retour
        mon_bouton_retour = QPushButton("Retour à la liste")
        mon_bouton_retour.setStyleSheet(BUTTON_SECONDARY_STYLE)
        mon_bouton_retour.clicked.connect(self.retourner_liste)
        layout_boutons.addWidget(mon_bouton_retour)
        
        mon_layout.addLayout(layout_boutons)
        
    def actualiser_selection_case(self, case):
        """
        Met à jour la sélection des produits lors de la sélection
        d'une zone sur le plan.
        """
        self.mes_produits.choisir_case(case)
        
    def actualiser_plan(self, produits):
        """
        Met à jour l'affichage du plan suite à une modification
        des produits d'une zone.
        """
        # Recréer la scène avec le plan actuel
        nouvelle_scene = ScenePlan(self.gestion_projet.projet_actuel['chemin_plan'])
        self.ma_vue_plan.setScene(nouvelle_scene)
        self.ma_vue_plan.scene_plan = nouvelle_scene
        nouvelle_scene.case_selectionnee.connect(self.actualiser_selection_case)
        
    def sauvegarder_projet(self):
        """
        Sauvegarde l'état actuel du projet avec gestion des erreurs.
        """
        try:
            self.gestion_projet.sauvegarder()
            QMessageBox.information(
                self,
                "Succès",
                "Le projet a été sauvegardé avec succès."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de la sauvegarde : {str(e)}"
            )
            
    def retourner_liste(self):
        """
        Retourne à l'interface de gestion des projets.
        """
        if self.parent:
            self.parent.show()
        self.close() 