# Phase 17 — Intermediate Exercise Solutions

---

## Q1. Retry Decorator Factory

```python
import time
import functools
import random

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator factory: retries the wrapped function on any exception."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise        # all retries exhausted — re-raise last exception
                    print(f"Attempt {attempt}/{max_attempts} failed: {e}. "
                          f"Retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

# Three levels of nesting: factory → decorator → wrapper
@retry(max_attempts=3, delay=0.1)
def flaky_task(x: int) -> str:
    """Fails ~70% of the time to demonstrate retrying."""
    if random.random() < 0.7:
        raise ValueError("Random failure")
    return f"Success: {x}"

try:
    print(flaky_task(42))
except ValueError as e:
    print(f"All attempts exhausted: {e}")
```

---

## Q2. Generator Pipeline

```python
transactions = [
    {"name": "Lunch",         "amount": 12.50, "category": "food"},
    {"name": "Bus",           "amount":  2.00, "category": "transport"},
    {"name": "Dinner",        "amount": 38.00, "category": "food"},
    {"name": "Movie",         "amount": 15.00, "category": "entertainment"},
    {"name": "Coffee",        "amount":  4.50, "category": "food"},
]

def filter_category(records, category: str):
    """Yield only records whose category field matches."""
    for record in records:
        if record["category"] == category:
            yield record          # lazy — processes one record at a time

def extract_amounts(records):
    """Yield just the amount value from each record."""
    for record in records:
        yield record["amount"]

# Chain generators into a pipeline — nothing runs until sum() pulls values
food_amounts = extract_amounts(filter_category(transactions, "food"))
total = sum(food_amounts)
print(f"Food total: ${total:.2f}")    # Food total: $55.00

# Generator pipelines are memory-efficient — no intermediate lists are created
```

---

## Q3. Class-Based Context Manager

```python
class MockDatabase:
    """Class-based context manager simulating a database connection."""

    def __init__(self, host: str):
        self.host = host
        self.connection = None

    def __enter__(self):
        """Called on entry to the with-block; the return value is bound to 'as'."""
        print(f"Connecting to {self.host}...")
        self.connection = {"host": self.host, "status": "open"}
        return self.connection       # available as the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called on exit — even if an exception occurred inside the with-block."""
        print(f"Closing connection to {self.host}...")
        self.connection["status"] = "closed"
        if exc_type is not None:
            print(f"Exception detected: {exc_val}. Rolling back transaction.")
        return False    # False = do NOT suppress exceptions; True would swallow them

with MockDatabase("localhost:5432") as db:
    print(f"Status: {db['status']}")   # Status: open
    print("Executing query...")
print(f"After block: {db['status']}")  # After block: closed
```

---

## Q4. Dataclass with Validation

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Product:
    name:     str
    price:    float
    quantity: int
    TAX_RATE: ClassVar[float] = 0.1    # ClassVar is excluded from __init__ and __repr__

    def __post_init__(self):
        """Runs automatically after __init__ — ideal for validation and normalisation."""
        if self.price < 0:
            raise ValueError(f"Price must be non-negative, got {self.price}")
        if self.quantity < 0:
            raise ValueError(f"Quantity must be non-negative, got {self.quantity}")
        self.name = self.name.strip().title()    # normalise: "  laptop  " → "Laptop"

    @property
    def total_value(self) -> float:
        """Computed on access — not stored as a field."""
        return self.price * self.quantity

    @property
    def total_with_tax(self) -> float:
        return self.total_value * (1 + self.TAX_RATE)

p = Product(name="  laptop  ", price=999.99, quantity=3)
print(p)                              # Product(name='Laptop', price=999.99, quantity=3)
print(f"Name:      {p.name}")         # Laptop
print(f"Total:     ${p.total_value:,.2f}")       # $2,999.97
print(f"With tax:  ${p.total_with_tax:,.2f}")    # $3,299.97

try:
    bad = Product("Chair", -50.0, 1)
except ValueError as e:
    print(f"Error: {e}")              # Error: Price must be non-negative, got -50.0
```

---

## Q5. Async Concurrent Fetch

```python
import asyncio

async def fetch_url(url: str) -> dict:
    """Simulate an async HTTP request with a 100 ms delay."""
    await asyncio.sleep(0.1)    # yields control to the event loop during the "wait"
    return {"url": url, "status": 200, "content": f"Content of {url}"}

async def fetch_all(urls: list) -> list:
    """Fetch all URLs concurrently — total time ≈ 100 ms, not N × 100 ms."""
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)    # all tasks run at the same time
    return results

urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
]

results = asyncio.run(fetch_all(urls))    # asyncio.run() is the entry point
for r in results:
    print(f"{r['url']} -> status {r['status']}")
# https://example.com/page1 -> status 200
# https://example.com/page2 -> status 200
# https://example.com/page3 -> status 200
```

---

## Q6. Group Transactions with itertools

```python
import itertools

transactions = [
    {"category": "food",          "amount": 45.00},
    {"category": "transport",     "amount": 12.50},
    {"category": "food",          "amount": 32.00},
    {"category": "entertainment", "amount": 89.00},
    {"category": "transport",     "amount":  8.00},
    {"category": "food",          "amount": 21.00},
]

# CRITICAL: groupby produces one group per consecutive run of the same key.
# Without sorting first, "food" would appear as two separate groups.
sorted_txns = sorted(transactions, key=lambda t: t["category"])

for category, group in itertools.groupby(sorted_txns, key=lambda t: t["category"]):
    items = list(group)      # consume the group iterator into a list
    total = sum(t["amount"] for t in items)
    print(f"{category}: {len(items)} transactions, total ${total:.2f}")
# entertainment: 1 transactions, total $89.00
# food: 3 transactions, total $98.00
# transport: 2 transactions, total $20.50
```

---

## Q7. Partial and Reduce Pipeline

```python
import functools

# Generic two-argument functions
def multiply(factor: float, x: float) -> float:
    return x * factor

def add(amount: float, x: float) -> float:
    return x + amount

def clamp(minimum: float, maximum: float, x: float) -> float:
    return max(minimum, min(maximum, x))

# functools.partial fixes the first argument(s), returning a new single-arg callable
double    = functools.partial(multiply, 2)
add_ten   = functools.partial(add, 10)
clamp_100 = functools.partial(clamp, 0, 100)

def pipeline(*funcs):
    """Return a function that threads a value through each function in sequence."""
    def apply(value, func):
        return func(value)
    return lambda x: functools.reduce(apply, funcs, x)

transform = pipeline(double, add_ten, clamp_100)

for n in [5, 50, 60]:
    print(f"{n:>3} -> {transform(n)}")
# Output:
#   5 -> 20   (5×2=10  → 10+10=20  → clamp=20)
#  50 -> 100  (50×2=100 → 100+10=110 → clamp=100)
#  60 -> 100  (60×2=120 → 120+10=130 → clamp=100)
```

---

> **Exercises:** → [../../exercises/intermediate/exercises.md](../../exercises/intermediate/exercises.md)
