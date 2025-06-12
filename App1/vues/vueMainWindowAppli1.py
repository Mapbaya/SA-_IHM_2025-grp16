from PyQt6.QtWidgets import QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton, QStatusBar, QToolBar
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

from constantes import Constantes
from vues.vueScenePlan import ScenePlan
from vues.vueInteraction import VueInteraction
from styles import (WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        DOCK_STYLE, GRAPHICS_VIEW_STYLE, COLORS)




class MainWindowAppli1(QMainWindow):
    """
    La fenêtre principale qui affiche le projet.
    Elle contient le plan, les outils pour le manipuler,
    et bientôt les fonctions pour placer les produits !
    """
    
    signalNouveauProjet = pyqtSignal()
    signalOuvrirProjet = pyqtSignal()
    signalEnregistrerProjet = pyqtSignal()
    signalQuitter = pyqtSignal()
    signalInitZoom = pyqtSignal()
       
    
    def __init__(self, projet, parent=None):
        super().__init__(parent)
        
        self.projet = projet
        self.parent = parent
        

        
        # Style global de la fenêtre
        self.setStyleSheet(WINDOW_STYLE)

        try:
            self.setWindowTitle("Fenetre affichage plan")
            #self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_but.png'))
            #self.setGeometry(100, 100, 500, 300)



            # On prépare la scène avec le plan
            print(f"Création de la scène avec le plan: {self.projet['chemin_plan']}")
            self.scene = ScenePlan(
                self.projet['chemin_plan'],
            )
            
            self.view_scene = VueInteraction(self.scene) # remplace QGraphicsView(self.scene) car VueZoomSouris est un QGraphicsView
            
            # ajout au widget central
            self.setCentralWidget(self.view_scene)
            
            # dock
            self.mainDock = QDockWidget('Produits')
            self.mainDock.setStyleSheet(DOCK_STYLE)
            self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.mainDock)
            self.mainDock.setMaximumWidth(400)

            # gestion du conteneur du dock
            conteneur = QWidget()
            conteneur.setStyleSheet(f"background-color: {COLORS['surface']}; padding: 15px;")
            layout = QVBoxLayout(conteneur)
            layout.setSpacing(15)

        # Les boutons pour gérer les produits
            btn_selectionner = QPushButton("Sélectionner les produits")
            btn_selectionner.setStyleSheet(BUTTON_STYLE)
            btn_selectionner.clicked.connect(self.selectionner_produits)
            layout.addWidget(btn_selectionner)
            
            btn_placer = QPushButton("Placer les produits")
            btn_placer.setStyleSheet(BUTTON_STYLE)
            btn_placer.clicked.connect(self.placer_produits)
            layout.addWidget(btn_placer)
            
            # Un bouton pour revenir à la liste des projets
            btn_retour = QPushButton("Retour à la liste")
            btn_retour.setStyleSheet(BUTTON_SECONDARY_STYLE)
            btn_retour.clicked.connect(self.retour_liste)
            layout.addWidget(btn_retour)
            
            # Contraintes de taille
            conteneur.setMinimumWidth(200)
            
            # Ajouter le conteneur dans le dock
            self.mainDock.setWidget(conteneur)
        

            # barre d'état
            self.barreEtat = QStatusBar()
            self.setStatusBar(self.barreEtat)
            self.barreEtat.showMessage("Lancement de la création de projet ...", 3000)
            self.barreEtat.showMessage(
                    f"Projet: {self.projet['nom']} | "
                    f"Magasin: {self.projet['magasin']} | "
                    f"Auteur: {self.projet['auteur']}"
                )

            # barre de menu
            menuBarre = self.menuBar()
            menuFichier = menuBarre.addMenu('&Fichier')
            menuEdition = menuBarre.addMenu('&Edition')
            menuAffichage = menuBarre.addMenu('&Affichage')
            menuAide = menuBarre.addMenu('&Aide')

            # ajout d'une barre d'outils
            barre_outil = QToolBar('Principaux outils')
            self.addToolBar(barre_outil)

            '''__________________________________________________________________
                                    Gestion du Menu
            _____________________________________________________________________'''
            # Ajout des éléments de menus + raccourcis clavier + Barre boutons
            # MENU FICHIER
            actionNouveau = QAction(QIcon(Constantes.CHEMIN_ICONES + 'newFile.png'), 'Nouveau Projet', self)
            actionNouveau.setShortcut('Ctrl+N')
            actionNouveau.triggered.connect(self.signalNouveauProjet.emit)
            menuFichier.addAction(actionNouveau)
            barre_outil.addAction(actionNouveau)
            
            actionOuvrir = QAction(QIcon(Constantes.CHEMIN_ICONES + 'openFile.png'), 'Ouvrir', self)
            actionOuvrir.setShortcut('Ctrl+O')
            actionOuvrir.triggered.connect(self.signalOuvrirProjet.emit)
            menuFichier.addAction(actionOuvrir)
            barre_outil.addAction(actionOuvrir)   
            
            actionSauvegarder = QAction(QIcon(Constantes.CHEMIN_ICONES + 'save.png'), 'Enregistrer', self)
            actionSauvegarder.setShortcut('Ctrl+S')
            actionSauvegarder.triggered.connect(self.signalEnregistrerProjet.emit)
            menuFichier.addAction(actionSauvegarder)
            barre_outil.addAction(actionSauvegarder)  
            
            menuFichier.addSeparator()
            
            actionQuitter = QAction(QIcon(Constantes.CHEMIN_ICONES + 'suppress.png'), 'Quitter', self)
            actionQuitter.setShortcut('Ctrl+Q')
            actionQuitter.triggered.connect(self.signalQuitter.emit)
            menuFichier.addAction(actionQuitter)
            barre_outil.addAction(actionQuitter)     
            
            barre_outil.addSeparator()  
            
            # MENU EDITION
            actionPrecedent = QAction(QIcon(Constantes.CHEMIN_ICONES + 'flechePrecedent.png'), 'Précédent', self)
            actionPrecedent.setShortcut('Ctrl+Z')
            # action_retablir.triggered.connect(self.text_edit.undo)
            menuEdition.addAction(actionPrecedent)
            barre_outil.addAction(actionPrecedent)
            
            actionSuivant = QAction(QIcon(Constantes.CHEMIN_ICONES + 'flecheSuivant.png'), 'Suivant', self)
            actionSuivant.setShortcut('Ctrl+Y')
            # action_retablir.triggered.connect(self.text_edit.redo)
            menuEdition.addAction(actionSuivant)
            barre_outil.addAction(actionSuivant)
            
            menuFichier.addSeparator()
            
            barre_outil.addSeparator() 

            # MENU AFFICHAGE
            actionInitZoom = QAction(QIcon(Constantes.CHEMIN_ICONES + 'initZoom.png'), 'Initialisation Zoom', self)
            actionInitZoom.setShortcut('Ctrl+0')
            actionInitZoom.triggered.connect(self.signalInitZoom.emit)
            menuAffichage.addAction(actionInitZoom)
            barre_outil.addAction(actionInitZoom)
            # TODO 
            # Gérer les thèmes
            # Gérer la taille des barres de boutons
            
            
            # MENU EDITION
            # TODO
            # Aide à l'utilisation
            # FAQ?
            
            self.showMaximized()
        
        except Exception as e:
            print(f"Oups ! Problème lors de l'initialisation de la vue: {str(e)}")
            raise


    # fonction redimensionnant automatiquement la scene en fonction de la dimension de la fenetre. methode héritant de QWidget
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view_scene.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


    def selectionner_produits(self):
        """
        Cette fonction permettra bientôt de choisir les produits
        à placer dans le magasin
        """
        self.barre_etat.showMessage("La sélection des produits arrive bientôt !", 3000)
        
    def placer_produits(self):
        """
        Cette fonction permettra bientôt de placer les produits
        sur le plan du magasin
        """
        self.barre_etat.showMessage("Le placement des produits arrive bientôt !", 3000)
        
    def retour_liste(self):
        """
        Ferme la vue du projet et revient à la liste des projets
        """
        if self.parent:
            self.parent.show()
        self.close() 