from typing import List, Tuple
import random

from .Individual import Individual


class Selection:
    RANK = 0
    ROULETTE = 1
    TOURNAMENT = 2
    def __init__(self, selection_type=0):
        self._selection_type = selection_type if 0 <= selection_type <= 2 else Selection.RANK
        
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
        
        # Сортируем популяцию по возрастанию fitness (худшие в начале, лучшие в конце)
        sorted_pop = sorted(population, key=lambda ind: ind.get_fitness())
        
        # Задаем веса (ранги): худшая особь (индекс 0) получает вес 1, лучшая (индекс n-1) — вес n
        ranks = [i + 1 for i in range(len(population))]
        
        for _ in range(num_pairs):
            p1 = random.choices(sorted_pop, weights=ranks, k=1)[0]
            p2 = random.choices(sorted_pop, weights=ranks, k=1)[0]
            pairs.append((p1, p2))
            
        return pairs
    
    def roulette_selection(self, population: List[Individual]) -> List[Tuple[Individual, Individual]]:
        pass