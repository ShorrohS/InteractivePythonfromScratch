# Phase 05 — Beginner Solutions: File Handling

---

## Q1. Create and read a file

```python
# Write
with open("hello.txt", "w") as f:
    f.write("Hello, World!\n")

# Read
with open("hello.txt", "r") as f:
    content = f.read()
print(content)

import os
os.remove("hello.txt")   # cleanup
```

---

## Q2. Append 5 lines and count

```python
# Append 5 lines
with open("log.txt", "w") as f:    # use "w" first to start fresh
    for i in range(1, 6):
        f.write(f"Log line {i}\n")

# Read and count
with open("log.txt", "r") as f:
    lines = f.readlines()
print(f"Line count: {len(lines)}")  # 5
```

---

## Q3. Mode error

The code opens the file in `"r"` (read-only) mode but tries to write.
It raises: `io.UnsupportedOperation: not writable`

Fix: change mode to `"w"`:
```python
with open("data.txt", "w") as f:
    f.write("Hello")
```

---

## Q4. file_exists function

```python
import os

def file_exists(filename: str) -> bool:
    return os.path.exists(filename)
    # or: from pathlib import Path; return Path(filename).exists()

print(file_exists("hello.txt"))   # True or False
```

---

## Q5. Read, sort, and print names

```python
import os

# Create the file first
with open("names.txt", "w") as f:
    f.write("Charlie\nAlice\nBob\nDiana\nEve\n")

# Read and sort
with open("names.txt", "r") as f:
    names = [line.strip() for line in f if line.strip()]

for name in sorted(names):
    print(name)

os.remove("names.txt")
```

---

## Q6. count_lines function

```python
def count_lines(filename: str) -> int:
    with open(filename, "r") as f:
        return sum(1 for _ in f)
```

---

## Q7. "w" vs "a"

| Mode | Behaviour |
|------|-----------|
| `"w"` | Creates new file or **erases** existing file completely |
| `"a"` | Creates new file or **appends** to end of existing file |

Use `"w"` when you want to start fresh.
Use `"a"` when you want to add to existing content (logs, journals).

---

## Q8. save_list function

```python
def save_list(filename: str, items: list) -> None:
    with open(filename, "w") as f:
        for item in items:
            f.write(str(item) + "\n")
```

---

## Q9. load_list function

```python
def load_list(filename: str) -> list:
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]
```

---

## Q10. Fix with 'with' statement

```python
# Wrong — no automatic close
f = open("data.txt", "r")
content = f.read()
# f might never close if an error occurs

# Correct — auto-closes even on error
with open("data.txt", "r") as f:
    content = f.read()
# f is closed here, guaranteed
print(content)
```
