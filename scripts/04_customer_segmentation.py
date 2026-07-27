"""
04_customer_segmentation.py
Customer Segmentation using RFM (Recency, Frequency, Monetary) analysis
combined with K-Means clustering.

Outputs:
    data/customer_segments.csv
    visuals/06_rfm_elbow_method.png
    visuals/07_customer_segments_scatter.png
    visuals/08_segment_distribution.png
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

sns.set_theme(style="whitegrid")
plt.rcParams["figure.dpi"] = 120

DATA = "/home/claude/customer-segmentation-project/data/online_retail_transactions.csv"
OUT_DATA = "/home/claude/customer-segmentation-project/data/customer_segments.csv"
OUT_VIS = "/home/claude/customer-segmentation-project/visuals"

df = pd.read_csv(DATA, parse_dates=["InvoiceDate"])

# ---------------------------------------------------------------
# 1. Build RFM table
# ---------------------------------------------------------------
ref_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (ref_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("TotalPrice", "sum")
).reset_index()

# ---------------------------------------------------------------
# 2. Scale features & find optimal K (elbow method)
# ---------------------------------------------------------------
features = rfm[["Recency", "Frequency", "Monetary"]]
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

inertias = []
K_range = range(2, 10)
for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(scaled)
    inertias.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(list(K_range), inertias, marker="o", color="#3B5BDB")
plt.title("Elbow Method for Optimal K", fontsize=14, weight="bold")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("Inertia")
plt.tight_layout()
plt.savefig(f"{OUT_VIS}/06_rfm_elbow_method.png")
plt.close()

# ---------------------------------------------------------------
# 3. Fit final KMeans model (K=4: chosen from elbow + business interpretability)
# ---------------------------------------------------------------
K_FINAL = 4
kmeans = KMeans(n_clusters=K_FINAL, random_state=42, n_init=10)
rfm["Cluster"] = kmeans.fit_predict(scaled)

# ---------------------------------------------------------------
# 4. Label clusters by business meaning (based on mean RFM per cluster)
# ---------------------------------------------------------------
cluster_summary = rfm.groupby("Cluster")[["Recency", "Frequency", "Monetary"]].mean()
cluster_summary["RFM_Score"] = (
    cluster_summary["Monetary"].rank() +
    cluster_summary["Frequency"].rank() -
    cluster_summary["Recency"].rank()
)
ranked_clusters = cluster_summary.sort_values("RFM_Score", ascending=False).index.tolist()

segment_names = ["Champions", "Loyal Customers", "Potential / At-Risk", "Lost / Low-Value"]
label_map = {cluster_id: segment_names[i] for i, cluster_id in enumerate(ranked_clusters)}
rfm["Segment"] = rfm["Cluster"].map(label_map)

print("=== Cluster mean RFM values (business interpretation) ===")
print(cluster_summary.round(2))
print("\n=== Segment label mapping ===")
print(label_map)

# ---------------------------------------------------------------
# 5. Save results
# ---------------------------------------------------------------
rfm.to_csv(OUT_DATA, index=False)
print(f"\nSaved segmented customer data to {OUT_DATA}")

# ---------------------------------------------------------------
# 6. Visualization: Frequency vs Monetary scatter colored by segment
# ---------------------------------------------------------------
plt.figure(figsize=(9, 6))
sns.scatterplot(
    data=rfm, x="Frequency", y="Monetary", hue="Segment",
    palette="Set2", s=60, alpha=0.8
)
plt.title("Customer Segments — Frequency vs Monetary Value", fontsize=14, weight="bold")
plt.xlabel("Frequency (number of orders)")
plt.ylabel("Monetary Value (total spend)")
plt.legend(title="Segment", bbox_to_anchor=(1.02, 1), loc="upper left")
plt.tight_layout()
plt.savefig(f"{OUT_VIS}/07_customer_segments_scatter.png")
plt.close()

# ---------------------------------------------------------------
# 7. Visualization: segment distribution
# ---------------------------------------------------------------
plt.figure(figsize=(8, 5))
seg_counts = rfm["Segment"].value_counts()
sns.barplot(x=seg_counts.values, y=seg_counts.index, hue=seg_counts.index, legend=False, palette="Set2")
plt.title("Customer Count by Segment", fontsize=14, weight="bold")
plt.xlabel("Number of Customers")
plt.ylabel("")
plt.tight_layout()
plt.savefig(f"{OUT_VIS}/08_segment_distribution.png")
plt.close()

print("Saved segmentation visualizations to visuals/")

# ---------------------------------------------------------------
# 8. Business insight summary printed to console (also saved to docs/)
# ---------------------------------------------------------------
total_customers = len(rfm)
summary_lines = ["# Customer Segmentation — Key Insights\n"]
for seg in rfm["Segment"].unique():
    seg_df = rfm[rfm["Segment"] == seg]
    pct = 100 * len(seg_df) / total_customers
    summary_lines.append(
        f"- **{seg}**: {len(seg_df)} customers ({pct:.1f}%) | "
        f"Avg Recency: {seg_df['Recency'].mean():.0f} days | "
        f"Avg Frequency: {seg_df['Frequency'].mean():.1f} orders | "
        f"Avg Monetary: {seg_df['Monetary'].mean():,.0f}"
    )

with open("/home/claude/customer-segmentation-project/docs/segmentation_insights.md", "w") as f:
    f.write("\n".join(summary_lines))

print("\n".join(summary_lines))
