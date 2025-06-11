"""
Configuration globale de l'application.

Ce fichier contient les constantes et paramètres de configuration
utilisés dans toute l'application.
"""

import os
import json

# Chemins des dossiers
DOSSIER_PROJETS = 'projets'
DOSSIER_DATA = 'data'
DOSSIER_IMAGES = 'images'

# Fichiers partagés
FICHIER_PRODUITS = os.path.join(DOSSIER_DATA, "produits.json")

def creer_dossier_si_necessaire(chemin):
    """
    Crée un dossier s'il n'existe pas déjà.
    Retourne True si le dossier a été créé, False s'il existait déjà.
    """
    if not os.path.exists(chemin):
        os.makedirs(chemin)
        return True
    return False

def obtenir_chemin_data(nom_fichier):
    """
    Retourne le chemin complet d'un fichier dans le dossier data.
    Crée le dossier data si nécessaire.
    """
    creer_dossier_si_necessaire(DOSSIER_DATA)
    return os.path.join(DOSSIER_DATA, nom_fichier)

def obtenir_chemin_image(nom_fichier):
    """
    Retourne le chemin complet d'un fichier dans le dossier images.
    Crée le dossier images si nécessaire.
    """
    creer_dossier_si_necessaire(DOSSIER_IMAGES)
    return os.path.join(DOSSIER_IMAGES, nom_fichier)

def obtenir_chemin_projet(nom_projet):
    """
    Retourne le chemin complet d'un projet.
    Crée le dossier projets si nécessaire.
    """
    creer_dossier_si_necessaire(DOSSIER_PROJETS)
    return os.path.join(DOSSIER_PROJETS, nom_projet)

# Configuration de l'interface
TAILLE_QUADRILLAGE_MIN = 50
TAILLE_QUADRILLAGE_MAX = 200
TAILLE_QUADRILLAGE_DEFAUT = 100

# Types de fichiers acceptés
EXTENSIONS_IMAGES = ['.png', '.jpg', '.jpeg']

def charger_produits():
    """Charge la liste des produits depuis le fichier JSON"""
    try:
        with open(FICHIER_PRODUITS, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def sauvegarder_produits(produits):
    """Sauvegarde la liste des produits dans le fichier JSON"""
    with open(FICHIER_PRODUITS, 'w', encoding='utf-8') as f:
        json.dump(produits, f, indent=4, ensure_ascii=False) 