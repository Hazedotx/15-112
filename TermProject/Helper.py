#This file is for helper functions which shouldnt take up space in Main.py
import tkinter as tk # this will only be utilized to grab the players screen dimensions

def grabScreenDimensions():
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width,height