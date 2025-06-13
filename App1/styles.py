"""
Système de style unifié pour l'application.

Ce module définit l'ensemble des styles visuels utilisés dans l'application,
assurant une cohérence graphique à travers toutes les interfaces. Il comprend :
- Une palette de couleurs harmonieuse basée sur le bleu
- Des styles de composants réutilisables (boutons, champs, listes...)
- Des règles de mise en page communes
"""

# Palette de couleurs principale
COLORS = {
    'primary': '#1E88E5',       # Bleu principal - Actions et éléments importants
    'primary_light': '#64B5F6', # Bleu clair - Actions secondaires et survol
    'primary_dark': '#1565C0',  # Bleu foncé - États actifs et focus
    'accent': '#00BCD4',        # Cyan - Éléments d'accentuation
    'warning': '#FF5722',       # Orange - Alertes et actions critiques
    'success': '#4CAF50',       # Vert - Actions réussies
    'error': '#F44336',         # Rouge - Erreurs
    'background': '#FFFFFF',    # Blanc - Fond d'interface
    'surface': '#FFFFFF',       # Blanc - Surface des composants
    'text': '#000000',          # Noir - Texte principal
    'text_light': '#424242',    # Gris foncé - Texte secondaire
}

# Style global des fenêtres
WINDOW_STYLE = f"""
    QMainWindow, QDialog {{
        background-color: {COLORS['background']};
    }}
    QLabel {{
        color: {COLORS['text']};
        font-size: 16px;
    }}
    QStatusBar {{
        background-color: {COLORS['primary']};
        color: white;
        padding: 8px;
        font-weight: bold;
        font-size: 15px;
    }}
"""

# Style des boîtes de dialogue
DIALOG_STYLE = f"""
    QDialog {{
        background-color: {COLORS['background']};
        min-width: 400px;
    }}
    QLabel {{
        color: {COLORS['text']};
        font-size: 16px;
        padding: 8px;
    }}
    QGroupBox {{
        border: 2px solid {COLORS['primary']};
        border-radius: 6px;
        margin-top: 12px;
        padding: 12px;
    }}
    QGroupBox::title {{
        color: {COLORS['primary']};
        font-weight: bold;
        padding: 0 8px;
    }}
"""

# Style des champs de saisie
INPUT_STYLE = f"""
    QLineEdit, QSpinBox {{
        padding: 12px;
        border: 2px solid {COLORS['primary']};
        border-radius: 6px;
        background-color: {COLORS['surface']};
        color: {COLORS['text']};
        font-size: 16px;
        min-width: 200px;
    }}
    QLineEdit:focus, QSpinBox:focus {{
        border-color: {COLORS['primary_dark']};
        background-color: #F8F8F8;
    }}
    QLineEdit:hover, QSpinBox:hover {{
        border-color: {COLORS['primary_dark']};
    }}
    QSpinBox::up-button, QSpinBox::down-button {{
        background-color: {COLORS['primary']};
        border-radius: 3px;
        margin: 2px;
        min-height: 24px;
    }}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {{
        background-color: {COLORS['primary_dark']};
    }}
"""

# Style des boutons principaux
BUTTON_STYLE = f"""
    QPushButton {{
        padding: 12px 24px;
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 16px;
        font-weight: bold;
        min-width: 150px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_dark']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary_dark']};
        padding: 13px 23px 11px 25px;
    }}
    QPushButton:disabled {{
        background-color: #BDBDBD;
    }}
"""

# Style des boutons secondaires
BUTTON_SECONDARY_STYLE = f"""
    QPushButton {{
        padding: 12px 24px;
        background-color: {COLORS['primary_light']};
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 16px;
        font-weight: bold;
        min-width: 150px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary']};
    }}
    QPushButton:pressed {{
        background-color: {COLORS['primary']};
        padding: 13px 23px 11px 25px;
    }}
"""

# Style des boutons d'alerte
BUTTON_WARNING_STYLE = f"""
    QPushButton {{
        padding: 12px 24px;
        background-color: {COLORS['warning']};
        color: white;
        border: none;
        border-radius: 6px;
        font-size: 16px;
        font-weight: bold;
        min-width: 150px;
    }}
    QPushButton:hover {{
        background-color: #F4511E;
    }}
    QPushButton:pressed {{
        background-color: #E64A19;
        padding: 13px 23px 11px 25px;
    }}
"""

# Style des listes interactives
LIST_STYLE = f"""
    QListWidget {{
        background-color: {COLORS['surface']};
        border: 2px solid {COLORS['primary']};
        border-radius: 6px;
        padding: 8px;
        font-size: 16px;
    }}
    QListWidget::item {{
        padding: 12px;
        border-radius: 4px;
        color: {COLORS['text']};
    }}
    QListWidget::item:selected {{
        background-color: {COLORS['primary']};
        color: white;
    }}
    QListWidget::item:hover {{
        background-color: #E3F2FD;
    }}
"""

# Style des panneaux latéraux
DOCK_STYLE = f"""
    QDockWidget {{
        border: 2px solid {COLORS['primary']};
        background-color: {COLORS['surface']};
    }}
    QDockWidget::title {{
        background-color: {COLORS['primary']};
        color: white;
        padding: 12px;
        text-align: center;
        font-size: 16px;
        font-weight: bold;
    }}
"""

# Style des titres
TITLE_LABEL_STYLE = f"""
    font-size: 28px;
    color: {COLORS['text']};
    font-weight: bold;
    padding: 24px;
"""

# Style des labels de champs
FIELD_LABEL_STYLE = f"""
    color: {COLORS['text']};
    font-weight: bold;
    font-size: 16px;
    padding: 8px;
"""

# Style des vues graphiques
GRAPHICS_VIEW_STYLE = f"""
    QGraphicsView {{
        background-color: {COLORS['background']};
        border: 2px solid {COLORS['primary']};
        border-radius: 6px;
    }}
"""

# Style des messages d'erreur
ERROR_STYLE = f"""
    color: {COLORS['error']};
    font-weight: bold;
    font-size: 14px;
    padding: 8px;
"""

# Style des messages de succès
SUCCESS_STYLE = f"""
    color: {COLORS['success']};
    font-weight: bold;
    font-size: 14px;
    padding: 8px;
""" 


# Style spécifique pour la notice d'utilisation
NOTICE_STYLE = f"""
    QDialog {{
        background-color: {COLORS['background']};
    }}
    QScrollArea, QScrollArea > QWidget > QWidget {{
        background-color: {COLORS['background']};
        border: none;
    }}
    QLabel {{
        color: {COLORS['text']};
        font-size: 12px;
        padding: 2px;
        background-color: transparent;
    }}
    QPushButton {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        padding: 8px 15px;
        border-radius: 4px;
        font-weight: bold;
        min-width: 80px;
    }}
    QPushButton:hover {{
        background-color: {COLORS['primary_light']};
    }}
"""