"""
Project 03 — Payroll Processor
Phase 02: Control Flow

SKILLS PRACTICED:
  - for loops over employee data
  - Nested if/elif for tax brackets
  - Accumulating totals with running sums
  - Formatted table output

HOW TO RUN:
  python main.py
"""

# Sample employee data
EMPLOYEES = [
    {"name": "Alice Johnson",  "hours": 45, "rate": 35.00, "dept": "Engineering"},
    {"name": "Bob Smith",      "hours": 40, "rate": 28.50, "dept": "Sales"},
    {"name": "Carol Davis",    "hours": 38, "rate": 42.00, "dept": "Engineering"},
    {"name": "Dave Wilson",    "hours": 50, "rate": 25.00, "dept": "Marketing"},
    {"name": "Eve Martinez",   "hours": 40, "rate": 55.00, "dept": "Management"},
    {"name": "Frank Lee",      "hours": 35, "rate": 22.00, "dept": "Support"},
    {"name": "Grace Kim",      "hours": 42, "rate": 38.00, "dept": "Sales"},
]

TAX_BRACKETS = [
    (5000, 0.10),    # Up to $5,000 — 10%
    (15000, 0.15),   # $5,001 to $15,000 — 15%
    (float("inf"), 0.22),  # Above $15,000 — 22%
]

OVERTIME_MULTIPLIER = 1.5
STANDARD_HOURS = 40


def calculate_gross(hours: float, rate: float) -> float:
    """Calculate gross pay with overtime."""
    if hours <= STANDARD_HOURS:
        return hours * rate
    regular = STANDARD_HOURS * rate
    overtime = (hours - STANDARD_HOURS) * rate * OVERTIME_MULTIPLIER
    return regular + overtime


def calculate_tax(gross: float) -> float:
    """Calculate tax using progressive brackets."""
    if gross <= 5000:
        return gross * 0.10
    elif gross <= 15000:
        return 5000 * 0.10 + (gross - 5000) * 0.15
    else:
        return 5000 * 0.10 + 10000 * 0.15 + (gross - 15000) * 0.22


def process_payroll(employees: list) -> list:
    """Process payroll for all employees."""
    results = []
    for emp in employees:
        gross   = calculate_gross(emp["hours"], emp["rate"])
        tax     = calculate_tax(gross)
        net     = gross - tax
        overtime = max(0, emp["hours"] - STANDARD_HOURS)
        results.append({
            **emp,
            "gross":    gross,
            "tax":      tax,
            "net":      net,
            "overtime": overtime
        })
    return results


def display_payroll(results: list) -> None:
    """Display full payroll report."""
    print()
    print("=" * 80)
    print("  MONTHLY PAYROLL REPORT")
    print("=" * 80)
    print(f"  {'Name':<20} {'Dept':<12} {'Hrs':>4} {'OT':>4} "
          f"{'Gross':>10} {'Tax':>10} {'Net':>10}")
    print("  " + "-" * 74)

    totals = {"gross": 0, "tax": 0, "net": 0}

    for r in results:
        print(f"  {r['name']:<20} {r['dept']:<12} {r['hours']:>4} "
              f"{r['overtime']:>4} ${r['gross']:>9,.2f} "
              f"${r['tax']:>9,.2f} ${r['net']:>9,.2f}")
        totals["gross"] += r["gross"]
        totals["tax"]   += r["tax"]
        totals["net"]   += r["net"]

    print("  " + "-" * 74)
    print(f"  {'TOTALS':<38} ${totals['gross']:>9,.2f} "
          f"${totals['tax']:>9,.2f} ${totals['net']:>9,.2f}")
    print()

    # Department summary
    dept_totals = {}
    for r in results:
        dept = r["dept"]
        if dept not in dept_totals:
            dept_totals[dept] = {"count": 0, "gross": 0}
        dept_totals[dept]["count"] += 1
        dept_totals[dept]["gross"] += r["gross"]

    print("  DEPARTMENT SUMMARY")
    print("  " + "-" * 45)
    print(f"  {'Department':<15} {'Headcount':>10} {'Total Gross':>15}")
    print("  " + "-" * 45)
    for dept, data in sorted(dept_totals.items()):
        print(f"  {dept:<15} {data['count']:>10} ${data['gross']:>14,.2f}")

    print()
    avg_gross = totals["gross"] / len(results)
    highest = max(results, key=lambda x: x["gross"])
    print(f"  Average gross pay: ${avg_gross:,.2f}")
    print(f"  Highest earner:    {highest['name']} (${highest['gross']:,.2f})")
    print("=" * 80)


def main():
    print("=" * 80)
    print("  PAYROLL PROCESSING SYSTEM")
    print("=" * 80)
    print(f"\n  Processing {len(EMPLOYEES)} employees...")
    print(f"  Standard hours: {STANDARD_HOURS} | Overtime rate: {OVERTIME_MULTIPLIER}x")

    results = process_payroll(EMPLOYEES)
    display_payroll(results)


if __name__ == "__main__":
    main()
