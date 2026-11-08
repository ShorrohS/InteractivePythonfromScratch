# Phase 02 — Intermediate Exercise Solutions

---

## Q1. Prime Number Checker

```python
num = int(input("Enter a number (>= 2): "))

if num < 2:
    print(f"{num} is NOT prime.")
else:
    is_prime = True             # assume prime until a divisor is found
    i = 2
    while i < num:
        if num % i == 0:        # i divides num evenly → not prime
            is_prime = False
            break               # no need to keep checking
        i += 1

    if is_prime:
        print(f"{num} is PRIME.")
    else:
        print(f"{num} is NOT prime.")
```

**Explanation:** Test every integer from 2 up to (not including) `num`. The first divisor found proves non-primality, and `break` exits immediately. For large numbers, you can replace `while i < num` with `while i <= int(num**0.5)` — any factor larger than √N must be paired with one smaller than √N, so checking up to √N is sufficient.

---

## Q2. FizzBuzz Extended

```python
fizz_count = buzz_count = fizzbuzz_count = plain_count = 0

for i in range(1, 101):
    # Test the combined case FIRST — 15 is divisible by both 3 and 5
    # Testing 3 first would print "Fizz" for 15 instead of "FizzBuzz"
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz", end=" ")
        fizzbuzz_count += 1
    elif i % 3 == 0:
        print("Fizz", end=" ")
        fizz_count += 1
    elif i % 5 == 0:
        print("Buzz", end=" ")
        buzz_count += 1
    else:
        print(i, end=" ")
        plain_count += 1

print()  # newline after the sequence

print(f"\nSummary:")
print(f"  FizzBuzz : {fizzbuzz_count}")
print(f"  Fizz     : {fizz_count}")
print(f"  Buzz     : {buzz_count}")
print(f"  Plain    : {plain_count}")
```

---

## Q3. Word Frequency Counter

```python
sentence = input("Enter a sentence: ")
words = sentence.lower().split()    # lowercase then split on whitespace

# Build a frequency dictionary manually — key = word, value = count
freq = {}
for word in words:
    if word in freq:
        freq[word] += 1             # word seen before: increment
    else:
        freq[word] = 1              # first occurrence: initialise to 1

# Sort by frequency descending; alphabetically for ties
sorted_items = sorted(freq.items(), key=lambda item: (-item[1], item[0]))

print(f"\nWord frequencies ({len(words)} words, {len(freq)} unique):")
for word, count in sorted_items:
    bar = "█" * count
    print(f"  {word:<15} : {count:>3}  {bar}")
```

---

## Q4. Formatted Multiplication Table

```python
n = int(input("Enter N (1-20): "))

# Print the header row (column numbers)
print(f"  {'':5}", end="")
for j in range(1, n + 1):
    print(f"{j:5}", end="")
print()
print("  " + "-" * (5 * n + 5))     # separator line

# Print each row: row label then products
for i in range(1, n + 1):
    print(f"  {i:2} |", end="")     # row label, right-aligned in 2 chars
    for j in range(1, n + 1):
        print(f"{i * j:5}", end="") # each product right-aligned in 5 chars
    print()
```

---

## Q5. Find Common Elements (No Set Operations)

```python
list_a = [3, 7, 1, 9, 4, 6, 11, 2, 8]
list_b = [6, 2, 7, 13, 4, 9, 20, 7]

common = []

for a in list_a:
    # Search for 'a' in list_b using a nested loop
    found = False
    for b in list_b:
        if a == b:
            found = True
            break               # match confirmed — no need to scan the rest of list_b

    # Add to results only if found AND not already recorded (avoids duplicates)
    if found and a not in common:
        common.append(a)

print(f"List A: {list_a}")
print(f"List B: {list_b}")
print(f"Common elements: {common}")
print(f"Count: {len(common)}")
```

---

## Q6. Simple ATM Menu Loop

```python
balance = 1_000.00

print("=" * 35)
print("           ATM")
print("=" * 35)

while True:
    # Display menu on every iteration
    print("\n1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Exit")

    choice = input("Choice: ").strip()

    if choice == "1":
        print(f"  Balance: ${balance:,.2f}")

    elif choice == "2":
        try:
            amount = float(input("  Amount to deposit: $"))
        except ValueError:
            print("  Invalid amount.")
            continue            # jump back to the menu
        if amount <= 0:
            print("  Amount must be positive.")
            continue
        balance += amount
        print(f"  Deposited ${amount:,.2f}. New balance: ${balance:,.2f}")

    elif choice == "3":
        try:
            amount = float(input("  Amount to withdraw: $"))
        except ValueError:
            print("  Invalid amount.")
            continue
        if amount <= 0:
            print("  Amount must be positive.")
            continue
        if amount > balance:
            print("  Error: insufficient funds.")
            continue            # skip the update, go back to menu
        balance -= amount
        print(f"  Withdrew ${amount:,.2f}. New balance: ${balance:,.2f}")

    elif choice == "4":
        print("  Goodbye!")
        break                   # exit the while loop — session ends

    else:
        print("  Invalid option. Please enter 1-4.")
```

---

## Q7. Running Average with Early Exit

```python
THRESHOLD = 80.0
total = 0
count = 0

print("Enter positive numbers one at a time (0 to stop).")

while True:
    try:
        num = float(input("Enter number (0 to stop): "))
    except ValueError:
        print("  Please enter a valid number.")
        continue                # invalid input — re-prompt without counting it

    if num == 0:
        print("  Sentinel 0 received — stopping.")
        break

    total += num
    count += 1
    average = total / count
    print(f"  Running average: {average:.2f}")

    if average > THRESHOLD:     # second exit condition
        print(f"  Average exceeded {THRESHOLD} — stopping.")
        break

if count > 0:
    print(f"\nNumbers entered: {count}  |  Final average: {total / count:.2f}")
else:
    print("\nNo numbers were entered.")
```

**Explanation:** Two `break` statements handle the two stopping conditions independently. The `continue` on invalid input is essential — without it, an invalid entry would be counted and would corrupt the average.
