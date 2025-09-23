
-- An individual book
CREATE TABLE Book
(
	ISBN13		INTEGER PRIMARY KEY,
    Published   DATE,
    Title       TEXT NOT NULL
);

-- A single author
CREATE TABLE Author 
(
	ID			INTEGER PRIMARY KEY,
	AuthorName	TEXT NOT NULL
	-- Maybe any other author metadata?
);

-- The relationship between any one author and any one book
CREATE TABLE BookAuthor
(
	AuthorID	INTEGER NOT NULL,
	BookISBN13	INTEGER NOT NULL,
	PRIMARY KEY (AuthorID, BookISBN13)
	FOREIGN KEY (AuthorID)
		REFERENCES Author (ID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
	FOREIGN KEY (BookISBN13)
		REFERENCES Book (ISBN13)
		ON UPDATE CASCADE
		ON DELETE CASCADE
	CONSTRAINT book_author_relationship_is_unique 
		UNIQUE (AuthorID, BookISBN13)
);

