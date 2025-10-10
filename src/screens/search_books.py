import tkinter as tk
from .util import resize_window
from .main_portal import MainPortal

class SearchBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Search Books")
        resize_window(base)
        tk.Button(self, text="Home", command=self.return_home).pack()
        # add elements here

        tk.Label(self, text="Search Books Screen").pack()

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