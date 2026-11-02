# Lesson 01 — Functions: Basics

**Phase:** 04 — Functions | **Time:** ~30 min

---

## Part 1: What is a Function?

A function is a **named, reusable block of code** that performs a specific task.

**Analogy:** A toaster has one job. You put bread in, press the lever, get toast out. You don't need to understand how the heating elements work — you just use it. Functions are the same: define the task once, use it anywhere.

---

## Part 2: Defining and Calling

```python
# DEFINE (blueprint)
def say_hello():
    print("Hello, World!")

# CALL (use it)
say_hello()        # Hello, World!
say_hello()        # Hello, World!  (use it again)
say_hello()        # Hello, World!  (and again)
```

Structure:
```
def function_name():
    body  ← indented 4 spaces
```

---

## Part 3: Parameters and Return Values

```python
# With parameter (input)
def greet(name: str) -> None:
    print(f"Hello, {name}!")

greet("Alice")    # Hello, Alice!
greet("Bob")      # Hello, Bob!

# With return value (output)
def add(a: int, b: int) -> int:
    return a + b

result = add(10, 5)
print(result)          # 15
print(add(100, 200))   # 300

# Multiple return values
def min_max(numbers: list) -> tuple:
    return min(numbers), max(numbers)

low, high = min_max([3, 1, 7, 5, 2])
print(f"Min: {low}, Max: {high}")   # Min: 1, Max: 7
```

---

## Part 4: Type Hints

Type hints make your code clearer and catch bugs earlier:

```python
# Without type hints
def calculate_tax(amount, rate):
    return amount * rate

# With type hints (PROFESSIONAL STANDARD)
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax amount.
    
    Args:
        amount: The base amount
        rate: Tax rate as decimal (e.g., 0.15 for 15%)
    
    Returns:
        The tax amount
    """
    return amount * rate

tax = calculate_tax(1000.0, 0.15)
print(f"Tax: ${tax}")   # Tax: $150.0
```

---

## Part 5: Docstrings

Every function should have a docstring:

```python
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate Body Mass Index.
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
        
    Returns:
        BMI value as float
        
    Example:
        >>> calculate_bmi(70, 1.75)
        22.86
    """
    return weight_kg / (height_m ** 2)
```

---

## Part 6: Functions Calling Functions

```python
def get_first_name(full_name: str) -> str:
    return full_name.split()[0]

def get_last_name(full_name: str) -> str:
    return full_name.split()[-1]

def format_employee_id(full_name: str, number: int) -> str:
    first = get_first_name(full_name)
    last = get_last_name(full_name)
    return f"{first[0].upper()}{last.upper()}{number:04d}"

name = "Alice Johnson"
emp_id = format_employee_id(name, 42)
print(emp_id)   # AJOHNSON0042
```

---

## Part 7: Business Example

```python
"""
Payroll calculation functions — reusable across the application.
"""

INCOME_TAX_RATE = 0.20
NATIONAL_INSURANCE_RATE = 0.12

def calculate_gross_pay(hours: float, hourly_rate: float) -> float:
    """Calculate gross pay from hours worked."""
    overtime_hours = max(0, hours - 40)
    regular_hours = min(hours, 40)
    regular_pay = regular_hours * hourly_rate
    overtime_pay = overtime_hours * hourly_rate * 1.5
    return regular_pay + overtime_pay

def calculate_income_tax(gross: float) -> float:
    """Calculate income tax (20% flat rate)."""
    return gross * INCOME_TAX_RATE

def calculate_net_pay(gross: float) -> float:
    """Calculate net pay after all deductions."""
    income_tax = calculate_income_tax(gross)
    national_insurance = gross * NATIONAL_INSURANCE_RATE
    return gross - income_tax - national_insurance

# Use the functions
hours_worked = 45
rate = 25.00

gross = calculate_gross_pay(hours_worked, rate)
tax = calculate_income_tax(gross)
net = calculate_net_pay(gross)

print(f"Gross Pay:    ${gross:,.2f}")
print(f"Income Tax:   ${tax:,.2f}")
print(f"Net Pay:      ${net:,.2f}")
```

---

## Practice Exercises

1. Write a function `is_even(n)` that returns True if n is even.

2. Write a function `celsius_to_fahrenheit(c)` and `fahrenheit_to_celsius(f)`.

3. Write a function `word_count(text)` that returns the number of words.

4. Write a function `calculate_circle_area(radius)` using `math.pi`.

5. Write a function `format_currency(amount, symbol='$')` that formats a number as currency.

---

## Next Lesson

**[Lesson 02 → Parameters & Return Values](lesson-02-parameters.md)**
