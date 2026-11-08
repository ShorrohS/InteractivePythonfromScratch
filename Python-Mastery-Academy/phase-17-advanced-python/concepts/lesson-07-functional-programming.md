# Lesson 07 — Functional Programming

**Phase:** 17 — Advanced Python | **Time:** ~40 min

---

## Part 1: Functional Programming Concepts

Functional programming (FP) treats computation as the evaluation of mathematical functions. Python is not a purely functional language, but it has strong support for the style.

**Pure functions** — same input always produces the same output, with no side effects:

```python
# Pure: depends only on its arguments, touches nothing outside itself
def add(a: int, b: int) -> int:
    return a + b

# Impure: reads from external state, modifies it
total = 0
def add_to_total(n: int) -> int:
    global total          # side effect — mutates external state
    total += n
    return total
```

**Immutability** — instead of changing data in place, produce new data:

```python
prices = [10.0, 20.0, 30.0]

# Mutable style (modifies the original list)
for i, p in enumerate(prices):
    prices[i] = round(p * 1.1, 2)    # original list is destroyed

# Immutable style (original unchanged)
prices = [10.0, 20.0, 30.0]
new_prices = [round(p * 1.1, 2) for p in prices]   # new list, prices intact
```

**Why FP makes code easier to test and reason about:**

- Pure functions have no hidden dependencies — unit tests need no mocking or setup
- No shared mutable state means no race conditions in concurrent code
- Small, composable functions are easier to read and combine into pipelines

---

## Part 2: map(), filter(), zip()

These three built-ins are the workhorses of functional Python.

```python
employees = [
    {"name": "Alice", "salary": 95000, "active": True},
    {"name": "Bob",   "salary": 82000, "active": False},
    {"name": "Carol", "salary": 77000, "active": True},
]

# ── map(func, iterable) — transform every element ─────────────────
names = list(map(lambda e: e["name"], employees))
# ["Alice", "Bob", "Carol"]

# A named function is cleaner than lambda for complex transforms
def get_name(emp: dict) -> str:
    return emp["name"].upper()

upper_names = list(map(get_name, employees))
# ["ALICE", "BOB", "CAROL"]

# ── filter(func, iterable) — keep elements where func returns True ─
active = list(filter(lambda e: e["active"], employees))
# [{"name": "Alice", ...}, {"name": "Carol", ...}]

inactive_count = sum(1 for e in employees if not e["active"])
# 1 (Bob)

# ── zip(a, b) — pair up two sequences element-by-element ──────────
months = ["Jan", "Feb", "Mar"]
sales  = [12400, 15800,  9300]

monthly_report = list(zip(months, sales))
# [("Jan", 12400), ("Feb", 15800), ("Mar", 9300)]

for month, amount in zip(months, sales):
    print(f"{month}: ${amount:,}")
```

**All three are lazy** — they return iterators, not lists. Wrap in `list()` to materialise, or iterate directly for memory efficiency:

```python
# Memory-efficient: no intermediate list is created
total_payroll = sum(map(lambda e: e["salary"], employees))
# 254000
```

---

## Part 3: functools

The `functools` module extends Python's functional toolkit.

```python
from functools import reduce, partial, lru_cache

# ── reduce(func, iterable[, initial]) ────────────────────────────
# Fold a sequence down to a single value

numbers = [1, 2, 3, 4, 5]

total   = reduce(lambda acc, x: acc + x, numbers)        # 15
product = reduce(lambda acc, x: acc * x, numbers, 1)     # 120 (1 is the initial value)

# Merge a list of dicts into one
dicts  = [{"a": 1}, {"b": 2}, {"c": 3}]
merged = reduce(lambda acc, d: {**acc, **d}, dicts)
# {"a": 1, "b": 2, "c": 3}


# ── partial(func, *args, **kwargs) ────────────────────────────────
# Pre-fill some arguments to create a more specialised function

def power(base: float, exponent: float) -> float:
    return base ** exponent

square = partial(power, exponent=2)   # exponent pre-filled to 2
cube   = partial(power, exponent=3)   # exponent pre-filled to 3

print(square(4))   # 16.0
print(cube(3))     # 27.0

# Practical: create a convenience logger
import logging
log_error = partial(logging.log, logging.ERROR)
log_error("Something went wrong")   # equivalent to logging.log(logging.ERROR, "...")


# ── lru_cache(maxsize=128) ────────────────────────────────────────
# Memoisation: cache expensive results so they are never recomputed

@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Fibonacci with automatic caching — without it this is O(2^n)."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(fibonacci(50))              # instant — cached results reused for every sub-call
print(fibonacci.cache_info())     # CacheInfo(hits=48, misses=51, maxsize=128, currsize=51)
fibonacci.cache_clear()           # call this to release memory when done
```

---

## Part 4: operator Module

The `operator` module provides named functions for Python operators — useful as `key=` arguments and avoids redundant one-liner lambdas.

