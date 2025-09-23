from tkinter import *
from initialize import initialize_database
import database
import os
from os import path

class App:
    """
        The core functionality of the application
    
    """

    def __init__(self):
        self.db = database.DbHandle()
        initialize_database(self.db)
        print("Found tables: ", self.db.tables)
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

        # cmd = f"INSERT INTO Books (Title, Published, Author) VALUES (\"{title}\", '{published}', \"{author}\");"
        # print("Attempting command: ", cmd)
        # self.db.execute(cmd)
        # self.db.commit()

    def mainloop(self):
        """
            Runs the application mainloop
        """
        self.root.mainloop()


if __name__ == "__main__":
    if path.isfile("db"):
        print("WARNING! DELETING DATABASE FOR TESTING PURPOSES REMOVE THIS CODE ONCE TESTING COMPLETED")
        os.remove("db")
    app = App()
    app.mainloop()
