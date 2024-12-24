import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import *
import sys

if len(sys.argv) < 2:
    print("Missing Sudoku type (4x4, 6x6, 9x9)")
    sys.exit(1)
#sudoku type
sudoku_type = sys.argv[1]

clues_map ={
    "4x4": {"Easy": 9, "Medium": 7, "Hard": 5},   
    "6x6": {"Easy": 18, "Medium": 14, "Hard": 10},   
    "9x9": {"Easy": 49, "Medium": 38, "Hard": 30},
}

# Create the main window
select = tk.Tk()
select.title("Main Page")
select.geometry("800x600") 

# background
path = './photos/select level.png'
Set_background(event=None, page_name=select, path=path)
# resize image dynamic
select.bind('<Configure>', lambda e:Set_background(e, page_name=select, path=path))

flex_window(select, 800, 600)

#button back
path_action = './GUI/Puzzle solver.py'
create_back_button(select,path_action)

#sudoku function based on difficulty
def sudoku_action(difficulty):
    clues = clues_map[sudoku_type][difficulty]
    path_to_sudoku = f'./GUI/sudoku_{sudoku_type}.py'
    go_with_clues(select, path_to_sudoku, clues)
    


#Easy
easy = tk.Button(
    select,
    text="Easy",
    font=("Helvetica", 16, "bold"),
    bg="#ADD8E6",
    fg="white",
    padx=20,
    pady=10,
    borderwidth=5,
    relief="raised",  
    highlightthickness=2,
    highlightbackground="#ADD8E6",
    command=lambda: sudoku_action("Easy")
)
easy.place(relx=0.2, rely=0.5, anchor="center")

#Medium
medium = tk.Button(
    select,
    text="Medium",
    font=("Helvetica", 16, "bold"),
    bg="#FFA500",
    fg="white",
    padx=20,
    pady=10,
    borderwidth=5,
    relief="raised",  
    highlightthickness=2,
    highlightbackground="#FFA500",
    command=lambda: sudoku_action("Medium")
)
medium.place(relx=0.5, rely=0.5, anchor="center")

#hard
hard = tk.Button(
    select,
    text="Hard",
    font=("Helvetica", 16, "bold"),
    bg="#8B0000",
    fg="white",
    padx=20,
    pady=10,
    borderwidth=5,
    relief="raised",  
    highlightthickness=2,
    highlightbackground="#8B0000",
    command=lambda: sudoku_action("Hard")
)
hard.place(relx=0.8, rely=0.5, anchor="center")


select.mainloop()