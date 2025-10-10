import sqlite3 as sq
import os
from os import path
import csv
from collections import namedtuple

def init():
    print("Time to init the database")
    connection = sq.connect("db")
    if not create_tables(connection):
        return
    if not load_data(connection):
        return
    validate_entries(connection)
    connection.close()

def create_tables(connection):
    cursor = connection.cursor()
    statements = load_statements()
    for s in statements:
        try:
            cursor.executescript(s)
        except sq.OperationalError as oe:
            print("OperationError\n", oe, "in:\n", s)
            return False

    # fetch table names to verify creation
    # cursor.execute("SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    # for row in cursor.fetchall():
    #     print("Got entry: ", row)
    cursor.close()
    return True

def load_statements():
    with open("src/initialize.sql", 'r', encoding="utf8") as file:
        statements = []
        current = ""
        for line in file.readlines():
            current += line
            if ';' in line:
                statements.append(current)
                current = ""
        return statements
    return []


def load_data(connection):
    Row = namedtuple('Row', ['id', 'title', 'author', 'category'])
    books = []
    authors = []
    categories = []
    relationships = []
    with open("dataset/simple_book_data.csv", 'r', encoding="utf8") as file:
        file.readline() # skips header line
        reader = csv.reader(file)
        cursor = connection.cursor()
        for [a, b, c, d] in reader:
            row = Row(a, b, c, d)
            book = [row.id, row.title]
            author = [row.author]
            category = [row.category]
            relationships.append(row)

            if book not in books:
                books.append(book)

            if author not in authors:
                authors.append(author)
            if category not in categories:
                categories.append(category)
 
    # Insert books
    cursor.executemany("""
        INSERT INTO Book 
            (ID, Title)
        VALUES
            (?, ?);
    """, books)
    # Insert authors
    cursor.executemany("""
        INSERT INTO Author 
            (Name)
        VALUES
            (?);
    """, authors)
    # Categories
    cursor.executemany("""
        INSERT INTO Category
            (Name)
        VALUES
            (?);
    """, categories)

    for r in relationships:
        book_id = cursor.execute("SELECT ID FROM Book WHERE Title=?;", [r.title]).fetchone()[0]
        author_id = cursor.execute("SELECT ID FROM Author WHERE Name=?;", [r.author]).fetchone()[0]
        category_id = cursor.execute("SELECT ID FROM Category WHERE Name=?;", [r.category]).fetchone()[0]

        cursor.execute("""
            INSERT INTO BookAuthor
                (AuthorID, BookID)
            VALUES
                (?, ?);
        """, [author_id, book_id])

        cursor.execute("""
            INSERT INTO BookIsCategory
                (BookID, CategoryID)
            VALUES
                (?, ?);
        """, [book_id, category_id])

    cursor.close()
    return True

def validate_entries(connection):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT Book.Title, Author.Name, Category.Name
        FROM BookAuthor
        INNER JOIN Book 
            ON BookAuthor.BookID = Book.ID
        INNER JOIN Author
            ON BookAuthor.AuthorID = Author.ID
        INNER JOIN BookIsCategory
            ON BookAuthor.BookID = BookIsCategory.BookID
        INNER JOIN Category
            ON BookIsCategory.CategoryID = Category.ID
        ;
    """)
    rows = list(cursor.fetchall())
    print("Found ", len(rows), " rows available for book data (this should match CSV size of 677entries)")
    for r in rows[:25:5]:
        print("Sample", r)
    return True

# allow running this scrip manually ro reinit the database in case of corruption
if __name__ == "__main__":
    if path.isfile("db"):
        os.remove("db")
    init()

