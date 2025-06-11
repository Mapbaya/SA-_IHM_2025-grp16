"""
Gestionnaire de projets de magasin.

Ce module constitue le cœur de l'application, gérant le cycle de vie complet
des projets de magasin. Il assure :
- La création sécurisée de nouveaux projets
- Le chargement et la validation des projets existants
- La gestion des ressources (plans, configurations)
- La suppression sécurisée des projets
"""

import os
import json
import shutil
from datetime import datetime
from config import DOSSIER_PROJETS

class GestionProjet:
    """
    Gestionnaire central des projets de magasin.
    
    Cette classe assure la gestion complète des projets, garantissant
    l'intégrité des données et la cohérence des fichiers associés.
    Elle maintient une structure organisée des projets et de leurs ressources.
    """
    def __init__(self):
        """
        Initialise le gestionnaire de projets.
        """
        self.projet_courant = None
        
    def creer_projet(self, nom, magasin, auteur, chemin_plan, taille_quadrillage=100):
        """
        Crée un nouveau projet de magasin avec ses ressources associées.
        
        Cette méthode :
        1. Vérifie la disponibilité du nom de projet
        2. Crée une structure de dossiers dédiée
        3. Copie et organise les ressources nécessaires
        4. Génère et sauvegarde la configuration initiale
        
        Args:
            nom: Nom unique du projet
            magasin: Nom du magasin
            auteur: Nom de l'auteur du projet
            chemin_plan: Chemin vers le fichier du plan
            taille_quadrillage: Taille du quadrillage en pixels (défaut: 100)
            
        Returns:
            dict: Configuration complète du projet créé
            
        Raises:
            ValueError: Si le nom de projet est déjà utilisé
        """
        # Vérification et création du dossier principal
        if not os.path.exists(DOSSIER_PROJETS):
            os.makedirs(DOSSIER_PROJETS)
            
        # Préparation du dossier projet
        dossier_projet = os.path.join(DOSSIER_PROJETS, nom)
        
        # Vérification de l'unicité du nom
        if os.path.exists(dossier_projet):
            raise ValueError(f"Un projet nommé '{nom}' existe déjà")
            
        # Création de la structure du projet
        os.makedirs(dossier_projet)
        
        # Copie et organisation des ressources
        nom_fichier = os.path.basename(chemin_plan)
        nouveau_chemin = os.path.join(dossier_projet, nom_fichier)
        shutil.copy2(chemin_plan, nouveau_chemin)
        
        # Génération de la configuration initiale
        config = {
            'nom': nom,
            'magasin': magasin,
            'auteur': auteur,
            'date_creation': datetime.now().strftime("%d/%m/%Y"),
            'chemin_plan': nouveau_chemin,
            'taille_quadrillage': taille_quadrillage,
            'produits': []
        }
        
        # Sauvegarde de la configuration
        chemin_config = os.path.join(dossier_projet, 'config.json')
        with open(chemin_config, 'w') as f:
            json.dump(config, f, indent=4)
            
        return config
        
    def charger_projet(self, nom):
        """
        Charge et valide un projet existant.
        
        Cette méthode :
        1. Vérifie l'existence du projet
        2. Valide l'intégrité des fichiers
        3. Met à jour les anciens formats si nécessaire
        4. Vérifie la présence des ressources requises
        
        Args:
            nom: Nom du projet à charger
            
        Returns:
            dict: Configuration complète du projet
            
        Raises:
            ValueError: Si le projet est introuvable ou corrompu
        """
        # Localisation du projet
        dossier_projet = os.path.join(DOSSIER_PROJETS, nom)
        
        # Vérification de l'existence
        if not os.path.exists(dossier_projet):
            raise ValueError(f"Le projet '{nom}' n'existe pas")
            
        # Chargement de la configuration
        chemin_config = os.path.join(dossier_projet, 'config.json')
        
        if not os.path.exists(chemin_config):
            raise ValueError(f"Le fichier de configuration du projet '{nom}' est manquant")
            
        # Lecture et validation
        with open(chemin_config, 'r') as f:
            config = json.load(f)
            
        # Migration des anciens formats
        if 'plan' in config and 'chemin_plan' not in config:
            config['chemin_plan'] = os.path.join(dossier_projet, config['plan'])
            del config['plan']
            with open(chemin_config, 'w') as f:
                json.dump(config, f, indent=4)
            
        # Vérification des ressources
        if not os.path.exists(config['chemin_plan']):
            nom_fichier = os.path.basename(config['chemin_plan'])
            nouveau_chemin = os.path.join(dossier_projet, nom_fichier)
            if os.path.exists(nouveau_chemin):
                config['chemin_plan'] = nouveau_chemin
            else:
                raise ValueError(f"Le fichier du plan est manquant: {config['chemin_plan']}")
            
        # Activation du projet
        self.projet_courant = config
        return config
        
    def supprimer_projet(self, nom):
        """
        Supprime définitivement un projet et ses ressources.
        
        Cette méthode :
        1. Vérifie l'existence du projet
        2. Supprime l'ensemble des fichiers et dossiers associés
        3. Met à jour l'état du gestionnaire si nécessaire
        
        Args:
            nom: Nom du projet à supprimer
            
        Raises:
            ValueError: Si le projet est introuvable
        """
        # Localisation du projet
        dossier_projet = os.path.join(DOSSIER_PROJETS, nom)
        
        # Vérification de l'existence
        if not os.path.exists(dossier_projet):
            raise ValueError(f"Le projet '{nom}' n'existe pas")
            
        # Suppression des ressources
        shutil.rmtree(dossier_projet)
        
        # Mise à jour de l'état
        if self.projet_courant and self.projet_courant['nom'] == nom:
            self.projet_courant = None 