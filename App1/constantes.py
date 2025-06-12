import os
from PyQt6.QtCore import Qt


class Constantes:
    TAILLE_CASE : int = 100
    CHEMIN_IMAGE_PLAN : str = os.path.join('App1', 'img', 'plan.jpg')
    EPAISS_LIGNE_QUADRILLAGE : int = 3
    COULEUR_QUADRILLAGE = Qt.GlobalColor.red
    CHEMIN_ICONES : str = os.path.join('App1', 'img', 'icones')
    