from typing import List, Tuple
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Individual:
    MAX_WIDTH = 20
    def __init__(self, M: int, bounds: Tuple[int, int, int, int], coeff: float, init=True):
        self._c_squares = M
        self._bounds = bounds
        self._coeff = coeff
        self._chromosomes: List[Tuple[float, float, float]] = self._generate_chromosomes() if init else []
        self._fitness = 0
    
    def _generate_chromosomes(self):
        chromosomes = []
        for _ in range(self._c_squares):
            x = random.randint(self._bounds[0], self._bounds[2])
            y = random.randint(self._bounds[1], self._bounds[3])
            w = max(1, random.expovariate(self._coeff)) # <--- изменить | vrsn 09.07
            gen = (x, y, w)            
            chromosomes.append(gen)
        return chromosomes

    def _validate_gen(self, gen):
        pass
    
    def get_coeff(self) -> float:
        return self._coeff
    
    def get_fitness(self) -> float:
        return self._fitness
    
    def get_chromosomes(self) ->  List[Tuple[float, float, float]]:
        return self._chromosomes
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        return self._bounds
    
    def set_chromosomes(self, chromosomes: List[Tuple[float, float, float]]) -> None:
        self._chromosomes = list(chromosomes)

    def set_fitness(self, value: float):
        self._fitness = value

# Считать макс расстоние между точками. Взять сторону случайно от 1 до (макс. расст.) / M
    def draw_squares(self, points=None):
        """
        Рисует квадраты на графике.

        Параметры:
        squares : list of tuples (x, y, a)
            Список квадратов, где x, y – координаты левого нижнего угла,
            a – длина стороны.
        """
        fig, ax = plt.subplots()
        ax.set_xlim(self._bounds[0] - self.MAX_WIDTH, self._bounds[2] + self.MAX_WIDTH)
        ax.set_ylim(self._bounds[1] - self.MAX_WIDTH, self._bounds[2] + self.MAX_WIDTH)
        # Добавляем каждый квадрат как прямоугольник
        for (x, y, a) in self._chromosomes:
            rect = patches.Rectangle(
                (x, y), a, a,
                linewidth=1, edgecolor='black', facecolor='none'
            )
            ax.add_patch(rect)
        
        if points is not None:
            # Если переданы точки – рисуем их
            # Предполагаем, что points – список кортежей (x, y)
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            ax.scatter(xs, ys, color='red', s=30, zorder=5, label='Точки')
            ax.legend()  # опционально

        # Равный масштаб по осям
        ax.set_aspect('equal', adjustable='box')
        plt.show()
        

if __name__ == '__main__':
    xy = (-10, -10)
    xy2 = (10, 10)
        
    individ = Individual(8, (xy[0], xy[1], xy2[0], xy2[1]), 1/(20/8))
    individ.draw_squares(points=None)