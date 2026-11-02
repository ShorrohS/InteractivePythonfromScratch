"""
Project 01 — Sales Analytics Dashboard
Phase 13: Data Analysis

SKILLS PRACTICED:
  - pandas: read CSV, filter, groupby, aggregate
  - matplotlib: bar, line, pie charts
  - Data cleaning and transformation
  - Business report generation

SETUP:
  pip install pandas matplotlib openpyxl

HOW TO RUN:
  python main.py
  (Creates sample data + charts + Excel report)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from datetime import datetime, timedelta
import random
import os


# ============================================================
# SAMPLE DATA GENERATOR
# ============================================================

def generate_sales_data(rows: int = 200) -> pd.DataFrame:
    """Generate realistic sample sales data."""
    random.seed(42)
    
    products = ["Laptop", "Monitor", "Mouse", "Keyboard", "Headset", "Webcam", "USB Hub", "Desk Lamp"]
    regions = ["North", "South", "East", "West"]
    reps = ["Alice Johnson", "Bob Smith", "Carol Davis", "Dave Wilson", "Eve Martinez"]
    
    base_prices = {
        "Laptop": 1200, "Monitor": 350, "Mouse": 35, "Keyboard": 85,
        "Headset": 120, "Webcam": 95, "USB Hub": 45, "Desk Lamp": 55
    }
    
    start_date = datetime(2024, 1, 1)
    
    records = []
    for _ in range(rows):
        product = random.choice(products)
        quantity = random.randint(1, 15)
        base_price = base_prices[product]
        unit_price = base_price * random.uniform(0.85, 1.15)
        revenue = unit_price * quantity
        cost = unit_price * random.uniform(0.55, 0.75)
        
        records.append({
            "date": start_date + timedelta(days=random.randint(0, 364)),
            "product": product,
            "region": random.choice(regions),
            "rep": random.choice(reps),
            "quantity": quantity,
            "unit_price": round(unit_price, 2),
            "revenue": round(revenue, 2),
            "cost": round(cost * quantity, 2),
        })
    
    df = pd.DataFrame(records)
    df["profit"] = df["revenue"] - df["cost"]
    df["month"] = df["date"].dt.strftime("%Y-%m")
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    return df.sort_values("date").reset_index(drop=True)


# ============================================================
# ANALYTICS FUNCTIONS
# ============================================================

def summary_stats(df: pd.DataFrame) -> dict:
    """Calculate high-level summary statistics."""
    return {
        "total_revenue": df["revenue"].sum(),
        "total_profit": df["profit"].sum(),
        "total_orders": len(df),
        "avg_order_value": df["revenue"].mean(),
        "profit_margin": df["profit"].sum() / df["revenue"].sum() * 100,
        "top_product": df.groupby("product")["revenue"].sum().idxmax(),
        "top_region": df.groupby("region")["revenue"].sum().idxmax(),
        "top_rep": df.groupby("rep")["revenue"].sum().idxmax(),
    }


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Monthly revenue and profit trend."""
    return df.groupby("month").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("revenue", "count")
    ).reset_index()


