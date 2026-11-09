# ✅ Phase 18 — Advanced Solutions

> Each solution is a complete, runnable application.
> Study the module structure, menu loop patterns, and how business logic is
> separated from persistence (load/save) and presentation (print formatting).

---

## Solution Q1 — Invoice Management CLI

```python
"""
invoice_manager.py — CLI tool for creating and tracking client invoices.

Persist: invoices.json
Run:     python invoice_manager.py
"""

import json
import datetime
import sys
from pathlib import Path

DATA_FILE = Path("invoices.json")


# ── Persistence ────────────────────────────────────────────────────────────────

def load() -> list[dict]:
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def save(invoices: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(invoices, indent=2), encoding="utf-8")


def next_id(invoices: list[dict]) -> int:
    return max((i["id"] for i in invoices), default=0) + 1


# ── Business logic ──────────────────────────────────────────────────────────────

def invoice_status(inv: dict) -> str:
    if inv["paid"]:
        return "Paid"
    due = datetime.date.fromisoformat(inv["due_date"])
    return "OVERDUE" if due < datetime.date.today() else "Unpaid"


def create_invoice(invoices: list[dict]) -> None:
    client      = input("  Client name: ").strip()
    description = input("  Description: ").strip()

    try:
        amount = float(input("  Amount: ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  Error: amount must be a positive number")
        return

    due_date = input("  Due date (YYYY-MM-DD): ").strip()
    try:
        datetime.date.fromisoformat(due_date)
    except ValueError:
        print("  Error: date must be YYYY-MM-DD")
        return

    inv = {
        "id":           next_id(invoices),
        "client":       client,
        "description":  description,
        "amount":       round(amount, 2),
        "due_date":     due_date,
        "issued_date":  datetime.date.today().isoformat(),
        "paid":         False,
        "paid_date":    None,
    }
    invoices.append(inv)
    save(invoices)
    print(f"  ✓ Invoice #{inv['id']} created for {client}")


def list_invoices(invoices: list[dict]) -> None:
    if not invoices:
        print("  No invoices.")
        return
    hdr = f"  {'ID':<4} {'Client':<20} {'Description':<30} {'Amount':>10}  {'Due Date':<12} {'Status'}"
    print(hdr)
    print("  " + "-" * 90)
    for inv in sorted(invoices, key=lambda i: i["id"]):
        status = invoice_status(inv)
        print(
            f"  {inv['id']:<4} {inv['client']:<20} {inv['description']:<30}"
            f" ${inv['amount']:>9,.2f}  {inv['due_date']:<12} {status}"
        )


def mark_paid(invoices: list[dict]) -> None:
    try:
        inv_id = int(input("  Invoice ID to mark paid: ").strip())
    except ValueError:
        print("  Error: ID must be a number")
        return

    for inv in invoices:
        if inv["id"] == inv_id:
            if inv["paid"]:
                print(f"  Invoice #{inv_id} is already paid.")
                return
            inv["paid"]      = True
            inv["paid_date"] = datetime.date.today().isoformat()
            save(invoices)
            print(f"  ✓ Invoice #{inv_id} marked as paid.")
            return
    print(f"  Invoice #{inv_id} not found.")


def monthly_summary(invoices: list[dict]) -> None:
    month = input("  Month (YYYY-MM): ").strip()
    relevant = [i for i in invoices if i["issued_date"][:7] == month]
    if not relevant:
        print(f"  No invoices found for {month}.")
        return

    total_amount = sum(i["amount"] for i in relevant)
    paid_invs    = [i for i in relevant if i["paid"]]
    overdue_invs = [i for i in relevant if not i["paid"] and
                    datetime.date.fromisoformat(i["due_date"]) < datetime.date.today()]

    paid_amount    = sum(i["amount"] for i in paid_invs)
    overdue_amount = sum(i["amount"] for i in overdue_invs)

    month_label = datetime.datetime.strptime(month, "%Y-%m").strftime("%B %Y")
    print(f"\n  Monthly Summary — {month_label}")
    print(f"  Invoiced:    ${total_amount:>10,.2f}  ({len(relevant)} invoice(s))")
    print(f"  Paid:        ${paid_amount:>10,.2f}  ({len(paid_invs)} invoice(s))")
    print(f"  Overdue:     ${overdue_amount:>10,.2f}  ({len(overdue_invs)} invoice(s))")
    print(f"  Outstanding: ${total_amount - paid_amount:>10,.2f}")


# ── Menu ────────────────────────────────────────────────────────────────────────

def main() -> None:
    invoices = load()
    while True:
        print("\nInvoice Manager")
        print("  1. Create invoice")
        print("  2. List invoices")
        print("  3. Mark invoice paid")
        print("  4. Monthly summary")
        print("  5. Exit")
        choice = input("Choice: ").strip()

        if   choice == "1": create_invoice(invoices)
        elif choice == "2": list_invoices(invoices)
        elif choice == "3": mark_paid(invoices)
        elif choice == "4": monthly_summary(invoices)
        elif choice == "5": print("Goodbye."); break
        else:               print("  Enter 1–5")


if __name__ == "__main__":
    main()
```

