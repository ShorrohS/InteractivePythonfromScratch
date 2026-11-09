# Phase 17 — Advanced Python Cheat Sheet

---

## Decorator Basics

```python
import functools

def my_decorator(func):
    @functools.wraps(func)          # preserves __name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        # -- setup --
        result = func(*args, **kwargs)
        # -- teardown --
        return result
    return wrapper

@my_decorator
def greet(name: str) -> str:
    """Return a greeting."""
    return f"Hello, {name}!"
```

---

## Parameterized Decorator Factory

```python
def repeat(times: int):             # factory — accepts parameters
    def decorator(func):            # actual decorator
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(times=3)
def say(msg: str) -> None:
    print(msg)
```

---

## Generator Syntax

```python
# yield — pause and emit a value
def countdown(n: int):
    while n > 0:
        yield n
        n -= 1

# yield from — delegate to another iterable
def chain(a, b):
    yield from a
    yield from b

# send() — coroutine pattern (prime with next() first)
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)           # prime
acc.send(10)        # → 10
acc.send(20)        # → 30
```

---

## @contextmanager Pattern

```python
from contextlib import contextmanager

@contextmanager
def managed_resource(name: str):
    print(f"Opening {name}")
    resource = {"name": name, "open": True}
    try:
        yield resource          # with-block runs here
    finally:
        resource["open"] = False
        print(f"Closing {name}")

with managed_resource("db") as r:
    print(r["open"])            # True
```

---

## Class-Based Context Manager

```python
class ManagedFile:
    def __init__(self, path: str, mode: str = "r"):
        self.path = path
        self.mode = mode
        self._file = None

    def __enter__(self):
        self._file = open(self.path, self.mode)
        return self._file           # bound to 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file:
            self._file.close()
        return False                # False = don't suppress exceptions
                                    # True  = suppress (swallow) the exception

with ManagedFile("data.txt") as f:
    content = f.read()
```

---

## Type Hints

```python
from typing import Optional, Union, List, Dict, Callable, Tuple

def process(
    name:     str,
    count:    int,
    values:   list[float],                  # Python 3.9+
    mapping:  dict[str, int],               # Python 3.9+
    callback: Callable[[int], str],
    label:    Optional[str] = None,         # str | None
    result:   Union[int, float] = 0,        # int or float
) -> tuple[str, int]:                       # Python 3.9+
    return name, count

# Type aliases
Vector = list[float]
Matrix = list[list[float]]

# Older style (Python 3.5–3.8)
from typing import List, Dict, Tuple, Optional
def old_style(names: List[str]) -> Dict[str, int]: ...
```

---

## Dataclass Syntax

```python
from dataclasses import dataclass, field
from typing import ClassVar

@dataclass
class Employee:
    name:       str
    salary:     float
    department: str    = "Engineering"              # default value
    skills:     list   = field(default_factory=list)  # mutable default
    _id_counter: ClassVar[int] = 0                  # class variable (not a field)

    def __post_init__(self):
        """Runs after __init__ — use for validation and derived fields."""
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")
        self.name = self.name.strip().title()

    @property
    def summary(self) -> str:
        return f"{self.name} ({self.department}) — ${self.salary:,.0f}"

e = Employee("alice smith", 75000.0)
print(e.summary)   # Alice Smith (Engineering) — $75,000
```

---

## async / await Patterns

```python
import asyncio

# Basic async function
async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)      # non-blocking wait
    return f"data from {url}"

# Concurrent execution — all tasks run at the same time
async def fetch_all(urls: list) -> list:
    return await asyncio.gather(*[fetch(u) for u in urls])

# Sequential execution — one at a time
async def fetch_seq(urls: list) -> list:
    results = []
    for url in urls:
        results.append(await fetch(url))
    return results

# asyncio.Queue — producer / consumer
async def producer(q: asyncio.Queue):
    for i in range(5):
        await q.put(i)
    await q.put(None)             # sentinel

async def consumer(q: asyncio.Queue):
    while (item := await q.get()) is not None:
        print(item)

async def main():
    q = asyncio.Queue()
    await asyncio.gather(producer(q), consumer(q))

asyncio.run(main())               # entry point for async code
```

---

## itertools Quick Reference

```python
import itertools

# chain — flatten multiple iterables into one
list(itertools.chain([1, 2], [3, 4], [5]))        # [1, 2, 3, 4, 5]

# groupby — group consecutive equal keys (sort first!)
data = sorted([("a", 1), ("b", 2), ("a", 3)], key=lambda x: x[0])
for key, grp in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(grp))

# islice — lazy slice of any iterable
list(itertools.islice(range(100), 5, 15, 2))      # [5, 7, 9, 11, 13]

# product — Cartesian product (like nested for-loops)
list(itertools.product("AB", [1, 2]))              # [('A',1),('A',2),('B',1),('B',2)]

# combinations — ordered subsets, no repetition
list(itertools.combinations("ABC", 2))             # [('A','B'),('A','C'),('B','C')]

# combinations_with_replacement — repetition allowed
list(itertools.combinations_with_replacement("AB", 2))  # [('A','A'),('A','B'),('B','B')]

# takewhile / dropwhile
list(itertools.takewhile(lambda x: x < 4, [1,2,3,4,5]))  # [1, 2, 3]
list(itertools.dropwhile(lambda x: x < 4, [1,2,3,4,5]))  # [4, 5]
```

---

## functools Quick Reference

```python
import functools

# wraps — copy metadata from wrapped function to wrapper
@functools.wraps(func)
def wrapper(*args, **kwargs): ...

# lru_cache — memoize function results (caches by argument tuple)
@functools.lru_cache(maxsize=128)
def fib(n: int) -> int:
    return n if n <= 1 else fib(n-1) + fib(n-2)
fib.cache_info()      # CacheInfo(hits=..., misses=..., ...)
fib.cache_clear()     # clear the cache

# partial — fix one or more arguments of a function
multiply = lambda a, b: a * b
double   = functools.partial(multiply, 2)   # double(5) → 10
triple   = functools.partial(multiply, 3)   # triple(5) → 15

# reduce — fold a sequence into a single value
functools.reduce(lambda acc, x: acc + x, [1, 2, 3, 4])   # 10
functools.reduce(lambda acc, x: acc * x, [1,2,3,4], 1)   # 24  (with initial)

# cache (Python 3.9+) — shorthand for lru_cache(maxsize=None)
@functools.cache
def expensive(n: int) -> int: ...
```
