import mysql.connector
import pandas as pd
import numpy as np
from tabulate import tabulate
def get_database_connection():
    """Establishes a connection to your local MySQL database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="BAHULSB",
        port="3307",
        database="smart_budget_db"
    )
def analyze_expenses():
    conn = get_database_connection()
    query = """
    SELECT e.purchase_date, e.item, e.categoryname, e.amount AS amount_spent,
           b.maxlimit, b.warning
    FROM Expenses e
    LEFT JOIN Budgets b ON e.categoryname = b.categoryname;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    if df.empty:
        print("No expense data found to analyze.")
        return
    df['amount_spent'] = pd.to_numeric(df['amount_spent'])
    df['maxlimit'] = pd.to_numeric(df['maxlimit'])
    print("\n" + "="*60)
    print(" ALGORITHMIC BUDGET RUNTIME REPORT")
    print("="*60)
    summary = df.groupby('categoryname').agg(
        Total_Spent=('amount_spent', 'sum'),
        Budget_Limit=('maxlimit', 'first'),
        Warning_Threshold=('warning', 'first')
    ).reset_index()
    summary['Percentage_Used'] = (summary['Total_Spent'] / summary['Budget_Limit']) * 100 
    print("\n[1] CATEGORY BUDGET STATUS:")
    print(tabulate(summary[['categoryname', 'Total_Spent', 'Budget_Limit', 'Percentage_Used']], 
                   headers=['Category', 'Total Spent', 'Limit', '% Used'], 
                   tablefmt='psql', floatfmt=".2f", showindex=False))
    print("\n SYSTEM ALERTS:")
    has_alerts = False
    for _, row in summary.iterrows():
        threshold_limit = row['Budget_Limit'] * row['Warning_Threshold']
        if row['Total_Spent'] >= row['Budget_Limit']:
            print(f" CRITICAL OVER-BUDGET: '{row['categoryname']}' has exceeded its limit! (Spent {row['Total_Spent']:.2f}/{row['Budget_Limit']:.2f})")
            has_alerts = True
        elif row['Total_Spent'] >= threshold_limit:
            print(f" WARNING: '{row['categoryname']}' has breached its {int(row['Warning_Threshold']*100)}% alert threshold.")
            has_alerts = True
    if not has_alerts:
        print(" All categories are currently operating within safe financial limits.")
    mean_spend = np.mean(df['amount_spent'])
    std_spend = np.std(df['amount_spent'])
    anomaly_cutoff = mean_spend + (2 * std_spend)
    anomalies = df[df['amount_spent'] > anomaly_cutoff]
    if not anomalies.empty:
        print(f"️ DETECTED {len(anomalies)} UNUSUAL SPENDING ANOMALIES (Transactions > {anomaly_cutoff:.2f}):")
        print(tabulate(anomalies[['purchase_date', 'item', 'categoryname', 'amount_spent']], 
                       headers=['Date', 'Item Description', 'Category', 'Amount'], 
                       tablefmt='psql', floatfmt=".2f", showindex=False))
        print("\n Recommendation: Review these isolated spike purchases to stabilize your monthly averages.")
    else:
        print(" No statistical transaction anomalies detected in this billing cycle.")
    print("="*60 + "\n")
if __name__ == "__main__":
    analyze_expenses()
