# Phase 17 — Advanced Exercise Solutions

---

## Q1. Stacking Decorators

```python
import time
import functools

# ── Three independent decorators ──────────────────────────────────────────────

def cache(func):
    """Cache results by args; skip the real function on a hit."""
    _store = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in _store:
            _store[args] = func(*args)    # cache miss — compute and store
        return _store[args]
    return wrapper

def timer(func):
    """Print how long the function took."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"[TIMER] {func.__name__} took {time.perf_counter() - start:.6f}s")
        return result
    return wrapper

def logger(func):
    """Print function name, args, and return value."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"[LOG] {func.__name__}({args}) called")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} returned {result}")
        return result
    return wrapper

# ── Stacked: cache wraps first, then timer, then logger ───────────────────────
# Execution order at CALL TIME (outermost first):
#   logger.wrapper → timer.wrapper → cache.wrapper → expensive_computation (or cache hit)
@logger
@timer
@cache
def expensive_computation(n: int) -> int:
    """Sum of squares up to n."""
    return sum(i ** 2 for i in range(n))

print("=== First call (cache miss) ===")
expensive_computation(1000)
# [LOG] expensive_computation((1000,)) called
# [TIMER] expensive_computation took 0.000123s  ← real work done
# [LOG] expensive_computation returned 332833500

print("\n=== Second call (cache hit) ===")
expensive_computation(1000)
# [LOG] expensive_computation((1000,)) called
# [TIMER] expensive_computation took 0.000002s  ← instant — cache served it
# [LOG] expensive_computation returned 332833500

# EXECUTION ORDER EXPLANATION:
# Decorators are applied bottom-up at *definition* time:
#   1. cache    wraps expensive_computation  → cache_wrapper
#   2. timer    wraps cache_wrapper          → timer_wrapper
#   3. logger   wraps timer_wrapper          → logger_wrapper
# At *call* time, the chain runs outer-first:
#   logger_wrapper → timer_wrapper → cache_wrapper → (func or cache hit)
```

---

## Q2. Async Producer-Consumer Pipeline

```python
import asyncio
import random

async def producer(queue: asyncio.Queue, n_items: int) -> None:
    """Generate random integers and place them on the queue."""
    for i in range(n_items):
        item = random.randint(1, 100)
        await queue.put(item)              # blocks if queue is full (maxsize)
        print(f"[Producer] produced {item}")
        await asyncio.sleep(0.05)          # yield control between items
    await queue.put(None)                  # sentinel — signals the consumer to stop

async def consumer(queue: asyncio.Queue) -> None:
    """Consume items until the sentinel None is received."""
    total = 0
    count = 0
    while True:
        item = await queue.get()           # wait for an item; yield to event loop
        if item is None:
            break
        total += item
        count += 1
        print(f"[Consumer] consumed {item}  (running total: {total})")
        queue.task_done()
        await asyncio.sleep(0.1)           # consumer is slower than producer
    print(f"[Consumer] done — {count} items, total = {total}")

async def main() -> None:
    queue = asyncio.Queue(maxsize=5)       # back-pressure: producer waits when full
    await asyncio.gather(
        producer(queue, 10),
        consumer(queue),
    )

asyncio.run(main())
```

---

## Q3. Thread-Safe Counter

```python
import threading
import time

# ── Safe version ──────────────────────────────────────────────────────────────

class ThreadSafeCounter:
    """Counter protected by a Lock — safe to use from multiple threads."""

    def __init__(self):
        self._count = 0
        self._lock  = threading.Lock()   # one thread at a time may hold this lock

    def increment(self):
        with self._lock:          # acquire lock, run block, release — even on exception
            self._count += 1

    def decrement(self):
        with self._lock:
            self._count -= 1

    @property
    def value(self) -> int:
        with self._lock:          # read also needs the lock to avoid torn reads
            return self._count

counter = ThreadSafeCounter()

def worker(n: int):
    for _ in range(n):
        counter.increment()

threads = [threading.Thread(target=worker, args=(100,)) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

assert counter.value == 1000, f"Expected 1000, got {counter.value}"
print(f"Final count: {counter.value}")   # Always 1000

# ── Broken version (for comparison) ───────────────────────────────────────────

class BrokenCounter:
    """Counter WITHOUT a lock — demonstrates a race condition."""

    def __init__(self):
        self.count = 0
        # BUG: no lock here

    def increment(self):
        # count += 1 is NOT atomic — it compiles to three bytecode steps:
        #   1. LOAD  self.count      (read current value)
        #   2. BINARY_ADD  1         (compute count + 1)
        #   3. STORE self.count      (write back result)
        # If Thread B reads self.count between Thread A's LOAD and STORE,
        # both threads read the same old value, both add 1, and both store
        # the same result — one increment is silently lost.
        self.count += 1

broken = BrokenCounter()
threads2 = [threading.Thread(target=lambda: [broken.increment() for _ in range(1000)])
            for _ in range(10)]
for t in threads2: t.start()
for t in threads2: t.join()
print(f"Broken counter: {broken.count} (expected 10000, may be less)")
```

---

## Q4. Enforcing Contracts with a Metaclass

