from typing import List, Tuple
import random

from .Individual import Individual


class Crossover:
    def __init__(self):
        pass

    def do(self, parent_pairs: List[Tuple[Individual, Individual]], crossover_prob: float) -> List[Individual]:
        """
        Выполняет двухточечное скрещивание для списка пар родителей.
        
        Параметры:
        parent_pairs : список кортежей с парами родителей (всего N/2 пар)
        crossover_rate : вероятность скрещивания (например, 0.8)
        
        Возвращает:
        new_population : список из N потомков
        """
        new_population = []
        
        for parent1, parent2 in parent_pairs:
            chromosomes1 = parent1.get_chromosomes()
            coeff1 = parent1.get_coeff()
            chromosomes2 = parent2.get_chromosomes()
            coeff2 = parent2.get_coeff()
            M = len(chromosomes1)  # Количество квадратов
            bounds = parent1.get_bounds() # Границы для инициализации детей
            
            # Проверяем, сработает ли скрещивание по вероятности
            # Также проверяем M: если квадрат всего 1 или 2, двухточечный разрез невозможен
            if random.random() > crossover_prob or M < 3:
                # Скрещивание НЕ происходит. Создаем точные копии родителей
                child1 = Individual(M, bounds, coeff1, init=False)
                child1.set_chromosomes(list(chromosomes1))
                
                child2 = Individual(M, bounds, coeff2, init=False)
                child2.set_chromosomes(list(chromosomes2))
                
            else:
                # Скрещивание через двухточечный кроссовер
                # Выбираем две уникальные случайные точки разреза массива хромосом
                # Точки выбираются в диапазоне от 1 до M-1
                point1 = random.randint(1, M - 2)
                point2 = random.randint(point1 + 1, M - 1)
                
                # Создаем пустые экземпляры детей
                child1 = Individual(M, bounds, coeff1, init=False)
                child2 = Individual(M, bounds, coeff2,init=False)
                
                # Формируем хромосомы для первого ребенка:
                # Начало от P1, середина от P2, конец от P1
                child1_chromosomes = (
                    chromosomes1[:point1] + 
                    chromosomes2[point1:point2] + 
                    chromosomes1[point2:]
                )
                
                # Формируем хромосомы для второго ребенка (инверсивно):
                # Начало от P2, середина от P1, конец от P2
                child2_chromosomes = (
                    chromosomes2[:point1] + 
                    chromosomes1[point1:point2] + 
                    chromosomes2[point2:]
                )
                
                child1.set_chromosomes(child1_chromosomes)
                child2.set_chromosomes(child2_chromosomes)
            
            # Добавляем обоих детей в будущую популяцию
            new_population.append(child1)
            new_population.append(child2)
            
        return new_population