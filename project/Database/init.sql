CREATE DATABASE IF NOT EXISTS my_test_db;
USE my_test_db;

CREATE TABLE Users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username CHAR(50) NOT NULL,
    password CHAR(50) NOT NULL
);

CREATE TABLE Contacts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name CHAR(50) NOT NULL,
    phone CHAR(12) NOT NULL,
    birthday DATE NOT NULL,
    owner_id INT,
    FOREIGN KEY (owner_id) REFERENCES Users (id)
);

INSERT INTO Users (username, password) values ('admin', 'admin');
