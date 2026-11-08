"""
Demo 03 — For Loops
Phase 02: Control Flow

Run: python demo-03-for-loops.py
"""

print("=" * 50)
print("DEMO 03 — For Loops")
print("=" * 50)

# --- ITERATING OVER A LIST ---
print("\n1. Iterating over a list:")
# The for loop binds each element to the loop variable in turn.
# No index needed — Python handles advancement automatically.

fruits = ["apple", "banana", "cherry", "date"]
for fruit in fruits:
    print(f"  {fruit.capitalize()}")

# --- ITERATING OVER A STRING ---
print("\n2. Iterating over a string:")
# Strings are iterable — each character is visited one at a time.

word = "Python"
print(f"  Characters in '{word}':", end=" ")
for char in word:
    print(char, end="-")
print()

# Practical: count vowels by iterating over the string
vowel_count = 0
for char in word.lower():
    if char in "aeiou":
        vowel_count += 1
print(f"  Vowels in '{word}': {vowel_count}")

# --- ITERATING OVER A TUPLE ---
print("\n3. Iterating over a tuple:")
# Tuples work identically to lists in a for loop.

rgb = (255, 128, 0)
labels = ("Red", "Green", "Blue")
print("  RGB values:")
for label, value in zip(labels, rgb):      # zip() shown properly in section 7
    print(f"    {label}: {value}")

# Tuple unpacking inside a for loop — very common pattern
employees = [("Alice", 75_000), ("Bob", 82_000), ("Carol", 69_000)]
print("  Employee salaries:")
for name, salary in employees:              # each tuple auto-unpacked into two variables
    print(f"    {name:<8} ${salary:,}")

# --- ITERATING OVER A DICTIONARY ---
print("\n4. Iterating over a dictionary:")
config = {"host": "localhost", "port": 5432, "db": "prod"}

# Default iteration: keys only
print("  Keys:", list(config.keys()))

# Values only
print("  Values:", list(config.values()))

# Key-value pairs with .items() — the most common dict loop pattern
print("  Key-value pairs:")
for key, value in config.items():
    print(f"    {key:<6}: {value}")

# --- range() ---
print("\n5. range() — start / stop / step:")
# range(stop)             → 0 up to (but not including) stop
# range(start, stop)      → start up to (not including) stop
# range(start, stop, step)→ start up to stop, advancing by step each time
# The stop value is NEVER included — remember "up to but not including".

print("  range(5):", end="  ")
for i in range(5):
    print(i, end=" ")
print()

print("  range(1, 6):", end="  ")
for i in range(1, 6):
    print(i, end=" ")
print()

print("  range(0, 20, 4):", end="  ")
for i in range(0, 20, 4):
    print(i, end=" ")
print()

print("  range(10, 0, -2):", end="  ")  # negative step counts downward
for i in range(10, 0, -2):
    print(i, end=" ")
print()

# --- enumerate() ---
print("\n6. enumerate() — index and value together:")
# Without enumerate, you'd need a separate counter variable.
# enumerate(iterable, start=0) yields (index, element) pairs.

menu_items = ["New Game", "Load Game", "Settings", "Quit"]

print("  0-indexed menu:")
for index, item in enumerate(menu_items):
    print(f"    {index}. {item}")

print("  1-indexed menu (start=1):")
for index, item in enumerate(menu_items, start=1):  # shift starting index
    print(f"    {index}. {item}")

# --- zip() ---
print("\n7. zip() — parallel iteration over multiple sequences:")
# zip() pairs elements from two or more iterables by position.
# It stops as soon as the shortest iterable is exhausted.

names  = ["Alice", "Bob", "Carol"]
scores = [88, 95, 72]
grades = ["B", "A", "C"]

print("  Report card:")
for name, score, grade in zip(names, scores, grades):
    print(f"    {name:<8} score: {score:>3}  grade: {grade}")

# --- for-else ---
print("\n8. for-else construct:")
# The else block runs when the loop exhausts the iterable normally (no break).
# Mirrors while-else — ideal for "search and report" patterns.

numbers = [3, 5, 9, 2, 8]
for target in [9, 7]:           # first target is present, second is absent
    for n in numbers:
        if n == target:
            print(f"  Found {target} in {numbers}.")
            break
    else:
        # Runs only when no break was hit — the whole list was scanned
        print(f"  {target} not in {numbers} — else block ran.")

# --- ACCUMULATION PATTERNS ---
print("\n9. Accumulation patterns:")
# for loops are ideal for building up a result item by item.

data = [4, 7, 1, 9, 3, 6, 8, 2, 5]

# Running sum
total = 0
for n in data:
    total += n
print(f"  Data: {data}")
print(f"  Sum:  {total}")

# Manual maximum (without max())
maximum = data[0]               # seed with the first element
for n in data:
    if n > maximum:
        maximum = n
print(f"  Max:  {maximum}")

# Build a filtered list
evens = []
for n in data:
    if n % 2 == 0:
        evens.append(n)
print(f"  Evens: {evens}")

# --- PRACTICAL EXAMPLE ---
print("\n10. Practical: monthly sales report:")
monthly_sales = {
    "Jan": 42_500, "Feb": 38_200, "Mar": 51_000,
    "Apr": 47_800, "May": 55_300, "Jun": 61_000,
}

annual_total = 0
best_month  = ""
best_amount = 0

print(f"\n  {'Month':<5}  {'Sales':>10}  Chart")
print("  " + "-" * 40)

for month, sales in monthly_sales.items():
    bar = "█" * (sales // 5_000)            # one block per $5,000
    print(f"  {month}:  ${sales:>8,}  {bar}")
    annual_total += sales
    if sales > best_amount:
        best_amount = sales
        best_month  = month

print("  " + "-" * 40)
print(f"  Total: ${annual_total:,}")
print(f"  Best:  {best_month} (${best_amount:,})")

print("\n" + "=" * 50)
