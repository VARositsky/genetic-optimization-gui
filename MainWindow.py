import sys

import PyQt5.QtWidgets as qtw
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from DataUtils import DataUtils
from core.GeneticAlgorithm import GeneticAlgorithm
from VisualWidget import VisualWidget
from Constants import *


class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_population = None
        self.input_points = None
        self.algorithm = None
        self.current_step = 0
        self.max_computed_step = 0
        self.setup_ui()
        self.show()

    def setup_ui(self):
        self.setWindowTitle("Генетический алгоритм. Вариант 8")
        self.setGeometry(*WINDOW_GEOMETRY)

        self.central_widget = qtw.QWidget()
        self.setCentralWidget(self.central_widget)
        main_splitter = qtw.QSplitter(Qt.Horizontal, self.central_widget)
        layout = qtw.QHBoxLayout(self.central_widget)
        layout.setContentsMargins(*MARGINS)
        layout.addWidget(main_splitter)

        self.setup_left_panel(main_splitter)
        self.setup_central_panel(main_splitter)
        self.setup_right_panel(main_splitter)

    def setup_left_panel(self, main_splitter):
        left_splitter = qtw.QSplitter(Qt.Vertical)
        main_splitter.addWidget(left_splitter)

        # Блок с вводом точек
        points_box = qtw.QVBoxLayout()
        self.button_generate = qtw.QPushButton("Случайные точки")
        self.button_generate.clicked.connect(self.generate_random_points_clicked)
        points_box.addWidget(self.button_generate)
        self.button_load = qtw.QPushButton("Загрузить точки")
        self.button_load.clicked.connect(self.nothing)  # Написать функцию
        points_box.addWidget(self.button_load)
        self.button_manually = qtw.QPushButton("Ввести точки вручную")
        self.button_manually.clicked.connect(self.manual_points_input)
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
        param_group = qtw.QGroupBox("Параметры алгоритма")
        param_group.setLayout(param_form)
        left_splitter.addWidget(param_group)

        # Задание размера популяции
        self.spin_population_size = qtw.QSpinBox()
        self.spin_population_size.setRange(MIN_NUM_PARAM, MAX_NUM_PARAM)
        self.spin_population_size.setValue(START_NUM_PARAM)
        param_form.addRow("Размер популяции", self.spin_population_size)

        # Задание числа поколений
        self.spin_generation = qtw.QSpinBox()
        self.spin_generation.setRange(MIN_NUM_PARAM, MAX_NUM_PARAM)
        self.spin_generation.setValue(START_NUM_PARAM)
        param_form.addRow("Число поколений", self.spin_generation)

        # Задание числа квадратов
        self.spin_squares_num = qtw.QSpinBox()
        self.spin_squares_num.setRange(MIN_NUM_PARAM, MAX_NUM_PARAM)
        self.spin_squares_num.setValue(START_NUM_PARAM)
        param_form.addRow("Число квадратов", self.spin_squares_num)

        # Задание вероятности мутации
        self.spin_mutation = qtw.QDoubleSpinBox()
        self.spin_mutation.setRange(MIN_PROB, MAX_PROB)
        self.spin_mutation.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_mutation.setDecimals(DECIMALS_NUM)
        self.spin_mutation.setValue(START_PROB)
        param_form.addRow("Вероятность мутации", self.spin_mutation)

        # Задание вероятности скрещивания
        self.spin_crossover = qtw.QDoubleSpinBox()
        self.spin_crossover.setRange(MIN_PROB, MAX_PROB)
        self.spin_crossover.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_crossover.setDecimals(DECIMALS_NUM)
        self.spin_crossover.setValue(START_PROB)
        param_form.addRow("Вероятность скрещивания", self.spin_crossover)

        # Задание штрафа за пересечение квадратов
        self.spin_intersection_penalty= qtw.QDoubleSpinBox()
        self.spin_intersection_penalty.setRange(MIN_PENALTY, MAX_PENALTY)
        self.spin_intersection_penalty.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_intersection_penalty.setValue(START_PENALTY)
        param_form.addRow("Штраф за пересечение квадратов", self.spin_intersection_penalty)

        # Задание штрафа за
        self.spin_esqrs_pen = qtw.QDoubleSpinBox()
        self.spin_esqrs_pen.setRange(MIN_PENALTY, MAX_PENALTY)
        self.spin_esqrs_pen.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_esqrs_pen.setValue(START_PENALTY)
        param_form.addRow("Штраф за пустые квадраты", self.spin_esqrs_pen)

        self.combo_selection_method = qtw.QComboBox()
        self.combo_selection_method.addItems([
            "Турнирный отбор",
            "Рулетка",
            "Ранжированный отбор"
        ])
        param_form.addRow("Метод отбора родителей", self.combo_selection_method)

        # Кнопка запуска алгоритма
        self.button_start = qtw.QPushButton("Запустить алгоритм")
        self.button_start.clicked.connect(self.launch_algorithm)
        param_form.addRow(self.button_start)

        # Блок с таблицей
        self.table_widget = qtw.QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Поколение", "Лучшая fitness", "Среднее fitness"])
        self.table_widget.cellClicked.connect(self.on_table_cell_clicked)
        self.table_widget.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        left_splitter.addWidget(self.table_widget)

        # Кнопка сохранения поколений
        self.save_button = qtw.QPushButton("Сохранить популяции")
        self.save_button.clicked.connect(self.nothing)  # Написать функцию
        left_splitter.addWidget(self.save_button)

    def setup_central_panel(self, main_splitter):
        center_splitter = qtw.QSplitter(Qt.Vertical)
        main_splitter.addWidget(center_splitter)

        # Блок визуализации
        visual_box = qtw.QVBoxLayout()
        visual_group = qtw.QGroupBox("Визуализация")
        visual_group.setLayout(visual_box)
        center_splitter.addWidget(visual_group)

        # Окно визуализации
        self.visual_widget = VisualWidget()
        visual_box.addWidget(self.visual_widget)

        # Информация о номере популяции и выбранном индивидууме
        information_layout = qtw.QHBoxLayout()
        visual_box.addLayout(information_layout)

        # Номер рассматриваемой популяции
        self.label_population_num = qtw.QLabel(f"Рассматриваемая популяция: {self.current_step}")
        information_layout.addWidget(self.label_population_num)

        # Fitness рассматриваемого индивидуума
        self.label_individuum_fitness = qtw.QLabel(f"Fitness индивидуума: 0")
        information_layout.addWidget(self.label_individuum_fitness)

        # Блок кнопок выбора и просмотра индивидуумов
        buttons_individuum = qtw.QHBoxLayout()
        visual_box.addLayout(buttons_individuum)

        # Кнопка просмотра генов выбранного индивидуума
        self.view_sol_button = qtw.QPushButton("Посмотреть гены")
        self.view_sol_button.clicked.connect(self.show_chromosomes)
        buttons_individuum.addWidget(self.view_sol_button)
        buttons_individuum.addSpacing(20)

        # Выбор для просмотра индивидуума
        self.spin_individuum = qtw.QSpinBox()
        self.spin_individuum.setRange(MIN_INDIVIDUUM_VALUE, MAX_NUM_PARAM)
        self.spin_individuum.setValue(START_INDIVIDUUM_VALUE)
        self.spin_individuum.valueChanged.connect(self.individuum_value_changed)
        ind_form = qtw.QFormLayout()
        ind_form.addRow("Индивид", self.spin_individuum)
        buttons_individuum.addLayout(ind_form)
        buttons_individuum.addSpacing(20)

        # Кнопка просмотра лучшего индивидуума из популяции
        self.best_ind_button = qtw.QPushButton("Выбрать лучшего")
        self.best_ind_button.clicked.connect(self.choose_best_individual)
        buttons_individuum.addWidget(self.best_ind_button)

        # Кнопки переключения
        widget = qtw.QWidget()
        navigation_layout = qtw.QHBoxLayout(widget)
        center_splitter.addWidget(widget)

        # Кнопка перехода к предыдущему поколению
        self.prev_button = qtw.QPushButton("Предыдущий шаг")
        self.prev_button.clicked.connect(self.prev_step)
        navigation_layout.addWidget(self.prev_button)

        # Кнопка перехода к следующему поколению
        self.next_button = qtw.QPushButton("Следующий шаг")
        self.next_button.clicked.connect(self.next_step)
        navigation_layout.addWidget(self.next_button)

        # Кнопка перехода сразу к конечному ответу
        self.result_button = qtw.QPushButton("Перейти к результату")
        self.result_button.clicked.connect(self.get_result)
        navigation_layout.addWidget(self.result_button)

    def setup_right_panel(self, main_splitter):
        # График функции качества
        visual_group = qtw.QGroupBox("График")
        main_splitter.addWidget(visual_group)
        right_layout = qtw.QVBoxLayout(visual_group)

        self.figure_quality = Figure(figsize=(5, 4))
        self.canvas_quality = FigureCanvas(self.figure_quality)
        self.ax_quality = self.figure_quality.add_subplot(111)
        right_layout.addWidget(self.canvas_quality)
        self.graph_toolbar = NavigationToolbar(self.canvas_quality)
        right_layout.addWidget(self.graph_toolbar)

        self.ax_quality.set_title("Изменение функции качества")
        self.ax_quality.set_xlabel("Поколение")
        self.ax_quality.set_ylabel("Fitness")
        self.ax_quality.grid(True)
        self.canvas_quality.draw()

    def nothing(self):
        pass

    def add_table_row(self, gen_index):
        pop_fitness = [x.get_fitness() for x in self.algorithm.get_population(gen_index - 1)]
        best = max(pop_fitness)
        mean = sum(pop_fitness) / len(pop_fitness)
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.table_widget.setItem(row, 0, qtw.QTableWidgetItem(str(gen_index)))
        self.table_widget.setItem(row, 1, qtw.QTableWidgetItem(f"{best:.4f}"))
        self.table_widget.setItem(row, 2, qtw.QTableWidgetItem(f"{mean:.4f}"))

    def launch_algorithm(self):
        if self.input_points is None:
            qtw.QMessageBox.critical(self, "Ошибка запуска алгоритма", "Введите точки!")
            return

        self.algorithm = GeneticAlgorithm(
            points=self.input_points,
            pop_size=self.spin_population_size.value(),
            square_count=self.spin_squares_num.value(),
            gen_count=self.spin_generation.value(),
            mut_prob=self.spin_mutation.value(),
            cross_prob=self.spin_crossover.value(),
            intrsc_pen=self.spin_intersection_penalty.value(),
            esqrs_pen=self.spin_esqrs_pen.value()
        )
        self.algorithm.initialize()

        self.current_step = 1
        self.max_computed_step = 1
        self.table_widget.setRowCount(0)
        self.add_table_row(1)
        self.current_population = self.algorithm.get_population(self.current_step - 1)
        self.draw_fitness_plot()
        self.spin_individuum.setRange(MIN_INDIVIDUUM_VALUE, self.algorithm.get_population_size())
        self.choose_best_individual()
        self.label_population_num.setText(f"Рассматриваемая популяция: 1")

    def next_step(self):
        if self.algorithm is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        # Перерисовывает графики и обновляет таблицу при переходе к невычисленному шагу
        if self.current_step == self.max_computed_step:
            self.algorithm.step()
            self.max_computed_step += 1
            self.add_table_row(self.max_computed_step)
            self.draw_fitness_plot()
            self.current_step = self.max_computed_step
        else:
            self.current_step += 1

        # Обновляем визуализацию для текущего поколения
        self.current_population = self.algorithm.get_population(self.current_step - 1)
        self.choose_best_individual()
        self.label_population_num.setText(f"Рассматриваемая популяция: {self.current_step}")

    def go_to_step(self, step):
        if self.algorithm is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        if step < 1 or step > self.max_computed_step:
            raise Exception(f"Переход может быть только к вычисленному шагу (от 1 до {self.max_computed_step})")

        self.current_step = step
        self.current_population = self.algorithm.get_population(self.current_step - 1)
        self.label_population_num.setText(f"Рассматриваемая популяция: {self.current_step}")
        self.choose_best_individual()

    def prev_step(self):
        if self.current_step - 1 < 1:
            return
        self.go_to_step(self.current_step - 1)

    def get_result(self):
        self.algorithm.run()

        self.max_computed_step = len(self.algorithm.get_history())
        for i in range(self.current_step + 1, self.max_computed_step + 1):
            self.add_table_row(i)

        self.current_step = self.max_computed_step
        self.current_population = self.algorithm.get_population(self.current_step - 1)
        self.draw_fitness_plot()
        self.choose_best_individual()
        self.label_population_num.setText(f"Рассматриваемая популяция: {self.current_step}")

    def on_table_cell_clicked(self, row, column):
        self.go_to_step(row + 1)

    def show_chromosomes(self):
        if self.current_population is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        text = ""
        chromosomes = self.current_population[self.spin_individuum.value() - 1].get_chromosomes()
        for square in chromosomes:
            text += f"{square[0]:.4f} {square[1]:.4f} {square[2]:.4f}\n"

        title = f"Хромосомы индивидуума {self.spin_individuum.value()} из популяции {self.current_step}"

        message_box = QMessageBox(self)
        message_box.setWindowTitle(title)
        message_box.setText(text)
        message_box.setTextInteractionFlags(Qt.TextSelectableByMouse)
        message_box.setStandardButtons(QMessageBox.Ok)
        message_box.show()

    def choose_best_individual(self):
        if self.current_population is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        idx, best_individual = max(enumerate(self.current_population), key=lambda x: x[1].get_fitness())
        self.spin_individuum.setValue(idx + 1)
        self.visual_widget.set_data(self.input_points, best_individual.get_chromosomes())
        self.label_individuum_fitness.setText(f"Fitness индивидуума: {best_individual.get_fitness()}")

    def individuum_value_changed(self):
        if self.current_population is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        new_individuum = self.spin_individuum.value()
        cur_individuum = self.current_population[new_individuum - 1]
        self.visual_widget.set_data(self.input_points, cur_individuum.get_chromosomes())
        self.label_individuum_fitness.setText(f"Fitness индивидуума: {cur_individuum.get_fitness()}")

    def generate_random_points_clicked(self):
        points_count, ok = qtw.QInputDialog.getInt(
            self,
            "Случайная генерация точек",
            "Введите количество точек:",
            5,
            1,
            10000
        )

        if not ok: return
        self.input_points = DataUtils.generate_random_points(points_count)
        self.points_info.setText(f"Точек: {len(self.input_points)}")
        self.visual_widget.set_data(self.input_points, [])

    def manual_points_input(self):
        text, ok = qtw.QInputDialog.getMultiLineText(
            self,
            "Ручной ввод точек",
            "Введите точки построчно в формате x,y:"
        )

        if not ok: return

        points = []
        try:
            for line in text.splitlines():
                line = line.strip()

                if not line:
                    continue

                line = line.replace(";", ",")
                x_str, y_str = line.split(",")
                points.append((float(x_str), float(y_str)))

        except Exception as error:
            qtw.QMessageBox.critical(self, "Ошибка ввода", f"Некорректный формат точек:\n{error}")
            return

        self.points = points
        self.points_info.setText(f"Точек: {len(self.points)}")
        self.visual_widget.set_data(self.points, [])

    def draw_fitness_plot(self):
        self.ax_quality.clear()

        best_fitness = []
        average_fitness = []
        for population in self.algorithm.get_history():
            best_fitness.append(population[0].get_fitness())
            average_fitness.append(0)
            for x in population:
                best_fitness[-1] = max(x.get_fitness(), best_fitness[-1])
                average_fitness[-1] += x.get_fitness()
            average_fitness[-1] /= self.algorithm.get_population_size()

        generations = list(range(1, len(self.algorithm.get_history()) + 1))

        self.ax_quality.plot(
            generations,
            best_fitness,
            marker="o",
            markersize=3,
            linewidth=1,
            label="Лучший результат",
            color="red"
        )

        self.ax_quality.plot(
            generations,
            average_fitness,
            marker="o",
            markersize=3,
            linewidth=1,
            label="Средний результат",
            color="blue"
        )

        self.ax_quality.set_title("Изменение функции качества")
        self.ax_quality.set_xlabel("Поколение")
        self.ax_quality.set_ylabel("Fitness")
        self.ax_quality.grid(True)

        self.canvas_quality.draw()



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())   