import sys
import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from VisualWidget import VisualWidget

from GeneticAlgorithm import GeneticAlgorithm

class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.algorithm = None
        self.current_step = 0
        self.cur_ind = None
        self.population_size = 0
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Генетический алгоритм. Вариант 9")
        self.setGeometry(100, 100, 1600, 700)

        self.central_widget = qtw.QWidget()
        self.setCentralWidget(self.central_widget)
        main_splitter = qtw.QSplitter(Qt.Horizontal, self.central_widget)
        layout = qtw.QHBoxLayout(self.central_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.addWidget(main_splitter)


        # Левая колонка
        left_splitter = qtw.QSplitter(Qt.Vertical)
        main_splitter.addWidget(left_splitter)

        # Блок с вводом точек
        points_box = qtw.QVBoxLayout()
        self.button_generate = qtw.QPushButton("Случайные точки")
        self.button_generate.clicked.connect(self.nothing)      # Написать функцию
        points_box.addWidget(self.button_generate)
        self.button_load = qtw.QPushButton("Загрузить точки")
        self.button_load.clicked.connect(self.nothing)      # Написать функцию
        points_box.addWidget(self.button_load)
        self.button_manually = qtw.QPushButton("Ввести точки вручную")
        self.button_manually.clicked.connect(self.nothing)      # Написать функцию
        points_box.addWidget(self.button_manually)
        self.points_info = qtw.QLabel("Точек: 0")
        points_box.addWidget(self.points_info)
        points_group = qtw.QGroupBox("Входные данные")
        points_group.setLayout(points_box)
        left_splitter.addWidget(points_group)


        # Блок с параметрами
        # Возможно можно добавить отслеживание сигналов для того, чтобы во время хода алгоритма менять значения
        # и смотреть что будет
        param_form = qtw.QFormLayout()
        self.spin_population = qtw.QSpinBox()
        self.spin_population.setRange(1, 100000)
        self.spin_population.setValue(10)
        param_form.addRow("Размер популяции", self.spin_population)

        self.spin_generation = qtw.QSpinBox()
        self.spin_generation.setRange(1, 100000)
        self.spin_generation.setValue(50)
        param_form.addRow("Число поколений", self.spin_generation)

        self.spin_squares_num = qtw.QSpinBox()
        self.spin_squares_num.setRange(1, 100000)
        self.spin_squares_num.setValue(5)
        param_form.addRow("Число квадратов", self.spin_squares_num)

        self.spin_mutation = qtw.QDoubleSpinBox()
        self.spin_mutation.setRange(0, 1)
        self.spin_mutation.setSingleStep(0.001)
        self.spin_mutation.setDecimals(3)
        self.spin_mutation.setValue(0.01)
        param_form.addRow("Вероятность мутации", self.spin_mutation)

        self.spin_int_pen = qtw.QDoubleSpinBox()
        self.spin_int_pen.setRange(0, 100000)
        self.spin_int_pen.setSingleStep(0.1)
        self.spin_int_pen.setValue(0.5)
        param_form.addRow("Штраф за пересечение квадратов", self.spin_int_pen)

        self.spin_out_pen = qtw.QDoubleSpinBox()
        self.spin_out_pen.setRange(0, 100000)
        self.spin_out_pen.setSingleStep(0.1)
        self.spin_out_pen.setValue(0.5)
        param_form.addRow("Штраф за выход за границы", self.spin_out_pen)

        self.button_start = qtw.QPushButton("Запустить алгоритм")
        self.button_start.clicked.connect(self.nothing) # Написать функцию
        param_form.addRow(self.button_start)

        param_group = qtw.QGroupBox("Параметры алгоритма")
        param_group.setLayout(param_form)
        left_splitter.addWidget(param_group)

        # Блок с таблицей
        self.table_widget = qtw.QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Поколение", "Fitness"])
        self.table_widget.cellClicked.connect(self.nothing) # Написать функцию
        self.table_widget.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        left_splitter.addWidget(self.table_widget)

        self.save_button = qtw.QPushButton("Сохранить популяции")
        self.save_button.clicked.connect(self.nothing)  # Написать функцию
        left_splitter.addWidget(self.save_button)


        # Центральная колонка
        center_splitter = qtw.QSplitter(Qt.Vertical)
        main_splitter.addWidget(center_splitter)

        # Блок визуализации
        visual_box = qtw.QVBoxLayout()
        visual_group = qtw.QGroupBox("Визуализация")
        visual_group.setLayout(visual_box)
        center_splitter.addWidget(visual_group)

        self.visual_widget = VisualWidget(points=[(1, 3), (4, 4)], squares=[(0, -1, 2), (1, 1, 5)])
        visual_box.addWidget(self.visual_widget)
        buttons_individuum = qtw.QHBoxLayout()
        visual_box.addLayout(buttons_individuum)

        self.view_sol_button = qtw.QPushButton("Посмотреть гены")
        self.view_sol_button.clicked.connect(self.nothing) # Поставить функцию
        buttons_individuum.addWidget(self.view_sol_button)
        buttons_individuum.addSpacing(20)

        self.spin_individuum = qtw.QSpinBox()
        self.spin_individuum.setRange(1, self.population_size)
        self.spin_individuum.setValue(1)
        self.spin_individuum.valueChanged.connect(self.nothing) # Поставить функцию
        ind_form = qtw.QFormLayout()
        ind_form.addRow("Индивид", self.spin_individuum)
        buttons_individuum.addLayout(ind_form)
        buttons_individuum.addSpacing(20)

        self.best_ind_button = qtw.QPushButton("Выбрать лучшего")
        self.best_ind_button.clicked.connect(self.nothing) # Поставить функцию
        buttons_individuum.addWidget(self.best_ind_button)

        # Кнопки переключения
        widget = qtw.QWidget()
        navigation_layout = qtw.QHBoxLayout(widget)
        center_splitter.addWidget(widget)
        self.prev_button = qtw.QPushButton("Предыдущий шаг")
        self.prev_button.clicked.connect(self.nothing) # Поставить функцию
        navigation_layout.addWidget(self.prev_button)
        self.next_button = qtw.QPushButton("Следующий шаг")
        self.next_button.clicked.connect(self.nothing) # Поставить функцию
        navigation_layout.addWidget(self.next_button)
        self.result_button = qtw.QPushButton("Перейти к результату")
        self.result_button.clicked.connect(self.nothing) # Поставить функцию
        navigation_layout.addWidget(self.result_button)


        # Правая колонка
        visual_group = qtw.QGroupBox("График")
        main_splitter.addWidget(visual_group)
        right_layout = qtw.QVBoxLayout(visual_group)
        self.figure_quality = Figure(figsize=(5, 4))
        self.canvas_quality = FigureCanvas(self.figure_quality)
        self.ax_quality = self.figure_quality.add_subplot(111)
        right_layout.addWidget(self.canvas_quality)
        self.graph_toolbar = NavigationToolbar(self.canvas_quality)
        right_layout.addWidget(self.graph_toolbar)


    def nothing(self):
        pass



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())