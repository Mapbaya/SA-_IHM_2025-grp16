"""
Gestion de l'affichage et de l'interaction avec le plan du magasin.

Ce module implémente :
- L'affichage du plan de base
- Un système de quadrillage pour le positionnement
- La gestion des interactions utilisateur
- L'affichage des produits par zone
"""

from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsView
from PyQt6.QtGui import QPixmap, QPen, QColor, QBrush, QPainter
from constantes import Constantes
from PyQt6.QtCore import pyqtSignal, Qt, QRectF
from styles import GRAPHICS_VIEW_STYLE
from PyQt6.QtWidgets import QAbstractScrollArea


class ScenePlan(QGraphicsScene):
    """
    C'est ici qu'on gère l'affichage du plan du magasin et son quadrillage.
    Le quadrillage aide à placer les produits de façon précise.
    """
    case_selectionnee = pyqtSignal(str)

    def __init__(self, chemin_plan):
        super().__init__()
        self.taille_case = 100  # Taille fixe du quadrillage
        
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
            for x in range(0, largeurPlan, self.taille_case):
                ligne = QGraphicsLineItem(x, 0, x, hauteurPlan)
                ligne.setPen(crayon1)
                ligne.setZValue(1)
                self.addItem(ligne)
                
            for y in range(0, hauteurPlan, self.taille_case):
                ligne = QGraphicsLineItem(0, y, largeurPlan, y)
                ligne.setPen(crayon1)
                ligne.setZValue(1)
                self.addItem(ligne)
        
        except Exception as e:
            print(f"Oups ! Problème lors de la création de la scène: {str(e)}")
            raise

    def mousePressEvent(self, event):
        pos = event.scenePos()
        colonne = int(pos.x() // self.taille_case)
        ligne = int(pos.y() // self.taille_case)
        
        if (0 <= colonne * self.taille_case < self.imagePlan.pixmap().width() and 
            0 <= ligne * self.taille_case < self.imagePlan.pixmap().height()):
            colonne_lettre = self.convertir_colonne_excel(colonne)
            case = f"{colonne_lettre}{ligne + 1}"
            
            if hasattr(self, 'case_actuelle') and self.case_actuelle:
                self.effacer_surbrillance(self.case_actuelle)
            
            self.mettre_en_surbrillance(case, colonne, ligne)
            self.case_actuelle = case
            self.case_selectionnee.emit(case)
            print(f"Case sélectionnée : {case}")

    def convertir_colonne_excel(self, colonne):
        resultat = ""
        while colonne >= 0:
            reste = colonne % 26
            resultat = chr(65 + reste) + resultat
            colonne = colonne // 26 - 1
        return resultat

    def mettre_en_surbrillance(self, case, colonne, ligne):
        rect = self.addRect(
            colonne * self.taille_case,
            ligne * self.taille_case,
            self.taille_case,
            self.taille_case,
            QPen(QColor(255, 165, 0)),
            QBrush(QColor(255, 165, 0, 50))
        )
        rect.setZValue(1)
        if not hasattr(self, 'produits_cases'):
            self.produits_cases = {}
        self.produits_cases[case] = rect

    def effacer_surbrillance(self, case):
        if hasattr(self, 'produits_cases') and case in self.produits_cases:
            self.removeItem(self.produits_cases[case])
            del self.produits_cases[case]


class VuePlan(QGraphicsView):
    """
    Vue pour afficher et interagir avec le plan du magasin.
    Gère aussi le zoom à la molette et le déplacement (drag) si activé.
    """
    def __init__(self, chemin_plan, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
        self.scene_plan = ScenePlan(chemin_plan)
        self.setScene(self.scene_plan)
        self.resetTransform()
        self.ensureVisible(self.scene_plan.sceneRect())
        self.set_vue_generale(True)

    def set_vue_generale(self, active=True):
        self.vue_generale_active = active
        if active:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            self.resetTransform()
            self.fitInView(self.scene_plan.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
        else:
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.viewport().update()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'vue_generale_active') and self.vue_generale_active:
            self.fitInView(self.scene_plan.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        if hasattr(self, 'vue_generale_active') and not self.vue_generale_active:
            zoom_in_factor = 1.25
            zoom_out_factor = 1 / zoom_in_factor
            old_pos = self.mapToScene(event.position().toPoint())
            if event.angleDelta().y() > 0:
                self.scale(zoom_in_factor, zoom_in_factor)
            else:
                self.scale(zoom_out_factor, zoom_out_factor)
            new_pos = self.mapToScene(event.position().toPoint())
            delta = new_pos - old_pos
            self.translate(delta.x(), delta.y())
        else:
            super().wheelEvent(event)

    def keyPressEvent(self, event):
        if hasattr(self, 'vue_generale_active') and not self.vue_generale_active:
            zoom_factor = 1.1
            if event.key() in (Qt.Key_Plus, Qt.Key_Equal):
                self.scale(zoom_factor, zoom_factor)
            elif event.key() == Qt.Key_Minus:
                self.scale(1 / zoom_factor, 1 / zoom_factor)
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)