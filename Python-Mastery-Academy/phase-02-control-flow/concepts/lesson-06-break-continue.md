# Lesson 06 — break, continue, pass

**Phase:** 02 — Control Flow | **Time:** ~20 min

---

## Part 1: Three Loop Control Keywords

| Keyword | What it does |
|---------|-------------|
| `break` | Exit the loop immediately |
| `continue` | Skip current iteration, go to next |
| `pass` | Do nothing (placeholder) |

---

## Part 2: break — Exit the Loop

```python
# Find first even number
numbers = [1, 3, 7, 4, 9, 2, 6]

for n in numbers:
    if n % 2 == 0:
        print(f"First even number: {n}")
        break    # Stop searching — we found it

# Without break it would keep going after finding 4

# While loop with break (common input validation pattern)
while True:
    age = int(input("Enter age (1-120): "))
    if 1 <= age <= 120:
        break    # Valid input — exit the loop
    print("Invalid. Try again.")

print(f"Age accepted: {age}")
```

---

## Part 3: continue — Skip an Iteration

```python
# Print only odd numbers
for i in range(1, 11):
    if i % 2 == 0:
        continue    # skip even numbers
    print(i)        # only reaches here for odd numbers

# Skip empty strings in a list
names = ["Alice", "", "Bob", "  ", "Carol"]
for name in names:
    if not name.strip():
        continue    # skip blank entries
    print(f"Hello, {name.strip()}!")
```

---

## Part 4: pass — Placeholder

```python
# Placeholder — code not written yet
for i in range(10):
    if i < 5:
        pass       # TODO: handle small numbers
    else:
        print(f"Large: {i}")

# Empty if block (needed syntactically)
x = 10
if x > 100:
    pass   # nothing to do if x is large — code required by syntax
else:
    print(f"x is {x}")

# Future function stub
def process_payment():
    pass   # implementation coming later
```

---

## Part 5: for/else and while/else

The `else` block runs only if the loop finished WITHOUT a `break`:

```python
# Search — use for/else
target = 42
numbers = [10, 25, 33, 50, 71]

for n in numbers:
    if n == target:
        print(f"Found {target}!")
        break
else:
    print(f"{target} not found in list.")   # runs if loop ended without break

# Login attempt — use while/else
MAX = 3
for attempt in range(1, MAX + 1):
    pwd = input(f"Password (attempt {attempt}/{MAX}): ")
    if pwd == "secret":
        print("Access granted!")
        break
else:
    print("Too many failed attempts. Account locked.")
```

---

## Part 6: Practical Examples

```python
# Process orders — skip invalid, stop on 'quit'
orders = ["laptop", "mouse", "", "keyboard", "quit", "monitor"]

for order in orders:
    if order == "quit":
        print("Processing stopped by user.")
        break
    if not order:
        print("  Skipping empty order.")
        continue
    print(f"  Processing: {order}")

# FizzBuzz with continue
for n in range(1, 21):
    if n % 15 == 0:
        print("FizzBuzz")
        continue
    if n % 3 == 0:
        print("Fizz")
        continue
    if n % 5 == 0:
        print("Buzz")
        continue
    print(n)
```

---

## Practice Exercises

1. Use `break` to find the first number in a list that is both even and divisible by 7.

2. Use `continue` to print only words longer than 4 characters from a sentence.

3. Write a number guessing game using `while True` and `break` to exit when the user guesses correctly.

4. Demonstrate for/else by searching for a value in a list — print "Found" or "Not found" appropriately.

---

## Next — Build the Projects

**[Project 01 → Grade System](../guided-projects/project-01-grade-system/)**
**[Project 02 → ATM Menu](../guided-projects/project-02-atm-menu/)**
**[Project 03 → Payroll Processor](../guided-projects/project-03-payroll-processor/)**
