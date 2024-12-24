import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import *
from GA_4x4 import GeneticAlgorithm
import sys

if len(sys.argv) > 1:
    clues = int(sys.argv[1])

# Example puzzle
puzzle = random_puzzle(size=4, clues=clues)

# Function to display the board in the GUI
def display_board(board, labels):
    for r in range(4):
        for c in range(4):
            labels[r][c]["text"] = str(board[r][c]) if board[r][c] != 0 else " "

# Solve the Sudoku using the Genetic Algorithm
def solve_sudoku():
    global puzzle, labels, fitness_score_var

    # Initialize and solve the Sudoku puzzle using the Genetic Algorithm
    ga = GeneticAlgorithm(puzzle)
    best_fitness = ga.evolve()
    solution = ga.get_solution()

    # Update the GUI with the solution
    display_board(solution, labels)

    # Update the fitness score
    fitness_score_var.set(ga.best_individual.fitness)

# Create the Sudoku Solver GUI
sudoku_4x4 = tk.Tk()
sudoku_4x4.title("Sudoku 4x4 Solver")
sudoku_4x4.geometry("1000x700")

# background
path = './photos/Sudoku 4x4.png'
Set_background(event=None, page_name=sudoku_4x4, path=path)
# resize image dynamically
sudoku_4x4.bind('<Configure>', lambda e: Set_background(e, page_name=sudoku_4x4, path=path))

flex_window(sudoku_4x4, 1000, 700)

# Button back
path_action = './GUI/select_difficulty.py'
create_back_button(sudoku_4x4, path_action, "4x4")

# to make the grid like board sudoku
for i in range(8): 
    sudoku_4x4.grid_rowconfigure(i, weight=1)
    sudoku_4x4.grid_columnconfigure(i, weight=1)

# Display the puzzle grid (centered)
labels = [[None for _ in range(4)] for _ in range(4)]
for r in range(4):
    for c in range(4):
        label = tk.Label(
            sudoku_4x4,
            text=".",
            font=("Helvetica", 20, "bold"),
            width=2,
            height=2,
            relief="solid",
            borderwidth=1,
            bg="white"
        )
        # Offset grid placement to center the board (starts at row=2, column=2)
        label.grid(row=r + 2, column=c + 2, padx=5, pady=5, sticky="nsew")
        labels[r][c] = label

# Display the initial puzzle
display_board(puzzle, labels)

# Fitness Score Label (centered in the frame)
fitness_score_label = tk.Label(
    sudoku_4x4,
    text="Fitness Score:",
    font=("Helvetica", 14, "bold"),
)
fitness_score_label.place(relx=0.3, rely=0.9, anchor="center")

# Fitness Score Entry (set to N/A, centered)
fitness_score_var = tk.StringVar(value="N/A")
fitness_score_entry = ttk.Entry(
    sudoku_4x4,
    textvariable=fitness_score_var,
    font=("Helvetica", 14),
    width=10
)
fitness_score_entry.place(relx=0.5, rely=0.9, anchor="center")

# Correct Fitness Label (next to Fitness Score label)
correct_fitness_label = tk.Label(
    sudoku_4x4,
    text="Correct Fitness:",
    font=("Helvetica", 14, "bold"),
)
correct_fitness_label.place(relx=0.3, rely=0.96, anchor="center")

# Correct Fitness Entry (set to 48)
correct_fitness_var = tk.StringVar(value="48")
correct_fitness_entry = ttk.Entry(
    sudoku_4x4,
    textvariable=correct_fitness_var,
    font=("Helvetica", 14),
    width=10
)
correct_fitness_entry.place(relx=0.5, rely=0.96, anchor="center")

# Solver Button (centered below the entries)
solver_button = tk.Button(
    sudoku_4x4,
    text="Solver",
    font=("Helvetica", 14, "bold"),
    fg="white",
    width=10,
    height=2,
    command=solve_sudoku,
    relief="raised",
    bg='#8B4513'
)
solver_button.place(relx=0.7, rely=0.92, anchor="center") 

# Run the GUI
sudoku_4x4.mainloop()
