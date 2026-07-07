import random

class DataUtils:
    @staticmethod
    def generate_random_points(count, x_min =0, x_max=500, y_min=0, y_max=500):
        return [(random.randint(x_min, x_max), random.randint(y_min, y_max)) for _ in range(count)]