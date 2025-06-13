"""
Contrôleur pour la gestion du plan de magasin.

Ce module gère les interactions entre la vue du plan
et le modèle de données, notamment :
- La création de nouveaux plans
- L'ouverture de plans existants
- La sauvegarde des modifications
- Le contrôle du zoom
"""

import os
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTransform
from config import DOSSIER_PROJETS, EXTENSIONS_IMAGES


class PlanController:
    """
    Contrôleur pour la gestion du plan de magasin.
    
    Fait le lien entre l'interface utilisateur et les données,
    en gérant les actions sur le plan.
    """
    
    def __init__(self, modele, vue):
        """
        Initialise le contrôleur avec son modèle et sa vue.
        
        Args:
            modele: Le modèle de données du plan
            vue: La vue qui affiche le plan
        """
        self.modele = modele
        self.vue = vue
        self.chemin_courant = None
        self.connecter_signaux()
class ControllerPlan:
    """
    Contrôleur pour gérer les actions sur le plan.
    """

    def __init__(self, modele, vue):
        """
        Initialise le contrôleur avec son modèle et sa vue.
        
        Args:
            modele: Le modèle de données du plan
            vue: La vue qui affiche le plan
        """
        self.modele = modele
        self.vue = vue
        self.chemin_courant = None
        self.connecter_signaux()

    def connecter_signaux(self):
        """
        Connecte les signaux de la vue aux méthodes du contrôleur.
        """
        self.vue.signalNouveauProjet.connect(self.nouveau)
        self.vue.signalOuvrirProjet.connect(self.ouvrir)
        self.vue.signalEnregistrerProjet.connect(self.enregistrer)
        self.vue.signalInitZoom.connect(self.init_zoom)

    def nouveau(self):
        """
        Crée un nouveau projet avec un plan vierge.
        Demande à l'utilisateur de choisir une image de plan.
        """
        self.vue.statusBar().showMessage('Création d\'un nouveau projet...', 2000)
        
        # Filtre pour les images
        filtres = "Images (*.png *.jpg *.jpeg);;Tous les fichiers (*.*)"
        
        # Ouverture de la boîte de dialogue
        chemin, _ = QFileDialog.getOpenFileName(
            self.vue,
            "Choisir une image de plan",
            "",
            filtres
        )
        
        if chemin:
            try:
                # Vérification de l'extension
                _, ext = os.path.splitext(chemin)
                if ext.lower() not in ['.png', '.jpg', '.jpeg']:
                    raise ValueError("Le fichier sélectionné n'est pas une image valide.")
                
                # Charger l'image ou effectuer une autre action
                self.chemin_courant = chemin
                self.vue.statusBar().showMessage(f"Projet créé avec l'image : {chemin}", 2000)
            except Exception as e:
                self.vue.statusBar().showMessage(f"Erreur : {str(e)}", 2000)
        else:
            self.vue.statusBar().showMessage("Aucun fichier sélectionné.", 2000)

    def ouvrir(self):
        """
        Ouvre un projet existant.
        """
        self.vue.statusBar().showMessage('Ouverture d\'un projet existant...', 2000)
        # Implémentation à ajouter

    def enregistrer(self):
        """
        Enregistre le projet actuel.
        """
        self.vue.statusBar().showMessage('Enregistrement du projet...', 2000)
        # Implémentation à ajouter

    def init_zoom(self):
        """
        Initialise le zoom pour afficher tout le plan.
        """
        self.vue.statusBar().showMessage('Initialisation du zoom...', 2000)
        self.vue.afficher_vue_d_ensemble()
    def connecter_signaux(self):
        """
        Connecte les signaux de la vue aux méthodes du contrôleur.
        """
        self.vue.signalNouveauProjet.connect(self.nouveau)
        self.vue.signalOuvrirProjet.connect(self.ouvrir)
        self.vue.signalEnregistrerProjet.connect(self.enregistrer)
        self.vue.signalInitZoom.connect(self.initZoom)

    def nouveau(self):
        """
        Crée un nouveau projet avec un plan vierge.
        Demande à l'utilisateur de choisir une image de plan.
        """
        self.vue.statusBar().showMessage('Création d\'un nouveau projet...', 2000)
        
        # Filtre pour les images
        filtres = "Images (*.png *.jpg *.jpeg);;Tous les fichiers (*.*)"
        
        # Ouverture de la boîte de dialogue
        chemin, _ = QFileDialog.getOpenFileName(
            self.vue,
            "Choisir une image de plan",
            "",
            filtres
        )
        
        if chemin:
            # Vérification de l'extension
            _, ext = os.path.splitext(chemin)
            if ext.lower() not in EXTENSIONS_IMAGES:
                QMessageBox.warning(
                    self.vue,
                    "Format non supporté",
                    "Veuillez choisir une image au format PNG ou JPEG."
                )
                return
                
            try:
                # Chargement du plan
                self.modele.charger_plan(chemin)
                self.chemin_courant = chemin
                self.vue.statusBar().showMessage('Nouveau projet créé', 2000)
            except Exception as e:
                QMessageBox.critical(
                    self.vue,
                    "Erreur",
                    f"Impossible de charger le plan : {str(e)}"
                )
    
    def ouvrir(self):
        """
        Ouvre un projet existant à partir d'un fichier.
        """
        self.vue.statusBar().showMessage('Ouverture d\'un projet...', 2000)
        
        # Ouverture de la boîte de dialogue
        chemin, _ = QFileDialog.getOpenFileName(
            self.vue,
            "Ouvrir un projet",
            DOSSIER_PROJETS,
            "Projets (*.json);;Tous les fichiers (*.*)"
        )
        
        if chemin:
            try:
                # Chargement du projet
                self.modele.charger_projet(chemin)
                self.chemin_courant = chemin
                self.vue.statusBar().showMessage('Projet ouvert avec succès', 2000)
            except Exception as e:
                QMessageBox.critical(
                    self.vue,
                    "Erreur",
                    f"Impossible d'ouvrir le projet : {str(e)}"
                )
                
    def enregistrer(self):
        """
        Enregistre les modifications du projet courant.
        """
        if not self.chemin_courant:
            return self.enregistrer_sous()
            
        try:
            # Sauvegarde du projet
            self.modele.sauvegarder(self.chemin_courant)
            self.vue.statusBar().showMessage('Projet enregistré', 2000)
        except Exception as e:
            QMessageBox.critical(
                self.vue,
                "Erreur",
                f"Impossible d'enregistrer le projet : {str(e)}"
            )
            
    def enregistrer_sous(self):
        """
        Enregistre le projet sous un nouveau nom.
        """
        self.vue.statusBar().showMessage('Enregistrement du projet...', 2000)
        
        # Ouverture de la boîte de dialogue
        chemin, _ = QFileDialog.getSaveFileName(
            self.vue,
            "Enregistrer le projet",
            DOSSIER_PROJETS,
            "Projets (*.json);;Tous les fichiers (*.*)"
        )
        
        if chemin:
            try:
                # Sauvegarde du projet
                self.modele.sauvegarder(chemin)
                self.chemin_courant = chemin
                self.vue.statusBar().showMessage('Projet enregistré', 2000)
            except Exception as e:
                QMessageBox.critical(
                    self.vue,
                    "Erreur",
                    f"Impossible d'enregistrer le projet : {str(e)}"
                )
            
    def initZoom(self):
        """
        Réinitialise le zoom pour afficher le plan entier.
        """
        self.vue.view_scene.setTransform(QTransform()) 
        self.vue.view_scene.fitInView(
            self.vue.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        ) 