"""
Demo 01 - try/except Basics
Phase 06: Error Handling

Run: python demo-01-try-except.py
"""

print("=" * 55)
print("DEMO 01 - try/except Error Handling")
print("=" * 55)

# --- BASIC try/except ---
print("\n1. Basic try/except:")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("  Caught ZeroDivisionError!")
    result = 0
print(f"  Result: {result}")

# --- CATCHING WITH MESSAGE ---
print("\n2. Catching the error message:")
values = ["42", "hello", "3.14", ""]
for v in values:
    try:
        n = int(v)
        print(f"  '{v}' -> {n} (int)")
    except ValueError as e:
        print(f"  '{v}' -> Error: {e}")

# --- MULTIPLE EXCEPT BLOCKS ---
print("\n3. Multiple except blocks:")
def safe_lookup(lst: list, idx: str) -> str:
    try:
        index = int(idx)
        return lst[index]
    except ValueError:
        return f"'{idx}' is not a valid index"
    except IndexError:
        return f"Index {idx} out of range (list has {len(lst)} items)"

fruits = ["apple", "banana", "cherry"]
for idx in ["1", "abc", "10", "-1"]:
    print(f"  lookup({idx}): {safe_lookup(fruits, idx)}")

# --- TRY/EXCEPT/ELSE/FINALLY ---
print("\n4. Full try/except/else/finally:")
import os
filename = "_demo_temp.txt"
open(filename, "w").close()   # create empty file

try:
    print("  Opening file...")
    with open(filename, "r") as f:
        content = f.read()
except FileNotFoundError:
    print("  File not found!")
except PermissionError:
    print("  Permission denied!")
else:
    print(f"  Success! Read {len(content)} chars.")
finally:
    print("  Cleanup: always runs.")
    if os.path.exists(filename):
        os.remove(filename)

# --- PRACTICAL: INPUT VALIDATION LOOP ---
print("\n5. Practical: validated input:")
def get_int_in_range(prompt: str, min_val: int, max_val: int) -> int:
    while True:
        try:
            value = int(input(prompt))
            if not min_val <= value <= max_val:
                raise ValueError(f"Must be {min_val}–{max_val}")
            return value
        except ValueError as e:
            print(f"  Invalid: {e}")

score = get_int_in_range("  Enter score (0-100): ", 0, 100)
print(f"  Score accepted: {score}")
