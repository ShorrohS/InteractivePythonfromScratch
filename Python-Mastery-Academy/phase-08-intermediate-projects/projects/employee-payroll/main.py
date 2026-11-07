"""
Employee Payroll System
Phase 08: Intermediate Projects

SKILLS USED: OOP, CSV export, JSON persistence, payroll calculations

HOW TO RUN: python main.py
"""

import json
import csv
import os
from datetime import datetime
from collections import defaultdict


class PayrollRecord:
    def __init__(self, emp_id: str, name: str, dept: str,
                 hours: float, rate: float, month: str = None):
        self.emp_id = emp_id
        self.name   = name
        self.dept   = dept
        self.hours  = hours
        self.rate   = rate
        self.month  = month or datetime.now().strftime("%Y-%m")

    @property
    def regular_hours(self) -> float:
        return min(self.hours, 40.0)

    @property
    def overtime_hours(self) -> float:
        return max(0, self.hours - 40.0)

    @property
    def gross(self) -> float:
        return round(self.regular_hours * self.rate +
                     self.overtime_hours * self.rate * 1.5, 2)

    @property
    def tax(self) -> float:
        return round(self.gross * 0.20, 2)

    @property
    def ni(self) -> float:
        return round(self.gross * 0.12, 2)

    @property
    def net(self) -> float:
        return round(self.gross - self.tax - self.ni, 2)

    def to_dict(self) -> dict:
        return {
            "emp_id": self.emp_id, "name": self.name,
            "dept": self.dept, "hours": self.hours,
            "rate": self.rate, "month": self.month
        }


class PayrollSystem:
    FILE = "payroll_data.json"

    def __init__(self):
        self._employees: dict[str, dict] = {}
        self._records:   list[PayrollRecord] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.FILE): return
        with open(self.FILE) as f:
            data = json.load(f)
            self._employees = data.get("employees", {})
            self._records   = [
                PayrollRecord(**r) for r in data.get("records", [])
            ]

    def _save(self) -> None:
        with open(self.FILE, "w") as f:
            json.dump({
                "employees": self._employees,
                "records":   [r.to_dict() for r in self._records]
            }, f, indent=2)

    def add_employee(self, emp_id: str, name: str, dept: str,
                     rate: float) -> None:
        self._employees[emp_id] = {
            "name": name, "dept": dept, "rate": rate
        }
        self._save()
        print(f"  Added: {name} ({emp_id}) — ${rate}/hr")

    def process_payroll(self, emp_id: str, hours: float,
                        month: str = None) -> PayrollRecord:
        if emp_id not in self._employees:
            raise ValueError(f"Employee {emp_id} not found")
        emp = self._employees[emp_id]
        rec = PayrollRecord(emp_id, emp["name"], emp["dept"],
                            hours, emp["rate"], month)
        self._records.append(rec)
        self._save()
        return rec

    def get_records(self, month: str = None) -> list[PayrollRecord]:
        if month:
            return [r for r in self._records if r.month == month]
        return self._records

    def export_csv(self, month: str, filename: str = None) -> str:
        records = self.get_records(month)
        filename = filename or f"payroll_{month}.csv"
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Dept", "Hours", "Rate",
                             "Gross", "Tax", "NI", "Net"])
            for r in records:
                writer.writerow([r.emp_id, r.name, r.dept,
                                 r.hours, r.rate, r.gross, r.tax, r.ni, r.net])
        return filename

    def dept_summary(self, month: str) -> dict:
        summary = defaultdict(lambda: {"count": 0, "gross": 0, "net": 0})
        for r in self.get_records(month):
            summary[r.dept]["count"] += 1
            summary[r.dept]["gross"] += r.gross
            summary[r.dept]["net"]   += r.net
        return dict(summary)


def main():
    sys = PayrollSystem()

    # Seed employees if empty
    if not sys._employees:
        employees = [
            ("E001","Alice Johnson","Engineering",42.50),
            ("E002","Bob Smith",    "Sales",       28.00),
            ("E003","Carol Davis",  "Engineering", 55.00),
            ("E004","Dave Wilson",  "Marketing",   35.00),
            ("E005","Eve Martinez", "Sales",       30.00),
        ]
        for eid, name, dept, rate in employees:
            sys.add_employee(eid, name, dept, rate)

    print("=" * 65)
    print("  EMPLOYEE PAYROLL SYSTEM")
    print("=" * 65)

    while True:
        print("\n  [1] List Employees    [2] Add Employee")
        print("  [3] Process Payroll   [4] View Monthly Report")
        print("  [5] Department Report [6] Export CSV")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            print(f"\n  {'ID':<8} {'Name':<22} {'Dept':<14} {'Rate':>8}")
            print("  " + "-" * 56)
            for eid, emp in sys._employees.items():
                print(f"  {eid:<8} {emp['name']:<22} {emp['dept']:<14} ${emp['rate']:>7.2f}/hr")

        elif choice == "2":
            eid  = input("  Employee ID: ").strip().upper()
            name = input("  Name: ").strip().title()
            dept = input("  Department: ").strip().title()
            try:
                rate = float(input("  Hourly rate ($): "))
                sys.add_employee(eid, name, dept, rate)
            except ValueError:
                print("  Invalid rate.")

        elif choice == "3":
            eid = input("  Employee ID: ").strip().upper()
            try:
                hours = float(input("  Hours worked: "))
                month = input("  Month (YYYY-MM, blank=current): ").strip() or None
                rec = sys.process_payroll(eid, hours, month)
                print(f"\n  Payslip: {rec.name}")
                print(f"  Hours:   {rec.hours} ({rec.overtime_hours:.0f} OT)")
                print(f"  Gross:   ${rec.gross:,.2f}")
                print(f"  Tax:     ${rec.tax:,.2f}")
                print(f"  NI:      ${rec.ni:,.2f}")
                print(f"  Net:     ${rec.net:,.2f}")
            except (ValueError, KeyError) as e:
                print(f"  Error: {e}")

        elif choice == "4":
            month = input("  Month (YYYY-MM): ").strip()
            records = sys.get_records(month)
            if not records:
                print(f"  No records for {month}.")
                continue
            print(f"\n  {'Name':<22} {'Hrs':>5} {'Gross':>10} {'Tax':>8} {'Net':>10}")
            print("  " + "-" * 58)
            totals = {"gross": 0, "tax": 0, "net": 0}
            for r in records:
                print(f"  {r.name:<22} {r.hours:>5.1f} ${r.gross:>9,.2f} "
                      f"${r.tax:>7,.2f} ${r.net:>9,.2f}")
                totals["gross"] += r.gross
                totals["tax"]   += r.tax
                totals["net"]   += r.net
            print("  " + "-" * 58)
            print(f"  {'TOTALS':<28} ${totals['gross']:>9,.2f} "
                  f"${totals['tax']:>7,.2f} ${totals['net']:>9,.2f}")

        elif choice == "5":
            month = input("  Month (YYYY-MM): ").strip()
            summary = sys.dept_summary(month)
            print(f"\n  {'Dept':<16} {'Employees':>10} {'Gross':>12} {'Net':>12}")
            print("  " + "-" * 54)
            for dept, data in sorted(summary.items()):
                print(f"  {dept:<16} {data['count']:>10} "
                      f"${data['gross']:>11,.2f} ${data['net']:>11,.2f}")

        elif choice == "6":
            month = input("  Month (YYYY-MM): ").strip()
            fname = sys.export_csv(month)
            print(f"  Exported: {fname}")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
