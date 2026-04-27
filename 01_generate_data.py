"""
E-commerce Funnel & Churn Analysis — Data Generation
======================================================
Generates a realistic UK e-commerce dataset (2021–2024) covering:
  - Customer transactions and order history
  - Funnel stage events (visit → browse → cart → purchase)
  - Cohort tables for retention analysis
  - RFM (Recency, Frequency, Monetary) segmentation
  - Churn labels and predictor features

Modelled on UK e-commerce benchmarks:
  - Average cart abandonment rate: ~75% (Baymard Institute)
  - Average order value UK: £65–£85 (ONS Retail Sales)
  - Monthly active user churn: ~5–8% (SaaS/e-com benchmarks)

Run:
    pip install pandas numpy
    python 01_generate_data.py
"""

import pandas as pd
import numpy as np
import json, os
from datetime import datetime, timedelta

np.random.seed(42)

# ── Config ────────────────────────────────────────────────────────────────────

N_CUSTOMERS   = 5000
START_DATE    = datetime(2021, 1, 1)
END_DATE      = datetime(2024, 12, 31)
TOTAL_DAYS    = (END_DATE - START_DATE).days

CATEGORIES = ["Clothing", "Electronics", "Home & Garden", "Beauty", "Sports", "Books", "Toys"]
CAT_WEIGHTS = [0.28, 0.22, 0.18, 0.12, 0.10, 0.06, 0.04]

CHANNELS = ["Organic Search", "Paid Search", "Email", "Social Media", "Direct", "Referral"]
CHANNEL_WEIGHTS = [0.30, 0.22, 0.18, 0.15, 0.10, 0.05]

DEVICES = ["Mobile", "Desktop", "Tablet"]
DEVICE_WEIGHTS = [0.58, 0.34, 0.08]

UK_REGIONS = ["London", "South East", "North West", "Yorkshire", "Midlands",
              "South West", "North East", "Scotland", "Wales"]
REGION_WEIGHTS = [0.18, 0.14, 0.12, 0.09, 0.11, 0.08, 0.07, 0.13, 0.08]

# Average order value by category (£)
AOV_BY_CAT = {
    "Clothing": 62, "Electronics": 145, "Home & Garden": 78,
    "Beauty": 38, "Sports": 55, "Books": 22, "Toys": 34
}

# Seasonal multipliers for purchase probability
MONTHLY_SEASON = {
    1: 0.82, 2: 0.78, 3: 0.88, 4: 0.92, 5: 0.95,
    6: 0.97, 7: 0.93, 8: 0.90, 9: 0.94, 10: 1.05,
    11: 1.35, 12: 1.55  # Black Friday + Christmas
}

# ── Customer Table ────────────────────────────────────────────────────────────

def build_customers():
    customers = []
    for i in range(N_CUSTOMERS):
        reg_offset = np.random.randint(0, TOTAL_DAYS - 30)
        reg_date   = START_DATE + timedelta(days=int(reg_offset))
        segment    = np.random.choice(
            ["Champions", "Loyal", "At Risk", "Hibernating", "New", "Lost"],
            p=[0.10, 0.20, 0.18, 0.15, 0.22, 0.15]
        )
        # Segment drives behaviour
        base_purchase_prob = {
            "Champions": 0.72, "Loyal": 0.55, "At Risk": 0.28,
            "Hibernating": 0.12, "New": 0.38, "Lost": 0.05
        }[segment]

        customers.append({
            "customer_id": f"C{i+1:05d}",
            "registration_date": reg_date.strftime("%Y-%m-%d"),
            "region": np.random.choice(UK_REGIONS, p=REGION_WEIGHTS),
            "acquisition_channel": np.random.choice(CHANNELS, p=CHANNEL_WEIGHTS),
            "preferred_device": np.random.choice(DEVICES, p=DEVICE_WEIGHTS),
            "preferred_category": np.random.choice(CATEGORIES, p=CAT_WEIGHTS),
            "segment": segment,
            "base_purchase_prob": base_purchase_prob,
            "age_band": np.random.choice(["18-24","25-34","35-44","45-54","55+"],
                                          p=[0.15,0.30,0.25,0.18,0.12]),
        })
    return pd.DataFrame(customers)


# ── Orders Table ──────────────────────────────────────────────────────────────

