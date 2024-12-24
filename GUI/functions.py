import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess
import numpy as np
import random
from random_generation import *

# to make the background fill the screen
def Set_background(event , page_name, path):
    
    window_width = page_name.winfo_width()
    window_height = page_name.winfo_height()

    bg_image = Image.open(path)
    bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    # Check if the label already exists, if not, create it
    if not hasattr(page_name, 'bg_label'):
        page_name.bg_label = tk.Label(page_name, image=bg_photo)
        page_name.bg_label.place(relwidth=1, relheight=1)  
    else:
        # If the label exists, just update the image
        page_name.bg_label.config(image=bg_photo)
    
    
    page_name.bg_label.image = bg_photo
    
 # Back button
def back_previous_page(path, page_name, *args):
    subprocess.Popen(['python', path] + list(map(str, args)))
    page_name.quit()
    
# go to the next page
def go_next_page(path, page_name, *args):
    subprocess.Popen(['python', path]+ list(map(str, args)))
    page_name.quit()


# to make flexable window
def flex_window(page_name, width, height):
    screen_width = page_name.winfo_screenwidth()
    screen_height = page_name.winfo_screenheight()
    
    window_width = width
    window_height = height
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # new postion 
    page_name.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    
#to create back button
def create_back_button(page_name, path_action, *args):
    icon_path='./photos/back-icon.png'
    button_size=(50, 50)
    button_position=(10, 10)
    back_icon = Image.open(icon_path)
    back_icon = back_icon.resize(button_size, Image.Resampling.LANCZOS)
    back_photo = ImageTk.PhotoImage(back_icon)

    # Create the back button
    back_button = tk.Button(
        page_name,
        image=back_photo,
        command=lambda: back_previous_page(path_action, page_name, *args),
        borderwidth=5,
        relief="raised",
        bg='#A0A0A0'
    )
    back_button.image = back_photo 
    back_button.place(x=button_position[0], y=button_position[1])

    return back_button


#generate the random initialize puzzle
def random_puzzle(size, clues):
    SPG = SudokuPuzzleGenerator(size=size)
    solution = SPG.generate_full_solution()
    puzzle = SPG.remove_values_to_create_puzzle(solution, clues=clues)
    
    return puzzle

#go to next page based on difficulty:
def go_with_clues(page_name, path, clues, *args):
    subprocess.Popen(['python', path, str(clues)] + list(map(str, args)))
    page_name.quit()