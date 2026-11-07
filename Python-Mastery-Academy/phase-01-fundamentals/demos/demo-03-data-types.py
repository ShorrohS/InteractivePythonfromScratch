"""
Demo 03 — Data Types
Phase 01: Python Fundamentals

Run: python demo-03-data-types.py
"""

print("=" * 55)
print("DEMO 03 - Python Data Types")
print("=" * 55)

# --- INT ---
print("\n1. Integer (int) - whole numbers:")
age = 30
population = 8_000_000_000
negative = -42
print(f"  age = {age}             type: {type(age).__name__}")
print(f"  population = {population:,}  type: {type(population).__name__}")
print(f"  negative = {negative}        type: {type(negative).__name__}")

# --- FLOAT ---
print("\n2. Float - decimal numbers:")
price = 19.99
pi = 3.14159
rate = 0.075
print(f"  price = {price}        type: {type(price).__name__}")
print(f"  pi = {pi}        type: {type(pi).__name__}")
print(f"  0.1 + 0.2 = {0.1 + 0.2}  (floating point quirk!)")
import math
print(f"  Fixed: {round(0.1 + 0.2, 2)}")

# --- STRING ---
print("\n3. String (str) - text:")
name = "Alice Johnson"
city = 'New York'
multi = """Line 1
Line 2"""
print(f"  name = '{name}'   type: {type(name).__name__}")
print(f"  length = {len(name)}")
print(f"  multi-line: {repr(multi)}")

# --- BOOLEAN ---
print("\n4. Boolean (bool) - True or False:")
is_active = True
is_deleted = False
print(f"  is_active = {is_active}      type: {type(is_active).__name__}")
print(f"  10 > 5 = {10 > 5}")
print(f"  10 == 5 = {10 == 5}")

# --- NONE ---
print("\n5. NoneType - absence of value:")
result = None
print(f"  result = {result}       type: {type(result).__name__}")
print(f"  result is None: {result is None}")

# --- TYPE CONVERSION ---
print("\n6. Type conversion:")
print(f"  int('42')   = {int('42')}    ({type(int('42')).__name__})")
print(f"  float('3.14') = {float('3.14')} ({type(float('3.14')).__name__})")
print(f"  str(100)    = '{str(100)}'   ({type(str(100)).__name__})")
print(f"  bool(0)     = {bool(0)}  ({type(bool(0)).__name__})")
print(f"  bool('')    = {bool('')}  (empty string is falsy)")
print(f"  bool('hi')  = {bool('hi')}  (non-empty is truthy)")

# --- BUSINESS EXAMPLE ---
print("\n7. Business record - all types together:")
product_id   = 10042        # int
product_name = "Laptop Pro" # str
price        = 1299.99      # float
in_stock     = True         # bool
discount     = None         # NoneType

print(f"  ID:       {product_id}  ({type(product_id).__name__})")
print(f"  Name:     {product_name}  ({type(product_name).__name__})")
print(f"  Price:    ${price}  ({type(price).__name__})")
print(f"  In stock: {in_stock}  ({type(in_stock).__name__})")
print(f"  Discount: {discount}  ({type(discount).__name__})")
