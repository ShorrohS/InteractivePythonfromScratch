# Phase 17 — Intermediate Exercises

> Difficulty: ⭐⭐
> These require writing complete functions or classes, not just single lines.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Retry Decorator Factory**

Write a parameterized decorator factory `retry(max_attempts, delay)` that:
- Retries the decorated function on any exception
- Waits `delay` seconds between attempts
- Re-raises the last exception after all attempts have failed
- Uses `functools.wraps`

Example usage:
```python
@retry(max_attempts=3, delay=0.5)
def flaky_task(x):
    ...  # may raise an exception randomly

# Output when retrying:
# Attempt 1/3 failed: Random failure. Retrying in 0.5s...
# Attempt 2/3 failed: Random failure. Retrying in 0.5s...
# Success: 42
```

(Hint: a decorator factory is a function that *returns* a decorator, which in turn returns a `wrapper`; three levels of nesting in total)

---

**Q2. Generator Pipeline**

Given a list of transaction dicts `[{"name": ..., "amount": ..., "category": ...}, ...]`:
1. Write a generator `filter_category(records, category)` that yields only matching records
2. Write a generator `extract_amounts(records)` that yields only the `amount` from each record
3. Chain them together and use `sum()` to total food-category amounts

Example:
```python
transactions = [
    {"name": "Lunch",  "amount": 12.50, "category": "food"},
    {"name": "Bus",    "amount":  2.00, "category": "transport"},
    {"name": "Dinner", "amount": 38.00, "category": "food"},
]
total = sum(extract_amounts(filter_category(transactions, "food")))
# total == 50.50
```

(Hint: both generators use `for record in records: yield ...`; no list creation needed — they stay lazy)

---

**Q3. Class-Based Context Manager**

Create a class `MockDatabase` that acts as a context manager simulating a database connection:
- `__enter__`: prints a connection message and returns a connection dict `{"host": ..., "status": "open"}`
- `__exit__`: prints a close message; if an exception occurred, print a rollback message

Example:
```python
with MockDatabase("localhost:5432") as db:
    print(db["status"])   # open
    # run queries...
# Closing connection to localhost:5432...
```

(Hint: `__exit__` receives `exc_type, exc_val, exc_tb`; return `False` to let exceptions propagate normally)

---

**Q4. Dataclass with Validation**

Create a `Product` dataclass with fields `name: str`, `price: float`, `quantity: int`.
- In `__post_init__`, raise `ValueError` if `price < 0` or `quantity < 0`
- Normalise `name` to title case in `__post_init__`
- Add a `@property` called `total_value` returning `price * quantity`
- Add a `@property` called `total_with_tax` applying 10% tax to `total_value`

Example:
```python
p = Product(name="  laptop  ", price=999.99, quantity=3)
print(p.name)           # Laptop
print(p.total_value)    # 2999.97
print(p.total_with_tax) # 3299.967
```

(Hint: import `dataclass` from `dataclasses` and `ClassVar` from `typing`; `@property` works normally inside a dataclass)

---

**Q5. Async Concurrent Fetch**

Write an `async` function `fetch_url(url)` that simulates a network request using `await asyncio.sleep(0.1)` and returns `{"url": url, "status": 200}`.

Write an `async` function `fetch_all(urls)` that fetches **all URLs concurrently** using `asyncio.gather`.
Run it with `asyncio.run()` and print each result.

Example:
```python
urls = ["https://example.com/a", "https://example.com/b", "https://example.com/c"]
# All three fetches happen at the same time — total time ≈ 0.1s, not 0.3s
```

(Hint: `asyncio.gather(*[fetch_url(u) for u in urls])` schedules all coroutines concurrently; `await asyncio.sleep()` yields control to the event loop during the simulated wait)

---

**Q6. Group Transactions with itertools**

Given a list of transaction dicts with a `"category"` key, use `itertools.groupby` to print each category and its total amount.

```python
transactions = [
    {"category": "food",          "amount": 45.00},
    {"category": "transport",     "amount": 12.50},
    {"category": "food",          "amount": 32.00},
    {"category": "entertainment", "amount": 89.00},
    {"category": "transport",     "amount":  8.00},
    {"category": "food",          "amount": 21.00},
]
# Expected output:
# entertainment: 1 transactions, total $89.00
# food: 3 transactions, total $98.00
# transport: 2 transactions, total $20.50
```

(Hint: `itertools.groupby` requires the input to be **sorted by the same key** before grouping — unsorted input will create duplicate groups)

---

**Q7. Partial and Reduce Pipeline**

1. Write generic `multiply(factor, x)` and `add(amount, x)` functions
2. Use `functools.partial` to create `double` (multiply by 2) and `add_ten` (add 10)
3. Write a `pipeline(*funcs)` function using `functools.reduce` that applies each function in sequence
4. Test with a `double → add_ten → clamp(0, 100)` pipeline on values 5, 50, 60

Expected:
```
  5 ->  20   (5×2=10 → 10+10=20 → clamp=20)
 50 -> 100   (50×2=100 → 100+10=110 → clamp=100)
 60 -> 100   (60×2=120 → 120+10=130 → clamp=100)
```

(Hint: `functools.reduce(lambda val, fn: fn(val), funcs, initial_value)` threads a value through a sequence of functions)

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
