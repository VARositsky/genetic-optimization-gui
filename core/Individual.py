from typing import List, Tuple
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Individual:
    # MAX_WIDTH = 20
    def __init__(self, M: int, bounds: list, points: list, init=True):
        self._initialized = False
        self._c_squares = M
        self._bounds = bounds # размер поля
        self._L = max(abs(bounds[2] - bounds[0]), abs(bounds[3] - bounds[1]))
        self._points = points
        self._noise_percent_width_size = 0.2
        self._noise_percent_point_spawn = 0.05
        self._chromosomes: list = None
        self._fitness = float('-inf')
        
        if init:
            self.initialize()
    
    def initialize(self):
        if not self._initialized:
            self._chromosomes = self.generate_chromosomes()
            self._initialized = True
    
    def _generate_width(self):
        """Возвращает сторону квадрата"""
        average_size = self._L / max(1, self._c_squares) 
        return average_size + abs(random.gauss(0, average_size * self._noise_percent_width_size * 3))
    
    def _generate_coords(self):
        """Возвращает координаты левого нижнего угла квадрата"""
        p = random.choice(self._points)
        
        dx = random.gauss(0, self._noise_percent_point_spawn * 3 * abs(p[0]))
        dy = random.gauss(0, self._noise_percent_point_spawn * 3 * abs(p[1]))
        
        return p[0] + dx, p[1] + dy
    
    def generate_chromosomes(self):
        # if not self._initialized:
        #     raise RuntimeError('Класс не инициализирован')
  
        chromosomes = []
        for _ in range(self._c_squares):
            w = self._generate_width()
            x, y = self._generate_coords()
            chromosomes.append((x, y, w))
        return chromosomes

    def _validate_gen(self, gen):
        pass
    
    # def get_coeff(self) -> float:
    #     return self._coeff
    
    def get_points(self):
        return self._points
    
    def get_fitness(self) -> float:
        return self._fitness
    
    def get_chromosomes(self) ->  List[Tuple[float, float, float]]:
        if self._initialized:
            return self._chromosomes
        raise RuntimeError('Класс не инициализирован')
    
    def get_bounds(self) -> list:
        return self._bounds
    
    def set_chromosomes(self, chromosomes: List[Tuple[float, float, float]]) -> None:
        self._chromosomes = list(chromosomes)
        self._initialized = True

    def set_fitness(self, value: float):
        self._fitness = value

    def copy(self):
        """Создаёт и возвращает полную копию текущего индивида."""
        new_ind = Individual(
            M=self._c_squares,
            bounds=self._bounds,
            points=self._points,
            init=False
        )
        # Явно копируем список хромосом (глубокое копирование каждого кортежа)
        new_ind._chromosomes = [tuple(ch) for ch in self._chromosomes]
        new_ind._fitness = self._fitness
        new_ind._initialized = True
        # Остальные атрибуты (константы) уже установлены в __init__
        return new_ind
    
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
        ax.set_xlim(self._bounds[0] - self._L, self._bounds[2] + self._L)
        ax.set_ylim(self._bounds[1] - self._L, self._bounds[2] + self._L)
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
        
    # individ = Individual(8, (xy[0], xy[1], xy2[0], xy2[1]), 1/(20/8))
    # individ.draw_squares(points=None)