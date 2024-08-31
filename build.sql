CREATE DATABASE papadb;
CREATE USER 'api'@'localhost' IDENTIFIED BY 'pass';
USE papadb;
CREATE TABLE Cards (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    email VARCHAR(100) NOT NULL,
    url VARCHAR(255)
);
GRANT ALL PRIVILEGES ON papadb.* TO 'api'@'localhost';
FLUSH PRIVILEGES;
