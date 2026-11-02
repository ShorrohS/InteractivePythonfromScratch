# Lesson 02 — Generators

**Phase:** 17 — Advanced Python | **Time:** ~30 min

---

## Part 1: What is a Generator?

A generator is a function that **yields values one at a time** instead of returning them all at once.

**Why it matters:** Memory efficiency. Instead of loading 1 million items into a list, you process one at a time.

```
Regular function: returns ALL results at once (list in memory)
Generator:        returns ONE result at a time, on demand
```

---

## Part 2: yield vs return

```python
# Regular function — creates entire list in memory
def get_squares(n: int) -> list[int]:
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result    # Returns all at once

squares = get_squares(1_000_000)   # 8 MB in memory!

# Generator — one value at a time
def gen_squares(n: int):
    for i in range(n):
        yield i ** 2    # Pauses here, resumes on next call

squares = gen_squares(1_000_000)   # Almost no memory!
```

---

## Part 3: Using Generators

```python
# next() — get one value
gen = gen_squares(5)
print(next(gen))   # 0
print(next(gen))   # 1
print(next(gen))   # 4

# for loop — iterate all
for square in gen_squares(5):
    print(square)   # 0, 1, 4, 9, 16

# List conversion
squares_list = list(gen_squares(10))

# Sum (never builds list)
total = sum(gen_squares(1000))
```

---

## Part 4: Infinite Generators

```python
def counter(start: int = 0, step: int = 1):
    """Infinite counter — generates numbers forever."""
    current = start
    while True:
        yield current
        current += step

# Use with limits
gen = counter(1)
first_10 = [next(gen) for _ in range(10)]    # [1, 2, ..., 10]

def fibonacci():
    """Infinite Fibonacci sequence."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
first_20 = [next(fib) for _ in range(20)]
```

---

## Part 5: Generator Expressions

Like list comprehensions but lazy:

```python
# List comprehension — all in memory
squares_list = [i**2 for i in range(1_000_000)]

# Generator expression — lazy
squares_gen = (i**2 for i in range(1_000_000))

# Use generator expression directly in functions
total = sum(i**2 for i in range(1000))
filtered = list(x for x in range(100) if x % 7 == 0)
```

---

## Part 6: Real-World Use Cases

```python
def read_large_file(filename: str):
    """Process a huge log file line by line without loading it all."""
    with open(filename) as f:
        for line in f:
            yield line.strip()

# Only one line in memory at a time — can handle 10GB files!
for line in read_large_file("massive_log.txt"):
    if "ERROR" in line:
        print(line)


def batch_query(query: str, batch_size: int = 100):
    """Process database results in batches."""
    offset = 0
    while True:
        results = db.execute(f"{query} LIMIT {batch_size} OFFSET {offset}").fetchall()
        if not results:
            break
        yield from results    # yield from = yield each item
        offset += batch_size


def pipeline(*generators):
    """Chain generators for data pipeline."""
    data = generators[0]
    for gen in generators[1:]:
        data = gen(data)
    return data
```

---

## Part 7: Memory Comparison

```python
import sys

# List: stores everything
big_list = list(range(1_000_000))
print(f"List size: {sys.getsizeof(big_list):,} bytes")    # ~8 MB

# Generator: stores almost nothing
big_gen = (x for x in range(1_000_000))
print(f"Generator size: {sys.getsizeof(big_gen)} bytes")  # ~104 bytes
```

---

## Practice Exercises

1. Write a generator `even_numbers(start, end)` that yields all even numbers in a range.

2. Write a generator that yields lines from a file, one at a time.

3. Write a `countdown(n)` generator that counts from n down to 0.

4. Write a generator that yields the running average of a sequence of numbers.

---

## Next Lesson

**[Lesson 03 → Context Managers](lesson-03-context-managers.md)**