def by_product(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue and profit by product."""
    return df.groupby("product").agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        units=("quantity", "sum"),
        orders=("revenue", "count")
    ).reset_index().sort_values("revenue", ascending=False)


def by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue by region."""
    return df.groupby("region")["revenue"].sum().reset_index()


def top_reps(df: pd.DataFrame) -> pd.DataFrame:
    """Sales rep performance."""
    return df.groupby("rep").agg(
        revenue=("revenue", "sum"),
        orders=("revenue", "count"),
        avg_deal=("revenue", "mean")
    ).reset_index().sort_values("revenue", ascending=False)


# ============================================================
# VISUALIZATION
# ============================================================

def create_dashboard(df: pd.DataFrame) -> None:
    """Create a multi-panel sales dashboard."""
    
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Sales Analytics Dashboard — 2024", fontsize=16, fontweight="bold", y=0.98)
    
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.4, wspace=0.35)
    
    colors = ["#4472C4", "#ED7D31", "#A9D18E", "#FF6B6B", "#9B59B6", "#2ECC71", "#F1C40F", "#E74C3C"]
    
    # 1. Monthly Revenue Trend (top, full width)
    ax1 = fig.add_subplot(gs[0, :])
    monthly = monthly_trend(df)
    ax1.bar(monthly["month"], monthly["revenue"] / 1000, color="#4472C4", alpha=0.8, label="Revenue")
    ax1.plot(monthly["month"], monthly["profit"] / 1000, color="#ED7D31", marker="o", linewidth=2, label="Profit")
    ax1.set_title("Monthly Revenue vs Profit ($000s)")
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Amount ($000s)")
    ax1.legend()
    ax1.tick_params(axis="x", rotation=45)
    
    # 2. Revenue by Product (middle left)
    ax2 = fig.add_subplot(gs[1, :2])
    products = by_product(df)
    bars = ax2.barh(products["product"], products["revenue"] / 1000, color=colors[:len(products)])
    ax2.set_title("Revenue by Product ($000s)")
    ax2.set_xlabel("Revenue ($000s)")
    
    # 3. Revenue by Region (middle right, pie)
    ax3 = fig.add_subplot(gs[1, 2])
    regions = by_region(df)
    ax3.pie(regions["revenue"], labels=regions["region"], autopct="%1.1f%%",
            colors=colors[:len(regions)], startangle=90)
    ax3.set_title("Revenue by Region")
    
    # 4. Sales Rep Performance (bottom left)
    ax4 = fig.add_subplot(gs[2, :2])
    reps = top_reps(df)
    ax4.bar(reps["rep"], reps["revenue"] / 1000, color=colors[:len(reps)])
    ax4.set_title("Sales Rep Performance ($000s)")
    ax4.set_ylabel("Revenue ($000s)")
    ax4.tick_params(axis="x", rotation=20)
    
    # 5. KPI Summary (bottom right)
    ax5 = fig.add_subplot(gs[2, 2])
    ax5.axis("off")
    stats = summary_stats(df)
    kpi_text = (
        f"KEY PERFORMANCE INDICATORS\n\n"
        f"Total Revenue:   ${stats['total_revenue']:,.0f}\n"
        f"Total Profit:    ${stats['total_profit']:,.0f}\n"
        f"Profit Margin:   {stats['profit_margin']:.1f}%\n"
        f"Total Orders:    {stats['total_orders']:,}\n"
        f"Avg Order Value: ${stats['avg_order_value']:.0f}\n\n"
        f"Top Product: {stats['top_product']}\n"
        f"Top Region:  {stats['top_region']}\n"
        f"Top Rep:     {stats['top_rep'].split()[0]}"
    )
    ax5.text(0.05, 0.95, kpi_text, transform=ax5.transAxes, fontsize=9,
             verticalalignment="top", fontfamily="monospace",
             bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))
    
    plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
    print("  ✅ Dashboard saved: sales_dashboard.png")
    plt.show()


# ============================================================
# EXCEL REPORT
# ============================================================

def export_excel_report(df: pd.DataFrame, filename: str = "sales_report.xlsx") -> None:
    """Export analytics to Excel with multiple sheets."""
    try:
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Raw Data", index=False)
            monthly_trend(df).to_excel(writer, sheet_name="Monthly Trend", index=False)
            by_product(df).to_excel(writer, sheet_name="By Product", index=False)
            by_region(df).to_excel(writer, sheet_name="By Region", index=False)
            top_reps(df).to_excel(writer, sheet_name="Sales Reps", index=False)
        print(f"  ✅ Excel report saved: {filename}")
    except ImportError:
        print("  ⚠️  openpyxl not installed. Run: pip install openpyxl")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 55)
    print("  📊 SALES ANALYTICS DASHBOARD")
    print("=" * 55)
    
    print("\n  Generating sample sales data...")
    df = generate_sales_data(300)
    print(f"  ✅ Generated {len(df)} sales records")
    
    # Summary
    stats = summary_stats(df)
    print()
    print("  BUSINESS SUMMARY")
    print("  " + "─" * 45)
    print(f"  Total Revenue:    ${stats['total_revenue']:>12,.2f}")
    print(f"  Total Profit:     ${stats['total_profit']:>12,.2f}")
    print(f"  Profit Margin:    {stats['profit_margin']:>11.1f}%")
    print(f"  Total Orders:     {stats['total_orders']:>12,}")
    print(f"  Avg Order Value:  ${stats['avg_order_value']:>12,.2f}")
    print(f"  Top Product:      {stats['top_product']:>15}")
    print(f"  Top Region:       {stats['top_region']:>15}")
    print()
    
    # Top products table
    print("  TOP PRODUCTS BY REVENUE")
    print(f"  {'Product':<15} {'Revenue':>12} {'Units':>7} {'Margin':>8}")
    print("  " + "─" * 45)
    prods = by_product(df)
    for _, row in prods.iterrows():
        margin = row["profit"] / row["revenue"] * 100
        print(f"  {row['product']:<15} ${row['revenue']:>11,.0f} {row['units']:>7,} {margin:>7.1f}%")
    
    print()
    print("  Creating dashboard charts...")
    create_dashboard(df)
    
    print("  Exporting Excel report...")
    export_excel_report(df)
    
    print()
    print("=" * 55)
    print("  Analysis complete!")
    print("  Files created: sales_dashboard.png, sales_report.xlsx")
    print("=" * 55)


if __name__ == "__main__":
    main()
