from typing import List, Tuple
import random

from .Individual import Individual


class Crossover:
    """
    Отвечает за скрещивание индивидуумов
    """
    def __init__(self, prob: float):
        self._crossover_prob = prob # Вероятность скрещивания двух индивидуумов

    def do(self, parent_pairs: List[Tuple[Individual, Individual]]) -> List[Individual]:
        """
        Выполняет двухточечное скрещивание для списка пар родителей.
        """
        new_population = []
        
        for parent1, parent2 in parent_pairs:
            chromosome1 = parent1.get_chromosome()
            chromosome2 = parent2.get_chromosome()
            
            M = len(chromosome1)  # Количество квадратов
            bounds = parent1.get_bounds() # Границы для инициализации детей
            
            # Проверяем, подвергается ли  данная пара скрещиванию. 
            # Также проверяем M. Если квадратов 1 или 2, то двухточечное скрещивание невозможно
            if random.random() > self._crossover_prob or M < 3:
                child1 = parent1.copy()
                
                child2 = parent2.copy()
            else:
                point1 = random.randint(1, M - 2)
                point2 = random.randint(point1 + 1, M - 1)
                
                child1 = Individual(M, bounds, parent1.get_points(), init=False)
                child2 = Individual(M, bounds, parent2.get_points(), init=False)
                
                # Формируем хромосомы для первого и второго ребенка
                child1_chromosome = [
                    square.copy()
                    for square in (
                        chromosome1[:point1]
                        + chromosome2[point1:point2]
                        + chromosome1[point2:]
                    )
                ]
                
                child2_chromosome = [
                    square.copy()
                    for square in (
                        chromosome2[:point1]
                        + chromosome1[point1:point2]
                        + chromosome2[point2:]
                    )
                ]
                
                child1.set_chromosome(child1_chromosome)
                child2.set_chromosome(child2_chromosome)
            
            new_population.append(child1)
            new_population.append(child2)
            
        return new_population