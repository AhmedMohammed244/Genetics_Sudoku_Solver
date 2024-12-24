import random
import matplotlib.pyplot as plt

class Individual:
    
    def __init__(self, board):
        self.board = board
        self.fitness = 0
    
    def calculate_fitness(self):
        # Fitness will be based on rows, columns, and subgrids having unique values
        row_score = sum(len(set(row)) for row in self.board)
        col_score = sum(len(set(self.board[r][c] for r in range(9))) for c in range(9))
        subgrid_score = 0
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                subgrid = set()
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        subgrid.add(self.board[r][c])
                subgrid_score += len(subgrid)

        # Penalize based on duplicate values
        duplicate_penalty = 0
        for row in self.board:
            duplicate_penalty += len(row) - len(set(row))
        for col in range(9):
            column = [self.board[row][col] for row in range(9)]
            duplicate_penalty += len(column) - len(set(column))
        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                subgrid = [self.board[r][c] for r in range(start_row, start_row + 3) for c in range(start_col, start_col + 3)]
                duplicate_penalty += len(subgrid) - len(set(subgrid))

        # Penalize incomplete solutions
        incomplete_penalty = sum(row.count(0) for row in self.board)
        self.fitness = row_score + col_score + subgrid_score - duplicate_penalty - incomplete_penalty


class GeneticAlgorithm:
    def __init__(self, puzzle, population_size=100, generations=500, mutation_rate=0.1, crossover_rate = 0.7):
        self.puzzle = puzzle
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate =crossover_rate
        self.population = []
        self.best_individual = None

    def initialize_population(self):
        for _ in range(self.population_size):
            board = [row[:] for row in self.puzzle]  # Copy the puzzle

            # Fill empty cells intelligently with possible values
            for r in range(9):
                empty_cells = [c for c in range(9) if board[r][c] == 0]
                for c in empty_cells:
                    possible_values = set(range(1, 10))
                    for i in range(9):
                        possible_values.discard(board[r][i])  # Row values
                        possible_values.discard(board[i][c])  # Column values
                    # Subgrid values
                    start_row, start_col = (r // 3) * 3, (c // 3) * 3
                    for rr in range(start_row, start_row + 3):
                        for cc in range(start_col, start_col + 3):
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
            crossover_point = random.randint(0, 8)
            offspring1 = [
                parent1.board[row][:crossover_point] + parent2.board[row][crossover_point:]
                for row in range(9)
            ]
            
            return Individual(offspring1)
        else:
            return  Individual(parent1.board[:])

    def mutate(self, individual):
        for r in range(9):
            if random.random() < self.mutation_rate:
                empty_cells = [c for c in range(9) if self.puzzle[r][c] == 0]
                if len(empty_cells) > 1:
                    c1, c2 = random.sample(empty_cells, 2)
                    individual.board[r][c1], individual.board[r][c2] = individual.board[r][c2], individual.board[r][c1]

        # Ensure that empty cells
        for r in range(9):
            for c in range(9):
                if self.puzzle[r][c] == 0:  # Only mutate empty cells
                    possible_values = set(range(1, 10))
                    for i in range(9):
                        possible_values.discard(individual.board[r][i])  # Row values
                        possible_values.discard(individual.board[i][c])  # Column values
                    # Subgrid values
                    start_row, start_col = (r // 3) * 3, (c // 3) * 3
                    for rr in range(start_row, start_row + 3):
                        for cc in range(start_col, start_col + 3):
                            possible_values.discard(individual.board[rr][cc])
                    if possible_values:
                        individual.board[r][c] = random.choice(list(possible_values))


    def evolve(self):
        self.initialize_population()
        best_fitness_over_time = []
        best_fitness = -float('inf')  # Set an initial "worst" fitness value

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
            
         # Check for incomplete solution after all generations
        if any(0 in row for row in self.best_individual.board):
            print("Incomplete solution detected. Increase generations or adjust parameters.")
            
        return best_fitness_over_time

    def get_solution(self):
        return self.best_individual.board
