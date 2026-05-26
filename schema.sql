CREATE DATABASE IF NOT EXISTS budget_db;
USE budget_db;

CREATE TABLE Budgets (
    category VARCHAR(50) PRIMARY KEY,
    maxlimit DECIMAL(10,2) NOT NULL,
    warning DECIMAL(3,2) DEFAULT 0.80
);

CREATE TABLE Expenses (
    trans_id INT AUTO_INCREMENT PRIMARY KEY,
    purchase_date DATE NOT NULL,
    item VARCHAR(50),
    category VARCHAR(50),
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    FOREIGN KEY (category) REFERENCES Budgets(category)
);