import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import *


#Create the puzzle solver window
puzzle_solver = tk.Tk()
puzzle_solver.title("Puzzle solver Page")
puzzle_solver.geometry("800x600")

# background
path = './photos/Puzzle solver.png'
Set_background(event=None, page_name=puzzle_solver, path=path)
# resize image dynamic
puzzle_solver.bind('<Configure>', lambda e:Set_background(e, page_name=puzzle_solver, path=path))

flex_window(puzzle_solver, 800, 600)

#button back
path_action = './GUI/Main Page.py'
create_back_button(puzzle_solver,path_action)

# go to select difficulty page
path_select = './GUI/select_difficulty.py'
def select_difficulty_action(sudoku_type):
    subprocess.Popen(['python', path_select, sudoku_type])
    puzzle_solver.quit()

# 4x4 Sudoku Button
sudoku_4x4_button = tk.Button(
    puzzle_solver,
    text="4x4 Sudoku",
    font=("Helvetica", 16, "bold"),
    bg="#4CAF50",
    fg="white",
    padx=20,
    pady=10,
    borderwidth=5,
    relief="raised",  
    highlightthickness=2,
    highlightbackground="#4CAF50",
    command=lambda: select_difficulty_action("4x4")
)
sudoku_4x4_button.place(relx=0.5, rely=0.3, anchor="center")

# 6x6 sudoku Button
sudoku_6x6_button = tk.Button(
    puzzle_solver,
    text="6x6 Sudoku",
    font=("Helvetica", 16, "bold"),
    bg="#FF6347",
    fg="white",
    padx=20,
    pady=10,
    borderwidth=5,
    relief="raised",  
    highlightthickness=2,
    highlightbackground="#FF6347",
    command=lambda: select_difficulty_action("6x6")
)
sudoku_6x6_button.place(relx=0.5, rely=0.5, anchor="center")

# 9x9 sudoku Button
sudoku_9x9_button = tk.Button(
    puzzle_solver,
    text="9x9 Sudoku",
    font=("Helvetica", 16, "bold"),
    bg="#FFD700",
    fg="white",
    padx=20,
    pady=10,
    borderwidth=5,
    relief="raised",  
    highlightthickness=2,
    highlightbackground="#FFD700",
    command=lambda: select_difficulty_action("9x9")
)
sudoku_9x9_button.place(relx=0.5, rely=0.7, anchor="center")


# Run
puzzle_solver.mainloop()
