"""
E-commerce Funnel & Churn Analysis — EDA & Charts
===================================================
Generates 7 charts for the portfolio.

Run:
    pip install pandas numpy matplotlib seaborn
    python 03_eda_analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import warnings, os

warnings.filterwarnings("ignore")
plt.rcParams["font.family"] = "sans-serif"

DATA = "/home/claude/ecommerce-churn/data/processed"
OUT  = "/home/claude/ecommerce-churn/outputs"
os.makedirs(OUT, exist_ok=True)

orders  = pd.read_csv(f"{DATA}/orders.csv", parse_dates=["order_date"])
funnel  = pd.read_csv(f"{DATA}/funnel.csv")
rfm     = pd.read_csv(f"{DATA}/rfm_segments.csv")
churn   = pd.read_csv(f"{DATA}/churn_features.csv")
cohort  = pd.read_csv(f"{DATA}/cohort_retention.csv")
kpis    = pd.read_csv(f"{DATA}/monthly_kpis.csv")

# ── Palette — dark editorial ──────────────────────────────────────────────────
BG      = "#0F1117"
BG2     = "#1A1D27"
CARD    = "#22263A"
ACCENT  = "#6C63FF"
GREEN   = "#00D4AA"
AMBER   = "#FFB547"
RED     = "#FF5C5C"
PINK    = "#FF6B9D"
MUTED   = "#6B7280"
TEXT    = "#E5E7EB"
TEXT2   = "#9CA3AF"

SEG_COLORS = {
    "Champions":        "#6C63FF",
    "Loyal Customers":  "#00D4AA",
    "Recent Customers": "#4FC3F7",
    "Needs Attention":  "#FFB547",
    "At Risk":          "#FF8C42",
    "Cannot Lose Them": "#FF5C5C",
    "Hibernating":      "#9CA3AF",
    "Lost":             "#4B5563",
}

def dark_style(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(BG2)
    fig = ax.get_figure()
    fig.patch.set_facecolor(BG)
    ax.spines[:].set_color("#2D3748")
    ax.tick_params(colors=TEXT2, labelsize=9)
    ax.xaxis.label.set_color(TEXT2)
    ax.yaxis.label.set_color(TEXT2)
    if title:
        ax.set_title(title, fontsize=12, fontweight="bold", color=TEXT, pad=12)
    if xlabel: ax.set_xlabel(xlabel, fontsize=9, color=TEXT2)
    if ylabel: ax.set_ylabel(ylabel, fontsize=9, color=TEXT2)
    ax.grid(axis="y", color="#2D3748", linewidth=0.5, linestyle="--")
    ax.grid(axis="x", visible=False)


# ── Chart 1: Revenue & AOV Trend ─────────────────────────────────────────────
def chart_revenue_trend():
    monthly = kpis.copy()
    monthly["period_dt"] = pd.to_datetime(monthly["period"])
    monthly = monthly.sort_values("period_dt")

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 7), facecolor=BG)
    fig.patch.set_facecolor(BG)

    # Revenue bars
    colours = [GREEN if m in [11,12] else ACCENT for m in monthly["month"]]
    ax1.bar(range(len(monthly)), monthly["revenue"]/1000, color=colours, alpha=0.85, width=0.8)
    ax1.set_facecolor(BG2)
    ax1.spines[:].set_color("#2D3748")
    ax1.tick_params(colors=TEXT2, labelsize=8)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"£{x:.0f}k"))
    ax1.set_title("Monthly Revenue 2021–2024  ·  Green = Peak Season (Nov/Dec)", fontsize=11, fontweight="bold", color=TEXT, pad=10)
    ax1.set_xticks([])
    ax1.grid(axis="y", color="#2D3748", linewidth=0.4)

    # AOV line
    ax2.plot(range(len(monthly)), monthly["avg_order_value"], color=AMBER, linewidth=2, marker="o", markersize=3)
    ax2.fill_between(range(len(monthly)), monthly["avg_order_value"], alpha=0.15, color=AMBER)
    ax2.set_facecolor(BG2)
    ax2.spines[:].set_color("#2D3748")
    ax2.tick_params(colors=TEXT2, labelsize=8)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"£{x:.0f}"))
    ax2.set_title("Average Order Value (AOV) Trend", fontsize=11, fontweight="bold", color=TEXT, pad=10)
    ticks = list(range(0, len(monthly), 6))
    ax2.set_xticks(ticks)
    ax2.set_xticklabels([monthly.iloc[i]["period"] for i in ticks], rotation=30, ha="right")
    ax2.grid(axis="y", color="#2D3748", linewidth=0.4)

    plt.tight_layout(pad=2)
    plt.savefig(f"{OUT}/01_revenue_aov_trend.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 01_revenue_aov_trend.png")


# ── Chart 2: Funnel Waterfall ─────────────────────────────────────────────────
def chart_funnel():
    latest_year = funnel[funnel["year"]==2024].mean(numeric_only=True)
    stages = ["Sessions", "PDP Views", "Cart Adds", "Checkouts", "Purchases"]
    values = [int(latest_year["sessions"]), int(latest_year["pdp_views"]),
              int(latest_year["cart_adds"]), int(latest_year["checkouts_started"]),
              int(latest_year["purchases"])]

    fig, ax = plt.subplots(figsize=(11, 6), facecolor=BG)
    ax.set_facecolor(BG2)

    colors = [ACCENT, "#8B80FF", GREEN, AMBER, PINK]
    bar_width = 0.55
    max_val = values[0]

    for i, (stage, val, col) in enumerate(zip(stages, values, colors)):
        left = (max_val - val) / 2 / max_val * 10
        width_norm = val / max_val * 10
        ax.barh(i, width_norm, left=left, height=bar_width, color=col, alpha=0.88)
        pct = f"{val/values[0]*100:.1f}%" if i > 0 else "100%"
        drop = f"  ↓ {(values[i-1]-val)/values[i-1]*100:.1f}% drop" if i > 0 else ""
        ax.text(left + width_norm/2, i, f"{val:,}  ({pct}){drop}",
                ha="center", va="center", color="white", fontsize=9, fontweight="bold")

    ax.set_yticks(range(len(stages)))
    ax.set_yticklabels(stages, color=TEXT, fontsize=11, fontweight="bold")
    ax.invert_yaxis()
    ax.set_xticks([])
    ax.spines[:].set_visible(False)
    ax.set_title("Conversion Funnel — 2024 Average Monthly Flow\nWhere are customers dropping off?",
                 fontsize=12, fontweight="bold", color=TEXT, pad=14)
    ax.grid(False)

    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(f"{OUT}/02_conversion_funnel.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 02_conversion_funnel.png")


# ── Chart 3: RFM Segment Bubble Chart ────────────────────────────────────────
def chart_rfm_segments():
    seg_stats = rfm.groupby("rfm_segment").agg(
        n=("customer_id","count"),
        avg_recency=("recency_days","mean"),
        avg_frequency=("frequency","mean"),
        avg_monetary=("monetary","mean"),
        total_rev=("monetary","sum")
    ).reset_index()

    fig, ax = plt.subplots(figsize=(11, 7), facecolor=BG)
    ax.set_facecolor(BG2)

    for _, row in seg_stats.iterrows():
        col = SEG_COLORS.get(row["rfm_segment"], MUTED)
        size = row["total_rev"] / seg_stats["total_rev"].max() * 2500
        ax.scatter(row["avg_recency"], row["avg_frequency"],
                   s=size, color=col, alpha=0.80, edgecolors="white", linewidths=0.5)
        ax.annotate(row["rfm_segment"],
                    (row["avg_recency"], row["avg_frequency"]),
                    fontsize=8.5, color=TEXT, ha="center",
                    xytext=(0, -20), textcoords="offset points", fontweight="bold")

    ax.set_xlabel("Avg Recency (days since last purchase) ← Lower = More Recent", fontsize=9, color=TEXT2)
    ax.set_ylabel("Avg Purchase Frequency (orders)", fontsize=9, color=TEXT2)
    ax.set_title("RFM Segment Map — Bubble Size = Total Segment Revenue\nIdeal: Top-Left (Recent + Frequent + High Value)",
                 fontsize=12, fontweight="bold", color=TEXT, pad=12)
    ax.invert_xaxis()
    ax.spines[:].set_color("#2D3748")
    ax.tick_params(colors=TEXT2, labelsize=9)
    ax.grid(color="#2D3748", linewidth=0.4, linestyle="--")
    fig.patch.set_facecolor(BG)

    plt.tight_layout()
    plt.savefig(f"{OUT}/03_rfm_segment_map.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 03_rfm_segment_map.png")


# ── Chart 4: Cohort Retention Heatmap ────────────────────────────────────────
def chart_cohort_heatmap():
    cohort_pivot = cohort[cohort["period_number"] <= 9].pivot_table(
        index="cohort_month", columns="period_number", values="retention_rate"
    )
    cohort_pivot = cohort_pivot.head(20)

    fig, ax = plt.subplots(figsize=(12, 8), facecolor=BG)
    im = ax.imshow(cohort_pivot.values, cmap="RdYlGn", aspect="auto", vmin=0, vmax=100)

    ax.set_xticks(range(len(cohort_pivot.columns)))
    ax.set_xticklabels([f"Month {c}" for c in cohort_pivot.columns], fontsize=8, color=TEXT2)
    ax.set_yticks(range(len(cohort_pivot.index)))
    ax.set_yticklabels(cohort_pivot.index, fontsize=8, color=TEXT2)

    for i in range(len(cohort_pivot.index)):
        for j in range(len(cohort_pivot.columns)):
            val = cohort_pivot.values[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                        fontsize=7.5, color="white" if val < 40 else "#111",
                        fontweight="bold")

    cbar = plt.colorbar(im, ax=ax, shrink=0.6, pad=0.02)
    cbar.set_label("Retention Rate (%)", color=TEXT2, fontsize=9)
    cbar.ax.yaxis.set_tick_params(color=TEXT2)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=TEXT2)

    ax.set_title("Cohort Retention Heatmap — % Still Purchasing After N Months\nRow = Acquisition Cohort · Column = Months Since First Purchase",
                 fontsize=12, fontweight="bold", color=TEXT, pad=12)
    ax.spines[:].set_visible(False)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG2)

    plt.tight_layout()
    plt.savefig(f"{OUT}/04_cohort_retention_heatmap.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 04_cohort_retention_heatmap.png")


# ── Chart 5: Churn Rate by Channel ───────────────────────────────────────────
def chart_churn_by_channel():
    ch_churn = churn.groupby("acquisition_channel").agg(
        total=("churned","count"), churned=("churned","sum")
    ).reset_index()
    ch_churn["churn_rate"] = ch_churn["churned"] / ch_churn["total"] * 100
    ch_churn = ch_churn.sort_values("churn_rate", ascending=True)

    ch_rev = rfm.groupby("acquisition_channel")["monetary"].mean().reset_index()
    ch_rev.columns = ["acquisition_channel", "avg_ltv"]
    ch_churn = ch_churn.merge(ch_rev, on="acquisition_channel")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

    col1 = [RED if v > ch_churn["churn_rate"].median() else GREEN for v in ch_churn["churn_rate"]]
    bars = ax1.barh(ch_churn["acquisition_channel"], ch_churn["churn_rate"],
                    color=col1, height=0.6, alpha=0.88)
    for bar, val in zip(bars, ch_churn["churn_rate"]):
        ax1.text(val+0.5, bar.get_y()+bar.get_height()/2,
                 f"{val:.1f}%", va="center", fontsize=9, color=TEXT, fontweight="bold")
    dark_style(ax1, title="Churn Rate by Acquisition Channel\nWhich channels retain customers best?",
               xlabel="Churn Rate (%)")
    ax1.set_xlim(0, 80)

    col2 = [ACCENT for _ in ch_churn["acquisition_channel"]]
    bars2 = ax2.barh(ch_churn["acquisition_channel"], ch_churn["avg_ltv"],
                     color=col2, height=0.6, alpha=0.88)
    for bar, val in zip(bars2, ch_churn["avg_ltv"]):
        ax2.text(val+5, bar.get_y()+bar.get_height()/2,
                 f"£{val:.0f}", va="center", fontsize=9, color=TEXT, fontweight="bold")
    dark_style(ax2, title="Average LTV by Acquisition Channel\nHigher LTV = more valuable customer segment",
               xlabel="Avg Customer Lifetime Revenue (£)")

    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(f"{OUT}/05_churn_by_channel.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 05_churn_by_channel.png")


# ── Chart 6: Category Revenue & AOV ──────────────────────────────────────────
def chart_category_revenue():
    cat = orders.groupby("category").agg(
        revenue=("revenue","sum"),
        orders=("order_id","count"),
        aov=("revenue","mean"),
        customers=("customer_id","nunique")
    ).reset_index().sort_values("revenue", ascending=False)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), facecolor=BG)

    cmap_colors = [ACCENT, GREEN, AMBER, PINK, RED, "#4FC3F7", "#A78BFA"]
    ax1.bar(cat["category"], cat["revenue"]/1000, color=cmap_colors, alpha=0.88, width=0.65)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"£{x:.0f}k"))
    dark_style(ax1, title="Total Revenue by Category", ylabel="Revenue (£k)")
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=9)

    ax2.scatter(cat["aov"], cat["customers"], s=[r/50 for r in cat["revenue"]],
                color=cmap_colors, alpha=0.85, edgecolors="white", linewidths=0.5)
    for _, row in cat.iterrows():
        ax2.annotate(row["category"], (row["aov"], row["customers"]),
                     fontsize=8, color=TEXT2, xytext=(5, 5), textcoords="offset points")
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"£{x:.0f}"))
    dark_style(ax2, title="AOV vs Unique Buyers\nBubble size = total revenue",
               xlabel="Average Order Value (£)", ylabel="Unique Buyers")

    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(f"{OUT}/06_category_revenue.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 06_category_revenue.png")


# ── Chart 7: Retention Strategy — Segment Action Matrix ──────────────────────
def chart_retention_strategy():
    seg_data = churn.groupby("rfm_segment").agg(
        n=("churned","count"),
        churn_rate=("churned","mean"),
        avg_rev=("monetary","mean"),
        avg_recency=("recency_days","mean")
    ).reset_index()
    seg_data["churn_rate"] *= 100

    action_map = {
        "Champions":        ("Reward & Upsell",      GREEN),
        "Loyal Customers":  ("Cross-sell",            ACCENT),
        "Recent Customers": ("Onboard & Nurture",     "#4FC3F7"),
        "Needs Attention":  ("Re-engage Now",         AMBER),
        "At Risk":          ("Win-back Campaign",     "#FF8C42"),
        "Cannot Lose Them": ("Priority Outreach",     RED),
        "Hibernating":      ("Reactivation Email",    MUTED),
        "Lost":             ("Sunset / Re-acquire",   "#4B5563"),
    }

    fig, ax = plt.subplots(figsize=(11, 7), facecolor=BG)
    ax.set_facecolor(BG2)

    for _, row in seg_data.iterrows():
        label, col = action_map.get(row["rfm_segment"], ("Other", MUTED))
        size = row["n"] * 8
        ax.scatter(row["churn_rate"], row["avg_rev"], s=size, color=col, alpha=0.85,
                   edgecolors="white", linewidths=0.5)
        ax.annotate(f'{row["rfm_segment"]}\n→ {label}',
                    (row["churn_rate"], row["avg_rev"]),
                    fontsize=8, color=TEXT, ha="center",
                    xytext=(0, 14), textcoords="offset points", fontweight="bold")

    ax.axhline(seg_data["avg_rev"].median(), color=MUTED, linewidth=0.8, linestyle="--", alpha=0.5)
    ax.axvline(seg_data["churn_rate"].median(), color=MUTED, linewidth=0.8, linestyle="--", alpha=0.5)
    ax.text(seg_data["churn_rate"].max()*0.05, seg_data["avg_rev"].max()*0.98,
            "HIGH VALUE\nLOW CHURN\n→ Retain & grow", fontsize=8, color=GREEN, alpha=0.7, fontweight="bold")
    ax.text(seg_data["churn_rate"].max()*0.65, seg_data["avg_rev"].max()*0.98,
            "HIGH VALUE\nHIGH CHURN\n→ Priority win-back", fontsize=8, color=RED, alpha=0.7, fontweight="bold")

    ax.set_xlabel("Churn Rate (%)", fontsize=9, color=TEXT2)
    ax.set_ylabel("Average Customer Lifetime Revenue (£)", fontsize=9, color=TEXT2)
    ax.set_title("Retention Strategy Matrix — Bubble Size = Segment Size\nPrioritise: High Value + High Churn = most urgent action",
                 fontsize=12, fontweight="bold", color=TEXT, pad=12)
    ax.spines[:].set_color("#2D3748")
    ax.tick_params(colors=TEXT2, labelsize=9)
    ax.grid(color="#2D3748", linewidth=0.4, linestyle="--")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"£{x:.0f}"))
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x,_: f"{x:.0f}%"))
    fig.patch.set_facecolor(BG)

    plt.tight_layout()
    plt.savefig(f"{OUT}/07_retention_strategy_matrix.png", dpi=150, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  Saved: 07_retention_strategy_matrix.png")


if __name__ == "__main__":
    print("Generating e-commerce analysis charts...\n")
    chart_revenue_trend()
    chart_funnel()
    chart_rfm_segments()
    chart_cohort_heatmap()
    chart_churn_by_channel()
    chart_category_revenue()
    chart_retention_strategy()
    print(f"\nAll 7 charts saved to {OUT}/")
