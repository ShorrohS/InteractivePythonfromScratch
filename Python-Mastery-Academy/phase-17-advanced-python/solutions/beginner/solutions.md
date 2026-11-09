# Phase 17 — Beginner Exercise Solutions

---

## Q1. Timing Decorator

```python
import time
import functools

def timer(func):
    @functools.wraps(func)       # copies __name__, __doc__, etc. onto wrapper
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()        # high-resolution timer
        result = func(*args, **kwargs)      # call the original function
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_add(a: int, b: int) -> int:
    """Add two numbers after a short delay."""
    time.sleep(0.1)
    return a + b

result = slow_add(3, 4)
print(f"Result: {result}")            # Result: 7
print(f"Name: {slow_add.__name__}")   # Name: slow_add  (not 'wrapper')
print(f"Doc:  {slow_add.__doc__}")    # Doc:  Add two numbers after a short delay.
```

---

## Q2. Countdown Generator

```python
def countdown(n: int):
    """Yield integers from n down to 1."""
    while n > 0:
        yield n      # yield pauses execution and returns the value to the caller
        n -= 1       # resumes here on the next iteration

# Use in a for loop
for value in countdown(5):
    print(value)
# 5  4  3  2  1

# Collect all values at once
print(list(countdown(3)))    # [3, 2, 1]

# Generators are lazy — no memory is allocated for all values up front
gen = countdown(1_000_000)
print(next(gen))              # 1000000 — only the first value is computed
```

---

## Q3. Timer Context Manager

```python
import time
from contextlib import contextmanager

@contextmanager
def timer_context(label: str = ""):
    """Context manager that prints elapsed time for the enclosed with-block."""
    start = time.perf_counter()
    yield                                    # with-block runs here; we pause at yield
    elapsed = time.perf_counter() - start
    print(f"{label} elapsed: {elapsed:.4f}s")

with timer_context("data processing"):
    total = sum(range(1_000_000))            # simulate some work
# data processing elapsed: 0.0312s

# @contextmanager converts a generator with exactly one yield into a context manager:
#   code before yield  →  __enter__
#   code after yield   →  __exit__
```

---

## Q4. Add Type Hints

```python
# Python 3.9+ syntax: built-in list[float] instead of List[float] from typing

def add(a: int, b: int) -> int:
    return a + b

def greet(name: str) -> str:
    return f"Hello, {name}!"

def average(numbers: list[float]) -> float:
    """Average of a list of numbers."""
    return sum(numbers) / len(numbers)

# Type hints are advisory — tools like mypy and IDEs use them, but Python
# does NOT enforce them at runtime. Passing the wrong type won't raise an error
# unless you add explicit validation.

print(add(2, 3))                    # 5
print(greet("Alice"))               # Hello, Alice!
print(average([1.0, 2.0, 3.0]))     # 2.0
```

---

## Q5. Memoised Fibonacci

```python
import functools

@functools.lru_cache(maxsize=None)    # cache every unique argument indefinitely
def fib(n: int) -> int:
    """Return the nth Fibonacci number (0-indexed)."""
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)   # recursive; cache turns O(2^n) into O(n)

for i in range(10):
    print(f"fib({i}) = {fib(i)}")

# Inspect cache usage
print(f"\nCache info: {fib.cache_info()}")
# CacheInfo(hits=8, misses=10, maxsize=None, currsize=10)
# Without lru_cache, fib(35) would make ~29 million function calls
```

---

> **Exercises:** → [../../exercises/beginner/exercises.md](../../exercises/beginner/exercises.md)
