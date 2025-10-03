from .util import center_window
import tkinter as tk
from .main_portal import MainPortal 


class ManageBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("")
        center_window(200, 150, base)
        # add elements here




        # 
        self.pack()