"""
Project 03 - Report Generator
Phase 04: Functions

SKILLS PRACTICED:
  - Functions as building blocks
  - *args and **kwargs
  - Default parameters
  - Closures for configurable formatters
  - map, filter, sorted with lambdas

HOW TO RUN:
  python main.py
"""

from datetime import datetime


# ============================================================
# FORMATTING FUNCTIONS
# ============================================================

def format_currency(amount: float, symbol: str = "$", decimals: int = 2) -> str:
    return f"{symbol}{amount:,.{decimals}f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    return f"{value:.{decimals}f}%"


def make_header(title: str, width: int = 60, char: str = "=") -> str:
    border = char * width
    padded = f"  {title.upper()}"
    return f"{border}\n{padded}\n{border}"


def make_row(label: str, value: str, width: int = 40) -> str:
    return f"  {label:<{width-15}} {value:>12}"


def make_table(
    data: list[dict],
    columns: list[tuple],      # (header, key, width, align)
    title: str = ""
) -> str:
    """Generate a formatted text table."""
    lines = []
    total_width = sum(col[2] for col in columns) + len(columns) + 2

    if title:
        lines.append(f"  {title}")

    # Header row
    header = "  " + " ".join(f"{col[0]:{col[3]}{col[2]}}" for col in columns)
    lines.append(header)
    lines.append("  " + "-" * (total_width))

    # Data rows
    for row in data:
        cells = []
        for _, key, width, align in columns:
            val = row.get(key, "")
            cells.append(f"{str(val):{align}{width}}")
        lines.append("  " + " ".join(cells))

    return "\n".join(lines)


# ============================================================
# ANALYTICS FUNCTIONS
# ============================================================

def calculate_stats(values: list[float]) -> dict:
    """Calculate descriptive statistics."""
    if not values:
        return {}
    sorted_v = sorted(values)
    n = len(sorted_v)
    return {
        "count":  n,
        "sum":    round(sum(sorted_v), 2),
        "min":    sorted_v[0],
        "max":    sorted_v[-1],
        "avg":    round(sum(sorted_v) / n, 2),
        "median": sorted_v[n // 2] if n % 2 else (sorted_v[n//2-1] + sorted_v[n//2]) / 2
    }


def growth_rate(current: float, previous: float) -> float:
    """Calculate percentage growth rate."""
    if previous == 0:
        return 0.0
    return round(((current - previous) / previous) * 100, 2)


def rank_items(
    items: list[dict],
    key: str,
    reverse: bool = True,
    top_n: int = None
) -> list[dict]:
    """Rank items by a key, optionally limiting to top N."""
    ranked = sorted(items, key=lambda x: x.get(key, 0), reverse=reverse)
    if top_n:
        ranked = ranked[:top_n]
    return [{"rank": i+1, **item} for i, item in enumerate(ranked)]


# ============================================================
# REPORT SECTIONS
# ============================================================

def generate_executive_summary(data: dict) -> str:
    """Generate executive summary section."""
    lines = [make_header("EXECUTIVE SUMMARY")]
    for label, value in data.items():
        lines.append(make_row(label + ":", value))
    return "\n".join(lines)


def generate_regional_report(regions: list[dict]) -> str:
    """Generate regional breakdown."""
    lines = ["\n" + make_header("REGIONAL BREAKDOWN")]

    columns = [
        ("Region",   "region",   12, "<"),
        ("Revenue",  "revenue",  12, ">"),
        ("Units",    "units",     8, ">"),
        ("Growth%",  "growth",   10, ">"),
        ("Rank",     "rank",      5, ">"),
    ]

    ranked = rank_items(regions, "revenue")
    for r in ranked:
        r["revenue"] = format_currency(r["revenue"])
        r["growth"]  = format_percentage(r["growth"])
        r["rank"]    = f"#{r['rank']}"

    lines.append(make_table(ranked, columns))
    return "\n".join(lines)


def generate_product_report(products: list[dict]) -> str:
    """Generate top product section."""
    top = rank_items(products, "revenue", top_n=5)
    lines = ["\n" + make_header("TOP 5 PRODUCTS")]
    for p in top:
        bar = "#" * int(p["revenue"] / 5000)
        lines.append(f"  #{p['rank']} {p['name']:<20} "
                     f"{format_currency(p['revenue']):<12} {bar}")
    return "\n".join(lines)


def generate_full_report(
    title: str,
    period: str,
    executive_data: dict,
    regions: list[dict],
    products: list[dict]
) -> str:
    """Generate a complete business report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"\n{'='*60}",
        f"  {title}",
        f"  Period: {period}",
        f"  Generated: {timestamp}",
        "=" * 60,
        generate_executive_summary(executive_data),
        generate_regional_report(regions),
        generate_product_report(products),
        "\n" + "=" * 60,
        "  END OF REPORT",
        "=" * 60
    ]
    return "\n".join(lines)


# ============================================================
# MAIN
# ============================================================

def main():
    # Sample business data
    executive_summary = {
        "Total Revenue":    format_currency(2_847_500),
        "Total Expenses":   format_currency(1_923_200),
        "Net Profit":       format_currency(924_300),
        "Profit Margin":    format_percentage(32.5),
        "Total Orders":     "14,250",
        "New Customers":    "1,847",
        "YoY Growth":       format_percentage(18.3),
    }

    regions = [
        {"region": "North",  "revenue": 820000, "units": 3200, "growth": 22.5},
        {"region": "South",  "revenue": 650000, "units": 2800, "growth": 15.1},
        {"region": "East",   "revenue": 750000, "units": 3100, "growth": 19.8},
        {"region": "West",   "revenue": 627500, "units": 2900, "growth": 11.2},
    ]

    products = [
        {"name": "Laptop Pro",    "revenue": 480000, "units": 400},
        {"name": "Smart Monitor", "revenue": 320000, "units": 900},
        {"name": "Keyboard Pro",  "revenue": 185000, "units": 2300},
        {"name": "USB Hub",       "revenue": 95000,  "units": 2400},
        {"name": "Webcam HD",     "revenue": 142000, "units": 1600},
        {"name": "Desk Lamp",     "revenue": 67000,  "units": 1340},
    ]

    report = generate_full_report(
        title="QUARTERLY SALES REPORT — Q4 2024",
        period="October — December 2024",
        executive_data=executive_summary,
        regions=regions,
        products=products
    )

    print(report)

    # Optionally save to file
    save = input("\n  Save report to file? (yes/no): ").strip().lower()
    if save in ("yes", "y"):
        filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        with open(filename, "w") as f:
            f.write(report)
        print(f"  Saved to: {filename}")


if __name__ == "__main__":
    main()
