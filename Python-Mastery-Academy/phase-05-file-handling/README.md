# 📁 Phase 05 — File Handling

> **Goal:** Read and write data to files — text, CSV, and JSON.

---

## Why File Handling?

Variables are temporary. Files are permanent. File handling is how Python programs save data between runs, share data with other programs, and process large datasets.

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-text-files.md](concepts/lesson-01-text-files.md) | Read/write text files |
| 02 | [lesson-02-csv.md](concepts/lesson-02-csv.md) | CSV files with csv module |
| 03 | [lesson-03-json.md](concepts/lesson-03-json.md) | JSON files |
| 04 | [lesson-04-paths.md](concepts/lesson-04-paths.md) | os and pathlib modules |

---

## Core Concepts

```python
# Text file
with open("file.txt", "r") as f:
    content = f.read()

with open("file.txt", "w") as f:
    f.write("Hello\n")

# CSV
import csv
with open("data.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# JSON
import json
with open("data.json", "r") as f:
    data = json.load(f)

with open("data.json", "w") as f:
    json.dump(data, f, indent=2)
```

---

## File Modes

| Mode | Meaning |
|------|---------|
| `"r"` | Read (default) |
| `"w"` | Write (overwrites!) |
| `"a"` | Append (adds to end) |
| `"r+"` | Read + Write |
| `"rb"` | Read binary |
| `"wb"` | Write binary |

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Journal App](guided-projects/project-01-journal-app/) | Write/read personal journal entries |
| [Expense Tracker](guided-projects/project-02-expense-tracker/) | CSV-based expense tracking |
| [Customer Data](guided-projects/project-03-customer-data/) | JSON-based customer management |

---

## ✅ Completion Checklist

- [ ] Can read and write text files
- [ ] Always use `with` statement (context manager)
- [ ] Can read/write CSV files with DictReader/DictWriter
- [ ] Can read/write JSON files
- [ ] Can use `os.path` for safe file operations

---

## Previous: [Phase 04](../phase-04-functions/README.md) | Next: [Phase 06](../phase-06-error-handling/README.md)
