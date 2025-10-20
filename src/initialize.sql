-- ================================
-- Library Catalog System Database
-- ================================

-- Table: Book
CREATE TABLE Book (
    ISBN13      INTEGER PRIMARY KEY,
    Title       TEXT NOT NULL,
    Published   DATE,
    Publisher   TEXT,
    Edition     TEXT,
    PageCount   INTEGER,
    Language    TEXT,
    Summary     TEXT
);

-- Table: Author
CREATE TABLE Author (
    ID          INTEGER PRIMARY KEY,
    AuthorName  TEXT NOT NULL
    -- Additional metadata can be added here
);

-- Table: BookAuthor (Many-to-Many Relationship)
CREATE TABLE BookAuthor (
    AuthorID    INTEGER NOT NULL,
    BookISBN13  INTEGER NOT NULL,
    PRIMARY KEY (AuthorID, BookISBN13),
    FOREIGN KEY (AuthorID)
        REFERENCES Author(ID)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (BookISBN13)
        REFERENCES Book(ISBN13)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    CONSTRAINT book_author_relationship_is_unique 
        UNIQUE (AuthorID, BookISBN13)
);

-- Table: Genre
CREATE TABLE Genre (
    ID      INTEGER PRIMARY KEY,
    Name    TEXT NOT NULL UNIQUE
);

-- Table: BookGenre (Many-to-Many Relationship)
CREATE TABLE BookGenre (
    BookISBN13  INTEGER NOT NULL,
    GenreID     INTEGER NOT NULL,
    PRIMARY KEY (BookISBN13, GenreID),
    FOREIGN KEY (BookISBN13)
        REFERENCES Book(ISBN13)
        ON DELETE CASCADE,
    FOREIGN KEY (GenreID)
        REFERENCES Genre(ID)
        ON DELETE CASCADE
);

-- Table: HoldRequest
CREATE TABLE HoldRequest (
    ID              INTEGER PRIMARY KEY AUTOINCREMENT,
    BookISBN13      INTEGER NOT NULL,
    RequesterName   TEXT NOT NULL,
    RequestDate     DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (BookISBN13)
        REFERENCES Book(ISBN13)
        ON DELETE CASCADE
);

-- Indexes for performance
CREATE INDEX idx_book_title ON Book(Title);
CREATE INDEX idx_author_name ON Author(AuthorName);
CREATE INDEX idx_hold_book ON HoldRequest(BookISBN13);
CREATE INDEX idx_genre_name ON Genre(Name);
