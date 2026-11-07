# Phase 05 — Completion Assessment

> Pass mark: 80% | Time: 25 minutes

---

## PART A: Practical Tasks

**Task 1.** Write a complete logging system:
- `log_event(message, level="INFO")` — appends to `events.log` with timestamp
- `read_logs(level=None)` — reads log, optionally filter by level
- `stats()` — returns count per level

---

**Task 2.** Write a CSV-based student grade tracker:
- Accept a list of student dicts and write to `grades.csv`
- Read them back and calculate the class average
- Save a summary report to `summary.json`

---

**Task 3.** Using pathlib:
- Create this folder structure programmatically: `workspace/src/`, `workspace/data/`, `workspace/output/`
- Create a `workspace/README.txt` with some content
- List all files in the workspace recursively

---

## PART B: Predict the Output

**Q4.**
```python
with open("x.txt", "w") as f:
    f.write("Hello\nWorld\n")
with open("x.txt", "r") as f:
    lines = f.readlines()
print(len(lines), repr(lines[0]))
import os; os.remove("x.txt")
```

**Q5.**
```python
import json
d = {"a": 1, "b": [1, 2, 3]}
s = json.dumps(d)
print(type(s).__name__, s)
```

---

## PART C: Find the Bug

**Q6.**
```python
import csv
with open("data.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["x", "y"])
```

**Q7.**
```python
import json
data = {"key": "value"}
with open("out.json", "w") as f:
    result = json.dump(data, f)
print(result["key"])
```

---

## Answers

**Q4:** `2 'Hello\n'` — readlines keeps newlines

**Q5:** `str {"a": 1, "b": [1, 2, 3]}` — json.dumps returns a string

**Q6 bug:** Missing `newline=""` → on Windows, CSV rows have blank lines between them.
Fix: `with open("data.csv", "w", newline="") as f:`

**Q7 bug:** `json.dump()` returns `None` (writes to file). Cannot index None.
Fix: Don't assign the return value. Or use `json.dumps()` if you need the string.
