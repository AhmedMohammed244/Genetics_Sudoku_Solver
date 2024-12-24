import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import *
from GA_6x6 import GeneticAlgorithm
import sys

if len(sys.argv) > 1:
    clues = int(sys.argv[1])
    
# Example puzzle
puzzle = random_puzzle(size=6, clues=clues)

# display puzzle
def display_board(board, labels):
    for r in range(6):
        for c in range(6):
            labels[r][c]["text"] = str(board[r][c]) if board[r][c] != 0 else " "

# Solve the Sudoku using the Genetic Algorithm
def solve_sudoku():
    global puzzle, labels, fitness_score_var

    ga = GeneticAlgorithm(puzzle)
    best_fitness = ga.evolve()
    solution = ga.get_solution()

    # Update GUI with solution
    display_board(solution, labels)

    # Update the fitness score
    fitness_score_var.set(ga.best_individual.fitness)

# Create the Sudoku Solver GUI
sudoku_6x6 = tk.Tk()
sudoku_6x6.title("Sudoku 6x6 Solver")
sudoku_6x6.geometry("1000x600")

# Background image for the main window
path = "./photos/Sudoku 6x6.png"
Set_background(event=None, page_name=sudoku_6x6, path=path)

# Resize image dynamically
sudoku_6x6.bind('<Configure>', lambda event: Set_background(event, page_name=sudoku_6x6, path=path))

flex_window(sudoku_6x6, 1000, 600)

# Button back
path_action = './GUI/select_difficulty.py'
create_back_button(sudoku_6x6,path_action, "6x6")

# to make the grid like board sudoku
for i in range(16):
    sudoku_6x6.grid_rowconfigure(i, weight=1)
    sudoku_6x6.grid_columnconfigure(i, weight=1)

# Display the puzzle grid (centered within the frame)
labels = [[None for _ in range(6)] for _ in range(6)]
for r in range(6):
    for c in range(6):
        label = tk.Label(
            sudoku_6x6,
            text=". ",
            font=("Helvetica", 20, "bold"),
            width=2,
            height=2,
            relief="solid",
            borderwidth=1,
            bg='white' 
        )
        label.grid(row=r+2, column=c+2, padx=5, pady=5, sticky="nsew")
        labels[r][c] = label

# Display initial puzzle
display_board(puzzle, labels)

# Fitness Score Label 
fitness_score_label = tk.Label(
    sudoku_6x6,
    text="Fitness Score:",
    font=("Helvetica", 14, "bold"),
    bg="#ffffff"
)
fitness_score_label.place(relx=0.74, rely=0.3, anchor="center")

# Fitness Score Entry
fitness_score_var = tk.StringVar(value="N/A")
fitness_score_entry = ttk.Entry(
    sudoku_6x6,
    textvariable=fitness_score_var,
    font=("Helvetica", 14),
    width=10
)
fitness_score_entry.place(relx=0.9, rely=0.3, anchor="center")

# Correct Fitness Label 
correct_fitness_label = tk.Label(
    sudoku_6x6,
    text="Correct Fitness:",
    font=("Helvetica", 14, "bold"),
    bg="#ffffff"
)
correct_fitness_label.place(relx=0.74, rely=0.4, anchor="center")

# Correct Fitness Entry 
correct_fitness_var = tk.StringVar(value="108")
correct_fitness_entry = ttk.Entry(
    sudoku_6x6,
    textvariable=correct_fitness_var,
    font=("Helvetica", 14),
    width=10
)
correct_fitness_entry.place(relx=0.9, rely=0.4, anchor="center")

# Solver Button 
solver_button = tk.Button(
    sudoku_6x6,
    text="Solver",
    font=("Helvetica", 14, "bold"),
    fg="white",
    width=10,
    height=2,
    command=solve_sudoku,
    relief="raised",
    bg='#FFA500'
)
solver_button.place(relx=0.83, rely=0.6, anchor="center") 

# Run the GUI
sudoku_6x6.mainloop()
