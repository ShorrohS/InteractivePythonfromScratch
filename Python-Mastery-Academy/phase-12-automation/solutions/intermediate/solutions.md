# Phase 12 — Intermediate Solutions: Automation

> Q1–Q4 use `tempfile.mkdtemp()` and create all sample files programmatically.
> Q5 uses the `schedule` library (`pip install schedule`).
> Q6 uses `hashlib` from the standard library.

---

## Q1. Organize by Extension

```python
import shutil
import tempfile
from pathlib import Path
from collections import defaultdict

def organize_by_extension(folder):
    """Move files into per-extension subfolders. Returns a summary dict."""
    folder = Path(folder)
    summary = defaultdict(int)    # maps folder_name → count of moved files

    for entry in list(folder.iterdir()):   # list() snapshots the dir before we mutate it
        if not entry.is_file():            # skip any subdirectories that already exist
            continue

        ext = entry.suffix.lstrip(".")          # ".pdf" → "pdf"
        target_name = ext if ext else "no_extension"
        target_folder = folder / target_name
        target_folder.mkdir(exist_ok=True)      # create subfolder if not already there

        dest = target_folder / entry.name
        shutil.move(str(entry), str(dest))      # move the file
        print(f"Moved: {entry.name:<25} → {target_name}/{entry.name}")
        summary[target_name] += 1

    return dict(summary)


# --- Setup: populate a temp directory with sample files ---
tmp = Path(tempfile.mkdtemp())
for name in ["report.pdf", "photo.jpg", "notes.txt", "data.csv", "readme.txt", "archive.zip"]:
    (tmp / name).write_text(f"content of {name}")

# --- Run ---
result = organize_by_extension(tmp)
print("---")
print(f"Summary: {result}")

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** We call `list(folder.iterdir())` to snapshot the directory contents before the loop begins mutating it — iterating a directory while moving its files can cause unexpected behaviour on some platforms. `defaultdict(int)` starts every new key at 0, so `summary[key] += 1` works without an existence check.

---

## Q2. Recursive File Search

```python
import shutil
import tempfile
from pathlib import Path

def find_log_files(root_dir):
    """Walk all subdirectories for *.log files. Returns (count, total_bytes)."""
    root_dir = Path(root_dir)
    total_bytes = 0
    count = 0

    for log_file in sorted(root_dir.rglob("*.log")):    # rglob searches all subdirs
        size_bytes = log_file.stat().st_size
        size_kb    = size_bytes / 1024
        rel        = log_file.relative_to(root_dir)     # shorter display path
        print(f"{str(rel):<40} — {size_kb:.2f} KB")
        total_bytes += size_bytes
        count += 1

    print("---")
    print(f"Total: {count} log files | {total_bytes / 1024:.2f} KB combined")
    return count, total_bytes


# --- Setup: create a nested directory tree with .log and non-log files ---
tmp = Path(tempfile.mkdtemp())
(tmp / "app").mkdir()
(tmp / "app" / "server.log").write_text("server log " * 200)
(tmp / "app" / "errors.log").write_text("error log " * 50)
(tmp / "archive" / "2024").mkdir(parents=True)
(tmp / "archive" / "2024" / "access.log").write_text("access log " * 1500)
(tmp / "archive" / "2024" / "notes.txt").write_text("not a log file")   # should be skipped

# --- Run ---
find_log_files(tmp)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `Path.rglob("*.log")` is the single-line replacement for a manual recursive `os.walk` + filter loop. Wrapping with `sorted()` makes the output deterministic across runs and platforms. `relative_to(root_dir)` strips the leading temp-directory prefix so the printed paths are readable.

---

## Q3. Batch Rename

```python
import shutil
import tempfile
from pathlib import Path
from datetime import date

def batch_date_rename(folder):
    """Prepend today's date to all .txt files not already date-prefixed."""
    folder = Path(folder)
    today = date.today().isoformat()    # e.g. "2024-05-20"
    count = 0

    for txt_file in folder.glob("*.txt"):          # non-recursive; only this folder
        if txt_file.stem[0].isdigit():             # already starts with a date digit
            print(f"  Skipped (already prefixed): {txt_file.name}")
            continue
        new_name  = f"{today}_{txt_file.name}"
        new_path  = txt_file.parent / new_name
        txt_file.rename(new_path)                  # rename in-place; no file copy
        print(f"  {txt_file.name:<25} → {new_name}")
        count += 1

    print(f"---\nRenamed: {count} files")
    return count


# --- Setup ---
tmp = Path(tempfile.mkdtemp())
for name in ["notes.txt", "todo.txt", "report.txt"]:
    (tmp / name).write_text(f"content of {name}")
(tmp / "2024-01-01_old.txt").write_text("already prefixed — should be skipped")

# --- Run ---
batch_date_rename(tmp)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `Path.glob("*.txt")` matches only files in the immediate directory — it does not recurse. `path.rename()` is an in-place rename and is far more efficient than copy+delete. Checking `stem[0].isdigit()` is a simple heuristic that catches files already prefixed with a date like `2024-05-20_`.

---

## Q4. CSV Filter + Write

```python
import csv
import shutil
import tempfile
from pathlib import Path