```python
from operator import itemgetter, attrgetter, add

employees = [
    {"name": "Carol", "salary": 77000, "department": "Marketing"},
    {"name": "Alice", "salary": 95000, "department": "Engineering"},
    {"name": "Bob",   "salary": 82000, "department": "Engineering"},
]

# ── itemgetter — extract a key from dicts or an index from sequences
by_salary         = sorted(employees, key=itemgetter("salary"))
# lowest to highest

by_dept_then_name = sorted(employees, key=itemgetter("department", "name"))
# sort by department first, then by name within each department

# vs. lambda equivalents (more verbose)
# sorted(employees, key=lambda e: e["salary"])
# sorted(employees, key=lambda e: (e["department"], e["name"]))


# ── attrgetter — extract an attribute from objects ────────────────
from dataclasses import dataclass

@dataclass
class Product:
    name: str
    price: float

products = [
    Product("Pen",      1.50),
    Product("Notebook", 4.99),
    Product("Ruler",    2.25),
]

cheapest_first = sorted(products, key=attrgetter("price"))
# [Product(name='Pen', price=1.5), ...]


# ── operator functions in reduce ──────────────────────────────────
from functools import reduce

total = reduce(add, [10, 20, 30, 40])   # 100 — cleaner than a lambda
```

---

## Part 5: Comprehensions as Functional Style

List, dict, and set comprehensions are idiomatic Python alternatives to `map` and `filter` — often more readable.

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Equivalent to map(lambda n: n ** 2, numbers)
squares = [n ** 2 for n in numbers]

# Equivalent to filter(lambda n: n % 2 == 0, numbers)
evens = [n for n in numbers if n % 2 == 0]

# map + filter in one expression
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
# [4, 16, 36, 64, 100]

# Dict comprehension
word_lengths: dict[str, int] = {w: len(w) for w in ["apple", "banana", "cherry"]}
# {'apple': 5, 'banana': 6, 'cherry': 6}

# Set comprehension — produces unique values
unique_lengths: set[int] = {len(w) for w in ["cat", "dog", "ant", "bear"]}
# {3, 4}


# ── Generator expressions — lazy pipelines ────────────────────────
# Syntax is identical to a list comprehension but uses () instead of []
# No intermediate list is created — memory stays flat

total = sum(n ** 2 for n in range(1_000_000))   # processes one value at a time

# Chained pipeline: filter → transform → aggregate
payroll = sum(
    e["salary"] * 1.05       # 5 % raise
    for e in employees
    if e["active"]            # only active staff
)
```

**Guideline:** use comprehensions when the transform is short and readable. Use `map`/`filter` when you already have a named function:

```python
# Clear — reuses an existing named function
names = list(map(get_name, employees))

# Slightly noisier — lambda just wraps the same function
names = [get_name(e) for e in employees]   # both are fine; pick one and be consistent
```

---

## Part 6: Real-World Pipeline

The same task implemented in both imperative and functional styles, side by side.

**Goal:** from a list of sales records, return the names of the top 3 active reps by revenue.

```python
from operator import itemgetter

sales_data = [
    {"rep": "Alice", "region": "North", "amount": 12400, "active": True},
    {"rep": "Bob",   "region": "South", "amount":  8900, "active": False},
    {"rep": "Carol", "region": "North", "amount": 15800, "active": True},
    {"rep": "Dave",  "region": "East",  "amount": 21300, "active": True},
    {"rep": "Eve",   "region": "South", "amount":  9700, "active": True},
    {"rep": "Frank", "region": "East",  "amount": 18400, "active": True},
]


# ── Imperative style ──────────────────────────────────────────────
def top_reps_imperative(data: list[dict], n: int = 3) -> list[str]:
    """Return names of top-n active reps by amount (for-loop version)."""
    active = []
    for record in data:
        if record["active"]:          # step 1: filter
            active.append(record)

    active.sort(key=lambda r: r["amount"], reverse=True)   # step 2: sort

    result = []
    for record in active[:n]:         # step 3: take top n
        result.append(record["rep"])  # step 4: extract names
    return result


# ── Functional style ──────────────────────────────────────────────
def top_reps_functional(data: list[dict], n: int = 3) -> list[str]:
    """Return names of top-n active reps by amount (pipeline version)."""
    return [
        record["rep"]
        for record in sorted(
            filter(lambda r: r["active"], data),   # 1. filter active records
            key=itemgetter("amount"),               # 2. sort by amount
            reverse=True,
        )[:n]                                       # 3. take top n, extract name
    ]


# Both produce identical results
print(top_reps_imperative(sales_data))    # ['Dave', 'Frank', 'Carol']
print(top_reps_functional(sales_data))    # ['Dave', 'Frank', 'Carol']
```

The functional version is more concise. The imperative version is easier to step through with a debugger. Choose based on the complexity of the transform and what your team finds more readable.

---

## Practice Exercises

1. Use `map` and `filter` to build a list of names for employees earning more than $80,000.

2. Rewrite the above using a list comprehension. Which version do you find more readable?

3. Use `functools.reduce` to find the maximum value in a list — without calling `max()`.

4. Write a `compose(f, g)` function that returns a new function equivalent to `lambda x: f(g(x))`. Test it by composing `str.upper` and `str.strip`.

---

## Next Lesson

**[Lesson 08 → Metaclasses](lesson-08-metaclasses.md)**