---

## Solution Q2 — Employee Attendance System

```python
"""
attendance.py — Track employee clock-in/clock-out times with daily and weekly reports.

Persist: attendance.json
Run:     python attendance.py
"""

import json
import datetime
import csv
from pathlib import Path

DATA_FILE = Path("attendance.json")
DAILY_OT_HOURS  = 8.0
WEEKLY_OT_HOURS = 40.0


# ── Persistence ─────────────────────────────────────────────────────────────────

def load() -> list[dict]:
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []


def save(records: list[dict]) -> None:
    DATA_FILE.write_text(json.dumps(records, indent=2), encoding="utf-8")


def next_id(records: list[dict]) -> int:
    return max((r["id"] for r in records), default=0) + 1


# ── Business logic ───────────────────────────────────────────────────────────────

def calc_hours(clock_in: str, clock_out: str) -> float:
    fmt = "%H:%M"
    start = datetime.datetime.strptime(clock_in,  fmt)
    end   = datetime.datetime.strptime(clock_out, fmt)
    delta = end - start
    return round(delta.seconds / 3600, 2)


def clock_in(records: list[dict]) -> None:
    emp_id = input("  Employee ID: ").strip().upper()
    now    = datetime.datetime.now()
    date   = now.date().isoformat()
    time   = now.strftime("%H:%M")

    # Check not already clocked in today
    open_record = next((r for r in records
                        if r["employee_id"] == emp_id and r["date"] == date and r.get("clock_out") is None), None)
    if open_record:
        print(f"  {emp_id} is already clocked in at {open_record['clock_in']}.")
        return

    records.append({
        "id":          next_id(records),
        "employee_id": emp_id,
        "date":        date,
        "clock_in":    time,
        "clock_out":   None,
        "hours":       None,
    })
    save(records)
    print(f"  {emp_id} clocked IN at {time} on {date}")


def clock_out(records: list[dict]) -> None:
    emp_id = input("  Employee ID: ").strip().upper()
    now    = datetime.datetime.now()
    date   = now.date().isoformat()
    time   = now.strftime("%H:%M")

    open_record = next((r for r in records
                        if r["employee_id"] == emp_id and r["date"] == date and r.get("clock_out") is None), None)
    if not open_record:
        print(f"  {emp_id} is not clocked in today.")
        return

    open_record["clock_out"] = time
    open_record["hours"]     = calc_hours(open_record["clock_in"], time)
    save(records)
    print(f"  {emp_id} clocked OUT at {time} — {open_record['hours']:.2f} hours today")


def daily_summary(records: list[dict]) -> None:
    date = input("  Date (YYYY-MM-DD): ").strip()
    day_records = [r for r in records if r["date"] == date and r["clock_out"]]
    if not day_records:
        print(f"  No completed records for {date}.")
        return

    print(f"\n  Daily Summary — {date}")
    print(f"  {'Employee':<12} {'Clock In':<10} {'Clock Out':<11} {'Hours':>6}  {'Overtime'}")
    print("  " + "-" * 55)
    for r in sorted(day_records, key=lambda x: x["employee_id"]):
        ot = r["hours"] - DAILY_OT_HOURS
        ot_str = f"{ot:.2f} hrs" if ot > 0 else "—"
        print(f"  {r['employee_id']:<12} {r['clock_in']:<10} {r['clock_out']:<11} {r['hours']:>6.2f}  {ot_str}")


def weekly_report(records: list[dict]) -> None:
    date_str = input("  Any date in the target week (YYYY-MM-DD): ").strip()
    try:
        anchor = datetime.date.fromisoformat(date_str)
    except ValueError:
        print("  Invalid date format.")
        return

    # Monday–Sunday of the target week
    monday = anchor - datetime.timedelta(days=anchor.weekday())
    sunday = monday + datetime.timedelta(days=6)
    week_dates = {(monday + datetime.timedelta(days=i)).isoformat() for i in range(7)}

    week_records = [r for r in records if r["date"] in week_dates and r["clock_out"]]

    # Sum hours per employee
    totals: dict[str, float] = {}
    for r in week_records:
        totals[r["employee_id"]] = totals.get(r["employee_id"], 0.0) + r["hours"]

    if not totals:
        print("  No records for that week.")
        return

    print(f"\n  Weekly Report — Week of {monday.isoformat()}")
    print(f"  {'Employee':<12} {'Total Hrs':>10}  {'Overtime Hrs'}")
    print("  " + "-" * 40)
    for emp, total in sorted(totals.items()):
        ot = max(0.0, total - WEEKLY_OT_HOURS)
        ot_str = f"{ot:.2f}" if ot > 0 else "—"
        print(f"  {emp:<12} {total:>10.2f}  {ot_str}")


def export_csv(records: list[dict]) -> None:
    out = Path("attendance_export.csv")
    complete = [r for r in records if r["clock_out"]]
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id","employee_id","date","clock_in","clock_out","hours"])
        writer.writeheader()
        writer.writerows(complete)
    print(f"  ✓ Exported {len(complete)} records to {out.resolve()}")


def main() -> None:
    records = load()
    while True:
        print("\nAttendance System")
        print("  1. Clock in")
        print("  2. Clock out")
        print("  3. Daily summary")
        print("  4. Weekly report")
        print("  5. Export to CSV")
        print("  6. Exit")
        choice = input("Choice: ").strip()

        if   choice == "1": clock_in(records)
        elif choice == "2": clock_out(records)
        elif choice == "3": daily_summary(records)
        elif choice == "4": weekly_report(records)
        elif choice == "5": export_csv(records)
        elif choice == "6": print("Goodbye."); break
        else:               print("  Enter 1–6")


if __name__ == "__main__":
    main()
```

