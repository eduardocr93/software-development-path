-- =========================================
-- RESULTADOS EJERCICIO TEORÍA DE CONJUNTOS
-- =========================================
-- Even U Odd = {1,2,3,4,5,6,7,8,9,10}
-- Even ∩ Odd = {}
-- All - Odd = {2,4,6,8,10}
-- C(Even) = {1,3,5,7,9}
-- C(Odd - All) = {1,2,3,4,5,6,7,8,9,10}
-- =========================================

CREATE TABLE Authors (
    ID INT PRIMARY KEY,
    Name VARCHAR(100)
);

CREATE TABLE Books (
    ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Author INT,
    FOREIGN KEY (Author) REFERENCES Authors(ID)
);

CREATE TABLE Customers (
    ID INT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100)
);

CREATE TABLE Rents (
    ID INT PRIMARY KEY,
    BookID INT,
    CustomerID INT,
    State VARCHAR(50),
    FOREIGN KEY (BookID) REFERENCES Books(ID),
    FOREIGN KEY (CustomerID) REFERENCES Customers(ID)
);


INSERT INTO Authors VALUES
(1,'Miguel de Cervantes'),
(2,'Dante Alighieri'),
(3,'Takehiko Inoue'),
(4,'Akira Toriyama'),
(5,'Walt Disney');

INSERT INTO Books VALUES
(1,'Don Quijote',1),
(2,'La Divina Comedia',2),
(3,'Vagabond 1-3',3),
(4,'Dragon Ball 1',4),
(5,'The Book of the 5 Rings',NULL);

INSERT INTO Customers VALUES
(1,'John Doe','j.doe@email.com'),
(2,'Jane Doe','jane@doe.com'),
(3,'Luke Skywalker','darth.son@email.com');

INSERT INTO Rents VALUES
(1,1,2,'Returned'),
(2,2,2,'Returned'),
(3,1,1,'On time'),
(4,3,1,'On time'),
(5,2,2,'Overdue');

SELECT Books.Name, Authors.Name
FROM Books
INNER JOIN Authors ON Books.Author = Authors.ID;

SELECT *
FROM Books
WHERE Author IS NULL;

SELECT Authors.*
FROM Authors
LEFT JOIN Books ON Authors.ID = Books.Author
WHERE Books.ID IS NULL;

SELECT DISTINCT Books.Name
FROM Books
INNER JOIN Rents ON Books.ID = Rents.BookID;

SELECT Books.Name
FROM Books
LEFT JOIN Rents ON Books.ID = Rents.BookID
WHERE Rents.ID IS NULL;

SELECT Customers.Name
FROM Customers
LEFT JOIN Rents ON Customers.ID = Rents.CustomerID
WHERE Rents.ID IS NULL;

SELECT Books.Name
FROM Books
INNER JOIN Rents ON Books.ID = Rents.BookID
WHERE Rents.State = 'Overdue';