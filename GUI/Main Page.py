import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from functions import *


# Create the main window
Main = tk.Tk()
Main.title("Main Page")
Main.geometry("800x600") 

# Background
path = "./photos/main page.png"
Set_background(event=None, page_name=Main, path=path)

# resize image dynamic
Main.bind('<Configure>', lambda event: Set_background(event, page_name=Main, path=path))

flex_window(Main, 800, 600)


# welcome label
Welcom_label = tk.Label(
    Main,
    text="Welcome to the Puzzels solver",
    font=("Helvetica", 18, "bold"),
    bg="#FF4500",
    fg="white"
)
Welcom_label.pack(pady=20)


# to go puzzle solver page
path_action = './GUI/Puzzle solver.py'
def go():
    go_next_page(path_action, Main)

# Play button
play_button = tk.Button(
    Main,
    text="Play",
    font=("Helvetica", 20, "bold"),
    bg="#FF4500", 
    fg="white", 
    padx=20,
    pady=10,
    borderwidth=5,  
    relief="raised",  
    highlightthickness=2,  
    highlightbackground="#4CAF50",  
    command= go
)
play_button.place(relx=0.5, rely=1.0, anchor="s", y= -25)

# Run
Main.mainloop()
