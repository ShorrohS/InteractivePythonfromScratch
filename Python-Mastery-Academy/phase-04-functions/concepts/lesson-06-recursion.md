# Lesson 06 — Recursion

**Phase:** 04 — Functions | **Time:** ~30 min

---

## Part 1: What is Recursion?

Recursion is when a function calls itself.

**Analogy:** Russian nesting dolls (Matryoshka). Open one → find another inside → open that → find another... until you reach the smallest one (base case).

Every recursive function MUST have:
1. A **base case** — condition to stop (otherwise: infinite recursion)
2. A **recursive case** — calls itself with a smaller/simpler version of the problem

---

## Part 2: Your First Recursive Function

```python
def countdown(n: int) -> None:
    """Count down from n to 0."""
    if n <= 0:          # BASE CASE — stop here
        print("Done!")
        return
    print(n)
    countdown(n - 1)    # RECURSIVE CASE — smaller problem

countdown(5)
# 5
# 4
# 3
# 2
# 1
# Done!
```

Call stack visualised:
```
countdown(5)
  countdown(4)
    countdown(3)
      countdown(2)
        countdown(1)
          countdown(0)  ← BASE CASE
```

---

## Part 3: Factorial

```python
def factorial(n: int) -> int:
    """
    n! = n × (n-1) × (n-2) × ... × 1
    5! = 5 × 4 × 3 × 2 × 1 = 120
    """
    if n <= 1:          # base case: 0! = 1, 1! = 1
        return 1
    return n * factorial(n - 1)   # recursive case

for i in range(8):
    print(f"{i}! = {factorial(i)}")
```

---

## Part 4: Fibonacci

```python
def fibonacci(n: int) -> int:
    """Return nth Fibonacci number. (0,1,1,2,3,5,8,13,...)"""
    if n <= 1:              # base cases
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)   # recursive

# Print first 10
for i in range(10):
    print(fibonacci(i), end=" ")
```

Note: naive Fibonacci is exponentially slow. Use memoisation for real use:

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fibonacci_fast(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_fast(n-1) + fibonacci_fast(n-2)
```

---

## Part 5: Recursion vs Iteration

```python
# Same problem — two approaches

# ITERATIVE (usually faster, no stack risk)
def sum_iter(n: int) -> int:
    total = 0
    for i in range(1, n + 1):
        total += i
    return total

# RECURSIVE (elegant for tree/nested structures)
def sum_rec(n: int) -> int:
    if n <= 0:
        return 0
    return n + sum_rec(n - 1)

print(sum_iter(100))  # 5050
print(sum_rec(100))   # 5050
```

**When to use recursion:**
- Tree traversal (file systems, org charts, JSON)
- Divide-and-conquer algorithms
- When the problem is naturally recursive
- Backtracking problems

**When NOT to:**
- Simple loops (iteration is faster, clearer)
- Very deep recursion (Python default limit: 1000)

---

## Part 6: Practical — Nested Structure Traversal

```python
def flatten(nested: list) -> list:
    """Flatten a list of any depth."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))   # recursive
        else:
            result.append(item)
    return result

data = [1, [2, 3], [4, [5, 6]], 7, [[8, 9], 10]]
print(flatten(data))   # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def calculate_nested_total(data) -> float:
    """Sum all numbers in arbitrarily nested structure."""
    if isinstance(data, (int, float)):
        return data
    if isinstance(data, list):
        return sum(calculate_nested_total(item) for item in data)
    return 0

totals = [100, [200, 300], [400, [50, 50]]]
print(calculate_nested_total(totals))   # 1100
```

---

## Practice Exercises

1. Write a recursive function `power(base, exp)` without using `**`.

2. Write a recursive function `reverse_string(s)` that reverses a string.

3. Write a recursive function `count_down_to_zero(n)` that prints all numbers from n to 0.

4. What happens if a recursive function has no base case?

---

## Next Lesson

**[Lesson 07 → Lambda Functions](lesson-07-lambda.md)**
