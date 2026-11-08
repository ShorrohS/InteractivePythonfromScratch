# Phase 03 — Advanced Exercises

> These exercises involve complex data manipulation: nested structures, grouping,
> aggregation, and multi-step transformations using comprehensions.
> Attempt all questions before checking solutions.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Group Records by Key**

*Difficulty: Advanced*

Given a flat list of employee records, group them by department:

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
```

Produce two outputs:
1. `grouped` — a dict mapping each department to a list of employee names:
   ```python
   {"Engineering": ["Alice", "Carol", "Frank"], "Sales": ["Bob", "Eve"], "HR": ["Dave", "Grace"]}
   ```
2. `dept_stats` — a dict mapping each department to `{"count": n, "avg_salary": x, "max_salary": y}`:
   ```python
   {"Engineering": {"count": 3, "avg_salary": 96000.0, "max_salary": 105000}, ...}
   ```

Do NOT use `collections.defaultdict` or `itertools.groupby`. Use only plain dicts.
Aim to compute `dept_stats` in one pass over the employees list.

**Hints:**
- First collect all employees per department using a plain dict, then compute stats
- `dept_stats = {dept: {"count": len(members), ...} for dept, members in grouped.items()}`
- For `avg_salary`, build a parallel dict of `{dept: [salaries]}` first

---

**Q2. Dictionary Inversion with Duplicate Values**

*Difficulty: Advanced*

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
```

Part A: Invert the dict so that each course maps to a **sorted** list of students enrolled:
```python
{"Python": ["Alice", "Carol", "Eve"], "JavaScript": ["Bob", "Frank"], ...}
```

Part B: From the inverted dict, find:
- The most popular course (most students)
- The least popular course
- Any courses with exactly one student
- Total unique courses

Part C: Write a function `invert_dict(d)` that works for any dict where values may repeat.

**Hints:**
- Use `setdefault()` or test-and-insert to build the inverted dict
- `max(inverted, key=lambda k: len(inverted[k]))` for most popular
- You can also do this in one pass with a comprehension using `.items()`

---

**Q3. Matrix Transposition with Comprehensions**

*Difficulty: Advanced*

```python
matrix = [
    [1,  2,  3,  4],
    [5,  6,  7,  8],
    [9, 10, 11, 12],
]
```

Part A: Transpose the matrix using a nested list comprehension (do not use `zip`):
```python
# Input is 3 rows × 4 cols → output should be 4 rows × 3 cols
[[1, 5, 9], [2, 6, 10], [3, 7, 11], [4, 8, 12]]
```

Part B: Verify your result using `zip(*matrix)` and confirm both methods give the same output.

Part C: Write a function `matrix_multiply(A, B)` that multiplies two matrices using
list comprehensions. Test with:
```python
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
# Expected: [[19, 22], [43, 50]]
```

**Hints:**
- For the transpose: `[[matrix[row][col] for row in range(len(matrix))] for col in range(len(matrix[0]))]`
- For multiplication: `result[i][j] = sum(A[i][k] * B[k][j] for k in range(len(B)))`
- Validate dimensions before multiplying (cols of A must equal rows of B)

---

**Q4. Anagram Detection and Grouping**

*Difficulty: Advanced*

```python
word_list = [
    "listen", "silent", "enlist",
    "triangle", "integral", "alerting",
    "python", "typhon",
    "eating", "tinge",
    "hello", "world",
]
```

Part A: Group all anagrams together. Two words are anagrams if they contain exactly
the same letters (case-insensitive). The key insight: sorting the characters of an
anagram always produces the same string.

Expected output (order within groups may vary):
```python
[
    ["listen", "silent", "enlist"],
    ["triangle", "integral", "alerting"],
    ["python", "typhon"],
    ["eating", "tinge"],
    ["hello"],
    ["world"],
]
```

Part B: Filter the result to show only groups with 2 or more anagrams.

Part C: Write a function `are_anagrams(word1, word2)` that returns `True` if the
two words are anagrams.

**Hints:**
- Use `tuple(sorted(word.lower()))` as the dict key for grouping
- Build `{sorted_key: [list of words]}` as you iterate
- Groups with one word are single non-anagram words

---

**Q5. Top-N Word Frequency Counter**

*Difficulty: Advanced*

```python
text = """
Python is a versatile programming language. Python is used for web development,
data science, and automation. Many developers love Python because Python syntax
is clean and Python code is readable. Learning Python is rewarding because Python
has a large and active community that contributes to Python's growth every year.
"""

stop_words = {"is", "a", "and", "for", "many", "because", "has", "to", "that",
              "the", "an", "in", "of", "it", "its", "be", "are", "was", "were"}
```

Write a function `top_words(text, stop_words, n=5)` that:
1. Lowercases the text and strips all punctuation (`,`, `.`, `'`, `"`, `!`, `?`, `\n`)
2. Splits into words and removes empty strings and stop words
3. Counts frequency of each remaining word
4. Returns a list of the top `n` `(word, count)` tuples sorted by count descending,
   then alphabetically for ties

Example call: `top_words(text, stop_words, n=5)`

Expected output (approximate):
```python
[('python', 9), ('language', 1), ('versatile', 1), ...]
```

Also compute:
- Total word count (including stop words)
- Unique word count (excluding stop words)
- The word that appears exactly twice (if any)

**Hints:**
- Use `str.translate(str.maketrans("", "", string.punctuation))` or a manual replace loop
- Use a dict comprehension or `dict.get()` loop to count frequencies
- Sort with `sorted(freq.items(), key=lambda x: (-x[1], x[0]))`

---

**Q6. Nested Dictionary Flattening**

*Difficulty: Advanced*

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
```

Part A: Write a function `flatten(d, parent_key="", sep=".")` that flattens a nested dict
into a single-level dict with dot-notation keys:

```python
{
    "database.host": "localhost",
    "database.port": 5432,
    "database.credentials.username": "admin",
    "database.credentials.password": "secret",
    "app.debug": True,
    "app.version": "1.0.0",
    "app.features.auth": True,
    "app.features.logging.level": "INFO",
    "app.features.logging.file": "app.log",
    "timeout": 30,
}
```

Part B: Write the inverse function `unflatten(d, sep=".")` that reconstructs the
original nested structure from a flat dict.

Part C: Verify round-trip: `unflatten(flatten(config)) == config`

**Hints:**
- Use recursion: if a value is a dict, recurse with `parent_key + sep + child_key`
- Base case: the value is NOT a dict → store it directly
- For `unflatten`, split each key on `sep` and navigate/create the nested structure

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
