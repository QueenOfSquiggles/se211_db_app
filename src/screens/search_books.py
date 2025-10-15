import tkinter as tk
from tkinter import ttk
import sqlite3
from .util import resize_window
from .main_portal import MainPortal

DATABASE_NAME = "library.sqlite3"

class SearchBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Search Books")
        resize_window(base)
        self.connection = sqlite3.connect("db")

        # Search input variables
        self.title_var = tk.StringVar()
        self.author_var = tk.StringVar()
        self.category_var = tk.StringVar()

        # Search results
        self.results_var = tk.StringVar(value=[])

        self.build_ui()
        self.pack(expand=True, fill=tk.BOTH)

    def build_ui(self):
        # Home button
        tk.Button(self, text="Home", command=self.return_home).pack(anchor='ne', padx=10, pady=10)

        form_frame = tk.LabelFrame(self, text="Search for Books")
        form_frame.pack(padx=10, pady=10, fill=tk.X)

        # Title search
        tk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.title_var).grid(row=0, column=1, sticky=tk.EW)

        # Author search
        tk.Label(form_frame, text="Author:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.author_var).grid(row=1, column=1, sticky=tk.EW)

        # Category search
        tk.Label(form_frame, text="Category:").grid(row=2, column=0, sticky=tk.W)
        tk.Entry(form_frame, textvariable=self.category_var).grid(row=2, column=1, sticky=tk.EW)

        form_frame.columnconfigure(1, weight=1)

        # Search button
        tk.Button(self, text="Search", command=self.perform_search).pack(pady=5)

        # Results list
        results_frame = tk.LabelFrame(self, text="Search Results")
        results_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.results_listbox = tk.Listbox(results_frame, listvariable=self.results_var, height=10)
        self.results_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.results_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_listbox.config(yscrollcommand=scrollbar.set)

    def perform_search(self):
        title = self.title_var.get().strip()
        author = self.author_var.get().strip()
        category = self.category_var.get().strip()

        c = self.connection.cursor()
        query = """
            SELECT DISTINCT Book.Title
            FROM Book
            LEFT JOIN BookAuthor ON Book.ID = BookAuthor.BookID
            LEFT JOIN Author ON BookAuthor.AuthorID = Author.ID
            LEFT JOIN BookIsCategory ON Book.ID = BookIsCategory.BookID
            LEFT JOIN Category ON BookIsCategory.CategoryID = Category.ID
            WHERE 1 = 1
        """
        params = []

        if title:
            query += " AND Book.Title LIKE ?"
            params.append(f"%{title}%")
        if author:
            query += " AND Author.Name LIKE ?"
            params.append(f"%{author}%")
        if category:
            query += " AND Category.Name LIKE ?"
            params.append(f"%{category}%")

        print("Executing query:", query)
        print("With parameters:", params)
        c.execute(query, params)
        results = c.fetchall()
        c.close()

        # Update listbox with results
        if results:
            book_titles = [r[0] for r in results]
        else:
            book_titles = ["No results found."]

        self.results_var.set(book_titles)

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.connection.close()
        self.destroy()
        MainPortal(self.base)

