"""
03_eda_visualizations.py
Exploratory Data Analysis + business visualizations.
Saves PNG charts into visuals/.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.dpi"] = 120

DATA = "/home/claude/customer-segmentation-project/data/online_retail_transactions.csv"
OUT = "/home/claude/customer-segmentation-project/visuals"

df = pd.read_csv(DATA, parse_dates=["InvoiceDate"])

# ---------------------------------------------------------------
# 1. Monthly revenue trend
# ---------------------------------------------------------------
monthly = df.groupby(df["InvoiceDate"].dt.to_period("M"))["TotalPrice"].sum()
plt.figure(figsize=(10, 5))
monthly.plot(kind="line", marker="o", color="#3B5BDB")
plt.title("Monthly Revenue Trend", fontsize=14, weight="bold")
plt.ylabel("Revenue")
plt.xlabel("Month")
plt.tight_layout()
plt.savefig(f"{OUT}/01_monthly_revenue_trend.png")
plt.close()

# ---------------------------------------------------------------
# 2. Revenue by category
# ---------------------------------------------------------------
cat_rev = df.groupby("Category")["TotalPrice"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
sns.barplot(x=cat_rev.values, y=cat_rev.index, hue=cat_rev.index, legend=False, palette="mako")
plt.title("Revenue by Product Category", fontsize=14, weight="bold")
plt.xlabel("Revenue")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT}/02_revenue_by_category.png")
plt.close()

# ---------------------------------------------------------------
# 3. Top 10 products by revenue
# ---------------------------------------------------------------
top_products = df.groupby("ProductName")["TotalPrice"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9, 5))
sns.barplot(x=top_products.values, y=top_products.index, hue=top_products.index, legend=False, palette="crest")
plt.title("Top 10 Products by Revenue", fontsize=14, weight="bold")
plt.xlabel("Revenue")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT}/03_top10_products.png")
plt.close()

# ---------------------------------------------------------------
# 4. Revenue by country
# ---------------------------------------------------------------
country_rev = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
sns.barplot(x=country_rev.values, y=country_rev.index, hue=country_rev.index, legend=False, palette="flare")
plt.title("Revenue by Country", fontsize=14, weight="bold")
plt.xlabel("Revenue")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT}/04_revenue_by_country.png")
plt.close()

# ---------------------------------------------------------------
# 5. Order value distribution
# ---------------------------------------------------------------
order_value = df.groupby("InvoiceNo")["TotalPrice"].sum()
plt.figure(figsize=(9, 5))
sns.histplot(order_value, bins=40, kde=True, color="#5C7CFA")
plt.title("Distribution of Order Values", fontsize=14, weight="bold")
plt.xlabel("Order Value")
plt.tight_layout()
plt.savefig(f"{OUT}/05_order_value_distribution.png")
plt.close()

print("Saved 5 EDA charts to visuals/")
print("\n--- Quick stats ---")
print(f"Total revenue: {df['TotalPrice'].sum():,.2f}")
print(f"Total orders: {df['InvoiceNo'].nunique():,}")
print(f"Total customers: {df['CustomerID'].nunique():,}")
print(f"Avg order value: {order_value.mean():,.2f}")
