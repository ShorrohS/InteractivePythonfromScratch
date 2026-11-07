# Lesson 05 — List & Dictionary Comprehensions

**Phase:** 03 — Collections | **Time:** ~30 min

---

## Part 1: Why Comprehensions?

Comprehensions let you build lists and dicts in a single, readable line instead of 3–4 lines with a loop.

```python
# Traditional way
squares = []
for i in range(1, 11):
    squares.append(i ** 2)

# Comprehension — same result, one line
squares = [i ** 2 for i in range(1, 11)]
```

---

## Part 2: List Comprehension Syntax

```python
[expression for item in iterable]
[expression for item in iterable if condition]
```

---

## Part 3: List Comprehension Examples

```python
# Basic
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

squares   = [n**2 for n in numbers]
evens     = [n for n in numbers if n % 2 == 0]
even_sq   = [n**2 for n in numbers if n % 2 == 0]
strings   = [str(n) for n in numbers]

# Transform strings
names = ["  alice ", "BOB  ", "  carol"]
clean = [n.strip().title() for n in names]

# Nested comprehension (flattens a matrix)
matrix = [[1,2,3],[4,5,6],[7,8,9]]
flat   = [n for row in matrix for n in row]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Conditional expression (ternary in comprehension)
grades = [92, 45, 78, 61, 88, 39]
results = ["Pass" if g >= 60 else "Fail" for g in grades]
```

---

## Part 4: Dictionary Comprehensions

```python
{key_expr: value_expr for item in iterable}
{key_expr: value_expr for item in iterable if condition}

# Basic
word_lengths = {word: len(word) for word in ["Python", "is", "great"]}
# {'Python': 6, 'is': 2, 'great': 5}

# From two lists (zip)
names  = ["Alice", "Bob", "Carol"]
scores = [92, 78, 85]
grade_book = {name: score for name, score in zip(names, scores)}

# With condition
grade_book = {name: score for name, score in zip(names, scores) if score >= 80}

# Invert a dictionary
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}

# Prices with discount
prices = {"laptop": 1200, "mouse": 35, "keyboard": 80}
discounted = {item: round(p * 0.9, 2) for item, p in prices.items()}
```

---

## Part 5: Set Comprehensions

```python
# Unique squares
unique_sq = {n**2 for n in [1, -1, 2, -2, 3]}
# {1, 4, 9}

# Unique first letters
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
first_letters = {w[0] for w in words}
# {'a', 'b', 'c'}
```

---

## Part 6: When NOT to Use Comprehensions

```python
# BAD — too complex, hard to read
result = [transform(item) for item in data
          if condition1(item) and condition2(item)
          if not skip(item)]

# BETTER — use a regular loop for complex logic
result = []
for item in data:
    if condition1(item) and condition2(item):
        if not skip(item):
            result.append(transform(item))
```

Rule: if a comprehension needs more than one `if` condition or the logic is complex, use a loop.

---

## Part 7: Business Examples

```python
# Employee data processing
employees = [
    {"name": "Alice", "dept": "Eng",   "salary": 85000},
    {"name": "Bob",   "dept": "Sales", "salary": 62000},
    {"name": "Carol", "dept": "Eng",   "salary": 95000},
    {"name": "Dave",  "dept": "Sales", "salary": 71000},
]

# Extract all names
names = [e["name"] for e in employees]

# High earners only
high_earners = [e["name"] for e in employees if e["salary"] > 70000]

# Salary dict
salary_map = {e["name"]: e["salary"] for e in employees}

# After 10% raise for Engineering
updated = [
    {**e, "salary": e["salary"] * 1.10}
    if e["dept"] == "Eng" else e
    for e in employees
]

# Summary per department
depts = {e["dept"] for e in employees}   # unique departments
dept_avg = {
    dept: sum(e["salary"] for e in employees if e["dept"] == dept)
          / sum(1 for e in employees if e["dept"] == dept)
    for dept in depts
}
```

---

## Practice Exercises

1. From a list of numbers 1–50, create a list of all multiples of 6.

2. Given `words = ["hello", "python", "world", "code"]`, create a dict of `{word: word_reversed}`.

3. From a list of employee dicts with `name` and `score`, create a dict of only those who scored above 80: `{name: score}`.

4. Flatten this nested list into a single list: `[[1,2],[3,4],[5,6]]`.

---

## Next Lesson

**[Lesson 06 → Nested Data Structures](lesson-06-nested.md)**
