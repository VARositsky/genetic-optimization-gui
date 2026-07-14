from typing import List, Tuple
import random
from math import ceil, sqrt

from .Individual import Individual
from .Selection import Selection
from .Crossover import Crossover
from .Mutation import Mutation


class GeneticAlgorithm:
    """Класс генетического алгоритма"""
    def __init__(self, points=None, pop_size=70, square_count=3, gen_count=500, mut_prob=0.25, cross_prob=0.75, k_best_percent=0.05,
    covering_rew=12, uncovering_pen=37, intrsc_pen=20.0, esqrs_pen=35, area_pen=0.001, far_empty_pen=7, selection_method="tournament",):
        
        self._history = [] # История эволюции
        
        self._points = points if points is not None else [] # Точки на плоскости
        self._square_count = square_count # Количество рассматриваемых квадратов
        self._population_size = pop_size # Размер популяции
        self._generation_count = gen_count # Количество поколений
        
        self._mutation_probability = mut_prob # Вероятность мутации гена
        self._crossover_probability = cross_prob # Вероятность скрещивания родителей

        self._k_best_percent = k_best_percent # Процент лучших индивидуумов в популяции, проходящих между поколениями без изменений

        self._covering_rew = covering_rew # Награда за покрытие точки
        self._uncovering_pen = uncovering_pen # Штраф за непокрытые точки
        self._intersection_penalty = intrsc_pen # Штраф за пересечение квадратов
        self._empty_squares_penalty = esqrs_pen # Штраф за "пустые" квадраты
        self._area_penalty = area_pen # Штраф за общую площадь
        self._far_empty_penalty = far_empty_pen # Штраф за удаленные "пустые" квадраты
        self._selection_method = selection_method # Метод отбора
        
        if points is not None:
            self._set_fild_params() # Определяет параметры поля
        
        self._selection: Selection = Selection() # Определяет процесс селекции
        self._crossover: Crossover = Crossover(self._crossover_probability) # Определяет процесс скрещивания
        self._mutation: Mutation = Mutation(self._mutation_probability) # Определяет процесс мутации

    def get_points(self):
        return self._points        
    
    def set_point(self, points: list):
        if points is not None:
            self._points = points[:]
            self._set_fild_params()

    def get_square_count(self):
        return self._square_count

    def get_population_size(self):
        return self._population_size

    def get_generation_count(self):
        return self._generation_count

    def get_mutation_probability(self):
        return self._mutation_probability

    def get_crossover_probability(self):
        return self._crossover_probability

    def get_history(self):
        return self._history

    def get_population(self, generation_number) -> List[Individual]:
        """
        Возвращает популяцию определенного поколения
        """
        if 0 <= generation_number < len(self._history):
            return self._history[generation_number]
        raise IndexError(f"Номер поколения {generation_number} вне диапазона (0..{len(self._history)-1})")

    def initialize(self) -> None:
        """
        Инициализирует алгоритм
        """
        population = self._create_population()
        self._eval_fitness(population)
        self._history.append(population)
        
    def _create_population(self) -> List[Individual]:
        """
        Возвращает случайную популяцию
        """
        population = [Individual(self._square_count,
                                 (self._FILD_X_MIN, self._FILD_Y_MIN, 
                                  self._FILD_X_MAX, self._FILD_Y_MAX),
                                 self._points) for _ in range(self._population_size)]
        return population
        
    def _set_fild_params(self):
        """
        Определяет параметры квадратной области, в которой находятся точки
        """
        mx_x, mn_x = float('-inf'), float('+inf')
        mx_y, mn_y = float('-inf'), float('+inf')
        for x, y in self._points:
            mx_x, mn_x = max(mx_x, x), min(mn_x, x)
            mx_y, mn_y = max(mx_y, y), min(mn_y, y)
        
        self._FILD_MAX_SIDE_SIZE = max(mx_x - mn_x, mx_y - mn_y)
        
        self._FILD_X_MAX = mx_x
        self._FILD_X_MIN = mn_x
        
        self._FILD_Y_MAX = mx_y
        self._FILD_Y_MIN = mn_y
        
        self._FIELD_CENTER_X = (mx_x + mn_x) / 2
        self._FIELD_CENTER_Y = (mx_y + mn_y) / 2

    def fitness(self, individual: Individual) -> float:
        """
        F = A * covered_points^2
            - B * intersection_area
            - C * empty_squares
            - sqrt(D * total_area)
            - E * uncovered_points
            - F * sum_relative_distance_empty_squares
        """
        squares = individual.get_chromosome()

        covered_points, empty_squares, covered_set = self._calculate_covering(squares)
        intersection_area = self._calculate_intersection_area(squares)
        total_area = self._calculate_total_area(squares)
        sum_relative_distance_emptysqrs = self._calculate_far_empty_squares(squares, covered_set)
        return (
            self._covering_rew * (covered_points ** 2)
            - self._intersection_penalty * intersection_area
            - self._empty_squares_penalty * empty_squares
            - self._area_penalty * total_area
            - self._uncovering_pen * (len(self._points) - covered_points)
            - self._far_empty_penalty * sum_relative_distance_emptysqrs 
        )
    
    def _calculate_covering(self, squares) -> Tuple[int, int, set]:
        covered_points = set()
        empty_squares = 0

        for square in squares:
            square.is_empty = True
            contains_points = False

            for point_id, (point_x, point_y) in enumerate(self._points):
                x, y, width = square.x, square.y, square.w

                if (
                    x <= point_x <= x + width
                    and y <= point_y <= y + width
                ):
                    covered_points.add(point_id)
                    contains_points = True

            if contains_points:
                square.is_empty = False
            else:
                empty_squares += 1

        return len(covered_points), empty_squares, covered_points
    
    def _calculate_intersection_area(self, squares):
        """
        Возвращает суммарную площадь пересечений
        """
        intersection_area = 0.0

        for i in range(len(squares)):
            square1 = squares[i]
            x1, y1, w1 = square1.x, square1.y, square1.w

            for j in range(i + 1, len(squares)):
                square2 = squares[j]
                x2, y2, w2 = square2.x, square2.y, square2.w

                overlap_width = min(x1 + w1, x2 + w2) - max(x1, x2)
                overlap_height = min(y1 + w1, y2 + w2) - max(y1, y2)

                if overlap_width > 0 and overlap_height > 0:
                    intersection_area += overlap_width * overlap_height

        return intersection_area

    def _calculate_total_area(self, squares):
        """
        Возвращает суммарную площадь квадратов
        """
        return sum(square.w ** 2 for square in squares)
    
    def _calculate_far_empty_squares(self, squares, covered_set) -> float:
        """Считает удалённость пустых квадратов
        от ближайших непокрытых точек.
        """
        uncovered_points = [
            point
            for point_id, point in enumerate(self._points)
            if point_id not in covered_set
        ]

        if not uncovered_points:
            return 0.0

        total_distance = 0.0

        for square in squares:
            if not square.is_empty:
                continue

            center_x = square.x + square.w / 2
            center_y = square.y + square.w / 2

            min_distance = min(
                sqrt(
                    (center_x - point_x) ** 2
                    + (center_y - point_y) ** 2
                )
                for point_x, point_y in uncovered_points
            )

            # Нормализация, чтобы расстояние меньше зависело
            # от масштаба координат.
            field_size = max(self._FILD_MAX_SIDE_SIZE, 1e-9)
            total_distance += min_distance / field_size

        return total_distance    

    def _eval_fitness(self, population: List[Individual]) -> None:
        for individual in population:
            individual.set_fitness(
                self.fitness(individual)
            )

    def run(self):
        """Выполняет алгоритм до лимита поколений или допустимого решения."""
        while len(self._history) < self._generation_count:
            if self.current_population_has_solution():
                break

            if not self.step():
                break
    
    def get_current_solution(self):
        """
        Возвращает лучшее допустимое решение
        из последней популяции.
        """
        if not self._history:
            return None

        solutions = [
            individual
            for individual in self._history[-1]
            if self.individual_is_solution(individual)
        ]

        if not solutions:
            return None

        return max(
            solutions,
            key=lambda individual: individual.get_fitness()
        )

    def individual_is_solution(self, individual: Individual) -> bool:
        """
        Проверяет, является ли индивидуум допустимым решением:
        все точки покрыты, квадраты не пересекаются.
        """
        if not self._points:
            return False

        squares = individual.get_chromosome()

        covered_points, _, _ = self._calculate_covering(squares)
        intersection_area = self._calculate_intersection_area(squares)

        return (
            covered_points == len(self._points)
            and intersection_area <= 1e-9
        )

    def current_population_has_solution(self) -> bool:
        return self.get_current_solution() is not None

    def _select_parents(self, population):
        if self._selection_method == "roulette":
            return self._selection.roulette_selection(population)

        if self._selection_method == "rank":
            return self._selection.rank_selection(population)

        return self._selection.tournament_selection(
            population,
            k=min(3, len(population))
        )

    def step(self):
        """Создаёт следующее поколение."""

        if not self._history:
            raise RuntimeError("Алгоритм ещё не инициализирован")

        if len(self._history) >= self._generation_count:
            return False

        if self.current_population_has_solution():
            return False

        prev_population = sorted(
            self._history[-1],
            key=lambda individual: individual.get_fitness(),
            reverse=True
        )

        elite_count = ceil(
            self._population_size * self._k_best_percent
        )

        elite_count = max(
            1,
            min(elite_count, self._population_size - 1)
        )

        elites = [
            individual.copy()
            for individual in prev_population[:elite_count]
        ]

        children_count = self._population_size - elite_count

        # Лучшие особи тоже участвуют в отборе родителей.
        parents = self._select_parents(prev_population)

        children = self._crossover.do(parents)

        # При нечётном размере популяции детей всё равно должно хватать.
        children = children[:children_count]
        children = self._mutation.do(children)

        new_population = elites + children

        self._eval_fitness(new_population)
        self._history.append(new_population)

        return True