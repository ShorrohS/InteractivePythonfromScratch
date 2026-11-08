# Phase 03 — Advanced Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/advanced/exercises.md`

---

## Q1. Group Records by Key

```python
employees = [
    {"name": "Alice",  "dept": "Engineering", "salary": 95000},
    {"name": "Bob",    "dept": "Sales",        "salary": 65000},
    {"name": "Carol",  "dept": "Engineering",  "salary": 105000},
    {"name": "Dave",   "dept": "HR",           "salary": 72000},
    {"name": "Eve",    "dept": "Sales",        "salary": 80000},
    {"name": "Frank",  "dept": "Engineering",  "salary": 88000},
    {"name": "Grace",  "dept": "HR",           "salary": 68000},
]

# ── Part 1: group names by department ─────────────────────
# Technique: build the dict incrementally.
# setdefault(key, []) returns an existing list or creates a new empty one.
grouped = {}
for emp in employees:
    grouped.setdefault(emp["dept"], []).append(emp["name"])

print("Grouped by department:")
for dept, names in sorted(grouped.items()):
    print(f"  {dept}: {names}")

# ── Part 2: department statistics ─────────────────────────
# Collect salaries per department first, then derive stats.
dept_salaries = {}
for emp in employees:
    dept_salaries.setdefault(emp["dept"], []).append(emp["salary"])

# Dict comprehension over the collected salary lists
dept_stats = {
    dept: {
        "count":      len(salaries),
        "avg_salary": round(sum(salaries) / len(salaries), 2),
        "max_salary": max(salaries),
    }
    for dept, salaries in dept_salaries.items()
}

print("\nDepartment stats:")
for dept, stats in sorted(dept_stats.items()):
    print(f"  {dept}: count={stats['count']}, "
          f"avg=${stats['avg_salary']:,.0f}, max=${stats['max_salary']:,}")
```

---

## Q2. Dictionary Inversion with Duplicate Values

```python
course_enrollment = {
    "Alice":   "Python",
    "Bob":     "JavaScript",
    "Carol":   "Python",
    "Dave":    "Java",
    "Eve":     "Python",
    "Frank":   "JavaScript",
    "Grace":   "Java",
    "Hannah":  "Rust",
}

# ── Part A: invert — course → sorted list of students ─────
inverted = {}
for student, course in course_enrollment.items():
    inverted.setdefault(course, []).append(student)

# Sort the student lists for deterministic output
inverted = {course: sorted(students) for course, students in inverted.items()}
print("Inverted enrollment:")
for course, students in sorted(inverted.items()):
    print(f"  {course}: {students}")

# ── Part B: statistics from the inverted dict ─────────────
most_popular  = max(inverted, key=lambda c: len(inverted[c]))
least_popular = min(inverted, key=lambda c: len(inverted[c]))
solo_courses  = [c for c, s in inverted.items() if len(s) == 1]
unique_courses = len(inverted)

print(f"\nMost popular:  {most_popular} ({len(inverted[most_popular])} students)")
print(f"Least popular: {least_popular} ({len(inverted[least_popular])} students)")
print(f"Solo courses:  {solo_courses}")
print(f"Total courses: {unique_courses}")

# ── Part C: reusable inversion function ───────────────────
def invert_dict(d):
    """Invert a dict, grouping duplicate values into sorted lists.

    >>> invert_dict({"a": 1, "b": 2, "c": 1})
    {1: ['a', 'c'], 2: ['b']}
    """
    result = {}
    for key, value in d.items():
        result.setdefault(value, []).append(key)
    return {v: sorted(keys) for v, keys in result.items()}

print("\nFunction test:", invert_dict({"a": 1, "b": 2, "c": 1}))
```

---

## Q3. Matrix Transposition with Comprehensions

```python
matrix = [
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  8],
    [ 9, 10, 11, 12],
]
rows = len(matrix)       # 3
cols = len(matrix[0])    # 4

# ── Part A: transpose using nested comprehension ──────────
# New matrix has `cols` rows and `rows` columns.
# transposed[col][row] = matrix[row][col]
transposed = [[matrix[row][col] for row in range(rows)] for col in range(cols)]

print("Original matrix:")
for row in matrix:
    print(" ", row)
print("Transposed matrix:")
for row in transposed:
    print(" ", row)

# ── Part B: verify using zip() ────────────────────────────
# zip(*matrix) unpacks the rows and pairs elements at the same position.
# Each zip output is a tuple, so map(list, ...) converts them to lists.
transposed_zip = [list(row) for row in zip(*matrix)]
print(f"\nzip method equals comprehension: {transposed == transposed_zip}")

# ── Part C: matrix multiplication ─────────────────────────
def matrix_multiply(A, B):
    """Multiply two matrices A (m×n) and B (n×p) → result (m×p)."""
    m, n, p = len(A), len(A[0]), len(B[0])
    assert len(B) == n, f"Incompatible dimensions: A is {m}×{n}, B is {len(B)}×{p}"
    # result[i][j] is the dot product of row i in A and column j in B
    return [
        [sum(A[i][k] * B[k][j] for k in range(n)) for j in range(p)]
        for i in range(m)
    ]

A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = matrix_multiply(A, B)
print(f"\nA × B = {C}")   # [[19, 22], [43, 50]]
```

