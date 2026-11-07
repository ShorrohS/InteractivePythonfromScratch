"""
Expense Manager
Phase 08: Intermediate Projects

SKILLS USED: OOP, JSON persistence, monthly/category analytics, budget tracking

HOW TO RUN: python main.py
"""

import json
import os
from datetime import datetime
from collections import defaultdict


CATEGORIES = ["Housing", "Food", "Transport", "Utilities", "Entertainment",
              "Health", "Clothing", "Education", "Savings", "Other"]


class Expense:
    def __init__(self, amount: float, category: str, description: str,
                 date: str = None):
        self.id          = None
        self.amount      = round(float(amount), 2)
        self.category    = category
        self.description = description.strip()
        self.date        = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Expense":
        e = cls(d["amount"], d["category"], d["description"], d["date"])
        e.id = d["id"]
        return e

    def __str__(self) -> str:
        return (f"[{self.id:04d}] {self.date}  {self.category:<14} "
                f"${self.amount:>8.2f}  {self.description[:30]}")


class Budget:
    def __init__(self, category: str, monthly_limit: float):
        self.category     = category
        self.monthly_limit = monthly_limit


class ExpenseManager:
    FILE = "expenses_data.json"

    def __init__(self):
        self._expenses: list[Expense] = []
        self._budgets:  dict[str, float] = {}
        self._next_id   = 1
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.FILE): return
        with open(self.FILE) as f:
            data = json.load(f)
            self._expenses = [Expense.from_dict(d) for d in data.get("expenses", [])]
            self._budgets  = data.get("budgets", {})
            self._next_id  = data.get("next_id", len(self._expenses) + 1)

    def _save(self) -> None:
        with open(self.FILE, "w") as f:
            json.dump({
                "expenses": [e.to_dict() for e in self._expenses],
                "budgets":  self._budgets,
                "next_id":  self._next_id
            }, f, indent=2)

    def add(self, amount: float, category: str, description: str,
            date: str = None) -> Expense:
        e = Expense(amount, category, description, date)
        e.id = self._next_id
        self._next_id += 1
        self._expenses.append(e)
        self._save()
        return e

    def delete(self, eid: int) -> bool:
        e = next((x for x in self._expenses if x.id == eid), None)
        if not e: return False
        self._expenses.remove(e)
        self._save()
        return True

    def set_budget(self, category: str, limit: float) -> None:
        self._budgets[category] = limit
        self._save()

    def current_month_expenses(self) -> list[Expense]:
        month = datetime.now().strftime("%Y-%m")
        return [e for e in self._expenses if e.date.startswith(month)]

    def by_category(self, expenses: list[Expense] = None) -> dict[str, float]:
        ex = expenses or self._expenses
        totals = defaultdict(float)
        for e in ex:
            totals[e.category] += e.amount
        return dict(totals)

    def monthly_totals(self) -> dict[str, float]:
        monthly = defaultdict(float)
        for e in self._expenses:
            monthly[e.date[:7]] += e.amount
        return dict(monthly)

    def budget_status(self) -> list[dict]:
        month_totals = self.by_category(self.current_month_expenses())
        results = []
        for cat, limit in self._budgets.items():
            spent = month_totals.get(cat, 0)
            pct   = (spent / limit * 100) if limit > 0 else 0
            results.append({
                "category": cat, "budget": limit,
                "spent": spent, "remaining": limit - spent, "pct": pct
            })
        return results

    @property
    def total(self) -> float:
        return sum(e.amount for e in self._expenses)

    @property
    def month_total(self) -> float:
        return sum(e.amount for e in self.current_month_expenses())


def main():
    mgr = ExpenseManager()
    print("=" * 60)
    print("  EXPENSE MANAGER")
    print("=" * 60)

    while True:
        print(f"\n  This month: ${mgr.month_total:,.2f}  |  All time: ${mgr.total:,.2f}")
        print("\n  [1] View This Month  [2] Add Expense    [3] Category Report")
        print("  [4] Monthly Trend    [5] Set Budget     [6] Budget Status")
        print("  [7] Delete Expense   [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            expenses = mgr.current_month_expenses()
            if not expenses:
                print("  No expenses this month.")
            else:
                for e in expenses: print(f"  {e}")
                print(f"\n  Month total: ${sum(e.amount for e in expenses):,.2f}")

        elif choice == "2":
            print(f"\n  Categories: {', '.join(CATEGORIES)}")
            try:
                amount = float(input("  Amount ($): "))
                cat    = input("  Category: ").strip().title()
                if cat not in CATEGORIES:
                    cat = "Other"
                desc   = input("  Description: ").strip()
                date   = input("  Date (YYYY-MM-DD, blank=today): ").strip() or None
                e = mgr.add(amount, cat, desc, date)
                print(f"  Added: {e}")
            except ValueError:
                print("  Invalid amount.")

        elif choice == "3":
            cats = mgr.by_category(mgr.current_month_expenses())
            total = sum(cats.values())
            print(f"\n  {'Category':<15} {'Amount':>10} {'%':>6}")
            print("  " + "-" * 35)
            for cat, amt in sorted(cats.items(), key=lambda x: x[1], reverse=True):
                pct = (amt / total * 100) if total else 0
                print(f"  {cat:<15} ${amt:>9.2f} {pct:>5.1f}%")

        elif choice == "4":
            monthly = mgr.monthly_totals()
            print(f"\n  {'Month':<10} {'Total':>12}")
            print("  " + "-" * 25)
            for month, total in sorted(monthly.items()):
                bar = "#" * int(total // 100)
                print(f"  {month}  ${total:>10,.2f}  {bar}")

        elif choice == "5":
            cat   = input("  Category: ").strip().title()
            try:
                limit = float(input(f"  Monthly budget for {cat} ($): "))
                mgr.set_budget(cat, limit)
                print(f"  Budget set: {cat} = ${limit:,.2f}/month")
            except ValueError:
                print("  Invalid amount.")

        elif choice == "6":
            statuses = mgr.budget_status()
            if not statuses:
                print("  No budgets set. Use option [5] to set budgets.")
            else:
                print(f"\n  {'Category':<14} {'Budget':>9} {'Spent':>9} {'Remaining':>10} {'%':>6}")
                print("  " + "-" * 55)
                for s in sorted(statuses, key=lambda x: x["pct"], reverse=True):
                    flag = " [OVER]" if s["pct"] > 100 else " [WARN]" if s["pct"] > 80 else ""
                    print(f"  {s['category']:<14} ${s['budget']:>8,.0f} "
                          f"${s['spent']:>8,.2f} ${s['remaining']:>9,.2f} "
                          f"{s['pct']:>5.0f}%{flag}")

        elif choice == "7":
            try:
                eid = int(input("  Expense ID to delete: "))
                print("  Deleted." if mgr.delete(eid) else "  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
