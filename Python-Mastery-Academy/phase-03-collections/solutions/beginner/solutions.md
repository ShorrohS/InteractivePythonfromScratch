# Phase 03 — Beginner Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/beginner/exercises.md`

---

## A1. Favourite movies list

```python
movies = ["Inception", "The Matrix", "Interstellar", "Dune", "Blade Runner 2049"]

print(movies[0])          # first item — index 0
print(movies[-1])         # last item — negative index -1 always means the end
print(movies[::-1])       # reverse using slice with step -1
print(len(movies))        # built-in len() counts items
```

---

## A2. Score statistics

```python
scores = [72, 85, 90, 68, 95, 78, 82]

highest = max(scores)
lowest  = min(scores)
average = sum(scores) / len(scores)
above_80 = len([s for s in scores if s > 80])   # list comp counts matches

print(f"Highest: {highest}")
print(f"Lowest:  {lowest}")
print(f"Average: {average:.1f}")
print(f"Above 80: {above_80}")
```

---

## A3. What is the output?

```python
numbers = [1, 2, 3, 4, 5]
numbers.append(6)          # list is now [1, 2, 3, 4, 5, 6]
numbers.insert(0, 0)       # insert 0 at index 0 → [0, 1, 2, 3, 4, 5, 6]
numbers.remove(3)          # remove first occurrence of 3 → [0, 1, 2, 4, 5, 6]
print(numbers)             # [0, 1, 2, 4, 5, 6]
print(len(numbers))        # 6
```

**Output:**
```
[0, 1, 2, 4, 5, 6]
6
```

---

## A4. Even squares via comprehension

```python
# Pattern: [expression for item in iterable if condition]
# We want x**2 for x in 1-10, BUT only where the SQUARE is even.
# A square is even whenever x is even (odd**2 is always odd).

even_squares = [x**2 for x in range(1, 11) if (x**2) % 2 == 0]
print(even_squares)    # [4, 16, 36, 64, 100]

# Equivalent filter on x directly (x even → x**2 even)
even_squares_v2 = [x**2 for x in range(1, 11) if x % 2 == 0]
print(even_squares_v2) # [4, 16, 36, 64, 100]
```

---

## A5. Shopping cart program

```python
cart = []                                         # start with an empty list

while True:
    item = input("Add item (or 'done' to finish): ").strip()
    if item.lower() == "done":
        break
    if item:                                      # ignore empty input
        cart.append(item)

print(f"\nYour cart ({len(cart)} items):")
for i, item in enumerate(cart, 1):               # enumerate gives (index, value) pairs
    print(f"  {i}. {item}")
```

---

## A6. What is wrong and how to fix it

```python
# PROBLEM: modifying a list while iterating over it causes Python to skip elements.
# Removing an item shifts all subsequent indices left, so the loop's internal
# pointer advances past the next element without checking it.

# Broken code (produces wrong result — some even numbers are skipped):
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)
print(items)   # [1, 3, 5] — looks correct here, but with more even numbers it fails

# FIX 1 — iterate over a copy of the list (the slice [:] creates a copy)
items = [1, 2, 3, 4, 5]
for item in items[:]:
    if item % 2 == 0:
        items.remove(item)
print(items)   # [1, 3, 5]

# FIX 2 — use a list comprehension (cleanest and most Pythonic)
items = [1, 2, 3, 4, 5]
items = [x for x in items if x % 2 != 0]
print(items)   # [1, 3, 5]
```

---

## B7. GPS coordinates tuple

```python
# Tuples are immutable — their contents cannot be changed after creation.
# That makes them ideal for values that should NEVER change, like coordinates.

gps = (40.7128, -74.0060, 10)   # (latitude, longitude, altitude_metres)
latitude, longitude, altitude = gps   # tuple unpacking

print(f"Latitude:  {latitude}")
print(f"Longitude: {longitude}")
print(f"Altitude:  {altitude}m")

# Why tuple and not list?
# - A list could be accidentally mutated (gps[0] = 999.0 would silently corrupt the data)
# - Tuples signal to other developers: "these values are fixed"
# - Tuples are slightly faster and use less memory
# - Tuples can be used as dictionary keys; lists cannot
```

---

## B8. What is the output?

```python
point = (3, 7)
x, y = point        # tuple unpacking assigns 3 to x, 7 to y
print(f"X: {x}, Y: {y}")    # X: 3, Y: 7
print(point[0] + point[1])  # 3 + 7 = 10
```

**Output:**
```
X: 3, Y: 7
10
```

---

## B9. Sort list of tuples by score

```python
leaderboard = [("Alice", 88), ("Bob", 95), ("Carol", 72), ("Dave", 95), ("Eve", 81)]

# sorted() with key= does not modify the original list
# lambda extracts the second element (score) for comparison
# reverse=True sorts from highest to lowest
sorted_board = sorted(leaderboard, key=lambda player: player[1], reverse=True)

print("Leaderboard:")
for rank, (name, score) in enumerate(sorted_board, 1):
    print(f"  {rank}. {name:<8} {score}")
```

**Output:**
```
Leaderboard:
  1. Bob       95
  2. Dave      95
  3. Alice     88
  4. Eve       81
  5. Carol     72
```

---

## C10. Set operations on visitor IDs

