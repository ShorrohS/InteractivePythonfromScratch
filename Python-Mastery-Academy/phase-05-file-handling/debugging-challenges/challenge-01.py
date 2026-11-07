"""
Debugging Challenge 01 - Phase 05: File Handling
=================================================

7 bugs hidden in this file.
All relate to file modes, reading, writing, CSV, or JSON.

Find and fix each bug. The program should run and produce correct output.
"""

import csv
import json
import os

print("=" * 50)
print("DEBUGGING CHALLENGE - File Handling")
print("=" * 50)

# BUG 1: Wrong mode — trying to read a file opened for writing
print("\nBug 1 - File mode:")
with open("test.txt", "w") as f:
    content = f.read()   # BUG: mode "w" doesn't allow reading
print(f"  Content: {content}")


# BUG 2: Forgetting newline= on Windows (CSV gets blank lines)
print("\nBug 2 - CSV blank lines:")
data = [["Alice", 30], ["Bob", 25]]
with open("people.csv", "w") as f:   # BUG: missing newline=""
    writer = csv.writer(f)
    writer.writerows(data)


# BUG 3: All CSV values are strings — wrong type comparison
print("\nBug 3 - CSV type conversion:")
with open("scores.csv", "w", newline="") as f:
    csv.writer(f).writerows([["name","score"],["Alice",95],["Bob",78]])

with open("scores.csv", "r") as f:
    for row in csv.DictReader(f):
        if row["score"] > 80:    # BUG: comparing str > int
            print(f"  High scorer: {row['name']}")


# BUG 4: Append mode writing, but reading expects fresh data
print("\nBug 4 - Append accumulation:")
for i in range(3):
    with open("counter.txt", "a") as f:    # BUG: should be "w" to reset
        f.write(f"Run {i}\n")

with open("counter.txt", "r") as f:
    lines = f.readlines()
print(f"  Expected 3 lines, got: {len(lines)}")  # might be more from previous runs


# BUG 5: json.dump vs json.dumps confusion
print("\nBug 5 - JSON serialization:")
config = {"version": "1.0", "debug": False}
with open("config.json", "w") as f:
    json_text = json.dumps(config)
    f.write(json_text)   # BUG: json.dump(config, f) is simpler but this technically works
    # The actual BUG: reading it back wrong:

with open("config.json", "r") as f:
    loaded = json.dump(f)   # BUG: should be json.load(f)
print(f"  Version: {loaded['version']}")


# BUG 6: File not closed properly before reading (no 'with')
print("\nBug 6 - File not closed:")
f = open("notes.txt", "w")
f.write("Important note\n")
# BUG: forgot f.close() — data might not be flushed
with open("notes.txt", "r") as reader:
    print(f"  Content: {reader.read()}")


# BUG 7: os.path.exists check is wrong way round
print("\nBug 7 - Existence check:")
filename = "maybe_exists.txt"
if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write("Created fresh\n")

if os.path.exists(filename):    # BUG: should read if EXISTS not if not exists
    print("  File does NOT exist")
else:
    with open(filename, "r") as f:
        print(f"  Content: {f.read()}")


# Cleanup
for fn in ["test.txt","people.csv","scores.csv","counter.txt","config.json","notes.txt","maybe_exists.txt"]:
    if os.path.exists(fn):
        os.remove(fn)

print("\n" + "=" * 50)
print("Fixed all 7 bugs?")
print("=" * 50)

# ============================================================
# ANSWERS
# ============================================================
#
# Bug 1: Change "w" to "r" (and create the file first):
#   with open("test.txt", "r") as f:
#
# Bug 2: Add newline="":
#   with open("people.csv", "w", newline="") as f:
#
# Bug 3: Convert to int before comparing:
#   if int(row["score"]) > 80:
#
# Bug 4: Use "w" to reset each time:
#   with open("counter.txt", "w") as f:  (on first write)
#   or write all 3 lines in one "w" open
#
# Bug 5: json.dump vs json.load:
#   loaded = json.load(f)    (not json.dump)
#
# Bug 6: Add f.close() or use 'with':
#   with open("notes.txt", "w") as f:
#       f.write("Important note\n")
#
# Bug 7: Flip the condition:
#   if os.path.exists(filename):
#       with open(filename, "r") as f:
#           print(...)
