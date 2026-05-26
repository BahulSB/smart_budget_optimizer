# Algorithmic "Smart-Budget" Expense Optimizer

This is a local backend project I built to connect a relational MySQL database directly to Python data analytics tools. It extracts daily transaction inputs, aggregates them into categories, and automatically flags sudden spike purchases using statistical metrics.

---

## 🛠️ How It Works

1. **Database Backend:** A two-table MySQL setup that links individual transactions to core category targets safely using a Foreign Key link. This prevents typos and keeps data clean.
2. **Data Aggregation:** The script runs an SQL `LEFT JOIN` query to pull records directly into a Pandas DataFrame to measure how much of your budget limit has been used.
3. **Anomaly Identification:** Instead of using fixed alarms, the program uses NumPy to find the average spending size and its standard deviation. It automatically flags any single purchase that sits drastically higher than your typical baseline.

---

## 🗄️ Database Table Setup

Both tables share the clean, unified `category` key:

```sql
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
==================================================
 FINANCIAL OPTIMIZER RUNTIME SHELL
==================================================

[1] CURRENT BUDGET OVERVIEW:
+---------------------------+-------------+-----------+----------+
| Category                  | Total Spent | Max Limit | % Used   |
+---------------------------+-------------+-----------+----------+
| Entertainment & Streaming | 7850.00     | 1500.00   | 523.33%  |
| Food & Canteen            | 2950.00     | 5000.00   | 59.00%   |
+---------------------------+-------------+-----------+----------+

 SYSTEM ALERTS:
 LIMIT BREACHED: 'Entertainment & Streaming' is over budget! (7850.00/1500.00)

 [2] CALCULATING TRANSACTION ANOMALIES...
 SPIKE DETECTED: Found spending anomalies above ₹3800.50:
+------------+-----------------------------+---------------------------+---------+
| Date       | Item                        | Category                  | Amount  |
+------------+-----------------------------+---------------------------+---------+
| 2026-05-20 | Noise Cancelling Headphones | Entertainment & Streaming | 7500.00 |
+------------+-----------------------------+---------------------------+---------+
==================================================
