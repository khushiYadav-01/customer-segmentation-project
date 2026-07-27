# 🛍️ Customer Segmentation & Business Insights

An end-to-end data analytics project that segments e-commerce customers using
**RFM analysis + K-Means clustering**, extracts **business insights via SQL**,
visualizes key trends, and powers a **product recommendation system**
(collaborative filtering + market basket analysis).

**Skills demonstrated:** SQL · Python · Data Visualization · Business Analysis · Recommendation Systems

---

## 📌 Project Overview

Using a simulated online-retail transactions dataset (800 customers, ~8,400
orders, 25k order line items, 6 product categories, 10 countries), this
project answers:

- What are our overall revenue, order, and customer trends?
- Which products/categories/countries drive the most revenue?
- Who are our most valuable customers, and how do we segment them?
- Which customers are at risk of churning, and who are our champions?
- What should we recommend to a customer next, based on purchase behavior?

---

## 🗂️ Project Structure

```
customer-segmentation-project/
├── data/
│   ├── online_retail_transactions.csv   # Main transactions dataset (line items)
│   ├── customers_master.csv             # Customer master data
│   ├── products_master.csv              # Product master data
│   ├── customer_segments.csv            # Output: RFM + segment labels per customer
│   ├── association_rules.csv            # Output: market basket association rules
│   └── retail.db                        # SQLite database (for SQL analysis)
│
├── sql/
│   └── business_insights.sql            # 10 SQL queries: KPIs, trends, RFM, top customers, etc.
│
├── scripts/
│   ├── 01_generate_data.py              # Synthetic dataset generator
│   ├── 02_load_to_sql.py                # Loads CSVs into SQLite
│   ├── 03_eda_visualizations.py         # EDA + charts
│   ├── 04_customer_segmentation.py      # RFM + K-Means segmentation
│   ├── 05_recommendation_system.py      # Collaborative filtering + Apriori
│   └── build_notebook.py                # Generates the consolidated notebook
│
├── notebooks/
│   └── Customer_Segmentation_Analysis.ipynb   # Full walkthrough notebook
│
├── visuals/                             # All generated PNG charts
│   ├── 01_monthly_revenue_trend.png
│   ├── 02_revenue_by_category.png
│   ├── 03_top10_products.png
│   ├── 04_revenue_by_country.png
│   ├── 05_order_value_distribution.png
│   ├── 06_rfm_elbow_method.png
│   ├── 07_customer_segments_scatter.png
│   └── 08_segment_distribution.png
│
├── models/
│   └── item_similarity_matrix.csv       # Item-item cosine similarity matrix
│
├── docs/
│   ├── segmentation_insights.md         # Business insight summary
│   └── sample_recommendations.md        # Example recommendation outputs
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd customer-segmentation-project

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline in order
python scripts/01_generate_data.py            # generates the dataset
python scripts/02_load_to_sql.py               # loads data into SQLite
python scripts/03_eda_visualizations.py        # EDA + charts
python scripts/04_customer_segmentation.py     # RFM + K-Means segmentation
python scripts/05_recommendation_system.py     # recommendation system

# 4. (Optional) Explore the SQL queries
sqlite3 data/retail.db < sql/business_insights.sql

# 5. (Optional) Open the full notebook walkthrough
jupyter notebook notebooks/Customer_Segmentation_Analysis.ipynb
```

> Note: `data/online_retail_transactions.csv` is **synthetically generated**
> (see `scripts/01_generate_data.py`) so the project is fully self-contained
> and reproducible without needing an external dataset download. The
> generation logic bakes in realistic customer loyalty tiers, seasonal
> purchase timing, and category-level co-purchase behavior, so the
> segmentation and recommendation outputs are meaningful.

---

## 🔍 Methodology

### 1. SQL — Business Insights (`sql/business_insights.sql`)
10 queries covering: overall KPIs, monthly revenue trend, top products,
category/country revenue share, RFM base metrics (with `NTILE` quartile
scoring), top customers by lifetime value, repeat purchase rate, and
co-purchase pairs.

### 2. EDA & Visualization (`scripts/03_eda_visualizations.py`)
Revenue trends, category/product/country breakdowns, and order value
distribution — visualized with Matplotlib/Seaborn.

### 3. Customer Segmentation (`scripts/04_customer_segmentation.py`)
- **RFM feature engineering**: Recency, Frequency, Monetary value per customer.
- **K-Means clustering** (features standardized, optimal K chosen via elbow
  method) into 4 segments.
- Segments are business-labeled by ranking cluster-level RFM stats:

| Segment | Description | Suggested Action |
|---|---|---|
| **Champions** | Most recent, most frequent, highest spend | Loyalty rewards, early access, referral programs |
| **Loyal Customers** | Regular, healthy spend | Cross-sell/upsell personalized offers |
| **Potential / At-Risk** | Moderate activity, declining engagement | Win-back campaigns, targeted discounts |
| **Lost / Low-Value** | Long inactive, low spend | Low-cost reactivation or deprioritize |

### 4. Recommendation System (`scripts/05_recommendation_system.py`)
Two complementary approaches:
- **Item-based collaborative filtering** — cosine similarity on the
  customer × product purchase matrix → "customers who bought X also bought…"
  and personalized per-customer recommendations.
- **Market basket analysis (Apriori)** — association rules (support,
  confidence, lift) for cross-sell bundle suggestions.

---

## 📊 Sample Insights

- ~8% of customers are **Champions**, contributing a disproportionately high
  share of total revenue — prioritize retention for this group.
- ~50% of customers fall into the **Potential / At-Risk** bucket — the
  single largest opportunity for win-back campaigns.
- Certain product pairs (e.g. kitchen appliances, stationery items) show high
  **lift** in the association rules — good candidates for bundle promotions.

(Full breakdown in `docs/segmentation_insights.md` and
`docs/sample_recommendations.md`.)

---

## 🛠️ Tech Stack

- **Python**: pandas, numpy
- **SQL**: SQLite
- **ML**: scikit-learn (K-Means, StandardScaler), mlxtend (Apriori, association rules)
- **Visualization**: matplotlib, seaborn
- **Notebook**: Jupyter

---

## 📈 Possible Extensions

- Swap in a real dataset (e.g. UCI Online Retail) via the same pipeline.
- Add a Streamlit/Dash dashboard for interactive segment exploration.
- Try alternative clustering (DBSCAN, hierarchical) and compare silhouette scores.
- Deploy the recommendation engine behind a simple Flask/FastAPI endpoint.

---

## 👤 Author

Built as an internship project to demonstrate SQL, Python, data
visualization, business analysis, and recommendation system skills.
