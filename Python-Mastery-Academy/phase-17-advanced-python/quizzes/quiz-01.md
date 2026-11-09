# Phase 17 — Quiz 01: Advanced Python

**Questions:** 20 | **Pass:** 16/20 | **Time:** 25 min (no notes)

---

## Section 1: Decorators (Q1–Q4)

**Q1.** What is the primary purpose of `@functools.wraps(func)` inside a decorator?
```
A) It speeds up the decorated function by caching results
B) It copies __name__, __doc__, and other attributes from func onto the wrapper
C) It converts the function into a coroutine
D) It prevents the decorator from being applied more than once
```

---

**Q2.** What is printed when `greet("Alice")` is called?
```python
def bold(func):
    def wrapper(*args, **kwargs):
        print("before")
        result = func(*args, **kwargs)
        print("after")
        return result
    return wrapper

@bold
def greet(name):
    print(f"Hi, {name}")

greet("Alice")
```
```
A) Hi, Alice
B) before
   Hi, Alice
   after
C) after
   Hi, Alice
   before
D) before
   after
```

---

**Q3.** Given `@logger @timer @cache def f(): ...`, which decorator's wrapper runs **first** when `f()` is called?
```
A) cache  — it is closest to the original function
B) timer  — it is in the middle
C) logger — it is the outermost wrapper
D) All wrappers run simultaneously
```

---

**Q4.** What is a **decorator factory**?
```
A) A built-in Python class that auto-generates decorators
B) A function that accepts parameters and returns a decorator
C) A decorator that wraps class instances instead of functions
D) A special method called __decorate__ on a class
```

---

## Section 2: Generators (Q5–Q8)

**Q5.** Which keyword turns a regular function into a generator function?
```
A) return
B) async
C) yield
D) generate
```

---

**Q6.** What does `list(gen)` return when `gen` is an already-exhausted generator?
```
A) Raises StopIteration
B) Returns the last yielded value
C) Returns an empty list []
D) Resets the generator and returns all values again
```

---

**Q7.** What is printed by this code?
```python
def counter():
    yield 10
    yield 20
    yield 30

g = counter()
print(next(g))
print(next(g))
print(list(g))
```
```
A) 10
   20
   [30]
B) 10
   20
   [10, 20, 30]
C) 10
   20
   30
D) [10, 20, 30]
```

---

**Q8.** What must you do before calling `.send(value)` on a generator for the **first** time?
```
A) Call .close() to initialise the generator's internal state
B) Call next() to prime the generator and advance it to the first yield
C) Call .throw() to set the generator's starting context
D) Nothing — .send() can be called immediately on a new generator
```

---

## Section 3: Context Managers (Q9–Q11)

**Q9.** Which two methods are required for a class-based context manager?
```
A) __init__ and __del__
B) __open__ and __close__
C) __enter__ and __exit__
D) __start__ and __stop__
```

---

**Q10.** What does returning `True` from `__exit__` do?
```
A) Re-raises the exception that occurred inside the with-block
B) Suppresses the exception — prevents it from propagating further
C) Closes the context manager and prevents re-entry
D) Triggers the __enter__ method again
```

---

**Q11.** What is printed?
```python
class CM:
    def __enter__(self):
        print("A")
        return "X"
    def __exit__(self, *args):
        print("C")
        return False

with CM() as val:
    print(f"B:{val}")
print("D")
```
```
A) A
   B:X
   C
   D
B) A
   C
   B:X
   D
C) B:X
   A
   C
   D
D) A
   B:CM
   C
   D
```

---

## Section 4: Type Hints & Dataclasses (Q12–Q14)

**Q12.** Are Python type hints enforced at runtime?
```
A) Yes — passing the wrong type raises TypeError automatically
B) No — they are hints for static analysis tools (mypy, IDEs) only
C) Only for built-in types like int and str
D) Only when from __future__ import annotations is present
```

---

