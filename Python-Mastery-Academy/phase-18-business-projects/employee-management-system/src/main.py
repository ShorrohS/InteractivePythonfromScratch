"""
Employee Management System
Phase 18: Business Projects

This is a complete end-to-end business application demonstrating:
  - OOP (Employee class hierarchy)
  - SQLite database with proper CRUD
  - Input validation and error handling
  - CSV report generation
  - Professional project structure
  - Logging

HOW TO RUN:
  python main.py
"""

import sqlite3
import csv
import logging
import os
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


# ============================================================
# LOGGING SETUP
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("ems.log")
    ]
)
logger = logging.getLogger(__name__)


# ============================================================
# CONFIG
# ============================================================

DB_FILE = "employees.db"
INCOME_TAX_RATE = 0.20
NI_RATE = 0.12


# ============================================================
# DOMAIN MODELS (Dataclasses)
# ============================================================

class EmploymentStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

@dataclass
class Employee:
    first_name: str
    last_name: str
    department: str
    salary: float
    email: str = ""
    job_title: str = ""
    employee_id: str = ""
    status: str = EmploymentStatus.ACTIVE
    hire_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))
    db_id: Optional[int] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    @property
    def monthly_salary(self) -> float:
        return self.salary / 12
    
    @property
    def monthly_tax(self) -> float:
        return self.monthly_salary * INCOME_TAX_RATE
    
    @property
    def monthly_ni(self) -> float:
        return self.monthly_salary * NI_RATE
    
    @property
    def monthly_net(self) -> float:
        return self.monthly_salary - self.monthly_tax - self.monthly_ni


# ============================================================
# DATABASE LAYER
# ============================================================

class Database:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        self.init()
    
    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def init(self) -> None:
        """Create all tables."""
        with self._conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS employees (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT    UNIQUE NOT NULL,
                    first_name  TEXT    NOT NULL,
                    last_name   TEXT    NOT NULL,
                    email       TEXT,
                    department  TEXT    NOT NULL,
                    job_title   TEXT,
                    salary      REAL    NOT NULL,
                    hire_date   TEXT    NOT NULL,
                    status      TEXT    DEFAULT 'active',
                    created_at  TEXT    DEFAULT (datetime('now'))
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS salary_history (
                    id          INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id TEXT    NOT NULL,
                    old_salary  REAL    NOT NULL,
                    new_salary  REAL    NOT NULL,
                    reason      TEXT,
                    changed_at  TEXT    DEFAULT (datetime('now'))
                )
            """)
            conn.commit()
    
    def _generate_id(self) -> str:
        """Generate next employee ID."""
        with self._conn() as conn:
            row = conn.execute("SELECT MAX(CAST(SUBSTR(employee_id, 4) AS INTEGER)) FROM employees").fetchone()
            n = (row[0] or 0) + 1
            return f"EMP{n:04d}"
    
    def add(self, emp: Employee) -> Employee:
        emp.employee_id = self._generate_id()
        with self._conn() as conn:
            cursor = conn.execute(
                """INSERT INTO employees 
                   (employee_id, first_name, last_name, email, department, job_title, salary, hire_date)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (emp.employee_id, emp.first_name, emp.last_name, emp.email,
                 emp.department, emp.job_title, emp.salary, emp.hire_date)
            )
            conn.commit()
            emp.db_id = cursor.lastrowid
        logger.info(f"Added employee: {emp.full_name} ({emp.employee_id})")
        return emp
    
    def get_all(self, active_only: bool = True) -> list[Employee]:
        with self._conn() as conn:
            query = "SELECT * FROM employees"
            if active_only:
                query += " WHERE status = 'active'"
            query += " ORDER BY last_name, first_name"
            rows = conn.execute(query).fetchall()
            return [self._row_to_employee(r) for r in rows]
    
    def get_by_id(self, employee_id: str) -> Optional[Employee]:
        with self._conn() as conn:
            row = conn.execute(
                "SELECT * FROM employees WHERE employee_id = ?", (employee_id,)
            ).fetchone()
            return self._row_to_employee(row) if row else None
    
    def search(self, query: str) -> list[Employee]:
        with self._conn() as conn:
            rows = conn.execute(
                """SELECT * FROM employees 
                   WHERE (first_name || ' ' || last_name LIKE ? OR department LIKE ?)
                   AND status = 'active'""",
                (f"%{query}%", f"%{query}%")
            ).fetchall()
            return [self._row_to_employee(r) for r in rows]
    
    def update_salary(self, employee_id: str, new_salary: float, reason: str = "") -> bool:
        emp = self.get_by_id(employee_id)
        if not emp:
            return False
        with self._conn() as conn:
            conn.execute("UPDATE employees SET salary = ? WHERE employee_id = ?", (new_salary, employee_id))
            conn.execute(
                "INSERT INTO salary_history (employee_id, old_salary, new_salary, reason) VALUES (?, ?, ?, ?)",
                (employee_id, emp.salary, new_salary, reason)
            )
            conn.commit()
        logger.info(f"Salary updated for {employee_id}: ${emp.salary:,.0f} → ${new_salary:,.0f}")
        return True
    
    def deactivate(self, employee_id: str) -> bool:
        with self._conn() as conn:
            cursor = conn.execute(
                "UPDATE employees SET status = 'inactive' WHERE employee_id = ?", (employee_id,)
            )
            conn.commit()
            return cursor.rowcount > 0
    
    def get_department_stats(self) -> list[dict]:
        with self._conn() as conn:
            rows = conn.execute("""
                SELECT department,
                       COUNT(*) as headcount,
                       ROUND(AVG(salary), 2) as avg_salary,
                       MAX(salary) as max_salary,
                       MIN(salary) as min_salary,
                       SUM(salary) as total_payroll
                FROM employees WHERE status = 'active'
                GROUP BY department
                ORDER BY total_payroll DESC
            """).fetchall()
            return [dict(r) for r in rows]
    
    def _row_to_employee(self, row: sqlite3.Row) -> Employee:
        return Employee(
            first_name=row["first_name"], last_name=row["last_name"],
            department=row["department"], salary=row["salary"],
            email=row["email"] or "", job_title=row["job_title"] or "",
            employee_id=row["employee_id"], status=row["status"],
            hire_date=row["hire_date"], db_id=row["id"]
        )


