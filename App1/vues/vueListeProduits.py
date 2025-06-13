"""
Interface d'affichage de la liste des produits par magasin.

Cette interface permet de :
- Voir tous les produits placés dans le magasin
- Voir leur emplacement
- Filtrer par catégorie
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QTreeWidget, QTreeWidgetItem, QScrollArea)
from PyQt6.QtCore import Qt
from styles import DIALOG_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE, TITLE_LABEL_STYLE
import json
import os

class VueListeProduits(QDialog):
    """
    Interface de dialogue pour afficher la liste des produits par magasin.
    """
    
    def __init__(self, gestion_projet, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Liste des produits")
        self.gestion_projet = gestion_projet
        
        # Application du style
        self.setStyleSheet(DIALOG_STYLE)
        
        # Configuration de l'interface
        self.initialiser_interface()
        
    def initialiser_interface(self):
        """
        Configure l'interface utilisateur avec l'arborescence des produits
        et les boutons de contrôle.
        """
        # Configuration de la mise en page
        mon_layout = QVBoxLayout(self)
        mon_layout.setSpacing(15)
        
        # Titre
        titre = QLabel("Liste des produits par magasin")
        titre.setStyleSheet(TITLE_LABEL_STYLE)
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mon_layout.addWidget(titre)
        
        # Arborescence des produits
        self.liste_produits = QTreeWidget()
        self.liste_produits.setHeaderLabels(["Produit", "Emplacement"])
        self.liste_produits.setColumnWidth(0, 200)
        
        # Zone de défilement
        ma_zone_defilement = QScrollArea()
        ma_zone_defilement.setWidget(self.liste_produits)
        ma_zone_defilement.setWidgetResizable(True)
        mon_layout.addWidget(ma_zone_defilement)
        
        # Bouton de fermeture
        layout_boutons = QHBoxLayout()
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.setStyleSheet(BUTTON_SECONDARY_STYLE)
        bouton_fermer.clicked.connect(self.close)
        layout_boutons.addWidget(bouton_fermer)
        mon_layout.addLayout(layout_boutons)
        
        # Chargement des données
        self.charger_produits()
        
    def charger_produits(self):
        """
        Charge et affiche la liste des produits placés dans le magasin.
        """
        # Récupération des données du projet
        projet = self.gestion_projet.projet_actuel
        if not projet or 'produits' not in projet:
            return
            
        # Chargement des catégories depuis le fichier de produits
        try:
            with open('App1/list/liste_produits_original.json', 'r', encoding='utf-8') as f:
                categories_produits = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement des catégories : {str(e)}")
            categories_produits = {}
            
        # Création des catégories
        categories = {}
        for case, produits in projet['produits'].items():
            for nom_produit in produits:
                # Recherche de la catégorie du produit
                categorie = 'Non catégorisé'
                for cat, prods in categories_produits.items():
                    if nom_produit in prods:
                        categorie = cat
                        break
                        
                if categorie not in categories:
                    categories[categorie] = []
                categories[categorie].append((nom_produit, case))
        
        # Remplissage de l'arborescence
        for categorie, produits in sorted(categories.items()):
            item_categorie = QTreeWidgetItem(self.liste_produits)
            item_categorie.setText(0, categorie)
            
            for nom_produit, case in sorted(produits):
                item_produit = QTreeWidgetItem(item_categorie)
                item_produit.setText(0, nom_produit)
                item_produit.setText(1, case) 