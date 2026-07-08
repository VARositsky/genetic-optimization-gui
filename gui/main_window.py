from PyQt5.QtWidgets import QWidget
from templates.templates_py.mainwindow_ui import Ui_MainWindow

class MainWindow(QWidget):
    """Класс основного окна."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)