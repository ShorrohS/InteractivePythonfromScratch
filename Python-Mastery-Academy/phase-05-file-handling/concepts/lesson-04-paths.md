# Lesson 04 — File Paths & the os / pathlib Modules

**Phase:** 05 — File Handling | **Time:** ~25 min

---

## Part 1: Why Paths Matter

Hardcoded paths break on other machines:

```python
# WRONG — only works on your machine
open("C:\\Users\\Alice\\Desktop\\data.csv")

# CORRECT — works everywhere
from pathlib import Path
path = Path.home() / "Desktop" / "data.csv"
```

---

## Part 2: pathlib — Modern Path Handling

```python
from pathlib import Path

# Current directory
here = Path.cwd()
home = Path.home()

# Build paths with /
data_dir  = Path("data")
csv_file  = data_dir / "sales.csv"
log_file  = Path("logs") / "app.log"

# Path info
p = Path("reports/sales/q4.csv")
print(p.name)       # q4.csv
print(p.stem)       # q4
print(p.suffix)     # .csv
print(p.parent)     # reports/sales
print(p.parts)      # ('reports', 'sales', 'q4.csv')

# Check existence
print(p.exists())
print(p.is_file())
print(p.is_dir())

# Create directories
Path("output/reports").mkdir(parents=True, exist_ok=True)

# List files
for f in Path("data").glob("*.csv"):
    print(f)

# Recursive
for f in Path(".").rglob("*.py"):
    print(f)
```

---

## Part 3: os Module — Classic Approach

```python
import os

# Current directory
print(os.getcwd())

# Change directory
os.chdir("/tmp")

# Join paths (cross-platform)
path = os.path.join("data", "sales.csv")

# Existence checks
os.path.exists("file.txt")
os.path.isfile("file.txt")
os.path.isdir("data/")

# File info
os.path.getsize("file.txt")    # bytes
os.path.basename("data/file.txt")   # file.txt
os.path.dirname("data/file.txt")    # data

# List directory
files = os.listdir(".")
print(files)

# Walk directory tree
for root, dirs, files in os.walk("."):
    for f in files:
        full_path = os.path.join(root, f)
        print(full_path)

# Create/remove
os.makedirs("data/exports", exist_ok=True)
os.remove("temp.txt")
os.rmdir("empty_dir")

# Environment variables
home = os.environ.get("HOME", os.path.expanduser("~"))
```

---

## Part 4: Safe File Operations Pattern

```python
from pathlib import Path

def safe_read(filepath: str, default: str = "") -> str:
    """Read file safely, return default if not found."""
    path = Path(filepath)
    if not path.exists():
        return default
    return path.read_text(encoding="utf-8")


def ensure_dir(dirpath: str) -> Path:
    """Create directory if it doesn't exist."""
    path = Path(dirpath)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_data_path(*parts) -> Path:
    """Build a path relative to a 'data' subfolder."""
    base = Path(__file__).parent / "data"
    base.mkdir(exist_ok=True)
    return base.joinpath(*parts)


# Usage
log_path = get_data_path("logs", "app.log")
ensure_dir(log_path.parent)
print(log_path)
```

---

## Part 5: File Information & Stats

```python
from pathlib import Path
from datetime import datetime

def file_info(filepath: str) -> dict:
    """Get comprehensive file information."""
    p = Path(filepath)
    if not p.exists():
        return {"error": "File not found"}

    stat = p.stat()
    return {
        "name":     p.name,
        "size_kb":  round(stat.st_size / 1024, 2),
        "created":  datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M"),
        "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
        "suffix":   p.suffix,
        "parent":   str(p.parent),
        "absolute": str(p.absolute()),
    }
```

---

## Practice Exercises

1. Write a function that lists all `.py` files in the current directory.

2. Write a function `find_files(directory, extension)` that recursively finds all files with a given extension.

3. Write a function that creates a project folder structure: `project/src/`, `project/tests/`, `project/data/`.

4. What is the difference between `os.path.join()` and `Path() /`?

---

## Phase 05 Complete — Build the Projects!

**→ [Project 01 — Journal App](../guided-projects/project-01-journal-app/)**
**→ [Project 02 — CSV Expense Tracker](../guided-projects/project-02-expense-tracker/)**
**→ [Project 03 — Customer Data Processor](../guided-projects/project-03-customer-data/)**
