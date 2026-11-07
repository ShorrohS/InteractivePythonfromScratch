"""
Demo 04 — Input & Output
Phase 01: Python Fundamentals

Run: python demo-04-input-output.py
"""

print("=" * 55)
print("DEMO 04 - Input and Output")
print("=" * 55)

# --- BASIC INPUT ---
print("\n1. Basic input (always returns string):")
name = input("   Enter your name: ")
print(f"   Hello, {name}! You entered a {type(name).__name__}.")

# --- TYPE CONVERSION ON INPUT ---
print("\n2. Converting input to numbers:")
age = int(input("   Enter your age: "))
height = float(input("   Enter your height in metres (e.g. 1.75): "))
print(f"   Age: {age} ({type(age).__name__})")
print(f"   Height: {height}m ({type(height).__name__})")
print(f"   In 5 years: {age + 5}")

# --- F-STRING FORMATTING ---
print("\n3. Output formatting with f-strings:")
salary = 75000.5
score = 0.923
item_count = 42

print(f"   Basic:        {salary}")
print(f"   2 decimals:   {salary:.2f}")
print(f"   With commas:  {salary:,.2f}")
print(f"   Percentage:   {score:.1%}")
print(f"   Zero-padded:  {item_count:05d}")
print(f"   Left align:   |{name:<20}|")
print(f"   Right align:  |{name:>20}|")
print(f"   Centre:       |{name:^20}|")

# --- PRACTICAL EXAMPLE: TIP CALCULATOR ---
print("\n4. Practical: Tip Calculator")
print("   " + "-" * 35)
bill   = float(input("   Bill amount ($): "))
tip_pct = float(input("   Tip percentage (e.g. 15): "))
people  = int(input("   Number of people: "))

tip   = bill * (tip_pct / 100)
total = bill + tip
each  = total / people

print()
print(f"   Bill:        ${bill:>8.2f}")
print(f"   Tip ({tip_pct:.0f}%):   ${tip:>8.2f}")
print(f"   Total:       ${total:>8.2f}")
print(f"   Per person:  ${each:>8.2f}")
