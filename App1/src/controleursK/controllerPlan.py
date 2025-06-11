import sys
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTransform



class PlanController:
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue
        self.connecter_signaux()

    def connecter_signaux(self):
        self.vue.signalNouveauProjet.connect(self.nouveau)
        self.vue.signalOuvrirProjet.connect(self.ouvrir)
        self.vue.signalEnregistrerProjet.connect(self.enregistrer)
        # self.vue.signalQuitterProjet.connect(self.destroy)
        self.vue.signalInitZoom.connect(self.initZoom)


            
    # TODO non valide = juste pour eviter les erreurs
    def nouveau(self):
        self.vue.statusBar().showMessage('Créer un nouveau projet', 5000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin
    
    # TODO non valide = juste pour eviter les erreurs
    def ouvrir(self):
        self.vue.statusBar().showMessage('Ouvrir un projet existant', 5000)
        boite = QFileDialog()
        chemin, validation = boite.getOpenFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin

    # TODO non valide = juste pour eviter les erreurs
    def enregistrer(self):
        self.vue.statusBar().showMessage('Enregistrer....', 5000 )
        boite = QFileDialog()
        chemin, validation = boite.getSaveFileName(directory = sys.path[0])
        if validation:
            self.__chemin = chemin
            
    def initZoom(self):
        self.vue.view_scene.setTransform(QTransform()) 
        self.vue.view_scene.fitInView(self.vue.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio) 