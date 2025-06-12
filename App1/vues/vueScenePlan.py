from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem
from PyQt6.QtGui import QPixmap, QPen
from constantes import Constantes


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
            
            # ajoute l'image a la scene
            self.addItem(self.imagePlan)
        
        
            # Récupération de la taille du plan
            largeurPlan = self.imagePlan.pixmap().width()
            hauteurPlan = self.imagePlan.pixmap().height()
            
            # Crayon utilisé pour le quadrillage
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
        
        except Exception as e:
            print(f"Oups ! Problème lors de la création de la scène: {str(e)}")
            raise

