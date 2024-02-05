-- init_db.mysql
CREATE DATABASE IF NOT EXISTS vetchat;
USE vetchat;

CREATE TABLE IF NOT EXISTS example_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

INSERT INTO items (name, description) VALUES ('Item1', 'Description for Item1');
INSERT INTO items (name, description) VALUES ('Item2', 'Description for Item2');