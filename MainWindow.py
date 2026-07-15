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
        self.graph_colors = GRAPH_THEMES["white"]
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
        
        self.setup_menu()
        self.setup_left_panel(main_splitter)
        self.setup_central_panel(main_splitter)
        self.setup_right_panel(main_splitter)
        
        self.theme_group.actions()[1].trigger()

    def setup_menu(self):
        menubar = self.menuBar()

        self.theme_menu = qtw.QMenu(self)

        self.theme_group = qtw.QActionGroup(self)
        self.theme_group.setExclusive(True)

        light_theme_action = qtw.QAction(
            "Светлая", self, checkable=True
        )
        light_theme_action.setChecked(True)

        dark_theme_action = qtw.QAction(
            "Тёмная", self, checkable=True
        )

        self.theme_group.addAction(light_theme_action)
        self.theme_group.addAction(dark_theme_action)
    
        self.theme_menu.addActions([
            light_theme_action,
            dark_theme_action
        ])

        self.theme_button = qtw.QToolButton(self)
        self.theme_button.setStyleSheet("QToolButton::menu-indicator { image: none; }")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.setText("Тема")
        self.theme_button.setMenu(self.theme_menu)
        self.theme_button.setPopupMode(qtw.QToolButton.InstantPopup)

        menubar.setCornerWidget(
            self.theme_button,
            Qt.TopRightCorner
        )

        # self.theme_changed()
        self.theme_group.triggered.connect(self.theme_changed)

    def setup_left_panel(self, main_splitter):
        left_splitter = qtw.QSplitter(Qt.Vertical)
        main_splitter.addWidget(left_splitter)

        # Блок с вводом точек
        points_box = qtw.QVBoxLayout()
        self.button_generate = qtw.QPushButton("Случайные точки")
        self.button_generate.setCursor(Qt.PointingHandCursor)
        self.button_generate.clicked.connect(self.generate_random_points_clicked)
        points_box.addWidget(self.button_generate)
        self.button_load = qtw.QPushButton("Загрузить точки")
        self.button_load.setCursor(Qt.PointingHandCursor)
        self.button_load.clicked.connect(self.load_points_from_file)
        points_box.addWidget(self.button_load)

        self.button_save_points = qtw.QPushButton("Сохранить точки")
        self.button_save_points.setCursor(Qt.PointingHandCursor)
        self.button_save_points.clicked.connect(self.save_points_to_file)
        points_box.addWidget(self.button_save_points)

        self.button_manually = qtw.QPushButton("Ввести точки вручную")
        self.button_manually.setCursor(Qt.PointingHandCursor)
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
        self.spin_population_size.setValue(START_NUM_PARAM * 10)
        param_form.addRow("Размер популяции", self.spin_population_size)

        # Задание числа поколений
        self.spin_generation = qtw.QSpinBox()
        self.spin_generation.setRange(MIN_NUM_PARAM, MAX_NUM_PARAM)
        self.spin_generation.setValue(START_NUM_PARAM * 50)
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
        self.spin_mutation.setValue(START_MUT_PROB)
        param_form.addRow("Вероятность мутации", self.spin_mutation)

        # Задание вероятности скрещивания
        self.spin_crossover = qtw.QDoubleSpinBox()
        self.spin_crossover.setRange(MIN_PROB, MAX_PROB)
        self.spin_crossover.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_crossover.setDecimals(DECIMALS_NUM)
        self.spin_crossover.setValue(START_CROSS_PROB)
        param_form.addRow("Вероятность скрещивания", self.spin_crossover)

        # Награда за покрытие точки
        self.spin_covering_reward = qtw.QDoubleSpinBox()
        self.spin_covering_reward.setRange(0, 10000)
        self.spin_covering_reward.setDecimals(3)
        self.spin_covering_reward.setSingleStep(1)
        self.spin_covering_reward.setValue(12)

        param_form.addRow("Награда за покрытие точки", self.spin_covering_reward)

        # Штраф за непокрытые точки
        self.spin_uncovering_penalty = qtw.QDoubleSpinBox()
        self.spin_uncovering_penalty.setRange(0, 10000)
        self.spin_uncovering_penalty.setDecimals(3)
        self.spin_uncovering_penalty.setSingleStep(1)
        self.spin_uncovering_penalty.setValue(37)

        param_form.addRow("Штраф за непокрытые точки", self.spin_uncovering_penalty)

        # Задание штрафа за пересечение квадратов
        self.spin_intersection_penalty = qtw.QDoubleSpinBox()
        self.spin_intersection_penalty.setRange(MIN_PENALTY, MAX_PENALTY)
        self.spin_intersection_penalty.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_intersection_penalty.setValue(20)
        param_form.addRow("Штраф за пересечение квадратов", self.spin_intersection_penalty)

        # Задание штрафа за пустые квадраты
        self.spin_esqrs_pen = qtw.QDoubleSpinBox()
        self.spin_esqrs_pen.setRange(MIN_PENALTY, MAX_PENALTY)
        self.spin_esqrs_pen.setSingleStep(SINGLE_STEP_VALUE)
        self.spin_esqrs_pen.setValue(35)
        param_form.addRow("Штраф за пустые квадраты", self.spin_esqrs_pen)

        self.spin_area_penalty = qtw.QDoubleSpinBox()
        self.spin_area_penalty.setRange(0, 100)
        self.spin_area_penalty.setDecimals(6)
        self.spin_area_penalty.setSingleStep(0.001)
        self.spin_area_penalty.setValue(0.001)

        param_form.addRow("Штраф за общую площадь", self.spin_area_penalty)

        self.spin_far_empty_penalty = qtw.QDoubleSpinBox()
        self.spin_far_empty_penalty.setRange(0, 10000)
        self.spin_far_empty_penalty.setDecimals(3)
        self.spin_far_empty_penalty.setSingleStep(1)
        self.spin_far_empty_penalty.setValue(10)

        param_form.addRow('Штраф за удалённые "пустые" квадраты', self.spin_far_empty_penalty)

        self.combo_selection_method = qtw.QComboBox()
        self.combo_selection_method.addItem("Турнирный отбор", "tournament")
        self.combo_selection_method.addItem("Рулетка", "roulette")
        self.combo_selection_method.addItem("Ранжированный отбор", "rank")

        param_form.addRow("Метод отбора родителей", self.combo_selection_method)

        # Кнопка запуска алгоритма
        self.button_start = qtw.QPushButton("Запустить алгоритм")
        self.button_start.setCursor(Qt.PointingHandCursor)
        self.button_start.clicked.connect(self.launch_algorithm)
        param_form.addRow(self.button_start)

        # Блок с таблицей
        self.table_widget = qtw.QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Поколение", "Лучшая fitness", "Среднее fitness"])
        self.table_widget.cellClicked.connect(self.on_table_cell_clicked)
        self.table_widget.setEditTriggers(qtw.QTableWidget.NoEditTriggers)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setVisible(False)
        left_splitter.addWidget(self.table_widget)

        # Кнопка сохранения поколений
        self.save_button = qtw.QPushButton("Сохранить популяции")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.clicked.connect(self.save_populations_to_file)
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
        self.view_sol_button.setCursor(Qt.PointingHandCursor)
        self.view_sol_button.clicked.connect(self.show_chromosome)
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
        self.best_ind_button.setCursor(Qt.PointingHandCursor)
        self.best_ind_button.clicked.connect(self.choose_best_individual)
        buttons_individuum.addWidget(self.best_ind_button)

        # Кнопки переключения
        widget = qtw.QWidget()
        navigation_layout = qtw.QHBoxLayout(widget)
        center_splitter.addWidget(widget)

        # Кнопка перехода к предыдущему поколению
        self.prev_button = qtw.QPushButton("Предыдущий шаг")
        self.prev_button.setCursor(Qt.PointingHandCursor)
        self.prev_button.clicked.connect(self.prev_step)
        navigation_layout.addWidget(self.prev_button)

        # Кнопка перехода к следующему поколению
        self.next_button = qtw.QPushButton("Следующий шаг")
        self.next_button.setCursor(Qt.PointingHandCursor)
        self.next_button.clicked.connect(self.next_step)
        navigation_layout.addWidget(self.next_button)

        # Кнопка перехода сразу к конечному ответу
        self.result_button = qtw.QPushButton("Перейти к результату")
        self.result_button.setCursor(Qt.PointingHandCursor)
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
            selection_method=self.combo_selection_method.currentData(),

            covering_rew=self.spin_covering_reward.value(),
            uncovering_pen=self.spin_uncovering_penalty.value(),
            intrsc_pen=self.spin_intersection_penalty.value(),
            esqrs_pen=self.spin_esqrs_pen.value(),
            area_pen=self.spin_area_penalty.value(),
            far_empty_pen=self.spin_far_empty_penalty.value()
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
            qtw.QMessageBox.critical(
                self,
                "Ошибка в работе алгоритма",
                "Алгоритм ещё не запущен!"
            )
            return

        if self.current_step == self.max_computed_step:
            generation_limit = (
                self.algorithm.get_generation_count()
            )

            if self.max_computed_step >= generation_limit:
                qtw.QMessageBox.information(
                    self,
                    "Алгоритм завершён",
                    (
                        "Достигнуто заданное число поколений: "
                        f"{generation_limit}."
                    )
                )
                return

            generation_created = self.algorithm.step()

            if not generation_created:
                if self.algorithm.current_population_has_solution():
                    qtw.QMessageBox.information(
                        self,
                        "Алгоритм завершён",
                        (
                            "Алгоритм остановлен досрочно: "
                            "в текущей популяции найдено полное покрытие всех точек."
                        )
                    )
                else:
                    qtw.QMessageBox.information(
                        self,
                        "Алгоритм завершён",
                        "Достигнуто заданное число поколений."
                    )

                return

            self.max_computed_step += 1

            self.add_table_row(self.max_computed_step)
            self.draw_fitness_plot()

            self.current_step = self.max_computed_step

        else:
            self.current_step += 1

        self.current_population = self.algorithm.get_population(
            self.current_step - 1
        )

        if self.algorithm.current_population_has_solution():
            self.show_solution_individual()
        else:
            self.choose_best_individual()

        self.label_population_num.setText(
            f"Рассматриваемая популяция: {self.current_step}"
        )

        if self.algorithm.current_population_has_solution():
            qtw.QMessageBox.information(
                self,
                "Полное покрытие",
                (
                    "Все точки покрыты.\n"
                    f"Алгоритм остановлен на поколении {self.current_step}."
                )
            )

    def go_to_step(self, step):
        if self.algorithm is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        if step < 1 or step > self.max_computed_step:
            qtw.QMessageBox.warning(
                self,
                "Некорректное поколение",
                (
                    "Переход возможен только к вычисленному "
                    f"поколению от 1 до {self.max_computed_step}."
                )
            )
            return

        self.current_step = step
        self.current_population = self.algorithm.get_population(self.current_step - 1)
        self.label_population_num.setText(f"Рассматриваемая популяция: {self.current_step}")
        self.choose_best_individual()

    def prev_step(self):
        if self.current_step - 1 < 1:
            return
        self.go_to_step(self.current_step - 1)

    def get_result(self):
        if self.algorithm is None:
            qtw.QMessageBox.critical(
                self,
                "Ошибка в работе алгоритма",
                "Сначала задайте точки и запустите алгоритм!"
            )
            return

        self.algorithm.run()

        self.max_computed_step = len(
            self.algorithm.get_history()
        )

        # Перестраиваем таблицу полностью,
        # чтобы в ней не появлялись повторяющиеся строки.
        self.table_widget.setRowCount(0)

        for step in range(1, self.max_computed_step + 1):
            self.add_table_row(step)

        self.current_step = self.max_computed_step

        self.current_population = self.algorithm.get_population(
            self.current_step - 1
        )

        self.draw_fitness_plot()
        if self.algorithm.current_population_has_solution():
            self.show_solution_individual()
        else:
            self.choose_best_individual()

        self.label_population_num.setText(
            f"Рассматриваемая популяция: {self.current_step}"
        )

    def on_table_cell_clicked(self, row, column):
        step = row + 1

        if 1 <= step <= self.max_computed_step:
            self.go_to_step(step)

    def show_chromosome(self):
        if self.current_population is None:
            qtw.QMessageBox.critical(
                self,
                "Ошибка",
                "Алгоритм ещё не запущен!"
            )
            return

        individual_index = self.spin_individuum.value() - 1

        if not 0 <= individual_index < len(self.current_population):
            qtw.QMessageBox.critical(
                self,
                "Ошибка",
                "Выбранного индивидуума нет в популяции."
            )
            return

        chromosome = self.current_population[
            individual_index
        ].get_chromosome()

        lines = []

        for number, square in enumerate(chromosome, start=1):
            # Поддерживает и объекты Square, и кортежи.
            if hasattr(square, "x"):
                x, y, width = square.x, square.y, square.w
            else:
                x, y, width = square

            lines.append(
                f"Квадрат {number}: "
                f"x = {x:.4f}, "
                f"y = {y:.4f}, "
                f"сторона = {width:.4f}"
            )

        text = "\n".join(lines)

        qtw.QMessageBox.information(
            self,
            (
                f"Гены индивидуума "
                f"{self.spin_individuum.value()}, "
                f"поколение {self.current_step}"
            ),
            text
        )

    def show_solution_individual(self):
        solution = self.algorithm.get_current_solution()

        if solution is None:
            self.choose_best_individual()
            return

        solution_index = next(
            index
            for index, individual in enumerate(self.current_population)
            if individual is solution
        )

        self.spin_individuum.setValue(solution_index + 1)

        self.visual_widget.set_data(
            self.input_points,
            solution.get_chromosome()
        )

        self.label_individuum_fitness.setText(
            f"Fitness индивидуума: {solution.get_fitness()}"
        )

    def choose_best_individual(self):
        if self.current_population is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        idx, best_individual = max(enumerate(self.current_population), key=lambda x: x[1].get_fitness())
        self.spin_individuum.setValue(idx + 1)
        self.visual_widget.set_data(self.input_points, best_individual.get_chromosome())
        self.label_individuum_fitness.setText(f"Fitness индивидуума: {best_individual.get_fitness()}")

    def individuum_value_changed(self):
        if self.current_population is None:
            qtw.QMessageBox.critical(self, "Ошибка в работе алгоритма", f"Алгоритм ещё не запущен!")
            return

        new_individuum = self.spin_individuum.value()
        cur_individuum = self.current_population[new_individuum - 1]
        self.visual_widget.set_data(self.input_points, cur_individuum.get_chromosome())
        self.label_individuum_fitness.setText(f"Fitness индивидуума: {cur_individuum.get_fitness()}")

    def generate_random_points_clicked(self):
        points_count, ok = qtw.QInputDialog.getInt(
            self,
            "Случайная генерация точек",
            "Введите количество точек:",
            10,
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

        self.input_points = points
        self.points_info.setText(f"Точек: {len(self.input_points)}")
        self.visual_widget.set_data(self.input_points, [])

    def draw_fitness_plot(self):
        self.figure_quality.set_facecolor(self.graph_colors["background_color"])
        self.ax_quality.set_facecolor(self.graph_colors["background_color"])
        self.ax_quality.clear()

        best_fitness = []
        average_fitness = []
        generations = []

        if self.algorithm is not None:
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
            color=self.graph_colors["best_color"]
        )

        self.ax_quality.plot(
            generations,
            average_fitness,
            marker="o",
            markersize=3,
            linewidth=1,
            label="Средний результат",
            color=self.graph_colors["average_color"]
        )

        self.ax_quality.set_title("Изменение функции качества", color=self.graph_colors["text_color"])
        self.ax_quality.set_xlabel("Поколение", color=self.graph_colors["text_color"])
        self.ax_quality.set_ylabel("Fitness", color=self.graph_colors["text_color"])
        self.ax_quality.tick_params(color=self.graph_colors["text_color"], labelcolor=self.graph_colors["text_color"])
        self.ax_quality.grid(True, color=self.graph_colors["grid_color"])
        legend = self.ax_quality.legend(facecolor=self.graph_colors["legend_background_color"])
        for text in legend.get_texts():
            text.set_color(self.graph_colors["legend_text_color"])
        self.canvas_quality.draw()

    def _reset_algorithm_state_after_points_change(self):
        self.algorithm = None
        self.current_population = None
        self.current_step = 0
        self.max_computed_step = 0

        self.table_widget.setRowCount(0)
        self.label_population_num.setText("Рассматриваемая популяция: 0")
        self.label_individuum_fitness.setText("Fitness индивидуума: 0")

        self.ax_quality.clear()
        self.ax_quality.set_title("Изменение функции качества")
        self.ax_quality.set_xlabel("Поколение")
        self.ax_quality.set_ylabel("Fitness")
        self.ax_quality.grid(True)
        self.canvas_quality.draw()

    def load_points_from_file(self):
        file_name, _ = qtw.QFileDialog.getOpenFileName(
            self,
            "Загрузить точки",
            "",
            "Текстовый файл (*.txt);;JSON-файл (*.json)"
        )

        if not file_name.strip():
            return

        file_name = DataUtils.normalize_file_path(file_name)

        try:
            self.input_points = DataUtils.load_points_from_file(file_name)
        except Exception as error:
            qtw.QMessageBox.critical(
                self,
                "Ошибка загрузки",
                f"Не удалось загрузить точки:\n{error}"
            )
            return

        self.points_info.setText(f"Точек: {len(self.input_points)}")
        self.visual_widget.set_data(self.input_points, [])
        self._reset_algorithm_state_after_points_change()

        qtw.QMessageBox.information(
            self,
            "Загрузка выполнена",
            f"Точки успешно загружены:\n{file_name}"
        )

    def save_points_to_file(self):
        if not self.input_points:
            qtw.QMessageBox.critical(
                self,
                "Ошибка сохранения",
                "Нет точек для сохранения."
            )
            return

        file_name, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Сохранить точки",
            "",
            "Текстовый файл (*.txt);;JSON-файл (*.json)"
        )

        if not file_name.strip():
            return

        file_name = DataUtils.normalize_file_path(file_name)
        file_name = DataUtils.add_selected_extension(file_name, ".json")

        try:
            DataUtils.save_points_to_file(file_name, self.input_points)
        except Exception as error:
            qtw.QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить точки:\n{error}"
            )
            return

        qtw.QMessageBox.information(
            self,
            "Сохранение выполнено",
            f"Точки успешно сохранены:\n{file_name}"
        )

    def save_populations_to_file(self):
        if self.algorithm is None:
            qtw.QMessageBox.critical(
                self,
                "Ошибка сохранения",
                "Сначала запустите алгоритм."
            )
            return

        history = self.algorithm.get_history()

        if not history:
            qtw.QMessageBox.critical(
                self,
                "Ошибка сохранения",
                "История популяций пуста."
            )
            return

        file_name, _ = qtw.QFileDialog.getSaveFileName(
            self,
            "Сохранить популяции",
            "",
            "Текстовый файл (*.txt);;JSON-файл (*.json)"
        )

        if not file_name.strip():
            return

        file_name = DataUtils.normalize_file_path(file_name)
        file_name = DataUtils.add_selected_extension(file_name, ".json")

        try:
            DataUtils.save_populations_to_file(
                file_name,
                self.input_points,
                history
            )
        except Exception as error:
            qtw.QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"Не удалось сохранить популяции:\n{error}"
            )
            return
        

        qtw.QMessageBox.information(
            self,
            "Сохранение выполнено",
            f"Популяции успешно сохранены:\n{file_name}"
        )

    def theme_changed(self, action):
        settings = THEMES.get(action.text(), None)
        if not settings:
            return

        style, graph_theme, visual_theme = settings
        self.visual_widget.set_theme(visual_theme)
        qtw.QApplication.instance().setStyleSheet(style)
        self.graph_colors = GRAPH_THEMES[graph_theme]
        self.draw_fitness_plot()
    

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())   