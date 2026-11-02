# Lesson 04 — Input & Output

**Phase:** 01 — Fundamentals | **Time:** ~30 min | **Prerequisite:** Lesson 03

---

## Part 1: Concept

### What is input()?

`input()` pauses your program and waits for the user to type something.

**Analogy:** A form on a website. The browser pauses, you type your name, you click Submit — then the form processes your input.

**Critical rule:** `input()` ALWAYS returns a string, even if the user types a number.

---

## Part 2: Basic Input

```python
# Simple input
name = input("Enter your name: ")
print("Hello, " + name)
```

Running this program:
```
Enter your name: Alice
Hello, Alice
```

---

## Part 3: Input Always Returns String

```python
age = input("Enter your age: ")
print(type(age))     # <class 'str'>  ← ALWAYS string!

# This will cause an error:
new_age = age + 1    # TypeError: can only concatenate str to str

# CORRECT — convert first:
new_age = int(age) + 1
print(f"Next year you will be {new_age}")
```

---

## Part 4: Converting Input

```python
# Get an integer
age = int(input("Enter your age: "))
print(f"In 10 years you'll be {age + 10}")

# Get a float
price = float(input("Enter price: "))
tax = price * 0.15
print(f"Tax: ${tax:.2f}")

# Keep as string
name = input("Enter your name: ")
print(f"Welcome, {name}!")
```

---

## Part 5: Output Formatting

### f-strings (Recommended)

```python
name = "Alice"
age = 30
salary = 75000.5

# Basic f-string
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Salary: {salary}")

# Formatting numbers
print(f"Salary: ${salary:,.2f}")     # $75,000.50
print(f"Salary: ${salary:.0f}")      # $75001 (no decimal)
print(f"Score: {95:5d}")             # "   95" (5 chars wide)
print(f"Pi: {3.14159:.2f}")          # 3.14

# Expressions inside f-strings
print(f"10 + 5 = {10 + 5}")          # 10 + 5 = 15
print(f"Name length: {len(name)}")   # Name length: 5
```

### format() method (older style)

```python
# format() — still used, know it when you see it
print("Name: {}".format(name))
print("Salary: ${:.2f}".format(salary))
print("{} is {} years old".format(name, age))
```

### % formatting (legacy — avoid in new code)

```python
print("Name: %s" % name)
print("Salary: $%.2f" % salary)
```

---

## Part 6: Number Formatting Reference

```python
x = 1234567.891

print(f"{x}")             # 1234567.891
print(f"{x:.2f}")         # 1234567.89  (2 decimal places)
print(f"{x:,.2f}")        # 1,234,567.89  (comma separator)
print(f"{x:>15.2f}")      # right-aligned in 15 chars
print(f"{x:<15.2f}")      # left-aligned
print(f"{x:^15.2f}")      # center-aligned

pct = 0.156
print(f"{pct:.1%}")       # 15.6%  (percentage format)

n = 42
print(f"{n:05d}")         # 00042  (zero-padded, 5 wide)
print(f"{n:+d}")          # +42    (show sign)
```

---

## Part 7: Multiple Inputs

```python
# One input at a time
first = input("First name: ")
last = input("Last name: ")
age = int(input("Age: "))
salary = float(input("Salary: $"))

print()
print("=" * 35)
print("PROFILE SUMMARY")
print("=" * 35)
print(f"Full Name: {first} {last}")
print(f"Age:       {age}")
print(f"Salary:    ${salary:,.2f}")
print("=" * 35)
```

---

## Part 8: Business Example — Age Calculator

```python
"""
Age Calculator
Calculates your age details given birth year.
"""

print("=" * 40)
print("    AGE CALCULATOR")
print("=" * 40)

current_year = 2024
birth_year = int(input("Enter your birth year: "))

age = current_year - birth_year
retirement_age = 65
years_to_retire = retirement_age - age

print()
print(f"Birth Year:      {birth_year}")
print(f"Current Year:    {current_year}")
print(f"Your Age:        {age}")
print(f"Retirement Age:  {retirement_age}")
print(f"Years to Retire: {years_to_retire}")
```

---

## Part 9: Tip Calculator

```python
"""
Tip Calculator
Splits a restaurant bill with tip.
"""

print("=" * 40)
print("    TIP CALCULATOR")
print("=" * 40)

bill = float(input("Enter bill amount: $"))
tip_pct = float(input("Enter tip percentage (e.g., 15): "))
people = int(input("Number of people: "))

tip_amount = bill * (tip_pct / 100)
total = bill + tip_amount
per_person = total / people

print()
print(f"Bill:        ${bill:.2f}")
print(f"Tip ({tip_pct}%): ${tip_amount:.2f}")
print(f"Total:       ${total:.2f}")
print(f"Per Person:  ${per_person:.2f}")
```

---

## Part 10: Common Mistakes

### Mistake 1: Not converting input

```python
# WRONG
num1 = input("Enter a number: ")
num2 = input("Enter another: ")
print(num1 + num2)    # "55" instead of 10!

# CORRECT
num1 = int(input("Enter a number: "))
num2 = int(input("Enter another: "))
print(num1 + num2)    # 10
```

### Mistake 2: Crashing on invalid input

```python
# PROBLEM: User types "abc" instead of a number
age = int(input("Age: "))   # ValueError if user types "abc"

# BETTER SOLUTION (Preview — covered in Phase 06 — Error Handling):
try:
    age = int(input("Age: "))
except ValueError:
    print("Please enter a valid number.")
```

### Mistake 3: f-string syntax error

```python
# WRONG
name = "Alice"
print(f"Hello {name")    # SyntaxError: missing }

# CORRECT
print(f"Hello {name}")
```

---

## Practice Exercises

1. Write a program that asks for two numbers and prints their sum, difference, product, and quotient.

2. Write a program that asks for a person's name and birth year, then prints: "Hello [name], you are approximately [age] years old."

3. Ask the user for a price and tax rate, then display the tax amount and total price formatted as currency.

4. What is the output?
   ```python
   x = input("Enter: ")   # User types: 5
   print(x * 3)
   ```

5. Fix this code:
   ```python
   price = input("Enter price: ")
   discount = 0.20
   final = price - (price * discount)
   print(f"Final: ${final:.2f}")
   ```

---

## Summary

| Operation | Code | Notes |
|-----------|------|-------|
| Get string input | `name = input("prompt")` | Always returns str |
| Get int input | `age = int(input("prompt"))` | Convert immediately |
| Get float input | `price = float(input("prompt"))` | Convert immediately |
| f-string | `f"Hello {name}"` | Preferred output method |
| Format decimal | `f"{x:.2f}"` | 2 decimal places |
| Format currency | `f"{x:,.2f}"` | Comma + 2 decimals |
| Format percent | `f"{x:.1%}"` | Multiply by 100 + % |

---

## Next Lesson

**[Lesson 05 → Operators](lesson-05-operators.md)**
