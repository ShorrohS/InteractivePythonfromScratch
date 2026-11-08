# Phase 03 — Intermediate Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/intermediate/exercises.md`

---

## Q1. Grade Book Manager

```python
students = [
    {"name": "Alice",  "scores": [85, 92, 78, 95, 88]},
    {"name": "Bob",    "scores": [72, 68, 75, 70, 80]},
    {"name": "Carol",  "scores": [95, 98, 92, 97, 100]},
    {"name": "Dave",   "scores": [55, 60, 58, 62, 50]},
    {"name": "Eve",    "scores": [88, 85, 91, 83, 90]},
]

def letter_grade(avg):
    """Map a numeric average to a letter grade."""
    if avg >= 90: return "A"
    if avg >= 80: return "B"
    if avg >= 70: return "C"
    if avg >= 60: return "D"
    return "F"

# Build a richer list of student records with computed stats
records = []
for s in students:
    avg = round(sum(s["scores"]) / len(s["scores"]), 1)
    records.append({
        "name":  s["name"],
        "avg":   avg,
        "high":  max(s["scores"]),
        "low":   min(s["scores"]),
        "grade": letter_grade(avg),
    })

# Class-wide statistics
class_avg   = round(sum(r["avg"] for r in records) / len(records), 1)
top_student = max(records, key=lambda r: r["avg"])
failing     = [r["name"] for r in records if r["avg"] < 60]

# Display formatted table
print(f"{'Name':<10} {'Avg':>6}  {'High':>5}  {'Low':>4}  {'Grade'}")
print("-" * 38)
for r in records:
    print(f"{r['name']:<10} {r['avg']:>6}  {r['high']:>5}  {r['low']:>4}  {r['grade']}")

print(f"\nClass average: {class_avg}")
print(f"Top student:   {top_student['name']} ({top_student['avg']})")
print(f"Failing:       {failing}")
```

---

## Q2. Inventory Dashboard

```python
inventory = {
    "laptops":    {"quantity": 12, "price": 999.99},
    "mice":       {"quantity": 3,  "price": 29.99},
    "keyboards":  {"quantity": 8,  "price": 79.99},
    "monitors":   {"quantity": 2,  "price": 449.99},
    "headsets":   {"quantity": 15, "price": 199.99},
    "webcams":    {"quantity": 4,  "price": 89.99},
}

# Dict comprehension: compute total value per item
values = {
    item: round(data["quantity"] * data["price"], 2)
    for item, data in inventory.items()
}

# Find extremes using max/min with key= function
most_expensive   = max(inventory, key=lambda k: inventory[k]["price"])
highest_value    = max(values, key=values.get)
total_value      = round(sum(values.values()), 2)

# List comprehension to collect low-stock items
low_stock = [item for item, data in inventory.items() if data["quantity"] < 5]

# Formatted output
print("INVENTORY DASHBOARD")
print("-" * 52)
print(f"{'Item':<14} {'Qty':>5}  {'Unit Price':>12}  {'Total Value':>12}")
print("-" * 52)
for item, data in inventory.items():
    print(f"{item:<14} {data['quantity']:>5}  ${data['price']:>11,.2f}  ${values[item]:>11,.2f}")
print("-" * 52)
print(f"Total inventory value:     ${total_value:>11,.2f}")
print(f"Low stock (qty < 5):       {low_stock}")
print(f"Most expensive unit:       {most_expensive} (${inventory[most_expensive]['price']:,.2f})")
print(f"Highest total stock value: {highest_value} (${values[highest_value]:,.2f})")
```

---

## Q3. Contact List Merger

```python
list_a = [
    {"name": "Alice",      "email": "alice@example.com",  "phone": "555-1234"},
    {"name": "Bob",        "email": "bob@example.com",    "phone": None},
    {"name": "Carol",      "email": "carol@example.com",  "phone": "555-5678"},
]
list_b = [
    {"name": "Bob Johnson","email": "bob@example.com",    "phone": "555-9999"},
    {"name": "Dave",       "email": "dave@example.com",   "phone": "555-4321"},
    {"name": "Eve",        "email": "eve@example.com",    "phone": None},
]

# Build a dict keyed by email so each email appears only once.
# Start with all of list_a. Then process list_b:
#   - If the email is new, add it directly.
#   - If it's a duplicate, keep the version that HAS a phone number.
merged = {contact["email"]: contact for contact in list_a}

for contact in list_b:
    email = contact["email"]
    if email not in merged:
        merged[email] = contact                       # new email — add it
    elif contact["phone"] and not merged[email]["phone"]:
        merged[email] = contact                       # list_b has a phone; list_a doesn't

# Display the merged list (sorted by name for readability)
contacts = sorted(merged.values(), key=lambda c: c["name"])
print(f"Merged contacts ({len(contacts)}):")
for c in contacts:
    print(f"  {c['name']:<15} {c['email']:<28} {c['phone']}")
```