---

## Q4. Anagram Detection and Grouping

```python
word_list = [
    "listen", "silent", "enlist",
    "triangle", "integral", "alerting",
    "python", "typhon",
    "eating", "tinge",
    "hello", "world",
]

# ── Part A: group anagrams ────────────────────────────────
# Sorting the characters of a word produces a canonical key.
# Two words that are anagrams share the same sorted-character key.
anagram_groups = {}
for word in word_list:
    key = tuple(sorted(word.lower()))   # e.g. "listen" → ('e','i','l','n','s','t')
    anagram_groups.setdefault(key, []).append(word)

# Convert dict values to a list of groups
all_groups = list(anagram_groups.values())

print("All anagram groups:")
for group in all_groups:
    print(f"  {group}")

# ── Part B: only groups with 2+ anagrams ─────────────────
multi_groups = [g for g in all_groups if len(g) >= 2]
print("\nGroups with 2+ anagrams:")
for group in multi_groups:
    print(f"  {group}")

# ── Part C: helper function ───────────────────────────────
def are_anagrams(word1: str, word2: str) -> bool:
    """Return True if word1 and word2 are anagrams (same letters, any order).

    >>> are_anagrams("listen", "silent")
    True
    >>> are_anagrams("hello", "world")
    False
    """
    return sorted(word1.lower()) == sorted(word2.lower())

print(f"\nare_anagrams('listen', 'silent'): {are_anagrams('listen', 'silent')}")
print(f"are_anagrams('hello', 'world'):   {are_anagrams('hello', 'world')}")
```

---

## Q5. Top-N Word Frequency Counter

```python
import string

text = """
Python is a versatile programming language. Python is used for web development,
data science, and automation. Many developers love Python because Python syntax
is clean and Python code is readable. Learning Python is rewarding because Python
has a large and active community that contributes to Python's growth every year.
"""

stop_words = {"is", "a", "and", "for", "many", "because", "has", "to", "that",
              "the", "an", "in", "of", "it", "its", "be", "are", "was", "were"}

def top_words(text: str, stop_words: set, n: int = 5):
    """Return top-n (word, count) tuples sorted by count desc, then alpha."""
    # Step 1: strip punctuation — str.translate removes every char in the table
    clean = text.lower().translate(str.maketrans("", "", string.punctuation))

    # Step 2: split and filter
    all_words    = [w for w in clean.split() if w]
    content_words = [w for w in all_words if w not in stop_words]

    # Step 3: count with a plain dict
    freq = {}
    for word in content_words:
        freq[word] = freq.get(word, 0) + 1

    # Step 4: sort by (-count, word) so highest count comes first;
    #         alphabetical order breaks ties
    ranked = sorted(freq.items(), key=lambda x: (-x[1], x[0]))

    return freq, ranked[:n], all_words, content_words

freq, top5, all_words, content_words = top_words(text, stop_words, n=5)

print(f"Total word count (incl. stop words): {len(all_words)}")
print(f"Unique content words: {len(freq)}")
print(f"\nTop 5 words:")
for word, count in top5:
    print(f"  {word:<15} {count}")

appears_twice = [w for w, c in freq.items() if c == 2]
print(f"\nWords appearing exactly twice: {sorted(appears_twice)}")
```

---

## Q6. Nested Dictionary Flattening

```python
config = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "credentials": {
            "username": "admin",
            "password": "secret"
        }
    },
    "app": {
        "debug": True,
        "version": "1.0.0",
        "features": {
            "auth": True,
            "logging": {
                "level": "INFO",
                "file": "app.log"
            }
        }
    },
    "timeout": 30,
}

# ── Part A: flatten ───────────────────────────────────────
def flatten(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    """Flatten a nested dict using dot-notation keys (recursive).

    >>> flatten({"a": {"b": 1}, "c": 2})
    {'a.b': 1, 'c': 2}
    """
    result = {}
    for key, value in d.items():
        # Build the full key path: prepend parent key if we're inside nesting
        full_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            # Value is itself a dict — recurse deeper
            result.update(flatten(value, full_key, sep))
        else:
            # Leaf value — store it directly
            result[full_key] = value
    return result

flat = flatten(config)
print("Flattened config:")
for key, value in flat.items():
    print(f"  {key:<45} = {value!r}")

# ── Part B: unflatten ─────────────────────────────────────
def unflatten(d: dict, sep: str = ".") -> dict:
    """Reconstruct a nested dict from a flat dot-notation dict.

    >>> unflatten({"a.b": 1, "c": 2})
    {'a': {'b': 1}, 'c': 2}
    """
    result = {}
    for full_key, value in d.items():
        parts   = full_key.split(sep)    # e.g. "database.host" → ["database", "host"]
        current = result
        for part in parts[:-1]:          # navigate/create all intermediate dicts
            current = current.setdefault(part, {})
        current[parts[-1]] = value       # set the leaf value
    return result

reconstructed = unflatten(flat)

# ── Part C: verify round-trip ─────────────────────────────
print(f"\nRound-trip match: {reconstructed == config}")
```
