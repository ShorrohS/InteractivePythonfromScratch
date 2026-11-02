# Lesson 04 — Dictionaries

**Phase:** 03 — Collections | **Time:** ~45 min

---

## Part 1: What is a Dictionary?

A dictionary stores **key-value pairs**. Like a real dictionary: look up a word (key), get its definition (value).

```python
# Creating dictionaries
empty = {}
person = {"name": "Alice", "age": 30, "city": "New York"}
product = {
    "id": 1001,
    "name": "Laptop",
    "price": 999.99,
    "in_stock": True
}
```

**Keys must be unique and immutable** (str, int, tuple).
**Values can be anything** — including other dicts or lists.

---

## Part 2: Accessing Values

```python
person = {"name": "Alice", "age": 30, "city": "New York"}

# Direct access
print(person["name"])      # Alice
print(person["age"])       # 30

# .get() — safe access (no KeyError)
print(person.get("name"))          # Alice
print(person.get("email"))         # None
print(person.get("email", "N/A"))  # N/A (default value)
```

---

## Part 3: Modifying Dictionaries

```python
employee = {"name": "Bob", "salary": 60000, "dept": "Sales"}

# Add new key
employee["email"] = "bob@company.com"

# Update value
employee["salary"] = 65000

# Update multiple keys at once
employee.update({"salary": 70000, "dept": "Engineering"})

# Remove
del employee["dept"]                    # Remove by key
email = employee.pop("email", None)     # Remove and return (safe)
employee.popitem()                      # Remove last inserted item

# Clear all
# employee.clear()
```

---

## Part 4: Dictionary Methods

```python
student = {"name": "Alice", "grade": "A", "score": 95, "age": 20}

# Keys, values, items
print(student.keys())           # dict_keys(['name', 'grade', 'score', 'age'])
print(student.values())         # dict_values(['Alice', 'A', 95, 20])
print(student.items())          # dict_items([('name', 'Alice'), ...])

# Convert to list
keys = list(student.keys())
vals = list(student.values())

# Check key existence
print("name" in student)        # True
print("email" in student)       # False

# Length
print(len(student))             # 4

# Copy
copy = student.copy()           # shallow copy
```

---

## Part 5: Iterating Dictionaries

```python
person = {"name": "Alice", "age": 30, "city": "New York"}

# Iterate over keys (default)
for key in person:
    print(key)

# Iterate over key-value pairs (most common)
for key, value in person.items():
    print(f"{key}: {value}")

# Iterate over values
for value in person.values():
    print(value)
```

---

## Part 6: Nested Dictionaries

```python
employees = {
    "E001": {
        "name": "Alice Johnson",
        "salary": 80000,
        "skills": ["Python", "SQL", "Excel"]
    },
    "E002": {
        "name": "Bob Smith",
        "salary": 65000,
        "skills": ["Java", "MySQL"]
    }
}

# Access nested data
print(employees["E001"]["name"])           # Alice Johnson
print(employees["E001"]["skills"][0])      # Python

# Iterate
for emp_id, data in employees.items():
    print(f"\n{emp_id}: {data['name']}")
    print(f"  Salary: ${data['salary']:,}")
    print(f"  Skills: {', '.join(data['skills'])}")
```

---

## Part 7: Dictionary Comprehensions

```python
# Traditional
squares = {}
for i in range(1, 6):
    squares[i] = i ** 2

# Comprehension
squares = {i: i ** 2 for i in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# From list of tuples
pairs = [("a", 1), ("b", 2), ("c", 3)]
d = {k: v for k, v in pairs}

# With condition
prices = {"apple": 1.2, "banana": 0.5, "cherry": 3.0, "mango": 2.5}
expensive = {k: v for k, v in prices.items() if v > 1.5}
# {'cherry': 3.0, 'mango': 2.5}
```

---

## Part 8: Business Example — Student Management

```python
"""Student Management using dictionaries."""

students = {}

def add_student(sid, name, score):
    students[sid] = {"name": name, "score": score, "grade": get_grade(score)}

def get_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"

def display_all():
    print(f"\n{'ID':<8} {'Name':<20} {'Score':>6} {'Grade':>6}")
    print("─" * 44)
    for sid, data in students.items():
        print(f"{sid:<8} {data['name']:<20} {data['score']:>6} {data['grade']:>6}")

def class_stats():
    if not students:
        return
    scores = [s["score"] for s in students.values()]
    print(f"\nClass Statistics:")
    print(f"  Count:   {len(scores)}")
    print(f"  Average: {sum(scores)/len(scores):.1f}")
    print(f"  Highest: {max(scores)}")
    print(f"  Lowest:  {min(scores)}")

# Add some students
add_student("S001", "Alice Johnson", 92)
add_student("S002", "Bob Smith", 78)
add_student("S003", "Carol Davis", 85)
add_student("S004", "Dave Wilson", 61)

display_all()
class_stats()
```

---

## Common Mistakes

```python
# Mistake 1: KeyError on missing key
d = {"name": "Alice"}
print(d["email"])    # KeyError!
# Fix: use .get()
print(d.get("email", "Not provided"))

# Mistake 2: Using mutable as key
d = {[1,2]: "list"}  # TypeError: unhashable type: 'list'
# Fix: use tuple
d = {(1,2): "tuple"}  # OK

# Mistake 3: Modifying during iteration
for key in d:
    del d[key]    # RuntimeError: dictionary changed size during iteration
# Fix:
for key in list(d.keys()):
    del d[key]
```

---

## Next Lesson

**[Lesson 05 → Comprehensions](lesson-05-comprehensions.md)**
