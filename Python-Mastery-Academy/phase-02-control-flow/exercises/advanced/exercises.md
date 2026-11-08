# Phase 02 — Advanced Exercises

> These exercises combine all Phase 02 control flow concepts to solve real algorithmic problems.
> Plan your loop structure carefully before writing any code.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Sieve of Eratosthenes**

Implement the Sieve of Eratosthenes to find every prime number up to a user-supplied limit N.

**Algorithm:**
1. Create a list of `True` values indexed 0 to N. Every index is a "candidate prime".
2. Mark indices 0 and 1 as `False` (they are not prime).
3. For each number `p` starting at 2: if `p` is still marked `True`, mark all of its multiples (starting from `p * p`) as `False`.
4. Repeat step 3 up to √N — anything larger cannot have an unmarked composite.
5. Collect all indices still marked `True`.

**Example (N = 30):**
```
Primes up to 30: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
Count: 10
```

> **Hints:**
> - `is_prime = [True] * (N + 1)` creates the initial list in one line.
> - Outer loop: `p` from 2 to `int(N**0.5) + 1`.
> - Inner loop: `range(p * p, N + 1, p)` marks multiples with a step of `p`.
> - Starting the inner loop at `p * p` (not `2 * p`) is the efficiency trick.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q2. Character Frequency Analysis**

Ask the user to enter a paragraph of text and perform a detailed frequency analysis:

- Total character count (including spaces and punctuation)
- Total word count
- Top 5 most frequent **letters** (letters only, case-insensitive), shown with a percentage of all letters and a proportional bar chart

**Example output:**
```
Characters : 142  |  Words: 28  |  Letters: 115

Top 5 letters:
  e: 18  (15.7%)  ████████████████
  t: 14  (12.2%)  ████████████
  a: 11   (9.6%)  █████████
  o: 10   (8.7%)  ████████
  i:  9   (7.8%)  ███████
```

> **Hints:**
> - Loop over every character; use `char.isalpha()` to filter letters.
> - Use a dictionary to accumulate counts, then extract the top 5 by sorting.
> - Bar length formula: `count * 20 // max_count` gives proportional bars up to 20 blocks wide.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q3. Bubble Sort**

Implement bubble sort from scratch — **no** `list.sort()` or `sorted()` allowed.

Bubble sort works by repeatedly stepping through the list, comparing adjacent elements, and swapping them if they are in the wrong order. After each full pass the largest unsorted element has "bubbled" to its final position.

Use this list: `[64, 34, 25, 12, 22, 11, 90]`

Display the state of the list after each pass.

**Example output:**
```
Original: [64, 34, 25, 12, 22, 11, 90]
Pass 1:   [34, 25, 12, 22, 11, 64, 90]
Pass 2:   [25, 12, 22, 11, 34, 64, 90]
Pass 3:   [12, 22, 11, 25, 34, 64, 90]
Pass 4:   [12, 11, 22, 25, 34, 64, 90]
Pass 5:   [11, 12, 22, 25, 34, 64, 90]
Pass 6:   [11, 12, 22, 25, 34, 64, 90]  ← no swaps
Sorted:   [11, 12, 22, 25, 34, 64, 90]
Passes needed: 6
```

> **Hints:**
> - Outer loop runs up to N-1 times (N = length of list).
> - Inner loop compares `data[j]` and `data[j+1]`; swap with `data[j], data[j+1] = data[j+1], data[j]`.
> - Add a `swapped` flag: if a full pass makes **no** swaps, the list is already sorted — use `break` to stop early.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q4. Spiral Number Grid**

Ask the user for N. Generate and print an N × N grid filled with the integers 1 to N² arranged in a **clockwise spiral** starting from the top-left corner.

**Example (N = 4):**
```
 1  2  3  4
12 13 14  5
11 16 15  6
10  9  8  7
```

> **Hints:**
> - Create a 2-D list: `grid = [[0] * N for _ in range(N)]`
> - Track four boundary pointers: `top`, `bottom`, `left`, `right`.
> - Use four loops inside a `while` loop:
>   1. Fill left → right across the top row; then `top += 1`
>   2. Fill top → bottom down the right column; then `right -= 1`
>   3. Fill right → left across the bottom row; then `bottom -= 1`
>   4. Fill bottom → top up the left column; then `left += 1`
> - Stop when the number to place exceeds N².

> **Difficulty:** ⭐⭐⭐⭐ Advanced+

---

**Q5. Fibonacci Sequence with Dual Stopping Conditions**

Generate Fibonacci numbers using a while loop. Stop when **either** condition is met first:
1. The current value **exceeds a user-supplied limit**, or
2. A user-supplied **maximum count** of numbers has been generated.

Print each number with its 1-based index. After the sequence ends, print:
- Which condition triggered the stop
- The ratio of the last two generated terms (approaches the golden ratio ≈ 1.618)

**Example (limit = 1000, max_count = 20):**
```
 1:        0
 2:        1
 3:        1
 ...
16:      610
17:      987
Stopped: next value (1597) would exceed limit 1000.
Ratio of last two terms: 1.6180
```

> **Hints:**
> - Start with `a, b = 0, 1`. Print `a`, then advance with `a, b = b, a + b`.
> - After advancing, check if the NEW value of `a` exceeds the limit before printing it.
> - Track the previous value so you can compute the final ratio.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q6. Caesar Cipher Brute-Force**

Implement a Caesar cipher brute-force decoder. Try all 25 possible shift values (1–25) and print each decoded candidate. Automatically identify the most likely correct shift by scoring each candidate against a small list of common English words.

Use this ciphertext: `"Khoor, Zruog! Wklv lv d vhfuhw phvvdjh."`

**Example output (partial):**
```
Shift  1: Jgnnq, Yqtnf! Vjku ku c ugetgv oguucig.
Shift  2: Ifmmp, Xpsme! Uijt jt b tfdsfu nfttbhf.
Shift  3: Hello, World! This is a secret message.  ← best match (score: 5)
...
Best match → Shift 3: Hello, World! This is a secret message.
```

> **Hints:**
> - Shift only alphabetic characters; preserve case, spaces, and punctuation.
> - Decode formula: `chr((ord(char) - ord('a') - shift) % 26 + ord('a'))` for lowercase.
> - Score each candidate by counting how many words (strip punctuation first) appear in a word list like `["the", "a", "is", "this", "hello", "world", "it"]`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q7. Pascal's Triangle**

Generate and print the first N rows of Pascal's Triangle, centred in the terminal.

Each row begins and ends with 1. Every interior element equals the sum of the two elements directly above it. Display the triangle with each row centred relative to the widest (last) row.

**Example (N = 6):**
```
          1
        1   1
      1   2   1
    1   3   3   1
  1   4   6   4   1
1   5  10  10   5   1
```

> **Hints:**
> - Store each row as a list. Row 0 = `[1]`.
> - Build each new row by starting with `[1]`, looping over adjacent pairs from the previous row and summing them, then appending a final `[1]`.
> - Convert each row to a string with `" ".join(...)` and use Python's `.center(width)` to align it.
> - `width` = the length of the last row's string.

> **Difficulty:** ⭐⭐⭐ Advanced

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
