from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import Qt
from constantes import Constantes


class VueInteraction(QGraphicsView):
    def __init__(self, scene):
        super().__init__()
        self.setScene(scene)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag) # Permet de se déplacer avec la main
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse) # Zoom au niveau du curseur

        
    # gestion de la molette de la souris
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
    
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Position dans la scène
            pos_scene = self.mapToScene(event.position().toPoint())

            # Conversion en indices de grille
            col = int(pos_scene.x() // Constantes.TAILLE_CASE)
            row = int(pos_scene.y() // Constantes.TAILLE_CASE)

            # Référence façon échiquier (ex : A1, B3, AA2, etc.)
            
            if (col < 26):
                lettre_col = chr(ord('A') + col)
            else:
                lettre_col = 'A' + chr(ord('A') + col%26)
            
            ref = f"{lettre_col}{row + 1}"  # ligne 0 devient "1", etc.

            print(f"Clic sur la case : {ref} (ligne {row}, colonne {col})")
        
        # Appel à l’événement de base pour conserver comportement (ex : drag)
        super().mousePressEvent(event)