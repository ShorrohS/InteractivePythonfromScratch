"""
Expense Management Application
Phase 18: Business Projects

End-to-end business application with:
  - SQLite database
  - Budget management
  - Category reporting
  - Monthly trend analysis
  - CSV export

HOW TO RUN:
  python main.py
"""

import sqlite3
import csv
from datetime import datetime, date
from pathlib import Path
from collections import defaultdict

DB = "expense_management.db"
CATEGORIES = ["Housing", "Food", "Transport", "Utilities", "Entertainment",
              "Health", "Salary", "Investment", "Office", "Other"]


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                date        TEXT    NOT NULL,
                category    TEXT    NOT NULL,
                description TEXT    NOT NULL,
                amount      REAL    NOT NULL,
                type        TEXT    NOT NULL DEFAULT 'expense',
                created_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                category    TEXT    NOT NULL UNIQUE,
                monthly_limit REAL  NOT NULL,
                updated_at  TEXT    DEFAULT (datetime('now'))
            )
        """)
        conn.commit()


def add_transaction(date_str: str, category: str,
                    description: str, amount: float,
                    txn_type: str = "expense") -> int:
    with get_conn() as conn:
        cursor = conn.execute(
            "INSERT INTO transactions (date, category, description, amount, type) VALUES (?,?,?,?,?)",
            (date_str, category, description, amount, txn_type)
        )
        conn.commit()
        return cursor.lastrowid


def set_budget(category: str, limit: float) -> None:
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)
            ON CONFLICT(category) DO UPDATE SET monthly_limit=?, updated_at=datetime('now')
        """, (category, limit, limit))
        conn.commit()


def monthly_summary(year_month: str) -> dict:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT category,
                   SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expenses,
                   SUM(CASE WHEN type='income'  THEN amount ELSE 0 END) AS income
            FROM transactions
            WHERE strftime('%Y-%m', date) = ?
            GROUP BY category
            ORDER BY expenses DESC
        """, (year_month,)).fetchall()
        return [dict(r) for r in rows]


def budget_vs_actual(year_month: str) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT b.category,
                   b.monthly_limit AS budget,
                   COALESCE(SUM(t.amount), 0) AS spent
            FROM budgets b
            LEFT JOIN transactions t
                ON b.category = t.category
               AND strftime('%Y-%m', t.date) = ?
               AND t.type = 'expense'
            GROUP BY b.category
            ORDER BY spent/b.monthly_limit DESC
        """, (year_month,)).fetchall()
        result = []
        for r in rows:
            d = dict(r)
            d["remaining"] = round(d["budget"] - d["spent"], 2)
            d["pct"]       = round(d["spent"] / d["budget"] * 100, 1) if d["budget"] else 0
            result.append(d)
        return result


