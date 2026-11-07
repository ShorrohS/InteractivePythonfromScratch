"""
Debugging Challenge 01 - Phase 06: Error Handling
==================================================

8 bugs related to error handling, exception types, and defensive programming.
"""

print("=" * 50)
print("DEBUGGING CHALLENGE - Error Handling")
print("=" * 50)

# BUG 1: Bare except catches everything (bad practice)
print("\nBug 1 - Bare except:")
try:
    x = int("not a number")
except:           # BUG: bare except — too broad
    print("  Caught something")

# BUG 2: Catching wrong exception type
print("\nBug 2 - Wrong exception type:")
try:
    result = [][0]    # IndexError
except KeyError:       # BUG: wrong exception type — IndexError won't be caught
    print("  Handled")

# BUG 3: Silently swallowing error
print("\nBug 3 - Silent failure:")
def get_value(d, key):
    try:
        return d[key]
    except KeyError:
        pass   # BUG: silently returns None with no indication of failure

result = get_value({"a": 1}, "b")
print(f"  Result: {result}")   # None — user has no idea why

# BUG 4: Exception variable not used
print("\nBug 4 - Ignoring exception info:")
try:
    x = 1 / 0
except ZeroDivisionError:
    print("  Math error")   # BUG: message gives no detail about what failed

# BUG 5: Custom exception missing self in __init__
print("\nBug 5 - Custom exception init:")
class PaymentError(Exception):
    def __init__(message: str, amount: float):   # BUG: missing 'self'
        super().__init__(message)
        self.amount = amount

try:
    raise PaymentError("Declined", 100.0)
except PaymentError as e:
    print(f"  Caught: {e}")

# BUG 6: finally returns overrides try return
print("\nBug 6 - return in finally:")
def calculate():
    try:
        return 42
    finally:
        return 0   # BUG: always returns 0, overrides the 42

print(f"  Result: {calculate()}")   # Should be 42

# BUG 7: Checking wrong attribute for exception type
print("\nBug 7 - Exception type check:")
try:
    value = int("abc")
except Exception as e:
    if e.name == "ValueError":    # BUG: Exception has no .name attribute — use type(e).__name__
        print("  Got a ValueError")

# BUG 8: Not re-raising in a catch-log-reraise pattern
print("\nBug 8 - Missing re-raise:")
import logging
def process(data):
    try:
        return dangerous_operation(data)
    except Exception as e:
        logging.error(f"Failed: {e}")
        # BUG: should re-raise so caller knows it failed
        # return None  ← silently hides the error

print("\n" + "=" * 50)
print("Fixed all 8 bugs?")
print("=" * 50)

# ============================================================
# ANSWERS
# ============================================================
#
# Bug 1: except ValueError:  (or except Exception as e:)
#
# Bug 2: except IndexError:  (match the actual exception raised)
#
# Bug 3: raise KeyError(f"Key '{key}' not found") or return a default
#
# Bug 4: except ZeroDivisionError as e: print(f"  Math error: {e}")
#
# Bug 5: def __init__(self, message: str, amount: float):
#
# Bug 6: Remove 'return 0' from finally (or don't use return in finally)
#
# Bug 7: if type(e).__name__ == "ValueError":
#         or better: if isinstance(e, ValueError):
#
# Bug 8: Add 'raise' after logging:
#         logging.error(f"Failed: {e}")
#         raise
