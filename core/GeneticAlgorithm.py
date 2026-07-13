from typing import List, Tuple
import random
from math import ceil, sqrt

from .Individual import Individual
from .Selection import Selection
from .Crossover import Crossover
from .Mutation import Mutation


class GeneticAlgorithm:
    """Класс генетического алгоритма"""
    def __init__(self, points=None, pop_size=70, square_count=3, gen_count=500, mut_prob=0.25, cross_prob=0.75, 
                 k_best_percent=0.25, covering_rew=12, uncovering_pen=37, intrsc_pen=20.0, esqrs_pen=35, area_pen=0.001):
        
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

    def fitness(self, individual: Individual) -> float:
        """
        F = A * covered_points^2
            - B * intersection_area
            - C * empty_squares
            - sqrt(D * total_area)
            - E * uncovered_points
        """
        squares = individual.get_chromosome()

        covered_points, empty_squares = self._calculate_covering(squares)
        intersection_area = self._calculate_intersection_area(squares)
        total_area = self._calculate_total_area(squares)

        return (
            self._covering_rew * (covered_points ** 2)
            - self._intersection_penalty * intersection_area
            - self._empty_squares_penalty * empty_squares
            - sqrt(self._area_penalty * total_area)
            - self._uncovering_pen * (len(self._points) - covered_points)
        )
    
    def _calculate_covering(self, squares) -> Tuple[int, int]:
        """
        Возвращает словарь из количества покрытых и непокрытых точек
        """
        covered_points = set()
        empty_squares = 0

        for square in squares:
            contains_points = False

            for point_id, (px, py) in enumerate(self._points):
                x, y, w = square.x, square.y, square.w
                if x <= px <= x + w and y <= py <= y + w:
                    covered_points.add(point_id)
                    contains_points = True

            if not contains_points:
                empty_squares += 1
                continue
            
            square.is_empty = False

        return len(covered_points), empty_squares
    
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
        
    def _eval_fitness(self, population: List[Individual]) -> None:
        """
        Определеяет для каждого индивидуума значение его фунции приспособленности
        """
        for i in range(self._population_size):
            population[i].set_fitness(self.fitness(population[i]))

    def run(self):
        """
        Выполняет алгоритм до конца (пока не будет достигнуто нужное число поколений)
        """
        while len(self._history) < self._generation_count:
            self.step()

    def step(self):
        """
        Выполняет один шаг алгоритма
        """
        K_BEST_PERCENT = self._k_best_percent
        proportion = ceil(self._square_count * K_BEST_PERCENT)
        if proportion % 2 != 0:
            proportion += 1
        
        prev_population = self._history[-1]
        new_population_best = prev_population[:proportion] # Сохранение лучших без изменений
        
        parents = self._selection.tournament_selection(prev_population[proportion:], k=3) # Выбор родителей
        
        new_population_children = sorted(self._crossover.do(parents), key=lambda ind: -ind.get_fitness())
        
        new_population = new_population_best + self._mutation.do(new_population_children) # Новая популяция
        
        self._eval_fitness(new_population)
        self._history.append(new_population)
    

if __name__ == '__main__':
    '''EXAMPLE'''
    N = 40
    ga = GeneticAlgorithm(points=[(random.randint(-500, 500), random.randint(-500, 500)) for _ in range(N)])
    ga.initialize()
    pop = ga.get_population(0)
    gen = pop[0]
    n = 0
    for i in range(1, len(pop)):
        if gen.get_fitness() < pop[i].get_fitness():
            gen = pop[i]
            n = i
    print(n)
    gen.draw_squares(ga.get_points())
    for j in range(ga.get_generation_count()):
        ga.step()
    
    pop = ga.get_population(ga.get_generation_count())
    gen = pop[0]
    n = 0
    for i in range(1, len(pop)):
        if gen.get_fitness() < pop[i].get_fitness():
            gen = pop[i]
            n = i
    print(n)
    gen.draw_squares(ga.get_points())

    '''EXAMPLE'''