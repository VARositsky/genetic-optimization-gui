import json
import random
import os

class DataUtils:
    @staticmethod
    def generate_random_points(count, x_min=0, x_max=500, y_min=0, y_max=500):
        return [
            (random.randint(x_min, x_max), random.randint(y_min, y_max))
            for _ in range(count)
        ]

    @staticmethod
    def _format_number(value):
        value = float(value)
        return str(int(value)) if value.is_integer() else f"{value:.10g}"

    @staticmethod
    def normalize_file_path(file_path):
        file_path = file_path.strip().strip('"').strip("'")
        file_path = os.path.expanduser(file_path)
        return os.path.abspath(file_path)

    @staticmethod
    def add_selected_extension(file_name, default_extension):
        if file_name.lower().endswith((".json", ".txt")):
            return file_name

        return file_name + default_extension

    @staticmethod
    def _parse_point(raw_point):
        if isinstance(raw_point, dict):
            if "x" not in raw_point or "y" not in raw_point:
                raise ValueError("В объекте точки должны быть поля x и y")
            return float(raw_point["x"]), float(raw_point["y"])

        if isinstance(raw_point, (list, tuple)) and len(raw_point) >= 2:
            return float(raw_point[0]), float(raw_point[1])

        raise ValueError(f"Некорректная точка: {raw_point}")

    @staticmethod
    def load_points_from_json(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            if "points" not in data:
                raise ValueError("В JSON-файле должен быть ключ points")
            data = data["points"]

        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список точек")

        return [DataUtils._parse_point(point) for point in data]

    @staticmethod
    def load_points_from_txt(file_path):
        points = []

        with open(file_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                parts = line.replace(",", " ").replace(";", " ").split()

                if len(parts) != 2:
                    raise ValueError(
                        f"Строка {line_number}: ожидались две координаты, получено: {line}"
                    )

                points.append((float(parts[0]), float(parts[1])))

        if not points:
            raise ValueError("Файл не содержит точек")

        return points

    @staticmethod
    def load_points_from_file(file_path):
        lower_path = file_path.lower()

        if lower_path.endswith(".json"):
            return DataUtils.load_points_from_json(file_path)

        if lower_path.endswith(".txt"):
            return DataUtils.load_points_from_txt(file_path)

        raise ValueError("Поддерживаются только файлы .json и .txt")

    @staticmethod
    def save_points_to_json(file_path, points):
        data = {
            "points": [
                {"x": float(x), "y": float(y)}
                for x, y in points
            ]
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def save_points_to_txt(file_path, points):
        with open(file_path, "w", encoding="utf-8") as file:
            for x, y in points:
                file.write(
                    f"{DataUtils._format_number(x)} {DataUtils._format_number(y)}\n"
                )

    @staticmethod
    def save_points_to_file(file_path, points):
        lower_path = file_path.lower()

        if lower_path.endswith(".json"):
            DataUtils.save_points_to_json(file_path, points)
            return

        if lower_path.endswith(".txt"):
            DataUtils.save_points_to_txt(file_path, points)
            return

        raise ValueError("Поддерживаются только файлы .json и .txt")

    @staticmethod
    def _individual_to_dict(individual):
        squares = []

        for square in individual.get_chromosome():
            squares.append({
                "x": float(square.x),
                "y": float(square.y),
                "side": float(square.w),
            })

        return {
            "fitness": float(individual.get_fitness()),
            "squares": squares,
        }

    @staticmethod
    def save_populations_to_json(file_path, points, history):
        generations = []

        for generation_index, population in enumerate(history, start = 1):
            individuals = [
                DataUtils._individual_to_dict(individual)
                for individual in population
            ]

            fitness_values = [
                individual["fitness"]
                for individual in individuals
            ]

            generations.append({
                "generation": generation_index,
                "best_fitness": max(fitness_values) if fitness_values else None,
                "average_fitness": (
                    sum(fitness_values) / len(fitness_values)
                    if fitness_values else None
                ),
                "individuals": individuals,
            })

        data = {
            "points": [
                {"x": float(x), "y": float(y)}
                for x, y in points
            ],
            "generations": generations,
        }

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def save_populations_to_txt(file_path, points, history):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("Исходные точки:\n")

            for x, y in points:
                file.write(
                    f"{DataUtils._format_number(x)} {DataUtils._format_number(y)}\n"
                )

            file.write("\nИстория популяций:\n")

            for generation_index, population in enumerate(history, start = 1):
                file.write(f"\nПоколение {generation_index}\n")

                fitness_values = [
                    float(individual.get_fitness())
                    for individual in population
                ]

                if fitness_values:
                    best_fitness = max(fitness_values)
                    average_fitness = sum(fitness_values) / len(fitness_values)

                    file.write(f"Лучшее значение fitness: {best_fitness:.6f}\n")
                    file.write(f"Среднее значение fitness: {average_fitness:.6f}\n")

                for individual_index, individual in enumerate(population):
                    file.write(
                        f"  Индивид {individual_index}, "
                        f"fitness = {individual.get_fitness():.6f}\n"
                    )

                    for square_index, square in enumerate(
                        individual.get_chromosome()
                    ):
                        file.write(
                            f"    Квадрат {square_index}: "
                            f"x={DataUtils._format_number(square.x)}, "
                            f"y={DataUtils._format_number(square.y)}, "
                            f"side={DataUtils._format_number(square.w)}\n"
                        )

    @staticmethod
    def save_populations_to_file(file_path, points, history):
        lower_path = file_path.lower()

        if lower_path.endswith(".json"):
            DataUtils.save_populations_to_json(file_path, points, history)
            return

        if lower_path.endswith(".txt"):
            DataUtils.save_populations_to_txt(file_path, points, history)
            return

        raise ValueError("Поддерживаются только файлы .json и .txt")