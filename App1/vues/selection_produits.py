"""
Interface de sélection et gestion des produits par zone.

Fonctionnalités principales :
- Gestion des produits par zone (maximum 5)
- Organisation hiérarchique par catégories
- Validation des contraintes de placement
- Gestion des conflits d'attribution
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QTreeWidget, QTreeWidgetItem, QLabel, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal
from modeles.modelePlan import ModelePlan
import json
import os

class SelectionProduits(QWidget):
    """
    Interface de gestion des produits par zone.
    
    Caractéristiques :
    - Limite de 5 produits par zone
    - Organisation hiérarchique par catégories
    - Validation des contraintes d'unicité
    """
    
    # Signal émis lors d'une modification de sélection
    selection_changee = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mes_produits = []        # Produits sélectionnés
        self.ma_case = None          # Zone en cours d'édition
        
        # Récupération du gestionnaire de projet
        self.mon_projet = None
        if hasattr(parent, 'gestion_projet'):
            self.mon_projet = parent.gestion_projet
            
        self.initialiser_interface()
        self.charger_produits()
        self.modele_plan = ModelePlan()
        
    def initialiser_interface(self):
        """
        Configuration de l'interface utilisateur avec ses composants.
        """
        mon_layout = QVBoxLayout(self)
        mon_layout.setSpacing(10)
        
        # Zone d'information
        self.texte_info = QLabel("Sélectionnez une zone sur le plan")
        mon_layout.addWidget(self.texte_info)
        
        # Arborescence des produits
        self.liste_produits = QTreeWidget()
        self.liste_produits.setHeaderLabel("Produits disponibles")
        
        # Zone de défilement
        ma_zone_defilement = QScrollArea()
        ma_zone_defilement.setWidget(self.liste_produits)
        ma_zone_defilement.setWidgetResizable(True)
        mon_layout.addWidget(ma_zone_defilement)
        
        # Boutons d'action
        self.bouton_ok = QPushButton("Valider la sélection")
        self.bouton_ok.clicked.connect(self.valider_selection)
        self.bouton_ok.setEnabled(False)
        mon_layout.addWidget(self.bouton_ok)
        
        self.bouton_vider = QPushButton("Vider la zone")
        self.bouton_vider.clicked.connect(self.vider_zone)
        self.bouton_vider.setEnabled(False)
        mon_layout.addWidget(self.bouton_vider)
        
        # Connexion des signaux
        self.liste_produits.itemChanged.connect(self.gerer_selection_produit)
        
    def charger_produits(self):
        """
        Charge la liste des produits depuis le fichier de données
        et applique les contraintes d'utilisation.
        """
        try:
            self.liste_produits.clear() #empeche les doublons
            # Chargement du fichier de données en utilisant os.path.join pour la compatibilité
            mon_fichier = os.path.join("App1", "list", "liste_produits_original.json")
            mon_fichier = os.path.normpath(mon_fichier)  # Normalise le chemin selon l'OS
            
            with open(mon_fichier, 'r', encoding='utf-8') as f:
                mes_categories = json.load(f)
                
            # Récupération des produits déjà placés
            produits_utilises = []
            if self.mon_projet:
                # On exclut les produits de la case en cours d'édition
                tous_produits = self.mon_projet.obtenir_tous_produits_places()
                produits_case_actuelle = self.mon_projet.obtenir_produits_case(self.ma_case) if self.ma_case else []
                produits_utilises = [p for p in tous_produits if p not in produits_case_actuelle]
                
            # Construction de l'arborescence
            for categorie, produits in mes_categories.items():
                # Création de la catégorie
                item_categorie = QTreeWidgetItem(self.liste_produits)
                item_categorie.setText(0, categorie)
                item_categorie.setFlags(item_categorie.flags() | Qt.ItemFlag.ItemIsEnabled)
                
                # Ajout des produits
                for produit in produits:
                    item_produit = QTreeWidgetItem(item_categorie)
                    item_produit.setText(0, produit)
                    
                    # Gestion des produits déjà utilisés
                    if produit in produits_utilises:
                        case_utilisee = self.mon_projet.trouver_case_produit(produit)
                        
                        flags = item_produit.flags()
                        flags &= ~Qt.ItemFlag.ItemIsUserCheckable  # empêche de cocher
                        flags &= ~Qt.ItemFlag.ItemIsSelectable     # empêche la sélection
                        # flags &= ~Qt.ItemFlag.ItemIsEnabled      # ne pas désactiver complètement
                        item_produit.setFlags(flags)

                        item_produit.setText(0, f"{produit} (utilisé en {case_utilisee})")
                        item_produit.setToolTip(0, f"Produit déjà placé dans la case {case_utilisee}")
                    else:
                        item_produit.setFlags(item_produit.flags() | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable)
                        item_produit.setCheckState(0, Qt.CheckState.Unchecked)
                    
        except Exception as e:
            print(f"Erreur lors du chargement des produits : {str(e)}")
    
    def filtrer_produits_par_categorie(self):
        for i in range(self.liste_produits.topLevelItemCount()):
            categorie = self.liste_produits.topLevelItem(i)
            cat_nom = categorie.text(0)
            
            # Si la catégorie n'est pas autorisée, on désactive tous ses produits
            autorisee = cat_nom in self.categories_autorisees
            
             # On cache la catégorie si elle n'est pas autorisée ou si elle n'a aucun produit visible
            any_produit_visible = False
        
            for j in range(categorie.childCount()):
                produit = categorie.child(j)
                
                # On affiche seulement les produits dont la catégorie est autorisée
                # et qui ne sont pas déjà utilisés ailleurs
                if autorisee and (produit.flags() & Qt.ItemFlag.ItemIsEnabled):
                    produit.setHidden(False)
                    produit.setFlags(produit.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                    # reset le check si besoin
                    produit.setCheckState(0, Qt.CheckState.Unchecked)
                    any_produit_visible = True
                else:
                    produit.setHidden(True)
        
            # Si aucune produit visible, on cache la catégorie entière
            categorie.setHidden(not any_produit_visible)
            
    def choisir_case(self, case):
        """
        Met à jour l'interface pour une nouvelle zone sélectionnée.
        
        Args:
            case: Référence de la zone sélectionnée
        """
        self.ma_case = case
        
        # On verifie si la case selectionnee peuvent recevoir des produits (pas de cses vides et pas de cases Caisses)
        if self.modele_plan:
            cases_valides = self.modele_plan.liste_cases_occupees_sans_caisse()
            if case not in cases_valides:
                QMessageBox.warning(self, "Zone invalide", f"La case {case} ne correspond à aucun rayon défini.")
                self.ma_case = None
                self.texte_info.setText("Sélectionnez une zone valide sur le plan")
                self.bouton_ok.setEnabled(False)
                self.bouton_vider.setEnabled(False)
                return
            
            # récupérer les catégories autorisées pour la case
            self.categories_autorisees = self.modele_plan.categories_autorisees_pour_case(case)

        
        self.mes_produits = []
        
        # Vérification du gestionnaire de projet
        if not self.mon_projet:
            if hasattr(self.parent(), 'gestion_projet'):
                self.mon_projet = self.parent().gestion_projet
            else:
                return
            
        try:
            # Récupération des produits existants
            produits_dedans = self.mon_projet.obtenir_produits_case(case)
            
            if produits_dedans:
                self.mes_produits = produits_dedans.copy()
                self.bouton_vider.setEnabled(True)
            else:
                self.bouton_vider.setEnabled(False)
        except Exception as e:
            QMessageBox.warning(self, "Erreur", "Impossible de récupérer les produits de la zone.")
            return
        
        self.filtrer_produits_par_categorie()
            
        # Cocher les produits déjà sélectionnés, uniquement s'ils sont visibles
        self.en_train_de_modifier = True
        self.reinitialiser_selection() # décoche tout
        
            
        for i in range(self.liste_produits.topLevelItemCount()):
            categorie = self.liste_produits.topLevelItem(i)
            for j in range(categorie.childCount()):
                produit = categorie.child(j)
                if produit.isHidden():
                    continue  # ignore les produits cachés
                
                nom_produit = produit.text(0).split(" (utilisé")[0]
                if nom_produit in self.mes_produits:
                    produit.setCheckState(0, Qt.CheckState.Checked)
                else:
                    produit.setCheckState(0, Qt.CheckState.Unchecked)
                            
        self.en_train_de_modifier = False
        
        # Activation des contrôles
        self.bouton_ok.setEnabled(True)
        
        # Mise à jour des informations
        self.actualiser_informations()
        
    def actualiser_informations(self):
        """
        Met à jour l'affichage des informations sur la zone courante.
        """
        if not self.ma_case:
            self.texte_info.setText("Sélectionnez une zone sur le plan")
            return
            
        if not self.mes_produits:
            self.texte_info.setText(f"Zone {self.ma_case} : Aucun produit")
            return
            
        # Élimination des doublons tout en préservant l'ordre
        produits_uniques = []
        for produit in self.mes_produits:
            if produit not in produits_uniques:
                produits_uniques.append(produit)
            
        # Affichage des produits
        mes_produits_str = ", ".join(produits_uniques)
        mon_texte = (f"Zone {self.ma_case}\n"
                f"Produits actuels ({len(produits_uniques)}/5) :\n"
                f"{mes_produits_str}")
        self.texte_info.setText(mon_texte)
        
    def gerer_selection_produit(self, item, column):
        """
        Gère les événements de sélection/désélection d'un produit.
        
        Applique les règles de validation :
        - Maximum 5 produits par zone
        - Unicité des produits sur le plan
        """
        if item.parent() is None or getattr(self, 'en_train_de_modifier', False):
            return
            
        if not self.ma_case:
            item.setCheckState(0, Qt.CheckState.Unchecked)
            self.texte_info.setText("Sélectionnez d'abord une zone sur le plan")
            return
            
            
        categorie_parente = item.parent()
        if categorie_parente:
            nom_categorie = categorie_parente.text(0)
            if nom_categorie not in self.categories_autorisees:
                item.setCheckState(0, Qt.CheckState.Unchecked)
                # QMessageBox.warning(self, "Produit non autorisé",
                #                     f"Le produit '{item.text(0)}' n'est pas autorisé dans cette zone.")
                return
        
        
        # Récupération du nom du produit sans le suffixe "(utilisé en...)"
        nom_produit = item.text(0).split(" (utilisé")[0]
        
        # Vérification de l'unicité seulement si le produit est coché
        if item.checkState(0) == Qt.CheckState.Checked and self.mon_projet:
            case_utilisee = self.mon_projet.trouver_case_produit(nom_produit)
            if case_utilisee and case_utilisee != self.ma_case:
                item.setCheckState(0, Qt.CheckState.Unchecked)
                # QMessageBox.warning(self, "Produit déjà attribué",
                #     f"Le produit '{nom_produit}' est déjà présent en zone {case_utilisee}")
                return
            
        # Compte le nombre de produits actuellement sélectionnés
        produits_selectionnes = []
        for i in range(self.liste_produits.topLevelItemCount()):
            categorie = self.liste_produits.topLevelItem(i)
            for j in range(categorie.childCount()):
                produit = categorie.child(j)
                if produit.checkState(0) == Qt.CheckState.Checked:
                    nom = produit.text(0).split(" (utilisé")[0]
                    if nom not in produits_selectionnes:  # Évite les doublons
                        produits_selectionnes.append(nom)
        
        # Si on essaie d'ajouter un produit et qu'on dépasse la limite
        if item.checkState(0) == Qt.CheckState.Checked and len(produits_selectionnes) > 5:
            item.setCheckState(0, Qt.CheckState.Unchecked)
            QMessageBox.warning(self, "Limite atteinte",
                f"Maximum 5 produits par zone. Vous avez actuellement {len(produits_selectionnes)-1} produits.")
            return
            
        # Détection des modifications pour activer/désactiver le bouton de validation
        self.bouton_ok.setEnabled(set(produits_selectionnes) != set(self.mes_produits))
        
    def valider_selection(self):
        """
        Valide et sauvegarde la sélection courante de produits.
        """
        if not self.ma_case:
            return
            
        # Vérification du gestionnaire de projet
        if not self.mon_projet:
            if hasattr(self.parent(), 'gestion_projet'):
                self.mon_projet = self.parent().gestion_projet
            else:
                QMessageBox.warning(self, "Erreur",
                    "Gestionnaire de projet non trouvé")
                return
            
        # Récupération de la sélection
        nouveaux_choix = []
        for i in range(self.liste_produits.topLevelItemCount()):
            categorie = self.liste_produits.topLevelItem(i)
            for j in range(categorie.childCount()):
                produit = categorie.child(j)
                if produit.checkState(0) == Qt.CheckState.Checked:
                    nom = produit.text(0).split(" (utilisé")[0]
                    if nom not in nouveaux_choix:  # Évite les doublons
                        nouveaux_choix.append(nom)
                    
        if set(nouveaux_choix) == set(self.mes_produits):
            return  # Aucune modification
            
        # Vérification de la limite
        if len(nouveaux_choix) > 5:
            QMessageBox.warning(self, "Erreur",
                "Maximum 5 produits par zone.")
            return
            
        # Demande de confirmation
        msg = f"Confirmer l'attribution des produits à la zone {self.ma_case} ?\n\n"
        msg += f"Produits sélectionnés ({len(nouveaux_choix)}/5) :\n"
        msg += ", ".join(nouveaux_choix)
        
        reponse = QMessageBox.question(
            self,
            "Confirmation",
            msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reponse == QMessageBox.StandardButton.Yes:
            try:
                # Sauvegarde des modifications
                self.mon_projet.definir_produits_case(self.ma_case, nouveaux_choix)
                self.mes_produits = nouveaux_choix
                self.bouton_ok.setEnabled(False)
                self.actualiser_informations()
                self.selection_changee.emit(nouveaux_choix)
                
                # Mise à jour de l'interface
                self.charger_produits()
                self.choisir_case(self.ma_case)
            except Exception as e:
                QMessageBox.critical(self, "Erreur",
                    f"Erreur lors de la sauvegarde : {str(e)}")
                
    def vider_zone(self):
        """
        Supprime tous les produits de la zone courante.
        """
        if not self.ma_case or not self.mes_produits:
            return
            
        reponse = QMessageBox.question(
            self,
            "Confirmation",
            f"Supprimer tous les produits de la zone {self.ma_case} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reponse == QMessageBox.StandardButton.Yes:
            try:
                self.mon_projet.definir_produits_case(self.ma_case, [])
                self.mes_produits = []
                self.bouton_ok.setEnabled(False)
                self.bouton_vider.setEnabled(False)
                self.actualiser_informations()
                self.selection_changee.emit([])
                
                # Mise à jour de l'interface
                self.charger_produits()
                self.choisir_case(self.ma_case)
            except Exception as e:
                QMessageBox.critical(self, "Erreur",
                    f"Erreur lors de la suppression : {str(e)}")
                
    def reinitialiser_selection(self):
        """
        Réinitialise l'état de sélection de tous les produits.
        """
        for i in range(self.liste_produits.topLevelItemCount()):
            categorie = self.liste_produits.topLevelItem(i)
            for j in range(categorie.childCount()):
                produit = categorie.child(j)
                if produit.flags() & Qt.ItemFlag.ItemIsUserCheckable:
                    produit.setCheckState(0, Qt.CheckState.Unchecked) 