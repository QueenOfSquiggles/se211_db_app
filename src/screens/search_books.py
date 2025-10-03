import tkinter as tk
from .util import center_window
from .main_portal import MainPortal

class SearchBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Insert Books")
        center_window(200, 150, base)
        tk.Button(self, text="Home", command=self.return_home).pack()
        # add elements here

        tk.Label(self, text="Insert Books Screen").pack()

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
    SearchBooksFrame(root)
    root.mainloop()