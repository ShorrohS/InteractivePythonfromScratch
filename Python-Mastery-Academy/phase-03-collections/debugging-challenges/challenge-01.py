"""
Debugging Challenge 01 — Phase 03: Collections
================================================

INSTRUCTIONS:
  This file contains 7 bugs — all related to collections.
  Find and fix every bug.
  When all bugs are fixed, the program runs without errors and prints correct output.

Run: python challenge-01.py

HINTS:
  - Read each error message carefully — it tells you the type and location
  - Bugs cover: off-by-one indexing, KeyError, mutating while iterating,
    wrong set operation, broken comprehension, unhashable type, wrong dict method
  - Fix one bug at a time, then rerun

DO NOT SCROLL TO THE ANSWER KEY UNTIL YOU'VE TRIED!
"""

print("=" * 50)
print("DEBUGGING CHALLENGE 01 - Collections Bugs")
print("=" * 50)

# ============================================================
# BUG 1 — Off-by-one list indexing
# ============================================================
# GOAL: Print the first and last element of the list, then
#       print the element in the exact middle (index 3 of 7).
print("\nBug 1 - List indexing:")
scores = [72, 85, 90, 68, 95, 78, 82]
print(f"  First score:  {scores[0]}")
print(f"  Last score:   {scores[7]}")        # BUG: list has 7 items (indices 0-6)
print(f"  Middle score: {scores[3]}")


# ============================================================
# BUG 2 — KeyError on missing dictionary key
# ============================================================
# GOAL: Look up each employee's department. If an employee is
#       not found, print "Unknown" instead of crashing.
print("\nBug 2 - Dictionary lookup:")
employee_dept = {
    "Alice": "Engineering",
    "Bob":   "Sales",
    "Carol": "HR",
}
names_to_look_up = ["Alice", "Dave", "Carol"]
for name in names_to_look_up:
    dept = employee_dept[name]              # BUG: raises KeyError for "Dave"
    print(f"  {name}: {dept}")


# ============================================================
# BUG 3 — Mutating a list while iterating over it
# ============================================================
# GOAL: Remove all even numbers from the list.
#       Expected result: [1, 3, 5, 7, 9]
print("\nBug 3 - Mutating while iterating:")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for n in numbers:                           # BUG: modifying the list you're iterating
    if n % 2 == 0:
        numbers.remove(n)
print(f"  Odds only: {numbers}")            # BUG: some even numbers survive


# ============================================================
# BUG 4 — Wrong set operation
# ============================================================
# GOAL: Find customers who placed orders on BOTH Monday AND Tuesday.
#       Expected: {1002, 1003}
print("\nBug 4 - Set operation:")
monday_orders  = {1001, 1002, 1003, 1004}
tuesday_orders = {1002, 1003, 1005, 1006}
repeat_customers = monday_orders | tuesday_orders   # BUG: | is union (all customers)
print(f"  Repeat customers: {repeat_customers}")    # expected {1002, 1003}


# ============================================================
# BUG 5 — Broken list comprehension (wrong filter condition)
# ============================================================
# GOAL: Create a list of words longer than 4 characters.
#       Expected: ['elephant', 'rhinoceros', 'giraffe']
print("\nBug 5 - Comprehension condition:")
animals = ["cat", "elephant", "dog", "rhinoceros", "ox", "giraffe"]
long_animals = [a for a in animals if len(a) < 4]   # BUG: < should be >
print(f"  Long animals: {long_animals}")


# ============================================================
# BUG 6 — Trying to use a list as a dictionary key
# ============================================================
# GOAL: Use coordinates as dict keys to store location names.
#       A tuple is the correct hashable type for this — not a list.
print("\nBug 6 - Unhashable dict key:")
locations = {}
coord_a = [40.7128, -74.0060]                       # BUG: list is not hashable
coord_b = [51.5074, -0.1278]
locations[coord_a] = "New York"
locations[coord_b] = "London"
print(f"  Locations: {locations}")


# ============================================================
# BUG 7 — Using .keys() when .values() is needed
# ============================================================
# GOAL: Sum all the prices in the catalogue dict.
#       Expected total: 2409.97
print("\nBug 7 - Wrong dict method:")
catalogue = {
    "Laptop":   1299.99,
    "Monitor":   449.99,
    "Keyboard":   89.99,
    "Mouse":      34.99,
    "USB Hub":    34.99,   # note: float arithmetic — use round()
    "Headset":   199.99,
    "Webcam":    129.99,   # total = round(sum, 2)
}
total_price = sum(catalogue.keys())                 # BUG: .keys() gives strings!
print(f"  Total: ${total_price:.2f}")

print("\n" + "=" * 50)
print("Fixed all 7 bugs? All sections should print correct output.")
print("=" * 50)


# ============================================================
# ANSWER KEY — do not read until you have tried!
# ============================================================
#
# Bug 1: scores[7] → scores[-1]  OR  scores[6]
#        Index 7 is out of range for a 7-element list (valid indices: 0-6).
#        Use -1 for the last element (always safe regardless of length).
#
# Bug 2: employee_dept[name] → employee_dept.get(name, "Unknown")
#        Direct key access raises KeyError when the key is missing.
#        .get(key, default) returns the default instead of crashing.
#
# Bug 3: Replace the for-loop mutation with a list comprehension:
#        numbers = [n for n in numbers if n % 2 != 0]
#        Modifying a list while iterating over it skips elements because
#        Python advances the index even after a removal.
#
# Bug 4: monday_orders | tuesday_orders → monday_orders & tuesday_orders
#        | is union (all elements from either set).
#        & is intersection (only elements in BOTH sets). "Both days" = intersection.
#
# Bug 5: len(a) < 4  →  len(a) > 4
#        < 4 keeps SHORT words (cat, dog, ox).
#        > 4 keeps LONG words (elephant, rhinoceros, giraffe).
#
# Bug 6: coord_a = [40.7128, -74.0060]  →  coord_a = (40.7128, -74.0060)
#        Lists are mutable and therefore not hashable — they cannot be dict keys.
#        Tuples are immutable and hashable — the correct type for fixed coordinates.
#
# Bug 7: sum(catalogue.keys()) → sum(catalogue.values())
#        .keys() returns the string keys ("Laptop", "Monitor", ...) — you can't sum strings.
#        .values() returns the float prices, which can be summed.
