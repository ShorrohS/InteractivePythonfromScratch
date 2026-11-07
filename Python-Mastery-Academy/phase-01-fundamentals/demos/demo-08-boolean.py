"""
Demo 08 — Boolean Logic
Phase 01: Python Fundamentals

Run: python demo-08-boolean.py
"""

print("=" * 55)
print("DEMO 08 - Boolean Logic")
print("=" * 55)

# --- BASIC BOOLEANS ---
print("\n1. Boolean values:")
print(f"  True  type: {type(True).__name__}")
print(f"  False type: {type(False).__name__}")
print(f"  int(True)  = {int(True)}")
print(f"  int(False) = {int(False)}")

# --- COMPARISON PRODUCES BOOLEANS ---
print("\n2. Comparisons return booleans:")
x = 42
print(f"  x = {x}")
print(f"  x > 10:   {x > 10}")
print(f"  x == 42:  {x == 42}")
print(f"  x != 42:  {x != 42}")
print(f"  10 < x < 100: {10 < x < 100}  (chained)")

# --- LOGICAL OPERATORS ---
print("\n3. and / or / not:")
a, b = True, False
print(f"  True and False = {a and b}")
print(f"  True or  False = {a or b}")
print(f"  not True       = {not a}")
print(f"  not False      = {not b}")

# --- TRUTHY AND FALSY ---
print("\n4. Truthy and Falsy values:")
values = [0, 1, -1, 0.0, 0.1, "", "hi", [], [0], {}, {"a":1}, None]
for v in values:
    print(f"  bool({str(v):<12}) = {bool(v)}")

# --- SHORT CIRCUIT ---
print("\n5. Short-circuit evaluation:")
print("  True or  expensive_call() -> short circuits at True")
print("  False and expensive_call() -> short circuits at False")

# Safe attribute access using short-circuit
user = None
name = user and user.get("name", "")
print(f"\n  user=None, name via short-circuit: {name}")

user = {"name": "Alice", "active": True}
name = user and user.get("name", "")
print(f"  user=dict, name via short-circuit: {name}")

# --- PRACTICAL: LOGIN VALIDATOR ---
print("\n6. Practical: Login Validator")
print("   " + "-" * 30)
username = input("   Username: ").strip()
password = input("   Password: ").strip()

has_username = len(username) >= 3
has_password = len(password) >= 6
inputs_valid = has_username and has_password

print()
print(f"   Username valid (>=3 chars): {has_username}")
print(f"   Password valid (>=6 chars): {has_password}")
print(f"   Both valid: {inputs_valid}")
if inputs_valid:
    print("   Result: Can proceed to authentication.")
else:
    print("   Result: Fix input errors before continuing.")
