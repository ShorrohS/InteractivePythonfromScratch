# 📝 Phase 17 — Beginner Exercises

> Difficulty: ⭐
> Attempt ALL questions before opening solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

**Q1. Timing Decorator**

Write a `timer` decorator that measures and prints how long a decorated function takes to run.
Use `functools.wraps` to preserve the original function's `__name__` and `__doc__`.

Example usage:
```python
@timer
def slow_add(a, b):
    """Add two numbers."""
    time.sleep(0.1)
    return a + b

result = slow_add(3, 4)
# slow_add took 0.1003s
# result == 7

print(slow_add.__name__)  # slow_add  (not 'wrapper')
```

(Hint: use `time.perf_counter()` before and after calling `func(*args, **kwargs)`; apply `@functools.wraps(func)` to the inner `wrapper` function, not to the outer decorator itself)

---

**Q2. Countdown Generator**

Write a generator function `countdown(n)` that yields integers from `n` down to `1` inclusive.

Example:
```python
for value in countdown(5):
    print(value)
# 5
# 4
# 3
# 2
# 1

print(list(countdown(3)))  # [3, 2, 1]
```

(Hint: use `yield` instead of `return`; a `while n > 0:` loop with `n -= 1` after the yield works well)

---

**Q3. Timer Context Manager**

Using `@contextmanager` from `contextlib`, write a `timer_context(label)` context manager that:
- Records the start time when the `with` block is entered
- Prints the elapsed time in seconds when the block exits

Example:
```python
with timer_context("my block"):
    time.sleep(0.05)
# my block elapsed: 0.0502s
```

(Hint: code before `yield` runs on entry; code after `yield` runs on exit; use `time.perf_counter()`)

---

**Q4. Add Type Hints**

These three functions have no type annotations. Add complete type hints to each — both parameters and return type:

```python
def add(a, b):
    return a + b

def greet(name):
    return f"Hello, {name}!"

def average(numbers):
    return sum(numbers) / len(numbers)
```

(Hint: use `int`, `float`, `str` for basic types; for the list parameter use `list[float]` in Python 3.9+, or `List[float]` from `typing` for earlier versions)

---

**Q5. Memoised Fibonacci**

Write a recursive `fib(n)` function that returns the nth Fibonacci number.
Decorate it with `@functools.lru_cache` so repeated calls use cached results instead of recomputing.

Expected output for `n = 0` through `9`:
```
fib(0) = 0
fib(1) = 1
fib(2) = 1
fib(3) = 2
fib(4) = 3
fib(5) = 5
fib(6) = 8
fib(7) = 13
fib(8) = 21
fib(9) = 34
```

(Hint: `@functools.lru_cache(maxsize=None)` caches every unique argument; without it, `fib(35)` calls the function millions of times due to repeated sub-problems)

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
