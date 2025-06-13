"""
Interface principale de gestion d'un projet de magasin.

Cette interface présente :
- Une visualisation interactive du plan du magasin
- Un gestionnaire de produits par zone
- Des outils de modification et de sauvegarde
"""
import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox, QGraphicsView, QToolBar, QStatusBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QIcon, QAction
from vues.vueScenePlan import VuePlan, ScenePlan
from vues.selection_produits import SelectionProduits
from vues.vueListeProduits import VueListeProduits
from constantes import Constantes
from styles import WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE, TITLE_LABEL_STYLE
from vues.notice_utilisation import NoticeUtilisation

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


        self.barre_etat = QStatusBar()
        self.setStatusBar(self.barre_etat)
        self.barre_etat.showMessage("Projet chargé.")
        
    def initialiser_interface(self):
        """
        Configure l'interface utilisateur avec l'ensemble des composants
        nécessaires à la gestion du projet.
        """
        # Initialisation du widget principal
        self.initialiser_menu()
        self.initialiser_toolbar()
        self.ajouter_raccourcis()


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


    def initialiser_menu(self):
        menu_bar = self.menuBar()
        menuFichier = menu_bar.addMenu('&Fichier')
        menuEdition = menu_bar.addMenu('&Edition')
        menuAffichage = menu_bar.addMenu('&Affichage')
        menuAide = menu_bar.addMenu('&Aide')
        
        action_notice = QAction("Notice d'utilisation", self)
        action_notice.setShortcut("F1")  # Raccourci clavier standard pour l'aide
        action_notice.triggered.connect(self.afficher_notice)
        menuAide.addAction(action_notice)

        action_sauvegarder = QAction("Enregistrer", self)
        action_sauvegarder.setShortcut("Ctrl+S")
        action_sauvegarder.triggered.connect(self.sauvegarder_projet)
        menuFichier.addAction(action_sauvegarder)

        action_quitter = QAction("Quitter", self)
        action_quitter.setShortcut("Ctrl+Q")
        action_quitter.triggered.connect(self.retourner_liste)
        menuFichier.addAction(action_quitter)

        # Ajout de l'action Vue générale dans Affichage
        action_vue_generale = QAction("Vue générale", self)
        action_vue_generale.setShortcut("Ctrl+0")
        action_vue_generale.triggered.connect(lambda: self.ma_vue_plan.set_vue_generale(True))
        menuAffichage.addAction(action_vue_generale)

        # Ajout de l'action Activer le zoom dans Affichage
        action_zoom = QAction("Activer le zoom", self)
        action_zoom.setShortcut("Ctrl+Z")
        action_zoom.triggered.connect(lambda: self.ma_vue_plan.set_vue_generale(False))
        menuAffichage.addAction(action_zoom)
        
        action_a_propos = QAction("A Propos ?", self)
        action_a_propos.triggered.connect(self.afficher_a_propos)
        menuAide.addAction(action_a_propos)


    def initialiser_toolbar(self):
        toolbar = QToolBar("Outils rapides")
        self.addToolBar(toolbar)
        print("CHEMIN_ICONES =", Constantes.CHEMIN_ICONES)
        print("Chemin complet =", os.path.join(Constantes.CHEMIN_ICONES, 'flechePrecedent.png'))
        action_sauvegarder = QAction(QIcon(os.path.join(Constantes.CHEMIN_ICONES, 'save.png')), 'Enregistrer', self)
        action_sauvegarder.setToolTip("Sauvegarder le projet")
        action_sauvegarder.triggered.connect(self.sauvegarder_projet)
        toolbar.addAction(action_sauvegarder)

        action_retour = QAction(QIcon(os.path.join(Constantes.CHEMIN_ICONES, 'flechePrecedent.png')), 'Précédent', self)
        action_retour.setToolTip("Retour")
        action_retour.triggered.connect(self.retourner_liste)
        toolbar.addAction(action_retour)

        # Ajout du bouton pour afficher la liste des produits
        action_liste = QAction(QIcon(os.path.join(Constantes.CHEMIN_ICONES, 'list.png')), 'Liste des produits', self)
        action_liste.setToolTip("Afficher la liste des produits")
        action_liste.triggered.connect(self.afficher_liste_produits)
        toolbar.addAction(action_liste)


    def ajouter_raccourcis(self):
        sauvegarde_rapide = QAction(self)
        sauvegarde_rapide.setShortcut("Ctrl+S")
        sauvegarde_rapide.triggered.connect(self.sauvegarder_projet)
        self.addAction(sauvegarde_rapide)

        quitter_rapide = QAction(self)
        quitter_rapide.setShortcut("Ctrl+Q")
        quitter_rapide.triggered.connect(self.retourner_liste)
        self.addAction(quitter_rapide)


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
        self.ma_vue_plan.set_vue_generale(True)
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
        self.barre_etat.showMessage("Projet sauvegardé avec succès", 3000)
            
    def retourner_liste(self):
        """
        Retourne à l'interface de gestion des projets.
        """
        if self.parent:
            self.parent.show()
        self.close() 

    def afficher_liste_produits(self):
        """
        Affiche la fenêtre de liste des produits.
        """
        dialogue = VueListeProduits(self.gestion_projet, self)
        dialogue.exec()

    def activer_zoom_plan(self):
        """
        Active le zoom sur le plan.
        """
        pass 
    
    def afficher_notice(self):
        """
        Affiche la notice d'utilisation
        """
        notice = NoticeUtilisation(self)
        notice.exec()

    def ajouter_produit_dans_case(self, case, produit, categorie):
        """
        Tente d’ajouter un produit dans une case donnée après validation.
        """
        modele = self.ma_vue_plan.scene_plan.modele
        if not modele.categorie_autorisee(case, categorie):
            QMessageBox.warning(self, "Placement interdit",
                f"La catégorie '{categorie}' n’est pas autorisée dans la case {case}.")
            return

        produits_existants = self.gestion_projet.obtenir_produits_case(case)
        if produit in produits_existants:
            QMessageBox.information(self, "Déjà présent", f"Le produit '{produit}' est déjà placé dans la case {case}.")
            return

        produits_existants.append(produit)
        self.gestion_projet.definir_produits_case(case, produits_existants)
        self.actualiser_plan([])       
    
    def afficher_a_propos(self):
        QMessageBox.information(
            self,
            "À propos",
            "<h3>Application Mon Magasin v1.0.19</h3>"
            "<p><b>Dernière mise à jour :</b> 14 juin 2025</p>"
            "<p><b>Créateurs :</b></p>"
            "<ul>"
            "<li>Marwa Kime – Cheffe de projet / Développeuse</li>"
            "<li>Neda Khelifi – Développeuse</li>"
            "<li>Mathys Levitre – Développeur</li>"
            "<li>Frédéric Gobfert – Développeur</li>"
            "</ul>",
            QMessageBox.StandardButton.Ok
        )
