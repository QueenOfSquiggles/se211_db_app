from util import resize_window
import tkinter as tk
import sqlite3
from main_portal import MainPortal 


class PlaceHoldFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Place Hold")
        self.connection = sqlite3.connect("db")
        resize_window(base)
        tk.Button(self, text="Home", command=self.return_home).pack()
        # add elements here

        tk.Label(self, text="Placing Holds Screen").pack()
        self.avar = tk.StringVar()
        self.bvar = tk.StringVar()
        ea = tk.Entry(self, textvariable=self.avar)
        eb = tk.Entry(self, textvariable=self.bvar)
        ea.pack()
        eb.pack()
        tk.Button(self, text="Submit", command=self.place_hold).pack()
        # end elements section

        self.pack()
        ea.bind("<Return>", self.handle_enter)
        eb.bind("<Return>", self.handle_enter)
    
    def place_hold(self):
        ta = self.avar.get().strip()
        tb = self.bvar.get().strip()
        print(f"A={ta}, B={tb}")
    
    def handle_enter(self, event):
        self.place_hold()


    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.connection.close()
        self.destroy()
        self.unbind("<Return>")
        MainPortal(self.base)

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    PlaceHoldFrame(root)
    root.mainloop()