---

## Solution Q3 — Budget Tracker with Alerts

```python
"""
budget_tracker.py — Track departmental spending against monthly budgets with alerts.

Persist: budget_data.json
Run:     python budget_tracker.py
"""

import json
import datetime
from pathlib import Path

DATA_FILE    = Path("budget_data.json")
ALERT_THRESH = 0.80   # 80% usage triggers a warning alert


# ── Persistence ─────────────────────────────────────────────────────────────────

def load() -> dict:
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"departments": [], "transactions": []}


def save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def next_tx_id(data: dict) -> int:
    txns = data["transactions"]
    return max((t["id"] for t in txns), default=0) + 1


# ── Business logic ───────────────────────────────────────────────────────────────

def month_spend(data: dict, dept_name: str, month: str) -> float:
    return sum(
        t["amount"]
        for t in data["transactions"]
        if t["department"] == dept_name and t["date"][:7] == month
    )


def check_alerts(data: dict, month: str) -> None:
    for dept in data["departments"]:
        budget = dept["monthly_budget"]
        spent  = month_spend(data, dept["name"], month)
        pct    = (spent / budget * 100) if budget else 0
        if pct >= ALERT_THRESH * 100:
            marker = "🔴 OVER BUDGET" if spent > budget else "⚠️  BUDGET ALERT"
            print(f"\n  {marker}: {dept['name']} has used ${spent:,.2f} of ${budget:,.2f} ({pct:.1f}%) this month")


def add_department(data: dict) -> None:
    name = input("  Department name: ").strip()
    if any(d["name"] == name for d in data["departments"]):
        print(f"  Department '{name}' already exists.")
        return
    try:
        budget = float(input("  Monthly budget ($): ").strip())
    except ValueError:
        print("  Invalid amount.")
        return
    data["departments"].append({"name": name, "monthly_budget": round(budget, 2)})
    save(data)
    print(f"  ✓ Added department '{name}' with budget ${budget:,.2f}/month")


def record_transaction(data: dict) -> None:
    dept_names = [d["name"] for d in data["departments"]]
    if not dept_names:
        print("  No departments set up yet. Add one first.")
        return

    print(f"  Departments: {', '.join(dept_names)}")
    dept = input("  Department: ").strip()
    if dept not in dept_names:
        print(f"  Unknown department '{dept}'.")
        return

    try:
        amount = float(input("  Amount ($): ").strip())
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  Amount must be a positive number.")
        return

    desc  = input("  Description: ").strip()
    date  = input("  Date (YYYY-MM-DD, Enter = today): ").strip()
    if not date:
        date = datetime.date.today().isoformat()
    else:
        try:
            datetime.date.fromisoformat(date)
        except ValueError:
            print("  Invalid date.")
            return

    txn = {"id": next_tx_id(data), "date": date, "department": dept,
           "amount": round(amount, 2), "description": desc}
    data["transactions"].append(txn)
    save(data)
    print(f"  ✓ Recorded ${amount:,.2f} to {dept}")
    check_alerts(data, date[:7])


def variance_report(data: dict) -> None:
    month = input("  Month (YYYY-MM): ").strip()
    if not data["departments"]:
        print("  No departments configured.")
        return

    print(f"\n  Budget Variance Report — {month}")
    print(f"  {'Department':<15} {'Budget':>12} {'Actual':>12} {'Variance':>12}  {'% Used':>7}")
    print("  " + "-" * 65)
    for dept in sorted(data["departments"], key=lambda d: d["name"]):
        budget   = dept["monthly_budget"]
        actual   = month_spend(data, dept["name"], month)
        variance = budget - actual
        pct      = (actual / budget * 100) if budget else 0
        flag     = "  🔴 OVER BUDGET" if actual > budget else ("  ⚠️ OVER 80%" if pct >= 80 else "")
        v_str    = f"+${variance:,.2f}" if variance >= 0 else f"-${abs(variance):,.2f}"
        print(f"  {dept['name']:<15} ${budget:>10,.2f} ${actual:>10,.2f} {v_str:>12}  {pct:>6.1f}%{flag}")


def list_transactions(data: dict) -> None:
    dept  = input("  Department: ").strip()
    month = input("  Month (YYYY-MM, Enter = all): ").strip()
    txns  = [t for t in data["transactions"]
             if t["department"] == dept and (not month or t["date"][:7] == month)]
    if not txns:
        print("  No transactions found.")
        return
    for t in sorted(txns, key=lambda x: x["date"]):
        print(f"  [{t['date']}] #{t['id']:>3}  ${t['amount']:>9,.2f}  {t['description']}")
    print(f"  Total: ${sum(t['amount'] for t in txns):,.2f}")


def main() -> None:
    data = load()
    while True:
        print("\nBudget Tracker")
        print("  1. Add department")
        print("  2. Record transaction")
        print("  3. Variance report")
        print("  4. List transactions")
        print("  5. Exit")
        choice = input("Choice: ").strip()

        if   choice == "1": add_department(data)
        elif choice == "2": record_transaction(data)
        elif choice == "3": variance_report(data)
        elif choice == "4": list_transactions(data)
        elif choice == "5": print("Goodbye."); break
        else:               print("  Enter 1–5")


if __name__ == "__main__":
    main()
```

