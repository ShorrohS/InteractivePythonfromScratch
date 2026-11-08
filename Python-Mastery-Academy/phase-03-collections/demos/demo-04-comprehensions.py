"""
Demo 04 — Comprehensions & Generator Expressions
Phase 03: Collections

Run: python demo-04-comprehensions.py
"""

import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 55)
print("DEMO 04 - Comprehensions & Generator Expressions")
print("=" * 55)

# ─── LIST COMPREHENSIONS: BASICS ──────────────────────────
print("\n1. List comprehensions — basics:")

# Pattern:  [expression  for item in iterable]
# Result:   a new list built by evaluating `expression` once per item

# Traditional for-loop approach
squares_loop = []
for i in range(1, 11):
    squares_loop.append(i ** 2)

# Equivalent one-line comprehension
squares_comp = [i**2 for i in range(1, 11)]

print(f"  Loop:   {squares_loop}")
print(f"  Comp:   {squares_comp}")
print(f"  Equal:  {squares_loop == squares_comp}")

# Transform a list of strings
names  = ["alice", "bob", "carol", "dave"]
titled = [name.title() for name in names]
lengths = [len(name) for name in names]
print(f"\n  Original:  {names}")
print(f"  Titled:    {titled}")
print(f"  Lengths:   {lengths}")

# ─── COMPREHENSIONS WITH A FILTER ────────────────────────
print("\n2. Comprehensions with a filter condition:")

# Pattern:  [expression  for item in iterable  if condition]
# Only items where condition is True are included in the result

numbers = range(1, 21)
evens = [n for n in numbers if n % 2 == 0]
print(f"  Evens 1-20:  {evens}")

# Combine filter and transform in one expression
long_upper = [
    w.upper()
    for w in ["cat", "elephant", "dog", "rhinoceros", "ox"]
    if len(w) > 3
]
print(f"  Long words uppercased: {long_upper}")

# Conditional EXPRESSION (ternary) — this is different from a filter!
# Pattern:  [val_if_true if condition else val_if_false  for item in iterable]
# Every item produces a result — the condition selects which value to use
labels = ["even" if n % 2 == 0 else "odd" for n in range(1, 9)]
print(f"  Labels (all items):  {labels}")

# ─── NESTED LIST COMPREHENSIONS ───────────────────────────
print("\n3. Nested comprehensions:")

# Two iterables — equivalent to two nested for-loops
# Pattern:  [expr  for outer in A  for inner in B]
pairs = [(x, y) for x in [1, 2, 3] for y in ["a", "b"]]
print(f"  All pairs: {pairs}")

# 2D: list of lists — [[expr for col in cols] for row in rows]
# Outer comprehension builds the rows, inner builds each row's values
table = [[r * c for c in range(1, 6)] for r in range(1, 6)]
print("\n  5×5 multiplication table:")
for row in table:
    print("    " + "  ".join(f"{v:>3}" for v in row))

# Flatten a 2D list into 1D
# [item  for row in matrix  for item in row]  — outer first, then inner
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat   = [item for row in matrix for item in row]
print(f"\n  Matrix:    {matrix}")
print(f"  Flattened: {flat}")

# TIP: more than 2 levels of nesting → switch to a regular loop for clarity

# ─── DICTIONARY COMPREHENSIONS ────────────────────────────
print("\n4. Dictionary comprehensions:")

# Pattern:  {key_expr: value_expr  for item in iterable  [if condition]}

# Map each word to its character count
words   = ["Python", "is", "powerful", "and", "readable"]
lengths = {w: len(w) for w in words}
print(f"  Word lengths: {lengths}")

# Filter — only words longer than 4 characters
long_dict = {w: len(w) for w in words if len(w) > 4}
print(f"  Long words:   {long_dict}")

# Invert a dict — swap keys and values
original = {"one": 1, "two": 2, "three": 3}
inverted = {v: k for k, v in original.items()}
print(f"  Original: {original}")
print(f"  Inverted: {inverted}")

# Transform values — apply a 15% discount to every item
prices  = {"apple": 1.20, "banana": 0.80, "cherry": 3.50}
on_sale = {item: round(price * 0.85, 2) for item, price in prices.items()}
print(f"  Prices:       {prices}")
print(f"  15% sale:     {on_sale}")

# ─── SET COMPREHENSIONS ───────────────────────────────────
print("\n5. Set comprehensions:")

# Pattern:  {expression  for item in iterable  [if condition]}
# Like a list comprehension but duplicates are removed automatically

