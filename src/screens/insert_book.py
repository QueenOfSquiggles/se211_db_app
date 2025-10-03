from .util import center_window
import tkinter as tk
from .main_portal import MainPortal 

class InsertBookFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Insert Books")
        center_window(200, 150, base)
        # add elements here
        tk.Button(self, text="Home", command=self.return_home).pack()
        tk.Label(self, text="Hello there").pack()


        # 
        self.pack()

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        MainPortal(self.base)