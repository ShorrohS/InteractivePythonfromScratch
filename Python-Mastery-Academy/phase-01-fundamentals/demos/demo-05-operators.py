"""
Demo 05 — Operators
Phase 01: Python Fundamentals

Run: python demo-05-operators.py
"""

print("=" * 55)
print("DEMO 05 - Python Operators")
print("=" * 55)

a, b = 17, 5

# --- ARITHMETIC ---
print("\n1. Arithmetic operators:")
print(f"  a={a}, b={b}")
print(f"  a + b  = {a + b}")
print(f"  a - b  = {a - b}")
print(f"  a * b  = {a * b}")
print(f"  a / b  = {a / b:.4f}  (always float)")
print(f"  a // b = {a // b}   (floor division)")
print(f"  a % b  = {a % b}    (remainder/modulo)")
print(f"  a ** b = {a ** b} (exponentiation)")

# --- ASSIGNMENT ---
print("\n2. Assignment operators:")
x = 100
print(f"  Start: x = {x}")
x += 15;  print(f"  x += 15  -> {x}")
x -= 5;   print(f"  x -= 5   -> {x}")
x *= 2;   print(f"  x *= 2   -> {x}")
x //= 3;  print(f"  x //= 3  -> {x}")
x %= 10;  print(f"  x %= 10  -> {x}")

# --- COMPARISON ---
print("\n3. Comparison operators (return bool):")
age = 25
print(f"  age = {age}")
print(f"  age == 25: {age == 25}")
print(f"  age != 30: {age != 30}")
print(f"  age > 18:  {age > 18}")
print(f"  age < 18:  {age < 18}")
print(f"  age >= 25: {age >= 25}")
print(f"  18 <= age <= 65: {18 <= age <= 65}  (chained)")

# --- LOGICAL ---
print("\n4. Logical operators:")
income, credit = 50000, 720
print(f"  income={income}, credit={credit}")
print(f"  income>30000 and credit>700: {income>30000 and credit>700}")
print(f"  income<20000 or credit>700:  {income<20000 or credit>700}")
print(f"  not (income < 20000):        {not (income < 20000)}")

# --- PRACTICAL: MODULO USES ---
print("\n5. Practical modulo uses:")
print(f"  Is 24 even?  {24 % 2 == 0}")
print(f"  Is 7 odd?    {7 % 2 != 0}")

minutes = 137
print(f"\n  137 minutes = {minutes // 60}h {minutes % 60}m")

for i in range(1, 11):
    if i % 3 == 0 and i % 5 == 0:
        label = "FizzBuzz"
    elif i % 3 == 0:
        label = "Fizz"
    elif i % 5 == 0:
        label = "Buzz"
    else:
        label = str(i)
    print(f"  {i:2d} -> {label}")
