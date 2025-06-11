from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt6.QtGui import QPixmap, QPen
from constantes import Constantes


class ScenePlan(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.imagePlan = QGraphicsPixmapItem(QPixmap(Constantes.CHEMIN_IMAGE_PLAN))
        
        # ajoute l'image a la scene
        self.addItem(self.imagePlan)
        
        
        '''__________________________________________________________________
                                Ajout du Quadrillage
        _____________________________________________________________________'''
    
        # Définition de la taille de l'image
        largeurPlan = self.imagePlan.pixmap().width()
        hauteurPlan = self.imagePlan.pixmap().height()
        
        # Crayon utilisé
        crayon1 = QPen(Constantes.COULEUR_QUADRILLAGE)
        crayon1.setWidth(Constantes.EPAISS_LIGNE_QUADRILLAGE)   
        
        # Tracé des lignes horizontales et verticales
        for abs in range(0, largeurPlan, Constantes.TAILLE_CASE):
            ligne = QGraphicsLineItem(abs, 0, abs, hauteurPlan)
            ligne.setPen(crayon1)
            ligne.setZValue(1)  # au-dessus du plan (Z=0 par defaut)
            self.addItem(ligne) # aj les lignes à la scène
            
        for ord in range(0, hauteurPlan, Constantes.TAILLE_CASE):
            ligne = QGraphicsLineItem(0, ord, largeurPlan, ord)
            ligne.setPen(crayon1)
            ligne.setZValue(1)  # au-dessus du plan (Z=0 par defaut)
            self.addItem(ligne) # aj les lignes à la scène

