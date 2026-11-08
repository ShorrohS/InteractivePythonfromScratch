"""
Demo 04 — Nested Loops
Phase 02: Control Flow

Run: python demo-04-nested-loops.py
"""

print("=" * 50)
print("DEMO 04 — Nested Loops")
print("=" * 50)

# --- BASIC NESTED FOR LOOPS ---
print("\n1. Basic nested for loops:")
# Place one loop inside another to iterate over combinations.
# The INNER loop completes fully for every single iteration of the outer loop.
# Outer runs M times × Inner runs N times = M × N total iterations.

for i in range(1, 4):           # outer: 3 iterations (i = 1, 2, 3)
    for j in range(1, 4):       # inner: 3 iterations per outer (j = 1, 2, 3)
        print(f"  ({i},{j})", end=" ")
    print()                     # newline after each row

# --- MULTIPLICATION TABLE ---
print("\n2. Multiplication table (1–10):")
# Outer loop = row (left-hand factor), inner loop = column (right-hand factor).
# A classic nested-loop application — every cell is the product of row × col.

# Header row
print("     ", end="")
for j in range(1, 11):
    print(f"{j:4}", end="")
print("\n  " + "-" * 42)

for i in range(1, 11):
    print(f"  {i:2}|", end="")
    for j in range(1, 11):
        print(f"{i * j:4}", end="")   # 4-char wide column keeps alignment
    print()

# --- TRIANGLE PATTERN ---
print("\n3. Triangle patterns:")
# Outer loop = which row (1 to N), inner loop = how many symbols on that row.

rows = 6

print("  Right triangle:")
for i in range(1, rows + 1):
    for _ in range(i):          # print i stars on row i
        print("*", end="")
    print()

print("  Inverted triangle:")
for i in range(rows, 0, -1):   # start full, shrink toward 1
    print("  " + "*" * i)

print("  Number staircase:")
for i in range(1, rows + 1):
    for j in range(1, i + 1):
        print(j, end="")        # print the column number, not a star
    print()

# --- RECTANGLE (HOLLOW BORDER) ---
print("\n4. Hollow rectangle:")
width, height = 12, 5
for row in range(height):
    for col in range(width):
        # Border condition: top/bottom row OR left/right column
        if row == 0 or row == height - 1 or col == 0 or col == width - 1:
            print("*", end="")
        else:
            print(" ", end="")  # interior stays empty
    print()

# --- NESTED WHILE LOOPS ---
print("\n5. Nested while loops:")
# While loops nest just like for loops.
# Remember to RESET the inner counter each time the outer advances.

row = 1
while row <= 5:
    col = 1
    while col <= row:           # inner counter resets to 1 for every new row
        print(col, end=" ")
        col += 1
    print()
    row += 1

# --- MATRIX TRAVERSAL ---
print("\n6. Matrix traversal:")
# A 2-D list (list of lists) represents a matrix.
# Outer loop visits each row; inner loop visits each element in that row.

matrix = [
    [ 1,  2,  3,  4],
    [ 5,  6,  7,  8],
    [ 9, 10, 11, 12],
]

print("  Matrix:")
for row in matrix:
    print("  ", end="")
    for cell in row:
        print(f"{cell:3}", end="")
    print()

# Locate the maximum value and its position (row, column)
max_val = matrix[0][0]
max_pos = (0, 0)
for r, row in enumerate(matrix):
    for c, cell in enumerate(row):
        if cell > max_val:
            max_val = cell
            max_pos = (r, c)
print(f"  Max: {max_val} at row {max_pos[0]}, col {max_pos[1]}")

# Compute the sum of the main diagonal (top-left to bottom-right)
diag_sum = 0
for i in range(len(matrix)):
    if i < len(matrix[i]):      # guard: only square matrices have a full diagonal
        diag_sum += matrix[i][i]
print(f"  Main diagonal sum: {diag_sum}")

# --- TIME COMPLEXITY AWARENESS ---
print("\n7. Time complexity — why nesting matters:")
# Each extra nesting level multiplies the number of operations.
# One loop over N items  → O(N)    — scales linearly
# Two nested loops       → O(N²)   — quadratic, gets slow fast
# Three nested loops     → O(N³)   — avoid except for small N
#
# At scale: N=1,000 → 1,000,000 operations for O(N²). N=1,000,000 → 1 trillion. Ouch.

print(f"\n  {'N':>7}  {'O(N)':>10}  {'O(N^2)':>14}  {'O(N^3)':>18}")
print("  " + "-" * 54)
for n in [10, 100, 1_000, 10_000]:
    print(f"  {n:>7,}  {n:>10,}  {n**2:>14,}  {n**3:>18,}")

# --- PRACTICAL: FIND ALL PAIRS THAT SUM TO A TARGET ---
print("\n8. Practical: find all pairs summing to a target:")
# Classic O(N²) algorithm — scan every possible pair.
# Acceptable for small lists; for large data a hash-based O(N) solution is better.

numbers    = [2, 7, 4, 1, 5, 8, 3, 6]
target_sum = 9
pairs      = []

for i in range(len(numbers)):
    for j in range(i + 1, len(numbers)):    # j starts AFTER i to avoid duplicates
        if numbers[i] + numbers[j] == target_sum:
            pairs.append((numbers[i], numbers[j]))

print(f"  Numbers:   {numbers}")
print(f"  Target:    {target_sum}")
print(f"  Pairs:     {pairs}  ({len(pairs)} found)")

print("\n" + "=" * 50)
