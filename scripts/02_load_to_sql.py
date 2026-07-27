"""
02_load_to_sql.py
Loads the generated CSV data into a SQLite database (data/retail.db)
so that all SQL analysis in sql/business_insights.sql can be run directly.
"""

import sqlite3
import pandas as pd

DB_PATH = "/home/claude/customer-segmentation-project/data/retail.db"

txn = pd.read_csv("/home/claude/customer-segmentation-project/data/online_retail_transactions.csv",
                   parse_dates=["InvoiceDate"])
customers = pd.read_csv("/home/claude/customer-segmentation-project/data/customers_master.csv")
products = pd.read_csv("/home/claude/customer-segmentation-project/data/products_master.csv")

conn = sqlite3.connect(DB_PATH)
txn.to_sql("transactions", conn, if_exists="replace", index=False)
customers.to_sql("customers", conn, if_exists="replace", index=False)
products.to_sql("products", conn, if_exists="replace", index=False)

conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_customer ON transactions(CustomerID)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_product ON transactions(ProductID)")
conn.execute("CREATE INDEX IF NOT EXISTS idx_txn_date ON transactions(InvoiceDate)")
conn.commit()
conn.close()

print(f"Loaded tables 'transactions', 'customers', 'products' into {DB_PATH}")
