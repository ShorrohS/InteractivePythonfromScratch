# Lesson 03 — Data Types

**Phase:** 01 — Fundamentals | **Time:** ~45 min | **Prerequisite:** Lesson 02

---

## Part 1: The 4 Core Data Types

Python has four fundamental data types you must know:

```
┌─────────┬───────────────────┬────────────────────┐
│ Type    │ What it stores    │ Example            │
├─────────┼───────────────────┼────────────────────┤
│ int     │ Whole numbers     │ 42, -10, 0         │
│ float   │ Decimal numbers   │ 3.14, -0.5, 100.0  │
│ str     │ Text / characters │ "Alice", "Python"  │
│ bool    │ True or False     │ True, False         │
└─────────┴───────────────────┴────────────────────┘
```

---

## Part 2: Integer (int)

Whole numbers — no decimal point.

```python
# Positive
age = 30
employees = 500
year = 2024

# Negative
temperature = -10
debt = -50000

# Zero
count = 0

# Large numbers — use underscores for readability
population = 8_000_000_000    # 8 billion
salary = 150_000

print(type(age))      # <class 'int'>
print(type(-10))      # <class 'int'>
```

**What can you do with int:**
```python
a = 10
b = 3

print(a + b)    # 13  (addition)
print(a - b)    # 7   (subtraction)
print(a * b)    # 30  (multiplication)
print(a // b)   # 3   (floor division — no decimal)
print(a % b)    # 1   (modulo — remainder)
print(a ** b)   # 1000 (exponentiation)
```

---

## Part 3: Float

Numbers with a decimal point.

```python
price = 19.99
height = 5.8
pi = 3.14159
tax_rate = 0.15

print(type(price))    # <class 'float'>
```

**Float arithmetic:**
```python
a = 10.0
b = 3.0

print(a / b)          # 3.3333333333333335
print(a + b)          # 13.0
print(round(a / b, 2)) # 3.33  (round to 2 decimal places)
```

**Int division produces float:**
```python
print(10 / 3)    # 3.3333...  (regular division — always float)
print(10 // 3)   # 3          (floor division — always int)
```

**Floating point precision:**
```python
print(0.1 + 0.2)   # 0.30000000000000004  (floating point quirk)
# Fix:
print(round(0.1 + 0.2, 2))   # 0.3
```

---

## Part 4: String (str)

Text — anything between quotes.

```python
# Single or double quotes — both valid
name1 = "Alice"
name2 = 'Bob'

# Multi-line string
address = """123 Main Street
             New York, NY 10001"""

# Empty string
blank = ""

# String with numbers (still a string!)
phone = "555-1234"
zip_code = "10001"

print(type(name1))   # <class 'str'>
print(type("99"))    # <class 'str'> — NOT an int!
```

**String operations:**
```python
first = "Hello"
second = "World"

# Concatenation (joining)
full = first + " " + second
print(full)          # Hello World

# Repetition
line = "-" * 30
print(line)          # ------------------------------ 

# Length
print(len(full))     # 11
```

---

## Part 5: Boolean (bool)

Only two possible values: `True` or `False`.

```python
is_active = True
is_deleted = False
has_permission = True

print(type(is_active))   # <class 'bool'>
```

Booleans come from comparisons:
```python
age = 20
print(age >= 18)    # True
print(age < 18)     # False
print(age == 20)    # True  (== checks equality)
print(age != 20)    # False (!= checks inequality)
```

---

## Part 6: Type Conversion

Convert between types:

```python
# String to integer
age_str = "25"
age_int = int(age_str)
print(age_int + 5)    # 30

# String to float
price_str = "19.99"
price_float = float(price_str)
print(price_float * 2)    # 39.98

# Integer to string
age = 30
age_str = str(age)
print("Age: " + age_str)   # Age: 30  (can't do "Age: " + 30)

# Integer to float
x = 5
y = float(x)
print(y)    # 5.0

# Float to integer (truncates decimal)
pi = 3.99
pi_int = int(pi)
print(pi_int)    # 3  (not rounded, truncated!)

# Boolean conversions
print(int(True))    # 1
print(int(False))   # 0
print(bool(0))      # False
print(bool(1))      # True
print(bool(""))     # False (empty string is falsy)
print(bool("hi"))   # True  (non-empty string is truthy)
```

---

## Part 7: Checking Types

```python
name = "Alice"
age = 30

# type() — returns the type
print(type(name))            # <class 'str'>

# isinstance() — checks if it IS a type (preferred in professional code)
print(isinstance(name, str))    # True
print(isinstance(age, int))     # True
print(isinstance(age, float))   # False
print(isinstance(age, (int, float)))   # True — check multiple types
```

---

## Part 8: Business Example

```python
# Product catalog entry
product_name = "Laptop Pro 15"     # str
product_id = 10042                  # int
price = 1299.99                     # float
in_stock = True                     # bool
quantity = 50                       # int
discount_rate = 0.10                # float

# Calculate discounted price
discounted_price = price * (1 - discount_rate)
final_price = round(discounted_price, 2)

print("=" * 40)
print(f"Product: {product_name}")
print(f"ID:      #{product_id}")
print(f"Price:   ${price}")
print(f"Sale:    ${final_price} (10% off)")
print(f"Stock:   {quantity} units")
print(f"Available: {in_stock}")
print("=" * 40)
```

---

## Part 9: Common Mistakes

### Mistake 1: Mixing string and number

```python
# WRONG
age = 30
print("Age: " + age)    # TypeError: can only concatenate str to str

# CORRECT
print("Age: " + str(age))
print(f"Age: {age}")    # f-string (easiest)
print("Age:", age)       # comma — auto-converts
```

### Mistake 2: Invalid type conversion

```python
# WRONG
x = int("hello")    # ValueError: invalid literal for int()

# CORRECT — only convert if the string IS a valid number
x = int("42")       # ✅ Works
y = float("3.14")   # ✅ Works
```

### Mistake 3: Float comparison

```python
# WRONG — unreliable
if 0.1 + 0.2 == 0.3:
    print("Equal")    # Does NOT print (0.1+0.2 = 0.30000000000004)

# CORRECT
import math
if math.isclose(0.1 + 0.2, 0.3):
    print("Equal")    # Prints correctly

# Or: round then compare
if round(0.1 + 0.2, 10) == 0.3:
    print("Equal")
```

---

## Part 10: Practice Exercises

1. Create one variable of each type (int, float, str, bool). Print each with its type.

2. What is the output?
   ```python
   x = "5"
   y = 10
   print(int(x) + y)
   ```

3. Convert `3.7` to an integer. What is the result? Why?

4. What is wrong with this code and how do you fix it?
   ```python
   score = 95
   message = "Your score is: " + score
   print(message)
   ```

5. Predict the output:
   ```python
   print(bool(0))
   print(bool(""))
   print(bool("False"))
   print(bool(0.0))
   print(bool(100))
   ```

---

## Summary

| Type | Example | Convert To |
|------|---------|-----------|
| `int` | `42`, `-5`, `0` | `int("42")`, `int(3.9)` |
| `float` | `3.14`, `-0.5` | `float("3.14")`, `float(5)` |
| `str` | `"hello"`, `"42"` | `str(42)`, `str(3.14)` |
| `bool` | `True`, `False` | `bool(0)`, `bool("")` |

---

## Next Lesson

**[Lesson 04 → Input & Output](lesson-04-input-output.md)**
