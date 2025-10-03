from .util import center_window
import tkinter as tk
from .main_portal import MainPortal 


class SearchBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("")
        center_window(200, 150, base)
        # add elements here

        submit_button = tk.Button(self, text="Back", width=8, command = self.on_back)
        submit_button.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()

    def on_back(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    SearchBooksFrame(root)
    root.mainloop()