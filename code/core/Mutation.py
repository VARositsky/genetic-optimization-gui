from typing import List
import random

from .Individual import Individual, Square


class Mutation:
    """
    Отвечает за мутацию генов индивидуумов
    """
    def __init__(self, prob: float):
        self._mutation_prob = prob # Вероятность мутации гена индивидуума

    def do(self, population: List[Individual]) -> List[Individual]:
        """
        Выполняет мутацию генов индивидуумов в одной популяции
        """
        for ind in population:
            chromosome = ind.get_chromosome()            
            mutated_chromosome = []
            for square in chromosome:
                x, y, w = square.x, square.y, square.w
                # Проверяем, подвергается ли данный конкретный квадрат мутации
                if random.random() < self._mutation_prob:
                    # Случайно выбираем один из 2 типов мутации
                    mutation_type = random.choices([1, 2], weights=[1, 1], k=1)[0]
                    if mutation_type == 1:
                        # 1. Мутация сдвига. Дигаем левый нижний угол в уже известную точку с шумом
                        if square.is_empty:
                            new_x, new_y = ind.generate_coords()
                        else:
                            dx = random.gauss(0, 0.2 * abs(x))
                            dy = random.gauss(0, 0.2 * abs(y))
                            new_x = x + dx
                            new_y = y + dy
                            
                        mutated_chromosome.append(Square(new_x, new_y, w, square.is_empty))
                    elif mutation_type == 2:
                        # 2. Мутация размера стороны w
                        if square.is_empty:
                            scale = random.uniform(1.8, 3.5)
                        else:
                            scale = random.uniform(0.4, 1.8)
                        new_w = max(ind.get_average_width() * 0.2, w * scale)
                        
                        mutated_chromosome.append(Square(x, y, new_w, square.is_empty))
                    else:
                        new_x, new_y = ind.generate_coords()
                        new_w = ind.generate_width()
                        
                        mutated_chromosome.append(Square(new_x, new_y, new_w))
                else:
                    mutated_chromosome.append(square.copy())
            
            ind.set_chromosome(mutated_chromosome)
            
        return population