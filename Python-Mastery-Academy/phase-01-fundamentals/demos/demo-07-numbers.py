"""
Demo 07 — Numbers & math Module
Phase 01: Python Fundamentals

Run: python demo-07-numbers.py
"""

import math
import random

print("=" * 55)
print("DEMO 07 - Numbers and the math Module")
print("=" * 55)

# --- BUILT-IN FUNCTIONS ---
print("\n1. Built-in number functions:")
nums = [4, 7, 2, 9, 1, 5, 8, 3, 6]
print(f"  List: {nums}")
print(f"  max:  {max(nums)}")
print(f"  min:  {min(nums)}")
print(f"  sum:  {sum(nums)}")
print(f"  abs(-42): {abs(-42)}")
print(f"  round(3.14159, 2): {round(3.14159, 2)}")
print(f"  round(2.5): {round(2.5)}  (banker's rounding)")
print(f"  round(3.5): {round(3.5)}")

# --- MATH MODULE ---
print("\n2. math module:")
print(f"  math.pi    = {math.pi:.6f}")
print(f"  math.e     = {math.e:.6f}")
print(f"  math.sqrt(144)   = {math.sqrt(144)}")
print(f"  math.floor(3.9)  = {math.floor(3.9)}")
print(f"  math.ceil(3.1)   = {math.ceil(3.1)}")
print(f"  math.factorial(6)= {math.factorial(6)}")
print(f"  math.log10(1000) = {math.log10(1000)}")
print(f"  math.pow(2, 8)   = {math.pow(2, 8)}")

# --- RANDOM ---
print("\n3. random module:")
print(f"  randint(1,10):   {random.randint(1, 10)}")
print(f"  random():        {random.random():.4f}")
print(f"  choice([...]):   {random.choice(['Python','Java','C++'])}")
nums_copy = nums.copy()
random.shuffle(nums_copy)
print(f"  shuffle:         {nums_copy}")

# --- PRACTICAL: CIRCLE CALCULATOR ---
print("\n4. Circle calculator:")
r = float(input("  Enter radius: "))
area = math.pi * r ** 2
circumference = 2 * math.pi * r
print(f"  Radius:        {r}")
print(f"  Area:          {area:.4f}")
print(f"  Circumference: {circumference:.4f}")

# --- PRACTICAL: COMPOUND INTEREST ---
print("\n5. Compound interest:")
principal = float(input("  Principal ($): "))
rate      = float(input("  Annual rate (%): ")) / 100
years     = int(input("  Years: "))
total     = principal * math.pow(1 + rate, years)
interest  = total - principal
print(f"\n  Principal: ${principal:,.2f}")
print(f"  After {years} years: ${total:,.2f}")
print(f"  Interest earned: ${interest:,.2f}")
