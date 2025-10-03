import tkinter as tk
from .util import center_window

class MainPortal(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.construct()

    def construct(self):
        self.base.title("Database System")
        center_window(200, 150, self.base)
        insert = tk.Button(self, \
            text="Insert function", \
            justify=tk.CENTER, \
            command=self.open_insert)
        insert.pack()

        self.pack()

    def open_insert(self):
        self.close_self()
        from . import insert_book
        insert_book.InsertBookFrame(self.base)

    def open_manage(self):
        self.close_self()
        from . import manage_books
        manage_books.ManageBooksFrame(self.base)

    def open_place_hold(self):
        self.close_self()
        from . import place_hold
        place_hold.PlaceHoldFrame(self.base)

    def open_search(self):
        self.close_self()
        from . import search_books
        search_books.SearchBooksFrame(self.base)

    def close_self(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

