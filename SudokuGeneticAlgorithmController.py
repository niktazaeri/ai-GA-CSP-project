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
        population_size = 300  # اندازه جمعیت اولیه
        mutation_rate = 0.15
        generations = 1000

        def create_individual():
            individual = np.copy(grid)
            for i in range(9):
                nums = [n for n in range(1, 10) if n not in individual[i]]
                random.shuffle(nums)
                for j in range(9):
                    if individual[i][j] == 0:
                        individual[i][j] = nums.pop()
            return individual

        def fitness(individual):
            row_fitness = sum(len(set(row)) for row in individual)
            col_fitness = sum(len(set(individual[:, j])) for j in range(9))
            return row_fitness + col_fitness

        def selection(population):
            sorted_population = sorted(population, key=fitness, reverse=True)
            return sorted_population[:population_size // 2]

        def crossover(parent1, parent2):
            crossover_point = random.randint(0, 8)
            child1 = np.vstack((parent1[:crossover_point+1, :], parent2[crossover_point+1:, :]))
            child2 = np.vstack((parent2[:crossover_point+1, :], parent1[crossover_point+1:, :]))
            return child1, child2

        def mutate(individual):
            for i in range(9):
                if random.random() < mutation_rate:
                    idx1, idx2 = random.sample(range(9), 2)
                    if grid[i][idx1] == 0 and grid[i][idx2] == 0:
                        individual[i][idx1], individual[i][idx2] = individual[i][idx2], individual[i][idx1]
            return individual

        population = [create_individual() for _ in range(population_size)]

        for generation in range(generations):
            population = sorted(population, key=fitness, reverse=True)
            selected_population = selection(population)
            new_population = []

            while len(new_population) < population_size:
                parents = random.sample(selected_population, 2)
                child1, child2 = crossover(parents[0], parents[1])
                new_population.append(mutate(child1))
                new_population.append(mutate(child2))

            population = new_population[:population_size]

            best_individual = max(population, key=fitness)
            best_fitness = fitness(best_individual)
            print(f'Generation {generation}, Best Fitness: {best_fitness}')

            if generation % 10 == 0:
                self.view.draw_numbers(best_individual.tolist())
                pygame.display.flip()

            if best_fitness == 162:
                break

        best_individual = max(population, key=fitness)
        return best_individual.tolist()
