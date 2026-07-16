from typing import List, Tuple
import random

from .Individual import Individual


class Selection:
    """
    Отвечает за селекцию индивидуумов
    """
    def __init__(self):
        pass
    
    def tournament_selection(self, population: List[Individual], k: int = 3) -> List[Tuple[Individual, Individual]]:
        """
        Турнирный отбор: для выбора одного родителя случайно берутся k особей,
        и из них выбирается особь с наилучшим fitness.
        """
        pairs = []
        num_pairs = len(population) // 2
        
        for _ in range(num_pairs):
            tournament1 = random.sample(population, k)
            p1 = max(tournament1, key=lambda ind: ind.get_fitness())

            tournament2 = random.sample(population, k)
            p2 = max(tournament2, key=lambda ind: ind.get_fitness())
            
            pairs.append((p1, p2))
            
        return pairs
    
    def rank_selection(self, population: List[Individual]) -> List[Tuple[Individual, Individual]]:
        """
        Ранговый отбор.
        Вероятность выбора зависит от места в рейтинге.
        """
        pairs = []
        num_pairs = len(population) // 2
        
        # Сортируем популяцию по возрастанию fitness
        sorted_pop = sorted(population, key=lambda ind: ind.get_fitness())
        
        # Чем больше ранг, тем выше вероятность выбора
        ranks = [i + 1 for i in range(len(population))]
        
        for _ in range(num_pairs):
            p1 = random.choices(sorted_pop, weights=ranks, k=1)[0]
            p2 = random.choices(sorted_pop, weights=ranks, k=1)[0]
            pairs.append((p1, p2))
            
        return pairs
    
    def roulette_selection(self, population: List[Individual]) -> List[Tuple[Individual, Individual]]:
        """Рулеточный отбор.

        Вероятность выбора особи пропорциональна её fitness.
        Значения сдвигаются, поскольку fitness может быть отрицательным.
        """
        if not population:
            return []

        fitness_values = [ind.get_fitness() for ind in population]
        min_fitness = min(fitness_values)

        # После сдвига все веса становятся положительными.
        weights = [
            fitness - min_fitness + 1e-9
            for fitness in fitness_values
        ]

        pairs = []
        num_pairs = len(population) // 2

        for _ in range(num_pairs):
            parent1 = random.choices(population, weights=weights, k=1)[0]
            parent2 = random.choices(population, weights=weights, k=1)[0]
            pairs.append((parent1, parent2))

        return pairs