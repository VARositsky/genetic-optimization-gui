from typing import List
import random
from Individual import Individual
from Selection import Selection
from Crossover import Crossover
from Mutation import Mutation


class GeneticAlgorithm:
    def __init__(self, points=None, pop_size=30, square_count=6, gen_count=200, mut_prob=0.25, cross_prob=0.75, intrsc_pen=3.5, esqrs_pen=6):
        self._history = [] # История эволюции
        
        self._points = points if points is not None else [] # Точки на плоскости
        self._square_count = square_count # Количество рассматриваемых квадратов
        self._population_size = pop_size # Размер популяции
        self._generation_count = gen_count # Количество поколений
        
        self._mutation_probability = mut_prob # Вероятность мутации гена
        self._crossover_probability = cross_prob # Вероятность скрещивания родителей
        
        self._intersection_penalty = intrsc_pen # Штраф за пересечение квадратов
        self._empty_squares_penalty = esqrs_pen # Штраф за "пустые" квадраты
        
        self._FILD_MAX_SIDE_SIZE = 0 # max(width, height), width := max(X_max - X_min), height := max(Y_max, Y_min)
        if points is not None:
            self._set_fild_params()
        
        self._selection: Selection = Selection(Selection.RANK) # Определяет процесс селекции
        self._crossover: Crossover = Crossover() # Определяет процесс скрещивания
        self._mutation: Mutation = Mutation() # Определяет процесс мутации

    def get_points(self):
        return self._points

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
        if 0 <= generation_number < len(self._history):
            return self._history[generation_number]
        raise IndexError(f"Номер поколения {generation_number} вне диапазона (0..{len(self._history)-1})")

    def initialize(self) -> None:
        """Инициализирует алгоритм"""
        self._population: List[Individual] = self._create_population()
        self._eval_fitness(self._population)
        self._history.append(self._population)
        
    def _create_population(self):
        """Создает случайную популяцию"""
        population = [Individual(self._square_count,
                                 (self._FILD_X_MIN, self._FILD_X_MIN, 
                                  self._FILD_X_MAX, self._FILD_Y_MAX),
                                 1/(self._FILD_MAX_SIDE_SIZE / self._square_count)) for _ in range(self._population_size)]
        return population
        
    def _set_fild_params(self):
        """Определяет параметры квадратной области, в которой находятся точки"""
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
        print(self._FILD_MAX_SIDE_SIZE, self._FILD_X_MAX, self._FILD_X_MIN, self._FILD_Y_MAX, self._FILD_Y_MIN)

    def fitness(self, Individualual: Individual) -> float:
        """
        Считает фитнес-функцию для одного индивидуума.
        F = C - lambda * K
        """
        squares = Individualual.get_chromosomes()
        M = len(squares)
        
        # Считаем количество пересечений между квадратами (K)
        intersections = 0
        
        for i in range(M):
            x1, y1, w1 = squares[i]
            for j in range(i + 1, M):
                x2, y2, w2 = squares[j]
                
                # Проверяем пересечение двух квадратов по осям X и Y
                not_intersect_x = (x1 + w1 < x2) or (x2 + w2 < x1)
                not_intersect_y = (y1 + w1 < y2) or (y2 + w2 < y1)
                
                if not (not_intersect_x or not_intersect_y):
                    intersections += 1
                    
        # Считаем количество уникальных покрытых точек (C)
        covered_points_count = 0        
        for px, py in self._points:
            is_covered = False
            for x, y, w in squares:
                # Точка внутри квадрата (включая границы)
                if (x <= px <= x + w) and (y <= py <= y + w):
                    is_covered = True
                    break
            if is_covered:
                covered_points_count += 1
        
        empty_squares_count = 0
        size_efficiency_penalty = 0.0
        
        for x, y, w in squares:
            points_in_square = 0
            for px, py in self._points:
                if (x <= px <= x + w) and (y <= py <= y + w):
                    points_in_square += 1
            
            if points_in_square == 0:
                # Квадрат пустой
                empty_squares_count += 1
            else:
                # Квадрат не пустой, оценим его эффективность:
                size_efficiency_penalty += (w ** 2) / points_in_square

        return 5 * covered_points_count \
                - self._intersection_penalty * intersections ** 2 \
                - self._empty_squares_penalty * empty_squares_count \
                - 0.05 * size_efficiency_penalty 
    
    def _eval_fitness(self, population: List[Individual]) -> None:
        """И значение целевой функции"""
        for i in range(self._population_size):
            population[i].set_fitness(self.fitness(population[i]))
            print(f'{i}) {population[i].get_fitness()}')
    
    def run(self):
        # while condition:
        # self.step()
        pass
    
    def step(self):
        parents = self._selection.tournament_selection(self._history[-1], k=3)
        
        new_population = self._mutation.do(
            self._crossover.do(
                parents, 
                self._crossover_probability), 
            self._mutation_probability)

        self._eval_fitness(new_population)
        self._history.append(new_population)
    

if __name__ == '__main__':
    '''EXAMPLE'''
    N = 20
    ga = GeneticAlgorithm(points=[(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(N)])
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
    