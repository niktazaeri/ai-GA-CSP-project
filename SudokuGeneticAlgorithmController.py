import time
import pygame
import numpy as np
import random

class SudokuGeneticAlgorithmController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def solve(self):
        self.model.grid = self._solve_sudoku_genetically(self.model.grid)

    def _solve_sudoku_genetically(self, grid):
        # تنظیمات الگوریتم ژنتیک
        population_size = 300
        mutation_rate = 0.2
        generations = 1000

        def create_individual():
            individual = np.copy(grid)
            for i in range(9):
                nums = list(range(1, 10))
                random.shuffle(nums)
                for j in range(9):
                    if individual[i][j] == 0:
                        individual[i][j] = nums.pop()
            return individual

        def fitness(individual):
            fitness = 0
            for row in individual:
                fitness += len(set(row))
            for col in individual.T:
                fitness += len(set(col))
            return fitness

        def selection(population):
            # روش انتخاب تورنمنت
            selected = []
            for _ in range(population_size):
                tournament = random.sample(population, 5)
                selected.append(max(tournament, key=fitness))
            return selected

        def crossover(parent1, parent2):
            crossover_point1 = random.randint(0, 40)
            crossover_point2 = random.randint(41, 80)
            child1 = np.copy(parent1)
            child2 = np.copy(parent2)
            child1.flat[crossover_point1:crossover_point2], child2.flat[crossover_point1:crossover_point2] = parent2.flat[crossover_point1:crossover_point2], parent1.flat[crossover_point1:crossover_point2]
            return child1, child2

        def mutate(individual):
            for i in range(9):
                if random.random() < mutation_rate:
                    idx1, idx2 = random.sample(range(9), 2)
                    individual[i][idx1], individual[i][idx2] = individual[i][idx2], individual[i][idx1]
            return individual

        # ایجاد جمعیت اولیه
        population = [create_individual() for _ in range(population_size)]

        for generation in range(generations):
            # محاسبه فیتنس
            population = sorted(population, key=fitness, reverse=True)

            # انتخاب افراد برای نسل جدید
            selected_population = selection(population)
            new_population = []

            # تولید فرزندان از والدین منتخب
            for i in range(0, population_size, 2):
                parent1 = selected_population[i]
                parent2 = selected_population[i + 1]
                child1, child2 = crossover(parent1, parent2)
                new_population.append(mutate(child1))
                new_population.append(mutate(child2))

            # جایگزینی جمعیت قدیمی با جمعیت جدید
            population = new_population

            # حذف افراد با فیتنس پایین
            population = sorted(population, key=fitness, reverse=True)[:population_size]

            best_individual = max(population, key=fitness)
            best_fitness = fitness(best_individual)
            print(f'Generation {generation}, Best Fitness: {best_fitness}')

            if generation % 10 == 0:  # به‌روزرسانی صفحه نمایش هر 10 نسل
                self.view.draw_numbers(best_individual.tolist())
                pygame.display.flip()

            if best_fitness == 162:  # 18 عدد یونیک برای سطر و ستون
                break

        best_individual = max(population, key=fitness)
        return best_individual.tolist()