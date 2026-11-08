# Phase 02 — Intermediate Exercises

> These exercises require complete programs. You will need while loops, for loops, nested loops, and break/continue.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Prime Number Checker**

Write a program that asks the user for a positive integer (≥ 2) and reports whether it is a **prime number**.

A prime number is greater than 1 and has no divisors other than 1 and itself (e.g. 2, 3, 5, 7, 11, 13 …).

**Example:**
```
Enter a number: 17
17 is PRIME.

Enter a number: 12
12 is NOT prime.
```

> **Hints:**
> - Use a while loop from 2 up to (but not including) the number.
> - As soon as you find any divisor, stop — the number is not prime.
> - Numbers ≤ 1 are never prime.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q2. FizzBuzz Extended**

Print all integers from 1 to 100, but replace:
- Multiples of 3 with **"Fizz"**
- Multiples of 5 with **"Buzz"**
- Multiples of both 3 and 5 with **"FizzBuzz"**

Then print a summary line: how many Fizz, Buzz, FizzBuzz, and plain numbers appeared.

**Expected summary:** Fizz: 27, Buzz: 14, FizzBuzz: 6, Plain: 53

> **Hints:**
> - Always check the combined case (divisible by both 3 and 5) **first** — otherwise 15 would incorrectly match just "Fizz".
> - Maintain four counter variables; increment the right one inside each branch.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q3. Word Frequency Counter**

Ask the user to enter a sentence. Count how many times each unique word appears (case-insensitive). Display the results sorted by frequency, most frequent first.

**Example:**
```
Enter a sentence: to be or not to be that is the question
to       : 2  ██
be       : 2  ██
or       : 1  █
not      : 1  █
that     : 1  █
is       : 1  █
the      : 1  █
question : 1  █
```

> **Hints:**
> - `sentence.lower().split()` gives you a list of lowercase words.
> - Use a dictionary to store word → count.
> - To loop over the dictionary in frequency order, sort `.items()` by value descending.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q4. Formatted Multiplication Table**

Ask the user for a number N (between 1 and 20). Print a formatted N × N multiplication table with aligned columns and a header row.

**Example (N = 4):**
```
        1    2    3    4
  1 |   1    2    3    4
  2 |   2    4    6    8
  3 |   3    6    9   12
  4 |   4    8   12   16
```

> **Hints:**
> - Use nested for loops: outer for rows, inner for columns.
> - `f"{value:4}"` right-aligns a number in a 4-character-wide field.
> - Print the header row and a separator line before the nested loops start.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q5. Find Common Elements (No Set Operations)**

Using only loops and lists (no `set`, `intersection`, or `in` on a set), find all elements that appear in **both** lists below. Print the common elements and the count.

```python
list_a = [3, 7, 1, 9, 4, 6, 11, 2, 8]
list_b = [6, 2, 7, 13, 4, 9, 20, 7]
```

**Expected output:**
```
Common elements: [7, 9, 4, 6, 2]
Count: 5
```

> **Hints:**
> - Use nested loops: for each element in `list_a`, loop through `list_b` checking for equality.
> - Before adding to your result list, check the element is not already there (to avoid duplicates).
> - `break` out of the inner loop as soon as a match is found.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q6. Simple ATM Menu Loop**

Build a simple ATM simulation using a `while True` loop and `break`/`continue`.

- Start with a balance of **$1,000.00**.
- Show a menu: 1) Check Balance  2) Deposit  3) Withdraw  4) Exit
- Validate: deposit/withdrawal amounts must be positive; withdrawals cannot exceed the current balance.
- Loop until the user chooses Exit.

**Example session:**
```
Choice: 3
Amount: 250
Withdrew $250.00. New balance: $750.00

Choice: 3
Amount: 900
Error: insufficient funds.

Choice: 4
Goodbye!
```

> **Hints:**
> - `while True:` with `break` on option 4 keeps the loop alive until Exit.
> - Use `continue` after an error message to re-show the menu immediately.
> - A single `balance` variable updated inside the loop persists across every iteration.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q7. Running Average with Early Exit**

Ask the user to enter positive numbers one at a time. After each entry, print the running average. Stop when:
1. The user enters **0** (sentinel), **or**
2. The running average **exceeds 80**

After stopping, print how many numbers were entered and the final average.

**Example:**
```
Enter number (0 to stop): 70
Running average: 70.00
Enter number (0 to stop): 85
Running average: 77.50
Enter number (0 to stop): 92
Running average: 82.33
Average exceeded 80 — stopping.
Numbers entered: 3  |  Final average: 82.33
```

> **Hints:**
> - Keep a `total` and a `count`. Average = `total / count`.
> - Check the sentinel first, then update totals, then check the threshold.
> - Both exit conditions should use `break`.

> **Difficulty:** ⭐⭐ Intermediate

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
