import sys
import PyQt5.QtWidgets as qtw
from gui.MainWindow import MainWindow


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())