"""
Demo 01 - Text Files
Phase 05: File Handling

Run: python demo-01-text-files.py
"""

import os

print("=" * 55)
print("DEMO 01 - Reading and Writing Text Files")
print("=" * 55)

# --- WRITING A FILE ---
print("\n1. Writing to a file:")
with open("demo_output.txt", "w") as f:
    f.write("Line 1: Hello from Python\n")
    f.write("Line 2: File handling is easy\n")
    f.write("Line 3: Always use 'with' statement\n")
print("  Written: demo_output.txt")

# --- READING THE FILE ---
print("\n2. Reading the whole file:")
with open("demo_output.txt", "r") as f:
    content = f.read()
print(f"  Content:\n{content}")

# --- READ LINE BY LINE ---
print("3. Reading line by line:")
with open("demo_output.txt", "r") as f:
    for i, line in enumerate(f, 1):
        print(f"  Line {i}: {line.strip()}")

# --- READLINES ---
print("\n4. readlines() returns a list:")
with open("demo_output.txt", "r") as f:
    lines = f.readlines()
print(f"  Lines list: {lines}")
print(f"  Line count: {len(lines)}")

# --- APPEND MODE ---
print("\n5. Appending to a file:")
with open("demo_output.txt", "a") as f:
    f.write("Line 4: Appended later\n")
    f.write("Line 5: Without overwriting\n")

with open("demo_output.txt", "r") as f:
    print(f"  After append: {len(f.readlines())} lines")

# --- FILE MODES ---
print("\n6. File modes summary:")
modes = {
    "r":  "Read only (default) — error if not found",
    "w":  "Write — creates or overwrites",
    "a":  "Append — adds to end",
    "r+": "Read and write",
    "x":  "Create new — error if exists",
}
for mode, desc in modes.items():
    print(f"  '{mode}' — {desc}")

# --- CLEANUP ---
os.remove("demo_output.txt")
print("\n  Cleaned up demo_output.txt")
print("=" * 55)
