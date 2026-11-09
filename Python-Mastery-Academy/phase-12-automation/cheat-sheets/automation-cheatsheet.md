# ⚡ Phase 12 Cheat Sheet — Automation

---

## pathlib Quick Reference

```python
from pathlib import Path

# Build paths — always use / not string concatenation
p = Path("data") / "reports" / "2024.csv"

# Common properties
p.name        # "2024.csv"
p.stem        # "2024"
p.suffix      # ".csv"
p.parent      # Path("data/reports")
p.parent.name # "reports"

# Existence and type checks
p.exists()    # True/False
p.is_file()   # True if it's a file
p.is_dir()    # True if it's a directory

# Read / write files directly
p.read_text(encoding="utf-8")
p.write_text("content", encoding="utf-8")
p.read_bytes()
p.write_bytes(b"binary content")

# Metadata
stat = p.stat()
stat.st_size    # size in bytes
stat.st_mtime   # modification time (epoch float)

from datetime import datetime
modified = datetime.fromtimestamp(stat.st_mtime)

# List directory — yields Path objects (files AND dirs)
for entry in Path("logs").iterdir():
    if entry.is_file():
        print(entry.name, entry.stat().st_size)

# Recursive search
for f in Path("src").rglob("*.py"):   # all .py files in all subdirs
    print(f)

for f in Path("logs").glob("*.log"):  # immediate directory only
    print(f)

# Create directories
Path("a/b/c").mkdir(parents=True, exist_ok=True)  # creates full tree; no error if exists

# Rename / move within same volume
p.rename(p.parent / "new_name.csv")

# Delete a file
p.unlink()

# Relative path for display
rel = p.relative_to(Path("data"))   # strips the "data/" prefix
```

---

## os and shutil

```python
import os
import shutil

# Environment variables
host = os.environ.get("SMTP_HOST", "smtp.example.com")
port = int(os.environ.get("SMTP_PORT", 587))

# Backdate a file's timestamps (useful in tests)
old_time = time.time() - (30 * 86400)   # 30 days ago
os.utime(path, (old_time, old_time))    # (atime, mtime)

# Copy a file
shutil.copy(src, dest)    # copy data + permissions (no timestamps)
shutil.copy2(src, dest)   # copy data + permissions + timestamps (prefer this)

# Move a file or directory
shutil.move(str(src), str(dest))   # overwrites dest if it exists

# Copy an entire directory tree
shutil.copytree(src_dir, dest_dir)

# Delete an entire directory tree (irreversible!)
shutil.rmtree(path)

# Create a zip/tar archive
shutil.make_archive(
    base_name="backup/2024-05-20",  # output path without extension
    format="zip",                   # "zip", "tar", "gztar", "bztar", "xztar"
    root_dir="backup",              # archive paths are relative to this
    base_dir="2024-05-20"           # which subfolder to include
)
# → produces backup/2024-05-20.zip
```

---

## CSV Read / Write

```python
import csv
from pathlib import Path

# ── Read with DictReader (recommended when file has a header row) ──
with open(Path("data.csv"), newline="", encoding="utf-8") as f:  # newline="" is required!
    reader = csv.DictReader(f)     # each row → dict keyed by column name
    for row in reader:
        print(row["name"], float(row["price"]))

# ── Read with plain reader (row → list) ──
with open(Path("data.csv"), newline="") as f:
    reader = csv.reader(f)
    header = next(reader)          # skip header row
    for row in reader:
        print(row[0], row[1])

# ── Write with DictWriter ──
fieldnames = ["name", "category", "price"]
with open(Path("out.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()           # writes the header row
    writer.writerows([
        {"name": "Widget", "category": "Electronics", "price": 29.99},
        {"name": "Notebook", "category": "Stationery", "price": 5.50},
    ])

# ── Write with plain writer ──
with open(Path("out.csv"), "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "score"])  # header
    writer.writerow(["Alice", 95])

# Common quoting options
csv.QUOTE_MINIMAL   # default — quote only when necessary
csv.QUOTE_ALL       # quote every field
csv.QUOTE_NONNUMERIC  # quote all non-numeric fields
```

---

## schedule Library

