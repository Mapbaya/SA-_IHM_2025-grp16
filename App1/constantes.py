import os
from PyQt6.QtCore import Qt


class Constantes:
    # Répertoire absolu du fichier constantes.py (donc dans App1/)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


    TAILLE_CASE : int = 100
    CHEMIN_IMAGE_PLAN : str = os.path.join(BASE_DIR, 'img', 'plan.jpg')
    EPAISS_LIGNE_QUADRILLAGE : int = 3
    COULEUR_QUADRILLAGE = Qt.GlobalColor.red

    CHEMIN_ICONES = os.path.join(BASE_DIR, 'img', 'icones')
    