def build_orders(customers_df):
    orders = []
    order_id = 1

    for _, cust in customers_df.iterrows():
        reg_date = datetime.strptime(cust["registration_date"], "%Y-%m-%d")
        days_active = (END_DATE - reg_date).days
        if days_active <= 0:
            continue

        prob = cust["base_purchase_prob"]
        # Expected orders over lifetime
        n_orders = max(0, int(np.random.negative_binomial(2, 1 - min(prob, 0.98)) + 1))
        if cust["segment"] in ["Lost", "Hibernating"]:
            n_orders = min(n_orders, 3)

        order_dates = sorted([
            reg_date + timedelta(days=int(np.random.randint(0, days_active)))
            for _ in range(n_orders)
        ])

        for odate in order_dates:
            cat  = cust["preferred_category"] if np.random.random() < 0.65 else np.random.choice(CATEGORIES, p=CAT_WEIGHTS)
            base_aov = AOV_BY_CAT[cat]
            season_mult = MONTHLY_SEASON[odate.month]
            aov  = max(5.0, np.random.normal(base_aov * season_mult, base_aov * 0.3))
            qty  = np.random.randint(1, 5)
            disc = round(np.random.uniform(0, 0.25) if np.random.random() < 0.35 else 0, 2)
            revenue = round(aov * qty * (1 - disc), 2)

            orders.append({
                "order_id":       f"O{order_id:07d}",
                "customer_id":    cust["customer_id"],
                "order_date":     odate.strftime("%Y-%m-%d"),
                "year":           odate.year,
                "month":          odate.month,
                "quarter":        f"Q{(odate.month-1)//3+1}",
                "category":       cat,
                "quantity":       qty,
                "unit_price":     round(aov, 2),
                "discount_pct":   disc,
                "revenue":        revenue,
                "channel":        cust["acquisition_channel"],
                "device":         cust["preferred_device"],
                "region":         cust["region"],
                "is_repeat":      int(len([o for o in orders if o["customer_id"]==cust["customer_id"]]) > 0),
            })
            order_id += 1

    return pd.DataFrame(orders)


# ── Funnel Events Table ───────────────────────────────────────────────────────

def build_funnel():
    """
    Monthly funnel: Sessions → PDP Views → Add to Cart → Checkout Start → Purchase
    Modelled on UK e-commerce conversion benchmarks.
    """
    rows = []
    base_sessions = 120_000

    for year in [2021, 2022, 2023, 2024]:
        for month in range(1, 13):
            if year == 2024 and month > 12:
                break
            season = MONTHLY_SEASON[month]
            yoy_growth = 1 + (year - 2021) * 0.12  # 12% YoY growth
            sessions = int(base_sessions * season * yoy_growth * np.random.uniform(0.96, 1.04))

            # Funnel drop-offs (realistic UK e-com rates)
            pdp_rate       = np.random.uniform(0.58, 0.68)   # 58-68% view a product
            cart_rate      = np.random.uniform(0.22, 0.30)   # 22-30% add to cart
            checkout_rate  = np.random.uniform(0.52, 0.62)   # 52-62% of cart starts checkout
            purchase_rate  = np.random.uniform(0.68, 0.78)   # 68-78% of checkouts complete

            pdp_views      = int(sessions * pdp_rate)
            cart_adds      = int(pdp_views * cart_rate)
            checkouts      = int(cart_adds * checkout_rate)
            purchases      = int(checkouts * purchase_rate)

            cart_abandon   = cart_adds - checkouts
            checkout_abandon = checkouts - purchases

            rows.append({
                "year": year, "month": month,
                "period": f"{year}-{month:02d}",
                "sessions": sessions,
                "pdp_views": pdp_views,
                "cart_adds": cart_adds,
                "checkouts_started": checkouts,
                "purchases": purchases,
                "cart_abandonment_rate": round((1 - checkout_rate) * 100, 1),
                "checkout_abandonment_rate": round((1 - purchase_rate) * 100, 1),
                "overall_conversion_rate": round(purchases / sessions * 100, 2),
                "pdp_conversion_rate": round(pdp_views / sessions * 100, 1),
                "cart_to_purchase_rate": round(purchases / cart_adds * 100, 1) if cart_adds > 0 else 0,
            })

    return pd.DataFrame(rows)


# ── Cohort Retention Table ────────────────────────────────────────────────────

