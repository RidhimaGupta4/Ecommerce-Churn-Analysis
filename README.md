# 🛒 E-commerce Funnel & Churn Analysis — UK Retail 2021–2024
![Retention](https://img.shields.io/badge/Retention_Strategy-Data--Driven-7C6FFF?style=for-the-badge) ![RFM](https://img.shields.io/badge/Customer_Segmentation-RFM_Model-7C6FFF?style=for-the-badge) ![SQL](https://img.shields.io/badge/SQL_Queries-12_Analytical-005EB8?style=for-the-badge)

> End-to-end analysis of a simulated UK e-commerce dataset covering funnel conversion, cohort retention, RFM segmentation, churn prediction, and data-backed retention strategy recommendations.

---

## 🔴 Live Dashboard

[![View Live Dashboard](https://img.shields.io/badge/Live%20Dashboard-View%20Now-7C6FFF?style=for-the-badge)](https://RidhimaGupta4.github.io/Ecommerce-Churn-Analysis/)

---

## 📌 Project Summary

This project answers five core business questions every UK e-commerce company faces:

> **1. Where in the purchase funnel are we losing customers — and how much does it cost?**
>
> **2. What % of customers from each cohort are still buying 3, 6, 12 months later?**
>
> **3. Which customers are about to churn — and which are too valuable to lose?**
>
> **4. Which acquisition channels produce customers who actually stick around?**
>
> **5. What specific actions should we take, for which segments, in what order?**

Built on 5,566 orders, 2,000 customers, 48 months of data (2021–2024).

---

## 🗂️ Repository Structure
```
Ecommerce-Churn-Analysis/
│
├── scripts/
│   ├── 01_generate_data.py        # Full synthetic UK e-commerce data pipeline
│   ├── 02_analysis_queries.sql    # 12 SQL queries (SQLite / DuckDB / PostgreSQL)
│   └── 03_eda_analysis.py         # EDA + chart generation (7 dark-themed charts)
│
├── data/
│   └── processed/
│       ├── customers.csv               # 2,000 customers with acquisition metadata
│       ├── orders.csv                  # 5,566 orders with category, channel, device
│       ├── funnel.csv                  # 48 months of funnel stage metrics
│       ├── cohort_retention.csv        # Month-0 to Month-11 retention per cohort
│       ├── rfm_segments.csv            # RFM scores + segment labels per customer
│       ├── churn_features.csv          # ML-ready feature table with churn label
│       ├── monthly_kpis.csv            # 48-row monthly KPI summary
│       └── dashboard_data.json         # All datasets combined for dashboard
│
├── dashboard/
│   └── index.html                 # Fully self-contained interactive dashboard
│
├── outputs/
│   ├── 01_revenue_aov_trend.png
│   ├── 02_conversion_funnel.png
│   ├── 03_rfm_segment_map.png
│   ├── 04_cohort_retention_heatmap.png
│   ├── 05_churn_by_channel.png
│   ├── 06_category_revenue.png
│   └── 07_retention_strategy_matrix.png
│
├── requirements.txt
├── .gitignore
└── README.md
```
---

## 📊 Dashboard Features

Open `dashboard/index.html` in any browser — **no installation, no server required.**

| Tab | What You See |
|---|---|
| **Overview** | Monthly revenue & AOV trend · Revenue by category · Year-on-year growth |
| **Funnel** | Interactive funnel waterfall · Conversion rate trend · Cart abandonment · Session volume |
| **Cohort** | Colour-coded retention heatmap · Retention curve · RFM segment donut |
| **Churn & RFM** | 7 RFM segment cards with actions · Churn rate by channel · LTV by channel |
| **Strategy** | 3 priority recommendation cards · Full segment action table · Revenue at stake · Optimisation opportunities |
| **Data Table** | Full 48-month KPI dataset filterable by year |

---

## 📐 Key Metrics Defined

### RFM Scoring
```
R (Recency)   = Days since last purchase  — scored 1–5  (5 = most recent)
F (Frequency) = Total number of orders    — scored 1–5  (5 = most frequent)
M (Monetary)  = Total lifetime revenue    — scored 1–5  (5 = highest value)
```
Customers are grouped into segments based on their R, F, M score combination:

| Segment | R Score | F Score | Description |
|---|---|---|---|
| Champions | ≥ 4 | ≥ 4 | Bought recently, buy often, spend the most |
| Loyal Customers | ≥ 3 | ≥ 3 | Regular buyers with solid lifetime spend |
| Recent Customers | ≥ 4 | ≤ 2 | New or recently reactivated |
| Cannot Lose Them | ≤ 2 | ≥ 4 | Used to buy a lot — now gone quiet |
| At Risk | ≤ 2 | ≥ 3 | Dropping off — need immediate attention |
| Hibernating | ≤ 2 | ≤ 2 | Low activity, long dormant |
| Lost | = 1 | = 1 | Likely churned permanently |

---
### 🔄 Churn Logic & Validation

For this analysis, **Churn** is defined using a **90-day inactivity window**. 

*   **Why 90 Days?** Based on UK e-commerce benchmarks, the typical customer purchase cycle for this category ranges from 30 to 60 days. A 90-day window ensures we are not flagging "active" customers who simply have a slightly longer replenishment cycle, while still capturing "at-risk" customers early enough for a win-back campaign.
*   **Segmentation Accuracy:** By combining this churn definition with RFM scores, we distinguish between **"Hibernating"** customers (low value, long gone) and **"Cannot Lose Them"** customers (high value, recently lapsed), allowing for prioritised marketing spend.

### Churn Definition
```
Churned = 1   if   days since last purchase  >  90
Churned = 0   if   days since last purchase  ≤  90
```
A 90-day window is the standard e-commerce benchmark where purchase cycles are typically monthly to quarterly.

---

### Cohort Retention Rate
```
Retention Rate (Month N) =  Customers from cohort still purchasing in Month N
                            ────────────────────────────────────────────────── × 100
                                       Cohort size at Month 0
```
---

### Overall Funnel Conversion Rate
```
Conversion Rate (%) = Purchases ÷ Sessions × 100
```
UK e-commerce average: 3–5%. This dataset achieves **6.8%** — above benchmark.

---

## 🔑 Key Findings

| Finding | Data Point |
|---|---|
| Total revenue growth 2021 → 2024 | **£46k → £640k — 1,284% increase** |
| Overall churn rate | **57.6%** of customers inactive for more than 90 days |
| Champions segment | **374 customers = 40% of all revenue (£428k)** — most critical to protect |
| Cannot Lose Them | **153 customers, £145k revenue** — highest urgency win-back target |
| Best acquisition channel by LTV | **Social Media: £682 avg LTV** |
| Worst acquisition channel by churn | **Organic Search: 61.7% churn rate** |
| Referral channel | **Lowest churn at 46.8%** — highest quality customers |
| Cart abandonment rate | **43.5%** — significantly better than UK average of ~75% |
| Checkout abandonment | **27%** — key drop-off point, fixing = ~£14k/month gain |
| Month 1 retention average | **~12%** — very steep initial drop, biggest intervention window |
| November revenue uplift | **~2.5× vs average month** — Black Friday impact |
| Repeat order rate 2024 | **78%** — up from 32% in 2021 |

---

### ⚠️ Project Limitations

This analysis provides a strategic overview of customer retention, but the following limitations apply:
*   **External Factors**: The dataset does not account for competitor pricing changes or macro-economic shifts (e.g., inflation impact on discretionary spend) which can cause sudden churn spikes independent of customer loyalty.
*   **Single-Event Bias**: RFM scoring treats all purchases equally, but does not distinguish between seasonal "one-off" gift buyers and true brand advocates without deeper sentiment analysis.
*   **Window Sensitivity**: The 90-day churn definition is an e-commerce benchmark, but may be too aggressive for high-ticket categories with naturally longer replacement cycles (e.g., furniture or luxury electronics).

---

## 🛠️ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/RidhimaGupta4/Ecommerce-Churn-Analysis.git
cd Ecommerce-Churn-Analysis
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate all datasets

```bash
python scripts/01_generate_data.py
```

Creates 7 CSV files and 1 JSON in `data/processed/`.

### 4. Generate all 7 charts

```bash
python scripts/03_eda_analysis.py
```

Outputs 7 PNG charts to `outputs/`.

### 5. Open the interactive dashboard

```bash
# macOS
open dashboard/index.html

# Windows
start dashboard/index.html

# Linux
xdg-open dashboard/index.html
```

Or simply double-click `dashboard/index.html` in your file explorer.

---

### Optional — Run SQL analysis with DuckDB

```bash
pip install duckdb
```

```python
import duckdb

con = duckdb.connect()
con.execute("CREATE TABLE orders    AS SELECT * FROM read_csv_auto('data/processed/orders.csv')")
con.execute("CREATE TABLE customers AS SELECT * FROM read_csv_auto('data/processed/customers.csv')")
con.execute("CREATE TABLE rfm       AS SELECT * FROM read_csv_auto('data/processed/rfm_segments.csv')")
con.execute("CREATE TABLE churn     AS SELECT * FROM read_csv_auto('data/processed/churn_features.csv')")
con.execute("CREATE TABLE funnel    AS SELECT * FROM read_csv_auto('data/processed/funnel.csv')")
con.execute("CREATE TABLE kpis      AS SELECT * FROM read_csv_auto('data/processed/monthly_kpis.csv')")
con.execute("CREATE TABLE cohort    AS SELECT * FROM read_csv_auto('data/processed/cohort_retention.csv')")

# RFM segment revenue breakdown
print(con.execute("""
    SELECT rfm_segment,
           COUNT(customer_id)                                           AS n_customers,
           ROUND(AVG(monetary), 2)                                     AS avg_ltv,
           ROUND(SUM(monetary), 0)                                     AS total_revenue,
           ROUND(SUM(monetary) * 100.0 / SUM(SUM(monetary)) OVER(), 1) AS pct_of_revenue
    FROM rfm
    GROUP BY rfm_segment
    ORDER BY avg_ltv DESC
""").df())
```

All 12 queries are in `scripts/02_analysis_queries.sql`.

---

## 🗃️ Dataset Schema

### `orders.csv` — 5,566 rows

| Column | Type | Description |
|---|---|---|
| `order_id` | string | Unique order identifier |
| `customer_id` | string | Customer reference |
| `order_date` | date | Order placement date |
| `year` / `month` / `quarter` | int | Temporal breakdowns |
| `category` | string | Product category (7 categories) |
| `quantity` | int | Items ordered |
| `unit_price` | float | Pre-discount price per unit (£) |
| `discount_pct` | float | Discount applied (0 to 0.25) |
| `revenue` | float | Final order revenue (£) |
| `channel` | string | Acquisition channel |
| `device` | string | Device type (Mobile / Desktop / Tablet) |
| `region` | string | UK region |
| `is_repeat` | int | 1 if not the customer's first order |

---

### `rfm_segments.csv` — one row per customer

RFM scores (1–5 each), segment label, recency in days, frequency, total monetary value, average order value, number of categories purchased, and acquisition metadata.

---

### `churn_features.csv` — ML-ready feature table

Binary churn label (1 = inactive >90 days), all RFM features, purchase rate per month, `is_high_value` flag, `is_frequent` flag. Ready for use directly in scikit-learn or XGBoost.

---

### `cohort_retention.csv`

Cohort month, period number (0–11), number of customers still active, cohort size, retention rate %. Suitable for direct use in a pivot table or heatmap.

---

### ⚖️ Data Ethics & Privacy

*   **Synthetic Logic**: While the dataset is synthetic, all distributions (AOV, conversion rates, abandonment) are calibrated against **UK Retail Benchmarks** and **ONS Retail Sales** data to ensure realistic business insights.
*   **Customer Anonymity**: The project follows **GDPR** principles by ensuring no PII (Personally Identifiable Information) is included. Data is aggregated at the segment and cohort level to demonstrate high-level business strategy without compromising individual privacy.
*   **Algorithmic Transparency**: RFM scoring and churn labeling are documented with clear, transparent logic to avoid "black-box" bias in customer segmentation.

---

## 📈 SQL Queries Included

| Query | Purpose |
|---|---|
| `01` — Revenue YoY | Annual growth in revenue, AOV, repeat rate, revenue per customer |
| `02` — Funnel Conversion | Stage-by-stage conversion rates by year |
| `03` — Peak Season | Nov/Dec vs Summer vs rest of year — conversion and abandonment |
| `04` — RFM Revenue | Segment contribution to total revenue with percentage share |
| `05` — Churn by Channel | Which channels produce the most loyal customers |
| `06` — Churn by Segment | Churn rate and revenue per RFM segment |
| `07` — Cohort Pivot | Month 0 to Month 11 retention rate pivot table |
| `08` — Category Analysis | Revenue, AOV, discount rate, items per order by category |
| `09` — Repeat Purchase Gap | Time between first and second purchase — key retention window |
| `10` — High Value Profile | Top 25% vs bottom 25% customer comparison |
| `11` — Win-Back Targets | Prioritised list of at-risk high-value customers to contact |
| `12` — Seasonality | Monthly revenue and conversion seasonality pattern |

---

## 🔗 Data Sources & Benchmarks

| Benchmark | Source | Value Used |
|---|---|---|
| UK e-commerce conversion rate | ONS / Statista | 3–5% average |
| Cart abandonment rate | Baymard Institute | ~75% global average |
| Average order value UK | ONS Retail Sales | £65–£85 typical range |
| RFM segmentation methodology | Harvard Business Review | Standard RFM framework |
| Churn definition (90-day) | Industry standard | E-commerce benchmark |

---

## 🧰 Tech Stack

| Tool | Badge | Role |
| :--- | :--- | :--- |
| **Python** | ![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white) | Customer behavior simulation & churn feature engineering |
| **SQL** | ![SQL](https://img.shields.io/badge/SQL-Analytical-CC0000?style=flat-square&logo=postgresql&logoColor=white) | 12 queries: Cohort pivots, RFM scoring, & peak season analysis |
| **DuckDB** | ![DuckDB](https://img.shields.io/badge/DuckDB-Fast_SQL-FFF000?style=flat-square&logo=duckdb&logoColor=black) | Local OLAP engine for high-speed retention calculations |
| **Pandas / NumPy**| ![Data](https://img.shields.io/badge/Pandas_/_NumPy-CRM_Data-150458?style=flat-square&logo=pandas&logoColor=white) | Cohort matrix generation & RFM segmentation logic |
| **JavaScript** | ![JS](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=flat-square&logo=javascript&logoColor=black) | Interactive funnel waterfall & cohort heatmap logic |
| **Chart.js** | ![Chart.js](https://img.shields.io/badge/Chart.js-UI-FF6384?style=flat-square&logo=chartdotjs&logoColor=white) | Dynamic churn dashboard & segment donut charts |
| **Matplotlib** | ![Matplotlib](https://img.shields.io/badge/Matplotlib-Dark_Theme-11557c?style=flat-square) | Professional dark-mode static charts for stakeholders |

---

## 💼 Skills Demonstrated

- End-to-end e-commerce analytics — funnel, cohort, RFM, and churn all in one project
- RFM segmentation from scratch — custom scoring, segment labelling, business action mapping
- Cohort analysis — monthly retention heatmap, retention curve, drop-off identification
- Churn feature engineering — binary labelling, purchase rate, lag variables, ML-ready output
- Business recommendation framing — every finding tied to a specific action with £ impact estimate
- SQL depth — 12 queries covering YoY, cohort pivot, repeat purchase gap, high-value profiling
- Dark-theme data visualisation — professional e-commerce analytics aesthetic

---

## 🔍 Visual Insights

### 💰 Revenue & AOV Trend (2021–2024)
![Revenue AOV Trend](outputs/01_revenue_aov_trend.png)
> **Analysis:** Identifies long-term growth trajectories and Black Friday seasonality peaks. The dual-axis chart highlights the relationship between transaction volume and average spend.

### 🌪️ E-commerce Conversion Funnel — 2024 Monthly Average
![Conversion Funnel](outputs/02_conversion_funnel.png)
> **Analysis:** Visualises drop-off points from session to purchase. The 27% checkout abandonment rate identified here represents a specific £14k/month optimisation opportunity.

### 🎯 RFM Segment Map — Bubble Size = Revenue
![RFM Segment Map](outputs/03_rfm_segment_map.png)
> **Analysis:** Bubble chart mapping Recency vs. Frequency, with bubble size representing Monetary value. This identifies the "Champions" segment (40% of revenue) versus "At Risk" high-value targets.

### 🗓️ Cohort Retention Heatmap
![Cohort Heatmap](outputs/04_cohort_retention_heatmap.png)
> **Analysis:** Tracks customer loyalty over 12 months. The heatmap identifies the "Month 1 Cliff," where initial retention drops to 12%, pinpointing the critical window for automated re-engagement.

### 📢 Churn Rate & LTV by Acquisition Channel Performance
![Churn by Channel](outputs/05_churn_by_channel.png)
> **Analysis:** Correlates churn rate with LTV across Social, Search, and Referral. Social Media produces the highest LTV (£682), while Referral traffic exhibits the lowest churn (46.8%).

### 📦 Category Revenue Breakdown & AOV
![Category Revenue](outputs/06_category_revenue.png)
> **Analysis:** Highlights the dominance of Electronics in total revenue (£480k+), driven by a high Average Order Value (£350+). In contrast, Clothing shows high volume (unique buyers) but lower AOV, suggesting a high-frequency replenishment model.

### 📈 Retention Strategy Matrix
![Retention Strategy](outputs/07_retention_strategy_matrix.png)
> **Analysis:** A decision-support matrix mapping specific business actions (e.g., win-back emails, VIP discounts) to the identified RFM segments based on their revenue-at-stake.

---

## 📄 Licence

MIT — free to use and adapt
---

## 🙋 Author

Built as a UK data analyst / data scientist portfolio project.

**Connect:** [LinkedIn](https://www.linkedin.com/in/ridhimagupta1623/) · [GitHub](https://github.com/RidhimaGupta4) 

> If this project helped you, please ⭐ star the repo — it helps others find it.

## 📁 Explore More Projects

*   **[🏠 UK Property Price Predictor](https://github.com/RidhimaGupta4/UK-Property-Price-Predictor)** — High-accuracy ML pipeline for real estate valuation and geospatial analysis.
*   **[🏥 NHS A&E Wait Time Analysis](https://github.com/RidhimaGupta4/NHS-AE-Wait-Time-Analysis)** — Operational healthcare analytics and trend forecasting.
*   **[🇬🇧 UK Cost-of-Living Dashboard](https://github.com/RidhimaGupta4/UK-Cost-of-Living)** — Regional economic data storytelling and affordability mapping.
