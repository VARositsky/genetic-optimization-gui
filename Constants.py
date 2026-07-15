# Константы визуализации
WINDOW_GEOMETRY = (100, 100, 1600, 700)
MARGINS = (15, 15, 15, 15)

# Константы крутилок параметров
MIN_NUM_PARAM = 1
MAX_NUM_PARAM = 10000
START_NUM_PARAM = 10
SINGLE_STEP_VALUE = 0.00001
DECIMALS_NUM = 5

# Отдельные константы для задания вероятности
MIN_PROB = 0
MAX_PROB = 1
START_PROB = 0.01

START_MUT_PROB = 0.25
START_CROSS_PROB = 0.75

# Отдельные константы для задания штрафов
MIN_PENALTY = 0
MAX_PENALTY = 10000
START_PENALTY = 0.1

# Константы выбора индивидуума
START_INDIVIDUUM_VALUE = 1
MIN_INDIVIDUUM_VALUE = 1



# Цвета

# Цвета графика
GRAPH_THEMES = {
    "white": {
        "background_color": "white",
        "text_color": "black",
        "grid_color": "black",
        "best_color": "red",
        "average_color": "blue",
        "legend_text_color": "black",
        "legend_background_color": "white"
    },
    "dark": {
        "background_color": "#140130",
        "text_color": "white",
        "grid_color": "gray",
        "best_color": "#d3d606",
        "average_color": "#d1722e",
        "legend_text_color": "#ffff",
        "legend_background_color": "#060126"
    }
}

# Цвета всего приложения
THEMES = {
    "Светлая": (
        "Fusion",
        "white",
        "white"
    ),
    "Тёмная": (
        """
            QMainWindow { background-color: #060126;}
            QLabel { color: #fff; }
            QMenuBar { background-color: #060126; color: #060126; }
            QMenuBar QToolButton {
                background-color: #9f06ba; 
                color: #fff; 
                border-radius: 3px;
                padding: 1px 3px;}
            QMenuBar QToolButton:hover {
                background-color: #fff; 
                color: #9f06ba;}
            
            QMenuBar::item:selected { background-color: #4a4a4a; }
            QMenu { background-color: #060126; color: #fff; }
            QMenu::item:selected { background-color: #4a4a4a; }

            QPushButton {
                margin: 2px;
                background-color: #66428f;
                color: #fff;
                padding: 3px 3px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #b22598; }
            QPushButton:pressed { background-color: #fff; color: #b22598; }

            QGroupBox {
                color: #fff;
                border: 1px solid #650580;
                padding-top: 15px;
                padding-left: 5px;
                padding-right: 5px;
                padding-bottom: 5px;
                margin-top: 15px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                top: 5;
                left: 10px;
                padding-left: 5px;
                padding-right: 5px;
            }
            
            QTableWidget { background-color: #140130; color: #fff; border: 1 solid #650580; gridline-color: gray; }
            QHeaderView::section { background-color: #6804b0; color: #fff; }
            QTableWidget { selection-background-color: #fff; selection-color: #6804b0; }
            QSpinBox, QDoubleSpinBox, QComboBox { background-color: #5e3c80; color: #fff; }
            
            QSpinBox {selection-color: #66428f; selection-background-color: #fff;}
            QSpinBox ButtonSymbols { background-color: red; }
            
            QDoubleSpinBox { selection-color: #66428f; selection-background-color: #fff; }
            
            QComboBox { selection-color: #fff; selection-background-color: #66428f;}
            QComboBox QAbstractItemView { background-color: #66428f; color: #fff; }
            QComboBox QAbstractItemView { selection-background-color: #fff; selection-color: #66428f; }
            
            QLineEdit, QTextEdit { background-color: #3c3c3c; color: #fff; }
            QSplitter::handle { background-color: #0e0121; }
            QSplitter::handle:pressed {
                background-color: #0e0121;
            }

            QMessageBox { background-color: #060126; color: #fff; }
            QMessageBox QLabel { color: #fff; }
            QMessageBox QPushButton {
                background-color: #66428f; color: #fff;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QMessageBox QPushButton:hover { background-color: #b22598; }
            QMessageBox QPushButton:pressed { background-color: #fff; color: #b22598; }
            
            QInputDialog { background-color: #060126; color: #fff; }
            QInputDialog QLabel { color: #fff; }
            QInputDialog QPushButton {
                background-color: #66428f; color: #fff;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QInputDialog QPushButton:hover { background-color: #b22598; }
            QInputDialog QPushButton:pressed { background-color: #fff; color: #b22598; }
            
            QToolBar { background-color: #140130}
            QToolBar QToolButton { background-color: #66428f; color: #fcca03; }
            QToolBar QToolButton:hover { background-color: #b22598; }
            QToolBar QToolButton:pressed { background-color: #fff; color: #b22598; }
            QToolBar QToolButton:disabled { color: #d68246; }
        """,
        "dark",
        "dark"
    )
}