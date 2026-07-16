from typing import List, Tuple
import random

import matplotlib.pyplot as plt
import matplotlib.patches as patches


class Square:
    """Описывает квадрат (один ген индивидуума)"""
    def __init__(self, x, y, width, is_empty=True):
        self.x = x # Координата по x
        self.y = y # Координата по у
        self.w = width # Размер стороны w
        self.is_empty = is_empty # Является ли пустым. Пустой, если не покрывает ни одной точки.
    
    def copy(self):
        square = Square(self.x, self.y, self.w, self.is_empty)
        return square
  

class Individual:
    """
    Описывает одного индивидуума
    """
    def __init__(self, M: int, bounds: list, points: list, init=True):
        self._c_squares = M # Количество квадратов
        self._bounds = bounds # Границы поля: x_min, y_min, x_max, y_max
        self._L = max(abs(bounds[2] - bounds[0]), abs(bounds[3] - bounds[1])) # Наибольшая стороны поля
        self._average_width = self._L / max(1, self._c_squares) # Средний размер квадрата
        self._points = points # Рассматриваемые точки
        self._noise_percent_width_size = 0.2 # Процент шума для размера
        self._noise_percent_point_spawn = 0.05 # Процент шума для размещения
        self._chromosome: List[Square] = self._generate_chromosome() if init else [] # Список генов
        self._fitness = float('-inf') # Значение функции приспособленности

    def generate_width(self) -> float:
        """
        Генерирует и возвращает сторону случайного квадрата
        """
        return self._average_width + abs(random.gauss(0, self._average_width * self._noise_percent_width_size * 3))
    
    def generate_coords(self) -> Tuple[float, float]:
        """
        Генерирует и возвращает координаты левого нижнего угла случайного квадрата
        """
        p = random.choice(self._points)
        
        dx = random.gauss(0, self._noise_percent_point_spawn * abs(p[0]))
        dy = random.gauss(0, self._noise_percent_point_spawn * abs(p[1]))
        
        return p[0] + dx, p[1] + dy
    
    def _generate_chromosome(self) -> List[Square]:
        """
        Генерирует и возвращает гены индивидуума
        """
        chromosome = []
        for _ in range(self._c_squares):
            w = self.generate_width()
            x, y = self.generate_coords()
            chromosome.append(Square(x, y, w))
        return chromosome
    
    def get_points(self) -> list:
        return self._points
    
    def get_fitness(self) -> float:
        return self._fitness
    
    def get_chromosome(self) ->  List[Tuple[float, float, float]]:
        return self._chromosome
    
    def get_bounds(self) -> list:
        return self._bounds
    
    def get_average_width(self) -> float:
        return self._average_width
    
    def set_chromosome(self, chromosome: List[Tuple[float, float, float]]) -> None:
        self._chromosome = list(chromosome)

    def set_fitness(self, value: float) -> None:
        self._fitness = value

    def copy(self):
        """
        Создаёт и возвращает полную копию текущего индивида.
        """
        new_ind = Individual(
            M=self._c_squares,
            bounds=self._bounds,
            points=self._points,
            init=False
        )

        new_ind._chromosome = [square.copy() for square in self._chromosome]
        new_ind._fitness = self._fitness
        
        return new_ind