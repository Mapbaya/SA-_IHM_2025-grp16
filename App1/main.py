
"""
Mon super programme de gestion de magasin ! ^^

Il permet de :
- Créer des plans de magasin trop stylés
- Placer les produits super facilement
- Faire ses courses sans se perdre (bientôt !)

J'ai fait ça pour mon projet de BUT Info,
et j'espère que ça va aider plein de gens !
"""

import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt
from main_app1 import MainApp1
from styles import WINDOW_STYLE, BUTTON_STYLE, BUTTON_SECONDARY_STYLE, TITLE_LABEL_STYLE

# Les dossiers seront créés uniquement quand ils seront nécessaires
DOSSIER_PROJETS = 'App1/projets'

class MaFenetrePrincipale(QMainWindow):
    """
    Page d'accueil de l'application de gestion de magasin.
    
    C'est ici que tout commence, avec :
    - Un gros bouton pour créer des plans de magasin
    - Un autre pour faire ses courses (bientôt !)
    
    L'interface utilise un design moderne avec une palette de couleurs bleue
    et une mise en page claire et intuitive.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mon Appli de Magasin")
        self.ma_fenetre_plans = None
        
        # Application du thème global
        self.setStyleSheet(WINDOW_STYLE)
        
        # Je prépare mon interface
        self.preparer_mon_interface()
        
    def preparer_mon_interface(self):
        """
        Je crée ma super interface avec tous les éléments !
        """
        # Mon widget principal
        mon_widget = QWidget()
        self.setCentralWidget(mon_widget)
        
        # Ma mise en page
        mon_layout = QVBoxLayout(mon_widget)
        mon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mon_layout.setSpacing(20)
        
        # Mon titre
        self.mettre_mon_titre(mon_layout)
        
        # Mes boutons
        self.mettre_mes_boutons(mon_layout)
        
        # Je finis ma fenêtre
        self.setMinimumSize(800, 600)
        self.centrer_ma_fenetre()
        
    def mettre_mon_titre(self, mon_layout):
        """
        Je mets mon super titre avec un message d'accueil !
        """
        # Mon gros titre
        mon_titre = QLabel("Mon Appli de Magasin")
        mon_titre.setStyleSheet(TITLE_LABEL_STYLE)
        mon_titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mon_layout.addWidget(mon_titre)
        
        # Mon petit message
        mon_message = QLabel("Choisis ce que tu veux faire !")
        mon_message.setStyleSheet("""
            font-size: 18px;
            color: #000000;
            font-weight: bold;
            margin: 20px;
        """)
        mon_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mon_layout.addWidget(mon_message)
        
    def mettre_mes_boutons(self, mon_layout):
        """
        Je mets mes super boutons pour choisir l'appli !
        """
        # Pour créer des plans
        mon_bouton_plans = QPushButton("Créer un plan de magasin")
        mon_bouton_plans.setStyleSheet(BUTTON_STYLE)
        mon_bouton_plans.clicked.connect(self.ouvrir_creation_plans)
        mon_layout.addWidget(mon_bouton_plans)
        
        # Pour faire les courses (bientôt !)
        mon_bouton_courses = QPushButton("Faire ses courses")
        mon_bouton_courses.setStyleSheet(BUTTON_SECONDARY_STYLE)
        mon_bouton_courses.clicked.connect(self.ouvrir_courses)
        mon_layout.addWidget(mon_bouton_courses)
        
    def centrer_ma_fenetre(self):
        """
        Je centre ma fenêtre sur l'écran, c'est plus joli !
        """
        ma_position = self.frameGeometry()
        mon_ecran = QApplication.primaryScreen().availableGeometry().center()
        ma_position.moveCenter(mon_ecran)
        self.move(ma_position.topLeft())
        
    def ouvrir_creation_plans(self):
        """
        J'ouvre ma super appli pour créer des plans !
        """
        # Je crée mon dossier si besoin
        if not os.path.exists(DOSSIER_PROJETS):
            os.makedirs(DOSSIER_PROJETS)
            
        self.ma_fenetre_plans = MainApp1(self)
        self.ma_fenetre_plans.show()
        self.hide()
        
    def ouvrir_courses(self):
        """
        Je préviens que cette partie arrive bientôt !
        """
        QMessageBox.information(
            self, 
            "Patience...", 
            "Cette super fonction arrive bientôt !\n"
            "Tu pourras faire tes courses sans te perdre ^^"
        )

if __name__ == '__main__':
    # Je lance mon appli
    mon_appli = QApplication(sys.argv)
    mon_appli.setStyle('Fusion')  # Style moderne
    
    # Je montre ma fenêtre
    ma_fenetre = MaFenetrePrincipale()
    ma_fenetre.show()
    
    # C'est parti !
    sys.exit(mon_appli.exec()) 