def build_cohort_retention(orders_df):
    """
    Monthly cohort retention: % of customers from acquisition month still purchasing N months later.
    """
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    orders_df["order_month"] = orders_df["order_date"].dt.to_period("M")

    # First purchase month per customer = cohort
    first_purchase = orders_df.groupby("customer_id")["order_month"].min().reset_index()
    first_purchase.columns = ["customer_id", "cohort_month"]

    merged = orders_df.merge(first_purchase, on="customer_id")
    merged["period_number"] = (merged["order_month"] - merged["cohort_month"]).apply(lambda x: x.n)

    cohort_data = merged.groupby(["cohort_month", "period_number"])["customer_id"].nunique().reset_index()
    cohort_data.columns = ["cohort_month", "period_number", "n_customers"]

    cohort_size = cohort_data[cohort_data["period_number"] == 0].set_index("cohort_month")["n_customers"]
    cohort_data["cohort_size"] = cohort_data["cohort_month"].map(cohort_size)
    cohort_data["retention_rate"] = (cohort_data["n_customers"] / cohort_data["cohort_size"] * 100).round(1)
    cohort_data["cohort_month"] = cohort_data["cohort_month"].astype(str)

    # Keep cohorts from 2021 only, up to 12 periods
    cohort_data = cohort_data[
        (cohort_data["cohort_month"] >= "2021-01") &
        (cohort_data["period_number"] <= 11)
    ]
    return cohort_data


# ── RFM Segmentation ──────────────────────────────────────────────────────────

def build_rfm(orders_df, customers_df):
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    snapshot = pd.Timestamp("2024-12-31")

    rfm = orders_df.groupby("customer_id").agg(
        recency_days   = ("order_date", lambda x: (snapshot - x.max()).days),
        frequency      = ("order_id", "count"),
        monetary       = ("revenue", "sum"),
        first_order    = ("order_date", "min"),
        last_order     = ("order_date", "max"),
        avg_order_value= ("revenue", "mean"),
        n_categories   = ("category", "nunique"),
    ).reset_index()

    # RFM scoring 1–5
    rfm["r_score"] = pd.qcut(rfm["recency_days"], 5, labels=[5,4,3,2,1]).astype(int)
    rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
    rfm["rfm_score"] = rfm["r_score"] * 100 + rfm["f_score"] * 10 + rfm["m_score"]

    def segment(row):
        r, f, m = row["r_score"], row["f_score"], row["m_score"]
        if r >= 4 and f >= 4: return "Champions"
        if r >= 3 and f >= 3: return "Loyal Customers"
        if r >= 4 and f <= 2: return "Recent Customers"
        if r <= 2 and f >= 3: return "At Risk"
        if r <= 2 and f >= 4: return "Cannot Lose Them"
        if r == 3 and f == 3: return "Needs Attention"
        if r <= 2 and f <= 2: return "Hibernating"
        if r == 1 and f == 1: return "Lost"
        return "Others"

    rfm["rfm_segment"] = rfm.apply(segment, axis=1)
    rfm["customer_lifetime_days"] = (rfm["last_order"] - rfm["first_order"]).dt.days
    rfm["recency_days"] = rfm["recency_days"].astype(int)
    rfm["monetary"] = rfm["monetary"].round(2)
    rfm["avg_order_value"] = rfm["avg_order_value"].round(2)
    rfm["first_order"] = rfm["first_order"].dt.strftime("%Y-%m-%d")
    rfm["last_order"] = rfm["last_order"].dt.strftime("%Y-%m-%d")

    return rfm.merge(customers_df[["customer_id","region","acquisition_channel","age_band"]], on="customer_id", how="left")


# ── Churn Feature Table ───────────────────────────────────────────────────────

def build_churn_features(rfm_df):
    """
    Binary churn label: 1 if customer has not purchased in last 90 days.
    Features for predictive model.
    """
    df = rfm_df.copy()
    df["churned"] = (df["recency_days"] > 90).astype(int)
    df["is_high_value"] = (df["monetary"] > df["monetary"].quantile(0.75)).astype(int)
    df["is_frequent"] = (df["frequency"] >= 5).astype(int)
    df["days_since_first"] = df["customer_lifetime_days"]
    df["purchase_rate"] = (df["frequency"] / (df["days_since_first"] + 1) * 30).round(3)  # orders/month
    df["discount_shopper"] = (df["rfm_segment"].isin(["Hibernating","Lost","At Risk"])).astype(int)
    return df[[
        "customer_id","churned","recency_days","frequency","monetary",
        "avg_order_value","n_categories","customer_lifetime_days",
        "purchase_rate","is_high_value","is_frequent","r_score","f_score","m_score",
        "rfm_segment","region","acquisition_channel","age_band"
    ]]


# ── Monthly KPI Summary ───────────────────────────────────────────────────────

