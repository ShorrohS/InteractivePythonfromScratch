# Phase 12 — Intermediate Exercises: Automation

> These exercises require complete programs combining pathlib, shutil, csv, and third-party libraries.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Organize by Extension** ⭐⭐ Intermediate

Write a function `organize_by_extension(folder)` that:
- Scans a flat folder (no recursion needed).
- Moves each **file** into a subfolder named after its extension (e.g. `.pdf` → `pdf/`, `.jpg` → `jpg/`).
- Skips items that are already directories.
- Files with no extension go into a folder called `no_extension/`.
- Returns a summary dict `{folder_name: count}`.

**Example output:**
```
Moved: report.pdf     → pdf/report.pdf
Moved: photo.jpg      → jpg/photo.jpg
Moved: notes.txt      → txt/notes.txt
Moved: makefile       → no_extension/makefile
---
Summary: {'pdf': 1, 'jpg': 1, 'txt': 1, 'no_extension': 1}
```

> **Hints:**
> - `path.suffix` returns the extension including the dot (e.g. `".pdf"`).
> - `path.suffix.lstrip(".")` strips the dot to get just `"pdf"`.
> - `shutil.move(str(src), str(dest))` moves the file; create the destination subfolder first.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q2. Recursive File Search** ⭐⭐ Intermediate

Write a function `find_log_files(root_dir)` that:
- Walks the entire directory tree starting at `root_dir` using `Path.rglob("*.log")`.
- Prints each file's path relative to `root_dir` and its size in KB.
- Returns a tuple `(file_count, total_size_bytes)`.

**Example output:**
```
app/server.log            — 12.34 KB
app/errors.log            —  3.20 KB
archive/2024/access.log   — 88.10 KB
---
Total: 3 log files | 103.64 KB combined
```

> **Hints:**
> - `path.relative_to(root_dir)` produces a shorter display path without the full prefix.
> - `path.stat().st_size` gives bytes; divide by 1024 for KB.
> - `rglob` traverses all subdirectories automatically — no manual recursion needed.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q3. Batch Rename** ⭐⭐ Intermediate

Write a function `batch_date_rename(folder)` that:
- Finds all `.txt` files in `folder` (non-recursive).
- Renames each one by prepending today's date: `YYYY-MM-DD_<original_name>`.
- Skips files that are already date-prefixed (their name starts with a digit).
- Prints each rename and returns the total count of renamed files.

**Example (run on 2024-05-20):**
```
notes.txt               → 2024-05-20_notes.txt
todo.txt                → 2024-05-20_todo.txt
2024-01-01_old.txt      ← skipped (already prefixed)
---
Renamed: 2 files
```

> **Hints:**
> - `date.today().isoformat()` returns `"2024-05-20"`.
> - `path.rename(path.parent / new_name)` renames in-place without moving.
> - `path.stem[0].isdigit()` detects filenames that already start with a date digit.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q4. CSV Filter + Write** ⭐⭐ Intermediate

Given a `products.csv` with columns `name, category, price`:

1. Read the file with `csv.DictReader`.
2. Filter to rows where `price > 50`.
3. Write the filtered rows to `products_expensive.csv` with `csv.DictWriter`, preserving the original headers.
4. Print how many rows were read and how many passed the filter.

**Sample `products.csv`:**
```
name,category,price
Widget A,Electronics,29.99
Headphones,Electronics,89.99
Monitor,Electronics,299.00
Notebook,Stationery,5.50
Pen Set,Stationery,12.00
```

**Expected output:**
```
Read 5 rows.
2 rows with price > 50 written to products_expensive.csv.
```

> **Hints:**
> - Keep the header with `fieldnames = reader.fieldnames` before iterating.
> - Open the output file with `"w"` mode and `newline=""` on Windows.
> - `writer.writeheader()` writes the header row; `writer.writerows(filtered)` writes all matching rows.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q5. Scheduled Task** ⭐⭐ Intermediate

> `pip install schedule`

Write a script that:
1. Defines a function `status_check()` that prints the current timestamp and a mock `"System OK"` message.
2. Schedules it to run every 10 seconds with `schedule.every(10).seconds.do(status_check)`.
3. Runs a `while` loop calling `schedule.run_pending()` and stops automatically after 3 executions.

**Expected output:**
```
[2024-05-20 14:00:00] Status: System OK (run 1/3)
[2024-05-20 14:00:10] Status: System OK (run 2/3)
[2024-05-20 14:00:20] Status: System OK (run 3/3)
Done.
```

> **Hints:**
> - Use a module-level `run_count` variable; increment it inside `status_check()`.
> - The `while` condition should check `run_count < MAX_RUNS`.
> - `time.sleep(1)` inside the loop prevents busy-waiting between pending-checks.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q6. Find Duplicates** ⭐⭐ Intermediate

Write a function `find_duplicates(folder)` that:
- Scans all files in `folder` (non-recursive).
- Computes each file's MD5 hash using `hashlib.md5`.
- Groups files that share the same hash.
- Prints each duplicate group and how many unique (non-duplicate) files exist.
- Returns a list of duplicate groups (each group is a list of filenames).

**Example output:**
```
Duplicates found:
  Group 1: ['photo.jpg', 'photo_copy.jpg', 'photo_backup.jpg']
  Group 2: ['report.pdf', 'report_v2.pdf']
No duplicates: 1 unique files
```

> **Hints:**
> - Build a `dict` mapping `hash → [list of paths]` as you scan.
> - Read each file in binary mode: `path.read_bytes()`.
> - `hashlib.md5(data).hexdigest()` returns the hash as a hex string.
> - Duplicate groups are entries where `len(paths) > 1`.

> **Difficulty:** ⭐⭐ Intermediate

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
