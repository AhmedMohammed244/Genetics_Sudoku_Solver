import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import *
from GA_9x9 import GeneticAlgorithm
import sys

if len(sys.argv) > 1:
    clues = int(sys.argv[1])
    
# Example puzzle
puzzle = random_puzzle(size=9,clues=clues)

# display board
def display_board(board, labels):
    for r in range(9):
        for c in range(9):
            labels[r][c]["text"] = str(board[r][c]) if board[r][c] != 0 else " "

# call GA file
def solve_sudoku():
    global puzzle, labels, fitness_score_var

    ga = GeneticAlgorithm(puzzle)
    best_fitness = ga.evolve()
    solution = ga.get_solution()

    # Update GUI with solution
    display_board(solution, labels)

    # Update fitness score
    fitness_score_var.set(ga.best_individual.fitness)

# Create the Sudoku Solver GUI
sudoku_9x9 = tk.Tk()
sudoku_9x9.title("Sudoku 9x9 Solver")
sudoku_9x9.geometry("1200x800")
sudoku_9x9.state("zoomed")

# Background image for the main window
path = "./photos/Sudoku 9x9.png"
Set_background(event=None, page_name=sudoku_9x9, path=path)

# Resize image dynamic
sudoku_9x9.bind('<Configure>', lambda event: Set_background(event, page_name=sudoku_9x9, path=path))

#resize window dynaminc
flex_window(sudoku_9x9, 1200, 800)

# Button back
path_action = './GUI/select_difficulty.py'
create_back_button(sudoku_9x9,path_action, "9x9")

# to make the grid like board sudoku
for i in range(16):
    sudoku_9x9.grid_rowconfigure(i, weight=1)
    sudoku_9x9.grid_columnconfigure(i, weight=1)

# Display the puzzle grid (centered within the frame)
labels = [[None for _ in range(9)] for _ in range(9)]
for r in range(9):
    for c in range(9):
        label = tk.Label(
            sudoku_9x9,
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

# Display the initial puzzle
display_board(puzzle, labels)

# Fitness Score Label (centered in the frame)
fitness_score_label = tk.Label(
    sudoku_9x9,
    text="Fitness Score:",
    font=("Helvetica", 14, "bold"),
    bg="#ffffff"
)
fitness_score_label.place(relx=0.85, rely=0.4, anchor="center")

# Fitness Score Entry (set to N/A, centered)
fitness_score_var = tk.StringVar(value="N/A")
fitness_score_entry = ttk.Entry(
    sudoku_9x9,
    textvariable=fitness_score_var,
    font=("Helvetica", 14),
    width=10
)
fitness_score_entry.place(relx=0.95, rely=0.4, anchor="center")

# Correct Fitness Label 
correct_fitness_label = tk.Label(
    sudoku_9x9,
    text="Correct Fitness:",
    font=("Helvetica", 14, "bold"),
    bg="#ffffff"
)
correct_fitness_label.place(relx=0.85, rely=0.5, anchor="center")

# Correct Fitness 
correct_fitness_var = tk.StringVar(value="243")
correct_fitness_entry = ttk.Entry(
    sudoku_9x9,
    textvariable=correct_fitness_var,
    font=("Helvetica", 14),
    width=10
)
correct_fitness_entry.place(relx=0.95, rely=0.5, anchor="center")

# Solver Button 
solver_button = tk.Button(
    sudoku_9x9,
    text="Solver",
    font=("Helvetica", 14, "bold"),
    fg="white",
    width=10,
    height=2,
    command=solve_sudoku,
    relief="raised",
    bg='#FFA500'
)
solver_button.place(relx=0.9, rely=0.6, anchor="center")  # Positioned below both fitness score and correct fitness

# Run the GUI
sudoku_9x9.mainloop()
