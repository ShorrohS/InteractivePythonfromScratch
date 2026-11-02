"""
Demo 01 — Lists
Phase 03: Collections

Run: python demo-01-lists.py
"""

import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 55)
print("DEMO 01 - Python Lists")
print("=" * 55)

# ─── CREATING LISTS ───────────────────────────────────────
print("\n1. Creating lists:")
empty = []
numbers = [1, 2, 3, 4, 5]
names = ["Alice", "Bob", "Carol"]
mixed = [1, "hello", 3.14, True, None]
nested = [[1, 2], [3, 4], [5, 6]]

print(f"  Numbers: {numbers}")
print(f"  Names:   {names}")
print(f"  Mixed:   {mixed}")
print(f"  Nested:  {nested}")

# ─── INDEXING ─────────────────────────────────────────────
print("\n2. Indexing:")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
print(f"  fruits[0]:   {fruits[0]}")
print(f"  fruits[-1]:  {fruits[-1]}")
print(f"  fruits[1:3]: {fruits[1:3]}")
print(f"  fruits[:3]:  {fruits[:3]}")
print(f"  fruits[::2]: {fruits[::2]}")
print(f"  reversed:    {fruits[::-1]}")

# ─── MODIFYING ────────────────────────────────────────────
print("\n3. Modifying lists:")
cart = ["milk", "eggs", "bread"]
print(f"  Initial: {cart}")
cart.append("butter")
print(f"  After append: {cart}")
cart.insert(0, "flour")
print(f"  After insert(0): {cart}")
cart.remove("eggs")
print(f"  After remove: {cart}")
popped = cart.pop()
print(f"  After pop: {cart} (popped: {popped})")

# ─── METHODS ──────────────────────────────────────────────
print("\n4. List methods:")
scores = [85, 92, 78, 95, 88, 72, 91]
print(f"  Original: {scores}")
print(f"  max:      {max(scores)}")
print(f"  min:      {min(scores)}")
print(f"  sum:      {sum(scores)}")
print(f"  sorted:   {sorted(scores)}")
print(f"  count(92): {scores.count(92)}")
print(f"  index(78): {scores.index(78)}")

# ─── COMPREHENSIONS ───────────────────────────────────────
print("\n5. List comprehensions:")
squares = [i**2 for i in range(1, 11)]
evens = [i for i in range(1, 21) if i % 2 == 0]
upper_names = [n.upper() for n in names]
print(f"  Squares:    {squares}")
print(f"  Evens:      {evens}")
print(f"  Uppercase:  {upper_names}")

# ─── ITERATION ────────────────────────────────────────────
print("\n6. Iterating:")
employees = [("Alice", 75000), ("Bob", 65000), ("Carol", 90000)]
print(f"  {'Name':<10} {'Salary':>10}")
print("  " + "─" * 22)
for i, (name, salary) in enumerate(employees, 1):
    print(f"  {i}. {name:<8} ${salary:>9,}")

total = sum(s for _, s in employees)
print(f"\n  Total payroll: ${total:,}")

print("\n" + "=" * 55)
