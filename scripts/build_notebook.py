"""
Builds notebooks/Customer_Segmentation_Analysis.ipynb — a single consolidated,
presentable notebook combining EDA, RFM segmentation, and recommendations.
This is generated (not hand-authored) so the underlying .py scripts stay the
source of truth; re-run this any time the scripts change.
"""
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

cells.append(nbf.v4.new_markdown_cell("""\
# Customer Segmentation & Business Insights

**Skills demonstrated:** SQL · Python · Data Visualization · Business Analysis · Recommendation Systems

This notebook walks through an end-to-end customer analytics pipeline on a
simulated online-retail dataset (800 customers, ~8,400 orders, 25k line items,
across 6 product categories and 10 countries):

1. Data overview & business KPIs (SQL + Pandas)
2. Exploratory Data Analysis & visualizations
3. RFM (Recency, Frequency, Monetary) feature engineering
4. K-Means customer segmentation
5. Segment profiling & business recommendations
6. Product recommendation system (collaborative filtering + market basket analysis)
"""))

cells.append(nbf.v4.new_code_cell("""\
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 110
pd.set_option("display.float_format", lambda x: f"{x:,.2f}")

df = pd.read_csv("../data/online_retail_transactions.csv", parse_dates=["InvoiceDate"])
df.head()"""))

cells.append(nbf.v4.new_markdown_cell("## 1. Business KPI Overview (via SQL)"))

cells.append(nbf.v4.new_code_cell("""\
conn = sqlite3.connect("../data/retail.db")

kpi = pd.read_sql('''
    SELECT
        COUNT(DISTINCT InvoiceNo)  AS total_orders,
        COUNT(DISTINCT CustomerID) AS total_customers,
        COUNT(DISTINCT ProductID)  AS total_products_sold,
        ROUND(SUM(TotalPrice), 2)  AS total_revenue,
        ROUND(AVG(TotalPrice), 2)  AS avg_line_item_value
    FROM transactions
''', conn)
kpi"""))

cells.append(nbf.v4.new_code_cell("""\
monthly = pd.read_sql('''
    SELECT strftime('%Y-%m', InvoiceDate) AS year_month,
           ROUND(SUM(TotalPrice), 2) AS revenue
    FROM transactions GROUP BY year_month ORDER BY year_month
''', conn)

plt.figure(figsize=(10,5))
plt.plot(monthly["year_month"], monthly["revenue"], marker="o", color="#3B5BDB")
plt.xticks(rotation=60)
plt.title("Monthly Revenue Trend", fontsize=14, weight="bold")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("## 2. Exploratory Data Analysis"))

cells.append(nbf.v4.new_code_cell("""\
cat_rev = df.groupby("Category")["TotalPrice"].sum().sort_values(ascending=False)
plt.figure(figsize=(9,5))
sns.barplot(x=cat_rev.values, y=cat_rev.index, hue=cat_rev.index, legend=False, palette="mako")
plt.title("Revenue by Product Category", fontsize=14, weight="bold")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_code_cell("""\
top_products = df.groupby("ProductName")["TotalPrice"].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(9,5))
sns.barplot(x=top_products.values, y=top_products.index, hue=top_products.index, legend=False, palette="crest")
plt.title("Top 10 Products by Revenue", fontsize=14, weight="bold")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("## 3. RFM Feature Engineering"))

cells.append(nbf.v4.new_code_cell("""\
ref_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (ref_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalPrice", "sum")
).reset_index()
rfm.describe()"""))

cells.append(nbf.v4.new_markdown_cell("## 4. K-Means Customer Segmentation"))

cells.append(nbf.v4.new_code_cell("""\
scaler = StandardScaler()
scaled = scaler.fit_transform(rfm[["Recency","Frequency","Monetary"]])

inertias = []
for k in range(2, 10):
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(8,5))
plt.plot(range(2,10), inertias, marker="o", color="#3B5BDB")
plt.title("Elbow Method for Optimal K", fontsize=14, weight="bold")
plt.xlabel("K"); plt.ylabel("Inertia")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_code_cell("""\
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm["Cluster"] = kmeans.fit_predict(scaled)

cluster_summary = rfm.groupby("Cluster")[["Recency","Frequency","Monetary"]].mean()
cluster_summary["RFM_Score"] = (cluster_summary["Monetary"].rank()
                                 + cluster_summary["Frequency"].rank()
                                 - cluster_summary["Recency"].rank())
ranked = cluster_summary.sort_values("RFM_Score", ascending=False).index.tolist()
names = ["Champions","Loyal Customers","Potential / At-Risk","Lost / Low-Value"]
label_map = {c: names[i] for i, c in enumerate(ranked)}
rfm["Segment"] = rfm["Cluster"].map(label_map)
cluster_summary"""))

cells.append(nbf.v4.new_code_cell("""\
plt.figure(figsize=(9,6))
sns.scatterplot(data=rfm, x="Frequency", y="Monetary", hue="Segment", palette="Set2", s=60, alpha=0.8)
plt.title("Customer Segments — Frequency vs Monetary", fontsize=14, weight="bold")
plt.legend(bbox_to_anchor=(1.02,1), loc="upper left")
plt.tight_layout()
plt.show()"""))

cells.append(nbf.v4.new_markdown_cell("""\
## 5. Segment Profiles & Business Recommendations

| Segment | Typical Profile | Suggested Business Action |
|---|---|---|
| **Champions** | Very recent, frequent, high spend | Reward with loyalty perks, early access, referral programs |
| **Loyal Customers** | Regular buyers, solid spend | Upsell/cross-sell bundles, personalized offers |
| **Potential / At-Risk** | Moderate recency & frequency | Win-back campaigns, targeted discounts, re-engagement emails |
| **Lost / Low-Value** | Long inactive, low spend | Low-cost reactivation campaigns or deprioritize marketing spend |
"""))

cells.append(nbf.v4.new_markdown_cell("## 6. Recommendation System"))

cells.append(nbf.v4.new_code_cell("""\
purchase_matrix = df.pivot_table(index="CustomerID", columns="ProductName",
                                  values="Quantity", aggfunc="sum", fill_value=0)
item_sim = cosine_similarity(purchase_matrix.T)
item_sim_df = pd.DataFrame(item_sim, index=purchase_matrix.columns, columns=purchase_matrix.columns)

def recommend_similar_products(product_name, top_n=5):
    scores = item_sim_df[product_name].drop(index=product_name).sort_values(ascending=False)
    return scores.head(top_n)

recommend_similar_products("Air Fryer")"""))

cells.append(nbf.v4.new_code_cell("""\
association_rules_df = pd.read_csv("../data/association_rules.csv")
association_rules_df.sort_values("lift", ascending=False).head(10)"""))

cells.append(nbf.v4.new_markdown_cell("""\
## Summary

- Built a full pipeline: **SQL** for KPI extraction -> **Python/Pandas** for RFM
  feature engineering -> **K-Means** for segmentation -> **cosine similarity /
  Apriori** for recommendations.
- Identified 4 actionable customer segments with distinct business strategies.
- Delivered a working recommendation engine usable for personalized marketing
  and cross-sell bundling.

See `README.md` for the full project write-up and `docs/` for detailed insight
summaries.
"""))

nb["cells"] = cells
with open("/home/claude/customer-segmentation-project/notebooks/Customer_Segmentation_Analysis.ipynb", "w") as f:
    nbf.write(nb, f)

print("Notebook created.")
