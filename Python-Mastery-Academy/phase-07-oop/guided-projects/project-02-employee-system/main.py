"""
Project 02 - Employee Management System (OOP)
Phase 07: OOP

SKILLS PRACTICED:
  - Class hierarchy (inheritance)
  - Polymorphism (calculate_pay varies per type)
  - Encapsulation (@property with validation)
  - Abstract base class
  - Dunder methods (__str__, __repr__, __eq__)

HOW TO RUN:
  python main.py
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


# ============================================================
# BASE CLASS
# ============================================================

class Employee(ABC):
    """Abstract base class for all employee types."""

    _id_counter = 1000

    def __init__(self, first: str, last: str, department: str):
        Employee._id_counter += 1
        self._employee_id  = f"EMP{Employee._id_counter:05d}"
        self.first_name    = first.strip().title()
        self.last_name     = last.strip().title()
        self.department    = department.strip().title()
        self._active       = True
        self.hire_date     = datetime.now().strftime("%Y-%m-%d")
        self._salary_history: list[dict] = []

    @property
    def employee_id(self) -> str:
        return self._employee_id

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self) -> bool:
        return self._active

    @abstractmethod
    def calculate_pay(self) -> float:
        """Each subclass calculates pay differently."""
        pass

    @abstractmethod
    def employment_type(self) -> str:
        pass

    def deactivate(self) -> None:
        self._active = False

    def __str__(self) -> str:
        return (f"{self._employee_id} | {self.full_name:<22} | "
                f"{self.department:<14} | {self.employment_type():<12} | "
                f"${self.calculate_pay():>10,.2f}")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.full_name!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Employee) and self._employee_id == other._employee_id


# ============================================================
# CONCRETE EMPLOYEE TYPES
# ============================================================

class SalariedEmployee(Employee):
    """Full-time employee paid annual salary."""

    def __init__(self, first, last, department, annual_salary: float):
        super().__init__(first, last, department)
        self._annual_salary = 0.0
        self.annual_salary  = annual_salary   # uses setter

    @property
    def annual_salary(self) -> float:
        return self._annual_salary

    @annual_salary.setter
    def annual_salary(self, amount: float) -> None:
        if amount < 0:
            raise ValueError(f"Salary cannot be negative: {amount}")
        self._annual_salary = round(float(amount), 2)

    def calculate_pay(self) -> float:
        return round(self._annual_salary / 12, 2)   # monthly

    def employment_type(self) -> str:
        return "Salaried"

    def give_raise(self, percentage: float) -> None:
        if not 0 < percentage <= 100:
            raise ValueError(f"Raise percentage must be 1–100, got {percentage}")
        old_salary = self._annual_salary
        self._annual_salary *= (1 + percentage / 100)
        self._salary_history.append({
            "date":    datetime.now().strftime("%Y-%m-%d"),
            "from":    old_salary,
            "to":      self._annual_salary,
            "pct":     percentage
        })
        print(f"  Raise applied: {self.first_name} ${old_salary:,.0f} → ${self._annual_salary:,.0f}")


class HourlyEmployee(Employee):
    """Part-time employee paid by the hour."""

    OVERTIME_RATE = 1.5
    STANDARD_HOURS = 40

    def __init__(self, first, last, department, hourly_rate: float, hours: float = 40):
        super().__init__(first, last, department)
        self._hourly_rate = hourly_rate
        self._hours_this_period = hours

    @property
    def hourly_rate(self) -> float:
        return self._hourly_rate

    def log_hours(self, hours: float) -> None:
        if hours < 0:
            raise ValueError("Hours cannot be negative")
        self._hours_this_period = hours

    def calculate_pay(self) -> float:
        h = self._hours_this_period
        if h <= self.STANDARD_HOURS:
            return round(h * self._hourly_rate, 2)
        regular  = self.STANDARD_HOURS * self._hourly_rate
        overtime = (h - self.STANDARD_HOURS) * self._hourly_rate * self.OVERTIME_RATE
        return round(regular + overtime, 2)

    def employment_type(self) -> str:
        return "Hourly"


class CommissionEmployee(SalariedEmployee):
    """Sales employee: base salary + commission on sales."""

    def __init__(self, first, last, department, base_salary: float,
                 commission_rate: float = 0.05):
        super().__init__(first, last, department, base_salary)
        self._commission_rate = commission_rate
        self._sales_total     = 0.0

    def record_sales(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Sales amount cannot be negative")
        self._sales_total += amount

    def calculate_pay(self) -> float:
        base_monthly = self._annual_salary / 12
        commission   = self._sales_total * self._commission_rate
        return round(base_monthly + commission, 2)

    def employment_type(self) -> str:
        return "Commission"

    def reset_period(self) -> None:
        self._sales_total = 0.0


# ============================================================
# DEPARTMENT CLASS
# ============================================================

class Department:
    def __init__(self, name: str, manager: Optional[SalariedEmployee] = None):
        self.name     = name
        self.manager  = manager
        self._staff:  list[Employee] = []

    def add_employee(self, emp: Employee) -> None:
        self._staff.append(emp)

    @property
    def headcount(self) -> int:
        return len([e for e in self._staff if e.is_active])

    @property
    def total_payroll(self) -> float:
        return sum(e.calculate_pay() for e in self._staff if e.is_active)

    def __str__(self) -> str:
        mgr = self.manager.full_name if self.manager else "Vacant"
        return f"{self.name} (Manager: {mgr}, {self.headcount} staff, ${self.total_payroll:,.2f}/mo)"


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 70)
    print("  EMPLOYEE MANAGEMENT SYSTEM — OOP Demo")
    print("=" * 70)

    # Create employees
    alice  = SalariedEmployee("Alice", "Johnson", "Engineering", 95000)
    bob    = HourlyEmployee("Bob",   "Smith",   "Operations",  28.50, 45)
    carol  = SalariedEmployee("Carol", "Davis",  "Management",  120000)
    dave   = CommissionEmployee("Dave", "Wilson", "Sales",       45000, 0.08)
    eve    = HourlyEmployee("Eve",   "Martinez","Engineering",  35.00, 38)

    # Record Dave's sales
    dave.record_sales(80000)

    # Give Alice a raise
    alice.give_raise(10)

    # Department
    eng_dept = Department("Engineering", alice)
    eng_dept.add_employee(alice)
    eng_dept.add_employee(eve)

    # Display payroll
    employees = [alice, bob, carol, dave, eve]
    print(f"\n  {'ID':<10} {'Name':<22} {'Dept':<14} {'Type':<12} {'Monthly Pay':>12}")
    print("  " + "=" * 74)

    total = 0
    for emp in employees:
        print(f"  {emp}")
        total += emp.calculate_pay()

    print("  " + "-" * 74)
    print(f"  {'TOTAL MONTHLY PAYROLL':>60} ${total:>10,.2f}")

    # Department summary
    print(f"\n  {eng_dept}")

    # Polymorphism demo
    print("\n  POLYMORPHISM: same calculate_pay() call, different results:")
    for emp in employees:
        print(f"  {emp.full_name:<22} ({emp.employment_type():<12}) → ${emp.calculate_pay():,.2f}")


if __name__ == "__main__":
    main()