```python
monday  = {1001, 1002, 1003, 1004}
tuesday = {1002, 1003, 1005, 1006}

both_days     = monday & tuesday         # intersection: in BOTH sets
either_day    = monday | tuesday         # union: in EITHER set
monday_only   = monday - tuesday         # difference: in monday but NOT tuesday

print(f"Visited both days:   {both_days}")       # {1002, 1003}
print(f"Visited either day:  {either_day}")      # {1001, 1002, 1003, 1004, 1005, 1006}
print(f"Monday only:         {monday_only}")     # {1001, 1004}
```

---

## C11. Find unique emails

```python
emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com", "b@x.com"]

# set() accepts any iterable and automatically discards duplicates
unique = set(emails)
print(unique)   # {'a@x.com', 'b@x.com', 'c@x.com'}
print(f"Unique count: {len(unique)}")

# To preserve original order (Python 3.7+ dict is ordered):
unique_ordered = list(dict.fromkeys(emails))
print(unique_ordered)   # ['a@x.com', 'b@x.com', 'c@x.com']
```

---

## C12. What is the output?

```python
s1 = {1, 2, 3}
s2 = {2, 3, 4}
print(s1 | s2)   # union:        {1, 2, 3, 4}
print(s1 & s2)   # intersection: {2, 3}
print(s1 - s2)   # difference:   {1}  (in s1 but not s2)
```

**Output:**
```
{1, 2, 3, 4}
{2, 3}
{1}
```

---

## C13. Sets are unordered — what does that mean?

Sets have no concept of "first", "second", or "position". The items are stored in a
hash table, not a sequence, so:

- You **cannot** access elements by index: `my_set[0]` raises `TypeError`
- The order you see when printing a set may change between runs or Python versions
- There is no guaranteed sort order

Practical implications:
```python
s = {3, 1, 4, 1, 5, 9}
# print(s[0])   # TypeError: 'set' object is not subscriptable

# To iterate in a predictable order, convert to a sorted list first:
for item in sorted(s):
    print(item)   # 1, 3, 4, 5, 9
```

---

## D14. Student dictionary

```python
student = {
    "name":    "Jordan Smith",
    "age":     21,
    "gpa":     3.75,
    "courses": ["Python", "Data Structures", "Algorithms"],
}

print(f"Name:    {student['name']}")
print(f"Age:     {student['age']}")
print(f"GPA:     {student['gpa']:.2f}")
print(f"Courses: {', '.join(student['courses'])}")
```

---

## D15. Employee salary operations

```python
employees = {"Alice": 75000, "Bob": 65000, "Carol": 90000}

# Highest salary: max() with key= extracts the dict value for comparison
top_earner = max(employees, key=employees.get)
print(f"Highest paid: {top_earner} (${employees[top_earner]:,})")

# 10% raise — build a new dict with updated values
employees = {name: salary * 1.10 for name, salary in employees.items()}
print(f"After raise: {employees}")

# Filter: employees earning over $70,000 after the raise
over_70k = {name: sal for name, sal in employees.items() if sal > 70000}
print(f"Over $70k:  {over_70k}")
```

---

## D16. What is the output?

```python
d = {"a": 1, "b": 2, "c": 3}
d["d"] = 4                         # add new key "d"
del d["a"]                         # remove key "a"
print(d.get("a", "Not found"))     # "a" was deleted → "Not found"
print(list(d.keys()))              # remaining keys: ['b', 'c', 'd']
```

**Output:**
```
Not found
['b', 'c', 'd']
```

---

## D17. Word frequency counter

```python
sentence = "the quick brown fox jumps over the lazy dog the fox"
words = sentence.split()

freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1    # get returns 0 if key missing, then add 1

# Sort by frequency (highest first), then alphabetically for ties
sorted_freq = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

print("Word frequencies:")
for word, count in sorted_freq:
    print(f"  {word:<12} {count}")
```

**Output:**
```
Word frequencies:
  the          3
  fox          2
  brown        1
  dog          1
  jumps        1
  lazy         1
  over         1
  quick        1
```

---

## D18. `d["key"]` vs `d.get("key")`

| Method | Missing key behaviour | When to use |
|--------|----------------------|-------------|
| `d["key"]` | Raises `KeyError` | When the key **must** exist (missing = programming bug) |
| `d.get("key")` | Returns `None` | When the key might legitimately be absent |
| `d.get("key", default)` | Returns `default` | When you need a fallback value |

```python
config = {"host": "localhost", "port": 5432}

host = config["host"]                    # OK — "host" always exists here
timeout = config.get("timeout", 30)     # OK — "timeout" is optional, default 30
debug = config.get("debug")             # returns None if not set
```

---

## E19. Word-length dictionary comprehension

```python
words = ["Python", "is", "powerful", "and", "readable"]

# Pattern: {key: value for item in iterable}
word_lengths = {word: len(word) for word in words}
print(word_lengths)
# {'Python': 6, 'is': 2, 'powerful': 8, 'and': 3, 'readable': 8}
```

---

## E20. Name-to-score dict from a list of dicts

```python
data = [
    {"name": "Alice", "score": 92},
    {"name": "Bob",   "score": 78},
    {"name": "Carol", "score": 95},
]

# Dictionary comprehension extracting specific fields from each record
name_score = {record["name"]: record["score"] for record in data}
print(name_score)
# {'Alice': 92, 'Bob': 78, 'Carol': 95}
```
