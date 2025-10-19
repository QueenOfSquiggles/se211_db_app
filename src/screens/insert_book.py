import tkinter as tk
from .util import resize_window
from .main_portal import MainPortal
from tkinter import messagebox


class InsertBookFrame(tk.Frame):
    def __init__(self, base):
        super().__init__()
        self.base = base
        self.base.title("Insert Books")
        resize_window(base)
        tk.Button(self, text="Home", command=self.return_home).pack()
        # add elements here

        tk.Label(self, text="Insert Books Screen").pack()

        # Form fields
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Title:").grid(
            row=0, column=0, sticky="e", padx=5, pady=3
        )
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, pady=3)

        tk.Label(form_frame, text="Author:").grid(
            row=1, column=0, sticky="e", padx=5, pady=3
        )
        self.author_entry = tk.Entry(form_frame, width=40)
        self.author_entry.grid(row=1, column=1, pady=3)

        tk.Label(form_frame, text="Genre:").grid(
            row=2, column=0, sticky="e", padx=5, pady=3
        )
        self.genre_entry = tk.Entry(form_frame, width=40)
        self.genre_entry.grid(row=2, column=1, pady=3)

        tk.Label(form_frame, text="ISBN:").grid(
            row=3, column=0, sticky="e", padx=5, pady=3
        )
        self.isbn_entry = tk.Entry(form_frame, width=40)
        self.isbn_entry.grid(row=3, column=1, pady=3)

        tk.Label(form_frame, text="Year:").grid(
            row=4, column=0, sticky="e", padx=5, pady=3
        )
        self.year_entry = tk.Entry(form_frame, width=40)
        self.year_entry.grid(row=4, column=1, pady=3)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Save",
            command=self.save_book,
            width=10,
            bg="#4CAF50",
            fg="white",
        ).grid(row=0, column=0, padx=10)
        tk.Button(
            btn_frame,
            text="Home",
            command=self.return_home,
            width=10,
            bg="#f44336",
            fg="white",
        ).grid(row=0, column=1, padx=10)

        # end elements section

        self.pack()

    def save_book(self):
        """Handles saving the new book (placeholder for DB or file operation)."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        isbn = self.isbn_entry.get().strip()
        year = self.year_entry.get().strip()

        # Basic validation
        if not title or not author or not genre or not isbn or not year:
            messagebox.showerror("Error", "Please fill in all fields before saving.")
            return

        messagebox.showinfo("Success", f"Book '{title}' added successfully!")

        # Clear entries
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.isbn_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def return_home(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.destroy()
        MainPortal(self.base)


if __name__ == "__main__":
    root = tk.Tk()
    root.eval("tk::PlaceWindow . center")
    InsertBookFrame(root)
    root.mainloop()
