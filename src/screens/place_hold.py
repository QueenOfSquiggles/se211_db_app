from .util import resize_window
import tkinter as tk
from .main_portal import MainPortal 


class PlaceHoldFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Place Hold")
        resize_window(base)
        tk.Button(self, text="Home", command=self.return_home).pack()
        # add elements here

        tk.Label(self, text="Placing Holds Screen").pack()

        # end elements section

        self.pack()

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        MainPortal(self.base)

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    PlaceHoldFrame(root)
    root.mainloop()