def build_monthly_kpis(orders_df, funnel_df):
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    monthly = orders_df.groupby(["year","month"]).agg(
        revenue         = ("revenue","sum"),
        orders          = ("order_id","count"),
        unique_customers= ("customer_id","nunique"),
        avg_order_value = ("revenue","mean"),
        repeat_orders   = ("is_repeat","sum"),
    ).reset_index()

    monthly["period"] = monthly["year"].astype(str)+"-"+monthly["month"].astype(str).str.zfill(2)
    monthly["repeat_rate_pct"] = (monthly["repeat_orders"]/monthly["orders"]*100).round(1)
    monthly["revenue"] = monthly["revenue"].round(2)
    monthly["avg_order_value"] = monthly["avg_order_value"].round(2)

    monthly = monthly.merge(
        funnel_df[["year","month","overall_conversion_rate","cart_abandonment_rate","sessions"]],
        on=["year","month"], how="left"
    )
    return monthly.sort_values(["year","month"])


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    out = "/home/claude/ecommerce-churn/data/processed"
    os.makedirs(out, exist_ok=True)

    print("Building customers...")
    customers = build_customers()
    customers.to_csv(f"{out}/customers.csv", index=False)
    print(f"  customers.csv — {len(customers)} rows")

    print("Building orders...")
    orders = build_orders(customers)
    orders.to_csv(f"{out}/orders.csv", index=False)
    print(f"  orders.csv — {len(orders)} rows")

    print("Building funnel...")
    funnel = build_funnel()
    funnel.to_csv(f"{out}/funnel.csv", index=False)
    print(f"  funnel.csv — {len(funnel)} rows")

    print("Building cohort retention...")
    cohort = build_cohort_retention(orders.copy())
    cohort.to_csv(f"{out}/cohort_retention.csv", index=False)
    print(f"  cohort_retention.csv — {len(cohort)} rows")

    print("Building RFM segmentation...")
    rfm = build_rfm(orders.copy(), customers)
    rfm.to_csv(f"{out}/rfm_segments.csv", index=False)
    print(f"  rfm_segments.csv — {len(rfm)} rows")

    print("Building churn features...")
    churn = build_churn_features(rfm.copy())
    churn.to_csv(f"{out}/churn_features.csv", index=False)
    print(f"  churn_features.csv — {len(churn)} rows")

    print("Building monthly KPIs...")
    kpis = build_monthly_kpis(orders.copy(), funnel)
    kpis.to_csv(f"{out}/monthly_kpis.csv", index=False)
    print(f"  monthly_kpis.csv — {len(kpis)} rows")

    # JSON for dashboard
    dash = {
        "funnel": funnel.to_dict(orient="records"),
        "monthly_kpis": kpis.to_dict(orient="records"),
        "rfm_summary": rfm.groupby("rfm_segment").agg(
            n_customers=("customer_id","count"),
            avg_recency=("recency_days","mean"),
            avg_frequency=("frequency","mean"),
            avg_monetary=("monetary","mean"),
            total_revenue=("monetary","sum"),
        ).reset_index().round(1).to_dict(orient="records"),
        "cohort": cohort.to_dict(orient="records"),
        "churn_summary": {
            "total_customers": len(churn),
            "churned": int(churn["churned"].sum()),
            "churn_rate": round(churn["churned"].mean()*100, 1),
            "by_segment": churn.groupby("rfm_segment")["churned"].agg(["sum","count","mean"]).reset_index().rename(columns={"sum":"churned","count":"total","mean":"churn_rate"}).round(2).to_dict(orient="records"),
            "by_channel": churn.groupby("acquisition_channel")["churned"].agg(["sum","count","mean"]).reset_index().rename(columns={"sum":"churned","count":"total","mean":"churn_rate"}).round(2).to_dict(orient="records"),
        },
        "category_revenue": orders.groupby("category")["revenue"].sum().reset_index().sort_values("revenue",ascending=False).round(2).to_dict(orient="records"),
        "channel_revenue": orders.groupby("channel")["revenue"].sum().reset_index().sort_values("revenue",ascending=False).round(2).to_dict(orient="records"),
    }
    with open(f"{out}/dashboard_data.json","w") as f:
        json.dump(dash, f, separators=(",",":"))
    print(f"  dashboard_data.json written")

    print("\n── Segment Summary ──")
    seg = rfm.groupby("rfm_segment").agg(n=("customer_id","count"),rev=("monetary","sum"),recency=("recency_days","mean")).sort_values("rev",ascending=False)
    print(seg.round(0).to_string())

    print("\n── Churn Rate by Channel ──")
    print(churn.groupby("acquisition_channel")["churned"].agg(["mean","count"]).round(3).to_string())

    print(f"\n── Funnel (Latest Month) ──")
    print(funnel.iloc[-1][["period","sessions","cart_adds","purchases","overall_conversion_rate","cart_abandonment_rate"]].to_string())


if __name__ == "__main__":
    main()
