class GeneticAlgorithm():
    def __init__(self, points=None, pop_size=10, square_count=8, gen_count=50, mut_prob=0.01, cross_prob=0.1):
        self.history = []
        self.points = points if points is not None else []
        self.square_count = square_count
        self.population_size = pop_size
        self.generation_count = gen_count
        self.mutation_probability = mut_prob
        self.crossover_probability = cross_prob

    def get_points(self):
        return self.points

    def get_square_count(self):
        return self.square_count

    def get_population_size(self):
        return self.population_size

    def get_generation_count(self):
        return self.generation_count

    def get_mutation_probability(self):
        return self.mutation_probability

    def get_crossover_probability(self):
        return self.crossover_probability

    def get_history(self):
        return self.history

    def get_population(self, generation_number):
        if 0 <= generation_number < len(self.history):
            return self.history[generation_number]
        raise IndexError(f"Номер поколения {generation_number} вне диапазона (0..{len(self.history)-1})")