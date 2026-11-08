"""
Demo 03 — Sets
Phase 03: Collections

Run: python demo-03-sets.py
"""

import sys
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 55)
print("DEMO 03 - Python Sets")
print("=" * 55)

# ─── CREATING SETS ────────────────────────────────────────
print("\n1. Creating sets:")

# Literal syntax: {value, value, ...}
colors = {"red", "green", "blue"}

# set() constructor converts any iterable — duplicates are dropped silently
from_list   = set([1, 2, 2, 3, 3, 3, 4])   # list with dupes → unique set
from_string = set("mississippi")             # unique characters only
from_range  = set(range(0, 10, 2))           # {0, 2, 4, 6, 8}

# IMPORTANT: {} alone creates an empty DICT, not an empty set!
empty_dict = {}        # type is <class 'dict'>
empty_set  = set()     # type is <class 'set'>

print(f"  Literal:      {colors}")
print(f"  From list:    {from_list}  (duplicates removed automatically)")
print(f"  From string:  {sorted(from_string)}  (unique chars, sorted to display)")
print(f"  From range:   {sorted(from_range)}")
print(f"  Empty dict:   {type(empty_dict)}")
print(f"  Empty set:    {type(empty_set)}")

# ─── ADDING & REMOVING ELEMENTS ──────────────────────────
print("\n2. Adding and removing elements:")
tech_skills = {"Python", "SQL", "Excel"}
print(f"  Initial: {tech_skills}")

# add() inserts a single element (no effect if already present)
tech_skills.add("Power BI")
tech_skills.add("Python")       # already there — no duplicate, no error
print(f"  After add('Power BI'): {tech_skills}")

# remove() deletes an element but raises KeyError if not found
tech_skills.remove("Excel")
print(f"  After remove('Excel'): {tech_skills}")

# discard() is the safe version — silently ignores missing elements
tech_skills.discard("Java")     # not in set — no KeyError raised
tech_skills.discard("SQL")      # found and removed
print(f"  After discard('Java'/'SQL'): {tech_skills}")

# pop() removes and returns an ARBITRARY element (order is not guaranteed)
if tech_skills:
    popped = tech_skills.pop()
    print(f"  After pop(): set={tech_skills}, popped='{popped}'")

# clear() empties the entire set
temp = {10, 20, 30}
temp.clear()
print(f"  After clear(): {temp}")

# ─── SET OPERATIONS ───────────────────────────────────────
print("\n3. Core set operations:")
A = {1, 2, 3, 4, 5}
B = {3, 4, 5, 6, 7}
print(f"  A = {A}")
print(f"  B = {B}")

# Union (|): every element from A OR B — no duplicates
print(f"\n  Union         A | B              = {A | B}")
print(f"  (method)      A.union(B)         = {A.union(B)}")

# Intersection (&): only elements present in BOTH A AND B
print(f"\n  Intersection  A & B              = {A & B}")
print(f"  (method)      A.intersection(B)  = {A.intersection(B)}")

# Difference (-): elements in A but NOT in B
print(f"\n  Difference    A - B              = {A - B}  (A only)")
print(f"  Difference    B - A              = {B - A}  (B only)")

# Symmetric difference (^): elements in either set but NOT in both
print(f"\n  Sym. diff     A ^ B              = {A ^ B}  (exclusive)")
print(f"  (method)      A.symmetric_difference(B) = {A.symmetric_difference(B)}")

# ─── IN-PLACE (UPDATE) OPERATORS ─────────────────────────
print("\n4. In-place set update operators:")
base = {1, 2, 3}
base |= {3, 4, 5}          # base.update({3, 4, 5}) — add all elements
print(f"  After |= {{3,4,5}}: {base}")

base &= {2, 3, 4}          # base.intersection_update(...) — keep only shared
print(f"  After &= {{2,3,4}}: {base}")

base -= {4}                 # base.difference_update(...) — remove matching
print(f"  After -= {{4}}:     {base}")

# ─── SET COMPARISONS ──────────────────────────────────────
print("\n5. Set comparisons (subset, superset, disjoint):")
all_students  = {"Alice", "Bob", "Carol", "Dave", "Eve"}
math_class    = {"Alice", "Carol", "Eve"}
science_class = {"Bob", "Dave", "Frank"}

print(f"  All:     {all_students}")
print(f"  Math:    {math_class}")
print(f"  Science: {science_class}")

# issubset: every element of math_class is in all_students
print(f"\n  math_class.issubset(all_students):     {math_class.issubset(all_students)}")
print(f"  math_class <= all_students (operator): {math_class <= all_students}")

# issuperset: all_students contains everything in math_class
print(f"  all_students.issuperset(math_class):   {all_students.issuperset(math_class)}")
print(f"  all_students >= math_class:            {all_students >= math_class}")

