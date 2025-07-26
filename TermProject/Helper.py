#This file is for helper functions which shouldnt take up space in Main.py
import tkinter as tk # this will only be utilized to grab the players screen dimensions

def grabScreenDimensions():
    root = tk.Tk()
    root.withdraw()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.destroy()
    return width,height


def getColliding(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 < x2 + w2) and (x1 + w1 > x2) and (y1 < y2 + h2) and (y1 + h1 > y2)