```python
# pip install schedule
import schedule
import time

def my_job():
    print("Running job...")

# Register tasks
schedule.every(10).seconds.do(my_job)
schedule.every(5).minutes.do(my_job)
schedule.every().hour.do(my_job)
schedule.every().day.at("09:00").do(my_job)

# Run the scheduler loop
while True:
    schedule.run_pending()  # executes any tasks that are due right now
    time.sleep(1)           # sleep to avoid busy-waiting

# Run for a fixed duration
start = time.time()
while time.time() - start < 60:    # run for 60 seconds
    schedule.run_pending()
    time.sleep(1)

# Cancel all jobs
schedule.clear()

# Cancel a specific job
job = schedule.every(10).seconds.do(my_job)
schedule.cancel_job(job)
```

---

## smtplib Email

```python
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

# Store credentials in environment variables, never hardcode them.
host     = os.environ.get("SMTP_HOST", "smtp.gmail.com")
port     = int(os.environ.get("SMTP_PORT", 587))
user     = os.environ.get("SMTP_USER")
password = os.environ.get("SMTP_PASS")

# Build the message
msg            = MIMEMultipart()
msg["From"]    = user
msg["To"]      = "recipient@example.com"
msg["Subject"] = "Weekly Report"
msg.attach(MIMEText("Please find the report attached.", "plain"))

# Attach a file
attachment = Path("report.csv")
data = attachment.read_bytes()
part = MIMEApplication(data, Name=attachment.name)
part["Content-Disposition"] = f'attachment; filename="{attachment.name}"'
msg.attach(part)

# Send — port 587 with STARTTLS (most common)
with smtplib.SMTP(host, port) as server:
    server.ehlo()
    server.starttls()          # MUST call before login — encrypts the channel
    server.login(user, password)
    server.sendmail(user, msg["To"], msg.as_string())

# Send — port 465 with implicit SSL
with smtplib.SMTP_SSL(host, 465) as server:
    server.login(user, password)
    server.sendmail(user, msg["To"], msg.as_string())
```

---

## openpyxl Excel

```python
# pip install openpyxl
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from pathlib import Path

# ── Create a new workbook ──
wb = Workbook()
wb.remove(wb.active)            # remove the default empty sheet
ws = wb.create_sheet("Summary")

# Write bold headers
headers = ["Region", "Revenue", "Units"]
for col, header in enumerate(headers, start=1):   # columns are 1-indexed
    cell      = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True)

# Write data rows
data = [("North", 12500.00, 320), ("South", 9800.50, 280)]
for row_idx, (region, revenue, units) in enumerate(data, start=2):
    ws.cell(row=row_idx, column=1, value=region)
    rev_cell               = ws.cell(row=row_idx, column=2, value=revenue)
    rev_cell.number_format = "#,##0.00"     # thousands separator + 2 decimals
    ws.cell(row=row_idx, column=3, value=units)

wb.save("report.xlsx")

# ── Open an existing workbook ──
wb2 = load_workbook("report.xlsx")
ws2 = wb2["Summary"]
print(ws2["A1"].value)          # "Region"
print(ws2.cell(row=2, column=2).value)  # 12500.0

# Iterate all rows (skipping header)
for row in ws2.iter_rows(min_row=2, values_only=True):
    region, revenue, units = row
    print(region, revenue, units)
```

---

## Common Automation Patterns

```python
import time
from pathlib import Path

# ── Scan files modified in the last N days ──
cutoff = time.time() - (7 * 86400)    # 7 days ago
recent = [
    f for f in Path("data").rglob("*")
    if f.is_file() and f.stat().st_mtime > cutoff
]

# ── Safe temp directory (cleaned up automatically) ──
import tempfile, shutil
tmp = Path(tempfile.mkdtemp())
try:
    # ... do work inside tmp ...
    pass
finally:
    shutil.rmtree(tmp)    # always clean up, even if an error occurs

# ── File watcher snapshot (polling) ──
previous = {p.name for p in Path("watch").iterdir() if p.is_file()}
time.sleep(5)
current  = {p.name for p in Path("watch").iterdir() if p.is_file()}
new_files     = current - previous
deleted_files = previous - current

# ── MD5 hash of a file ──
import hashlib
digest = hashlib.md5(Path("file.bin").read_bytes()).hexdigest()

# ── Compute file age in days ──
age_days = (time.time() - Path("app.log").stat().st_mtime) / 86400

# ── Sort files by modification time (newest first) ──
files = sorted(Path("logs").glob("*.log"), key=lambda p: p.stat().st_mtime, reverse=True)

# ── defaultdict accumulator for grouping ──
from collections import defaultdict
totals = defaultdict(float)
for row in rows:
    totals[row["region"]] += float(row["revenue"])
```