# isdisjoint: no elements in common (True = completely separate)
print(f"  math_class.isdisjoint(science_class):  {math_class.isdisjoint(science_class)}")

# Proper subset: subset but NOT equal (< is stricter than <=)
print(f"  math_class < all_students (proper):    {math_class < all_students}")
print(f"  all_students < all_students (proper):  {all_students < all_students}")

# ─── FROZENSET — IMMUTABLE SETS ───────────────────────────
print("\n6. frozenset — the immutable, hashable set:")

# Regular sets are mutable → cannot be used as dict keys or set members
# frozenset is immutable → can be used wherever a hashable type is needed
immutable = frozenset({1, 2, 3})
print(f"  frozenset value: {immutable}")

# Real use case: undirected graph edges
# frozenset({"A","B"}) == frozenset({"B","A"}) — order doesn't matter
graph = {
    frozenset({"A", "B"}): 10,   # edge between A and B, weight 10
    frozenset({"B", "C"}): 25,
    frozenset({"A", "C"}): 15,
}
print(f"  Edge A-B weight: {graph[frozenset({'A', 'B'})]}")
print(f"  Edge B-A weight: {graph[frozenset({'B', 'A'})]}")  # same edge!

# frozensets can live inside a regular set
combos = {frozenset({1, 2}), frozenset({1, 3}), frozenset({2, 3})}
print(f"  Set of frozensets: {combos}")

# ─── SET COMPREHENSIONS ───────────────────────────────────
print("\n7. Set comprehensions:")

# Pattern: {expression for item in iterable [if condition]}
# Like list comprehensions but the result is a set (unique values)

# Unique squares of 1-10
unique_squares = {x**2 for x in range(1, 11)}
print(f"  Squares 1-10 (unique): {sorted(unique_squares)}")

# With condition: only squares of odd numbers
odd_squares = {x**2 for x in range(1, 11) if x % 2 != 0}
print(f"  Odd squares:           {sorted(odd_squares)}")

# Extract unique email domains
emails = ["alice@gmail.com", "bob@yahoo.com", "carol@gmail.com", "dave@outlook.com"]
domains = {e.split("@")[1] for e in emails}
print(f"  Unique domains:        {domains}")

# ─── PRACTICAL: DUPLICATE REMOVAL ─────────────────────────
print("\n8. Practical: removing duplicates:")

tags = ["python", "data", "python", "ml", "data", "ai", "ml", "python"]

# Fast dedup — loses original order (sets are unordered)
deduped_unordered = list(set(tags))
print(f"  set() dedup:             {deduped_unordered}")

# Order-preserving dedup using dict.fromkeys() (Python 3.7+)
# dict.fromkeys() preserves insertion order and discards duplicate keys
deduped_ordered = list(dict.fromkeys(tags))
print(f"  Order-preserving dedup:  {deduped_ordered}")

# Practical: find emails that appear more than once
all_emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com", "b@x.com", "d@x.com"]
seen = set()
duplicates = set()
for email in all_emails:
    if email in seen:
        duplicates.add(email)
    seen.add(email)
print(f"  Duplicate emails:        {duplicates}")

# ─── PRACTICAL: O(1) MEMBERSHIP TEST ─────────────────────
print("\n9. Performance: O(1) set lookup vs O(n) list scan:")
import time

SIZE = 500_000
big_list = list(range(SIZE))
big_set  = set(range(SIZE))
target   = SIZE - 1   # worst case for list (element is at the very end)

t0 = time.perf_counter()
_ = target in big_list
list_ms = (time.perf_counter() - t0) * 1000

t0 = time.perf_counter()
_ = target in big_set
set_ms = (time.perf_counter() - t0) * 1000

print(f"  List in-check ({SIZE:,} items):  {list_ms:.4f} ms  (O(n))")
print(f"  Set  in-check ({SIZE:,} items):  {set_ms:.4f} ms  (O(1))")
if set_ms > 0:
    print(f"  Set is ~{list_ms / set_ms:.0f}x faster")

# ─── SETS VS LISTS: DECISION GUIDE ───────────────────────
print("\n10. Sets vs lists — when to choose which:")
print(f"  {'Requirement':<40} {'Use'}")
print("  " + "─" * 50)
guide = [
    ("Need unique elements guaranteed",   "Set"),
    ("Fast 'in' checks (O(1))",           "Set"),
    ("Union / intersection / difference", "Set"),
    ("Order matters (first, nth, last)",  "List"),
    ("Duplicate values are meaningful",   "List"),
    ("Index-based access (items[2])",     "List"),
    ("Elements are dicts or lists",       "List (unhashable)"),
]
for req, choice in guide:
    print(f"  {req:<40} {choice}")

print("\n" + "=" * 55)
