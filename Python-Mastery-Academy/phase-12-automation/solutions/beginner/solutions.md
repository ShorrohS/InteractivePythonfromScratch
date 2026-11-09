# Phase 12 — Beginner Solutions: Automation

> Each solution uses `tempfile.mkdtemp()` to create a throwaway temporary directory.
> The temp directory is deleted at the end of each solution with `shutil.rmtree(tmp)`.

---

## Q1. List Files

```python
import shutil
import tempfile
from pathlib import Path

# --- Setup: create a throwaway temp directory with sample files ---
tmp = Path(tempfile.mkdtemp())
(tmp / "report.txt").write_text("Annual report content " * 50)
(tmp / "data.csv").write_bytes(b"name,value\nA,1\n" * 500)    # larger file for size demo
(tmp / "notes.md").write_text("## My Notes\nHello world")

# --- Solution: list every file and print name + size in KB ---
total = 0
for entry in tmp.iterdir():           # yields every entry (files and directories)
    if entry.is_file():               # skip any subdirectories
        size_kb = entry.stat().st_size / 1024   # convert bytes → KB
        print(f"{entry.name:<20} — {size_kb:.2f} KB")
        total += 1

print(f"Total: {total} files")

# --- Cleanup: remove the temp directory and everything inside it ---
shutil.rmtree(tmp)
```

**Explanation:** `Path.iterdir()` is a generator that yields every entry in the directory — both files and subdirectories. Filtering with `.is_file()` ensures only actual files are counted. `stat().st_size` is always in bytes; dividing by 1024 gives KB. If you wanted MB, divide by 1024 twice (or by 1_048_576).

---

## Q2. File Existence

```python
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

def file_info(path):
    """Return a metadata dict for the given path, or None if it doesn't exist."""
    p = Path(path)               # accept both str and Path objects
    if not p.exists():
        return None              # file not found — return None as specified
    stat = p.stat()
    return {
        "exists": True,
        "size_bytes": stat.st_size,                         # raw bytes
        "modified": datetime.fromtimestamp(stat.st_mtime),  # mtime → datetime
    }

# --- Setup and demo ---
tmp = Path(tempfile.mkdtemp())
sample = tmp / "notes.txt"
sample.write_text("Hello, automation!")

print("Existing file:")
print(f"  {file_info(sample)}")

print("\nMissing file:")
print(f"  {file_info(tmp / 'ghost.txt')}")

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** Wrapping the input in `Path(path)` means callers can pass either a string or an existing Path — the function is flexible. Always check `.exists()` before `.stat()`; accessing `.stat()` on a missing path raises `FileNotFoundError`. `datetime.fromtimestamp` converts the epoch float to a human-readable datetime.

---

## Q3. Copy a File

```python
import shutil
import tempfile
from pathlib import Path

def safe_copy(src, dest_dir):
    """Copy src to dest_dir, creating dest_dir if it does not exist."""
    src = Path(src)
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)   # create the full dir tree if needed
    dest_file = dest_dir / src.name               # preserve the original filename
    shutil.copy2(str(src), str(dest_file))        # copy2 copies file + metadata
    print(f"Copied: {src.name} → {dest_file}")
    return dest_file

# --- Setup and demo ---
tmp = Path(tempfile.mkdtemp())
src_file = tmp / "report.txt"
src_file.write_text("Q3 demo content — file handling exercise")
backup_dir = tmp / "backup" / "reports"   # nested destination that doesn't exist yet

safe_copy(src_file, backup_dir)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `parents=True` handles the case where multiple levels of the destination path are missing. `exist_ok=True` makes the call safe to call more than once — no error if the directory already exists. `shutil.copy2` differs from `shutil.copy` in that it also preserves file metadata like the original modification timestamp.

---

## Q4. Create Directories

```python
import shutil
import tempfile
from pathlib import Path

# --- Setup: use a temp dir as the root so we don't pollute the workspace ---
tmp = Path(tempfile.mkdtemp())
base = tmp / "project"

# Define the directory structure
dirs = [
    base / "data" / "raw",
    base / "data" / "processed",
    base / "output",
]

# Create each directory (parents=True handles all intermediate dirs too)
for d in dirs:
    d.mkdir(parents=True, exist_ok=True)
    print(f"Created: {d.relative_to(tmp)}")   # short display path

# Write 3 sample files inside data/raw/
raw_dir = base / "data" / "raw"
for i in range(1, 4):
    file_path = raw_dir / f"sample_{i:02d}.txt"
    file_path.write_text(f"Sample data file {i}\nGenerated for Phase 12 exercise.\n")
    print(f"Written:  {file_path.relative_to(tmp)}")

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** Using Path's `/` operator to build paths is cross-platform and readable — it never has the ambiguity of whether to include a trailing slash that string concatenation carries. A single `mkdir(parents=True)` call on `data/raw` also creates the `data` intermediate directory, so you do not need separate calls for every level.

---

## Q5. Read a CSV

```python
import csv
import shutil
import tempfile
from pathlib import Path

# --- Setup: create a products CSV in the temp directory ---
tmp = Path(tempfile.mkdtemp())
csv_path = tmp / "products.csv"
csv_path.write_text(
    "name,category,price\n"
    "Widget A,Electronics,29.99\n"
    "Widget B,Electronics,49.99\n"
    "Notebook,Stationery,5.50\n"
    "Pen Set,Stationery,12.00\n"
    "Headphones,Electronics,89.99\n"
)

# --- Solution ---
row_count = 0
with open(csv_path, newline="", encoding="utf-8") as f:   # newline="" prevents blank rows on Windows
    reader = csv.DictReader(f)                             # each row is a dict keyed by header
    for i, row in enumerate(reader, start=1):
        name     = row["name"]
        category = row["category"]
        price    = float(row["price"])                     # convert string → float for formatting
        print(f"Row {i}: {name:<12} | {category:<12} | ${price:>6.2f}")
        row_count += 1

print("---")
print(f"Total rows: {row_count}")

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `csv.DictReader` is preferable to plain `csv.reader` when the file has a header row — you can access each field by name (`row["price"]`) instead of a fragile positional index. The `newline=""` argument is required on Windows because the CSV module handles its own newline translation; omitting it causes the csv reader to see double newlines and insert blank rows.
