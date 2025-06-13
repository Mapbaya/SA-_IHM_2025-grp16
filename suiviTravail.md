# SAE IHM

Groupe 16  

* Marwa Kime  
* Neda Khelifi  
* Mathys Levitre  
* Frédéric Gobfert  


## 27/05/25  
Présentation du projet et des consignes à respecter.
Formation du groupe.
Répartition des tâches :

    Appli 1 :   Marwa Kime
                Frédéric Gobfert
                
    Appli 2 :   Neda Khelifi
                Mathys Levitre

Création du git :
    Création des nouvelles branches : 
        **appli_1MF**
        **appli_2NM**

Création du Trello.

                
## 10/06/25  

**Appli 1** :

• Création de l'interface principale  
• Gestion de l'affichage du plan  
• Gestion de la grille  
• Gestion des actions souris, zoom et dézoom en respectant le format de la grille d'affichage  
• Réflexion commune sur :

    1) Le développement à venir de la fonction "mise en rayon"
    2) Le choix d'implémentation des listes de produits
    3) L'organisation globale de l'application

## 11/06/25
**Appli 1** :

• Implémentation complète de la gestion des projets :

    • Création de nouveaux projets
    • Ouverture des projets existants
    • Suppression de projets
    • Sauvegarde automatique des configurations

• Structure de données des projets :

    • Configuration JSON pour chaque projet
    • Gestion des plans de magasin

• Nouvelles fonctionnalités :
    
    • Séparation de la première partie du code selon le modèle MVC
    • Gestion du paramétrage de la grille
    • Navigation entre les projets
    • Interface de création de projet
    • Système de confirmation pour la suppression
    • Affichage des informations du projet (nom, magasin, auteur)


## 12/06/2025
**Appli 1**:

• Liste des produits (format JSON) :

    • Affichage des produits disponibles
    • Filtrage des produits déjà utilisés
    • Limite de 5 produits par case
    
• Placement des produits :

    • Possibilité de placer les produits dans les cases
    • Sauvegarde automatique des placements (dans le fichier de sauvegarde du projet)
    • Affichage des produits déjà placés
    
• Amélioration UX :

    • Style modifié pour une meilleure lisibilité
    • Interface plus intuitive
    • Meilleure organisation visuelle

• Gestion des erreurs :

    • Messages d'erreur explicites
    • Validation des actions

## 13/06/2025
**Appli 1**:

• Fonctionnalités :

    • Placement des produits restreint à leur rayon respectif (logique métier respectée).
    • Impossible de dépasser 5 produits par case.
    • Affichage dynamique de la liste complète des produits placés dans le magasin.
    • Affichage précis de la position de chaque produit sur la grille (numéro de case).

• Interaction utilisateur :

    •  Zoom sur le plan désormais disponible (meilleure navigation dans le quadrillage).
    •  Ajout d’une barre d’état avec accès à certains raccourcis importants.
    •  Possibilité de sauvegarder rapidement depuis la barre d’état.
    • Amélioration générale de l'interface utilisateur pour la rendre plus intuitive et claire.

• Qualité & Robustesse :

    • Ajout de notifications d'erreurs : l'utilisateur est informé s'il oublie de remplir des champs lors de la création d’un projet.
    • Une notice d'utilisation claire a été rédigée.
    • Une fenêtre "À propos" a été intégrée à l'application.







