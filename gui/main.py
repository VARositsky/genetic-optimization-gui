import sys
from menu_window import MenuWindow
from main_window import MainWindow 
from PyQt5.QtWidgets import QApplication, QStackedWidget, QDesktopWidget


class StackedWidget(QStackedWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def closeEvent(self, event):
        """Переопределяет закрытие всего приложения."""
        if self.currentWidget() == self.controller.main_window:
            event.ignore()
            self.controller.switch_to_menu()
        else:
            event.accept()


class AppController:
    def __init__(self):
        self.stacked_widget = StackedWidget(self)
        
        self.main_window = MainWindow()
        self.menu_window = MenuWindow(on_start_clicked=self.switch_to_main)
       
        self.stacked_widget.addWidget(self.menu_window)
        self.stacked_widget.addWidget(self.main_window)
        
        self.switch_to_menu()
        
    def center(self):
        """Центрирование окна на экране монитора."""
        geometry = self.stacked_widget.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.stacked_widget.move(geometry.topLeft())

    def switch_to_main(self):
        """Переход в главное окно."""
        self.stacked_widget.setMinimumSize(0, 0)
        self.stacked_widget.setMaximumSize(16777215, 16777215)
        
        self.stacked_widget.setCurrentWidget(self.main_window)
        
        self.stacked_widget.setFixedSize(1200, 600) 
        self.stacked_widget.setWindowTitle('Genetic Algorithm')
        self.center()
        
    def switch_to_menu(self):
        """Переход в меню."""
        self.stacked_widget.setMinimumSize(0, 0)
        self.stacked_widget.setMaximumSize(16777215, 16777215)
        
        self.stacked_widget.setCurrentWidget(self.menu_window)
        
        self.stacked_widget.setFixedSize(400, 600)
        self.stacked_widget.setWindowTitle('Menu')
        self.center()
        
    def show(self):
        self.stacked_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = AppController()
    controller.show()
    sys.exit(app.exec_())