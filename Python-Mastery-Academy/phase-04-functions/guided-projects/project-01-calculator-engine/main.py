"""
Project 01 — Calculator Engine
Phase 04: Functions

SKILLS PRACTICED:
  - Defining functions with type hints
  - Parameters and return values
  - Error handling in functions
  - Organizing code with functions

HOW TO RUN:
  python main.py
"""

import math


# ============================================================
# BASIC OPERATIONS
# ============================================================

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b


def divide(a: float, b: float) -> float | None:
    """Divide a by b. Returns None if b is zero."""
    if b == 0:
        return None
    return a / b


def modulo(a: float, b: float) -> float | None:
    """Return remainder of a / b."""
    if b == 0:
        return None
    return a % b


def power(base: float, exponent: float) -> float:
    """Raise base to exponent."""
    return base ** exponent


# ============================================================
# ADVANCED OPERATIONS
# ============================================================

def square_root(n: float) -> float | None:
    """Square root. Returns None for negative numbers."""
    if n < 0:
        return None
    return math.sqrt(n)


def percentage(value: float, total: float) -> float | None:
    """Calculate what percentage value is of total."""
    if total == 0:
        return None
    return (value / total) * 100


def percentage_of(percent: float, total: float) -> float:
    """Calculate percent% of total."""
    return (percent / 100) * total


# ============================================================
# FINANCIAL OPERATIONS
# ============================================================

def simple_interest(principal: float, rate: float, years: int) -> float:
    """Calculate simple interest."""
    return principal * (rate / 100) * years


def compound_interest(principal: float, rate: float, years: int, n: int = 12) -> float:
    """
    Calculate compound interest.
    n = number of times interest compounds per year (default: monthly)
    """
    monthly_rate = rate / 100 / n
    return principal * ((1 + monthly_rate) ** (n * years)) - principal


def emi(principal: float, annual_rate: float, years: int) -> float:
    """
    Calculate EMI (Equated Monthly Installment).
    Returns monthly payment amount.
    """
    r = (annual_rate / 100) / 12
    n = years * 12
    if r == 0:
        return principal / n
    return principal * r * (1 + r) ** n / ((1 + r) ** n - 1)


# ============================================================
# DISPLAY HELPER
# ============================================================

def display_result(operation: str, result) -> None:
    """Display a formatted operation result."""
    if result is None:
        print(f"  {operation}: ⚠️  Error (division by zero or invalid input)")
    else:
        print(f"  {operation}: {result:.6g}")


def display_separator(char: str = "─", width: int = 50) -> None:
    """Display a separator line."""
    print(char * width)


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    """Main calculator application."""
    
    print("=" * 50)
    print("     PYTHON CALCULATOR ENGINE")
    print("     Powered by Functions")
    print("=" * 50)
    print()
    
    a = float(input("Enter first number:  "))
    b = float(input("Enter second number: "))
    
    print()
    print("─" * 50)
    print("  BASIC OPERATIONS")
    print("─" * 50)
    
    display_result(f"{a} + {b}", add(a, b))
    display_result(f"{a} - {b}", subtract(a, b))
    display_result(f"{a} × {b}", multiply(a, b))
    display_result(f"{a} ÷ {b}", divide(a, b))
    display_result(f"{a} % {b}", modulo(a, b))
    display_result(f"{a} ^ {b}", power(a, b))
    
    print()
    print("─" * 50)
    print("  ADVANCED")
    print("─" * 50)
    
    display_result(f"√{a}", square_root(a))
    display_result(f"√{b}", square_root(b))
    display_result(f"{a} is {percentage(a, a+b):.1f}% of {a+b}", percentage(a, a + b))
    
    print()
    print("─" * 50)
    print("  FINANCIAL (treating numbers as loan params)")
    print("─" * 50)
    
    principal, rate = abs(a) or 10000, abs(b) or 5
    years = 3
    
    si = simple_interest(principal, rate, years)
    ci = compound_interest(principal, rate, years)
    monthly = emi(principal, rate, years)
    
    print(f"  Principal: ${principal:,.2f}, Rate: {rate}%, Years: {years}")
    print(f"  Simple Interest:   ${si:,.2f}")
    print(f"  Compound Interest: ${ci:,.2f}")
    print(f"  Monthly EMI:       ${monthly:,.2f}")
    
    print()
    print("=" * 50)


if __name__ == "__main__":
    main()
