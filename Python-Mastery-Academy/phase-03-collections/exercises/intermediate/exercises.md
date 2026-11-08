# Phase 03 — Intermediate Exercises

> These exercises require combining multiple collection types in a single program.
> Attempt all questions before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Grade Book Manager**

*Difficulty: Intermediate*

You are given the following student data:

```python
students = [
    {"name": "Alice",  "scores": [85, 92, 78, 95, 88]},
    {"name": "Bob",    "scores": [72, 68, 75, 70, 80]},
    {"name": "Carol",  "scores": [95, 98, 92, 97, 100]},
    {"name": "Dave",   "scores": [55, 60, 58, 62, 50]},
    {"name": "Eve",    "scores": [88, 85, 91, 83, 90]},
]
```

Write code to:
- Calculate each student's average score (round to 1 decimal place)
- Assign a letter grade: A ≥ 90, B ≥ 80, C ≥ 70, D ≥ 60, F < 60
- Identify the top student (highest average)
- List all students who are failing (average < 60)
- Calculate the class average
- Display a formatted table like:

```
Name       Avg    High  Low   Grade
--------------------------------------
Alice      87.6    95    78     B
Bob        73.0    80    68     C
Carol      96.4   100    92     A
Dave       57.0    62    50     F
Eve        87.4    91    83     B

Class average: 80.3
Top student: Carol (96.4)
Failing: ['Dave']
```

**Hints:**
- Use `sum(scores) / len(scores)` for averages
- Use `max()` and `min()` on the scores list
- Use a list comprehension to filter failing students

---

**Q2. Inventory Dashboard**

*Difficulty: Intermediate*

Given this inventory data:

```python
inventory = {
    "laptops":    {"quantity": 12, "price": 999.99},
    "mice":       {"quantity": 3,  "price": 29.99},
    "keyboards":  {"quantity": 8,  "price": 79.99},
    "monitors":   {"quantity": 2,  "price": 449.99},
    "headsets":   {"quantity": 15, "price": 199.99},
    "webcams":    {"quantity": 4,  "price": 89.99},
}
```

Use dict comprehensions and built-ins to:
- Build a `values` dict: `{item: quantity × price}` for each item
- Find all items with low stock (quantity < 5)
- Calculate the total value of all inventory
- Find the single most expensive item (by unit price)
- Find the item with the highest total stock value
- Print a formatted dashboard

Expected output (approximate):

```
INVENTORY DASHBOARD
--------------------------------------------
Item          Qty    Unit Price   Total Value
--------------------------------------------
laptops        12     $999.99    $11,999.88
mice            3      $29.99       $89.97
...
--------------------------------------------
Total inventory value: $15,899.67
Low stock items (qty < 5): ['mice', 'monitors']
Most expensive unit: laptops ($999.99)
Highest stock value: laptops ($11,999.88)
```

**Hints:**
- Use `{k: v["quantity"] * v["price"] for k, v in inventory.items()}`
- Use `min(inventory, key=lambda k: ...)` and `max(...)` to find extremes
- Use a list comprehension to find low-stock items

---

**Q3. Contact List Merger**

*Difficulty: Intermediate*

You have two contact lists imported from different sources:

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
```

Merge the two lists into one deduplicated list. Use email as the unique key.
If the same email appears in both lists, keep the record that has a phone number.
If both or neither have a phone, keep the one from `list_b`.

Expected output:
```
Merged contacts (5):
  Alice         alice@example.com    555-1234
  Bob Johnson   bob@example.com      555-9999
  Carol         carol@example.com    555-5678
  Dave          dave@example.com     555-4321
  Eve           eve@example.com      None
```

**Hints:**
- Build a `dict` keyed by email as you iterate (later entries overwrite earlier ones)
- After adding all of `list_a`, process `list_b`: update only if the entry has a phone or the existing one doesn't
- Use a set to track which emails you've seen to check for duplicates

---

**Q4. Word Frequency Analyzer**

*Difficulty: Intermediate*

Given the following text:

```python
text = """
Python is a versatile language. Python is used for web development, data science,
and automation. Many developers choose Python because Python is readable and Python
syntax is clean. Learning Python is rewarding because Python has a large community.
"""
stop_words = {"is", "a", "and", "for", "because", "has", "many"}
```

Write code to:
- Clean the text: lowercase, strip punctuation (`,`, `.`, `\n`)
- Split into words and count each word's frequency using a dict
- Exclude stop words from the frequency count
- Find the top 3 most frequent words
- Find all words that appear exactly once
- Display the full frequency table sorted by count (descending)

Expected output (approximate):
```
Word Frequency (excluding stop words):
  python      7
  learning    1
  ...

Top 3:  [('python', 7), ('is', ...), ...]
Unique: ['automation', 'clean', 'community', ...]
```

**Hints:**
- `text.replace(",", "").replace(".", "").lower().split()` to clean
- Use `freq[word] = freq.get(word, 0) + 1` to count
- `sorted(freq.items(), key=lambda x: x[1], reverse=True)` to sort

---

**Q5. Shopping Cart with Discount Codes**

*Difficulty: Intermediate*

```python
cart = [
    ("Laptop Pro",   1, 1299.99),
    ("Mouse",        2, 34.99),
    ("USB-C Hub",    1, 49.99),
    ("Keyboard",     1, 89.99),
    ("Monitor Stand",2, 39.99),
]
# (item_name, quantity, unit_price)

discount_codes = {
    "SAVE10":  0.10,
    "TECH20":  0.20,
    "HALFOFF": 0.50,
    "NONE":    0.00,
}
applied_code = "TECH20"
tax_rate      = 0.085
```

Write code to:
- Calculate each line's subtotal (quantity × price)
- Compute the cart total before discount
- Apply the discount code to get the discounted total
- Add tax on the discounted amount
- Print a formatted receipt

Expected output:
```
============================================
             RECEIPT
============================================
Item             Qty   Price    Subtotal
--------------------------------------------
Laptop Pro         1  $1,299.99 $1,299.99
Mouse              2     $34.99    $69.98
...
--------------------------------------------
Subtotal:                       $1,554.94
Discount (TECH20 - 20%):        -$310.99
After discount:                 $1,243.95
Tax (8.5%):                       $105.74
TOTAL:                          $1,349.69
============================================
```

**Hints:**
- Use a list comprehension to calculate each `(name, qty, price, qty * price)` tuple
- Retrieve the discount rate with `discount_codes.get(applied_code, 0.0)`

---

**Q6. Student Roster Comparison**

*Difficulty: Intermediate*

```python
python_class  = {"Alice", "Bob", "Carol", "Dave", "Eve"}
data_class    = {"Bob", "Carol", "Frank", "Grace"}
ml_class      = {"Carol", "Eve", "Frank", "Hannah"}
```

Using only set operations, find and print:
1. Students enrolled in ALL three classes
2. Students enrolled in exactly ONE class (not in any two)
3. All unique students across every class (total roster)
4. Students NOT in the Python class but enrolled in at least one other class
5. The class with the most students
6. Students shared between exactly two classes (any pair)

Expected output (approximate):
```
In all three:       ['Carol']
In exactly one:     ['Alice', 'Dave', 'Grace', 'Hannah']
Total roster:       ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Grace', 'Hannah']
Not Python, other:  ['Frank', 'Grace', 'Hannah']
Largest class:      python_class (5 students)
Exactly two classes:['Bob', 'Eve', 'Frank']
```

**Hints:**
- Use `&` for intersection, `|` for union, `-` for difference
- "Exactly one class": in a class AND NOT in the union of the other two
- "Exactly two classes": in at least two, but not all three
- Sort results before printing for consistent output

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
