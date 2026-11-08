# Lesson 01 — Introduction to Automation with Python

**Phase:** 12 — Automation | **Time:** ~35 min

---

## Part 1: What Is Automation?

Automation means writing code to perform repetitive tasks without human intervention.
In a business context this might mean:

- Collecting data from multiple sources and combining them into a single report
- Renaming and sorting hundreds of files by date or type
- Sending a scheduled email to your team every Monday morning
- Downloading the latest sales figures and updating a spreadsheet
- Backing up a critical directory every night at midnight

The goal is not to remove people from a process — it is to free skilled people from
mechanical work so they can focus on decisions only humans can make.

---

## Part 2: Types of Automation

| Type | What it does | Key tools |
|------|-------------|-----------|
| File / folder operations | Organise, rename, copy, archive files | `os`, `pathlib`, `shutil` |
| Data processing | Read, transform, write CSV/Excel/JSON | `csv`, `openpyxl`, `pandas` |
| Scheduled reports | Run a script on a timetable | `schedule`, `datetime` |
| Email notifications | Send alerts, summaries, digests | `smtplib`, `email` |
| Web interactions | Download pages, call APIs | `requests`, `selenium` |
| System commands | Run shell tools from inside Python | `subprocess` |

---

## Part 3: Automation ROI — Is It Worth Building?

Before writing a single line of code, ask whether the effort pays off:

```
Savings per year = runs_per_year × minutes_saved_per_run

It is worth automating when:
    (time_to_build + annual_maintenance) < savings_per_year
```

**Practical rules of thumb:**
- Task takes more than 30 minutes each time → consider it
- Task runs more than once per week → strong candidate
- Task is error-prone when done manually → automate it first
- Task needs an audit trail → logging + automation together

A script that takes 4 hours to build but saves 90 minutes every week pays back
in under two weeks and saves 60+ hours over a year.

---

## Part 4: Python's Automation Ecosystem

```python
# ── Standard library — no install needed ──────────────────────────────────
import os           # OS interface: env vars, process management
import pathlib      # Modern object-oriented file path handling
import shutil       # High-level file ops: copy, move, archive
import csv          # Read/write CSV files
import smtplib      # Send emails over SMTP
import subprocess   # Run shell commands from Python
import datetime     # Dates, times, and timedelta arithmetic
import time         # Delays (sleep) and timing (perf_counter)

# ── Third-party — install with pip ────────────────────────────────────────
# pip install schedule       — simple human-readable in-process scheduler
# pip install openpyxl       — read/write .xlsx Excel files
# pip install requests       — HTTP calls: APIs, file downloads, web pages
# pip install python-dotenv  — load .env files for secrets management
# pip install pandas         — powerful data analysis (Phase 13)
```

Each library has a dedicated lesson in this phase. You will use all of them
in the capstone automation pipeline at the end.

---

## Part 5: The Automation Mindset

Good automation follows a consistent process:

**Step 1 — Identify the manual steps**
Write them out one by one in plain language before touching code.
"Open Downloads folder, find all PDF files, move them to Documents/PDFs,
rename each as YYYY-MM-DD_original.pdf."

**Step 2 — Do it manually at least once**
Run through the full process by hand. You will catch edge cases:
what if a file already exists? What if the folder is empty?

**Step 3 — Automate incrementally**
Start with the core happy path. Get that working before adding error
handling, logging, or scheduling.

**Step 4 — Test with safe data first**
Never run a script that moves or deletes files on production data until
you have verified it in a temporary test directory.

**Step 5 — Add logging**
An automated script no one is watching needs to leave a trail. Log every
significant action with a timestamp.

---

## Part 6: Real-World Scenario — The Weekly Sales Report

A sales coordinator spends every Monday morning on this process:

| Step | Manual time |
|------|------------|
| Download 8 regional CSV files from shared drive | 15 min |
| Copy each into a master Excel workbook | 20 min |
| Calculate totals, highlight top performers | 25 min |
| Write summary email, send to 12 managers | 20 min |
| Archive last week's files into a dated folder | 10 min |
| **Total each week** | **~90 min** |

Over a year that is roughly 75 hours of repetitive work — and it is
error-prone because the steps are manual.

After automation, the same pipeline runs as a Python script triggered at
7:00 AM every Monday. It finishes in under 5 minutes and emails the
formatted report automatically. The coordinator reviews the output
instead of building it.

This is exactly what the five lessons in Phase 12 teach you to build.

---

## Part 7: Your First Automation — Directory Summary

```python
"""
directory_summary.py
Scans a folder, groups files by extension, prints a quick summary.
A good warm-up before every automation project.
"""

import os
from pathlib import Path
from datetime import datetime


def summarise_directory(folder: str) -> None:
    """Print a summary of files in a directory grouped by extension."""
    p = Path(folder)
    if not p.exists():
        print(f"Folder not found: {folder}")
        return

    groups: dict[str, list[Path]] = {}
    for item in p.iterdir():
        if item.is_file():
            ext = item.suffix.lower() or "(no ext)"
            groups.setdefault(ext, []).append(item)

    total = sum(len(v) for v in groups.values())
    print(f"\nDirectory : {p.resolve()}")
    print(f"Scanned   : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Files     : {total}\n")

    for ext, files in sorted(groups.items()):
        total_kb = sum(f.stat().st_size for f in files) / 1024
        print(f"  {ext:<22} {len(files):>4} file(s)   {total_kb:>8.1f} KB")


# Run on the current directory
summarise_directory(".")
```

Run this in any project folder before you start automating it.
The summary tells you exactly what you are working with.

---

## Part 8: Phase 12 Roadmap

| Lesson | Topic |
|--------|-------|
| **01** (this lesson) | Intro — what automation is and when to use it |
| **02** | File and folder automation — `pathlib`, `shutil`, `os.walk` |
| **03** | Scheduled tasks — `datetime`, `time`, `schedule` library |
| **04** | Email automation — `smtplib`, HTML emails, attachments |
| **05** | CSV and Excel automation — `csv`, `openpyxl`, formatted reports |

By the end of this phase you will have the building blocks to assemble
a complete end-to-end automation pipeline: read data files, process them,
generate a formatted Excel report, schedule the run, and email the result.

---

## Practice Exercises

1. List three repetitive tasks from your own workflow — file-related,
   report-related, or communication-related. Apply the ROI formula to each.
   Which is the strongest candidate for automation and why?

2. Run the `summarise_directory()` function on your Downloads folder or
   Desktop. How many files are there? Which extension appears most often?

3. Look up the `subprocess` module docs. Write a short script that uses
   `subprocess.run(["python", "--version"], capture_output=True)` and
   prints the version string from `result.stdout`.

4. Create a file called `automation_log.py`. Write a function
   `log_action(message: str)` that appends a timestamped line to a file
   called `automation.log`. Call it three times and confirm the log file
   contains all three entries with correct timestamps.

---

## Next Lesson

**[Lesson 02 → File and Folder Automation](lesson-02-file-folder-automation.md)**
