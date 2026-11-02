"""
Demo 01 — Hello World
Phase 00: Environment Setup

PURPOSE:
  Verify Python is installed and working.
  Learn the print() function.

HOW TO RUN:
  python demo-01-hello-world.py

EXPECTED OUTPUT:
  Hello, World!
  My name is Python.
  I am ready to learn.
"""

# ============================================================
# EXAMPLE 1: The classic Hello World
# ============================================================

print("Hello, World!")


# ============================================================
# EXAMPLE 2: Print multiple lines
# ============================================================

print("My name is Python.")
print("I am ready to learn.")


# ============================================================
# EXAMPLE 3: Print with numbers and math
# ============================================================

print(42)
print(3.14)
print(2 + 2)
print(10 * 5)


# ============================================================
# EXAMPLE 4: Print with a separator (empty line between)
# ============================================================

print("Line 1")
print()           # Empty print() creates a blank line
print("Line 2")


# ============================================================
# EXAMPLE 5: Print with sep and end parameters
# ============================================================

# sep = what goes between multiple items (default is a space)
print("Python", "is", "awesome")           # Python is awesome
print("Python", "is", "awesome", sep="-")  # Python-is-awesome
print("Python", "is", "awesome", sep="")   # Pythonisawesome

# end = what goes at the end (default is newline \n)
print("Hello", end=" ")
print("World!")  # prints: Hello World!  (on same line)


# ============================================================
# EXAMPLE 6: Print special characters
# ============================================================

print("Tab:\tHello")         # \t = tab
print("Newline:\nHello")     # \n = new line inside string
print("Backslash: \\")      # \\ = literal backslash
print("Quote: \"Hello\"")   # \" = literal quote


# ============================================================
# EXAMPLE 7: Print a decorative border
# ============================================================

print("=" * 40)
print("  Welcome to Python Mastery Academy!")
print("=" * 40)


# ============================================================
# RUN THIS FILE TO CONFIRM PYTHON WORKS
# ============================================================
print("\n[OK] Python is working correctly!")
print("[OK] You are ready to start learning.")