raw = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
unique_vals = {x for x in raw}
print(f"  Raw:    {raw}")
print(f"  Unique: {sorted(unique_vals)}")

# Extract the set of unique first characters
langs = ["Python", "Perl", "Java", "JavaScript", "Ruby", "Rust"]
initials = {lang[0] for lang in langs}
print(f"  Language initials: {sorted(initials)}")

# ─── GENERATOR EXPRESSIONS ────────────────────────────────
print("\n6. Generator expressions — lazy, memory-efficient iteration:")

# Generator expression looks like a list comp but uses () instead of []
# It does NOT build a list in memory — it computes values one at a time on demand

list_comp = [x**2 for x in range(10_000)]    # all 10 000 values stored NOW
gen_expr  = (x**2 for x in range(10_000))    # no values computed yet

list_size = sys.getsizeof(list_comp)
gen_size  = sys.getsizeof(gen_expr)

print(f"  [list comp]  memory: {list_size:>8,} bytes  (all values in RAM)")
print(f"  (gen expr)   memory: {gen_size:>8,} bytes  (nothing stored)")
print(f"  Memory ratio: list is {list_size // gen_size}x larger")

# Generators work perfectly with aggregation functions
total   = sum(x**2 for x in range(1, 101))    # no intermediate list needed
maximum = max(x**3 for x in range(1, 10))
print(f"\n  Sum of squares 1-100: {total}")
print(f"  Max cube 1-9:         {maximum}")

# any() and all() short-circuit — they stop early with generators
nums = [4, 8, 15, 16, 23, 42]
print(f"  all even? {all(n % 2 == 0 for n in nums)}")  # stops at 15
print(f"  any > 40? {any(n > 40    for n in nums)}")   # stops at 42

# ─── COMPREHENSIONS VS REGULAR LOOPS ─────────────────────
print("\n7. When to use comprehensions vs loops:")
print(f"  {'Situation':<48} {'Choose'}")
print("  " + "─" * 62)
guide = [
    ("Simple transform of one iterable",              "Comprehension"),
    ("Filter items based on a condition",              "Comprehension"),
    ("Result is a list / dict / set",                  "Comprehension"),
    ("Aggregate over large data (sum, max, any, all)", "Generator expr"),
    ("Multiple operations or statements per item",     "Regular loop"),
    ("Need break / continue logic",                    "Regular loop"),
    ("Side effects: print, file write, API call",      "Regular loop"),
    ("More than 2 levels of nesting",                  "Regular loop"),
]
for situation, choice in guide:
    print(f"  {situation:<48} {choice}")

# ─── REAL-WORLD DATA PIPELINE ─────────────────────────────
print("\n8. Real-world data transformation pipeline:")

employees = [
    {"id": 1, "name": "Alice",  "dept": "Engineering", "salary": 95000,  "active": True},
    {"id": 2, "name": "Bob",    "dept": "Sales",        "salary": 65000,  "active": True},
    {"id": 3, "name": "Carol",  "dept": "Engineering",  "salary": 105000, "active": True},
    {"id": 4, "name": "Dave",   "dept": "HR",           "salary": 72000,  "active": False},
    {"id": 5, "name": "Eve",    "dept": "Sales",        "salary": 80000,  "active": True},
    {"id": 6, "name": "Frank",  "dept": "Engineering",  "salary": 88000,  "active": False},
]

# Step 1 — Filter: keep only active employees
active = [e for e in employees if e["active"]]
print(f"  Active:           {[e['name'] for e in active]}")

# Step 2 — Transform + filter: names of active high earners
high_earners = [e["name"] for e in active if e["salary"] > 75000]
print(f"  High earners:     {high_earners}")

# Step 3 — Build a lookup dict (id → name) for quick access
id_lookup = {e["id"]: e["name"] for e in employees}
print(f"  ID lookup:        {id_lookup}")

# Step 4 — Collect unique departments
departments = {e["dept"] for e in employees}
print(f"  Departments:      {sorted(departments)}")

# Step 5 — Apply a 5% raise to all active employees
# {**dict} unpacks an existing dict; we override the "salary" key
with_raise = [{**e, "salary": round(e["salary"] * 1.05)} for e in active]
print(f"  After 5% raise:   {[(e['name'], e['salary']) for e in with_raise]}")

# Step 6 — Group names by department using a dict comprehension
dept_names = {
    dept: [e["name"] for e in employees if e["dept"] == dept]
    for dept in departments
}
print(f"  By department:")
for dept in sorted(dept_names):
    print(f"    {dept}: {dept_names[dept]}")

print("\n" + "=" * 55)
