"""
Demo 03 — Python Features Preview
Phase 00: Environment Setup

PURPOSE:
  Show a sneak peek of what Python can do.
  Don't worry about understanding the code yet.
  Just RUN it and see the output.
  
  You will learn all of this in the upcoming phases.

HOW TO RUN:
  python demo-03-python-features.py
"""

print("=" * 50)
print("   PYTHON FEATURES PREVIEW")
print("=" * 50)

# ============================================================
# FEATURE 1: VARIABLES (Phase 01)
# ============================================================
print("\n📌 Feature 1: Variables")
print("-" * 30)
employee_name = "Alice Johnson"
employee_salary = 75000
department = "Engineering"
print(f"Employee: {employee_name}")
print(f"Salary:   ${employee_salary:,}")
print(f"Dept:     {department}")

# ============================================================
# FEATURE 2: MATH & CALCULATIONS (Phase 01)
# ============================================================
print("\n📌 Feature 2: Calculations")
print("-" * 30)
price = 1500
tax_rate = 0.15
discount = 0.10
discounted_price = price * (1 - discount)
tax_amount = discounted_price * tax_rate
total = discounted_price + tax_amount
print(f"Original Price: ${price:.2f}")
print(f"After 10% Discount: ${discounted_price:.2f}")
print(f"Tax (15%): ${tax_amount:.2f}")
print(f"Final Total: ${total:.2f}")

# ============================================================
# FEATURE 3: DECISIONS (Phase 02)
# ============================================================
print("\n📌 Feature 3: Decisions")
print("-" * 30)
salary = 85000
if salary >= 100000:
    tier = "Senior"
elif salary >= 70000:
    tier = "Mid-level"
elif salary >= 50000:
    tier = "Junior"
else:
    tier = "Entry level"
print(f"Salary: ${salary:,}  →  Level: {tier}")

# ============================================================
# FEATURE 4: LOOPS (Phase 02)
# ============================================================
print("\n📌 Feature 4: Loops")
print("-" * 30)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenues = [45000, 52000, 48000, 61000, 58000, 70000]
print("Monthly Revenue:")
for i, month in enumerate(months):
    bar = "█" * (revenues[i] // 5000)
    print(f"  {month}: ${revenues[i]:,}  {bar}")

# ============================================================
# FEATURE 5: LISTS & DICTS (Phase 03)
# ============================================================
print("\n📌 Feature 5: Collections")
print("-" * 30)
students = [
    {"name": "Alice", "grade": 92},
    {"name": "Bob",   "grade": 85},
    {"name": "Carol", "grade": 97},
    {"name": "Dave",  "grade": 78},
]
print("Student Report:")
for student in students:
    stars = "⭐" * (student["grade"] // 20)
    print(f"  {student['name']:<8} {student['grade']}%  {stars}")

# ============================================================
# FEATURE 6: FUNCTIONS (Phase 04)
# ============================================================
print("\n📌 Feature 6: Functions")
print("-" * 30)

def calculate_bonus(salary: float, rating: int) -> float:
    """Calculate bonus based on salary and performance rating."""
    bonus_rates = {5: 0.20, 4: 0.15, 3: 0.10, 2: 0.05, 1: 0.00}
    rate = bonus_rates.get(rating, 0)
    return salary * rate

base_salary = 80000
for rating in [5, 4, 3, 2]:
    bonus = calculate_bonus(base_salary, rating)
    print(f"  Rating {rating}/5  →  Bonus: ${bonus:,.0f}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 50)
print("  All of the above awaits you in this academy!")
print("  Start with Phase 01 → Python Fundamentals")
print("=" * 50)
