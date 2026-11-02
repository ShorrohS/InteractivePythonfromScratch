"""
Demo 01 — Functions
Phase 04: Functions

Run: python demo-01-functions.py
"""

print("=" * 55)
print("DEMO 01 — Python Functions")
print("=" * 55)

# ─── BASIC FUNCTION ───────────────────────────────────────
print("\n1. Basic function:")

def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"

print(f"  {greet('Alice')}")
print(f"  {greet('World')}")

# ─── PARAMETERS ───────────────────────────────────────────
print("\n2. Parameters and return values:")

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate Body Mass Index."""
    return weight_kg / (height_m ** 2)

def bmi_category(bmi: float) -> str:
    """Return BMI category."""
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal"
    elif bmi < 30: return "Overweight"
    else: return "Obese"

bmi = calculate_bmi(70, 1.75)
print(f"  BMI: {bmi:.1f} ({bmi_category(bmi)})")

# ─── DEFAULT ARGUMENTS ────────────────────────────────────
print("\n3. Default arguments:")

def create_email(first: str, last: str, domain: str = "company.com") -> str:
    """Create a corporate email address."""
    return f"{first.lower()}.{last.lower()}@{domain}"

print(f"  {create_email('Alice', 'Johnson')}")
print(f"  {create_email('Bob', 'Smith', 'gmail.com')}")

# ─── MULTIPLE RETURN VALUES ───────────────────────────────
print("\n4. Multiple return values:")

def min_max_avg(numbers: list[float]) -> tuple[float, float, float]:
    """Return minimum, maximum, and average of a list."""
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

scores = [85, 92, 78, 95, 88]
low, high, avg = min_max_avg(scores)
print(f"  Scores: {scores}")
print(f"  Min: {low}, Max: {high}, Avg: {avg:.1f}")

# ─── *args ────────────────────────────────────────────────
print("\n5. *args — variable arguments:")

def add(*numbers: float) -> float:
    """Add any number of values."""
    return sum(numbers)

print(f"  add(1, 2):             {add(1, 2)}")
print(f"  add(1, 2, 3):          {add(1, 2, 3)}")
print(f"  add(10, 20, 30, 40):   {add(10, 20, 30, 40)}")

# ─── **kwargs ─────────────────────────────────────────────
print("\n6. **kwargs — keyword arguments:")

def display_profile(**info) -> None:
    """Display a profile from any keyword arguments."""
    print("  Profile:")
    for key, value in info.items():
        print(f"    {key.title()}: {value}")

display_profile(name="Alice", age=30, city="NYC", role="Engineer")

# ─── LAMBDA ───────────────────────────────────────────────
print("\n7. Lambda functions:")

square = lambda x: x ** 2
is_even = lambda n: n % 2 == 0
add_tax = lambda price, rate=0.15: price * (1 + rate)

print(f"  square(7):          {square(7)}")
print(f"  is_even(12):        {is_even(12)}")
print(f"  add_tax(100):       ${add_tax(100):.2f}")

# Sort by lambda
employees = [("Alice", 85000), ("Bob", 65000), ("Carol", 92000)]
sorted_by_salary = sorted(employees, key=lambda e: e[1], reverse=True)
print(f"\n  Sorted by salary:")
for name, salary in sorted_by_salary:
    print(f"    {name}: ${salary:,}")

# ─── RECURSION ────────────────────────────────────────────
print("\n8. Recursion:")

def factorial(n: int) -> int:
    """Calculate n! recursively."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

for i in range(6):
    print(f"  {i}! = {factorial(i)}")

print("\n" + "=" * 55)
