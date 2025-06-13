import sys
from PyQt6.QtWidgets import QApplication
from Donnees import Donnees

from MainWindow import MainWindow


if __name__ == "__main__":

    donnees_applications : Donnees = Donnees()

    app : QApplication = QApplication(sys.argv)

    window : MainWindow = MainWindow(donnees_applications)
   
    sys.exit(app.exec())


    