**Q13.** When does `__post_init__` run in a dataclass?
```
A) Before __init__, to set up default values
B) Only when the instance is serialised to JSON
C) Automatically after __init__ completes — used for validation and transformation
D) Only when called explicitly
```

---

**Q14.** What is the correct, complete type annotation for a function that accepts a `str` and returns nothing?
```
A) def func(s: str) -> None:
B) def func(s: str) -> void:
C) def func(s: str) -> Null:
D) def func(s: str) -> Empty:
```

---

## Section 5: Async & Concurrency (Q15–Q18)

**Q15.** What happens when you call an `async def` function **without** `await`?
```
A) The function runs synchronously and returns the result
B) A coroutine object is returned without the function body executing
C) RuntimeError is raised immediately
D) The event loop schedules it in a background thread
```

---

**Q16.** Which `asyncio` function runs multiple coroutines **concurrently** and returns all their results?
```
A) asyncio.run()
B) asyncio.wait()
C) asyncio.gather()
D) asyncio.sleep()
```

---

**Q17.** Which threading synchronisation primitive prevents race conditions on shared mutable data?
```
A) threading.Semaphore
B) threading.Lock
C) threading.Event
D) threading.Barrier
```

---

**Q18.** What is printed?
```python
import asyncio

async def shout(msg: str) -> str:
    await asyncio.sleep(0)
    return msg.upper()

async def main():
    results = await asyncio.gather(shout("hello"), shout("world"))
    print(results)

asyncio.run(main())
```
```
A) ['hello', 'world']
B) ['HELLO', 'WORLD']
C) HELLO WORLD
D) Error — gather() cannot accept coroutines directly
```

---

## Section 6: Functional Python (Q19–Q20)

**Q19.** What does `functools.partial(multiply, 3)` return when `multiply = lambda a, b: a * b`?
```
A) The integer 3
B) A new callable that multiplies its single argument by 3
C) A generator that yields multiples of 3
D) A copy of the multiply lambda
```

---

**Q20.** What is required before passing a list to `itertools.groupby` to get correct, complete groups?
```
A) The list must be deduplicated first
B) The list must be sorted by the same key used for grouping
C) The list must be converted to a set
D) Each element must be a named tuple
```

---

## Answers

.
.
.
.
.
.

| Q  | Answer | Explanation |
|----|--------|-------------|
| 1  | B | `@functools.wraps` preserves `__name__`, `__doc__`, and other metadata |
| 2  | B | wrapper prints "before", calls `greet` (which prints), then prints "after" |
| 3  | C | At call time, the outermost decorator's wrapper runs first |
| 4  | B | A decorator factory takes parameters and returns a decorator |
| 5  | C | `yield` turns a function into a generator |
| 6  | C | Consuming an exhausted generator with `list()` returns `[]` |
| 7  | A | Two `next()` calls consume the first two yields; `list(g)` gets the remaining `[30]` |
| 8  | B | Must prime with `next()` before sending a non-None value |
| 9  | C | `__enter__` and `__exit__` are the context manager protocol |
| 10 | B | `return True` from `__exit__` suppresses the exception |
| 11 | A | `__enter__` runs (A), with-block runs (B:X), `__exit__` runs (C), then D |
| 12 | B | Type hints are for static analysis tools only — not enforced at runtime |
| 13 | C | `__post_init__` runs automatically after `__init__` |
| 14 | A | `-> None` is the correct return annotation for void functions |
| 15 | B | Calling an async function without `await` returns a coroutine object |
| 16 | C | `asyncio.gather()` runs coroutines concurrently |
| 17 | B | `threading.Lock` prevents race conditions |
| 18 | B | `shout` returns `msg.upper()`, so the result is `['HELLO', 'WORLD']` |
| 19 | B | `functools.partial` fixes the first argument, creating a specialised callable |
| 20 | B | `groupby` groups consecutive equal keys — unsorted input produces duplicate groups |
