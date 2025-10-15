import tkinter as tk
import sqlite3
from .main_portal import MainPortal
from .util import resize_window

DATABASE_NAME = "library.sqlite3"

class SearchBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Search Books")
        resize_window(base)

        self.connection = sqlite3.connect("db")

        # Variables
        self.search_var = tk.StringVar()
        self.criteria_var = tk.StringVar(value="Title")  # default search by title
        self.results_var = tk.StringVar(value="")  # for displaying results

        # Widgets
        tk.Button(self, text="Home", command=self.return_home).pack(pady=5)

        # Search input
        form_frame = tk.Frame(self)
        tk.Label(form_frame, text="Search:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(form_frame, textvariable=self.search_var, width=40).grid(row=0, column=1, padx=5)

        # Criteria (Title / Author / Category)
        tk.Label(form_frame, text="Search by:").grid(row=1, column=0, sticky="e", padx=5)
        tk.OptionMenu(form_frame, self.criteria_var, "Title", "Author", "Category").grid(row=1, column=1, sticky="w", padx=5)

        form_frame.pack(pady=10)

        # Search button
        tk.Button(self, text="Search", command=self.perform_search).pack(pady=5)

        # Results label
        tk.Label(self, text="Results:").pack()
        self.results_text = tk.Text(self, height=15, width=60)
        self.results_text.pack(pady=5)

        self.pack()

    def perform_search(self):
        self.results_text.delete("1.0", tk.END)  # clear previous results
        search_text = self.search_var.get().strip()
        criteria = self.criteria_var.get()

        if not search_text:
            self.results_text.insert(tk.END, "Please enter a search term.\n")
            return

        cursor = self.connection.cursor()
        if criteria == "Title":
            query = """
                SELECT Book.Title, Author.Name, Category.Name
                FROM Book
                JOIN BookAuthor ON Book.ID = BookAuthor.BookID
                JOIN Author ON Author.ID = BookAuthor.AuthorID
                JOIN BookIsCategory ON Book.ID = BookIsCategory.BookID
                JOIN Category ON Category.ID = BookIsCategory.CategoryID
                WHERE Book.Title LIKE ?;
            """
        elif criteria == "Author":
            query = """
                SELECT Book.Title, Author.Name, Category.Name
                FROM Book
                JOIN BookAuthor ON Book.ID = BookAuthor.BookID
                JOIN Author ON Author.ID = BookAuthor.AuthorID
                JOIN BookIsCategory ON Book.ID = BookIsCategory.BookID
                JOIN Category ON Category.ID = BookIsCategory.CategoryID
                WHERE Author.Name LIKE ?;
            """
        else:  # Category
            query = """
                SELECT Book.Title, Author.Name, Category.Name
                FROM Book
                JOIN BookAuthor ON Book.ID = BookAuthor.BookID
                JOIN Author ON Author.ID = BookAuthor.AuthorID
                JOIN BookIsCategory ON Book.ID = BookIsCategory.BookID
                JOIN Category ON Category.ID = BookIsCategory.CategoryID
                WHERE Category.Name LIKE ?;
            """

        search_term = f"%{search_text}%"
        cursor.execute(query, (search_term,))
        results = cursor.fetchall()
        cursor.close()

        if results:
            for title, author, category in results:
                self.results_text.insert(tk.END, f"Title: {title}\nAuthor: {author}\nCategory: {category}\n\n")
        else:
            self.results_text.insert(tk.END, "No matching books found.\n")

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.connection.commit()
        self.connection.close()
        self.destroy()
        MainPortal(self.base)

if __name__ == "__main__":
    root = tk.Tk()
    SearchBooksFrame(root)
    root.mainloop()
