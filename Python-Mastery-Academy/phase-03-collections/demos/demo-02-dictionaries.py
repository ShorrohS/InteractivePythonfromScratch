"""
Demo 02 — Dictionaries
Phase 03: Collections

Run: python demo-02-dictionaries.py
"""

import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 55)
print("DEMO 02 - Python Dictionaries")
print("=" * 55)

# ─── CREATING ─────────────────────────────────────────────
print("\n1. Creating dictionaries:")
empty = {}
person = {"name": "Alice", "age": 30, "city": "New York"}
product = {
    "id": 1001,
    "name": "Laptop Pro",
    "price": 1299.99,
    "in_stock": True,
    "tags": ["electronics", "computing"]
}

print(f"  Person: {person}")
print(f"  Product name: {product['name']}, Price: ${product['price']}")

# ─── ACCESS ───────────────────────────────────────────────
print("\n2. Accessing values:")
employee = {"name": "Bob", "dept": "Sales", "salary": 65000}
print(f"  Direct:  {employee['name']}")
print(f"  .get():  {employee.get('salary', 0)}")
print(f"  Missing: {employee.get('email', 'Not provided')}")

# ─── MODIFYING ────────────────────────────────────────────
print("\n3. Modifying dictionaries:")
data = {"a": 1, "b": 2}
print(f"  Initial: {data}")
data["c"] = 3
print(f"  After add: {data}")
data.update({"d": 4, "e": 5})
print(f"  After update: {data}")
del data["a"]
print(f"  After del: {data}")

# ─── ITERATION ────────────────────────────────────────────
print("\n4. Iterating:")
grades = {"Alice": 92, "Bob": 78, "Carol": 95, "Dave": 81}

print("\n  By keys:")
for name in grades:
    print(f"    {name}")

print("\n  By key-value pairs:")
for name, grade in grades.items():
    status = "Pass" if grade >= 75 else "Fail"
    print(f"    {name:<8} {grade}%  {status}")

# ─── NESTED ───────────────────────────────────────────────
print("\n5. Nested dictionaries:")
company = {
    "name": "TechCorp",
    "departments": {
        "Engineering": {"headcount": 15, "avg_salary": 95000},
        "Sales": {"headcount": 8, "avg_salary": 70000},
        "Marketing": {"headcount": 5, "avg_salary": 75000}
    }
}

print(f"  Company: {company['name']}")
print(f"\n  {'Department':<15} {'Headcount':>10} {'Avg Salary':>12}")
print("  " + "─" * 40)
for dept, info in company["departments"].items():
    print(f"  {dept:<15} {info['headcount']:>10} ${info['avg_salary']:>11,}")

# ─── COMPREHENSION ────────────────────────────────────────
print("\n6. Dictionary comprehensions:")
words = ["Python", "is", "awesome", "and", "powerful"]
word_lengths = {word: len(word) for word in words}
print(f"  Word lengths: {word_lengths}")

expensive = {k: v for k, v in {"laptop": 1200, "mouse": 30, "keyboard": 80}.items() if v > 50}
print(f"  Expensive items: {expensive}")

print("\n" + "=" * 55)
