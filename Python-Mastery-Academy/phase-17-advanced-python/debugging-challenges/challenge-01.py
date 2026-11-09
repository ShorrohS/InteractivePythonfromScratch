"""
Debugging Challenge 01 — Phase 17: Advanced Python
===================================================

INSTRUCTIONS:
  This file contains 7 bugs — all realistic Python pitfalls, not trivial typos.
  Some bugs cause crashes; others produce silently wrong output or behaviour.
  Read the comment above each section to understand what it SHOULD do.
  Fix all 7 bugs, then run the file — the final line will print correctly.

HINTS:
  Bug 1: Look carefully at the default argument value in the decorator factory signature
  Bug 2: What happens when you try to iterate a generator a second time?
  Bug 3: What metadata does a wrapper function lose when @functools.wraps is absent?
  Bug 4: What must happen before you can send() a value into a generator?
  Bug 5: What must __exit__ return to suppress an exception inside a with-block?
  Bug 6: What is missing when you call a coroutine function inside async code?
  Bug 7: What prevents two threads from interleaving on a shared variable?

DO NOT LOOK AT THE ANSWERS BELOW UNTIL YOU'VE TRIED!
"""

import time
import functools
import threading
import asyncio

print("=== Phase 17 Debugging Challenge ===\n")

# ─────────────────────────────────────────────────────────────────────────────
# Bug 1: Mutable default argument in decorator factory
#
# SHOULD: each call to log_calls() gets its own independent history list,
#         so task_a and task_b each track only their own calls.
# ─────────────────────────────────────────────────────────────────────────────

def log_calls(history=[]):  # Bug 1: [] is created ONCE at definition time and
                             # shared across every call to log_calls()
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            history.append(func.__name__)
            return func(*args, **kwargs)
        wrapper.history = history
        return wrapper
    return decorator

@log_calls()
def task_a():
    pass

@log_calls()
def task_b():
    pass

task_a()
task_b()
task_a()

# Expected: task_a.history == ['task_a', 'task_a']
#           task_b.history == ['task_b']
# Buggy:    both wrappers share the SAME list, so both show all 3 calls
print(f"Bug 1 — task_a history: {task_a.history}")
print(f"Bug 1 — task_b history: {task_b.history}")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Bug 2: Generator exhaustion
#
# SHOULD: print the same list of numbers on both passes.
# ─────────────────────────────────────────────────────────────────────────────

def count_up(n: int):
    for i in range(1, n + 1):
        yield i

numbers     = count_up(5)
first_pass  = list(numbers)   # [1, 2, 3, 4, 5] — generator consumed here
second_pass = list(numbers)   # Bug 2: generator is already exhausted → returns []
                               # FIX: call count_up(5) again to get a fresh generator

print(f"Bug 2 — first pass:  {first_pass}")
print(f"Bug 2 — second pass: {second_pass}   (should be [1, 2, 3, 4, 5])")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Bug 3: Missing @functools.wraps
#
# SHOULD: preserve the wrapped function's __name__ and __doc__.
# ─────────────────────────────────────────────────────────────────────────────

def my_timer(func):
    def wrapper(*args, **kwargs):  # Bug 3: missing @functools.wraps(func)
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"  [timer] {time.perf_counter() - start:.6f}s")
        return result
    return wrapper

@my_timer
def compute_sum(n: int) -> int:
    """Return the sum of integers from 1 to n."""
    return sum(range(n + 1))

compute_sum(1000)
print(f"Bug 3 — __name__: {compute_sum.__name__!r}")   # Should be 'compute_sum', not 'wrapper'
print(f"Bug 3 — __doc__:  {compute_sum.__doc__!r}")    # Should be the docstring, not None
print()


# ─────────────────────────────────────────────────────────────────────────────
# Bug 4: Forgetting to prime the generator before send()
#
# SHOULD: accept sent values and accumulate a running total.
# ─────────────────────────────────────────────────────────────────────────────

def running_total():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

acc = running_total()
# Bug 4: must call next(acc) here to advance the generator to the first yield
#        before sending any non-None value — otherwise: TypeError
try:
    result = acc.send(10)   # TypeError: can't send non-None to a just-started generator
    result = acc.send(20)
    result = acc.send(30)
    print(f"Bug 4 — running total after 10+20+30: {result}")   # Should be 60
except TypeError as e:
    print(f"Bug 4 — TypeError (bug still present): {e}")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Bug 5: __exit__ not returning True to suppress exceptions
#
# SHOULD: silently catch ValueError and allow execution to continue normally.
# ─────────────────────────────────────────────────────────────────────────────

class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is ValueError:
            print(f"  [context manager] caught ValueError: {exc_val}")
            # Bug 5: missing `return True`
            # Without it, Python treats __exit__ as returning None (falsy),
            # so the exception propagates even though we "handled" it.

