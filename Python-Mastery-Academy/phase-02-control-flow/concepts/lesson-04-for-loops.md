# Lesson 04 — For Loops

**Phase:** 02 — Control Flow | **Time:** ~30 min

---

## Part 1: Concept

A `for` loop iterates over a sequence — list, string, range, or any iterable.

**Analogy:** "FOR each student IN the classroom, take attendance."

---

## Part 2: For Loop with range()

```python
# range(stop) — 0 to stop-1
for i in range(5):
    print(i)          # 0, 1, 2, 3, 4

# range(start, stop)
for i in range(1, 6):
    print(i)          # 1, 2, 3, 4, 5

# range(start, stop, step)
for i in range(0, 11, 2):
    print(i)          # 0, 2, 4, 6, 8, 10

# Countdown
for i in range(10, 0, -1):
    print(i)          # 10, 9, 8, ..., 1
```

---

## Part 3: For Loop over Sequences

```python
# Over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Over a string
for char in "Python":
    print(char)        # P, y, t, h, o, n

# With index — enumerate()
for i, fruit in enumerate(fruits):
    print(f"{i+1}. {fruit}")     # 1. apple, 2. banana, etc.

# With index starting at 1
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
```

---

## Part 4: For Loop Patterns

```python
# Sum all numbers
total = 0
for i in range(1, 101):
    total += i
print(f"Sum 1-100: {total}")   # 5050

# Find maximum
numbers = [23, 45, 12, 67, 34]
maximum = numbers[0]
for n in numbers:
    if n > maximum:
        maximum = n
print(f"Max: {maximum}")   # 67  (better: use max())

# Multiplication table
n = 7
print(f"Multiplication table for {n}:")
for i in range(1, 13):
    print(f"  {n} × {i:2d} = {n*i:3d}")

# Build a string
words = ["Python", "is", "awesome"]
sentence = " ".join(words)
print(sentence)
```

---

## Part 5: Nested For Loops

```python
# Pattern printing
for i in range(1, 6):
    print("*" * i)

# Output:
# *
# **
# ***
# ****
# *****

# Multiplication grid
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i*j:3d}", end="")
    print()   # newline after each row

# Seating chart
rows = ["A", "B", "C"]
seats_per_row = 4
for row in rows:
    for seat in range(1, seats_per_row + 1):
        print(f"{row}{seat}", end=" ")
    print()
```

---

## Part 6: Business Example — Payroll Processor

```python
employees = [
    ("Alice", 80000),
    ("Bob", 65000),
    ("Carol", 95000),
    ("Dave", 72000),
]

print(f"{'Name':<15} {'Annual':>10} {'Monthly':>10} {'Tax (20%)':>12} {'Net':>12}")
print("-" * 60)

total_payroll = 0

for name, annual in employees:
    monthly = annual / 12
    tax = annual * 0.20
    net = annual - tax
    total_payroll += annual
    print(f"{name:<15} ${annual:>9,} ${monthly:>9,.0f} ${tax:>11,} ${net:>11,}")

print("-" * 60)
print(f"{'TOTAL PAYROLL':<15} ${total_payroll:>9,}")
```

---

## Part 7: Break and Continue

```python
# break — exit loop immediately
for i in range(10):
    if i == 5:
        break
    print(i)   # 0, 1, 2, 3, 4

# continue — skip current iteration
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)   # 1, 3, 5, 7, 9

# for/else
for i in range(5):
    if i == 10:
        print("Found!")
        break
else:
    print("Not found!")   # Runs because loop completed without break
```

---

## Practice Exercises

1. Print a multiplication table for numbers 1–12 × 1–12.

2. Write a program that asks for 5 exam scores and calculates the average.

3. Find all numbers between 1 and 100 divisible by both 3 and 7.

4. Print a right triangle pattern of `*` with height `n` (ask user for n).

5. Given a list of salaries, find the highest, lowest, and average.

---

## Next Lesson

**[Lesson 05 → Nested Loops & Patterns](lesson-05-nested-loops.md)**
