# Phase 02 — Advanced Exercise Solutions

---

## Q1. Sieve of Eratosthenes

```python
N = int(input("Find all primes up to N: "))

# Step 1: Create a boolean list; index = number, True = "still a candidate prime"
is_prime = [True] * (N + 1)

# Step 2: 0 and 1 are not prime by definition
is_prime[0] = False
is_prime[1] = False

# Step 3: Eliminate multiples
# Only need to sieve up to √N — any composite number must have a factor ≤ √N
p = 2
while p * p <= N:
    if is_prime[p]:                     # p is prime; mark all its multiples
        multiple = p * p                # start at p², because 2p…(p-1)p already sieved
        while multiple <= N:
            is_prime[multiple] = False  # composite — cross it out
            multiple += p               # advance by p to hit the next multiple
    p += 1

# Step 4: Collect all indices still marked True
primes = []
for i in range(N + 1):
    if is_prime[i]:
        primes.append(i)

print(f"Primes up to {N}: {primes}")
print(f"Count: {len(primes)}")
```

**Algorithm note:** Starting the inner sieve at `p * p` instead of `2 * p` is the classic optimisation — all smaller multiples of `p` were already eliminated by earlier primes. Time complexity: O(N log log N).

---

## Q2. Character Frequency Analysis

```python
text = input("Enter a paragraph of text:\n")

# Basic counts
total_chars = len(text)
total_words = len(text.split())

# Count letter frequencies (case-insensitive)
letter_counts = {}
total_letters = 0
for char in text:
    if char.isalpha():                      # only count alphabetic characters
        letter = char.lower()
        total_letters += 1
        if letter in letter_counts:
            letter_counts[letter] += 1
        else:
            letter_counts[letter] = 1

# Sort all letters by count descending, take top 5
sorted_letters = sorted(letter_counts.items(), key=lambda x: -x[1])
top5 = sorted_letters[:5]

print(f"\nCharacters: {total_chars}  |  Words: {total_words}  |  Letters: {total_letters}")

if top5:
    max_count = top5[0][1]              # highest frequency (for proportional bars)
    print("\nTop 5 letters:")
    for letter, count in top5:
        pct = count / total_letters * 100
        bar_len = count * 20 // max_count   # scale bar to max 20 blocks
        bar = "█" * bar_len
        print(f"  {letter}: {count:3}  ({pct:4.1f}%)  {bar}")
```

---

## Q3. Bubble Sort

```python
data = [64, 34, 25, 12, 22, 11, 90]
n = len(data)
passes = 0

print(f"Original: {data}")

for i in range(n - 1):              # at most n-1 passes are ever needed
    swapped = False

    # Inner loop: compare adjacent pairs; the largest unsorted element
    # "bubbles" to position n-1-i after each pass
    for j in range(n - i - 1):     # upper bound shrinks by 1 each pass (already sorted)
        if data[j] > data[j + 1]:
            data[j], data[j + 1] = data[j + 1], data[j]   # swap in one line
            swapped = True

    passes += 1
    label = "  ← no swaps" if not swapped else ""
    print(f"Pass {passes}:   {data}{label}")

    if not swapped:                 # optimisation: a pass with no swaps means sorted
        break

print(f"\nSorted:   {data}")
print(f"Passes needed: {passes}")
```

**Algorithm note:** The `swapped` early-exit flag turns best-case performance into O(N) — an already-sorted list finishes in a single pass. Without it, bubble sort always runs O(N²) regardless of input order.

---

## Q4. Spiral Number Grid

```python
N = int(input("Enter N: "))

# Build an N×N grid pre-filled with zeros
grid = [[0] * N for _ in range(N)]

# Four boundary pointers shrink inward as each edge is filled
top, bottom = 0, N - 1
left, right  = 0, N - 1
num = 1                             # start filling from 1

while num <= N * N:

    # → Fill left to right across the top row
    for col in range(left, right + 1):
        grid[top][col] = num
        num += 1
    top += 1                        # top boundary moves inward

    # ↓ Fill top to bottom down the right column
    for row in range(top, bottom + 1):
        grid[row][right] = num
        num += 1
    right -= 1                      # right boundary moves inward

    # ← Fill right to left across the bottom row
    for col in range(right, left - 1, -1):
        grid[bottom][col] = num
        num += 1
    bottom -= 1                     # bottom boundary moves inward

    # ↑ Fill bottom to top up the left column
    for row in range(bottom, top - 1, -1):
        grid[row][left] = num
        num += 1
    left += 1                       # left boundary moves inward

# Print the grid with right-aligned columns wide enough for the largest value
cell_width = len(str(N * N)) + 1
for row in grid:
    for cell in row:
        print(f"{cell:{cell_width}}", end="")
    print()
```

