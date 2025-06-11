from PyQt6.QtWidgets import QMainWindow, QDockWidget, QWidget, QVBoxLayout, QPushButton, QStatusBar, QToolBar
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

from constantes import Constantes
from vuesK.vueScenePlan import ScenePlan
from vuesK.vueInteraction import VueInteraction




class MainWindowAppli1(QMainWindow):
    signalNouveauProjet = pyqtSignal()
    signalOuvrirProjet = pyqtSignal()
    signalEnregistrerProjet = pyqtSignal()
    signalQuitter = pyqtSignal()
    signalInitZoom = pyqtSignal()
       
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Fenetre affichage plan")
        #self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_but.png'))
        #self.setGeometry(100, 100, 500, 300)

        # widget central
        # creation de la scene
        self.scene = ScenePlan()
        self.view_scene = VueInteraction(self.scene) # remplace QGraphicsView(self.scene) car VueZoomSouris est un QGraphicsView
        
        # ajout au widget central
        self.setCentralWidget(self.view_scene)
        
        # dock
        self.mainDock = QDockWidget('Outils Produits')
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.mainDock)
        self.mainDock.setMaximumWidth(400)

        # gestion du conteneur du dock
        conteneur = QWidget()
        layout = QVBoxLayout(conteneur)

        # Ajoute des widgets dans le conteneur
        btn_1 = QPushButton("Voir la liste")
        btn_2 = QPushButton("Supprimer la liste")
        layout.addWidget(btn_1)
        layout.addWidget(btn_2)
        
        # Contraintes de taille
        conteneur.setMinimumWidth(200)
        
        # Ajouter le conteneur dans le dock
        self.mainDock.setWidget(conteneur)
      

        # barre d'état
        self.barreEtat = QStatusBar()
        self.setStatusBar(self.barreEtat)
        self.barreEtat.showMessage("Lancement de la création de projet ...", 3000)

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


    # fonction redimensionnant automatiquement la scene en fonction de la dimension de la fenetre. methode héritant de QWidget
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view_scene.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

