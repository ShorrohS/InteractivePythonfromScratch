"""
Debugging Challenge 01 — Phase 02: Control Flow
================================================

INSTRUCTIONS:
  7 bugs are hidden in this file.
  All relate to control flow: if/else, loops, conditions.
  Find and fix each one.
  When all are fixed, the program runs and prints correct output.

Run: python challenge-01.py
"""

print("=" * 50)
print("DEBUGGING CHALLENGE 01 - Control Flow Bugs")
print("=" * 50)

# ============================================================
# BUG 1 — Wrong indentation breaks the if/else
# ============================================================
score = 75
print("\nBug 1 - Grade:")
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
    elif score >= 70:    # BUG: elif at wrong level
        grade = "C"
else:
    grade = "F"
print(f"  Grade: {grade}")


# ============================================================
# BUG 2 — Infinite loop: counter never changes
# ============================================================
print("\nBug 2 - Countdown:")
count = 5
while count > 0:
    print(f"  {count}")
    # BUG: count is never decremented — infinite loop!
print("  Blast off!")


# ============================================================
# BUG 3 — Off-by-one: should print 1 through 10 inclusive
# ============================================================
print("\nBug 3 - Numbers 1 to 10:")
for i in range(1, 10):    # BUG: stops at 9, should be range(1, 11)
    print(f"  {i}", end=" ")
print()


# ============================================================
# BUG 4 — Wrong comparison operator (assignment vs equality)
# ============================================================
print("\nBug 4 - Check temperature:")
temperature = 38
if temperature = 37:     # BUG: should be ==
    print("  Normal")
else:
    print("  Check with doctor")


# ============================================================
# BUG 5 — break placed incorrectly (exits too early)
# ============================================================
print("\nBug 5 - Find first number > 50:")
numbers = [10, 25, 55, 30, 70, 45]
for n in numbers:
    break               # BUG: break is before the condition check
    if n > 50:
        print(f"  First number > 50: {n}")


# ============================================================
# BUG 6 — Logic error: AND should be OR
# ============================================================
print("\nBug 6 - Weekend check:")
day = "Saturday"
if day == "Saturday" and day == "Sunday":   # BUG: can't be both at once — use 'or'
    print(f"  {day} is a weekend")
else:
    print(f"  {day} is a weekday")


# ============================================================
# BUG 7 — for/else used incorrectly
# ============================================================
print("\nBug 7 - Search for 42:")
nums = [10, 20, 30, 40, 50]
for n in nums:
    if n == 42:
        print("  Found 42!")
        break
    else:           # BUG: else belongs to for loop, not inside it
        print("  42 not found.")


print("\n" + "=" * 50)
print("Fixed all 7 bugs? The output should be logical.")
print("=" * 50)

# ============================================================
# ANSWER KEY
# ============================================================
#
# Bug 1: Remove extra indent from elif:
#   elif score >= 70:
#       grade = "C"
#
# Bug 2: Add count -= 1 inside the while loop
#
# Bug 3: range(1, 11) to include 10
#
# Bug 4: if temperature == 37: (use == not =)
#
# Bug 5: Move break after the if block:
#   for n in numbers:
#       if n > 50:
#           print(...)
#           break
#
# Bug 6: if day == "Saturday" or day == "Sunday":
#        (OR not AND — a day can't equal both at once)
#
# Bug 7: Move else to for loop level (not inside the for body):
#   for n in nums:
#       if n == 42:
#           print("Found 42!")
#           break
#   else:
#       print("42 not found.")
