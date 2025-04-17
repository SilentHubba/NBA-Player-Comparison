from tkinter import *
from tkinter import ttk
import numpy as np

class Canvas:
    def __init__(self, root):
        root.title("NBA Player Comparison")

        # Configure the root so that it stretches in all directions
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # change the style
        style = ttk.Style(root)
        style.theme_use('clam')

        # make a frame for the GUI
        self.frame = ttk.Frame(root, padding = "10 10 10 10")
        self.frame.grid(column=0, row=0, sticky=(N, W, E, S))

        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.columnconfigure(3, weight=1)

        # add a label for the new window
        label = ttk.Label(self.frame,
                          text="Select Two Players:", 
                          justify="center")
        label.grid(column=0, row=0, sticky=(W, E), columnspan=4)
        label.configure(anchor="center")



# create a root Tk object
root = Tk()

# create a HeyThere object with the Tk root object as an argument
Canvas(root)

# call the mainloop method on the Tk root object
root.mainloop()