---

## Solution Q4 — Sales Performance Reporter (CSV → HTML)

```python
"""
sales_reporter.py — Read a sales CSV and generate a self-contained HTML report.

Usage: python sales_reporter.py sales_2024.csv [sales_2023.csv]
"""

import csv
import sys
import datetime
from pathlib import Path
from collections import defaultdict

HTML_OUT = Path("sales_report.html")


def read_sales(path: Path) -> list[dict]:
    """Read and parse a sales CSV file, coercing amount to float."""
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)
    rows = []
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["amount"] = float(row["amount"])
            rows.append(row)
    return rows


def compute_metrics(sales: list[dict]) -> dict:
    total    = sum(s["amount"] for s in sales)
    count    = len(sales)
    average  = total / count if count else 0.0

    by_rep: dict[str, float] = defaultdict(float)
    by_month: dict[str, float] = defaultdict(float)
    by_cat: dict[str, float] = defaultdict(float)

    for s in sales:
        by_rep[s["rep"]]          += s["amount"]
        by_month[s["date"][:7]]   += s["amount"]
        by_cat[s["category"]]     += s["amount"]

    top_rep   = max(by_rep,   key=by_rep.get)   if by_rep   else "—"
    best_month= max(by_month, key=by_month.get) if by_month else "—"

    return {
        "total": total, "count": count, "average": average,
        "top_rep": top_rep, "top_rep_total": by_rep.get(top_rep, 0),
        "best_month": best_month, "best_month_total": by_month.get(best_month, 0),
        "by_rep":   dict(sorted(by_rep.items(),   key=lambda x: -x[1])),
        "by_cat":   dict(sorted(by_cat.items(),   key=lambda x: -x[1])),
        "by_month": dict(sorted(by_month.items())),
    }


def table_rows(data: dict[str, float], currency: bool = True) -> str:
    rows = ""
    for key, val in data.items():
        fmt = f"${val:,.2f}" if currency else str(val)
        rows += f"<tr><td>{key}</td><td>{fmt}</td></tr>\n"
    return rows


def generate_html(metrics: dict, yoy: float | None, source_file: str) -> str:
    generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    yoy_section = ""
    if yoy is not None:
        direction = "▲" if yoy >= 0 else "▼"
        color     = "green" if yoy >= 0 else "red"
        yoy_section = f"<p>Year-on-Year Change: <b style='color:{color}'>{direction} {abs(yoy):.1f}%</b></p>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Sales Performance Report</title>
<style>
  body  {{ font-family: Arial, sans-serif; margin: 40px; color: #333; }}
  h1    {{ color: #1a5276; }}
  h2    {{ color: #2874a6; border-bottom: 1px solid #aed6f1; padding-bottom: 4px; }}
  table {{ border-collapse: collapse; margin-bottom: 20px; min-width: 300px; }}
  th, td{{ border: 1px solid #d6eaf8; padding: 8px 14px; text-align: left; }}
  th    {{ background: #2874a6; color: white; }}
  tr:nth-child(even) {{ background: #ebf5fb; }}
  .footer {{ font-size: 0.85em; color: #999; margin-top: 30px; }}
</style>
</head>
<body>
<h1>Sales Performance Report</h1>
<p>Source: <em>{source_file}</em> &nbsp;|&nbsp; Generated: {generated}</p>
{yoy_section}

<h2>Key Metrics</h2>
<table>
  <tr><th>Metric</th><th>Value</th></tr>
  <tr><td>Total Revenue</td><td>${metrics['total']:,.2f}</td></tr>
  <tr><td>Transactions</td><td>{metrics['count']}</td></tr>
  <tr><td>Average Deal Size</td><td>${metrics['average']:,.2f}</td></tr>
  <tr><td>Top Performer</td><td>{metrics['top_rep']} (${metrics['top_rep_total']:,.2f})</td></tr>
  <tr><td>Best Month</td><td>{metrics['best_month']} (${metrics['best_month_total']:,.2f})</td></tr>
</table>

<h2>Revenue by Category</h2>
<table>
  <tr><th>Category</th><th>Total</th></tr>
  {table_rows(metrics['by_cat'])}
</table>

<h2>Revenue by Sales Rep</h2>
<table>
  <tr><th>Rep</th><th>Total</th></tr>
  {table_rows(metrics['by_rep'])}
</table>

<div class="footer">Generated by sales_reporter.py &mdash; Python Mastery Academy Phase 18</div>
</body>
</html>"""


def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python {Path(__file__).name} <current_year.csv> [prior_year.csv]")
        sys.exit(1)

    current_file = Path(sys.argv[1])
    prior_file   = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    print(f"Reading sales data from {current_file}...")
    current_sales = read_sales(current_file)
    metrics       = compute_metrics(current_sales)

    print(f"  {metrics['count']} transactions loaded")
    print(f"  Total revenue: ${metrics['total']:,.2f}")
    print(f"  Top performer: {metrics['top_rep']} (${metrics['top_rep_total']:,.2f})")
    print(f"  Best month:    {metrics['best_month']} (${metrics['best_month_total']:,.2f})")

    yoy = None
    if prior_file:
        prior_sales   = read_sales(prior_file)
        prior_metrics = compute_metrics(prior_sales)
        if prior_metrics["total"]:
            yoy = (metrics["total"] - prior_metrics["total"]) / prior_metrics["total"] * 100

    html = generate_html(metrics, yoy, current_file.name)
    HTML_OUT.write_text(html, encoding="utf-8")
    print(f"Report written to: {HTML_OUT.resolve()}")


if __name__ == "__main__":
    main()
```

