import csv
from datetime import datetime

def initialize_database(db):
    """
    Loads database structure from the `initialize.sql` script and inserts the dataset from GoodReads    
    """
    if not db.tables:
        db.execute_script("src/initialize.sql")
        insert_dataset(db)

def insert_dataset(db):
    """
        Pulls the data from the dataset CSV and pushes relevant data into our database
    """
    with open("dataset/books.csv","r", encoding="utf-8") as file:
        # CSV file in format of:
        # 0 bookID, 1 title, 2 authors, 3 average_rating, 4 isbn, 5 isbn13, 6 language_code, 
        # 7 num_pages, 8 ratings_count, 9 text_reviews_count, 10 publication_date, 11 publisher

        # Book table is (5, 10, 1)
        # Author table is (2)
        # BookAuthor is relationship (AuthorID, 5)

        csv_file = list(csv.reader(file))
        
        # skip first row to omit header row
        print("Loading database contents from CSV. ")
        books = list(map(extract_book_data, csv_file[1:]))
        authors = list(map(extract_book_data, csv_file[1:]))
        db.db.executemany("INSERT INTO Book (ISBN13, Published, Title) VALUES (?, ?, ?);", books)
        db.db.executemany("INSERT INTO Author (AuthorName) VALUES (?)", authors)

def extract_book_data(csv_line):
    # TODO: parse the datetime manually since the days/months aren't zero padded
    return (int(csv_line[5]), datetime.strptime(csv_line[10], "%d/%m/%Y"), csv_line[1])

def extract_author_data(csv_line):
    return (csv_line[2])