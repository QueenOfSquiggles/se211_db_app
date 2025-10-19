
-- An individual book
CREATE TABLE Book
(
	ID		VARCHAR(30) PRIMARY KEY,
	Title	TEXT NOT NULL
);

-- A single author
CREATE TABLE Author 
(
	ID			INTEGER PRIMARY KEY AUTOINCREMENT,
	Name		TEXT NOT NULL
);

-- The relationship between any one author and any one book
CREATE TABLE BookAuthor
(
	AuthorID	INTEGER NOT NULL,
	BookID		TEXT NOT NULL,
	PRIMARY KEY (AuthorID, BookID)
	FOREIGN KEY (AuthorID)
		REFERENCES Author (ID)
		ON UPDATE CASCADE
		ON DELETE CASCADE
	FOREIGN KEY (BookID)
		REFERENCES Book (ID)
		ON UPDATE CASCADE -- updates not really planned but whatever
		ON DELETE CASCADE 
);

-- A specific category
CREATE TABLE Category (
	ID		INTEGER PRIMARY KEY AUTOINCREMENT,
	Name	TEXT NOT NULL
);

-- A relationship of a book belonging to a particular category
CREATE TABLE BookIsCategory (
	BookID		TEXT NOT NULL,
	CategoryID	INT NOT NULL,
	PRIMARY KEY (BookID, CategoryID)
	FOREIGN KEY (BookID)
		REFERENCES Book (ID)
		ON UPDATE CASCADE -- updates not really planned but whatever
		ON DELETE CASCADE 
	FOREIGN KEY (CategoryID)
		REFERENCES Category (ID)
		ON UPDATE CASCADE -- updates not really planned but whatever
		ON DELETE CASCADE 
);

CREATE TABLE Patron (
	ID 		INTEGER PRIMARY KEY AUTOINCREMENT,
	Name	TEXT NOT NULL
);

CREATE TABLE Hold (
	BookID		TEXT NOT NULL,
	PatronID	INTEGER NOT NULL,
	DateCreated	Date NOT NULL,
	DateExpires	Date NOT NULL,
	PRIMARY KEY (BookID, PatronID)
);