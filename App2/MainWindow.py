from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget, QMessageBox, QSplashScreen, QApplication
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import Qt

from .Boutons import Boutons
from .Categories import Categories
from .Donnees import Donnees
from .Selection import Selection

from .styles import WINDOW_STYLE, BUTTON_WARNING_STYLE_QUIT, BUTTON_SECONDARY_STYLE_QUIT

class MainWindow(QMainWindow):

    def __init__(self, data : Donnees) -> None:
        super().__init__()

        self.widthWindow : int = 950; self.heightWindow : int = 650

        self.setStyleSheet(WINDOW_STYLE)
        self.setWindowTitle("Création d’une liste de courses")
        self.setFixedSize(self.widthWindow, self.heightWindow)


        # -- Splash pendant l'initialisation des produits --
        splash_pix = QPixmap(self.widthWindow, self.heightWindow)
        splash_pix.fill(QColor("white"))
        splash = QSplashScreen(splash_pix)
        splash.showMessage("Chargement des produits. Veuillez patienter...", Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.black)
        splash.show()
        QApplication.processEvents()
        # ---------------------------------------------------

        layout_top = QHBoxLayout()
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        self.data_app: Donnees = data

        self.selection = Selection()
        self.categories = Categories(self.data_app.listCategories, self.data_app.list_prod_checked, data=self.data_app, selection_widget=self.selection)

        layout_top.addWidget(self.categories)
        layout_top.addWidget(self.selection)

        main_layout.addLayout(layout_top)

        self.boutons = Boutons(self.data_app)
        self.boutons.cancel_btn.clicked.connect(self.afficher_popup_annulation)
        main_layout.addWidget(self.boutons)

        # Ferme le splash une fois que tout est prêt
        splash.close()
        self.show()

    def afficher_popup_annulation(self):
            message_box = QMessageBox(self)
            message_box.setWindowTitle("Vérification")
            message_box.setText("Êtes-vous sur d’annuler ?\nToutes modifications ne seront pas enregistrées.")
            quitter_btn = message_box.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)
            continuer_btn = message_box.addButton("Continuer", QMessageBox.ButtonRole.AcceptRole)

            quitter_btn.setStyleSheet(BUTTON_WARNING_STYLE_QUIT)
            continuer_btn.setStyleSheet(BUTTON_SECONDARY_STYLE_QUIT)

            message_box.exec()

            if message_box.clickedButton() == quitter_btn:               
                self.close()  