import tkinter as tk
from tkinter import messagebox
import csv
from .util import resize_window
from .main_portal import MainPortal

class ManageBooksFrame(tk.Frame):
    def __init__(self, base):
        super().__init__(base)
        self.base = base
        self.base.title("Manage Books")
        resize_window(base)

        # Navigation
        tk.Button(self, text="Home", command=self.return_home).pack(pady=5)
        tk.Label(self, text="Manage Books Screen", font=("Arial", 14)).pack(pady=10)

        # Book list
        self.book_listbox = tk.Listbox(self, width=70)
        self.book_listbox.pack(pady=5)

        # Load books from CSV
        self.books = self.load_books_from_csv("dataset/simple_book_data.csv")
        for book in self.books:
            display = f"ID {book['book_id']} - {book['title']} by {book['author']} ({book['category']})"
            self.book_listbox.insert(tk.END, display)

        # Action buttons
        tk.Button(self, text="Update Selected Book", command=self.update_book).pack(pady=5)
        tk.Button(self, text="Delete Selected Book", command=self.delete_book).pack(pady=5)

        self.pack()

    def load_books_from_csv(self, filename):
        books = []
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    books.append({
                        "book_id": row["Book ID"],
                        "title": row["Book Name"],
                        "author": row["Author"],
                        "category": row["Category"]
                    })
        except FileNotFoundError:
            messagebox.showerror("File Error", f"Could not find {filename}")
        return books

    def update_book(self):
        selected = self.book_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to update.")
            return
        book_info = self.book_listbox.get(selected[0])
        messagebox.showinfo("Update Book", f"Update logic for:\n{book_info}")
        # TODO: Add update form or logic here

    def delete_book(self):
        selected = self.book_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to delete.")
            return
        book_info = self.book_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete:\n{book_info}?")
        if confirm:
            self.book_listbox.delete(selected[0])
            messagebox.showinfo("Deleted", f"{book_info} has been deleted.")
            # TODO: Remove from CSV or database

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        MainPortal(self.base)

if __name__ == "__main__":
    root = tk.Tk()
    root.eval('tk::PlaceWindow . center')
    ManageBooksFrame(root)
    root.mainloop()
