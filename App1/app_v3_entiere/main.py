import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                           QVBoxLayout, QPushButton, QLabel, QMessageBox)
from PyQt6.QtCore import Qt
from app1.main_app1 import MainApp1
from app1.styles import (WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE,
                        TITLE_LABEL_STYLE)

# Les dossiers seront créés uniquement quand ils seront nécessaires
DOSSIER_PROJETS = 'projets'

class MainWindow(QMainWindow):
    """
    Page d'accueil de l'application de gestion de magasin.
    
    Cette interface permet de choisir entre deux fonctionnalités principales :
    - La création et gestion de projets de magasin
    - L'application de courses (à venir)
    
    L'interface utilise un design moderne avec une palette de couleurs bleue
    et une mise en page claire et intuitive.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion de Magasin")
        self.app1_window = None
        
        # Application du thème global
        self.setStyleSheet(WINDOW_STYLE)
        
        # Configuration de l'interface utilisateur
        self._setup_interface()
        
    def _setup_interface(self):
        """
        Configure l'interface utilisateur avec une mise en page élégante
        et des éléments visuels cohérents.
        """
        # Création du widget principal
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        
        # Configuration de la mise en page
        layout = QVBoxLayout(widget_central)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # En-tête de l'application
        self._setup_header(layout)
        
        # Boutons de navigation
        self._setup_navigation_buttons(layout)
        
        # Finalisation de la fenêtre
        self.setMinimumSize(800, 600)
        self.center()
        
    def _setup_header(self, layout):
        """
        Configure l'en-tête de l'application avec un titre 
        et un message d'accueil élégants.
        """
        # Titre principal
        titre = QLabel("Gestion de Magasin")
        titre.setStyleSheet(TITLE_LABEL_STYLE)
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titre)
        
        # Message d'accueil
        description = QLabel("Choisissez votre application")
        description.setStyleSheet("""
            font-size: 18px;
            color: #000000;
            font-weight: bold;
            margin: 20px;
        """)
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description)
        
    def _setup_navigation_buttons(self, layout):
        """
        Ajoute les boutons de navigation principaux avec 
        des styles visuels cohérents.
        """
        # Bouton de création de projet
        btn_app1 = QPushButton("Créer un projet de magasin")
        btn_app1.setStyleSheet(BUTTON_STYLE)
        btn_app1.clicked.connect(self.lancer_app1)
        layout.addWidget(btn_app1)
        
        # Bouton de l'application de courses
        btn_app2 = QPushButton("Faire ses courses")
        btn_app2.setStyleSheet(BUTTON_SECONDARY_STYLE)
        btn_app2.clicked.connect(self.lancer_app2)
        layout.addWidget(btn_app2)
        
    def center(self):
        """
        Centre la fenêtre sur l'écran pour une meilleure 
        expérience utilisateur.
        """
        frame = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())
        
    def lancer_app1(self):
        """
        Ouvre l'interface de création et gestion de projets 
        de magasin.
        """
        # Création du dossier projets uniquement si nécessaire
        if not os.path.exists(DOSSIER_PROJETS):
            os.makedirs(DOSSIER_PROJETS)
            
        self.app1_window = MainApp1(self)
        self.app1_window.show()
        self.hide()
        
    def lancer_app2(self):
        """
        Affiche un message d'information concernant la future 
        application de courses.
        """
        QMessageBox.information(
            self, 
            "Application de Courses", 
            "L'application de courses est en cours de développement.\n"
            "Elle sera bientôt disponible pour faciliter vos achats !"
        )

if __name__ == '__main__':
    # Initialisation de l'application
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Style moderne et cohérent
    
    # Lancement de l'interface principale
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 