def monthly_trend(months: int = 6) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT strftime('%Y-%m', date) AS month,
                   SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) AS expenses,
                   SUM(CASE WHEN type='income'  THEN amount ELSE 0 END) AS income
            FROM transactions
            GROUP BY month
            ORDER BY month DESC
            LIMIT ?
        """, (months,)).fetchall()
        return [dict(r) for r in rows]


def export_csv(year_month: str, filename: str = None) -> str:
    filename = filename or f"expenses_{year_month}.csv"
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM transactions WHERE strftime('%Y-%m', date) = ? ORDER BY date",
            (year_month,)
        ).fetchall()
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id","date","category","description","amount","type"])
        writer.writeheader()
        writer.writerows([dict(r) for r in rows])
    return filename


def seed_sample_data() -> None:
    count = get_conn().execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
    if count > 0:
        return
    today = date.today()
    month = today.strftime("%Y-%m")
    samples = [
        (f"{month}-01", "Salary",        "Monthly salary",      5000, "income"),
        (f"{month}-02", "Housing",        "Rent",                1200, "expense"),
        (f"{month}-03", "Food",           "Groceries",            180, "expense"),
        (f"{month}-05", "Transport",      "Monthly pass",          90, "expense"),
        (f"{month}-07", "Utilities",      "Electric bill",        120, "expense"),
        (f"{month}-10", "Food",           "Restaurant dinner",     65, "expense"),
        (f"{month}-12", "Entertainment",  "Streaming services",    30, "expense"),
        (f"{month}-15", "Health",         "Gym membership",        50, "expense"),
        (f"{month}-18", "Food",           "Groceries",            155, "expense"),
        (f"{month}-20", "Office",         "Office supplies",       45, "expense"),
        (f"{month}-22", "Investment",     "Stock purchase",       500, "expense"),
    ]
    for d, cat, desc, amt, typ in samples:
        add_transaction(d, cat, desc, amt, typ)
    for cat, lim in [("Housing", 1300), ("Food", 500), ("Transport", 150),
                     ("Entertainment", 100), ("Health", 100), ("Office", 100)]:
        set_budget(cat, lim)
    print("  Sample data loaded.")


def main():
    init_db()
    seed_sample_data()
    this_month = date.today().strftime("%Y-%m")

    print("=" * 60)
    print("  EXPENSE MANAGEMENT APPLICATION")
    print("=" * 60)

    while True:
        print(f"\n  Period: {this_month}")
        print("\n  [1] Add Transaction   [2] Monthly Summary")
        print("  [3] Budget vs Actual  [4] Monthly Trend")
        print("  [5] Set Budget        [6] Export CSV")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            print(f"  Categories: {', '.join(CATEGORIES)}")
            try:
                date_input = input("  Date (YYYY-MM-DD, blank=today): ").strip() or date.today().isoformat()
                category   = input("  Category: ").strip().title()
                desc       = input("  Description: ").strip()
                amount     = float(input("  Amount ($): "))
                txn_type   = input("  Type (expense/income) [expense]: ").strip() or "expense"
                add_transaction(date_input, category, desc, amount, txn_type)
                print("  Transaction added.")
            except ValueError:
                print("  Invalid input.")

        elif choice == "2":
            month  = input(f"  Month [{this_month}]: ").strip() or this_month
            rows   = monthly_summary(month)
            total_exp = sum(r["expenses"] for r in rows)
            total_inc = sum(r["income"]   for r in rows)
            print(f"\n  SUMMARY: {month}")
            print(f"  {'Category':<15} {'Expenses':>10} {'Income':>10}")
            print("  " + "-" * 38)
            for r in rows:
                print(f"  {r['category']:<15} ${r['expenses']:>9,.2f} ${r['income']:>9,.2f}")
            print("  " + "-" * 38)
            print(f"  {'TOTAL':<15} ${total_exp:>9,.2f} ${total_inc:>9,.2f}")
            print(f"  Net: ${total_inc - total_exp:,.2f}")

        elif choice == "3":
            month = input(f"  Month [{this_month}]: ").strip() or this_month
            rows  = budget_vs_actual(month)
            print(f"\n  BUDGET vs ACTUAL: {month}")
            print(f"  {'Category':<14} {'Budget':>8} {'Spent':>8} {'Remain':>8} {'%':>5} {'Status'}")
            print("  " + "-" * 58)
            for r in rows:
                flag = " OVER" if r["pct"] > 100 else " WARN" if r["pct"] > 80 else ""
                print(f"  {r['category']:<14} ${r['budget']:>7,.0f} ${r['spent']:>7,.2f} "
                      f"${r['remaining']:>7,.2f} {r['pct']:>4.0f}%{flag}")

        elif choice == "4":
            trend = monthly_trend()
            print("\n  MONTHLY TREND (last 6 months)")
            print(f"  {'Month':<10} {'Income':>10} {'Expenses':>10} {'Net':>10}")
            print("  " + "-" * 45)
            for r in trend:
                net = r["income"] - r["expenses"]
                print(f"  {r['month']:<10} ${r['income']:>9,.2f} ${r['expenses']:>9,.2f} ${net:>9,.2f}")

        elif choice == "5":
            cat = input("  Category: ").strip().title()
            try:
                limit = float(input(f"  Monthly budget for {cat} ($): "))
                set_budget(cat, limit)
                print(f"  Budget set: {cat} = ${limit:,.2f}/month")
            except ValueError:
                print("  Invalid amount.")

        elif choice == "6":
            month = input(f"  Month [{this_month}]: ").strip() or this_month
            fname = export_csv(month)
            print(f"  Exported: {fname}")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
