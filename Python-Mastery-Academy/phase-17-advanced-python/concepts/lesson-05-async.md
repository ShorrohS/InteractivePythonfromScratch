# Lesson 05 — Async/Await

**Phase:** 17 — Advanced Python | **Time:** ~35 min

---

## Part 1: Why Async?

Traditional code: waiting blocks everything.

```
Sync (sequential):
  Request 1 → wait 1s → Response 1
  Request 2 → wait 1s → Response 2
  Request 3 → wait 1s → Response 3
  Total time: 3 seconds

Async (concurrent):
  Request 1 ─────────────────► Response 1
  Request 2 ─────────────────► Response 2  (all started at once)
  Request 3 ─────────────────► Response 3
  Total time: ~1 second
```

Async is ideal for I/O-bound work: HTTP requests, database queries, file reads.

---

## Part 2: async/await Syntax

```python
import asyncio

async def greet(name: str) -> str:
    """An async function (coroutine)."""
    await asyncio.sleep(1)   # simulate I/O wait
    return f"Hello, {name}!"

async def main():
    result = await greet("Alice")
    print(result)

asyncio.run(main())   # run the event loop
```

Rules:
- `async def` creates a coroutine function
- `await` pauses the current coroutine (lets others run)
- You can only `await` inside an `async def`
- `asyncio.run()` starts the event loop (call once, in main)

---

## Part 3: Concurrent Execution with gather()

```python
import asyncio
import time

async def fetch_data(url: str, delay: float) -> str:
    """Simulate fetching data from a URL."""
    print(f"  Fetching {url}...")
    await asyncio.sleep(delay)   # simulate network latency
    return f"Data from {url}"

async def main():
    urls = [
        ("api.example.com/users",    1.0),
        ("api.example.com/products", 0.5),
        ("api.example.com/orders",   0.8),
    ]

    start = time.perf_counter()

    # Run all concurrently (not sequentially!)
    results = await asyncio.gather(
        *[fetch_data(url, delay) for url, delay in urls]
    )

    elapsed = time.perf_counter() - start
    print(f"\n  Results: {results}")
    print(f"  Total time: {elapsed:.2f}s")  # ~1s, not 2.3s

asyncio.run(main())
```

---

## Part 4: Real Async HTTP with aiohttp

```bash
pip install aiohttp
```

```python
import asyncio
import aiohttp

async def fetch_json(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch JSON from a URL asynchronously."""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()

async def fetch_multiple_apis() -> list[dict]:
    """Fetch from multiple APIs concurrently."""
    urls = [
        "https://jsonplaceholder.typicode.com/users/1",
        "https://jsonplaceholder.typicode.com/posts/1",
        "https://jsonplaceholder.typicode.com/todos/1",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if not isinstance(r, Exception)]

async def main():
    data = await fetch_multiple_apis()
    for item in data:
        print(item)

asyncio.run(main())
```

---

## Part 5: Async vs Threading vs Multiprocessing

```
USE ASYNC when:
  - Many I/O operations (HTTP, DB, files)
  - High concurrency needed
  - Examples: web servers, API clients, scrapers

USE THREADING when:
  - Some I/O + existing sync libraries
  - Limited concurrency (< 100 threads)
  - Examples: GUI + background tasks

USE MULTIPROCESSING when:
  - CPU-intensive work (math, ML, parsing)
  - Need true parallelism (GIL bypass)
  - Examples: data processing, image editing
```

---

## Practice Exercises

1. Write an async function that simulates 5 API calls taking different times. Run them concurrently and measure total time.

2. What happens if you `await` a regular (non-async) function?

3. Write an async file reader that reads 3 files concurrently.

---

## Next Lesson

**[Lesson 06 → Threading](lesson-06-threading.md)**
