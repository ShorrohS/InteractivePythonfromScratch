"""
Debugging Challenge 01 — Phase 01: Fundamentals
================================================

INSTRUCTIONS:
  This file contains 8 bugs.
  Find and fix every bug.
  Run the file — when all bugs are fixed, it will print "All bugs fixed!"

HINTS:
  - Read every error message carefully — it tells you the line and type of error
  - Common issues: missing quotes, wrong operators, type mismatches, indentation
  - Try to fix one bug at a time, run the file, then fix the next

DO NOT LOOK AT THE ANSWER BELOW UNTIL YOU'VE TRIED!
"""

# === BUG HUNT BEGIN ===

# Bug 1: Fix the variable name
first name = "Alice"    # hint: Python variable names can't have spaces

# Bug 2: Fix the comparison
age = 25
if age = 25:            # hint: what operator checks equality?
    print("Age is 25")

# Bug 3: Fix the string operation
score = 95
message = "Your score: " + score   # hint: can you add string + int directly?

# Bug 4: Fix the print statement
print(message

# Bug 5: Fix the division
total_minutes = 130
hours = total_minutes / 60    # should give whole hours only (no decimal)
remaining = total_minutes % 60
print(f"{hours}h {remaining}m")   # Expected: 2h 10m, not 2.1666...h

# Bug 6: Fix the f-string
name = "Bob"
print(f"Hello, {name!)   # hint: check the f-string syntax

# Bug 7: Fix the type conversion
price_str = "29.99"
price_num = int(price_str)   # hint: "29.99" is not an integer!
print(f"Price: ${price_num}")

# Bug 8: Fix the indentation
result = 100
    print(result)   # hint: this line shouldn't be indented

print("\n✅ All bugs fixed!")


# ====================================================================
# ANSWERS (don't scroll until you've tried!)
# ====================================================================
#
# Bug 1: first_name = "Alice"  (use underscore, not space)
#
# Bug 2: if age == 25:  (use == for comparison, not =)
#
# Bug 3: message = "Your score: " + str(score)
#        OR: message = f"Your score: {score}"
#
# Bug 4: print(message)  (missing closing parenthesis)
#
# Bug 5: hours = total_minutes // 60  (floor division, not regular division)
#
# Bug 6: print(f"Hello, {name}!")  (curly brace must close before !)
#
# Bug 7: price_num = float(price_str)  (use float, not int, for decimals)
#
# Bug 8: print(result)  (remove extra indentation)
#
# ====================================================================
