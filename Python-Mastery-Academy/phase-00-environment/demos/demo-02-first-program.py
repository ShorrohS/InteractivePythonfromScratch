"""
Demo 02 — First Real Program
Phase 00: Environment Setup

PURPOSE:
  Show a slightly more complex program.
  Introduce variables and user input.
  Demonstrate Python reads top to bottom.

HOW TO RUN:
  python demo-02-first-program.py
"""

# ============================================================
# A PROGRAM THAT ASKS FOR YOUR NAME AND GREETS YOU
# ============================================================

print("=" * 45)
print("   PYTHON MASTERY ACADEMY — Welcome!")
print("=" * 45)

# input() asks the user to type something
# The text inside "" is shown to the user
# What they type is stored in the variable 'name'
name = input("\nWhat is your name? ")

# We use the name they gave us
print(f"\nHello, {name}! 👋")
print(f"Welcome to your Python learning journey.")
print()

# Ask another question
goal = input("What do you want to build with Python? ")
print(f"\nExcellent! Let's help you build: {goal}")
print()

# Show a motivational message
print("Here's what you're about to learn:")
print("  Phase 00 → Environment Setup (you're here!)")
print("  Phase 01 → Python Fundamentals")
print("  Phase 02 → Control Flow")
print("  Phase 03 → Collections")
print("  ... and 17 more phases!")
print()
print(f"Let's start, {name}. Python awaits. 🐍")
print("=" * 45)