---

## Q4. Word Frequency Analyzer

```python
text = """
Python is a versatile language. Python is used for web development, data science,
and automation. Many developers choose Python because Python is readable and Python
syntax is clean. Learning Python is rewarding because Python has a large community.
"""
stop_words = {"is", "a", "and", "for", "because", "has", "many"}

# Clean: lowercase and strip punctuation, then split into words
clean = text.lower().replace(",", "").replace(".", "").replace("\n", " ")
words = clean.split()

# Build frequency dict, skipping stop words
freq = {}
for word in words:
    if word not in stop_words:
        freq[word] = freq.get(word, 0) + 1

# Sort by count descending, then alphabetically for ties
sorted_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

# Top 3 and unique words
top3         = sorted_freq[:3]
unique_words = sorted(w for w, c in freq.items() if c == 1)

print("Word Frequency (excluding stop words):")
for word, count in sorted_freq:
    print(f"  {word:<15} {count}")

print(f"\nTop 3:   {top3}")
print(f"Unique:  {unique_words}")
```

---

## Q5. Shopping Cart with Discount Codes

```python
cart = [
    ("Laptop Pro",    1, 1299.99),
    ("Mouse",         2, 34.99),
    ("USB-C Hub",     1, 49.99),
    ("Keyboard",      1, 89.99),
    ("Monitor Stand", 2, 39.99),
]
discount_codes = {
    "SAVE10":  0.10,
    "TECH20":  0.20,
    "HALFOFF": 0.50,
    "NONE":    0.00,
}
applied_code = "TECH20"
tax_rate      = 0.085

# List comprehension: add a subtotal field to each cart item
line_items = [(name, qty, price, qty * price) for name, qty, price in cart]

subtotal         = sum(sub for *_, sub in line_items)
discount_rate    = discount_codes.get(applied_code, 0.0)
discount_amount  = round(subtotal * discount_rate, 2)
after_discount   = round(subtotal - discount_amount, 2)
tax_amount       = round(after_discount * tax_rate, 2)
total            = round(after_discount + tax_amount, 2)

# Formatted receipt
W = 50
print("=" * W)
print("RECEIPT".center(W))
print("=" * W)
print(f"{'Item':<20} {'Qty':>4}  {'Price':>10}  {'Subtotal':>10}")
print("-" * W)
for name, qty, price, sub in line_items:
    print(f"{name:<20} {qty:>4}  ${price:>9,.2f}  ${sub:>9,.2f}")
print("-" * W)
print(f"{'Subtotal:':<38} ${subtotal:>9,.2f}")
print(f"{'Discount (' + applied_code + ' -' + str(int(discount_rate*100)) + '%):':<38} -${discount_amount:>8,.2f}")
print(f"{'After discount:':<38} ${after_discount:>9,.2f}")
print(f"{'Tax (' + str(int(tax_rate*100)) + '.5%):':<38} ${tax_amount:>9,.2f}")
print("=" * W)
print(f"{'TOTAL:':<38} ${total:>9,.2f}")
print("=" * W)
```

---

## Q6. Student Roster Comparison

```python
python_class  = {"Alice", "Bob", "Carol", "Dave", "Eve"}
data_class    = {"Bob", "Carol", "Frank", "Grace"}
ml_class      = {"Carol", "Eve", "Frank", "Hannah"}

# 1. In ALL three classes (triple intersection)
in_all = python_class & data_class & ml_class
print(f"In all three:      {sorted(in_all)}")

# 2. In EXACTLY ONE class
# A student is in exactly one class if they are in one class
# AND NOT in the union of the other two.
only_python = python_class - (data_class | ml_class)
only_data   = data_class   - (python_class | ml_class)
only_ml     = ml_class     - (python_class | data_class)
in_exactly_one = only_python | only_data | only_ml
print(f"In exactly one:    {sorted(in_exactly_one)}")

# 3. Total roster (union of all three)
total_roster = python_class | data_class | ml_class
print(f"Total roster:      {sorted(total_roster)}")

# 4. Not in Python but in at least one other class
not_python_but_other = (data_class | ml_class) - python_class
print(f"Not Python, other: {sorted(not_python_but_other)}")

# 5. Largest class
classes = {"python_class": python_class, "data_class": data_class, "ml_class": ml_class}
largest = max(classes, key=lambda k: len(classes[k]))
print(f"Largest class:     {largest} ({len(classes[largest])} students)")

# 6. In EXACTLY TWO classes (in at least two, but not all three)
in_at_least_two = (
    (python_class & data_class) |
    (python_class & ml_class)   |
    (data_class   & ml_class)
)
in_exactly_two = in_at_least_two - in_all
print(f"Exactly two:       {sorted(in_exactly_two)}")
```
