# Lesson 07 — Lambda Functions

**Phase:** 04 — Functions | **Time:** ~20 min

---

## Part 1: What is a Lambda?

A lambda is a small, anonymous (nameless) function defined in one line.

```python
# Normal function
def square(x):
    return x ** 2

# Lambda equivalent
square = lambda x: x ** 2

# Both work the same way
print(square(5))     # 25
```

Syntax: `lambda parameters: expression`

---

## Part 2: When to Use Lambdas

Lambdas are best as arguments to other functions — especially `sorted()`, `map()`, `filter()`.

```python
employees = [
    {"name": "Carol", "salary": 90000},
    {"name": "Alice", "salary": 75000},
    {"name": "Bob",   "salary": 85000},
]

# Sort by salary using lambda
by_salary = sorted(employees, key=lambda e: e["salary"])
# Sort by name descending
by_name_desc = sorted(employees, key=lambda e: e["name"], reverse=True)

# map() — apply function to every item
prices = [100, 200, 350, 80]
with_tax = list(map(lambda p: p * 1.10, prices))

# filter() — keep items matching condition
high_prices = list(filter(lambda p: p > 150, prices))

# Combined: high prices with tax
result = list(map(lambda p: p * 1.10,
               filter(lambda p: p > 150, prices)))
```

---

## Part 3: Lambda vs def

```python
# Use def when:
# - The logic is more than one expression
# - You need it in multiple places
# - Clarity matters more than brevity

def calculate_bonus(salary: float, rating: int) -> float:
    """Complex multi-step logic → use def."""
    if rating >= 4:
        rate = 0.20
    elif rating >= 3:
        rate = 0.10
    else:
        rate = 0.05
    return salary * rate

# Use lambda when:
# - Simple one-expression logic
# - Used as argument to another function
# - Throwaway function you won't reuse

sorter = lambda item: (item["dept"], -item["salary"])   # sort by dept, then salary desc
```

---

## Part 4: map, filter, reduce

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map — transform each item
doubled   = list(map(lambda n: n * 2, numbers))
as_str    = list(map(str, numbers))   # built-in without lambda

# filter — keep matching items
evens     = list(filter(lambda n: n % 2 == 0, numbers))
positives = list(filter(lambda n: n > 0, numbers))

# reduce — fold list into single value
total = reduce(lambda acc, n: acc + n, numbers)   # sum
product = reduce(lambda acc, n: acc * n, [1,2,3,4,5])  # factorial 5!

# Note: list comprehensions are often more readable than map/filter
doubled = [n * 2 for n in numbers]
evens   = [n for n in numbers if n % 2 == 0]
```

---

## Part 5: Practical Business Use

```python
transactions = [
    {"date": "2024-01-15", "amount": 1500, "type": "credit"},
    {"date": "2024-01-20", "amount": 300,  "type": "debit"},
    {"date": "2024-02-05", "amount": 2200, "type": "credit"},
    {"date": "2024-02-12", "amount": 450,  "type": "debit"},
]

# Sort by amount (largest first)
by_amount = sorted(transactions, key=lambda t: t["amount"], reverse=True)

# Credits only
credits = list(filter(lambda t: t["type"] == "credit", transactions))

# Total credits
total = sum(map(lambda t: t["amount"], credits))

# Apply 10% service charge to debits
charged = list(map(
    lambda t: {**t, "amount": t["amount"] * 1.10} if t["type"] == "debit" else t,
    transactions
))
```

---

## Practice Exercises

1. Use `sorted()` with a lambda to sort a list of tuples `(name, age)` by age descending.

2. Use `filter()` with a lambda to keep only strings longer than 5 chars.

3. Use `map()` to convert a list of temperatures from Celsius to Fahrenheit.

4. When should you use a list comprehension instead of `map()` + `lambda`?

---

## Phase 04 Complete — Build the Projects!

**[Project 01 → Calculator Engine](../guided-projects/project-01-calculator-engine/)**
**[Project 02 → Payroll Module](../guided-projects/project-02-payroll-module/)**
**[Project 03 → Report Generator](../guided-projects/project-03-report-generator/)**