```python
import inspect
from typing import get_type_hints

class StrictMeta(type):
    """Metaclass that enforces docstrings and full type hints on all public methods."""

    def __new__(mcs, name, bases, namespace):
        for attr_name, attr_value in namespace.items():
            if not callable(attr_value) or attr_name.startswith("_"):
                continue    # skip non-methods and private/dunder names

            # 1. Require a docstring
            if not attr_value.__doc__:
                raise TypeError(
                    f"Method '{attr_name}' in class '{name}' must have a docstring."
                )

            # 2. Require type hints on all parameters (except self) and return
            hints  = get_type_hints(attr_value)
            params = [
                p for p in inspect.signature(attr_value).parameters
                if p != "self"
            ]
            missing = [p for p in params if p not in hints]
            if missing or "return" not in hints:
                missing_all = missing + (["return"] if "return" not in hints else [])
                raise TypeError(
                    f"Method '{attr_name}' in class '{name}' missing hints for: "
                    f"{missing_all}"
                )

        return super().__new__(mcs, name, bases, namespace)

# ── Compliant class — passes ───────────────────────────────────────────────────
class MyService(metaclass=StrictMeta):
    def process(self, value: int) -> str:
        """Process an integer and return a formatted string."""
        return f"Processed: {value}"

    def validate(self, data: dict) -> bool:
        """Return True if data is non-empty."""
        return bool(data)

s = MyService()
print(s.process(42))           # Processed: 42
print(s.validate({"k": "v"}))  # True

# ── Non-compliant class — raises TypeError immediately ─────────────────────────
try:
    class BadService(metaclass=StrictMeta):
        def compute(self, x: int) -> int:
            # Missing docstring — TypeError raised here, at class definition time
            return x * 2
except TypeError as e:
    print(f"Caught at class creation: {e}")
```

---

## Q5. ValidatedAttribute Descriptor

```python
class ValidatedAttribute:
    """
    Descriptor that enforces type and range constraints on an attribute.
    Use as a class variable: age = ValidatedAttribute(int, min_val=0, max_val=150)
    """

    def __init__(self, expected_type: type, min_val=None, max_val=None):
        self.expected_type = expected_type
        self.min_val       = min_val
        self.max_val       = max_val
        self._private      = None     # set properly by __set_name__

    def __set_name__(self, owner, name: str):
        """Called automatically when the class body is processed."""
        self._private = f"_{name}"   # e.g. "age" → "_age" on the instance

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self              # accessed on the class itself
        return getattr(obj, self._private, None)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"Expected {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f"Value {value} is below minimum {self.min_val}")
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f"Value {value} exceeds maximum {self.max_val}")
        setattr(obj, self._private, value)    # store on the instance

class Person:
    age   = ValidatedAttribute(int,   min_val=0,   max_val=150)
    score = ValidatedAttribute(float, min_val=0.0, max_val=100.0)

    def __init__(self, age: int, score: float):
        self.age   = age      # calls ValidatedAttribute.__set__
        self.score = score

p = Person(25, 92.5)
print(f"Age: {p.age}, Score: {p.score}")   # Age: 25, Score: 92.5

try:
    p.age = -5
except ValueError as e:
    print(f"ValueError: {e}")    # ValueError: Value -5 is below minimum 0

try:
    p.score = "high"
except TypeError as e:
    print(f"TypeError: {e}")     # TypeError: Expected float, got str
```

---

## Q6. Coroutine State Machine

```python
def traffic_light():
    """
    Coroutine-based state machine for a traffic light.
    Yields the current state; accepts 'tick' or 'reset' via send().
    """
    states = ["red", "green", "yellow"]
    idx = 0
    while True:
        command = yield states[idx]     # pause here, return state, receive command
        if command == "reset":
            idx = 0
        elif command == "tick":
            idx = (idx + 1) % len(states)
        # Any other command: stay in the same state

# WHY next() is required before send():
# A freshly created generator sits BEFORE the first yield.
# send(value) requires the generator to already be suspended AT a yield so it
# can receive the sent value as the result of that expression.
# next(gen) advances it to the first yield without sending a value (same as send(None)).
light   = traffic_light()
current = next(light)          # PRIME the generator — advances to first yield
print(f"Initial: {current}")   # Initial: red

commands = ["tick", "tick", "tick", "reset", "tick"]
for cmd in commands:
    state = light.send(cmd)
    print(f"  send({cmd!r:6}) → {state}")
# send('tick')  → green
# send('tick')  → yellow
# send('tick')  → red
# send('reset') → red
# send('tick')  → green
```

---

## Q7. Paginated Data Loader

```python
class PaginatedLoader:
    """
    Iterator that returns data in fixed-size pages.
    Each page is a dict: {"page": N, "items": [...], "count": M}
    """

    def __init__(self, data: list, page_size: int = 3):
        self._data      = data
        self._page_size = page_size
        self._offset    = 0
        self._page_num  = 0

    def __iter__(self):
        return self          # the object is its own iterator

    def __next__(self) -> dict:
        if self._offset >= len(self._data):
            raise StopIteration   # signals the for-loop to stop

        page_items    = self._data[self._offset : self._offset + self._page_size]
        self._offset  += self._page_size
        self._page_num += 1
        return {
            "page":  self._page_num,
            "items": page_items,
            "count": len(page_items),
        }

data   = list(range(1, 12))          # 11 items: [1, 2, ..., 11]
loader = PaginatedLoader(data, page_size=3)

for page in loader:
    print(f"Page {page['page']}: {page['items']}  ({page['count']} items)")
# Page 1: [1, 2, 3]   (3 items)
# Page 2: [4, 5, 6]   (3 items)
# Page 3: [7, 8, 9]   (3 items)
# Page 4: [10, 11]    (2 items)
```

---

> **Exercises:** → [../../exercises/advanced/exercises.md](../../exercises/advanced/exercises.md)
