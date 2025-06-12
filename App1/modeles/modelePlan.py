"""
Modèle de données pour le plan de magasin.

Ce module gère les données du plan, notamment :
- Le chargement et la sauvegarde du plan
- Les informations sur les zones
- Les produits associés aux zones
"""

import os
import json
from PyQt6.QtGui import QImage
from config import DOSSIER_PROJETS


class ModelePlan:
    """
    Modèle de données pour le plan de magasin.
    
    Gère l'état et les données du plan, y compris :
    - L'image du plan
    - Les zones définies
    - Les produits par zone
    """
    
    def __init__(self):
        """Initialise un nouveau modèle de plan."""
        self.image_plan = None
        self.zones = {}  # Dictionnaire des zones avec leurs produits
        self.nom_projet = None
        self.chemin_plan = None
        
    def charger_plan(self, chemin):
        """
        Charge une nouvelle image de plan.
        
        Args:
            chemin: Chemin vers le fichier image du plan
            
        Raises:
            ValueError: Si le fichier est invalide ou illisible
        """
        # Vérification du fichier
        if not os.path.isfile(chemin):
            raise ValueError(f"Le fichier n'existe pas : {chemin}")
            
        # Chargement de l'image
        image = QImage(chemin)
        if image.isNull():
            raise ValueError(f"Format d'image non supporté : {chemin}")
            
        # Mise à jour du modèle
        self.image_plan = image
        self.chemin_plan = chemin
        self.zones.clear()
        
    def charger_projet(self, chemin):
        """
        Charge un projet existant.
        
        Args:
            chemin: Chemin vers le fichier de configuration du projet
            
        Raises:
            ValueError: Si le projet est invalide ou corrompu
        """
        try:
            # Lecture du fichier de configuration
            with open(chemin, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Validation de la structure
            if not all(k in config for k in ['nom', 'chemin_plan', 'zones']):
                raise ValueError("Format de projet invalide")
                
            # Chargement du plan
            self.charger_plan(config['chemin_plan'])
            
            # Mise à jour du modèle
            self.nom_projet = config['nom']
            self.zones = config['zones']
            
        except json.JSONDecodeError:
            raise ValueError("Fichier de projet corrompu")
        except Exception as e:
            raise ValueError(f"Erreur lors du chargement : {str(e)}")
            
    def sauvegarder(self, chemin):
        """
        Sauvegarde l'état actuel du projet.
        
        Args:
            chemin: Chemin où sauvegarder le projet
            
        Raises:
            ValueError: Si la sauvegarde échoue
        """
        if not self.image_plan:
            raise ValueError("Aucun plan à sauvegarder")
            
        try:
            # Préparation des données
            config = {
                'nom': self.nom_projet or os.path.splitext(os.path.basename(chemin))[0],
                'chemin_plan': self.chemin_plan,
                'zones': self.zones
            }
            
            # Sauvegarde du fichier
            with open(chemin, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            raise ValueError(f"Erreur lors de la sauvegarde : {str(e)}")
            
    def definir_produits_zone(self, zone, produits):
        """
        Définit les produits pour une zone donnée.
        
        Args:
            zone: Identifiant de la zone (ex: "A1")
            produits: Liste des produits à placer dans la zone
        """
        if produits:
            self.zones[zone] = produits
        elif zone in self.zones:
            del self.zones[zone]
            
    def obtenir_produits_zone(self, zone):
        """
        Récupère les produits d'une zone donnée.
        
        Args:
            zone: Identifiant de la zone (ex: "A1")
            
        Returns:
            Liste des produits dans la zone
        """
        return self.zones.get(zone, [])