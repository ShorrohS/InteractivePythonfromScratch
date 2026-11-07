"""
Demo 03 - Scope, Closures & Lambda
Phase 04: Functions

Run: python demo-03-scope-lambda.py
"""

print("=" * 55)
print("DEMO 03 - Scope, Closures and Lambda")
print("=" * 55)

# --- SCOPE LEGB ---
print("\n1. LEGB Scope:")

x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(f"  inner sees: '{x}'")
    inner()
    print(f"  outer sees: '{x}'")

outer()
print(f"  module sees: '{x}'")

# --- CLOSURES ---
print("\n2. Closures - factory functions:")

def make_multiplier(factor: float):
    def multiply(n: float) -> float:
        return n * factor    # captures 'factor' from enclosing scope
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
ten_pct = make_multiplier(0.10)

print(f"  double(25)  = {double(25)}")
print(f"  triple(7)   = {triple(7)}")
print(f"  10% of 500  = {ten_pct(500)}")

# Configurable tax calculator
uk_vat = make_multiplier(0.20)
us_tax = make_multiplier(0.085)
print(f"  UK VAT on 100  = {uk_vat(100):.2f}")
print(f"  US tax on 100  = {us_tax(100):.2f}")

# --- LAMBDA BASICS ---
print("\n3. Lambda basics:")

sq    = lambda x: x ** 2
add   = lambda a, b: a + b
greet = lambda name, msg="Hello": f"{msg}, {name}!"

print(f"  sq(9):              {sq(9)}")
print(f"  add(3, 7):          {add(3, 7)}")
print(f"  greet('Alice'):     {greet('Alice')}")
print(f"  greet('Bob','Hi'):  {greet('Bob', 'Hi')}")

# --- SORTED WITH LAMBDA ---
print("\n4. sorted() with lambda:")

employees = [
    {"name": "Carol", "dept": "Eng",   "salary": 90000},
    {"name": "Alice", "dept": "Sales", "salary": 75000},
    {"name": "Bob",   "dept": "Eng",   "salary": 85000},
    {"name": "Dave",  "dept": "Sales", "salary": 70000},
]

by_salary  = sorted(employees, key=lambda e: e["salary"], reverse=True)
by_dept_sal = sorted(employees, key=lambda e: (e["dept"], -e["salary"]))

print("  By salary (desc):")
for e in by_salary:
    print(f"    {e['name']:<8} ${e['salary']:,}")

print("  By dept then salary:")
for e in by_dept_sal:
    print(f"    {e['dept']:<6} {e['name']:<8} ${e['salary']:,}")

# --- MAP AND FILTER ---
print("\n5. map() and filter():")

prices = [100, 250, 50, 175, 320, 80]
print(f"  Prices: {prices}")

with_tax   = list(map(lambda p: round(p * 1.10, 2), prices))
expensive  = list(filter(lambda p: p > 150, prices))
discounted = list(map(lambda p: round(p * 0.85, 2),
                      filter(lambda p: p > 150, prices)))

print(f"  +10% tax:    {with_tax}")
print(f"  Over $150:   {expensive}")
print(f"  15% off >150:{discounted}")