# --- Setup ---
tmp = Path(tempfile.mkdtemp())
input_path  = tmp / "products.csv"
output_path = tmp / "products_expensive.csv"

input_path.write_text(
    "name,category,price\n"
    "Widget A,Electronics,29.99\n"
    "Headphones,Electronics,89.99\n"
    "Monitor,Electronics,299.00\n"
    "Notebook,Stationery,5.50\n"
    "Pen Set,Stationery,12.00\n"
)

# --- Read and filter ---
filtered    = []
total_read  = 0

with open(input_path, newline="", encoding="utf-8") as f:
    reader     = csv.DictReader(f)
    fieldnames = reader.fieldnames          # capture the original column headers
    for row in reader:
        total_read += 1
        if float(row["price"]) > 50:       # compare numerically after converting to float
            filtered.append(row)

# --- Write filtered rows ---
with open(output_path, "w", newline="", encoding="utf-8") as f:   # "w" not "r"!
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()                   # write the header row first
    writer.writerows(filtered)             # write all matching rows at once

print(f"Read {total_read} rows.")
print(f"{len(filtered)} rows with price > 50 written to {output_path.name}.")

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** Reading into a list first keeps both file handles simple — you do not need to have both files open simultaneously. `writer.writeheader()` uses the `fieldnames` from the reader, ensuring headers always match exactly. Opening the output file with `"w"` (not `"r"`) is a common beginner mistake; see the debugging challenge for that bug.

---

## Q5. Scheduled Task

```python
# pip install schedule
import time
import schedule

MAX_RUNS = 3
run_count = 0    # module-level counter — visible inside the callback

def status_check():
    """Print a timestamped status line; track run count."""
    global run_count
    run_count += 1
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Status: System OK (run {run_count}/{MAX_RUNS})")

# Schedule the task — the job is registered but not yet run
schedule.every(10).seconds.do(status_check)

print("Scheduler started — will run 3 times (every 10 seconds)...")
while run_count < MAX_RUNS:
    schedule.run_pending()   # runs any registered tasks that are due right now
    time.sleep(1)            # prevent busy-waiting; check every second

print("Done.")
```

**Explanation:** `schedule.every(10).seconds.do(job)` registers a task with the scheduler — it does not start any background thread. Without the `while` loop calling `schedule.run_pending()`, the task would never execute. `time.sleep(1)` keeps the loop from consuming 100% CPU between checks. The `global run_count` declaration is required here because `status_check` assigns to it — without `global`, Python would create a local variable instead.

---

## Q6. Find Duplicates

```python
import hashlib
import shutil
import tempfile
from pathlib import Path
from collections import defaultdict

def find_duplicates(folder):
    """Group files with identical content by MD5 hash. Returns list of duplicate groups."""
    folder   = Path(folder)
    hash_map = defaultdict(list)    # hash → list of filenames

    for entry in folder.iterdir():
        if not entry.is_file():
            continue
        data = entry.read_bytes()            # read in binary mode — works for any file type
        md5  = hashlib.md5(data).hexdigest() # compute a 32-char hex digest
        hash_map[md5].append(entry.name)

    # Separate duplicate groups from unique files
    duplicates   = [names for names in hash_map.values() if len(names) > 1]
    unique_count = sum(1 for names in hash_map.values() if len(names) == 1)

    if duplicates:
        print("Duplicates found:")
        for i, group in enumerate(duplicates, start=1):
            print(f"  Group {i}: {group}")
    else:
        print("No duplicates found.")

    print(f"No duplicates: {unique_count} unique files")
    return duplicates


# --- Setup: create files with shared and unique content ---
tmp = Path(tempfile.mkdtemp())
content_a = b"This is identical content — these files are duplicates"
content_b = b"A different block of content for another duplicate pair"

(tmp / "photo.jpg").write_bytes(content_a)
(tmp / "photo_copy.jpg").write_bytes(content_a)      # duplicate of photo.jpg
(tmp / "photo_backup.jpg").write_bytes(content_a)    # also a duplicate
(tmp / "report.pdf").write_bytes(content_b)
(tmp / "report_v2.pdf").write_bytes(content_b)       # duplicate of report.pdf
(tmp / "unique.txt").write_bytes(b"only one of this file")

# --- Run ---
find_duplicates(tmp)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** MD5 produces a fixed-length 128-bit hash from any input. Files with identical byte content will always produce the same hash, making it a reliable (though not cryptographically secure) duplicate detector. `read_bytes()` loads the full file into memory, which is fine for typical automation tasks; for very large files you would hash in chunks using `hashlib.md5()` with repeated `.update()` calls.
