# ⚡ Phase 17 Cheat Sheet — Advanced Python

---

## Decorators

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)       # preserves __name__, __doc__
    def wrapper(*args, **kwargs):
        # before
        result = func(*args, **kwargs)
        # after
        return result
    return wrapper

@my_decorator
def my_function():
    pass

# Decorator with arguments
def repeat(n):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(3)
def say_hi():
    print("Hi")
```

---

## Generators

```python
def count_up(start=0):
    while True:
        yield start
        start += 1

gen = count_up()
next(gen)    # 0
next(gen)    # 1

# Generator expression
squares = (n**2 for n in range(10))
total   = sum(n**2 for n in range(10))   # no list created

def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()
```

---

## Context Managers

```python
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {time.perf_counter()-start:.4f}s")

with timer("my_operation"):
    do_work()

# Class-based
class Managed:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        cleanup()
        return False    # don't suppress exceptions
```

---

## Dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float
    label: str = ""
    tags: list = field(default_factory=list)

@dataclass(frozen=True)  # immutable
class Config:
    host: str = "localhost"
    port: int = 5432

@dataclass(order=True)   # enables < > <= >=
class Version:
    major: int; minor: int; patch: int

from dataclasses import asdict
d = asdict(point)   # → dict
```

---

## Async/Await

```python
import asyncio

async def fetch(url): ...

# Run one coroutine
asyncio.run(fetch("url"))

# Run many concurrently
results = await asyncio.gather(
    fetch("url1"),
    fetch("url2"),
    fetch("url3"),
)

# Async context manager
async with aiohttp.ClientSession() as session:
    async with session.get(url) as r:
        data = await r.json()
```

---

## functools

```python
from functools import lru_cache, partial, reduce

# Memoization
@lru_cache(maxsize=128)
def fib(n):
    if n < 2: return n
    return fib(n-1) + fib(n-2)

# Partial application
from functools import partial
add = lambda x, y: x + y
add5 = partial(add, 5)
add5(3)    # 8

# Reduce
from functools import reduce
total = reduce(lambda a, x: a + x, [1,2,3,4])   # 10
```

---

## itertools

```python
import itertools

# Infinite
itertools.count(start=0, step=1)
itertools.cycle([1,2,3])
itertools.repeat(x, times=3)

# Finite
itertools.chain([1,2], [3,4])      # [1,2,3,4]
itertools.islice(gen, 5)           # first 5
itertools.groupby(data, key=fn)    # group by key
itertools.combinations([1,2,3],2)  # (1,2),(1,3),(2,3)
itertools.permutations([1,2,3],2)  # all ordered pairs
```
