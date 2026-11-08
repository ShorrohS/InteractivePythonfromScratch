# Lesson 02 — File and Folder Automation

**Phase:** 12 — Automation | **Time:** ~50 min

---

## Part 1: pathlib — The Modern Way to Handle Paths

`pathlib.Path` is the preferred way to work with file paths in Python 3.4+.
It is object-oriented, cross-platform (handles `\` vs `/` automatically),
and far more readable than the older `os.path` approach.

```python
from pathlib import Path

# Create path objects
p      = Path(".")                        # relative — current directory
home   = Path.home()                      # C:\Users\you  or  /home/you
cwd    = Path.cwd()                       # absolute current working directory
data   = Path("/data/reports")            # absolute path

# Join paths with the / operator — works on all platforms
reports  = home / "Documents" / "reports"
csv_file = reports / "sales_2024.csv"

# Inspect parts of a path
print(csv_file.name)      # sales_2024.csv
print(csv_file.stem)      # sales_2024
print(csv_file.suffix)    # .csv
print(csv_file.parent)    # ...reports
print(csv_file.resolve()) # full absolute path
```

---

## Part 2: Checking Existence and Creating Directories

```python
from pathlib import Path

p = Path("output/reports/monthly")

# Check what exists
print(p.exists())     # True if the path exists at all
print(p.is_file())    # True only if it is a regular file
print(p.is_dir())     # True only if it is a directory

# Create the full directory tree in one call
# parents=True  — create all missing parent directories
# exist_ok=True — no error if the directory already exists
p.mkdir(parents=True, exist_ok=True)

# Create an empty file (equivalent to Unix touch)
(p / "placeholder.txt").touch()
```

---

## Part 3: Listing and Searching Files

```python
from pathlib import Path

folder = Path("project")

# iterdir() — one level only, files and directories mixed
for item in folder.iterdir():
    kind = "DIR " if item.is_dir() else "FILE"
    print(f"{kind}  {item.name}")

# glob() — wildcard matching in a single directory
for csv in folder.glob("*.csv"):
    print(csv.name)

# rglob() — recursive wildcard, searches all subdirectories
for py in folder.rglob("*.py"):
    # relative_to() makes the path readable
    print(py.relative_to(folder))

# Sort results (iterdir order is not guaranteed)
all_files = sorted(folder.glob("*"), key=lambda x: x.name)
```

---

## Part 4: Reading and Writing Files

```python
from pathlib import Path

notes = Path("notes.txt")

# Write text — creates or overwrites the file
notes.write_text("Hello, automation!\nLine 2.", encoding="utf-8")

# Read the whole file as a string
content = notes.read_text(encoding="utf-8")
print(content)

# Read raw bytes (for non-text files)
raw = notes.read_bytes()

# Append lines — write_text() cannot append; use open() for that
with open(notes, "a", encoding="utf-8") as f:
    f.write("\nAppended line.")

# Get file metadata
stat = notes.stat()
print(f"Size: {stat.st_size} bytes")
print(f"Modified: {stat.st_mtime}")
```

---

## Part 5: Renaming, Moving, Copying, and Deleting

```python
import shutil
from pathlib import Path

src = Path("reports/january.csv")
dst = Path("archive/2024/january.csv")

# RENAME — in the same location, instant
src.rename(src.with_name("jan_2024.csv"))

# MOVE — works across drives and directories
shutil.move(str(src), str(dst))

# COPY a single file
shutil.copy(src, dst)          # file content only
shutil.copy2(src, dst)         # file content + timestamps preserved

# COPY an entire directory tree
shutil.copytree("reports/", "backup/reports_copy/")

# DELETE a single file
tmp = Path("temp/scratch.txt")
tmp.unlink()                   # error if not found
tmp.unlink(missing_ok=True)    # silently skip if not found

# DELETE an empty directory
Path("temp/empty").rmdir()

# DELETE a directory tree — DESTRUCTIVE, no undo
# Always confirm the path is correct before calling rmtree
shutil.rmtree("temp/old_run")
```

---

## Part 6: Deep Traversal with os.walk()

When you need to visit every subdirectory, `os.walk()` yields a
`(root, dirs, files)` tuple for each directory level.

```python
import os

for root, dirs, files in os.walk("project/"):
    # root  — current directory as a string
    # dirs  — list of subdirectory names inside root
    # files — list of filenames inside root
    level = root.replace("project/", "").count(os.sep)
    indent = "  " * level
    print(f"{indent}{os.path.basename(root)}/")
    for filename in files:
        print(f"{indent}  {filename}")
        full_path = os.path.join(root, filename)
        size_kb = os.path.getsize(full_path) / 1024
        # Process full_path here...
```

Use `os.walk()` when you need the directory structure context (root + dirs + files
together). Use `Path.rglob("*.ext")` when you only need a flat list of matching files.

---

## Part 7: Complete Example — Automatic File Organiser

```python
"""
file_organiser.py
Reads a source folder, groups files by extension into categorised
subfolders, and prints a summary of what was moved.
"""

import shutil
from pathlib import Path
from datetime import datetime

# Map category names to the extensions that belong there
CATEGORIES: dict[str, list[str]] = {
    "Images":   [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".bmp"],
    "Docs":     [".pdf", ".docx", ".doc", ".txt", ".md", ".pptx", ".xlsx", ".xls"],
    "Videos":   [".mp4", ".mov", ".avi", ".mkv", ".wmv"],
    "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
    "Code":     [".py", ".js", ".ts", ".html", ".css", ".json", ".yaml"],
}


def ext_to_category(ext: str) -> str:
    """Return the category name for a given file extension."""
    for category, extensions in CATEGORIES.items():
        if ext.lower() in extensions:
            return category
    return "Other"


def organise(source: str, destination: str) -> None:
    """
    Move every file in `source` into a matching category subfolder
    inside `destination`. Skips files that already exist at the target.
    """
    src_path = Path(source)
    dst_path = Path(destination)

    if not src_path.exists():
        print(f"Source folder not found: {src_path}")
        return

    moved:   dict[str, int] = {}
    skipped: int             = 0

    for file in src_path.iterdir():
        if not file.is_file():
            continue    # skip subdirectories

        category   = ext_to_category(file.suffix)
        target_dir = dst_path / category
        target_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_dir / file.name

        if target_file.exists():
            skipped += 1
            continue

        shutil.move(str(file), str(target_file))
        moved[category] = moved.get(category, 0) + 1

    # Print run summary
    print(f"\nFile Organiser — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Source      : {src_path.resolve()}")
    print(f"Destination : {dst_path.resolve()}\n")
    for category, count in sorted(moved.items()):
        print(f"  {category:<12}  {count:>4} file(s) moved")
    print(f"  Skipped (already exist): {skipped}")
    print(f"  Total moved: {sum(moved.values())}")


if __name__ == "__main__":
    organise("downloads/", "organised/")
```

---

## Practice Exercises

1. Write a script that uses `Path.rglob("*.log")` to find all log files
   anywhere under a given directory. Print each file's path and size in KB.
   Then move files whose `stat().st_mtime` is older than 7 days into an
   `old_logs/` subfolder.

2. Write a function `count_by_ext(folder: str) -> dict[str, int]` that
   returns a mapping of file extension → count for all files directly
   inside the folder (non-recursive, no subdirectories).

3. Extend the file organiser above to write an `organiser_report.txt` file
   inside the destination folder. Each line should record: timestamp, original
   path, new path, and category for every file that was moved.

4. Write a script that recursively finds all Python files under a project
   directory using `Path.rglob("*.py")` and prints the filename alongside
   its line count, computed with `path.read_text().count('\n') + 1`.

---

## Next Lesson

**[Lesson 03 → Scheduled Tasks and Working with Time](lesson-03-scheduled-tasks.md)**
