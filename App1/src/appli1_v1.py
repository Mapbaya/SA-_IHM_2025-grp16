import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QListWidget, QTextEdit, QGraphicsScene, QGraphicsPixmapItem, QGraphicsView, QLabel, QWidget, QVBoxLayout, QPushButton, QStatusBar, QToolBar, QFileDialog, QGraphicsLineItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap, QAction, QPen, QTransform
      

class VueZoomSouris(QGraphicsView):
    def __init__(self, scene):
        super().__init__()
        self.setScene(scene)


        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # Permet de se déplacer avec la main
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse) # Zoom au niveau du curseur

        

    def wheelEvent(self, event):
        # Détermine le facteur de zoom en fonction de la direction de la molette
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        # Sauvegarde la position de la souris dans la scène
        old_pos = self.mapToScene(event.position().toPoint())
        
        # Applique le zoom
        if event.angleDelta().y() > 0: # Molette vers le haut (zoom in)
            self.scale(zoom_in_factor, zoom_in_factor)
        else: # Molette vers le bas (zoom out)
            self.scale(zoom_out_factor, zoom_out_factor)
            
        # Ramène le point sous la souris à sa position initiale
        new_pos = self.mapToScene(event.position().toPoint())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def keyPressEvent(self, event):
        zoom_factor = 1.1 # Facteur de zoom pour les touches
        
        if event.key() in (Qt.Key_Plus, Qt.Key_Equal):
            self.scale(zoom_factor, zoom_factor)
        elif event.key() == Qt.Key_Minus:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
        else:
            super().keyPressEvent(event) # Laisse les autres événements clavier être traités normalement
          

class ScenePlan(QGraphicsScene):
    def __init__(self):
        '''Constructeur de la classe'''

        # appel au constructeur de la classe mère
        super().__init__()
        self.imagePlan = QGraphicsPixmapItem(QPixmap(sys.path[0] + '/../img/plan.jpg'))
        
        # ajoute l'image a la scene
        self.addItem(self.imagePlan)
        
        
        '''__________________________________________________________________
                                Gestion Quadrillage
        _____________________________________________________________________'''
    
        # Définir taille de l'image
        largeurPlan = self.imagePlan.pixmap().width()
        hauteurPlan = self.imagePlan.pixmap().height()
        tailleCase = 100
        
        # Crayon uilisé
        crayon1 = QPen(Qt.GlobalColor.red)
        crayon1.setWidth(3)   
        
        # Tracé des lignes horizontales et verticales
        for abs in range(0, largeurPlan, tailleCase):
            ligne = QGraphicsLineItem(abs, 0, abs, hauteurPlan)
            ligne.setPen(crayon1)
            ligne.setZValue(1)  # au-dessus du plan (Z=0 par defaut)
            self.addItem(ligne)
            
        for ord in range(0, hauteurPlan, tailleCase):
            ligne = QGraphicsLineItem(0, ord, largeurPlan, ord)
            ligne.setPen(crayon1)
            ligne.setZValue(1)  # au-dessus du plan (Z=0 par defaut)
            self.addItem(ligne)



class MainWindowAppli1(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Fenetre affichage plan")
        #self.setWindowIcon(QIcon(sys.path[0] + '/icones/logo_but.png'))
        #self.setGeometry(100, 100, 500, 300)


        # widget central
        # creation de la scene
        self.scene = ScenePlan()
        self.view_scene = VueZoomSouris(self.scene) # remplace QGraphicsView(self.scene) car VueZoomSouris est un QGraphicsView
        
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
        actionNouveau = QAction(QIcon(sys.path[0] + '/../img/icones/newFile.png'), 'Nouveau', self)
        actionNouveau.setShortcut('Ctrl+N')
        actionNouveau.triggered.connect(self.nouveau)
        menuFichier.addAction(actionNouveau)
        barre_outil.addAction(actionNouveau)
        
        actionOuvrir = QAction(QIcon(sys.path[0] + '/../img/icones/openFile.png'), 'Ouvrir', self)
        actionOuvrir.setShortcut('Ctrl+O')
        actionOuvrir.triggered.connect(self.ouvrir)
        menuFichier.addAction(actionOuvrir)
        barre_outil.addAction(actionOuvrir)   
        
        actionSauvegarder = QAction(QIcon(sys.path[0] + '/../img/icones/save.png'), 'Enregistrer', self)
        actionSauvegarder.setShortcut('Ctrl+S')
        actionSauvegarder.triggered.connect(self.enregistrer)
        menuFichier.addAction(actionSauvegarder)
        barre_outil.addAction(actionSauvegarder)  
        
        menuFichier.addSeparator()
        
        actionQuitter = QAction(QIcon(sys.path[0] + '/../img/icones/suppress.png'), 'Quitter', self)
        actionQuitter.setShortcut('Ctrl+Q')
        actionQuitter.triggered.connect(self.destroy)
        menuFichier.addAction(actionQuitter)
        barre_outil.addAction(actionQuitter)     
        
        barre_outil.addSeparator()  
        
        # MENU EDITION
        actionPrecedent = QAction(QIcon(sys.path[0] + '/../img/icones/flechePrecedent.png'), 'Précédent', self)
        actionPrecedent.setShortcut('Ctrl+Z')
        # action_retablir.triggered.connect(self.text_edit.undo)
        menuEdition.addAction(actionPrecedent)
        barre_outil.addAction(actionPrecedent)
        
        actionSuivant = QAction(QIcon(sys.path[0] + '/../img/icones/flecheSuivant.png'), 'Suivant', self)
        actionSuivant.setShortcut('Ctrl+Y')
        # action_retablir.triggered.connect(self.text_edit.redo)
        menuEdition.addAction(actionSuivant)
        barre_outil.addAction(actionSuivant)
        
        menuFichier.addSeparator()
        
        barre_outil.addSeparator() 

        # MENU AFFICHAGE
        actionInitZoom = QAction(QIcon(sys.path[0] + '/../img/icones/initZoom.png'), 'Initialisation Zoom', self)
        actionInitZoom.setShortcut('Ctrl+0')
        actionInitZoom.triggered.connect(self.initZoom)
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

    # TODO non valide = juste pour eviter les erreurs
    def nouveau(self):
        self.barre_etat.showMessage('Créer un nouveau projet', 5000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin
    
    # TODO non valide = juste pour eviter les erreurs
    def ouvrir(self):
        self.barre_etat.showMessage('Ouvrir un projet existant', 5000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin

    # TODO non valide = juste pour eviter les erreurs
    def enregistrer(self):
        self.barre_etat.showMessage('Enregistrer....', 5000 )
        boite = QFileDialog()
        chemin, validation = boite.getSaveFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin
            

    # fonction redimensionnant automatiquement la scene en fonction de la dimension de la fenetre. methode héritant de QWidget
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.view_scene.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)


    def initZoom(self):
        self.view_scene.setTransform(QTransform()) 
        self.view_scene.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio) 







# --- main --------------------------------------------------------------------
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    exemple: MainWindowAppli1 = MainWindowAppli1()
    
    sys.exit(app.exec())