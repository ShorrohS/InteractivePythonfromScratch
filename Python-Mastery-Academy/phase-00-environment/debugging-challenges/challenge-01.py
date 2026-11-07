"""
Debugging Challenge 01 — Phase 00: Environment Setup
=====================================================

INSTRUCTIONS:
  This file contains 6 deliberate environment and Python setup mistakes.
  Each mistake represents a real error beginners encounter.

  Read the SCENARIO for each bug, identify what's wrong,
  and write the correct fix in the space provided.

  DO NOT look at the answers until you have attempted each one.

  After fixing all bugs, you should be able to run this file with:
    python challenge-01.py
"""

import sys
import os

print("=" * 50)
print("DEBUGGING CHALLENGE 01 — Environment Setup")
print("=" * 50)

# ===========================================================
# BUG 1 — Wrong Python version check
# SCENARIO: A developer wants to confirm Python 3 is running.
# This code runs without error but gives wrong output.
# ===========================================================

print("\nBug 1: Version check")
version = sys.version_info
if version.major == 2:
    print("Running Python 3")   # BUG: condition is wrong
else:
    print("Running Python 2")   # BUG: messages are swapped

# FIX: (write your corrected code here)


# ===========================================================
# BUG 2 — Path separator
# SCENARIO: Cross-platform path building.
# This works on Windows but breaks on Mac/Linux.
# ===========================================================

print("\nBug 2: Path construction")
folder = "projects"
filename = "main.py"
path = folder + "\\" + filename   # BUG: hardcoded backslash breaks on Mac/Linux

print(f"Path: {path}")

# FIX: Use the correct cross-platform method
# path = ???


# ===========================================================
# BUG 3 — Virtual environment check
# SCENARIO: Developer checks if a virtual environment is active.
# The check always prints "venv is active" even when it's not.
# ===========================================================

print("\nBug 3: Venv detection")
venv_active = os.environ.get("VIRTUAL_ENV")

if venv_active = None:            # BUG: wrong operator
    print("No virtual environment active")
else:
    print(f"Venv active: {venv_active}")

# FIX:


# ===========================================================
# BUG 4 — Reading a requirements file
# SCENARIO: Script reads requirements.txt and prints packages.
# It crashes because of a wrong file open mode.
# ===========================================================

print("\nBug 4: Reading requirements")

# Create a temp requirements file for this test
with open("temp_requirements.txt", "w") as f:
    f.write("requests==2.31.0\nflask==3.0.0\n")

with open("temp_requirements.txt", "w") as req_file:   # BUG: wrong mode
    for line in req_file:
        print(f"  Package: {line.strip()}")

# Clean up
os.remove("temp_requirements.txt")

# FIX: Change "w" to the correct mode


# ===========================================================
# BUG 5 — Environment variable access
# SCENARIO: Script reads an env variable with a default fallback.
# The fallback never triggers — it raises KeyError instead.
# ===========================================================

print("\nBug 5: Environment variable")
debug_mode = os.environ["DEBUG_MODE"]   # BUG: raises KeyError if not set
print(f"Debug mode: {debug_mode}")

# FIX: Use the safe way to access env variables with a default


# ===========================================================
# BUG 6 — Python file execution check
# SCENARIO: Code that should only run when executed directly,
# not when imported as a module. But it runs in both cases.
# ===========================================================

print("\nBug 6: Module execution guard")

# This block should ONLY run when the script is run directly
# It should NOT run if someone does: import challenge_01
def main():
    print("Main function running!")

main()   # BUG: called outside the if __name__ guard

# FIX: Add the proper guard


# ===========================================================
print("\n" + "=" * 50)
print("Fixed all 6 bugs? Run the file to confirm.")
print("=" * 50)

# ===========================================================
# ANSWER KEY (scroll past the dashes when ready)
# ===========================================================
#
# -------------------------------------------------------------------
#
# BUG 1 FIX:
#   if version.major == 3:
#       print("Running Python 3")
#   else:
#       print("Running Python 2")
#
# BUG 2 FIX:
#   path = os.path.join(folder, filename)
#   # or with pathlib:
#   from pathlib import Path
#   path = Path(folder) / filename
#
# BUG 3 FIX:
#   if venv_active is None:      # use 'is None' not '= None'
#       print("No virtual environment active")
#
# BUG 4 FIX:
#   with open("temp_requirements.txt", "r") as req_file:  # "r" for read
#
# BUG 5 FIX:
#   debug_mode = os.environ.get("DEBUG_MODE", "false")   # .get() with default
#
# BUG 6 FIX:
#   if __name__ == "__main__":
#       main()
#
# -------------------------------------------------------------------
