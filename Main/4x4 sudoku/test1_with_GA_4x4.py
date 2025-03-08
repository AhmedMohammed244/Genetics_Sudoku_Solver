import random
import matplotlib.pyplot as plt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Random_Puzzle import *

class Individual:
    def __init__(self, board):
        self.board = board 
        self.fitness = 0  

    def calculate_fitness(self):
        row_score = 0
        col_score = 0
        subgrid_score = 0

        # Check the row
        for row in self.board:
            row_score += len(set(row)) 

        # Check the column
        for col in range(4):
            column = [self.board[row][col] for row in range(4)]
            col_score += len(set(column))

        # Check the subgrid
        for start_row in range(0, 4, 2):
            for start_col in range(0, 4, 2):
                subgrid = set()
                for r in range(start_row, start_row + 2):
                    for c in range(start_col, start_col + 2):
                        subgrid.add(self.board[r][c])
                subgrid_score += len(subgrid)
                
        duplicate_penalty = 0
        for row in self.board:
            duplicate_penalty += len(row) - len(set(row))
        for col in range(4):
            column = [self.board[row][col] for row in range(4)]
            duplicate_penalty += len(column) - len(set(column))
        for start_row in range(0, 4, 2):
            for start_col in range(0, 4, 2):
                subgrid = [
                    self.board[r][c]
                    for r in range(start_row, start_row + 2)
                    for c in range(start_col, start_col + 2)
                ]
                duplicate_penalty += len(subgrid) - len(set(subgrid))

        
        incomplete_penalty = sum(row.count(0) for row in self.board)
        self.fitness = row_score + col_score + subgrid_score - duplicate_penalty - incomplete_penalty


class GeneticAlgorithm:
    def __init__(self, puzzle, population_size=100, generations=500, mutation_rate=0.1, crossover_rate=0.7):
        self.puzzle = puzzle
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.best_individual = None

    def initialize_population(self):
        for _ in range(self.population_size):
            board = [row[:] for row in self.puzzle]

            for r in range(4):
                empty_cells = [c for c in range(4) if board[r][c] == 0]
                for c in empty_cells:
                    possible_values = set(range(1, 5))
                    for i in range(4):
                        possible_values.discard(board[r][i])
                        possible_values.discard(board[i][c])
                    start_row, start_col = (r // 2) * 2, (c // 2) * 2
                    for rr in range(start_row, start_row + 2):
                        for cc in range(start_col, start_col + 2):
                            possible_values.discard(board[rr][cc])
                    if possible_values:
                        board[r][c] = random.choice(list(possible_values))

            individual = Individual(board)
            individual.calculate_fitness()
            self.population.append(individual)

    def select_parents(self):
        total_fitness = sum(ind.fitness for ind in self.population)
        probabilities = [ind.fitness / total_fitness for ind in self.population]
        parents = random.choices(self.population, probabilities, k=2)
        return parents

    def crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            crossover_point = random.randint(0, 3)
            child_board = [
                parent1.board[row][:crossover_point] + parent2.board[row][crossover_point:]
                for row in range(4)
            ]
            return Individual(child_board)
        else:
            return  Individual(parent1.board[:])

    def mutate(self, individual):
        for r in range(4):
            if random.random() < self.mutation_rate:
                empty_cells = [c for c in range(4) if self.puzzle[r][c] == 0]
                if len(empty_cells) > 1:
                    c1, c2 = random.sample(empty_cells, 2)
                    individual.board[r][c1], individual.board[r][c2] = individual.board[r][c2], individual.board[r][c1]

        # Ensure that empty cells
        for r in range(4):
            for c in range(4):
                if self.puzzle[r][c] == 0:  # Only mutate empty cells
                    possible_values = set(range(1, 5))
                    for i in range(4):
                        possible_values.discard(individual.board[r][i])  # Row values
                        possible_values.discard(individual.board[i][c])  # Column values
                    # Subgrid values
                    start_row, start_col = (r // 2) * 2, (c // 2) * 2
                    for rr in range(start_row, start_row + 2):
                        for cc in range(start_col, start_col + 2):
                            possible_values.discard(individual.board[rr][cc])
                    if possible_values:
                        individual.board[r][c] = random.choice(list(possible_values))

    def evolve(self):
        self.initialize_population()
        best_fitness_over_time = []
        best_fitness = -float("inf")

        for generation in range(self.generations):
            self.population.sort(key=lambda ind: ind.fitness, reverse=True)
            best_fitness_over_time.append(self.population[0].fitness)

            if self.population[0].fitness > best_fitness:
                best_fitness = self.population[0].fitness
                self.best_individual = self.population[0]

            new_population = []

            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents()
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                child.calculate_fitness()
                new_population.append(child)

            self.population = new_population

        if any(0 in row for row in self.best_individual.board):
            print("Incomplete solution detected. Increase generations or adjust parameters.")

        return best_fitness_over_time

    def get_solution(self):
        return self.best_individual.board


# Example puzzle
SPG = SudokuPuzzleGenerator(size=4)
solution = SPG.generate_full_solution()
puzzle = SPG.remove_values_to_create_puzzle(solution, clues=5)

ga = GeneticAlgorithm(puzzle, crossover_rate=0.7)  # Set crossover_rate to 0.7
best_fitness_over_time = ga.evolve()

print("\nSolved Sudoku:")
for row in ga.get_solution():
    print(" ".join(str(num) if num != 0 else "." for num in row))
print("\nBest fitness score:", ga.best_individual.fitness)

plt.plot(best_fitness_over_time)
plt.title("Fitness Score Over Generations")
plt.xlabel("Generations")
plt.ylabel("Fitness Score")
plt.show()

