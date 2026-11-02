# Lesson 03 — While Loops

**Phase:** 02 — Control Flow | **Time:** ~30 min

---

## Part 1: Concept

A `while` loop repeats a block of code as long as a condition is True.

**Analogy:** "Keep refilling the glass WHILE it's not full."

```
WHILE condition is True:
    do this
    (update something to eventually make condition False)
```

---

## Part 2: Basic Syntax

```python
while condition:
    body
    # IMPORTANT: something must change to eventually end the loop
```

---

## Part 3: Examples

### Countdown

```python
count = 5
while count > 0:
    print(f"Countdown: {count}")
    count -= 1       # CRITICAL: without this, infinite loop
print("Launch!")
```

### Sum Until Threshold

```python
total = 0
n = 1
while total < 100:
    total += n
    n += 1

print(f"Sum reached {total} at n={n-1}")
```

### Input Validation Loop

```python
# Keep asking until valid input
while True:
    age = int(input("Enter age (0-120): "))
    if 0 <= age <= 120:
        break        # Exit loop when valid
    print("Invalid age. Try again.")

print(f"Valid age entered: {age}")
```

### ATM PIN Verification

```python
CORRECT_PIN = "1234"
attempts = 0
max_attempts = 3

while attempts < max_attempts:
    pin = input("Enter PIN: ")
    if pin == CORRECT_PIN:
        print("Access granted!")
        break
    else:
        attempts += 1
        remaining = max_attempts - attempts
        if remaining > 0:
            print(f"Wrong PIN. {remaining} attempt(s) left.")
        else:
            print("Card blocked. Too many failed attempts.")
```

---

## Part 4: While/Else

The `else` block runs if the loop completes WITHOUT hitting `break`:

```python
attempts = 0
found = False

while attempts < 5:
    guess = int(input("Guess (1-10): "))
    if guess == 7:
        print("Correct!")
        found = True
        break
    attempts += 1
else:
    print("Out of attempts!")   # Runs if loop finished without break
```

---

## Part 5: Common Mistakes

```python
# Mistake 1: Infinite loop (forgot to update counter)
count = 0
while count < 5:
    print(count)
    # Missing: count += 1  → runs forever!

# Mistake 2: Off-by-one
count = 1
while count < 5:
    print(count)   # Prints 1, 2, 3, 4  (not 5)
    count += 1

# For count 1-5:
while count <= 5:   # use <= 5 if you want to include 5
    print(count)
    count += 1
```

---

## Practice Exercises

1. Write a multiplication table generator: ask for a number, print its table from 1 to 12 using a while loop.

2. Write a number guessing game: generate a random 1-10 number, let user guess until correct (tracking attempts).

3. Sum all even numbers from 1 to 100 using a while loop.

4. Password strength checker: keep asking for a password until it's at least 8 characters, has a digit, and has an uppercase letter.

5. What's wrong?
   ```python
   n = 10
   while n > 0:
       print(n)
   ```

---

## Next Lesson

**[Lesson 04 → For Loops](lesson-04-for-loops.md)**
