-- =====================================================================
-- Customer Segmentation & Business Insights
-- SQL Analysis Queries  (SQLite dialect — run against data/retail.db)
-- =====================================================================

-- -----------------------------------------------------------------
-- 1. Overall business snapshot
-- -----------------------------------------------------------------
SELECT
    COUNT(DISTINCT InvoiceNo)      AS total_orders,
    COUNT(DISTINCT CustomerID)     AS total_customers,
    COUNT(DISTINCT ProductID)      AS total_products_sold,
    ROUND(SUM(TotalPrice), 2)      AS total_revenue,
    ROUND(AVG(TotalPrice), 2)      AS avg_line_item_value
FROM transactions;


-- -----------------------------------------------------------------
-- 2. Monthly revenue trend
-- -----------------------------------------------------------------
SELECT
    strftime('%Y-%m', InvoiceDate)   AS year_month,
    ROUND(SUM(TotalPrice), 2)        AS revenue,
    COUNT(DISTINCT InvoiceNo)        AS orders
FROM transactions
GROUP BY year_month
ORDER BY year_month;


-- -----------------------------------------------------------------
-- 3. Top 10 products by revenue
-- -----------------------------------------------------------------
SELECT
    ProductName,
    Category,
    SUM(Quantity)               AS units_sold,
    ROUND(SUM(TotalPrice), 2)   AS revenue
FROM transactions
GROUP BY ProductID, ProductName, Category
ORDER BY revenue DESC
LIMIT 10;


-- -----------------------------------------------------------------
-- 4. Revenue & order share by product category
-- -----------------------------------------------------------------
SELECT
    Category,
    COUNT(DISTINCT InvoiceNo)                                  AS orders,
    ROUND(SUM(TotalPrice), 2)                                  AS revenue,
    ROUND(100.0 * SUM(TotalPrice) / (SELECT SUM(TotalPrice) FROM transactions), 2) AS pct_of_total_revenue
FROM transactions
GROUP BY Category
ORDER BY revenue DESC;


-- -----------------------------------------------------------------
-- 5. Revenue by country
-- -----------------------------------------------------------------
SELECT
    Country,
    COUNT(DISTINCT CustomerID)   AS customers,
    ROUND(SUM(TotalPrice), 2)    AS revenue
FROM transactions
GROUP BY Country
ORDER BY revenue DESC;


-- -----------------------------------------------------------------
-- 6. Customer-level RFM base metrics
--    (Recency = days since last purchase relative to dataset's max date)
-- -----------------------------------------------------------------
WITH max_date AS (
    SELECT MAX(InvoiceDate) AS ref_date FROM transactions
)
SELECT
    t.CustomerID,
    c.CustomerName,
    c.Country,
    CAST(julianday((SELECT ref_date FROM max_date)) - julianday(MAX(t.InvoiceDate)) AS INTEGER) AS recency_days,
    COUNT(DISTINCT t.InvoiceNo)   AS frequency,
    ROUND(SUM(t.TotalPrice), 2)   AS monetary
FROM transactions t
JOIN customers c ON c.CustomerID = t.CustomerID
GROUP BY t.CustomerID, c.CustomerName, c.Country
ORDER BY monetary DESC;


-- -----------------------------------------------------------------
-- 7. Quick RFM scoring using NTILE quartiles (1 = worst, 4 = best)
-- -----------------------------------------------------------------
WITH max_date AS (
    SELECT MAX(InvoiceDate) AS ref_date FROM transactions
),
rfm_base AS (
    SELECT
        CustomerID,
        CAST(julianday((SELECT ref_date FROM max_date)) - julianday(MAX(InvoiceDate)) AS INTEGER) AS recency_days,
        COUNT(DISTINCT InvoiceNo)  AS frequency,
        SUM(TotalPrice)            AS monetary
    FROM transactions
    GROUP BY CustomerID
)
SELECT
    CustomerID,
    recency_days,
    frequency,
    ROUND(monetary, 2) AS monetary,
    NTILE(4) OVER (ORDER BY recency_days DESC) AS r_score,   -- more recent -> higher score
    NTILE(4) OVER (ORDER BY frequency ASC)     AS f_score,
    NTILE(4) OVER (ORDER BY monetary ASC)      AS m_score
FROM rfm_base
ORDER BY monetary DESC;


-- -----------------------------------------------------------------
-- 8. Top 20 customers by lifetime value
-- -----------------------------------------------------------------
SELECT
    t.CustomerID,
    c.CustomerName,
    c.Country,
    COUNT(DISTINCT t.InvoiceNo)  AS total_orders,
    ROUND(SUM(t.TotalPrice), 2)  AS lifetime_value
FROM transactions t
JOIN customers c ON c.CustomerID = t.CustomerID
GROUP BY t.CustomerID, c.CustomerName, c.Country
ORDER BY lifetime_value DESC
LIMIT 20;


-- -----------------------------------------------------------------
-- 9. Repeat purchase rate
-- -----------------------------------------------------------------
WITH order_counts AS (
    SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS orders
    FROM transactions
    GROUP BY CustomerID
)
SELECT
    ROUND(100.0 * SUM(CASE WHEN orders > 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS repeat_customer_pct,
    COUNT(*) AS total_customers
FROM order_counts;


-- -----------------------------------------------------------------
-- 10. Products frequently bought together (basic co-purchase pairs)
-- -----------------------------------------------------------------
SELECT
    a.ProductName AS product_a,
    b.ProductName AS product_b,
    COUNT(*)      AS times_bought_together
FROM transactions a
JOIN transactions b
    ON a.InvoiceNo = b.InvoiceNo
   AND a.ProductID < b.ProductID
GROUP BY a.ProductName, b.ProductName
ORDER BY times_bought_together DESC
LIMIT 15;
