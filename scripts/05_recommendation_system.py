"""
05_recommendation_system.py
Two complementary recommendation approaches:

1. Item-Based Collaborative Filtering (cosine similarity on the
   customer-product purchase matrix) -> "Customers who bought this also bought"
2. Market Basket Analysis (Apriori algorithm, mlxtend) -> association rules
   for cross-sell / bundle recommendations.

Outputs:
    models/item_similarity_matrix.csv
    data/association_rules.csv
    docs/sample_recommendations.md
"""

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

DATA = "/home/claude/customer-segmentation-project/data/online_retail_transactions.csv"
df = pd.read_csv(DATA)

# =================================================================
# PART 1 — Item-Based Collaborative Filtering
# =================================================================
print("Building customer-product purchase matrix...")
purchase_matrix = df.pivot_table(
    index="CustomerID", columns="ProductName", values="Quantity",
    aggfunc="sum", fill_value=0
)

# Item-item similarity based on co-purchase patterns
item_sim = cosine_similarity(purchase_matrix.T)
item_sim_df = pd.DataFrame(item_sim, index=purchase_matrix.columns, columns=purchase_matrix.columns)
item_sim_df.to_csv("/home/claude/customer-segmentation-project/models/item_similarity_matrix.csv")
print(f"Saved item-item similarity matrix ({item_sim_df.shape[0]} products).")


def recommend_similar_products(product_name, top_n=5):
    """Return top-N products most similar to a given product."""
    if product_name not in item_sim_df.columns:
        return []
    scores = item_sim_df[product_name].drop(index=product_name).sort_values(ascending=False)
    return list(scores.head(top_n).items())


def recommend_for_customer(customer_id, top_n=5):
    """
    Recommend products for a customer based on items similar to what
    they've already purchased, excluding items already bought.
    """
    if customer_id not in purchase_matrix.index:
        return []
    already_bought = purchase_matrix.loc[customer_id]
    bought_items = already_bought[already_bought > 0].index.tolist()
    if not bought_items:
        return []

    scores = item_sim_df[bought_items].sum(axis=1)
    scores = scores.drop(index=bought_items, errors="ignore")
    return list(scores.sort_values(ascending=False).head(top_n).items())


# =================================================================
# PART 2 — Market Basket Analysis (Apriori / Association Rules)
# =================================================================
print("\nRunning market basket analysis (Apriori)...")
basket = df.groupby(["InvoiceNo", "ProductName"])["Quantity"].sum().unstack().fillna(0)
basket_bool = (basket > 0)

frequent_itemsets = apriori(basket_bool, min_support=0.0015, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)
rules = rules.sort_values("lift", ascending=False)
rules_out = rules[["antecedents", "consequents", "support", "confidence", "lift"]].copy()
rules_out["antecedents"] = rules_out["antecedents"].apply(lambda x: ", ".join(list(x)))
rules_out["consequents"] = rules_out["consequents"].apply(lambda x: ", ".join(list(x)))
rules_out.to_csv("/home/claude/customer-segmentation-project/data/association_rules.csv", index=False)
print(f"Found {len(rules_out)} association rules. Saved to data/association_rules.csv")

# =================================================================
# PART 3 — Generate sample recommendations for a demo doc
# =================================================================
sample_customers = purchase_matrix.index[:3]
sample_products = purchase_matrix.columns[:3]

lines = ["# Sample Recommendation Output\n",
         "## 1. Item-based: \"Customers who bought X also bought...\"\n"]
for p in sample_products:
    recs = recommend_similar_products(p, top_n=5)
    lines.append(f"**{p}**")
    for name, score in recs:
        lines.append(f"  - {name}  (similarity: {score:.3f})")
    lines.append("")

lines.append("## 2. Personalized recommendations per customer\n")
for c in sample_customers:
    recs = recommend_for_customer(c, top_n=5)
    lines.append(f"**Customer {c}**")
    for name, score in recs:
        lines.append(f"  - {name}  (score: {score:.3f})")
    lines.append("")

lines.append("## 3. Top association rules (market basket)\n")
lines.append("| Antecedent | Consequent | Support | Confidence | Lift |")
lines.append("|---|---|---|---|---|")
for _, r in rules_out.head(10).iterrows():
    lines.append(f"| {r['antecedents']} | {r['consequents']} | {r['support']:.4f} | {r['confidence']:.3f} | {r['lift']:.2f} |")

with open("/home/claude/customer-segmentation-project/docs/sample_recommendations.md", "w") as f:
    f.write("\n".join(lines))

print("\nSaved sample recommendations to docs/sample_recommendations.md")
print("\n".join(lines[:25]))
