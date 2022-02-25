CREATE DATABASE IF NOT EXISTS phone_book;
USE phone_book;

CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username CHAR(50) NOT NULL,
    sha256_password CHAR(64) NOT NULL
);

CREATE TABLE Contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name CHAR(50) NOT NULL,
    phone CHAR(12) NOT NULL,
    birthday DATE NOT NULL,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES Users (id)
);

INSERT INTO Users (username, sha256_password) values ('admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918');

INSERT INTO Contacts (name, phone, birthday, owner_id) values
('Артём', '89119197174', NOW(), 1),
('Антон', '89119197174', NOW(), 1);
