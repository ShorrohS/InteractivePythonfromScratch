# Phase 17 — Advanced Exercises

> Difficulty: ⭐⭐⭐
> These are hard. Plan your approach on paper first.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Stacking Decorators**

Write three separate decorators: `@cache`, `@timer`, `@logger`.
- `cache`: stores results in a dict keyed on `args`; returns the cached value without calling the function again on a hit
- `timer`: prints how long the function took
- `logger`: prints function name, arguments, and return value

Apply all three to a function as `@logger @timer @cache def expensive_computation(n): ...`

a) Run the function twice with the same argument and describe the output difference.
b) In a comment, explain the execution order: which decorator's wrapper runs *first* when you call the function?

(Hint: decorators are applied bottom-up at definition time — `cache` wraps first, then `timer`, then `logger`; at *call* time, the outermost decorator's wrapper runs first)

---

**Q2. Async Producer-Consumer Pipeline**

Build an async producer-consumer system using `asyncio.Queue`:
- `producer(queue, n)`: puts `n` random integers (1–100) into the queue, sleeping 0.05s between items; sends `None` as a sentinel when done
- `consumer(queue)`: reads items until it receives `None`; prints each item and keeps a running total; calls `queue.task_done()` after each item
- `main()`: creates a `Queue(maxsize=5)`, runs both coroutines concurrently with `asyncio.gather`

(Hint: use `await queue.put(item)` and `item = await queue.get()` — these yield control to the event loop instead of blocking the thread)

---

**Q3. Thread-Safe Counter**

Write a `ThreadSafeCounter` class with `increment()`, `decrement()`, and a `value` property.
Use a `threading.Lock` inside every method that reads or modifies `_count`.

Launch 10 threads, each calling `increment()` 100 times, join them all, then assert `counter.value == 1000`.

Also write a `BrokenCounter` class (no lock) and add a comment explaining *why* the missing lock can produce incorrect results (describe what "read-modify-write" means in a multi-threaded context).

(Hint: `with self._lock:` is the preferred pattern; `count += 1` compiles to three operations — LOAD, ADD, STORE — another thread can interrupt between them)

---

**Q4. Enforcing Contracts with a Metaclass**

Write a metaclass `StrictMeta` that raises `TypeError` at **class creation time** if any public method (not starting with `_`) is missing either:
- A docstring
- Type hints for all parameters (excluding `self`) and the return type

Create a compliant class with two annotated, documented methods to confirm it passes.
Then add a method without a docstring and confirm `TypeError` is raised immediately.

(Hint: iterate `namespace.items()` in `__new__`; use `inspect.signature()` to get parameters and `typing.get_type_hints()` for annotations)

---

**Q5. ValidatedAttribute Descriptor**

Write a descriptor class `ValidatedAttribute` that:
- Takes `expected_type`, `min_val`, `max_val` at construction
- Implements `__set_name__`, `__get__`, `__set__`
- In `__set__`: raises `TypeError` if the value is the wrong type; raises `ValueError` if outside the allowed range

Use it in a `Person` class:
```python
class Person:
    age   = ValidatedAttribute(int,   min_val=0,   max_val=150)
    score = ValidatedAttribute(float, min_val=0.0, max_val=100.0)
```

Test with valid values, a wrong type, and an out-of-range value.

(Hint: store the actual value on the instance using `setattr(obj, self._private, value)` where `self._private` is something like `"_age"`; `__set_name__` is called automatically when the class is defined)

---

**Q6. Coroutine State Machine**

Use a generator with `send()` to build a traffic-light state machine cycling through `red → green → yellow → red`:
- The generator `yield`s the current state string on each step
- Sending `"tick"` advances to the next state
- Sending `"reset"` returns to `"red"`

Run 5 commands and print each resulting state.
Add a comment explaining **why** `next()` must be called once before any `send()`.

(Hint: the generator can't receive a sent value until it has reached a `yield` expression; `next(gen)` primes it by advancing to the first `yield`)

---

**Q7. Paginated Data Loader**

Write a class `PaginatedLoader` with `__iter__` and `__next__` that:
- Takes a `data` list and a `page_size` (default `3`)
- Each `__next__` call returns `{"page": N, "items": [...], "count": M}`
- Raises `StopIteration` when all data is exhausted

Test with 11 items and `page_size=3` — you should see 4 pages (sizes 3, 3, 3, 2).

(Hint: track `self._offset` and advance it by `page_size` on each call; `self._page_num` tracks the current page number)

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