**Algorithm note:** The four boundary pointers (`top`, `bottom`, `left`, `right`) each advance by 1 after their edge is filled. The outer `while` loop terminates when every cell has been assigned (num > N²). This handles all N, including odd N where the final position is the exact centre cell.

---

## Q5. Fibonacci Sequence with Dual Stopping Conditions

```python
limit    = int(input("Enter limit (stop when value exceeds this): "))
max_count = int(input("Enter max count (stop after this many numbers): "))

a, b = 0, 1                     # first two Fibonacci numbers
count = 0
prev = None                     # tracks the last printed value for the ratio

while True:
    # Check the limit BEFORE printing: stop if the current value already exceeded it
    if a > limit:
        print(f"Stopped: value {a} exceeds limit {limit}.")
        break

    count += 1
    print(f"{count:3}: {a:9}")
    prev = a                    # remember the value we just printed
    a, b = b, a + b             # advance: a becomes the next Fibonacci number

    # Check the count limit AFTER printing
    if count >= max_count:
        print(f"Stopped: reached max count of {max_count}.")
        break

# Golden-ratio approximation: ratio of consecutive Fibonacci terms → φ ≈ 1.618…
if count >= 2 and prev > 0:
    print(f"Ratio of last two terms: {a / prev:.4f}")
```

**Note on the golden ratio:** As the Fibonacci sequence grows, each term divided by the previous one converges to the golden ratio φ = (1 + √5) / 2 ≈ 1.6180339… This property makes Fibonacci numbers appear throughout nature and art.

---

## Q6. Caesar Cipher Brute-Force

```python
ciphertext = "Khoor, Zruog! Wklv lv d vhfuhw phvvdjh."

# Small list of common English words used for scoring candidates
word_list = ["the", "a", "is", "this", "hello", "world", "it", "and", "of",
             "to", "in", "that", "was", "he", "she", "are", "secret", "message"]

best_shift = 0
best_score = -1
best_text  = ""

for shift in range(1, 26):          # try every possible shift from 1 to 25
    decoded_chars = []

    for char in ciphertext:
        if char.isalpha():
            # Shift character back by 'shift' positions, wrapping with modulo 26
            base = ord('A') if char.isupper() else ord('a')
            decoded_chars.append(chr((ord(char) - base - shift) % 26 + base))
        else:
            decoded_chars.append(char)  # preserve spaces, punctuation, digits

    candidate = "".join(decoded_chars)

    # Score: count how many words in the decoded text match known English words
    score = 0
    for word in candidate.lower().split():
        clean_word = word.strip(".,!?;:\"'")   # strip punctuation before matching
        if clean_word in word_list:
            score += 1

    marker = f"  ← best match (score: {score})" if score >= best_score + 1 else ""
    print(f"Shift {shift:2}: {candidate}{marker}")

    if score > best_score:
        best_score = score
        best_shift = shift
        best_text  = candidate

print(f"\nBest match → Shift {best_shift}: {best_text}")
```

**Algorithm note:** Each letter is shifted back by the trial amount using `(ord(char) - base - shift) % 26`. The modulo 26 handles wrap-around (e.g. decoding 'A' with shift 3 correctly gives 'X'). A language model or larger word list would score more accurately.

---

## Q7. Pascal's Triangle

```python
N = int(input("Enter number of rows: "))

triangle = []

for i in range(N):
    if i == 0:
        row = [1]                       # first row is always just [1]
    else:
        prev = triangle[-1]             # the row immediately above
        row = [1]                       # every row starts with 1

        # Each interior element = sum of the two elements above it
        for j in range(len(prev) - 1):
            row.append(prev[j] + prev[j + 1])

        row.append(1)                   # every row ends with 1

    triangle.append(row)

# Convert the last (widest) row to a string to determine centering width
last_row_str = " ".join(str(x) for x in triangle[-1])
width = len(last_row_str)

print(f"\nPascal's Triangle — {N} row(s):\n")
for row in triangle:
    row_str = " ".join(str(x) for x in row)
    print(row_str.center(width))        # Python's str.center() handles the padding
```

**How it works:** Each element in Pascal's triangle is a binomial coefficient C(n, k). The construction rule — each element is the sum of the two above it — is directly encoded in the inner loop. `.center(width)` pads the string with spaces on both sides so the triangle looks symmetrical when printed.
