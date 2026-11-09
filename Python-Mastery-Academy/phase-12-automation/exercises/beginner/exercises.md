# Phase 12 — Beginner Exercises: Automation

> Attempt all before checking solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

**Q1. List Files** ⭐ Beginner

Use `Path(".").iterdir()` to list all **files** (not directories) in the current directory. For each file, print its name and its size in KB (rounded to 2 decimal places). Print the total file count at the end.

> **Note:** Create a small test folder with a few sample files first so there is something to list.

**Example output:**
```
report.txt           — 2.34 KB
data.csv             — 15.67 KB
notes.md             — 0.89 KB
Total: 3 files
```

> **Hints:**
> - `Path(".").iterdir()` yields all entries; filter with `.is_file()` to skip subdirectories.
> - `entry.stat().st_size` returns size in bytes — divide by 1024 for KB.
> - `entry.name` gives just the filename, not the full path.

> **Difficulty:** ⭐ Beginner

---

**Q2. File Existence** ⭐ Beginner

Write a function `file_info(path)` that accepts a file path (as a `Path` object or string) and returns a dictionary with these keys:

```python
{
    "exists": True,               # bool
    "size_bytes": 1024,           # int — size in bytes
    "modified": datetime(...)     # datetime object from mtime
}
```

Return `None` if the path does not exist.

> **Note:** Create a small text file to test the "found" case and call with a non-existent name for the "not found" case.

**Example:**
```
file_info("notes.txt")
→ {'exists': True, 'size_bytes': 312, 'modified': datetime.datetime(2024, 3, 15, 10, 22, 45)}

file_info("ghost.txt")
→ None
```

> **Hints:**
> - Convert the input to a `Path` first: `p = Path(path)`.
> - Check `p.exists()` before calling `p.stat()` — `.stat()` on a missing path raises `FileNotFoundError`.
> - `datetime.fromtimestamp(stat.st_mtime)` converts the raw timestamp to a readable datetime.

> **Difficulty:** ⭐ Beginner

---

**Q3. Copy a File** ⭐ Beginner

Write a function `safe_copy(src, dest_dir)` that:
1. Accepts a source file path and a destination directory path.
2. Creates `dest_dir` if it does not already exist (use `Path.mkdir(parents=True, exist_ok=True)`).
3. Copies the file using `shutil.copy2()`, which also preserves file metadata (timestamps).
4. Prints a confirmation line showing source and destination.

**Example output:**
```
Copied: report.txt → backup/reports/report.txt
```

> **Hints:**
> - The destination file path is `dest_dir / Path(src).name` — this preserves the original filename.
> - `shutil.copy2(src, dest)` returns the path of the new copy.
> - `parents=True` creates any missing intermediate directories in one call.

> **Difficulty:** ⭐ Beginner

---

**Q4. Create Directories** ⭐ Beginner

Use `Path.mkdir(parents=True, exist_ok=True)` to create this nested directory structure, then create 3 text files inside `project/data/raw/`:

```
project/
    data/
        raw/
        processed/
    output/
```

Print a confirmation line for each directory created and each file written.

**Example output:**
```
Created: project/data/raw
Created: project/data/processed
Created: project/output
Written: project/data/raw/sample_01.txt
Written: project/data/raw/sample_02.txt
Written: project/data/raw/sample_03.txt
```

> **Hints:**
> - Build nested paths with `/`: `base / "data" / "raw"` — never use string concatenation.
> - `path.write_text("content")` creates and writes a file in one step.
> - `path.relative_to(base)` produces a shorter display path.

> **Difficulty:** ⭐ Beginner

---

**Q5. Read a CSV** ⭐ Beginner

Use `csv.DictReader` to read a CSV file and print each row as a formatted string. Count the total rows at the end.

Create a file named `products.csv` with this content first:

```
name,category,price
Widget A,Electronics,29.99
Widget B,Electronics,49.99
Notebook,Stationery,5.50
Pen Set,Stationery,12.00
Headphones,Electronics,89.99
```

**Expected output:**
```
Row 1: Widget A    | Electronics  | $29.99
Row 2: Widget B    | Electronics  | $49.99
Row 3: Notebook    | Stationery   |  $5.50
Row 4: Pen Set     | Stationery   | $12.00
Row 5: Headphones  | Electronics  | $89.99
---
Total rows: 5
```

> **Hints:**
> - Open the file with `newline=""` — on Windows, omitting this inserts blank rows between data rows.
> - `csv.DictReader` gives each row as a dict: `row["name"]`, `row["category"]`, `row["price"]`.
> - `float(row["price"])` lets you format the price: `f"${float(row['price']):>6.2f}"`.

> **Difficulty:** ⭐ Beginner

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
