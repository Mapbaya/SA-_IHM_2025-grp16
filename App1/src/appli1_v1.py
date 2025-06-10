import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QListWidget, QTextEdit, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QLabel, QWidget, QVBoxLayout, QPushButton, QStatusBar, QToolBar, QFileDialog, QGraphicsLineItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction, QPen, QTransform
      



class ScenePlan(QGraphicsScene):
    def __init__(self):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__()
        self.imagePlan = QGraphicsPixmapItem(QPixmap(sys.path[0] + '/img/plan.jpg'))
        
        # ajoute l'image a la scene
        self.addItem(self.imagePlan)
        
        


class MainWindowAppli1(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Fenetre affichage plan")
        #self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_but.png'))
        #self.setGeometry(100, 100, 500, 300)


        # widget central
        # creation de la scene
        self.scene = ScenePlan()
        
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
        self.barreEtat.showMessage("Lancement de la création de projet ...", 5000)

        # barre de menu
        menuBarre = self.menuBar()
        menuFichier = menuBarre.addMenu('&Fichier')
        menuEdition = menuBarre.addMenu('&Edition')
        menuAffichage = menuBarre.addMenu('&Affichage')
        menuAide = menuBarre.addMenu('&Aide')

        # ajout d'une barre d'outils
        barre_outil = QToolBar('Principaux outils')
        self.addToolBar(barre_outil)


        # Ajout des éléments de menus + raccourcis clavier + Barre boutons
        # MENU FICHIER
        actionNouveau = QAction(QIcon(sys.path[0] + '/img/icones/newFile.png'), 'Nouveau', self)
        actionNouveau.setShortcut('Ctrl+N')
        actionNouveau.triggered.connect(self.nouveau)

        
        actionOuvrir = QAction(QIcon(sys.path[0] + '/img/icones/openFile.png'), 'Ouvrir', self)
        actionOuvrir.setShortcut('Ctrl+O')
        actionOuvrir.triggered.connect(self.ouvrir)

        
        actionSauvegarder = QAction(QIcon(sys.path[0] + '/img/icones/save.png'), 'Enregistrer', self)
        actionSauvegarder.setShortcut('Ctrl+S')
        actionSauvegarder.triggered.connect(self.enregistrer)

        
        menuFichier.addSeparator()
        
        actionQuitter = QAction(QIcon(sys.path[0] + '/img/icones/suppress.png'), 'Quitter', self)
        actionQuitter.setShortcut('Ctrl+Q')
        actionQuitter.triggered.connect(self.destroy)
 
        
        barre_outil.addSeparator()  
        
        # MENU EDITION
        actionPrecedent = QAction(QIcon(sys.path[0] + '/img/icones/flechePrecedent.png'), 'Précédent', self)
        actionPrecedent.setShortcut('Ctrl+Z')


        
        actionSuivant = QAction(QIcon(sys.path[0] + '/img/icones/flecheSuivant.png'), 'Suivant', self)
        actionSuivant.setShortcut('Ctrl+Y')


        # MENU AFFICHAGE
        actionInitZoom = QAction(QIcon(sys.path[0] + '/img/icones/initZoom.png'), 'Initialisation Zoom', self)
        actionInitZoom.setShortcut('Ctrl+0')
        actionInitZoom.triggered.connect(self.initZoom)
        menuAffichage.addAction(actionInitZoom)
        barre_outil.addAction(actionInitZoom)






# --- main --------------------------------------------------------------------
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    exemple: MainWindowAppli1 = MainWindowAppli1()
    
    sys.exit(app.exec())
    