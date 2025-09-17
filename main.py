import sqlite3
from tkinter import *


class App:
    """
        The core functionality of the application
    
    """

    def __init__(self):
        self.db = self.init_db()

        self.root = Tk()

        self.title_entry= StringVar()
        self.published_entry= StringVar()
        self.author_entry= StringVar()

        self.root.geometry('800x600')
        self.root.title("Library Database Application")
        Label(self.root, text="Hello, world!~").grid(row=0)

        Label(self.root, text="Title").grid(row=1, column=1)
        Entry(self.root, textvariable=self.title_entry).grid(row=1, column=2)

        Label(self.root, text="Published").grid(row=2, column=1)
        Entry(self.root, textvariable=self.published_entry).grid(row=2, column=2)

        Label(self.root, text="Author").grid(row=3, column=1)
        Entry(self.root, textvariable=self.author_entry).grid(row=3, column=2)

        Button(self.root, text="Add Book", command=self.add_object).grid(row=4)

    def add_object(self):
        """
        Inserts a new book into the DB
        """
        title = self.title_entry.get()
        published = self.published_entry.get()
        author = self.author_entry.get()

        print("added book (not really)")
        cmd = f"INSERT INTO Books (Title, Published, Author) VALUES (\"{title}\", '{published}', \"{author}\");"
        print("Attempting command: ", cmd)
        self.db.execute(cmd)
        books = self.db.execute("SELECT * FROM Books;").fetchall()
        print(books)
        self.db.commit()

    def init_db(self):
        """
            Sets up the database
        """
        conn = sqlite3.connect("./db")
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print(tables)
        if not tables:
            conn.execute('''
            CREATE TABLE Books
            (
                Title       VARCHAR(64) NOT NULL,
                Published   DATE,
                Author      VARCHAR(64) NOT NULL
            );
            ''')
            #  Using January 1st for date published for books that only have the publishing year listed
            conn.execute('''
                INSERT INTO Books (Title, Published, Author)
                VALUES
                ("Pride and Prejudice", '1813-01-01', "Jane Austen"),
                ("To Kill a Mockingbird", '1960-01-01', "Harper Lee"),
                ("The Great Gatsby", '1925-01-01', "F. Scott Fitzgerald"),
                ("One Hundred Years of Solitude", '1967-01-01', "Gabriel Garcia Marquez"),
                ("In Cold Blood", '1966-01-01', "Truman Capote"),
                ("Wide Sargasso Sea", '1966-01-01', "Jean Rhys");
            ''')
            conn.commit()
        books = conn.execute("SELECT * FROM Books;").fetchall()
        print(books)
        return conn

    def mainloop(self):
        """
            Runs the application mainloop
        """
        self.root.mainloop()

app = App()
app.mainloop()
