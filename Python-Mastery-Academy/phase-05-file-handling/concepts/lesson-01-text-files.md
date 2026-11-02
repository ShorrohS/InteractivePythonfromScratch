# Lesson 01 — Text Files

**Phase:** 05 — File Handling | **Time:** ~30 min

---

## Part 1: Opening Files

The `open()` function opens a file. Always use it with `with`:

```python
# CORRECT — with statement (context manager)
with open("hello.txt", "w") as f:
    f.write("Hello, World!")
# File is automatically closed here

# WRONG — manual close (easy to forget)
f = open("hello.txt", "r")
content = f.read()
f.close()   # If you forget this, data may be lost or corrupted
```

**Why `with`?** It guarantees the file is closed even if an error occurs.

---

## Part 2: Writing Files

```python
# Write (overwrites entire file)
with open("notes.txt", "w") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.write("Line 3\n")

# Writelines (write list of strings)
lines = ["Alice\n", "Bob\n", "Carol\n"]
with open("names.txt", "w") as f:
    f.writelines(lines)

# Append (add to end of file)
with open("notes.txt", "a") as f:
    f.write("Line 4\n")
    f.write("Line 5\n")
```

---

## Part 3: Reading Files

```python
# read() — entire file as one string
with open("notes.txt", "r") as f:
    content = f.read()
    print(content)

# readline() — one line at a time
with open("notes.txt", "r") as f:
    first_line = f.readline()
    second_line = f.readline()

# readlines() — list of all lines
with open("notes.txt", "r") as f:
    lines = f.readlines()   # ['Line 1\n', 'Line 2\n', ...]
    # Strip newlines:
    clean_lines = [line.strip() for line in lines]

# Iterate line by line (most memory-efficient)
with open("notes.txt", "r") as f:
    for line in f:
        print(line.strip())
```

---

## Part 4: File Paths

```python
import os

# Current directory
print(os.getcwd())

# Check if file exists
if os.path.exists("notes.txt"):
    print("File exists")

# Join paths safely (works on all OS)
path = os.path.join("data", "notes.txt")
print(path)   # data/notes.txt  or  data\notes.txt

# Get file info
print(os.path.basename("data/notes.txt"))   # notes.txt
print(os.path.dirname("data/notes.txt"))    # data
print(os.path.splitext("notes.txt"))        # ('notes', '.txt')

# Create directory
os.makedirs("data/exports", exist_ok=True)
```

---

## Part 5: Business Example — Journal App

```python
"""Simple journal app — reads/writes text files."""

import os
from datetime import datetime

JOURNAL_FILE = "journal.txt"

def add_entry(text: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(JOURNAL_FILE, "a") as f:
        f.write(f"\n[{timestamp}]\n{text}\n{'─'*40}\n")
    print("✅ Entry saved.")

def view_entries() -> None:
    if not os.path.exists(JOURNAL_FILE):
        print("No journal entries yet.")
        return
    with open(JOURNAL_FILE, "r") as f:
        print(f.read())

def count_entries() -> int:
    if not os.path.exists(JOURNAL_FILE):
        return 0
    with open(JOURNAL_FILE, "r") as f:
        return f.read().count("[20")   # Count timestamp headers

# Usage
print("MY JOURNAL")
print("─" * 30)
print("[1] Write Entry  [2] View All  [3] Exit")

while True:
    choice = input("\nOption: ")
    if choice == "1":
        entry = input("Write your entry:\n> ")
        add_entry(entry)
    elif choice == "2":
        view_entries()
    elif choice == "3":
        print(f"Total entries: {count_entries()}")
        break
```

---

## Part 6: Common Mistakes

```python
# Mistake 1: FileNotFoundError
with open("nonexistent.txt", "r") as f:    # Error if file doesn't exist
    content = f.read()

# Fix: check first
import os
if os.path.exists("file.txt"):
    with open("file.txt", "r") as f:
        content = f.read()

# Mistake 2: Overwriting instead of appending
with open("log.txt", "w") as f:    # "w" DELETES existing content!
    f.write("New entry")

# Fix: use "a" for append
with open("log.txt", "a") as f:
    f.write("New entry\n")

# Mistake 3: Forgetting \n
with open("names.txt", "w") as f:
    f.write("Alice")    # No newline
    f.write("Bob")      # Appears on SAME line: AliceBob

# Fix:
    f.write("Alice\n")
    f.write("Bob\n")
```

---

## Practice Exercises

1. Write a program that creates a file, writes 5 lines to it, then reads and prints it back.

2. Write a logging function that appends timestamped messages to `app.log`.

3. Read a file line by line and count the total number of words.

4. Create a contacts file: each line is "Name,Phone". Write 3 contacts, then read and print them formatted.

5. What's wrong?
   ```python
   with open("data.txt", "r") as f:
       f.write("Hello")
   ```

---

## Next Lesson

**[Lesson 02 → CSV Files](lesson-02-csv.md)**
