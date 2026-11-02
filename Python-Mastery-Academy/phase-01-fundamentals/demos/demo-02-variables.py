"""
Demo 02 — Variables
Phase 01: Python Fundamentals

Run: python demo-02-variables.py
"""

print("=" * 50)
print("DEMO 02 — Variables")
print("=" * 50)

# --- CREATING VARIABLES ---
print("\n1. Creating variables:")
name = "Alice Johnson"
age = 30
salary = 75000.50
is_employed = True

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Salary: ${salary:,.2f}")
print(f"Employed: {is_employed}")

# --- REASSIGNMENT ---
print("\n2. Variable reassignment:")
score = 0
print(f"Initial score: {score}")

score = 50
print(f"After assignment: {score}")

score = score + 10
print(f"After adding 10: {score}")

# --- AUGMENTED ASSIGNMENT ---
print("\n3. Augmented assignment operators:")
counter = 100
print(f"Start: {counter}")
counter += 10; print(f"After +=10: {counter}")
counter -= 5;  print(f"After -=5:  {counter}")
counter *= 2;  print(f"After *=2:  {counter}")
counter //= 3; print(f"After //=3: {counter}")

# --- MULTIPLE ASSIGNMENT ---
print("\n4. Multiple assignment:")
x, y, z = 10, 20, 30
print(f"x={x}, y={y}, z={z}")

a = b = c = 0
print(f"a={a}, b={b}, c={c}")

# --- SWAP ---
print("\n5. Swapping values:")
p = "first"
q = "second"
print(f"Before: p={p}, q={q}")
p, q = q, p
print(f"After:  p={p}, q={q}")

# --- TYPE CHECKING ---
print("\n6. Checking types:")
values = [name, age, salary, is_employed]
for v in values:
    print(f"  {str(v):<20} is type: {type(v).__name__}")

print("\n" + "=" * 50)
