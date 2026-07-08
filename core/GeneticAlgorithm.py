from typing import List
import random
from Individual import Individual
from Selection import Selection
from Crossover import Crossover
from Mutation import Mutation


class GeneticAlgorithm:
    def __init__(self, points=None, pop_size=10, square_count=8, gen_count=50, mut_prob=0.01, cross_prob=0.1, intersection_penalty=2):
        self._history = [] # История эволюции
        self._points = points if points is not None else []
        self._square_count = square_count
        self._population_size = pop_size
        self._generation_count = gen_count
        self._mutation_probability = mut_prob
        self._crossover_probability = cross_prob
        self._intersection_penalty = intersection_penalty
        
        self._selection: Selection = Selection(Selection.RANK)
        self._crossover: Crossover = Crossover()
        self._mutation: Mutation = Mutation()

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
        """Инициализирует алгоритм случайной популяцией"""
        self._population: List[Individual] = self._create_population()
        
        self._eval_fitness(self._population)
        
        self._history.append(self._population)

    def _create_population(self):
        """Создает случайную популяцию"""
        population = [Individual(self._square_count, (-20, -20, 20, 20)) for _ in range(self._population_size)]
        self._history.append(population)
        return population

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

        # Если пересечения есть, то fitness уменьшается.
        Individualual.set_fitness(covered_points_count - self._intersection_penalty * intersections)
        
        return Individualual.get_fitness()
    
    def run(self):
        # while condition:
        # self.step()
        pass
    
    def step(self):
        # parents := selection(population)
        # new_population := mutation(crossover(parents))
        # history.append(new_population)
        pass
    
    def _eval_fitness(self, population: List[Individual]) -> None:
        """И значение целевой функции"""
        for i in range(self._population_size):
            population[i].set_fitness(self.fitness(population[i]))
            print(f'{i}) {population[i].get_fitness()}')


if __name__ == '__main__':
    '''EXAMPLE'''
    N = 20
    ga = GeneticAlgorithm(points=[(random.randint(-20, 20), random.randint(-20, 20)) for _ in range(N)])
    ga.initialize()
    ga.step()
    
    pop = ga.get_population(0)
    gen = pop[0]
    n = 0
    for i in range(1, len(pop)):
        if gen.get_fitness() < pop[i].get_fitness():
            gen = pop[i]
            n = i
    print(n)
    gen.draw_squares(ga.get_points())
    
    pop = ga.get_population(1)
    gen = pop[0]
    n = 0
    for i in range(1, len(pop)):
        if gen.get_fitness() < pop[i].get_fitness():
            gen = pop[i]
            n = i
    print(n)
    gen.draw_squares(ga.get_points())
    '''EXAMPLE'''
    