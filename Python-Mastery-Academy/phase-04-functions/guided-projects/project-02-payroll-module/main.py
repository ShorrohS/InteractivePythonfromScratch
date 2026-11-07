"""
Project 02 - Payroll Module
Phase 04: Functions

SKILLS PRACTICED:
  - Functions with type hints and docstrings
  - Default arguments
  - Multiple return values
  - Functions calling functions
  - Pure functions (no side effects)

HOW TO RUN:
  python main.py
"""

from typing import Optional


# ============================================================
# PAYROLL CALCULATION FUNCTIONS
# ============================================================

def calculate_gross_pay(
    hours_worked: float,
    hourly_rate: float,
    overtime_multiplier: float = 1.5,
    standard_hours: float = 40.0
) -> dict:
    """
    Calculate gross pay including overtime.
    
    Args:
        hours_worked: Total hours worked in the period
        hourly_rate: Regular hourly rate in dollars
        overtime_multiplier: Rate multiplier for overtime (default 1.5x)
        standard_hours: Hours before overtime kicks in (default 40)
    
    Returns:
        Dict with regular_pay, overtime_pay, gross_pay, overtime_hours
    """
    if hours_worked <= standard_hours:
        regular_pay   = hours_worked * hourly_rate
        overtime_pay  = 0.0
        overtime_hours = 0.0
    else:
        regular_pay    = standard_hours * hourly_rate
        overtime_hours = hours_worked - standard_hours
        overtime_pay   = overtime_hours * hourly_rate * overtime_multiplier

    gross = regular_pay + overtime_pay

    return {
        "regular_pay":    round(regular_pay, 2),
        "overtime_pay":   round(overtime_pay, 2),
        "overtime_hours": overtime_hours,
        "gross_pay":      round(gross, 2)
    }


def calculate_income_tax(gross: float, tax_rate: float = 0.20) -> float:
    """Calculate income tax on gross pay."""
    return round(gross * tax_rate, 2)


def calculate_national_insurance(gross: float, ni_rate: float = 0.12) -> float:
    """Calculate national insurance contribution."""
    return round(gross * ni_rate, 2)


def calculate_pension(gross: float, employee_rate: float = 0.05) -> float:
    """Calculate employee pension contribution."""
    return round(gross * employee_rate, 2)


def calculate_net_pay(
    gross: float,
    tax_rate: float = 0.20,
    ni_rate: float = 0.12,
    pension_rate: float = 0.05
) -> dict:
    """
    Calculate all deductions and net pay.
    
    Returns:
        Dict with all deductions and final net pay
    """
    tax     = calculate_income_tax(gross, tax_rate)
    ni      = calculate_national_insurance(gross, ni_rate)
    pension = calculate_pension(gross, pension_rate)
    total_deductions = tax + ni + pension
    net = gross - total_deductions

    return {
        "income_tax":        tax,
        "national_insurance": ni,
        "pension":           pension,
        "total_deductions":  round(total_deductions, 2),
        "net_pay":           round(net, 2)
    }


def generate_payslip(
    employee_name: str,
    employee_id: str,
    period: str,
    hours_worked: float,
    hourly_rate: float,
    tax_rate: float = 0.20,
    ni_rate: float = 0.12,
    pension_rate: float = 0.05
) -> dict:
    """
    Generate a complete payslip for one employee.
    
    Returns:
        Complete payslip as a dict
    """
    gross_info = calculate_gross_pay(hours_worked, hourly_rate)
    gross      = gross_info["gross_pay"]
    net_info   = calculate_net_pay(gross, tax_rate, ni_rate, pension_rate)

    return {
        "employee_name": employee_name,
        "employee_id":   employee_id,
        "period":        period,
        "hours_worked":  hours_worked,
        "hourly_rate":   hourly_rate,
        **gross_info,
        **net_info
    }


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def print_payslip(payslip: dict) -> None:
    """Print a formatted payslip."""
    w = 48
    print("=" * w)
    print(f"  PAYSLIP")
    print("=" * w)
    print(f"  Employee:  {payslip['employee_name']}")
    print(f"  ID:        {payslip['employee_id']}")
    print(f"  Period:    {payslip['period']}")
    print("-" * w)
    print(f"  EARNINGS")
    print(f"  {'Hours Worked:':<28} {payslip['hours_worked']:.1f}h")
    print(f"  {'Hourly Rate:':<28} ${payslip['hourly_rate']:.2f}")
    if payslip["overtime_hours"] > 0:
        print(f"  {'Overtime Hours:':<28} {payslip['overtime_hours']:.1f}h (x1.5)")
        print(f"  {'Overtime Pay:':<28} ${payslip['overtime_pay']:,.2f}")
    print(f"  {'Regular Pay:':<28} ${payslip['regular_pay']:,.2f}")
    print(f"  {'Gross Pay:':<28} ${payslip['gross_pay']:,.2f}")
    print("-" * w)
    print(f"  DEDUCTIONS")
    print(f"  {'Income Tax:':<28} ${payslip['income_tax']:,.2f}")
    print(f"  {'National Insurance:':<28} ${payslip['national_insurance']:,.2f}")
    print(f"  {'Pension (5%):':<28} ${payslip['pension']:,.2f}")
    print(f"  {'Total Deductions:':<28} ${payslip['total_deductions']:,.2f}")
    print("=" * w)
    print(f"  {'NET PAY:':<28} ${payslip['net_pay']:,.2f}")
    print("=" * w)


def print_payroll_summary(payslips: list[dict]) -> None:
    """Print payroll summary for all employees."""
    print(f"\n{'='*65}")
    print(f"  PAYROLL SUMMARY")
    print(f"{'='*65}")
    print(f"  {'Name':<20} {'Gross':>10} {'Deductions':>12} {'Net':>10}")
    print(f"  {'-'*57}")

    totals = {"gross": 0, "deductions": 0, "net": 0}
    for p in payslips:
        print(f"  {p['employee_name']:<20} ${p['gross_pay']:>9,.2f} "
              f"${p['total_deductions']:>11,.2f} ${p['net_pay']:>9,.2f}")
        totals["gross"]      += p["gross_pay"]
        totals["deductions"] += p["total_deductions"]
        totals["net"]        += p["net_pay"]

    print(f"  {'-'*57}")
    print(f"  {'TOTALS':<20} ${totals['gross']:>9,.2f} "
          f"${totals['deductions']:>11,.2f} ${totals['net']:>9,.2f}")
    print(f"  Total employees: {len(payslips)}")
    print(f"{'='*65}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 55)
    print("  PAYROLL MODULE DEMO")
    print("=" * 55)

    # Employee data
    employees = [
        {"name": "Alice Johnson",  "id": "E001", "hours": 45.0, "rate": 35.00},
        {"name": "Bob Smith",      "id": "E002", "hours": 40.0, "rate": 28.50},
        {"name": "Carol Davis",    "id": "E003", "hours": 50.0, "rate": 42.00},
        {"name": "Dave Wilson",    "id": "E004", "hours": 38.5, "rate": 25.00},
        {"name": "Eve Martinez",   "id": "E005", "hours": 40.0, "rate": 55.00},
    ]

    period = "January 2024"
    payslips = []

    for emp in employees:
        payslip = generate_payslip(
            employee_name=emp["name"],
            employee_id=emp["id"],
            period=period,
            hours_worked=emp["hours"],
            hourly_rate=emp["rate"]
        )
        payslips.append(payslip)

    # Show individual payslip for first employee
    print_payslip(payslips[0])

    # Show summary for all
    print_payroll_summary(payslips)


if __name__ == "__main__":
    main()
