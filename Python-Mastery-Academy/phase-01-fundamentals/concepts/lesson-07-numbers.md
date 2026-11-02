# Lesson 07 — Numbers & the Math Module

**Phase:** 01 — Fundamentals | **Time:** ~30 min | **Prerequisite:** Lesson 06

---

## Part 1: Number Types Review

```python
# Integer
x = 42
# Float
y = 3.14
# Complex (less common)
z = 3 + 4j

print(type(x))    # <class 'int'>
print(type(y))    # <class 'float'>
print(type(z))    # <class 'complex'>
```

---

## Part 2: Number Limits

```python
# Python integers have no size limit
big = 10 ** 100    # a googol — Python handles this fine!
print(big)

# Floats have limits
import sys
print(sys.float_info.max)    # ~1.8e+308
print(sys.float_info.min)    # ~5e-324

# Infinity
pos_inf = float("inf")
neg_inf = float("-inf")
print(pos_inf > 999999)   # True
```

---

## Part 3: Built-in Number Functions

```python
# abs() — absolute value
print(abs(-42))    # 42
print(abs(42))     # 42

# round() — round to n decimal places
print(round(3.14159, 2))    # 3.14
print(round(3.7))            # 4  (rounds to nearest int)
print(round(2.5))            # 2  (Python uses banker's rounding)
print(round(3.5))            # 4

# max() and min()
print(max(10, 20, 30))    # 30
print(min(10, 20, 30))    # 10
numbers = [5, 2, 8, 1, 9]
print(max(numbers))        # 9
print(min(numbers))        # 1

# sum()
print(sum([10, 20, 30]))   # 60

# pow() — same as **
print(pow(2, 10))          # 1024
print(pow(2, 10, 100))     # 24  (2**10 % 100 — modular exponentiation)

# divmod() — returns quotient and remainder
quotient, remainder = divmod(17, 5)
print(quotient)    # 3
print(remainder)   # 2
```

---

## Part 4: The math Module

```python
import math

# Constants
print(math.pi)       # 3.141592653589793
print(math.e)        # 2.718281828459045
print(math.inf)      # inf
print(math.tau)      # 6.283... (2*pi)

# Rounding
print(math.floor(3.9))    # 3  (always rounds down)
print(math.ceil(3.1))     # 4  (always rounds up)
print(math.trunc(3.9))    # 3  (truncates decimal)

# Powers and roots
print(math.sqrt(16))      # 4.0
print(math.sqrt(2))       # 1.4142135623730951
print(math.pow(2, 10))    # 1024.0 (always float)
print(math.log(100, 10))  # 2.0 (log base 10 of 100)
print(math.log(math.e))   # 1.0 (natural log)

# Trigonometry
print(math.sin(math.pi / 2))    # 1.0
print(math.cos(0))               # 1.0
print(math.degrees(math.pi))    # 180.0
print(math.radians(180))        # 3.14159...

# Factorial
print(math.factorial(5))    # 120 (5! = 5×4×3×2×1)

# GCD and LCM
print(math.gcd(48, 36))     # 12
print(math.lcm(4, 6))       # 12

# Comparison (fixes floating point issues)
print(math.isclose(0.1 + 0.2, 0.3))    # True
```

---

## Part 5: Number Formatting

```python
number = 1234567.891

# f-string formatting
print(f"{number}")            # 1234567.891
print(f"{number:.2f}")        # 1234567.89
print(f"{number:,.2f}")       # 1,234,567.89
print(f"{number:.2e}")        # 1.23e+06 (scientific notation)

# Built-in format() function
print(format(number, ",.2f"))   # 1,234,567.89

# Percentage
rate = 0.156
print(f"{rate:.1%}")   # 15.6%
print(f"{rate:.2%}")   # 15.60%

# Binary, octal, hex
n = 255
print(f"{n:b}")    # 11111111  (binary)
print(f"{n:o}")    # 377       (octal)
print(f"{n:x}")    # ff        (hex lowercase)
print(f"{n:X}")    # FF        (hex uppercase)
print(bin(n))      # 0b11111111
print(oct(n))      # 0o377
print(hex(n))      # 0xff
```

---

## Part 6: Random Numbers

```python
import random

# Random float between 0 and 1
print(random.random())    # e.g., 0.7234...

# Random integer between a and b (inclusive)
print(random.randint(1, 10))    # e.g., 7

# Random float between a and b
print(random.uniform(1.0, 10.0))   # e.g., 6.54

# Random choice from a list
options = ["rock", "paper", "scissors"]
print(random.choice(options))    # e.g., "paper"

# Shuffle a list in-place
cards = [1, 2, 3, 4, 5]
random.shuffle(cards)
print(cards)    # e.g., [3, 1, 5, 2, 4]

# Sample without replacement
nums = list(range(1, 50))
lottery = random.sample(nums, 6)
print(lottery)   # 6 unique random numbers 1-49
```

---

## Part 7: Business Example — Interest Calculator

```python
"""
Interest Calculator
Calculates simple and compound interest.
"""
import math

print("=" * 45)
print("   INTEREST CALCULATOR")
print("=" * 45)

principal = float(input("Principal amount ($): "))
rate = float(input("Annual interest rate (%): ")) / 100
years = int(input("Number of years: "))

# Simple interest
simple_interest = principal * rate * years
simple_total = principal + simple_interest

# Compound interest (annually)
compound_total = principal * math.pow(1 + rate, years)
compound_interest = compound_total - principal

print()
print("RESULTS")
print("-" * 35)
print(f"Principal:               ${principal:>10,.2f}")
print()
print(f"Simple Interest:         ${simple_interest:>10,.2f}")
print(f"Simple Total:            ${simple_total:>10,.2f}")
print()
print(f"Compound Interest:       ${compound_interest:>10,.2f}")
print(f"Compound Total:          ${compound_total:>10,.2f}")
print()
difference = compound_total - simple_total
print(f"Compound benefit:        ${difference:>10,.2f} more")
print("-" * 35)
```

---

## Practice Exercises

1. Write a program that asks for a circle's radius and calculates:
   - Circumference (2πr)
   - Area (πr²)

2. Write a number guesser: generate a random number 1-100, ask the user to guess, and tell them "Higher" or "Lower". (Hint: use `random.randint`)

3. What is the output?
   ```python
   import math
   print(math.floor(4.9))
   print(math.ceil(4.1))
   print(round(4.5))
   print(round(5.5))
   ```

4. Calculate the hypotenuse of a right triangle given two sides using the Pythagorean theorem (hint: `math.sqrt`).

5. What is wrong?
   ```python
   print(math.sqrt(-1))
   ```

---

## Summary

| Function | Purpose | Example |
|----------|---------|---------|
| `abs(x)` | Absolute value | `abs(-5)` → `5` |
| `round(x, n)` | Round to n decimals | `round(3.14159, 2)` → `3.14` |
| `max(...)` | Maximum value | `max(1,5,3)` → `5` |
| `min(...)` | Minimum value | `min(1,5,3)` → `1` |
| `sum(list)` | Sum of list | `sum([1,2,3])` → `6` |
| `math.sqrt(x)` | Square root | `math.sqrt(16)` → `4.0` |
| `math.floor(x)` | Round down | `math.floor(3.9)` → `3` |
| `math.ceil(x)` | Round up | `math.ceil(3.1)` → `4` |
| `math.pi` | Pi constant | `3.14159...` |
| `random.randint(a,b)` | Random int | `random.randint(1,10)` |

---

## Next Lesson

**[Lesson 08 → Boolean Logic](lesson-08-boolean-logic.md)**