try:
    with SuppressValueError():
        raise ValueError("intentional test error")
    print("Bug 5 — exception was suppressed ✓")
except ValueError:
    print("Bug 5 — exception was NOT suppressed (bug still present)")
print()


# ─────────────────────────────────────────────────────────────────────────────
# Bug 6: Calling an async function without await
#
# SHOULD: print the actual string returned by get_message().
# ─────────────────────────────────────────────────────────────────────────────

async def get_message(name: str) -> str:
    await asyncio.sleep(0)
    return f"Hello, {name}!"

async def run_async():
    result = get_message("World")   # Bug 6: missing await
                                    # result is a coroutine object, not a string
    print(f"Bug 6 — type:  {type(result).__name__}")   # Should be 'str', not 'coroutine'
    print(f"Bug 6 — value: {result}")                  # Should be 'Hello, World!'
    # Without await the coroutine body never runs; Python may also warn:
    # RuntimeWarning: coroutine 'get_message' was never awaited
    if hasattr(result, "close"):
        result.close()   # suppress the RuntimeWarning for clean output

asyncio.run(run_async())
print()


# ─────────────────────────────────────────────────────────────────────────────
# Bug 7: Missing threading.Lock — race condition on shared counter
#
# SHOULD: final count == 10 000 every single run.
# ─────────────────────────────────────────────────────────────────────────────

class UnsafeCounter:
    def __init__(self):
        self.count = 0
        # Bug 7: no threading.Lock
        # count += 1 is NOT atomic — it compiles to three bytecode instructions:
        #   1. LOAD  self.count        (read current value into a register)
        #   2. BINARY_ADD 1            (add 1)
        #   3. STORE self.count        (write result back)
        # Thread B can execute its LOAD between Thread A's LOAD and STORE,
        # both reading the same stale value and both storing the same result —
        # one increment is silently lost each time this happens.

    def increment(self):
        self.count += 1   # not thread-safe

counter = UnsafeCounter()

def worker():
    for _ in range(1000):
        counter.increment()

threads = [threading.Thread(target=worker) for _ in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Bug 7 — final count: {counter.count}  (should be 10000; may be less due to race)")

print("\n=== All 7 bugs found and fixed? Check the answers below. ===")


# ====================================================================
# ANSWERS — do not scroll until you have tried all 7 bugs!
# ====================================================================
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Bug 1 — Mutable default argument
#   WRONG: def log_calls(history=[]):
#   FIX:   def log_calls(history=None):
#              if history is None:
#                  history = []
#   WHY: default argument values are evaluated ONCE when the function is
#        defined, not on each call. All calls share the same list object.
#
# Bug 2 — Generator exhaustion
#   WRONG: second_pass = list(numbers)     # numbers already spent
#   FIX:   second_pass = list(count_up(5)) # create a fresh generator
#   WHY: a generator can only be iterated once. After StopIteration is raised,
#        it stays exhausted. Always create a new generator for a second pass.
#
# Bug 3 — Missing @functools.wraps
#   WRONG: def wrapper(*args, **kwargs):
#   FIX:   @functools.wraps(func)
#          def wrapper(*args, **kwargs):
#   WHY: without @wraps, wrapper.__name__ is 'wrapper' and wrapper.__doc__
#        is None. @wraps copies the original function's metadata onto wrapper.
#
# Bug 4 — Generator not primed before send()
#   WRONG: result = acc.send(10)   # first call
#   FIX:   next(acc)               # prime — advance to first yield
#          result = acc.send(10)   # now safe to send
#   WHY: a new generator is suspended before the first line. send(value) needs
#        the generator to already be paused AT a yield to receive the value.
#        next() (or send(None)) advances it to the first yield without a value.
#
# Bug 5 — __exit__ not suppressing the exception
#   WRONG: (no return statement in the if block)
#   FIX:   return True
#   WHY: __exit__ must explicitly return a truthy value to suppress an
#        exception. If it returns None (implicit) or False, the exception
#        propagates even if __exit__ handled it internally.
#
# Bug 6 — Async function called without await
#   WRONG: result = get_message("World")
#   FIX:   result = await get_message("World")
#   WHY: calling an async function without await returns a coroutine object.
#        The function body does NOT run until the coroutine is awaited.
#        Python 3.10+ also emits a RuntimeWarning.
#
# Bug 7 — Missing threading.Lock
#   WRONG: self.count += 1   (no lock)
#   FIX:   add self._lock = threading.Lock() in __init__
#          def increment(self):
#              with self._lock:
#                  self.count += 1
#   WHY: count += 1 is a read-modify-write sequence. Without a lock, two
#        threads can read the same value before either writes back, causing
#        one increment to be silently dropped (a classic race condition).
#
# ====================================================================
