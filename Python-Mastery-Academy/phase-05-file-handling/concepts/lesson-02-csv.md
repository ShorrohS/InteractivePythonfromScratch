# Lesson 02 — CSV Files

**Phase:** 05 — File Handling | **Time:** ~30 min

---

## What is CSV?

CSV = Comma-Separated Values. A simple text format for storing tabular data.

```
name,age,salary,department
Alice,30,75000,Engineering
Bob,25,55000,Marketing
Carol,35,90000,Engineering
```

Every spreadsheet can be exported as CSV. Every database can import CSV. It's the universal data exchange format.

---

## Part 2: Writing CSV

```python
import csv

# Write rows
employees = [
    ["name", "age", "salary", "department"],   # header
    ["Alice", 30, 75000, "Engineering"],
    ["Bob", 25, 55000, "Marketing"],
    ["Carol", 35, 90000, "Engineering"],
]

with open("employees.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(employees)    # Write all rows at once

# DictWriter (more readable)
fieldnames = ["name", "age", "salary", "department"]
employees_dict = [
    {"name": "Alice", "age": 30, "salary": 75000, "department": "Engineering"},
    {"name": "Bob", "age": 25, "salary": 55000, "department": "Marketing"},
]

with open("employees.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()       # Write header row
    writer.writerows(employees_dict)
```

---

## Part 3: Reading CSV

```python
import csv

# Basic reader
with open("employees.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)    # Skip header row
    for row in reader:
        name, age, salary, dept = row
        print(f"{name}: ${int(salary):,}")

# DictReader (preferred — access by column name)
with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['name']} earns ${row['salary']}")

# Read all into list of dicts
with open("employees.csv", "r") as f:
    employees = list(csv.DictReader(f))

print(employees[0])   # {'name': 'Alice', 'age': '30', ...}
# Note: ALL values are strings! Convert as needed:
alice_salary = int(employees[0]["salary"])
```

---

## Part 4: CSV with Type Conversion

```python
import csv

def read_employees(filename: str) -> list[dict]:
    """Read employee CSV and convert types properly."""
    employees = []
    with open(filename, "r") as f:
        for row in csv.DictReader(f):
            employees.append({
                "name": row["name"],
                "age": int(row["age"]),
                "salary": float(row["salary"]),
                "department": row["department"]
            })
    return employees
```

---

## Part 5: Business Example — Expense Tracker

```python
"""CSV-based expense tracker."""

import csv
import os
from datetime import datetime

EXPENSE_FILE = "expenses.csv"
FIELDNAMES = ["date", "category", "description", "amount"]

def initialize_file():
    if not os.path.exists(EXPENSE_FILE):
        with open(EXPENSE_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()

def add_expense(category: str, description: str, amount: float) -> None:
    with open(EXPENSE_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writerow({
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": category,
            "description": description,
            "amount": amount
        })

def get_expenses() -> list[dict]:
    with open(EXPENSE_FILE, "r") as f:
        return [
            {**row, "amount": float(row["amount"])}
            for row in csv.DictReader(f)
        ]

def summarize_by_category() -> dict:
    expenses = get_expenses()
    totals = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0) + exp["amount"]
    return totals

# Usage
initialize_file()
add_expense("Food", "Lunch at restaurant", 25.50)
add_expense("Transport", "Uber to office", 12.00)
add_expense("Food", "Groceries", 85.00)
add_expense("Utilities", "Electric bill", 120.00)

print("Expenses by Category:")
for cat, total in summarize_by_category().items():
    print(f"  {cat:<15} ${total:,.2f}")

total = sum(e["amount"] for e in get_expenses())
print(f"\n  TOTAL: ${total:,.2f}")
```

---

## Common Mistakes

```python
# Mistake 1: Forgetting newline="" on Windows (creates blank rows)
with open("data.csv", "w") as f:          # WRONG on Windows
    writer = csv.writer(f)

with open("data.csv", "w", newline="") as f:   # CORRECT
    writer = csv.writer(f)

# Mistake 2: Not converting types (all values are strings)
with open("data.csv") as f:
    for row in csv.DictReader(f):
        salary = row["salary"]    # This is "75000" (string!)
        tax = salary * 0.20       # TypeError: can't multiply str * float
        # Fix:
        salary = float(row["salary"])
        tax = salary * 0.20

# Mistake 3: Not skipping header with csv.reader
with open("data.csv") as f:
    reader = csv.reader(f)
    for row in reader:    # First row is ['name', 'age', ...] (the header!)
        print(row)
    # Fix: next(reader) or use DictReader
```

---

## Practice Exercises

1. Write a function that reads a CSV of students and returns those with score above 80.

2. Write a program that exports monthly expense data to CSV with headers.

3. Given a CSV file, write code to calculate the average of a numeric column.

4. Append a new record to an existing CSV without overwriting it.

---

## Next Lesson

**[Lesson 03 → JSON Files](lesson-03-json.md)**
