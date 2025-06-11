"""
C'est ici qu'on affiche le plan du magasin avec son quadrillage !
Cette vue permet de zoomer, se déplacer, et bientôt on pourra
y placer les produits. C'est le cœur visuel de l'application.
"""

from PyQt6.QtWidgets import (QMainWindow, QDockWidget, QGraphicsScene,
                           QGraphicsPixmapItem, QGraphicsView, QWidget,
                           QVBoxLayout, QPushButton, QStatusBar, QToolBar,
                           QGraphicsLineItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPen, QColor
from app1.styles import (WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        DOCK_STYLE, GRAPHICS_VIEW_STYLE, COLORS)

class VueZoomSouris(QGraphicsView):
    """
    Cette vue spéciale permet de zoomer avec la molette de la souris
    et de se déplacer en glissant-déposant. Super pratique pour
    naviguer dans les grands plans de magasin !
    """
    def __init__(self, scene):
        super().__init__()
        self.setScene(scene)
        
        # Style moderne pour la vue
        self.setStyleSheet(GRAPHICS_VIEW_STYLE)
        
        # On active le mode "main" pour pouvoir déplacer le plan
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        # Le zoom se fait par rapport à la position de la souris, c'est plus naturel
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
    def wheelEvent(self, event):
        """
        Gère le zoom avec la molette de la souris.
        On zoome exactement là où pointe la souris !
        """
        # On définit de combien on veut zoomer/dézoomer
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        
        # On note où est la souris avant de zoomer
        old_pos = self.mapToScene(event.position().toPoint())
        
        # On zoome ou dézoome selon le sens de la molette
        if event.angleDelta().y() > 0:  # Molette vers le haut = zoom
            self.scale(zoom_in_factor, zoom_in_factor)
        else:  # Molette vers le bas = dézoom
            self.scale(zoom_out_factor, zoom_out_factor)
            
        # On recentre la vue pour que le point sous la souris reste au même endroit
        new_pos = self.mapToScene(event.position().toPoint())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
        
    def keyPressEvent(self, event):
        """
        Permet aussi de zoomer avec les touches + et - du clavier
        pour ceux qui préfèrent !
        """
        zoom_factor = 1.1  # Un zoom un peu plus doux avec le clavier
        
        if event.key() in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):
            self.scale(zoom_factor, zoom_factor)
        elif event.key() == Qt.Key.Key_Minus:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
        else:
            super().keyPressEvent(event)

class ScenePlan(QGraphicsScene):
    """
    C'est ici qu'on gère l'affichage du plan du magasin et son quadrillage.
    Le quadrillage aide à placer les produits de façon précise.
    """
    def __init__(self, chemin_plan, taille_quadrillage=100):
        super().__init__()
        
        try:
            # On charge l'image du plan
            pixmap = QPixmap(chemin_plan)
            if pixmap.isNull():
                raise ValueError(f"Impossible de charger l'image: {chemin_plan}")
            self.imagePlan = QGraphicsPixmapItem(pixmap)
            self.addItem(self.imagePlan)
            
            # On récupère les dimensions du plan
            largeur = self.imagePlan.pixmap().width()
            hauteur = self.imagePlan.pixmap().height()
            
            # On prépare un crayon pour le quadrillage
            crayon = QPen(QColor(COLORS['primary']))
            crayon.setWidth(1)
            
            # On dessine toutes les lignes verticales du quadrillage
            for x in range(0, largeur, taille_quadrillage):
                ligne = QGraphicsLineItem(x, 0, x, hauteur)
                ligne.setPen(crayon)
                ligne.setZValue(1)
                self.addItem(ligne)
                
            # Et maintenant toutes les lignes horizontales
            for y in range(0, hauteur, taille_quadrillage):
                ligne = QGraphicsLineItem(0, y, largeur, y)
                ligne.setPen(crayon)
                ligne.setZValue(1)
                self.addItem(ligne)
        except Exception as e:
            print(f"Oups ! Problème lors de la création de la scène: {str(e)}")
            raise

class VueProjet(QMainWindow):
    """
    La fenêtre principale qui affiche le projet.
    Elle contient le plan, les outils pour le manipuler,
    et bientôt les fonctions pour placer les produits !
    """
    def __init__(self, projet, parent=None):
        super().__init__(parent)
        self.projet = projet
        self.parent = parent
        
        # Style global de la fenêtre
        self.setStyleSheet(WINDOW_STYLE)
        
        try:
            # On met le nom du projet dans la barre de titre
            self.setWindowTitle(f"Projet: {self.projet['nom']}")
            
            # On prépare la scène avec le plan et son quadrillage
            print(f"Création de la scène avec le plan: {self.projet['chemin_plan']}")
            self.scene = ScenePlan(
                self.projet['chemin_plan'],
                self.projet['taille_quadrillage']
            )
            self.view_scene = VueZoomSouris(self.scene)
            self.setCentralWidget(self.view_scene)
            
            # On crée un panneau sur le côté pour les produits
            self.dock_produits = QDockWidget('Produits')
            self.dock_produits.setStyleSheet(DOCK_STYLE)
            self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock_produits)
            self.dock_produits.setMinimumWidth(250)
            
            # On prépare le contenu du panneau
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
            
            # On met tout ça dans le panneau
            self.dock_produits.setWidget(conteneur)
            
            # Une barre d'état en bas pour afficher les infos du projet
            self.barre_etat = QStatusBar()
            self.setStatusBar(self.barre_etat)
            self.barre_etat.showMessage(
                f"Projet: {self.projet['nom']} | "
                f"Magasin: {self.projet['magasin']} | "
                f"Auteur: {self.projet['auteur']}"
            )
            
            # On affiche tout ça en plein écran
            self.showMaximized()
        except Exception as e:
            print(f"Oups ! Problème lors de l'initialisation de la vue: {str(e)}")
            raise
        
    def resizeEvent(self, event):
        """
        Quand on redimensionne la fenêtre, on s'assure que le plan
        reste bien visible et proportionné
        """
        super().resizeEvent(event)
        self.view_scene.fitInView(
            self.scene.sceneRect(),
            Qt.AspectRatioMode.KeepAspectRatio
        )
        
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