import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QApplication
from templates.templates_py.menuwindow_ui import Ui_MenuWindow


class MenuWindow(QWidget):
    """Класс окна меню."""
    def __init__(self, on_start_clicked=None):
        super().__init__()
        self.on_start_clicked = on_start_clicked
        self.ui = Ui_MenuWindow()
        self.ui.setupUi(self)
        self.initUI()
        
    def initUI(self):
        self.ui.startButton.clicked.connect(self.on_start_clicked)
     
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())