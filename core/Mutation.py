from typing import List
import random
from Individual import Individual

class Mutation:
    def __init__(self):
        pass

    def do(self, population: List[Individual], mutation_prob: float) -> List[Individual]:
        """
        Применяет оператор мутации к популяции потомков.
        Проверяет каждый ген (квадрат) каждого индивида на вероятность мутации.
        
        Параметры:
        population : список особей Individual после скрещивания
        mutation_rate : вероятность мутации для отдельного гена (например, 0.05)
        
        Возвращает:
        population : измененная популяция с внесенными мутациями
        """
        for ind in population:
            chromosomes = ind.get_chromosomes()
            bounds = ind._bounds
            M = len(chromosomes)
            
            # Рассчитываем динамический шаг для локального сдвига на основе границ.
            # Это не даст квадратам прыгать слишком далеко.
            max_shift_x = max(1.0, (bounds[2] - bounds[0]) * 0.05)
            max_shift_y = max(1.0, (bounds[3] - bounds[1]) * 0.05)
            
            mutated_chromosomes = []
            
            for (x, y, w) in chromosomes:
                # Проверяем, подвергается ли данный конкретный квадрат мутации
                if random.random() < mutation_prob:
                    # Случайно выбираем один из 3 типов мутации
                    mutation_type = random.randint(1, 2)
                    
                    if mutation_type == 1:
                        # 1. Мутация сдвига (двигаем левый нижний угол)
                        new_x = x + random.uniform(-max_shift_x, max_shift_x)
                        new_y = y + random.uniform(-max_shift_y, max_shift_y)
                        
                        # Ограничиваем координаты рамками допустимой области bounds
                        new_x = max(bounds[0], min(new_x, bounds[2]))
                        new_y = max(bounds[1], min(new_y, bounds[3]))
                        
                        mutated_chromosomes.append((new_x, new_y, w))
                        
                    elif mutation_type == 2:
                        # 2. Мутация размера стороны w
                        # Изменяем размер в пределах +-20% от текущего, но не меньше 1
                        scale = random.uniform(0.8, 1.2)
                        new_w = max(1.0, w * scale)
                        
                        # Также следим, чтобы w не превышал MAX_WIDTH
                        new_w = min(new_w, Individual.MAX_WIDTH)
                        
                        mutated_chromosomes.append((x, y, new_w))
                        
                    # else:
                    #     # 3. Полный сброс (макро-мутация)
                    #     # Полностью перегенерируем данный квадрат в случайном месте
                    #     new_x = random.uniform(bounds[0], bounds[2])
                    #     new_y = random.uniform(bounds[1], bounds[3])
                    #     new_w = random.uniform(1.0, Individual.MAX_WIDTH)
                        
                    #     mutated_chromosomes.append((new_x, new_y, new_w))
                else:
                    # Если мутация не выпала, переносим квадрат без изменений
                    mutated_chromosomes.append((x, y, w))
            
            # Обновляем хромосомы у индивида
            ind.set_chromosomes(mutated_chromosomes)
            
        return population