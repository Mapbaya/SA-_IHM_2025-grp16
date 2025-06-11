from PyQt6.QtWidgets import QApplication
from vuesK.vueMainWindowAppli1 import MainWindowAppli1
from controleursK.controllerPlan import PlanController



app = QApplication([])


vue = MainWindowAppli1()
controleur = PlanController(None, vue)


vue.show()
app.exec()