# ============================================================
# REPORT SERVICE
# ============================================================

class ReportService:
    def __init__(self, db: Database):
        self.db = db
    
    def payroll_report(self, output_file: str = "payroll_report.csv") -> str:
        employees = self.db.get_all()
        
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Employee ID", "Name", "Department", "Annual Salary",
                "Monthly Gross", "Monthly Tax", "Monthly NI", "Monthly Net"
            ])
            
            total_annual = 0
            for emp in employees:
                writer.writerow([
                    emp.employee_id, emp.full_name, emp.department,
                    f"{emp.salary:.2f}", f"{emp.monthly_salary:.2f}",
                    f"{emp.monthly_tax:.2f}", f"{emp.monthly_ni:.2f}",
                    f"{emp.monthly_net:.2f}"
                ])
                total_annual += emp.salary
            
            writer.writerow([])
            writer.writerow(["TOTAL", "", "", f"{total_annual:.2f}"])
        
        logger.info(f"Payroll report generated: {output_file}")
        return output_file


# ============================================================
# MAIN CLI APPLICATION
# ============================================================

class EMSApplication:
    def __init__(self):
        self.db = Database()
        self.reports = ReportService(self.db)
        self._seed_data_if_empty()
    
    def _seed_data_if_empty(self):
        if not self.db.get_all():
            seed = [
                Employee("Alice", "Johnson", "Engineering", 85000, "alice@company.com", "Senior Developer"),
                Employee("Bob", "Smith", "Sales", 65000, "bob@company.com", "Account Manager"),
                Employee("Carol", "Davis", "Engineering", 92000, "carol@company.com", "Tech Lead"),
                Employee("Dave", "Wilson", "Marketing", 72000, "dave@company.com", "Marketing Manager"),
                Employee("Eve", "Martinez", "Sales", 68000, "eve@company.com", "Sales Rep"),
            ]
            for emp in seed:
                self.db.add(emp)
            print("  ✅ Sample data loaded.")
    
    def display_employees(self, employees: list[Employee]) -> None:
        if not employees:
            print("  No employees found.")
            return
        print(f"\n  {'ID':<10} {'Name':<25} {'Department':<15} {'Salary':>12}")
        print("  " + "─" * 65)
        for emp in employees:
            print(f"  {emp.employee_id:<10} {emp.full_name:<25} {emp.department:<15} ${emp.salary:>11,.2f}")
        print(f"\n  Total: {len(employees)} employee(s)")
    
    def run(self):
        print("=" * 65)
        print("  👥 EMPLOYEE MANAGEMENT SYSTEM")
        print("=" * 65)
        
        while True:
            print("\n  [1] View All Employees")
            print("  [2] Search Employees")
            print("  [3] Add New Employee")
            print("  [4] Update Salary")
            print("  [5] Deactivate Employee")
            print("  [6] Department Statistics")
            print("  [7] Generate Payroll Report")
            print("  [0] Exit")
            
            choice = input("\n  Option: ").strip()
            print()
            
            if choice == "1":
                self.display_employees(self.db.get_all())
                
            elif choice == "2":
                q = input("  Search (name or department): ")
                self.display_employees(self.db.search(q))
                
            elif choice == "3":
                print("  ADD NEW EMPLOYEE")
                first = input("  First Name: ").strip().title()
                last = input("  Last Name: ").strip().title()
                dept = input("  Department: ").strip().title()
                title = input("  Job Title: ").strip().title()
                email = input("  Email: ").strip().lower()
                try:
                    salary = float(input("  Annual Salary ($): "))
                    emp = Employee(first, last, dept, salary, email, title)
                    emp = self.db.add(emp)
                    print(f"\n  ✅ Employee added: {emp.full_name} ({emp.employee_id})")
                except ValueError:
                    print("  ❌ Invalid salary.")
                    
            elif choice == "4":
                emp_id = input("  Employee ID: ").strip().upper()
                emp = self.db.get_by_id(emp_id)
                if emp:
                    print(f"  Current salary: ${emp.salary:,.2f}")
                    try:
                        new_sal = float(input("  New salary ($): "))
                        reason = input("  Reason: ")
                        if self.db.update_salary(emp_id, new_sal, reason):
                            print(f"  ✅ Salary updated to ${new_sal:,.2f}")
                    except ValueError:
                        print("  ❌ Invalid salary.")
                else:
                    print(f"  ❌ Employee {emp_id} not found.")
                    
            elif choice == "5":
                emp_id = input("  Employee ID to deactivate: ").strip().upper()
                emp = self.db.get_by_id(emp_id)
                if emp:
                    confirm = input(f"  Deactivate {emp.full_name}? (yes/no): ")
                    if confirm.lower() == "yes":
                        self.db.deactivate(emp_id)
                        print(f"  ✅ {emp.full_name} deactivated.")
                else:
                    print(f"  ❌ Employee {emp_id} not found.")
                    
            elif choice == "6":
                stats = self.db.get_department_stats()
                print(f"  {'Department':<20} {'Count':>6} {'Avg Salary':>12} {'Total Payroll':>15}")
                print("  " + "─" * 58)
                for s in stats:
                    print(f"  {s['department']:<20} {s['headcount']:>6} ${s['avg_salary']:>11,.0f} ${s['total_payroll']:>14,.0f}")
                    
            elif choice == "7":
                filename = self.reports.payroll_report()
                employees = self.db.get_all()
                total = sum(e.salary for e in employees)
                print(f"  ✅ Payroll report generated: {filename}")
                print(f"  Employees: {len(employees)} | Total Payroll: ${total:,.2f}/year")
                    
            elif choice == "0":
                print("  Goodbye!")
                logger.info("Application closed.")
                break
            else:
                print("  Invalid option.")
            
            input("\n  Press Enter to continue...")


if __name__ == "__main__":
    app = EMSApplication()
    app.run()
