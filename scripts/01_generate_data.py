"""
01_generate_data.py
Generates a realistic synthetic e-commerce transactions dataset for the
Customer Segmentation & Business Insights project.

Output: data/online_retail_transactions.csv
Columns:
    InvoiceNo, InvoiceDate, CustomerID, CustomerName, Country,
    ProductID, ProductName, Category, Quantity, UnitPrice, TotalPrice
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ---------------------------------------------------------------------------
# 1. Reference data: customers, products, countries
# ---------------------------------------------------------------------------
N_CUSTOMERS = 800
N_PRODUCTS = 120
N_TRANSACTIONS = 25000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

countries = ["India", "United Kingdom", "United States", "Germany", "France",
             "Australia", "Canada", "UAE", "Singapore", "Netherlands"]
country_weights = [0.30, 0.18, 0.15, 0.08, 0.07, 0.06, 0.06, 0.04, 0.03, 0.03]

first_names = ["Aarav","Vivaan","Aditya","Isha","Riya","Ananya","James","Emma",
               "Liam","Olivia","Noah","Sophia","Ethan","Ava","Mason","Mia",
               "Rohan","Priya","Kabir","Diya","William","Charlotte","Lucas",
               "Amelia","Henry","Harper","Arjun","Sara","Karan","Meera"]
last_names = ["Sharma","Verma","Khan","Patel","Gupta","Smith","Johnson","Brown",
              "Williams","Jones","Garcia","Muller","Dubois","Rossi","Kumar",
              "Singh","Reddy","Nair","Iyer","Chopra","Malhotra","Fischer"]

customers = pd.DataFrame({
    "CustomerID": [f"C{str(i).zfill(4)}" for i in range(1, N_CUSTOMERS + 1)],
    "CustomerName": [f"{random.choice(first_names)} {random.choice(last_names)}"
                      for _ in range(N_CUSTOMERS)],
    "Country": np.random.choice(countries, size=N_CUSTOMERS, p=country_weights),
    "SignupDate": [START_DATE + timedelta(days=random.randint(0, 500))
                   for _ in range(N_CUSTOMERS)],
})

categories = {
    "Electronics": ["Wireless Earbuds", "Bluetooth Speaker", "Smart Watch",
                    "Power Bank", "USB-C Cable", "Laptop Stand", "Webcam",
                    "Mechanical Keyboard", "Wireless Mouse", "Phone Case"],
    "Home & Kitchen": ["Non-stick Pan", "Ceramic Mug Set", "LED Desk Lamp",
                       "Storage Boxes", "Cushion Cover Set", "Air Fryer",
                       "Electric Kettle", "Knife Set", "Wall Clock", "Bedsheet Set"],
    "Fashion": ["Cotton T-Shirt", "Denim Jacket", "Running Shoes", "Leather Wallet",
               "Sunglasses", "Formal Shirt", "Backpack", "Sports Cap",
               "Analog Watch", "Winter Hoodie"],
    "Beauty & Personal Care": ["Face Wash", "Moisturizer", "Shampoo", "Perfume",
                               "Lipstick", "Sunscreen", "Hair Dryer", "Trimmer",
                               "Face Mask Pack", "Body Lotion"],
    "Books & Stationery": ["Notebook Set", "Fiction Novel", "Sketch Pens",
                           "Desk Organizer", "Planner Diary", "Sticky Notes",
                           "Fountain Pen", "Bookmark Set", "Art Supplies Kit",
                           "Puzzle Book"],
    "Sports & Fitness": ["Yoga Mat", "Dumbbell Set", "Resistance Bands",
                         "Water Bottle", "Skipping Rope", "Cycling Gloves",
                         "Gym Bag", "Foam Roller", "Fitness Tracker", "Football"],
}

product_rows = []
pid = 1
for cat, items in categories.items():
    for item in items:
        for variant in range(2):  # 2 price variants per item -> 120 products
            base_price = {
                "Electronics": (800, 6000),
                "Home & Kitchen": (300, 3500),
                "Fashion": (400, 3000),
                "Beauty & Personal Care": (150, 1500),
                "Books & Stationery": (80, 800),
                "Sports & Fitness": (200, 2500),
            }[cat]
            price = round(random.uniform(*base_price), 2)
            product_rows.append({
                "ProductID": f"P{str(pid).zfill(4)}",
                "ProductName": item if variant == 0 else f"{item} Pro",
                "Category": cat,
                "UnitPrice": price
            })
            pid += 1

products = pd.DataFrame(product_rows).head(N_PRODUCTS)

# ---------------------------------------------------------------------------
# 2. Simulate customer purchase behavior (with realistic skew for RFM/segmentation)
# ---------------------------------------------------------------------------
# Assign each customer a "loyalty tier" which drives purchase frequency & spend
tiers = np.random.choice(
    ["champion", "loyal", "potential", "at_risk", "new", "lost"],
    size=N_CUSTOMERS,
    p=[0.08, 0.17, 0.20, 0.15, 0.20, 0.20]
)
customers["Tier"] = tiers

tier_txn_range = {
    "champion": (25, 45), "loyal": (15, 25), "potential": (8, 15),
    "at_risk": (4, 8), "new": (1, 4), "lost": (1, 3)
}
tier_recency_bias = {  # higher = more recent purchases
    "champion": 0.9, "loyal": 0.75, "potential": 0.6,
    "at_risk": 0.25, "new": 0.85, "lost": 0.05
}
tier_spend_mult = {
    "champion": 1.6, "loyal": 1.3, "potential": 1.0,
    "at_risk": 0.9, "new": 0.8, "lost": 0.7
}

date_range_days = (END_DATE - START_DATE).days

transactions = []
invoice_counter = 1000

for _, cust in customers.iterrows():
    tier = cust["Tier"]
    n_txn = random.randint(*tier_txn_range[tier])
    recency_bias = tier_recency_bias[tier]

    for _ in range(n_txn):
        # skew transaction dates towards "recent" for high recency_bias tiers
        if random.random() < recency_bias:
            day_offset = int(np.random.triangular(date_range_days * 0.6, date_range_days, date_range_days))
        else:
            day_offset = int(np.random.triangular(0, date_range_days * 0.3, date_range_days))
        day_offset = min(max(day_offset, 0), date_range_days)
        txn_date = START_DATE + timedelta(days=day_offset)

        n_items = random.randint(1, 5)
        invoice_no = f"INV{invoice_counter}"
        invoice_counter += 1

        # 65% of baskets stay within one category (realistic co-purchase
        # behavior), 35% are fully random cross-category baskets.
        if random.random() < 0.65:
            cat_choice = random.choice(list(categories.keys()))
            cat_pool = products[products["Category"] == cat_choice]
            n_pick = min(n_items, len(cat_pool))
            chosen_products = cat_pool.sample(n=n_pick, replace=False)
        else:
            chosen_products = products.sample(n=n_items, replace=False)
        for _, prod in chosen_products.iterrows():
            qty = random.randint(1, 6)
            price = round(prod["UnitPrice"] * tier_spend_mult[tier] * random.uniform(0.95, 1.05), 2)
            transactions.append({
                "InvoiceNo": invoice_no,
                "InvoiceDate": txn_date.strftime("%Y-%m-%d"),
                "CustomerID": cust["CustomerID"],
                "CustomerName": cust["CustomerName"],
                "Country": cust["Country"],
                "ProductID": prod["ProductID"],
                "ProductName": prod["ProductName"],
                "Category": prod["Category"],
                "Quantity": qty,
                "UnitPrice": price,
                "TotalPrice": round(qty * price, 2),
            })

df = pd.DataFrame(transactions)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)  # shuffle rows

# Trim/pad to roughly N_TRANSACTIONS worth of line items if needed
print(f"Generated {len(df):,} order line items across {df['InvoiceNo'].nunique():,} invoices "
      f"and {df['CustomerID'].nunique():,} customers.")

df.to_csv("/home/claude/customer-segmentation-project/data/online_retail_transactions.csv", index=False)
customers.to_csv("/home/claude/customer-segmentation-project/data/customers_master.csv", index=False)
products.to_csv("/home/claude/customer-segmentation-project/data/products_master.csv", index=False)

print("Saved: data/online_retail_transactions.csv")
print("Saved: data/customers_master.csv")
print("Saved: data/products_master.csv")
