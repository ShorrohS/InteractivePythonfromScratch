"""
Demo 01 — Hello World Variations
Phase 01: Python Fundamentals

Run: python demo-01-hello-world.py
"""

print("=" * 50)
print("DEMO 01 — Hello World Variations")
print("=" * 50)

# Basic print
print("\n1. Basic print:")
print("Hello, World!")

# Print with numbers
print("\n2. Print numbers and expressions:")
print(42)
print(3.14)
print(2 + 2)

# Print multiple items
print("\n3. Print multiple items:")
print("Name:", "Alice", "Age:", 30)

# Custom separator
print("\n4. Custom separator:")
print("2024", "01", "15", sep="-")     # 2024-01-15
print("Python", "is", "fun", sep=" | ")

# Custom end
print("\n5. Custom end character:")
print("Loading", end="")
print(".", end="")
print(".", end="")
print(".", end="")
print(" Done!")   # on same line: Loading... Done!

# Escape characters
print("\n6. Escape characters:")
print("Line 1\nLine 2\nLine 3")
print("Col1\tCol2\tCol3")

# Comments demo
print("\n7. This line has code + comment")  # This is ignored
# The next line is entirely a comment — won't print anything

print("\n" + "=" * 50)
print("All print() variations demonstrated!")
