# Phase 17 — Completion Assessment

> Complete before moving to Phase 18.
> Pass mark: 80% (11/13) | Time: 40 minutes

---

## PART A: Practical Coding Tasks

**Task 1.** Write a `retry_with_backoff` decorator that:
- Accepts `max_attempts` (int) and `base_delay` (float, seconds)
- Retries the decorated function on any exception
- Doubles the delay on each retry (exponential backoff): attempt 1 waits `base_delay`, attempt 2 waits `2 × base_delay`, attempt 3 waits `4 × base_delay`, etc.
- Re-raises the last exception after all retries are exhausted
- Preserves the original function's `__name__` and `__doc__`

Example usage:
```python
@retry_with_backoff(max_attempts=4, base_delay=0.5)
def call_api(url: str) -> dict:
    """Fetch data from a URL."""
    ...
```

---

**Task 2.** Build a `lazy_line_reader(filepath)` generator that:
- Opens the given file
- Yields one line at a time (stripped of trailing whitespace)
- Skips blank lines
- Never loads the entire file into memory at once

Example usage:
```python
for line in lazy_line_reader("data.txt"):
    print(line)
```

(Test it by creating a small temporary text file in code and reading it back.)

---

**Task 3.** Create a class-based context manager `TempDirectory` that:
- In `__enter__`: creates a temporary directory using `tempfile.mkdtemp()`, prints the path, and returns it
- In `__exit__`: removes the directory and all its contents using `shutil.rmtree()`, even if an exception occurred inside the with-block; prints a confirmation message

Example:
```python
with TempDirectory() as tmpdir:
    # write files to tmpdir
    print(f"Working in: {tmpdir}")
# Removed temporary directory: /tmp/tmpXXXXXX
```

---

**Task 4.** The function below runs synchronously and fetches three pieces of data one after another:

```python
import time

def get_user(user_id: int) -> dict:
    time.sleep(0.2)   # simulate a slow I/O operation
    return {"id": user_id, "name": f"User {user_id}"}

def get_all_users(ids: list) -> list:
    results = []
    for uid in ids:
        results.append(get_user(uid))
    return results

users = get_all_users([1, 2, 3])
# Takes ~0.6s — sequential
```

Convert both functions to `async` versions (`async_get_user` and `async_get_all_users`) so all three requests happen **concurrently** using `asyncio.gather`. The total time should be ~0.2s instead of ~0.6s.

---

## PART B: Written Questions

**Q5.** Explain the difference between a **list** and a **generator**. Give one scenario where a generator is clearly the better choice.

---

**Q6.** What is `asyncio.gather()` and how does it differ from calling `await coroutine()` three times in a row?

---

**Q7.** Describe the **descriptor protocol**. What are `__get__`, `__set__`, and `__delete__` used for? Give a real-world use case.

---

**Q8.** What is the **Global Interpreter Lock (GIL)** and how does it affect the choice between `threading` and `multiprocessing` for CPU-bound vs I/O-bound tasks?

---

**Q9.** What does `@dataclass` automatically generate for you? Name at least four things, and explain when you would add `__post_init__`.

---

## PART C: Predict the Output

Write down what each code block prints **before running it**.

**Q10.**
```python
def wrap_a(func):
    def inner():
        return "[A:" + func() + ":A]"
    return inner

def wrap_b(func):
    def inner():
        return "[B:" + func() + ":B]"
    return inner

@wrap_a
@wrap_b
def text():
    return "hello"

print(text())
```

---

**Q11.**
```python
def gen():
    for i in [1, 2, 3]:
        yield i * 2

g = gen()
print(next(g))
print(next(g))
for val in g:
    print(val)
print(list(g))
```

---

**Q12.**
```python
class Quiet:
    def __enter__(self):
        return self
    def __exit__(self, et, ev, tb):
        print(f"exit: {et is not None}")
        return True

with Quiet():
    x = 1 / 0
print("done")
```

---

**Q13.**
```python
import functools

call_count = 0

@functools.lru_cache(maxsize=3)
def sq(n: int) -> int:
    global call_count
    call_count += 1
    return n * n

for n in [2, 3, 2, 4, 3]:
    print(sq(n), end=" ")
print(f"\ncalls: {call_count}")
```

---

## Scoring

| Section | Items | Points each | Total |
|---------|-------|-------------|-------|
| Part A  | 4     | 1           | 4     |
| Part B  | 5     | 1           | 5     |
| Part C  | 4     | 1           | 4     |
| **Total** | **13** | — | **13** |

| Score  | Action |
|--------|--------|
| 11–13  | Move to Phase 18 |
| 9–10   | Review weak areas, then proceed |
| < 9    | Redo Phase 17 lessons before continuing |

---

## Answer Key

**Task 1 — expected implementation:**
```python
import time
import functools

def retry_with_backoff(max_attempts: int = 3, base_delay: float = 1.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2   # exponential backoff
        return wrapper
    return decorator
```

**Task 2 — expected implementation:**
```python
def lazy_line_reader(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.rstrip()
            if line:       # skip blank lines
                yield line
```

**Task 3 — expected implementation:**
```python
import tempfile
import shutil

class TempDirectory:
    def __enter__(self) -> str:
        self._path = tempfile.mkdtemp()
        print(f"Created temporary directory: {self._path}")
        return self._path

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self._path, ignore_errors=True)
        print(f"Removed temporary directory: {self._path}")
        return False   # do not suppress exceptions
```

**Task 4 — expected implementation:**
```python
import asyncio

async def async_get_user(user_id: int) -> dict:
    await asyncio.sleep(0.2)
    return {"id": user_id, "name": f"User {user_id}"}

async def async_get_all_users(ids: list) -> list:
    return await asyncio.gather(*[async_get_user(uid) for uid in ids])

users = asyncio.run(async_get_all_users([1, 2, 3]))
```

**Q10:** `[A:[B:hello:B]:A]`
- `@wrap_b` is applied first: `text()` → `"[B:hello:B]"`
- `@wrap_a` wraps that result: `"[A:[B:hello:B]:A]"`

**Q11:**
```
2
4
6
[]
```
- `next(g)` → 2, `next(g)` → 4
- `for val in g` gets remaining value: 6
- `list(g)` on exhausted generator → `[]`

**Q12:**
```
exit: True
done
```
- `ZeroDivisionError` is raised inside the with-block
- `__exit__` receives it, prints `exit: True`, and returns `True` (suppressed)
- Execution continues normally → prints `done`

**Q13:**
```
4 9 4 16 9 
calls: 3
```
- `sq(2)` → miss → calls=1 → 4
- `sq(3)` → miss → calls=2 → 9
- `sq(2)` → **hit** → calls=2 → 4
- `sq(4)` → miss → calls=3 → 16
- `sq(3)` → **hit** → calls=3 → 9