---

## Solution Q5 — Inventory Reorder System

```python
"""
inventory_reorder.py — Manage stock levels and auto-generate purchase orders when stock is low.

Persist: inventory.json, purchase_orders.json
Run:     python inventory_reorder.py
"""

import json
import datetime
from pathlib import Path
from collections import defaultdict

INV_FILE = Path("inventory.json")
PO_FILE  = Path("purchase_orders.json")


# ── Persistence ─────────────────────────────────────────────────────────────────

def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return default


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ── Business logic ───────────────────────────────────────────────────────────────

def needs_reorder(product: dict) -> bool:
    return product["stock"] < product["reorder_point"]


def po_number(sequence: int) -> str:
    today = datetime.date.today().strftime("%Y%m%d")
    return f"PO-{today}-{sequence:03d}"


def generate_purchase_orders(inventory: list[dict], existing_pos: list[dict]) -> list[dict]:
    """Create one PO per supplier for all products that need reordering."""
    under_stock = [p for p in inventory if needs_reorder(p)]
    if not under_stock:
        return []

    # Group items by supplier
    by_supplier: dict[str, list[dict]] = defaultdict(list)
    for p in under_stock:
        by_supplier[p["supplier"]].append(p)

    new_pos: list[dict] = []
    seq_start = len(existing_pos) + 1

    for idx, (supplier, products) in enumerate(by_supplier.items()):
        items = []
        total_value = 0.0
        for p in products:
            qty   = p["reorder_point"] * 2   # order twice the threshold
            total = round(qty * p["unit_cost"], 2)
            items.append({
                "sku":       p["sku"],
                "name":      p["name"],
                "quantity":  qty,
                "unit_cost": p["unit_cost"],
                "total":     total,
            })
            total_value += total

        delivery = (datetime.date.today() + datetime.timedelta(days=7)).isoformat()
        po = {
            "po_number":           po_number(seq_start + idx),
            "generated_date":      datetime.date.today().isoformat(),
            "estimated_delivery":  delivery,
            "supplier":            supplier,
            "supplier_email":      products[0]["supplier_email"],
            "items":               items,
            "total_value":         round(total_value, 2),
            "status":              "pending",
        }
        new_pos.append(po)

    return new_pos


def print_purchase_order(po: dict) -> None:
    width = 54
    print("\n" + "=" * width)
    print(f"PURCHASE ORDER: {po['po_number']}")
    print(f"Generated:  {po['generated_date']}")
    print("=" * width)
    print(f"To: {po['supplier_email']} ({po['supplier']})")
    print("\nPlease supply the following items:\n")
    print(f"  {'SKU':<14} {'Description':<22} {'Qty':>5}  {'Unit Cost':>10}  {'Total':>10}")
    print("  " + "-" * 65)
    for item in po["items"]:
        print(
            f"  {item['sku']:<14} {item['name']:<22} {item['quantity']:>5}"
            f"  ${item['unit_cost']:>9.2f}  ${item['total']:>9.2f}"
        )
    print("  " + "-" * 65)
    print(f"  {'ORDER TOTAL:':<40} ${po['total_value']:>9.2f}")
    print(f"\nEstimated Delivery: {po['estimated_delivery']}")
    print("=" * width)


def update_stock(inventory: list[dict]) -> list[dict]:
    """Ask user to update stock; return any new purchase orders if reorder triggered."""
    sku_map = {p["sku"]: p for p in inventory}

    print("\n  Current inventory:")
    for p in inventory:
        flag = "  ⚠️ BELOW REORDER POINT" if needs_reorder(p) else ""
        print(f"    {p['sku']:<14} {p['name']:<22} stock={p['stock']:>4}  reorder@{p['reorder_point']}{flag}")

    sku = input("\n  SKU to update: ").strip().upper()
    if sku not in sku_map:
        print(f"  SKU '{sku}' not found.")
        return []

    print("  Enter positive number for received shipment, negative for sale/usage:")
    try:
        change = int(input("  Quantity change: ").strip())
    except ValueError:
        print("  Must be a whole number.")
        return []

    product = sku_map[sku]
    old_stock = product["stock"]
    product["stock"] = max(0, old_stock + change)
    save_json(INV_FILE, inventory)
    print(f"  ✓ {product['name']}: {old_stock} → {product['stock']}")

    if needs_reorder(product):
        print(f"\n  ⚠️  {product['name']} is below reorder point ({product['reorder_point']}). Generating PO...")
        existing = load_json(PO_FILE, [])
        new_pos = generate_purchase_orders(inventory, existing)
        if new_pos:
            existing.extend(new_pos)
            save_json(PO_FILE, existing)
            for po in new_pos:
                print_purchase_order(po)
        return new_pos

    return []


def main() -> None:
    inventory = load_json(INV_FILE, [])

    if not inventory:
        print("No inventory found. Loading seed data...")
        inventory = [
            {"sku": "LAPTOP-001", "name": "Business Laptop",  "supplier": "TechSupply Co",
             "supplier_email": "orders@techsupply.com",  "stock": 8,  "reorder_point": 10, "unit_cost": 899.00},
            {"sku": "MOUSE-002",  "name": "Wireless Mouse",   "supplier": "TechSupply Co",
             "supplier_email": "orders@techsupply.com",  "stock": 45, "reorder_point": 20, "unit_cost":  24.99},
            {"sku": "DESK-003",   "name": "Standing Desk",    "supplier": "OfficeFurn Ltd",
             "supplier_email": "orders@officefurn.com",  "stock": 3,  "reorder_point": 5,  "unit_cost": 450.00},
            {"sku": "CHAIR-004",  "name": "Ergonomic Chair",  "supplier": "OfficeFurn Ltd",
             "supplier_email": "orders@officefurn.com",  "stock": 12, "reorder_point": 8,  "unit_cost": 320.00},
        ]
        save_json(INV_FILE, inventory)

    while True:
        print("\nInventory Reorder System")
        print("  1. View inventory")
        print("  2. Update stock / record sale")
        print("  3. View pending purchase orders")
        print("  4. Exit")
        choice = input("Choice: ").strip()

        if choice == "1":
            for p in inventory:
                flag = " ⚠️" if needs_reorder(p) else ""
                print(f"  {p['sku']:<14} {p['name']:<22} stock={p['stock']:>4}  reorder@{p['reorder_point']}{flag}")

        elif choice == "2":
            update_stock(inventory)

        elif choice == "3":
            pos = load_json(PO_FILE, [])
            if not pos:
                print("  No purchase orders on file.")
            else:
                for po in pos:
                    print(f"  {po['po_number']}  {po['supplier']:<20} ${po['total_value']:>10,.2f}  [{po['status']}]")

        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("  Enter 1–4")


if __name__ == "__main__":
    main()
```

---

> **Exercises:** → [../../exercises/advanced/exercises.md](../../exercises/advanced/exercises.md)
