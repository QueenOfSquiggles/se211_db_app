import tkinter as tk
from util import resize_window

class MainPortal(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.construct()

    def construct(self):
        self.base.title("Database System")
        resize_window(self.base)
        tk.Button(self, \
            text="Add books into collection", \
            justify=tk.CENTER, \
            command=self.open_insert).pack()
        tk.Button(self, \
            text="Manage collection", \
            justify=tk.CENTER, \
            command=self.open_manage).pack()
        tk.Button(self, \
            text="Place hold on book", \
            justify=tk.CENTER, \
            command=self.open_place_hold).pack()
        tk.Button(self, \
            text="Search books", \
            justify=tk.CENTER, \
            command=self.open_search).pack()
        self.pack()

    def open_insert(self):
        self.close_self()
        import insert_book
        insert_book.InsertBookFrame(self.base)

    def open_manage(self):
        self.close_self()
        import manage_books
        manage_books.ManageBooksFrame(self.base)

    def open_place_hold(self):
        self.close_self()
        import place_hold
        place_hold.PlaceHoldFrame(self.base)

    def open_search(self):
        self.close_self()
        import search_books
        search_books.SearchBooksFrame(self.base)

    def close_self(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()

