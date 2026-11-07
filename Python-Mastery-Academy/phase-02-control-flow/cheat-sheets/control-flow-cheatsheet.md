# ⚡ Phase 02 Cheat Sheet — Control Flow

---

## if / elif / else

```python
if condition:
    action
elif other_condition:
    other_action
else:
    default_action

# Ternary
value = "yes" if condition else "no"

# Chained comparison
if 0 <= score <= 100:   # Pythonic range check
```

---

## match / case (Python 3.10+)

```python
match variable:
    case "a":
        action_a
    case "b" | "c":     # OR: b or c
        action_bc
    case _:             # default (like else)
        default_action
```

---

## while Loop

```python
while condition:
    body
    # Must update something to avoid infinite loop

# Common patterns:
while True:
    ...
    if done: break

count = 0
while count < 10:
    ...
    count += 1
```

---

## for Loop

```python
for item in iterable:
    action

for i in range(5):        # 0, 1, 2, 3, 4
for i in range(1, 6):     # 1, 2, 3, 4, 5
for i in range(0, 10, 2): # 0, 2, 4, 6, 8
for i in range(10, 0, -1):# 10, 9, ..., 1

# With index
for i, item in enumerate(items):
for i, item in enumerate(items, start=1):

# Reversed
for item in reversed(items):
for i in range(n-1, -1, -1):
```

---

## Loop Control

```python
break       # Exit loop entirely
continue    # Skip to next iteration
pass        # Do nothing (placeholder)

# for/else and while/else
for item in items:
    if found: break
else:
    # Runs ONLY if loop completed without break
    print("Not found")
```

---

## Nested Loops

```python
for i in range(rows):
    for j in range(cols):
        print(f"({i},{j})", end=" ")
    print()   # newline after inner loop

# Pattern example
for i in range(1, 6):
    print("*" * i)
```

---

## Common Patterns

```python
# Input validation
while True:
    x = int(input("Enter 1-10: "))
    if 1 <= x <= 10: break
    print("Invalid.")

# Running total
total = 0
for n in numbers:
    total += n

# Find max without max()
best = items[0]
for item in items:
    if item > best:
        best = item

# Sum only certain items
evens_sum = sum(n for n in numbers if n % 2 == 0)
```

---

## Operator Quick Reference

| Operator | Meaning |
|----------|---------|
| `==` | Equal to |
| `!=` | Not equal to |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater or equal |
| `<=` | Less or equal |
| `and` | Both true |
| `or` | At least one true |
| `not` | Reverse |
| `in` | Member of |
| `is None` | None check |
