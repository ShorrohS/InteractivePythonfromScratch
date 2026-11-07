# Lesson 06 — Nested Data Structures

**Phase:** 03 — Collections | **Time:** ~25 min

---

## Part 1: What are Nested Structures?

Real-world data is rarely flat. Nested data structures let you represent complex, hierarchical information.

```python
# Flat — limited
name    = "Alice"
score_1 = 92
score_2 = 88

# Nested — represents real structure
student = {
    "name":   "Alice",
    "scores": [92, 88, 95, 71],
    "address": {
        "city":    "New York",
        "country": "USA"
    }
}
```

---

## Part 2: List of Dicts — Most Common Pattern

```python
# Real-world: a database table as a list of records
employees = [
    {"id": 1, "name": "Alice", "dept": "Engineering", "salary": 85000},
    {"id": 2, "name": "Bob",   "dept": "Sales",       "salary": 62000},
    {"id": 3, "name": "Carol", "dept": "Engineering", "salary": 95000},
]

# Access
print(employees[0]["name"])           # Alice
print(employees[2]["salary"])         # 95000

# Iterate
for emp in employees:
    print(f"{emp['name']:<10} ${emp['salary']:,}")

# Search
engineers = [e for e in employees if e["dept"] == "Engineering"]

# Sort by salary
by_salary = sorted(employees, key=lambda e: e["salary"], reverse=True)
```

---

## Part 3: Dict of Dicts

```python
# Lookup table structure
company = {
    "E001": {"name": "Alice", "salary": 85000, "skills": ["Python", "SQL"]},
    "E002": {"name": "Bob",   "salary": 62000, "skills": ["Excel", "PowerPoint"]},
    "E003": {"name": "Carol", "salary": 95000, "skills": ["Python", "Rust", "Go"]},
}

# Access nested data
print(company["E001"]["name"])          # Alice
print(company["E003"]["skills"][0])     # Python

# Add new record
company["E004"] = {"name": "Dave", "salary": 70000, "skills": ["Java"]}

# Update nested value
company["E001"]["salary"] = 90000

# Iterate
for emp_id, data in company.items():
    skills = ", ".join(data["skills"])
    print(f"{emp_id}: {data['name']:<10} ${data['salary']:,}  [{skills}]")
```

---

## Part 4: Safe Access — .get() and Defaults

```python
record = {"name": "Alice", "age": 30}

# Risky — KeyError if key missing
print(record["email"])     # KeyError!

# Safe — returns default
email = record.get("email", "no email")

# Safe nested access
user = {"profile": {"address": {"city": "London"}}}
city = user.get("profile", {}).get("address", {}).get("city", "Unknown")
print(city)   # London

# With missing keys
user2 = {}
city2 = user2.get("profile", {}).get("address", {}).get("city", "Unknown")
print(city2)  # Unknown (no KeyError)
```

---

## Part 5: Modifying Nested Structures

```python
catalog = {
    "electronics": [
        {"name": "Laptop", "price": 1200, "stock": 5},
        {"name": "Mouse",  "price": 35,   "stock": 50},
    ],
    "furniture": [
        {"name": "Desk",  "price": 450, "stock": 10},
    ]
}

# Add item to a category
catalog["electronics"].append({"name": "Keyboard", "price": 80, "stock": 30})

# Update nested price
for item in catalog["electronics"]:
    if item["name"] == "Laptop":
        item["price"] = 1100

# Add new category
catalog["books"] = [{"name": "Python Cookbook", "price": 45, "stock": 20}]

# Total value across all categories
total = 0
for category, items in catalog.items():
    for item in items:
        total += item["price"] * item["stock"]
print(f"Total inventory value: ${total:,}")
```

---

## Part 6: JSON — Real-World Nested Data

Nested structures in Python map directly to JSON. This is how APIs return data:

```python
import json

api_response = {
    "status": "success",
    "data": {
        "user": {
            "id": 1001,
            "name": "Alice Johnson",
            "roles": ["admin", "editor"],
            "preferences": {
                "theme": "dark",
                "language": "en"
            }
        }
    }
}

# Navigate deep nested data
user = api_response["data"]["user"]
print(user["name"])                     # Alice Johnson
print(user["roles"][0])                 # admin
print(user["preferences"]["theme"])     # dark

# Convert to JSON string
json_str = json.dumps(api_response, indent=2)
print(json_str)
```

---

## Practice Exercises

1. Create a list of 3 student dicts (name, grades list). Write code to calculate the average grade for each student.

2. Given a list of order dicts `{"product": str, "qty": int, "price": float}`, calculate the total order value.

3. Build a nested dict representing a school: departments → courses → students.

4. Write a function that safely gets a deeply nested value, returning a default if any key is missing.

---

## Phase 03 Complete

You now know all four collection types and comprehensions. Time to build the projects!

**→ [Project 01 — Shopping Cart](../guided-projects/project-01-shopping-cart/)**
**→ [Project 02 — Student Management](../guided-projects/project-02-student-management/)**
**→ [Project 03 — Inventory System](../guided-projects/project-03-inventory-system/)**
