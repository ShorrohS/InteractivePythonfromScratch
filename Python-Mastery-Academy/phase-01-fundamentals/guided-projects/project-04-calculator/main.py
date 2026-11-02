"""
Project 04 — Calculator
Phase 01: Python Fundamentals

SKILLS PRACTICED:
  - Arithmetic operators
  - User input and type conversion
  - f-string formatting
  - Division by zero awareness

HOW TO RUN:
  python main.py
"""

import math


def display_header() -> None:
    """Display calculator header."""
    print("=" * 45)
    print("         PYTHON CALCULATOR")
    print("=" * 45)


def get_number(prompt: str) -> float:
    """Get a number from the user."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  ⚠️  Invalid input. Enter a number.")


def display_result(operation: str, a: float, b: float, result) -> None:
    """Display a formatted calculation result."""
    if result is not None:
        print(f"  {a} {operation} {b} = {result}")
    else:
        print(f"  ⚠️  Cannot divide by zero!")


def main():
    """Main calculator function."""
    
    display_header()
    print()
    
    a = get_number("Enter first number:  ")
    b = get_number("Enter second number: ")
    
    print()
    print("─" * 45)
    print("  RESULTS")
    print("─" * 45)
    
    # Arithmetic operations
    print(f"\n  {'Addition:':<20} {a} + {b} = {a + b}")
    print(f"  {'Subtraction:':<20} {a} - {b} = {a - b}")
    print(f"  {'Multiplication:':<20} {a} × {b} = {a * b}")
    
    # Division — guard against zero
    if b != 0:
        print(f"  {'Division:':<20} {a} ÷ {b} = {a / b:.6f}")
        print(f"  {'Floor Division:':<20} {a} ÷ {b} = {a // b}")
        print(f"  {'Modulo:':<20} {a} % {b} = {a % b}")
    else:
        print(f"  {'Division:':<20} Cannot divide by zero!")
        print(f"  {'Floor Division:':<20} Cannot divide by zero!")
        print(f"  {'Modulo:':<20} Cannot divide by zero!")
    
    print(f"  {'Exponentiation:':<20} {a} ^ {b} = {a ** b}")
    
    # Advanced operations
    print()
    print("─" * 45)
    print("  ADVANCED")
    print("─" * 45)
    
    if a >= 0:
        print(f"  √{a} = {math.sqrt(a):.6f}")
    if b >= 0:
        print(f"  √{b} = {math.sqrt(b):.6f}")
    
    print(f"  |{a}| = {abs(a)}")
    print(f"  |{b}| = {abs(b)}")
    print(f"  max({a}, {b}) = {max(a, b)}")
    print(f"  min({a}, {b}) = {min(a, b)}")
    
    if a > 0 and b > 0:
        log_a = math.log10(a)
        log_b = math.log10(b)
        print(f"  log₁₀({a}) = {log_a:.4f}")
        print(f"  log₁₀({b}) = {log_b:.4f}")
    
    print()
    print("=" * 45)
    print("  Calculation complete!")
    print("=" * 45)


if __name__ == "__main__":
    main()
