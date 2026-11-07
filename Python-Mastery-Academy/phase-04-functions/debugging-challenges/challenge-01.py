"""
Debugging Challenge 01 - Phase 04: Functions
=============================================

8 bugs hidden in this file.
All relate to function definitions, parameters, scope, or recursion.

Find and fix every bug. Run the file to confirm.
"""

print("=" * 50)
print("DEBUGGING CHALLENGE - Functions")
print("=" * 50)

# BUG 1: Function never returns anything
print("\nBug 1 - Missing return:")
def square(n):
    result = n ** 2
    # BUG: forgot to return result

print(f"  square(5) = {square(5)}")   # Should print 25


# BUG 2: Wrong parameter order with default
print("\nBug 2 - Default parameter order:")
# BUG: default parameter before non-default (SyntaxError)
def greet(greeting="Hello", name):
    return f"{greeting}, {name}!"

print(f"  {greet('Alice')}")


# BUG 3: Mutable default argument
print("\nBug 3 - Mutable default:")
def add_score(score, scores=[]):   # BUG: mutable default
    scores.append(score)
    return scores

result1 = add_score(90)
result2 = add_score(85)   # Should be [85], not [90, 85]
print(f"  result1: {result1}")
print(f"  result2: {result2}")


# BUG 4: Trying to modify global without declaring it
print("\nBug 4 - Global scope:")
total = 0

def add_to_total(amount):
    total += amount    # BUG: UnboundLocalError

add_to_total(100)
print(f"  total = {total}")


# BUG 5: Wrong variable name (case sensitivity)
print("\nBug 5 - Case sensitivity:")
def format_name(first_name, last_name):
    return f"{First_Name} {Last_Name}"  # BUG: wrong case

print(f"  {format_name('alice', 'johnson')}")


# BUG 6: Missing base case in recursion
print("\nBug 6 - Missing base case:")
def countdown(n):
    print(n)
    countdown(n - 1)    # BUG: no base case — runs forever

countdown(3)    # Should print 3, 2, 1, Done!


# BUG 7: args captured as tuple but used as int
print("\nBug 7 - *args usage:")
def total(*amounts):
    return amounts * 2    # BUG: multiplies tuple, should sum amounts

print(f"  total(10, 20, 30) = {total(10, 20, 30)}")   # Should be 60


# BUG 8: Lambda with wrong syntax
print("\nBug 8 - Lambda syntax:")
multiply = lambda x y: x * y    # BUG: missing comma between parameters

print(f"  multiply(4, 5) = {multiply(4, 5)}")


print("\n" + "=" * 50)
print("Fixed all 8 bugs?")
print("=" * 50)

# ============================================================
# ANSWERS
# ============================================================
#
# Bug 1: Add: return result
#
# Bug 2: Move default to end:
#   def greet(name, greeting="Hello"):
#
# Bug 3: Use None sentinel:
#   def add_score(score, scores=None):
#       if scores is None: scores = []
#
# Bug 4: Declare global or use return:
#   def add_to_total(amount):
#       global total
#       total += amount
#
# Bug 5: Match parameter names:
#   return f"{first_name} {last_name}"
#
# Bug 6: Add base case:
#   def countdown(n):
#       if n <= 0:
#           print("Done!")
#           return
#       print(n)
#       countdown(n - 1)
#
# Bug 7: Use sum():
#   return sum(amounts)
#
# Bug 8: Add comma:
#   multiply = lambda x, y: x * y
