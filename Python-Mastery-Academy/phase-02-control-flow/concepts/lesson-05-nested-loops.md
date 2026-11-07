# Lesson 05 — Nested Loops

**Phase:** 02 — Control Flow | **Time:** ~30 min

---

## Part 1: What are Nested Loops?

A nested loop is a loop inside another loop. The inner loop runs completely for every single iteration of the outer loop.

**Analogy:** A car factory assembling seats. For each car (outer), they install each seat (inner). 3 cars × 4 seats = 12 installations total.

```
for each car (outer loop runs 3 times):
    for each seat (inner loop runs 4 times):
        install seat
        
Total iterations: 3 × 4 = 12
```

---

## Part 2: Basic Nested Loop

```python
for i in range(1, 4):          # outer: 3 iterations
    for j in range(1, 4):      # inner: 3 iterations each time
        print(f"({i},{j})", end=" ")
    print()    # newline after each outer iteration

# Output:
# (1,1) (1,2) (1,3)
# (2,1) (2,2) (2,3)
# (3,1) (3,2) (3,3)
```

---

## Part 3: Pattern Printing

```python
# Right triangle
rows = 5
for i in range(1, rows + 1):
    print("*" * i)

# Square
for i in range(rows):
    for j in range(rows):
        print("*", end=" ")
    print()

# Number pyramid
for i in range(1, rows + 1):
    for j in range(1, i + 1):
        print(j, end=" ")
    print()

# Hollow square
for i in range(rows):
    for j in range(rows):
        if i == 0 or i == rows-1 or j == 0 or j == rows-1:
            print("*", end=" ")
        else:
            print(" ", end=" ")
    print()
```

---

## Part 4: Multiplication Table

```python
print("    ", end="")
for j in range(1, 11):
    print(f"{j:4}", end="")
print()
print("    " + "-" * 40)

for i in range(1, 11):
    print(f"{i:3} |", end="")
    for j in range(1, 11):
        print(f"{i*j:4}", end="")
    print()
```

---

## Part 5: Seating Chart — Business Example

```python
"""Theatre seating chart generator."""

rows = ["A", "B", "C", "D", "E"]
seats_per_row = 8
booked = [("B", 3), ("B", 4), ("D", 1), ("D", 2), ("D", 3)]

print("\nTHEATRE SEATING CHART")
print("    " + " ".join(f"{s:2}" for s in range(1, seats_per_row + 1)))
print("    " + "---" * seats_per_row)

for row in rows:
    print(f" {row}  ", end="")
    for seat in range(1, seats_per_row + 1):
        if (row, seat) in booked:
            print(" X ", end="")    # X = booked
        else:
            print(" O ", end="")    # O = available
    print()

available = (len(rows) * seats_per_row) - len(booked)
print(f"\n  Total: {len(rows) * seats_per_row} | Booked: {len(booked)} | Available: {available}")
```

---

## Part 6: break and continue in Nested Loops

```python
# break only exits the INNER loop
for i in range(3):
    for j in range(5):
        if j == 3:
            break          # exits inner loop only
        print(f"({i},{j})", end=" ")
    print()

# To break both loops, use a flag
found = False
for i in range(5):
    for j in range(5):
        if i * j == 12:
            print(f"Found: {i} x {j} = 12")
            found = True
            break
    if found:
        break
```

---

## Practice Exercises

1. Print a right-aligned triangle:
```
    *
   **
  ***
 ****
*****
```

2. Build a times table for a number the user enters (1 through 12).

3. Write a nested loop that finds all pairs (i, j) where `i + j == 10`, with `i` and `j` both between 1 and 9.

4. Print a chess board pattern (8x8) using `#` and space characters.

---

## Next Lesson

**[Lesson 06 → Break, Continue, Pass](lesson-06-break-continue.md)**
