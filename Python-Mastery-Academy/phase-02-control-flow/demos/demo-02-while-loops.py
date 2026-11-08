"""
Demo 02 — While Loops
Phase 02: Control Flow

Run: python demo-02-while-loops.py
"""

print("=" * 50)
print("DEMO 02 — While Loops")
print("=" * 50)

# --- BASIC WHILE SYNTAX ---
print("\n1. Basic while syntax:")
# A while loop repeats its body as long as the condition is True.
# Three things are always needed: INITIALISE, TEST, UPDATE.

count = 1                       # 1. Initialise: set up the counter before the loop
while count <= 5:               # 2. Test: checked before every iteration
    print(f"  count = {count}")
    count += 1                  # 3. Update: move toward the exit condition
print(f"  Loop ended — count is now {count}.")

# --- COUNTER-CONTROLLED LOOPS ---
print("\n2. Counter-controlled loops:")
# The counter variable fully determines how many iterations occur.

# Counting up
print("  Count up (1–10):", end=" ")
i = 1
while i <= 10:
    print(i, end=" ")
    i += 1
print()

# Counting down
print("  Countdown:", end=" ")
i = 5
while i >= 1:
    print(i, end=" ")
    i -= 1
print("Go!")

# Custom step: add 3 each iteration
print("  Every 3rd number (0–30):", end=" ")
n = 0
while n <= 30:
    print(n, end=" ")
    n += 3
print()

# --- SENTINEL-VALUE LOOPS ---
print("\n3. Sentinel-value loops:")
# A sentinel is a special value that signals "stop processing".
# Common in real apps: summing sales until the user enters -1, reading lines
# until "quit", processing records until end-of-file.

# Simulate the user entering numbers until they type 0 (the sentinel).
# Fixed list is used here so the demo runs without interactive input.
values = [15, 42, 8, 73, 29, 0]    # 0 is the sentinel
index = 0
total = 0

print("  Summing numbers (0 = stop):")
while True:                         # run indefinitely ...
    n = values[index]               # in real code: n = int(input("Enter (0 to stop): "))
    index += 1
    if n == 0:                      # ... until the sentinel is received
        print("  [Sentinel 0 detected — stopping]")
        break
    total += n
    print(f"    Added {n} → running total: {total}")
print(f"  Final sum: {total}")

# --- INFINITE-LOOP PREVENTION AND BEST PRACTICES ---
print("\n4. Infinite-loop prevention:")
# COMMON MISTAKE — the variable never changes, so the condition is always True:
#
#   x = 0
#   while x < 5:
#       print(x)      # BUG: x never changes → loop never ends!
#
# Best practices:
#   1. Always update the loop variable inside the body.
#   2. Add a safety counter guard for loops driven by external conditions.
#   3. Trace the condition on paper before running.

# Safe pattern: cap iterations to prevent runaway loops
value = 1
iterations = 0
max_iter = 50                   # hard ceiling — loop can never exceed this

while value < 1_000_000:
    value *= 2
    iterations += 1
    if iterations >= max_iter:  # safety net
        print("  Safety guard triggered — stopping early!")
        break

print(f"  Result: {value:,} reached in {iterations} iteration(s).")

# --- WHILE-ELSE CONSTRUCT ---
print("\n5. while-else construct:")
# The else block runs ONLY when the loop ends normally (condition → False).
# It does NOT run if the loop exits via break.
# Best use: clearly signal "the search completed without finding a match."

haystack = [4, 7, 2, 9, 3, 6]

for target in [9, 99]:          # test with a value present, then one absent
    i = 0
    while i < len(haystack):
        if haystack[i] == target:
            print(f"  Found {target} at index {i}.")
            break               # match found — skip else block
        i += 1
    else:
        # Reached here because the while condition (i < len) became False
        print(f"  {target} not found in {haystack} — else block ran.")

# --- INPUT VALIDATION PATTERN ---
print("\n6. Input validation loop (simulated):")
# Keep asking until the user provides acceptable input.
# This pattern is everywhere: login forms, configuration prompts, numeric inputs.
# The loop only exits through break when validation passes.

attempts = ["abc", "", "-5", "42"]  # simulated responses (42 is the first valid one)
idx = 0

while True:
    user_input = attempts[idx]          # in real code: input("Enter a positive integer: ")
    idx += 1
    print(f"  Received: '{user_input}'", end="")
    # Validation: must be a string of digits and convert to a positive integer
    if user_input.isdigit() and int(user_input) > 0:
        print(f" → Valid! Accepted {user_input}.")
        break
    print(" → Invalid — must be a positive integer. Try again.")

# --- NUMBER-GUESSING GAME LOGIC ---
print("\n7. Number-guessing game logic (auto-play):")
# Combines while loop, conditionals, and break into a classic interactive program.
# The loop runs indefinitely; break fires only on a correct guess or when
# the player runs out of attempts.
import random
random.seed(7)                              # fixed seed → reproducible output
secret = random.randint(1, 20)
guesses = [5, 15, 12, 14, 13]              # pre-scripted guesses for the demo
max_guesses = 5
attempt = 0

print(f"  [Secret number is {secret}]  Max guesses: {max_guesses}")
while attempt < max_guesses:
    guess = guesses[attempt]
    attempt += 1
    print(f"  Guess {attempt}: {guess}", end=" ")
    if guess == secret:
        print(f"→ Correct! Won in {attempt} guess(es).")
        break
    elif guess < secret:
        print("→ Too low.")
    else:
        print("→ Too high.")
else:
    # Loop ended normally — player used all guesses without winning
    print(f"  Game over — the number was {secret}.")

print("\n" + "=" * 50)
