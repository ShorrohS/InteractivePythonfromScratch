"""
Project 02 - CSV Expense Tracker
Phase 05: File Handling

SKILLS PRACTICED:
  - Writing and reading CSV files
  - DictWriter and DictReader
  - Type conversion on read
  - Aggregation from file data

HOW TO RUN:
  python main.py
"""

import csv
import os
from datetime import datetime
from pathlib import Path

CSV_FILE = "expenses.csv"
FIELDNAMES = ["date", "category", "description", "amount"]

CATEGORIES = ["Food", "Transport", "Rent", "Utilities", "Entertainment",
              "Health", "Clothing", "Education", "Other"]


def initialize_file() -> None:
    """Create CSV file with header if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
        print("  Created new expense file.")


def add_expense(category: str, description: str, amount: float,
                date: str = None) -> None:
    """Append one expense to the CSV."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "date":        date,
            "category":    category,
            "description": description,
            "amount":      amount
        })
    print(f"  Added: {category} — {description} — ${amount:.2f}")


def load_expenses() -> list[dict]:
    """Load and return all expenses with proper types."""
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r") as f:
        return [
            {**row, "amount": float(row["amount"])}
            for row in csv.DictReader(f)
        ]


def display_expenses(expenses: list[dict] = None) -> None:
    """Display a formatted expense table."""
    expenses = expenses or load_expenses()
    if not expenses:
        print("  No expenses recorded.")
        return
    print(f"\n  {'Date':<12} {'Category':<15} {'Description':<25} {'Amount':>8}")
    print("  " + "-" * 64)
    for e in expenses:
        print(f"  {e['date']:<12} {e['category']:<15} "
              f"{e['description'][:24]:<25} ${e['amount']:>7.2f}")
    total = sum(e["amount"] for e in expenses)
    print("  " + "-" * 64)
    print(f"  {'TOTAL':<54} ${total:>7.2f}")


def summary_by_category(expenses: list[dict] = None) -> None:
    """Show spending breakdown by category."""
    expenses = expenses or load_expenses()
    if not expenses:
        print("  No data.")
        return

    totals = {}
    for e in expenses:
        cat = e["category"]
        totals[cat] = totals.get(cat, 0) + e["amount"]

    grand = sum(totals.values())
    print(f"\n  {'Category':<18} {'Amount':>10} {'%':>6}")
    print("  " + "-" * 36)
    for cat, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        pct = total / grand * 100
        bar = "#" * int(pct / 5)
        print(f"  {cat:<18} ${total:>9.2f} {pct:>5.1f}%  {bar}")
    print("  " + "-" * 36)
    print(f"  {'TOTAL':<18} ${grand:>9.2f}")


def monthly_report(expenses: list[dict] = None) -> None:
    """Show monthly spending totals."""
    expenses = expenses or load_expenses()
    if not expenses:
        print("  No data.")
        return

    monthly = {}
    for e in expenses:
        month = e["date"][:7]    # YYYY-MM
        monthly[month] = monthly.get(month, 0) + e["amount"]

    print(f"\n  {'Month':<12} {'Total':>10}")
    print("  " + "-" * 24)
    for month in sorted(monthly):
        print(f"  {month:<12} ${monthly[month]:>9.2f}")


def search_expenses(keyword: str) -> list[dict]:
    """Search by category or description."""
    q = keyword.lower()
    return [
        e for e in load_expenses()
        if q in e["category"].lower() or q in e["description"].lower()
    ]


def main():
    initialize_file()

    print("=" * 55)
    print("  CSV EXPENSE TRACKER")
    print("=" * 55)

    while True:
        expenses = load_expenses()
        total = sum(e["amount"] for e in expenses) if expenses else 0
        print(f"\n  Entries: {len(expenses)} | Total: ${total:,.2f}")
        print()
        print("  [1] Add Expense")
        print("  [2] View All Expenses")
        print("  [3] Category Summary")
        print("  [4] Monthly Report")
        print("  [5] Search")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            print("\n  CATEGORIES:")
            for i, cat in enumerate(CATEGORIES, 1):
                print(f"    [{i}] {cat}")
            try:
                cat_num = int(input("  Select category: ")) - 1
                category = CATEGORIES[cat_num]
            except (ValueError, IndexError):
                print("  Invalid category.")
                continue
            desc   = input("  Description: ").strip()
            try:
                amount = float(input("  Amount ($): "))
                add_expense(category, desc, amount)
            except ValueError:
                print("  Invalid amount.")

        elif choice == "2":
            display_expenses()

        elif choice == "3":
            summary_by_category()

        elif choice == "4":
            monthly_report()

        elif choice == "5":
            keyword = input("  Search: ").strip()
            results = search_expenses(keyword)
            if results:
                display_expenses(results)
            else:
                print("  No matches found.")

        elif choice == "0":
            print("  Goodbye! Track your spending!")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
