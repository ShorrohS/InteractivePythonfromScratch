# 🤖 Phase 12 — Automation

> **Goal:** Automate repetitive tasks using Python.

---

## What Python Can Automate

```
File management   → Organize, rename, sort, move files
Excel reports     → Create and update spreadsheets
Email sending     → Send automated emails with attachments
Scheduling        → Run tasks at set times
Web automation    → Selenium for browser control
Data entry        → Fill forms, process documents
```

---

## Core Libraries

```bash
pip install openpyxl schedule python-dotenv
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-file-automation.md](concepts/lesson-01-file-automation.md) | File system automation |
| 02 | [lesson-02-excel.md](concepts/lesson-02-excel.md) | Excel with openpyxl |
| 03 | [lesson-03-email.md](concepts/lesson-03-email.md) | Sending emails (smtplib) |
| 04 | [lesson-04-scheduling.md](concepts/lesson-04-scheduling.md) | Task scheduling |

---

## Code Examples

```python
# File organizer
import os
import shutil

DOWNLOADS = os.path.expanduser("~/Downloads")
FOLDERS = {
    "Images": [".jpg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".avi", ".mov"],
    "Archives": [".zip", ".tar", ".gz"],
}

for filename in os.listdir(DOWNLOADS):
    filepath = os.path.join(DOWNLOADS, filename)
    if os.path.isfile(filepath):
        ext = os.path.splitext(filename)[1].lower()
        for folder, extensions in FOLDERS.items():
            if ext in extensions:
                dest = os.path.join(DOWNLOADS, folder)
                os.makedirs(dest, exist_ok=True)
                shutil.move(filepath, os.path.join(dest, filename))
                print(f"Moved {filename} → {folder}/")
                break

# Excel automation
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill

wb = Workbook()
ws = wb.active
ws.title = "Sales Report"

# Headers with styling
headers = ["Product", "Units", "Price", "Total"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="4472C4")

# Data
data = [("Widget A", 100, 29.99), ("Widget B", 50, 49.99)]
for row, (product, units, price) in enumerate(data, 2):
    ws.cell(row=row, column=1, value=product)
    ws.cell(row=row, column=2, value=units)
    ws.cell(row=row, column=3, value=price)
    ws.cell(row=row, column=4, value=f"=B{row}*C{row}")

wb.save("sales_report.xlsx")
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [File Organizer](guided-projects/project-01-file-organizer/) | Auto-organize downloads folder |

---

## ✅ Completion Checklist

- [ ] Can automate file/folder operations
- [ ] Can create Excel files with openpyxl
- [ ] Can read and modify existing Excel files
- [ ] Know how to schedule Python tasks

---

## Previous: [Phase 11](../phase-11-apis/README.md) | Next: [Phase 13](../phase-13-data-analysis/README.md)
