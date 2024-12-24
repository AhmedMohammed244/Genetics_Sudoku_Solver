import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from random import randint
from functions import * 

# create a 9x9 grid
def create_sudoku_grid(frame):
    grid = []
    for i in range(9):
        row = []
        for j in range(9):
            # Create a button for each cell in the Sudoku grid
            cell = tk.Button(frame, text="", font=("Helvetica", 14), width=4, height=2,
                             relief="solid", command=lambda i=i, j=j: on_cell_click(i, j))
            cell.grid(row=i, column=j, padx=2, pady=2)
            row.append(cell)
        grid.append(row)
    return grid

# add random values 
def populate_grid(grid):
    for i in range(9):
        for j in range(9):
            random_number = randint(1, 9)
            grid[i][j].config(text=str(random_number))

# action when cell click
def on_cell_click(i, j):
    print(f"Cell {i},{j} clicked!")

# to solve sudoku
def solve_sudoku():
    print("Solving Sudoku...") 

# Create the sudoku window
sudoku = tk.Tk()
sudoku.title("Sudoku Page")
sudoku.geometry("1000x600")

# Background image for the main window
path = "./photos/Sudoku.png"
Set_background(event=None, page_name=sudoku, path=path)

# Resize image dynamically
sudoku.bind('<Configure>', lambda event: Set_background(event, page_name=sudoku, path=path))

flex_window(sudoku, 1000, 600)

# Create a frame widow 
frame = tk.Frame(sudoku)
frame.place(relx=0.5, rely=0.5, anchor="center") 

# background of frame
Set_background(event=None, page_name=frame, path=path)

# Resize frame dynamically
frame.bind('<Configure>', lambda event: Set_background(event, page_name=frame, path=path))

# Create Sudoku grid inside the frame
sudoku_grid = create_sudoku_grid(frame)

# Populate the grid with random numbers
populate_grid(sudoku_grid)

# Button to go back to the main page
back_icon = Image.open('./photos/back-icon.png')
back_icon = back_icon.resize((50, 50), Image.Resampling.LANCZOS)
back_photo = ImageTk.PhotoImage(back_icon)

# To go back to the main page 
path_action = './GUI/Puzzle solver.py'
def back():
    back_previous_page(path_action, sudoku)

back_button = tk.Button(
    sudoku,
    image=back_photo,
    command=back,
    borderwidth=5,
    relief="raised",
    bg='#A0A0A0'
)
back_button.image = back_photo
back_button.place(x=10, y=10)

# Create the Solver button
solver_button = tk.Button(
    sudoku,
    text="Solver",
    font=("Helvetica", 14 , 'bold'),
    fg='white',
    width=10,
    height=2,
    command=solve_sudoku,
    relief="raised",
    bg='#FFA500'
)
solver_button.place(relx=0.90, rely=0.5, anchor="center")  

# Run the sudoku window
sudoku.mainloop()
