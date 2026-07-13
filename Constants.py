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
        "average_color": "blue"
    },
    "dark": {
        "background_color": "#2b2b2b",
        "text_color": "white",
        "grid_color": "gray",
        "best_color": "#d1722e",
        "average_color": "#297bb0"
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
            QMainWindow { background-color: #2b2b2b; }
            QLabel { color: #fff; }
            QMenuBar { background-color: #3c3c3c; color: #fff; }
            QMenuBar::item:selected { background-color: #4a4a4a; }
            QMenu { background-color: #3c3c3c; color: #fff; }
            QMenu::item:selected { background-color: #4a4a4a; }

            QPushButton {
                margin: 2px;
                background-color: #d1722e;
                color: black;
                padding: 3px 3px;
                border-radius: 3px;
            }
            QPushButton:hover { background-color: #df9c6d; }
            QPushButton:pressed { background-color: #d68246; }

            QGroupBox {
                color: #fff;
                border: 1px solid #555; 
                padding-top: 15px;
                padding-left: 5px;
                padding-right: 5px;
                padding-bottom: 5px;
            }

            QTableWidget { background-color: #3c3c3c; color: #fff; }
            QHeaderView::section { background-color: #4a4a4a; color: #fff; }
            QSpinBox, QDoubleSpinBox, QComboBox { background-color: #3c3c3c; color: #fff; }
            QLineEdit, QTextEdit { background-color: #3c3c3c; color: #fff; }
            QSplitter::handle { background-color: #3c3c3c; }
            QSplitter::handle:pressed {
                background-color: #5a5a5a;
            }

            QMessageBox { background-color: #2b2b2b; color: #fff; }
            QMessageBox QLabel { color: #fff; }
            QMessageBox QPushButton {
                background-color: #3c3c3c; color: #fff;
                border: 1px solid #555;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QMessageBox QPushButton:hover { background-color: #4a4a4a; }
            QMessageBox QPushButton:pressed { background-color: #5a5a5a; }

            QInputDialog { background-color: #2b2b2b; color: #fff; }
            QInputDialog QLabel { color: #fff; }
            QInputDialog QPushButton {
                background-color: #3c3c3c;
                color: #fff;
                border: 1px solid #555;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QInputDialog QPushButton:hover { background-color: #4a4a4a; }
            QInputDialog QPushButton:pressed { background-color: #5a5a5a; }

            QToolBar { background-color: #3c3c3c}
            QToolBar QToolButton { background-color: #d1722e; color: #d1722e; }
            QToolBar QToolButton:hover { background-color: #df9c6d; }
            QToolBar QToolButton:pressed { background-color: #d68246; }
            QToolBar QToolButton:disabled { color: #d68246; }
        """,
        "dark",
        "dark"
    )
}