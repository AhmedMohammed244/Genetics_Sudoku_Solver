import random
import matplotlib.pyplot as plt
import math
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Random_Puzzle import *



class Individual:
    def __init__(self, board, size, subgrid_dims):
        self.board = board
        self.size = size
        self.subgrid_dims = subgrid_dims
        self.fitness = 0

    def calculate_fitness(self):
        row_score = sum(len(set(row)) for row in self.board)
        col_score = sum(len(set(self.board[r][c] for r in range(self.size))) for c in range(self.size))
            
        
        subgrid_score = 0
        rows, cols = self.subgrid_dims # 3x3
        for start_row in range(0, self.size, rows):
            for start_col in range(0, self.size, cols):
                subgrid = set()
                for r in range(start_row, start_row + rows):
                    for c in range(start_col, start_col + cols):
                        subgrid.add(self.board[r][c])
                subgrid_score += len(subgrid)
                
        # to check the duplicates
        duplicate_penalty = 0
        for row in self.board:
            duplicate_penalty += len(row) - len(set(row))
        for col in range(self.size):
            column = [self.board[row][col] for row in range(self.size)]
            duplicate_penalty += len(column) - len(set(column))
            
        #subgrid
        for start_row in range(0, self.size, rows):
            for start_col in range(0, self.size, cols):
                subgrid = [
                    self.board[r][c]
                    for r in range(start_row, start_row + rows)
                    for c in range(start_col, start_col + cols)
                ]
                duplicate_penalty += len(subgrid) - len(set(subgrid))

        incomplete_penalty = sum(row.count(0) for row in self.board)
        self.fitness = row_score + col_score + subgrid_score - duplicate_penalty - incomplete_penalty


class GeneticAlgorithm:
    def __init__(self, puzzle, size, population_size=100, generations=500, mutation_rate=0.1, crossover_rate=0.7):
        self.puzzle = puzzle
        self.size = size
        self.subgrid_dims = self.calculate_subgrid_dims(size)
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.population = []
        self.best_individual = None

    def calculate_subgrid_dims(self, size):
        # special cases
        if size == 6:
            return (2, 3)
        elif size == 12:
            return (3, 4)
        elif size == 20:
            return (4, 5)
        
        # find dimentions
        dimentions = []     
        for i in range(1, int(math.sqrt(size)) + 1):
            if size % i == 0:
                dimentions.append((i, size // i))   
    
        #the most square like subgrid (ex: (3,3))
        return dimentions[-1]


    def initialize_population(self):
        for _ in range(self.population_size):
            
            #copy puzzle in board
            board = [row[:] for row in self.puzzle]

            # Fill empty cells 
            for r in range(self.size):
                empty_cells = [c for c in range(self.size) if board[r][c] == 0]
                for c in empty_cells:
                    possible_values = set(range(1, self.size + 1))
                    for i in range(self.size):
                        possible_values.discard(board[r][i])  # Row values
                        possible_values.discard(board[i][c])  # Column values
                        
                    # Subgrid values 
                    start_row, start_col = (r // self.subgrid_dims[0]) * self.subgrid_dims[0], (c // self.subgrid_dims[1]) * self.subgrid_dims[1]
                    for rr in range(start_row, start_row + self.subgrid_dims[0]):
                        for cc in range(start_col, start_col + self.subgrid_dims[1]):
                            possible_values.discard(board[rr][cc])
                    if possible_values:
                        board[r][c] = random.choice(list(possible_values))   
            
            #create new individual
            individual = Individual(board, self.size, self.subgrid_dims)
            individual.calculate_fitness()
            self.population.append(individual)

    def select_parents(self):
        # using roulette wheel selection
        total_fitness = sum(ind.fitness for ind in self.population)
        probabilities = [ind.fitness / total_fitness for ind in self.population]
        return random.choices(self.population, probabilities, k=2)

    def crossover(self, parent1, parent2):
        # random from floating 0.0 and 1.0
        if random.random() < self.crossover_rate:   
            crossover_point = random.randint(0, self.size - 1) 
            offspring = [
                parent1.board[row][:crossover_point] + parent2.board[row][crossover_point:]
                for row in range(self.size)
            ]
            return Individual(offspring, self.size, self.subgrid_dims)
        else:
            
            return random.choices([parent1, parent2], k=1)[0]

    def mutate(self, individual):
        for r in range(self.size):
            if random.random() < self.mutation_rate:
                empty_cells = [c for c in range(self.size) if self.puzzle[r][c] == 0]
                if len(empty_cells) > 1:
                    c1, c2 = random.sample(empty_cells, 2)
                    individual.board[r][c1], individual.board[r][c2] = individual.board[r][c2], individual.board[r][c1]
                    
                    
        # Ensure that empty cells
        for r in range(self.size):
            for c in range(self.size):
                if self.puzzle[r][c] == 0:  # Only mutate empty cells
                    possible_values = set(range(1, self.size + 1))
                    for i in range(self.size):
                        possible_values.discard(individual.board[r][i])  # Row values
                        possible_values.discard(individual.board[i][c])  # Column values
                    # Subgrid values
                    start_row, start_col = (r // self.subgrid_dims[0]) * self.subgrid_dims[0], (c // self.subgrid_dims[1]) * self.subgrid_dims[1]
                    for rr in range(start_row, start_row + self.subgrid_dims[0]):
                        for cc in range(start_col, start_col + self.subgrid_dims[1]):
                            possible_values.discard(individual.board[rr][cc])
                    if possible_values:
                        individual.board[r][c] = random.choice(list(possible_values))

    def evolve(self, early_stopping = False):
        self.initialize_population()
        best_fitness_over_time = []
        best_fitness = -float("inf") # make it worst value
        
        target_fitness = self.size * self.size * 3
        

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
            
            
            
            if best_fitness == target_fitness and early_stopping:
                print(f"Optimal solution found at generation {generation + 1}!")
                break

            self.population = new_population

        if any(0 in row for row in self.best_individual.board):
            print("Incomplete solution detected. Increase generations or adjust parameters.")

        return best_fitness_over_time

    def get_solution(self):
        return self.best_individual.board


def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# Example usage
size = 9
clues = 40
SPG = SudokuPuzzleGenerator(size=size)
solution = SPG.generate_full_solution()
puzzle = SPG.remove_values_to_create_puzzle(solution, clues=clues) 

ga = GeneticAlgorithm(puzzle, size=size)
best_fitness_over_time = ga.evolve()


print("\nSolved Sudoku:")
print_board(ga.get_solution())
print("\nBest fitness score:", ga.best_individual.fitness)

plt.plot(best_fitness_over_time)
plt.title("Fitness Score Over Generations")
plt.xlabel("Generations")
plt.ylabel("Fitness Score")
plt.show()
