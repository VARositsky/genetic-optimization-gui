from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QWidget)

class Ui_MenuWindow(object):
    def setupUi(self, MenuWindow):
        if not MenuWindow.objectName():
            MenuWindow.setObjectName(u"MenuWindow")
        MenuWindow.resize(400, 600)
        MenuWindow.setMinimumSize(QSize(400, 600))
        MenuWindow.setMaximumSize(QSize(400, 600))
        MenuWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MenuWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(90, 80, 201, 61))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.startButton = QPushButton(self.centralwidget)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setGeometry(QRect(110, 400, 171, 41))
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(80, 220, 231, 31))

        self.retranslateUi(MenuWindow)

        QMetaObject.connectSlotsByName(MenuWindow)
    # setupUi

    def retranslateUi(self, MenuWindow):
        MenuWindow.setWindowTitle(QCoreApplication.translate("MenuWindow", u"Menu", None))
        self.label.setText(QCoreApplication.translate("MenuWindow", u"<html><head/><body><p><span style=\" font-size:22pt; font-weight:700;\">Menu</span></p></body></html>", None))
        self.startButton.setText(QCoreApplication.translate("MenuWindow", u"Start", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MenuWindow", u"Input", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MenuWindow", u"Load", None))

    # retranslateUi

