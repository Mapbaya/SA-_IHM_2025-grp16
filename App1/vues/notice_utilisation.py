from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QScrollArea, QWidget, QPushButton
from PyQt6.QtCore import Qt
from styles import NOTICE_STYLE, BUTTON_STYLE


class NoticeUtilisation(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Guide d'utilisation - Gestionnaire de Magasin")
        self.setMinimumSize(700, 500)
        self.setStyleSheet(NOTICE_STYLE)
        
        layout = QVBoxLayout(self)
        scroll = QScrollArea()
        content = QWidget()
        scroll_layout = QVBoxLayout(content)
        
        guide = [
            ("<h1 style='color: Black ;'> 📋 Notice d'utilisation</h1>",),
            
            ("<h2 style='color: #3498db;'>🗂️ 1. Création et gestion de projet</h2>",),
            ("• <b>Nouveau projet</b> (Ctrl+N) :",
             "  → Donnez un nom à votre projet",
             "  → Indiquez le nom du magasin",
             "  → Ajoutez votre nom comme créateur",
             "  → Sélectionnez une image du plan (.png, .jpg)"),
            ("• <b>Ouvrir un projet</b> (Ctrl+O) :",
             "  → Choisissez un projet existant dans la liste",
             "  → Double-cliquez ou utilisez le bouton 'Ouvrir'"),
            ("• <b>Enregistrer</b> (Ctrl+S) :",
             "  → Sauvegarde automatique à chaque modification",
             "  → Ou utilisez le menu Fichier > Enregistrer"),
            
            ("<h2 style='color: #3498db;'>🗺️ 2. Navigation dans le plan</h2>",),
            ("• <b>Déplacements</b> :",
             "  → Clic gauche maintenu pour déplacer le plan",
             "  → Molette pour zoomer/dézoomer",
             "  → Bouton 'Vue d'ensemble' pour voir tout le plan"),
            ("• <b>Sélection des zones</b> :",
             "  → Clic simple sur une case pour la sélectionner",
             "  → La case sélectionnée est mise en surbrillance",
             "  → Le code de la case s'affiche en bas de l'écran"),
            
            ("<h2 style='color: #3498db;'>📦 3. Gestion des produits</h2>",),
            ("• <b>Ajouter des produits</b> :",
             "  → Sélectionnez une case du plan",
             "  → Double-clic ou menu contextuel 'Ajouter produits'",
             "  → Choisissez les produits dans la liste (max 5)",
             "  → Validez avec le bouton 'Ajouter'"),
            ("• <b>Règles de placement</b> :",
             "  → Maximum 5 produits par case",
             "  → Certaines zones sont réservées (ex: frais, surgelés)",
             "  → Un produit ne peut être placé qu'une seule fois",
             "  → Les contraintes sont vérifiées automatiquement"),
            
            ("<h2 style='color: #3498db;'>📊 4. Visualisation et statistiques</h2>",),
            ("• <b>Liste des produits</b> (Menu Affichage) :",
             "  → Vue d'ensemble de tous les produits placés",
             "  → Organisés par catégories",
             "  → Indique l'emplacement de chaque produit"),
            ("• <b>Informations disponibles</b> :",
             "  → Nombre total de produits placés",
             "  → Taux d'occupation des zones",
             "  → Répartition par catégories"),
            
            ("<h2 style='color: #3498db;'>⚠️ 5. Astuces et raccourcis</h2>",),
            ("• <b>Raccourcis clavier</b> :",
             "  → F1 : Afficher cette aide",
             "  → Ctrl+2 : Active le zoom sur le plan",
             "  → Ctrl+O : Ouvrir projet",
             "  → Ctrl+S : Sauvegarder",
             "  → Échap : Fermer les fenêtres de dialogue"),
            ("• <b>Conseils pratiques</b> :",
             "  → Utilisez la vue d'ensemble pour une meilleure organisation",
             "  → Vérifiez les contraintes avant de placer les produits",
             "  → Sauvegardez régulièrement votre travail")
        ]
        
        for section in guide:
            for ligne in section:
                label = QLabel(ligne)
                label.setWordWrap(True)
                label.setTextFormat(Qt.TextFormat.RichText)
                scroll_layout.addWidget(label)
            scroll_layout.addWidget(QLabel(""))  # Espacement entre sections
        
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        bouton_fermer = QPushButton("Fermer")
        bouton_fermer.setStyleSheet(BUTTON_STYLE)
        bouton_fermer.clicked.connect(self.close)
        layout.addWidget(bouton_fermer)