# Phase 04 — Completion Assessment

> Pass mark: 80% | Time: 30 minutes

---

## PART A: Write the Code

**Task 1.** Write a complete function `process_employee(name, hourly_rate, hours, tax_rate=0.20)` that:
- Calculates gross pay (with 1.5x overtime after 40 hours)
- Calculates tax
- Returns a dict with name, gross, tax, net
- Has proper type hints and docstring

---

**Task 2.** Write two functions:
- `make_discount_calculator(percentage)` — returns a function
- The returned function takes a price and returns discounted price

Test: `summer_sale = make_discount_calculator(30)` then `summer_sale(100)` should return 70.

---

**Task 3.** Write a recursive function `flatten(nested_list)` that flattens any depth of nested lists into a single flat list.

Test with: `[[1, 2], [3, [4, 5]], 6]` → `[1, 2, 3, 4, 5, 6]`

---

## PART B: Predict the Output

**Q4.**
```python
def f(*args, **kwargs):
    print(len(args), len(kwargs))
f(1, 2, 3, x=4, y=5)
```

**Q5.**
```python
x = 10
def outer():
    x = 20
    def inner():
        return x
    return inner()
print(outer())
print(x)
```

**Q6.**
```python
result = sorted(
    [{"n":"C","v":3},{"n":"A","v":1},{"n":"B","v":2}],
    key=lambda d: d["v"],
    reverse=True
)
print([d["n"] for d in result])
```

---

## PART C: Find the Bugs

**Q7.**
```python
def add_tag(tags=[], tag):
    tags.append(tag)
    return tags
```

**Q8.**
```python
total_sales = 0
def record_sale(amount):
    total_sales = total_sales + amount
```

---

## PART D: Short Answer

**Q9.** What is the difference between `map()` and a list comprehension? When would you prefer each?

**Q10.** Why is it important for functions to be "pure" (no side effects)?

---

## Answers

**Q4:** `3 2`

**Q5:** `20` then `10` — inner sees enclosing x=20; module x=10 unchanged

**Q6:** `['C', 'B', 'A']`

**Q7 bugs:**
1. Default parameter `tags=[]` before non-default `tag` → SyntaxError
2. Mutable default trap → use `tags=None`

Fix:
```python
def add_tag(tag, tags=None):
    if tags is None: tags = []
    tags.append(tag)
    return tags
```

**Q8 bug:** `total_sales += amount` inside the function creates a local variable. Python sees the assignment and treats it as local, then raises `UnboundLocalError` when trying to read it before assignment.

Fix: `global total_sales` OR redesign to pass/return the total.

**Q9:** `map()` is lazy (doesn't compute until iterated), slightly faster in some cases, and can be composed. List comprehension is more readable, Pythonic, and better for complex transformations with conditions. Prefer comprehensions for clarity; use map when chaining lazy iterators.

**Q10:** Pure functions are predictable, testable, and safe to parallelize. Side effects (modifying globals, I/O) make functions harder to test, debug, and reason about. Code with pure functions is significantly easier to maintain.
