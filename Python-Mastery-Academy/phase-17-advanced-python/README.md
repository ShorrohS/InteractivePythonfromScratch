# ⚡ Phase 17 — Advanced Python

> **Goal:** Master Python's most powerful features used in professional codebases.

---

## Overview

This phase covers the advanced features that separate junior from senior Python developers. Every concept here is used daily in production code.

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-decorators.md](concepts/lesson-01-decorators.md) | Decorators |
| 02 | [lesson-02-generators.md](concepts/lesson-02-generators.md) | Generators and yield |
| 03 | [lesson-03-iterators.md](concepts/lesson-03-iterators.md) | Custom iterators |
| 04 | [lesson-04-context-managers.md](concepts/lesson-04-context-managers.md) | Context managers |
| 05 | [lesson-05-dataclasses.md](concepts/lesson-05-dataclasses.md) | Dataclasses |
| 06 | [lesson-06-async.md](concepts/lesson-06-async.md) | Async/await |
| 07 | [lesson-07-threading.md](concepts/lesson-07-threading.md) | Threading |
| 08 | [lesson-08-multiprocessing.md](concepts/lesson-08-multiprocessing.md) | Multiprocessing |

---

## Quick Reference

```python
# DECORATOR
from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

# GENERATOR
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

gen = fibonacci()
print([next(gen) for _ in range(10)])

# DATACLASS
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    tags: list[str] = field(default_factory=list)
    
    def total_value(self) -> float:
        return self.price * self.quantity

p = Product("Laptop", 999.99, 5)
print(p)   # Product(name='Laptop', price=999.99, quantity=5, tags=[])

# ASYNC
import asyncio
import aiohttp

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def main():
    urls = [
        "https://api.example.com/data/1",
        "https://api.example.com/data/2",
        "https://api.example.com/data/3",
    ]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# CONTEXT MANAGER
from contextlib import contextmanager

@contextmanager
def timer_context(operation_name: str):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{operation_name}: {elapsed:.4f}s")

with timer_context("data processing"):
    # process data here
    time.sleep(0.5)
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Async Downloader](guided-projects/project-01-async-downloader/) | Concurrent file downloads |

---

## ✅ Completion Checklist

- [ ] Can write decorators (logging, timing, retry)
- [ ] Can write generators for memory-efficient iteration
- [ ] Can create context managers with @contextmanager
- [ ] Understand dataclasses and when to use them
- [ ] Can write basic async/await code
- [ ] Understand threading vs multiprocessing vs async

---

## Previous: [Phase 16](../phase-16-web-development/README.md) | Next: [Phase 18](../phase-18-business-projects/)
