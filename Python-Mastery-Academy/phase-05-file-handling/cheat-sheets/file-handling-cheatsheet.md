# ⚡ Phase 05 Cheat Sheet — File Handling

---

## File Modes

| Mode | Meaning | Creates? | Clears? |
|------|---------|---------|---------|
| `"r"` | Read only | No | No |
| `"w"` | Write | Yes | Yes |
| `"a"` | Append | Yes | No |
| `"r+"` | Read + write | No | No |
| `"x"` | Create new | Yes (error if exists) | — |
| `"rb"` | Read binary | No | No |

---

## Text Files

```python
# Write
with open("file.txt", "w", encoding="utf-8") as f:
    f.write("line 1\n")
    f.writelines(["a\n", "b\n"])

# Read all
with open("file.txt", "r") as f:
    content  = f.read()         # single string
    lines    = f.readlines()    # list of lines (with \n)
    for line in f:              # iterate line by line
        clean = line.strip()

# Append
with open("file.txt", "a") as f:
    f.write("new line\n")
```

---

## CSV Files

```python
import csv

# Write
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "age"])   # header
    writer.writerows([["Alice",30],["Bob",25]])

# Write dicts
with open("data.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows([{"name": "Alice", "age": 30}])

# Read
with open("data.csv", "r") as f:
    reader = csv.reader(f)
    header = next(reader)           # skip header row
    rows   = list(reader)

# Read as dicts
with open("data.csv", "r") as f:
    records = list(csv.DictReader(f))
    # All values are strings — convert as needed:
    # float(row["price"]), int(row["qty"])
```

---

## JSON Files

```python
import json

# Write
with open("data.json", "w") as f:
    json.dump(my_data, f, indent=2)

# Read
with open("data.json", "r") as f:
    data = json.load(f)

# String ↔ object
json_str = json.dumps(data)        # → string
data     = json.loads(json_str)    # string → object
```

---

## Paths

```python
from pathlib import Path
import os

# Build path
p = Path("data") / "exports" / "report.csv"

# Info
p.name      # "report.csv"
p.stem      # "report"
p.suffix    # ".csv"
p.parent    # Path("data/exports")

# Check
p.exists()
p.is_file()
p.is_dir()

# Create dir
Path("output").mkdir(parents=True, exist_ok=True)

# List files
for f in Path(".").glob("*.csv"):     # one level
    print(f)
for f in Path(".").rglob("*.py"):     # recursive
    print(f)

# Current dir / home
Path.cwd()
Path.home()
```

---

## Safe Patterns

```python
import os
from pathlib import Path

# Safe read with default
def read_file(path, default=""):
    if not Path(path).exists():
        return default
    with open(path, encoding="utf-8") as f:
        return f.read()

# Ensure directory exists before writing
def write_to(filepath, content):
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
```
