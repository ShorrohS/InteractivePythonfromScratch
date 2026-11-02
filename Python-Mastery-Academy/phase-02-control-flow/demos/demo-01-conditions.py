"""
Demo 01 - Conditions (if/elif/else)
Phase 02: Control Flow

Run: python demo-01-conditions.py
"""

print("=" * 50)
print("DEMO 01 - Conditional Logic")
print("=" * 50)

# --- BASIC IF ---
print("\n1. Basic if statement:")
temperature = 35
if temperature > 30:
    print(f"  It's hot! ({temperature} degrees C)")

# --- IF / ELSE ---
print("\n2. if / else:")
age = 16
if age >= 18:
    print(f"  {age}: You can vote.")
else:
    print(f"  {age}: Too young to vote.")

# --- IF / ELIF / ELSE ---
print("\n3. if / elif / else:")
score = 78
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"  Score {score} -> Grade {grade}")

# --- NESTED IF ---
print("\n4. Nested if:")
income = 55000
credit_score = 720

if income >= 30000:
    print(f"  Income OK (${income:,})")
    if credit_score >= 700:
        print("  Credit OK - APPROVED!")
    else:
        print("  Poor credit - DENIED")
else:
    print("  Income too low - DENIED")

# --- TERNARY (INLINE) ---
print("\n5. Ternary / inline if:")
balance = 1500
status = "Positive" if balance >= 0 else "Negative"
print(f"  Balance ${balance:,} = {status}")

# --- CHAINED COMPARISONS ---
print("\n6. Chained comparisons:")
bmi = 22.5
if 18.5 <= bmi <= 24.9:
    category = "Normal weight"
elif bmi < 18.5:
    category = "Underweight"
elif 25 <= bmi <= 29.9:
    category = "Overweight"
else:
    category = "Obese"
print(f"  BMI {bmi} = {category}")

# --- BUSINESS EXAMPLE ---
print("\n7. Business example - Loan eligibility:")
applicants = [
    ("Alice", 30, 75000, 720),
    ("Bob", 17, 25000, 650),
    ("Carol", 22, 15000, 700),
    ("Dave", 28, 45000, 580),
]

print(f"\n  {'Name':<8} {'Age':>5} {'Income':>10} {'Credit':>7} {'Decision':>12}")
print("  " + "-" * 47)

for name, age, income, credit in applicants:
    if age < 21:
        decision = "Rejected: age"
    elif income < 25000:
        decision = "Rejected: income"
    elif credit < 620:
        decision = "Rejected: credit"
    else:
        decision = "[APPROVED]"
    print(f"  {name:<8} {age:>5} ${income:>9,} {credit:>7} {decision:>12}")
