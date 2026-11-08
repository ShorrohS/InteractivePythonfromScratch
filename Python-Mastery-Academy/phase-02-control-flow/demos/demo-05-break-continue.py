"""
Demo 05 — break and continue
Phase 02: Control Flow

Run: python demo-05-break-continue.py
"""

print("=" * 50)
print("DEMO 05 — break and continue")
print("=" * 50)

# --- BREAK IN A FOR LOOP ---
print("\n1. break in a for loop:")
# break immediately exits the NEAREST enclosing loop.
# Any code after the loop (outside it) continues normally.
# Use it when you have found what you need and don't want to keep looping.

print("  Find first even number greater than 5 in [3, 7, 4, 9, 8, 2]:")
numbers = [3, 7, 4, 9, 8, 2]
found = None
for n in numbers:
    print(f"    Checking {n}...", end=" ")
    if n > 5 and n % 2 == 0:
        found = n
        print(f"← match! Breaking.")
        break           # exit loop immediately — no need to check the rest
    print("no match.")
print(f"  Result: {found}")

# --- BREAK IN A WHILE LOOP ---
print("\n2. break in a while loop:")
# break works identically inside while loops.
# Combine with a counter or condition to exit mid-iteration.

value = 1
steps = 0
while value < 1_000_000:
    value *= 3
    steps += 1
    if value > 500:     # exit early once we cross 500
        print(f"  Crossed 500 after {steps} step(s). value = {value}")
        break
print(f"  Final value: {value:,}")

# --- CONTINUE TO SKIP ITERATIONS ---
print("\n3. continue — skip the rest of the current iteration:")
# continue jumps immediately to the NEXT iteration — it does NOT exit the loop.
# Useful for filtering: "if this item doesn't qualify, skip it cleanly."

print("  Numbers 1-15, skipping multiples of 3:")
for i in range(1, 16):
    if i % 3 == 0:
        continue        # jump to next i; everything below this line is skipped
    print(i, end=" ")
print()

# continue inside a while loop — skip negatives, sum only positives
values = [5, -1, 8, -3, 2, -7, 4]
total = 0
for v in values:
    if v < 0:
        continue        # negative? skip it
    total += v
print(f"  Values: {values}")
print(f"  Sum (positives only): {total}")

# --- while True WITH BREAK ---
print("\n4. while True with break — the indefinite-loop pattern:")
# When you cannot know in advance how many iterations are needed, use
# while True and break when the exit condition is triggered.
# This is the standard pattern for menus, retry logic, and polling.

# Simulated retry: first two attempts fail, third succeeds.
attempt = 0
while True:
    attempt += 1
    success = (attempt == 3)    # pretend the third try always works
    print(f"  Attempt {attempt}:", "Success — breaking." if success else "Failed — retrying.")
    if success:
        break                   # exit only when work is done

# --- COMBINING BREAK AND CONTINUE ---
print("\n5. Combining break and continue in the same loop:")
# Use continue for "skip this item and move on."
# Use break for "stop everything."
# They can coexist in one loop — each handles a different case.

print("  Processing list (skip negatives, stop at sentinel 999):")
items = [4, -1, 7, -3, 999, 5, 2]
processed = []
for item in items:
    if item < 0:
        print(f"    Skipping {item} (negative)")
        continue            # jump to next item — don't process negatives
    if item == 999:
        print(f"    Sentinel 999 found — stopping.")
        break               # done — exit the loop entirely
    processed.append(item)
    print(f"    Processed {item}")
print(f"  Processed items: {processed}")

# --- SEARCH-AND-STOP PATTERN ---
print("\n6. Search-and-stop pattern:")
# Stop the loop as soon as a match is found.
# More efficient than scanning the entire collection unnecessarily.

inventory = [
    {"sku": "A001", "name": "Widget",  "stock": 12},
    {"sku": "B002", "name": "Gadget",  "stock":  0},
    {"sku": "C003", "name": "Doohickey","stock": 5},
]

for search_sku in ["B002", "Z999"]:
    for item in inventory:
        if item["sku"] == search_sku:
            status = "IN STOCK" if item["stock"] > 0 else "OUT OF STOCK"
            print(f"  {search_sku} ({item['name']}): {status} — qty {item['stock']}")
            break               # found — no need to check remaining items
    else:
        # for-else: else runs only if no break was hit (item not found)
        print(f"  {search_sku}: NOT FOUND in inventory")

# --- MENU LOOP PATTERN ---
print("\n7. Menu loop pattern (simulated):")
# The while True + break pattern is the standard way to build interactive menus.
# The menu keeps redisplaying until the user chooses to exit.
# continue is used to silently skip invalid input.

# Pre-scripted choices so the demo runs without interactive input.
# In real code each line would be: choice = input("Choice: ").strip()
selections = ["1", "3", "2", "5", "4"]     # 5 is invalid, should be silently skipped
sel_idx = 0

balance = 1_250.00

print("\n  === ATM Demo ===")
print("  1. Check balance  2. Deposit  3. Withdraw  4. Exit")

while True:
    choice = selections[sel_idx]; sel_idx += 1
    print(f"\n  [User entered: '{choice}']")

    if choice == "1":
        print(f"  Balance: ${balance:,.2f}")

    elif choice == "2":
        amount = 500.00                 # simulated deposit amount
        balance += amount
        print(f"  Deposited ${amount:,.2f}. New balance: ${balance:,.2f}")

    elif choice == "3":
        amount = 200.00                 # simulated withdrawal amount
        balance -= amount
        print(f"  Withdrew ${amount:,.2f}. New balance: ${balance:,.2f}")

    elif choice == "4":
        print("  Goodbye!")
        break                           # exit the menu loop

    else:
        print("  Invalid option — please enter 1-4.")
        continue                        # skip back to top without any extra output

print("\n" + "=" * 50)
