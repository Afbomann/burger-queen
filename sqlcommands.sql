-- Lage tabeller --
CREATE TABLE user (
	id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(20) NOT NULL UNIQUE,
	password VARCHAR(200) NOT NULL,
	employee INTEGER NOT NULL
);

CREATE TABLE burger (
	id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL UNIQUE,
	ingredients VARCHAR(100) NOT NULL
);

CREATE TABLE burgerOrder (
	id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	userID INTEGER NOT NULL,
	burgerID INTEGER NOT NULL,
	produced INTEGER NOT NULL,
	amount INTEGER NOT NULL,
	
	FOREIGN KEY(userID) REFERENCES user(id),
	FOREIGN KEY(burgerID) REFERENCES burger(id)
);

CREATE TABLE ingredient (
	id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(30) NOT NULL UNIQUE,
	amount INTEGER NOT NULL
);

-- Fylle inn dummy data --
INSERT INTO user (name, password, employee)
VALUES
("Geralt", "hesterbest", 0),
("Yennefer", "qwerty", 0),
("Roach", "pizza", 0),
("Jaskier", "nyttpassord", 1);

INSERT INTO burger (name, ingredients)
VALUES
("Whopper Queen", "Burgerbrød,Burgerkjøtt,Salat,Tomat"),
("Triple Cheesy Princess", "Burgerbrød,Burgerkjøtt,Ost,Salat,Tomat"),
("Kingdom Fries", "Potet");

INSERT INTO burgerOrder (userID, burgerID, produced, amount)
VALUES
(1, 1, 1, 2),
(1, 1, 0, 1),
(4, 2, 0, 1),
(3, 1, 0, 3);

INSERT INTO ingredient (name, amount)
VALUES
("Burgerbrød topp og bunn", 9001),
("Burgerkjøtt", 10),
("Salat", 8008),
("Tomat", 1337),
("Ost", 42),
("Agurk", 666),
("Potet", 420);