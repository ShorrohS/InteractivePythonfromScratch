# Phase 12 — Completion Assessment

**Pass mark: 80% | Time: 30 minutes**

> Work through each part in order. Attempt your own solution before checking the answers.

---

## PART A: Write the Code

**Task 1.**

Write a function `scan_directory(path)` that:
- Accepts a directory path (as a `Path` or string).
- Returns a list of dicts — one per file — with these keys:
  - `name` — filename (string)
  - `extension` — file extension including the dot, e.g. `".csv"` (empty string if none)
  - `size_kb` — size in KB rounded to 2 decimal places (float)
  - `modified` — last modification time as a `datetime` object
- Excludes subdirectories — files only.
- Handles `PermissionError` gracefully: skip unreadable files and continue.

**Example call:**
```python
results = scan_directory(Path("/path/to/folder"))
for r in results:
    print(f"{r['name']:<25} {r['extension']:<8} {r['size_kb']:>8.2f} KB  {r['modified']:%Y-%m-%d}")
```

---

**Task 2.**

Write a function `organize_downloads(src, dest)` that:
- Moves files from `src` into `dest/<extension>/` subfolders (e.g. `.mp3` → `dest/mp3/`).
- Creates the destination subfolders as needed.
- Files with no extension go to `dest/other/`.
- Returns a summary dict: `{extension_folder: count_of_files_moved}`.

**Example:**
```python
result = organize_downloads(Path("Downloads"), Path("Sorted"))
# result → {"mp3": 5, "pdf": 3, "jpg": 12, "other": 2}
```

---

## PART B: Predict the Output / Identify the Error

**Q3.** What does this code print?

```python
from pathlib import Path

p = Path("/home/user/documents/report.tar.gz")
print(p.stem)
print(p.suffix)
print(p.parent.name)
```

---

**Q4.** What error does this code raise and why?

```python
import csv
from pathlib import Path

output = Path("results.csv")
with open(output, newline="") as f:     # note: no mode argument
    writer = csv.writer(f)
    writer.writerow(["name", "score"])
```

---

## PART C: Short Answer

**Q5.** Explain the difference between `shutil.copy()` and `shutil.copy2()`. When would you choose one over the other?

---

**Q6.** You run this scheduling code and nothing happens after the `schedule.every(...).do(job)` call. Why?

```python
import schedule, time

def job():
    print("Running!")

schedule.every(5).seconds.do(job)
time.sleep(10)
```

---

## PART D: CSV Aggregation

**Task 7.**

Given the CSV below, write code using `csv.DictReader` to compute the **total revenue per region**, then print the regions sorted by total revenue descending.

```
date,region,product,units,revenue
2024-01-10,North,Widget A,5,250.00
2024-01-11,South,Widget B,8,400.00
2024-01-12,North,Widget C,3,150.00
2024-01-13,East,Widget A,10,500.00
2024-01-14,South,Widget C,4,200.00
2024-01-15,East,Widget B,6,300.00
```

**Expected output:**
```
East   : $800.00
South  : $600.00
North  : $400.00
```

---

## Answers

---

### PART A — Task 1

```python
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

def scan_directory(path):
    """Return a list of file metadata dicts; skip subdirs and unreadable files."""
    path    = Path(path)
    results = []

    for entry in path.iterdir():
        if not entry.is_file():
            continue
        try:
            stat = entry.stat()
        except PermissionError:
            continue                    # skip files we cannot read
        results.append({
            "name":      entry.name,
            "extension": entry.suffix,  # includes the dot, or "" if none
            "size_kb":   round(stat.st_size / 1024, 2),
            "modified":  datetime.fromtimestamp(stat.st_mtime),
        })

    return results

# --- Demo ---
tmp = Path(tempfile.mkdtemp())
(tmp / "report.csv").write_text("data")
(tmp / "photo.jpg").write_bytes(b"\xff\xd8" * 100)
(tmp / "notes.txt").write_text("hello")

for r in scan_directory(tmp):
    print(f"{r['name']:<20} {r['extension']:<8} {r['size_kb']:>8.2f} KB  {r['modified']:%Y-%m-%d}")

shutil.rmtree(tmp)
```

---

### PART A — Task 2

```python
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path

def organize_downloads(src, dest):
    """Move files from src into dest/<ext>/ subfolders. Returns summary dict."""
    src    = Path(src)
    dest   = Path(dest)
    counts = defaultdict(int)

    for entry in list(src.iterdir()):       # snapshot before mutating
        if not entry.is_file():
            continue
        folder_name = entry.suffix.lstrip(".") or "other"
        target_dir  = dest / folder_name
        target_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(entry), str(target_dir / entry.name))
        counts[folder_name] += 1

    return dict(counts)

# --- Demo ---
tmp      = Path(tempfile.mkdtemp())
src_dir  = tmp / "Downloads"
dest_dir = tmp / "Sorted"
src_dir.mkdir()
for name in ["song.mp3", "doc.pdf", "photo.jpg", "music.mp3", "readme"]:
    (src_dir / name).write_text(f"content of {name}")

result = organize_downloads(src_dir, dest_dir)
print(result)

shutil.rmtree(tmp)
```

---

### PART B — Q3 Answer

```
report.tar      ← stem removes only the last extension (.gz), leaving "report.tar"
.gz             ← suffix is the last extension only
documents       ← parent.name is the name of the immediate parent directory
```

---

### PART B — Q4 Answer

**Error:** `io.UnsupportedOperation: not writable`

**Reason:** `open(output, newline="")` defaults to mode `"r"` (read-only). The file is opened for reading, so `csv.writer` cannot write to it. The fix is `open(output, "w", newline="")`.

---

### PART C — Q5 Answer

Both copy a file's **data** to the destination. The difference is in **metadata**:

- `shutil.copy()` copies data and permissions but does **not** preserve timestamps.
- `shutil.copy2()` copies data, permissions, **and** metadata including the original modification time (`st_mtime`).

Choose `copy2` when you want the copy to look like the original (e.g. backups, archives). Use `copy` when only the file content matters.

---

### PART C — Q6 Answer

`schedule.every(5).seconds.do(job)` **registers** the task with the scheduler — it does not start any background thread or timer. Without a loop calling `schedule.run_pending()`, the scheduler never checks whether any task is due and `job()` never runs.

**Fix:**
```python
import schedule, time

def job():
    print("Running!")

schedule.every(5).seconds.do(job)

start = time.time()
while time.time() - start < 10:    # run for 10 seconds
    schedule.run_pending()
    time.sleep(0.5)
```

---

### PART D — Task 7 Answer

```python
import csv
import shutil
import tempfile
from collections import defaultdict
from pathlib import Path

# --- Setup: write the CSV ---
tmp      = Path(tempfile.mkdtemp())
csv_path = tmp / "sales.csv"
csv_path.write_text(
    "date,region,product,units,revenue\n"
    "2024-01-10,North,Widget A,5,250.00\n"
    "2024-01-11,South,Widget B,8,400.00\n"
    "2024-01-12,North,Widget C,3,150.00\n"
    "2024-01-13,East,Widget A,10,500.00\n"
    "2024-01-14,South,Widget C,4,200.00\n"
    "2024-01-15,East,Widget B,6,300.00\n"
)

# --- Aggregate ---
totals = defaultdict(float)

with open(csv_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        totals[row["region"]] += float(row["revenue"])

# --- Sort descending and print ---
for region, total in sorted(totals.items(), key=lambda x: x[1], reverse=True):
    print(f"{region:<8}: ${total:.2f}")

shutil.rmtree(tmp)
```

**Output:**
```
East    : $800.00
South   : $600.00
North   : $400.00
```
