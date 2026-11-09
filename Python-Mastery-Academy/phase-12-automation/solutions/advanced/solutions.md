# Phase 12 — Advanced Solutions: Automation

> All filesystem solutions use `tempfile.mkdtemp()` for throwaway directories.
> Q2 uses placeholder credentials — see the inline comment about environment variables.
> Q6 requires `openpyxl` (`pip install openpyxl`).

---

## Q1. Backup Automation

```python
import os
import shutil
import tempfile
import time
from datetime import date
from pathlib import Path

def backup_recent(src_dir, dest_dir, days=7):
    """
    Copy files modified within the last 'days' days to dest_dir/YYYY-MM-DD/,
    zip the folder, and remove the unzipped copy.
    """
    src_dir  = Path(src_dir)
    dest_dir = Path(dest_dir)
    cutoff   = time.time() - (days * 86400)          # seconds since epoch
    dated    = dest_dir / date.today().isoformat()   # e.g. backup/2024-05-20

    print(f"Backing up files modified in the last {days} days...")
    count = 0

    for src_file in src_dir.rglob("*"):              # walk the entire source tree
        if not src_file.is_file():
            continue
        if src_file.stat().st_mtime < cutoff:        # skip files older than cutoff
            continue

        # Mirror the relative directory structure inside the backup folder
        rel       = src_file.relative_to(src_dir)
        dest_file = dated / rel
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src_file), str(dest_file))  # copy2 preserves timestamps
        print(f"  Copied: {rel} → {dated.name}/{rel}")
        count += 1

    if count == 0:
        print(f"No files modified in the last {days} days.")
        return 0

    # Zip the dated folder and remove the unzipped copy
    archive_base = str(dest_dir / date.today().isoformat())   # path without extension
    shutil.make_archive(
        base_name=archive_base,           # output: dest_dir/2024-05-20.zip
        format="zip",
        root_dir=str(dest_dir),           # paths inside the archive are relative to here
        base_dir=date.today().isoformat() # zip this subfolder
    )
    shutil.rmtree(dated)                  # remove the unzipped copy after archiving
    print(f"Archive created: {archive_base}.zip")
    print(f"Total files backed up: {count}")
    return count


# --- Setup ---
tmp = Path(tempfile.mkdtemp())
src = tmp / "src"
src.mkdir()
(src / "config.json").write_text('{"setting": "value"}')
(src / "data").mkdir()
(src / "data" / "sales.csv").write_text("date,revenue\n2024-05-20,1000\n")

# Simulate an old file by backdating its mtime to 10 days ago
old_file = src / "old_archive.log"
old_file.write_text("old content — should not be included in the 7-day backup")
old_time = time.time() - (10 * 86400)
os.utime(old_file, (old_time, old_time))

backup_dir = tmp / "backup"

# --- Run ---
backup_recent(src, backup_dir, days=7)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `rglob("*")` walks every file at any depth. The `relative_to` trick preserves the folder structure inside the backup, so `src/data/sales.csv` becomes `2024-05-20/data/sales.csv` in the archive. `shutil.make_archive` handles the zip creation; its `root_dir`/`base_dir` pair means the archive contains paths like `2024-05-20/data/sales.csv`, not absolute paths.

---

## Q2. Email with Attachment

```python
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

# Store credentials in environment variables, never hardcode them.
#
# Example — set before running (or use python-dotenv to load from a .env file):
#   export SMTP_HOST=smtp.gmail.com
#   export SMTP_PORT=587
#   export SMTP_USER=YOUR_EMAIL
#   export SMTP_PASS=YOUR_APP_PASSWORD
#
# Gmail note: standard account passwords are rejected by SMTP.
# Generate an App Password at myaccount.google.com/apppasswords.

def send_report(to_addr, subject, body, attachment_path):
    """Send a plain-text email with one file attachment via STARTTLS SMTP."""
    # Read settings from the environment
    host     = os.environ.get("SMTP_HOST", "smtp.example.com")
    port     = int(os.environ.get("SMTP_PORT", 587))
    user     = os.environ.get("SMTP_USER", "YOUR_EMAIL")
    password = os.environ.get("SMTP_PASS", "YOUR_PASSWORD")

    # Build the multipart message
    msg            = MIMEMultipart()
    msg["From"]    = user
    msg["To"]      = to_addr
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))     # add the plain-text body part

    # Attach the file
    attachment_path = Path(attachment_path)
    file_data = attachment_path.read_bytes()                      # binary read
    part      = MIMEApplication(file_data, Name=attachment_path.name)
    part["Content-Disposition"] = f'attachment; filename="{attachment_path.name}"'
    msg.attach(part)

    # Connect, upgrade to TLS, authenticate, and send
    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls()                  # upgrade plaintext → encrypted; MUST come before login
        server.login(user, password)
        server.sendmail(user, to_addr, msg.as_string())

    print(f"Email sent to {to_addr}: {subject}")


# --- Demo (placeholder only — credentials are not real) ---
# Set the four environment variables above, then uncomment the call below.
#
# send_report(
#     to_addr="manager@example.com",
#     subject="Weekly Sales Report",
#     body="Please find the weekly report attached.",
#     attachment_path=Path("reports/sales_2024_05_20.csv")
# )

print("send_report() is defined and ready.")
print("Set SMTP_HOST / SMTP_PORT / SMTP_USER / SMTP_PASS as environment variables to use it.")
```

**Explanation:** `MIMEMultipart` is a container that holds multiple MIME parts — the text body and the attachment. `starttls()` upgrades the connection to TLS before credentials are transmitted; calling `login()` without `starttls()` first sends the username and password in plaintext over the network. Reading credentials from `os.environ` means the source code never contains a password, even in version history.

---

## Q3. CSV Aggregation Pipeline

```python
import csv
import shutil
import tempfile
from pathlib import Path
from collections import defaultdict

def aggregate_by_region(input_path, output_path):
    """Read sales CSV, aggregate by region, sort by revenue desc, write summary."""
    input_path  = Path(input_path)
    output_path = Path(output_path)

    # Accumulate totals — each key is a region name
    totals = defaultdict(lambda: {"total_revenue": 0.0, "total_units": 0})

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            region = row["region"]
            totals[region]["total_revenue"] += float(row["revenue"])
            totals[region]["total_units"]   += int(row["units"])

    # Sort descending by revenue
    sorted_data = sorted(
        totals.items(),
        key=lambda item: item[1]["total_revenue"],
        reverse=True
    )

    # Write the summary CSV
    fieldnames = ["region", "total_revenue", "total_units"]
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for region, vals in sorted_data:
            writer.writerow({
                "region":        region,
                "total_revenue": round(vals["total_revenue"], 2),
                "total_units":   vals["total_units"],
            })

    # Print a formatted summary table
    print(f"{'Region':<15} {'Revenue':>10}  {'Units':>6}")
    print("-" * 35)
    for region, vals in sorted_data:
        print(f"{region:<15} {vals['total_revenue']:>10.2f}  {vals['total_units']:>6}")

    return sorted_data


# --- Setup ---
tmp = Path(tempfile.mkdtemp())
input_csv  = tmp / "sales.csv"
output_csv = tmp / "summary.csv"

input_csv.write_text(
    "date,region,product,units,revenue\n"
    "2024-01-15,North,Widget A,10,500.00\n"
    "2024-01-16,South,Widget B,5,250.00\n"
    "2024-01-17,North,Widget C,8,400.00\n"
    "2024-01-18,South,Widget A,12,600.00\n"
    "2024-01-19,East,Widget B,3,150.00\n"
)

# --- Run ---
aggregate_by_region(input_csv, output_csv)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `defaultdict(lambda: {...})` initialises each new region key with a fresh dict of zeroes — no `if region not in totals` check needed. `sorted(..., reverse=True)` returns a new list; it does not modify the dict in place. Writing to a `DictWriter` with explicit `fieldnames` guarantees the output column order regardless of insertion order.

---

## Q4. File Watcher

```python
import shutil
import tempfile
import threading
import time
from pathlib import Path

def watch_folder(folder, interval=5, duration=30):
    """
    Poll 'folder' every 'interval' seconds for new or deleted files.
    Stops automatically after 'duration' seconds.
    """
    folder    = Path(folder)
    previous  = {p.name for p in folder.iterdir() if p.is_file()}  # initial snapshot

    start         = time.time()
    new_total     = 0
    deleted_total = 0

    print(f"Watching: {folder} (checking every {interval}s, stopping in {duration}s)")

    while time.time() - start < duration:
        time.sleep(interval)                    # wait before taking next snapshot

        current = {p.name for p in folder.iterdir() if p.is_file()}
        new_files     = current - previous      # appeared since last check
        deleted_files = previous - current      # disappeared since last check

        ts = time.strftime("%H:%M:%S")
        for name in sorted(new_files):
            print(f"[{ts}] NEW:     {name}")
            new_total += 1
        for name in sorted(deleted_files):
            print(f"[{ts}] DELETED: {name}")
            deleted_total += 1

        previous = current                      # update snapshot for next cycle

    print(f"Watcher stopped after {duration}s. {new_total} new, {deleted_total} deleted.")


# --- Demo: a background thread mutates the folder while the watcher runs ---
tmp = Path(tempfile.mkdtemp())
(tmp / "existing.txt").write_text("present before watcher starts")

def mutate_folder():
    """Add and remove files to trigger watcher events."""
    time.sleep(3)
    (tmp / "new_data.csv").write_text("arrived during watch")
    time.sleep(3)
    (tmp / "existing.txt").unlink()          # delete the original file

thread = threading.Thread(target=mutate_folder, daemon=True)
thread.start()

# Run with short interval/duration so the demo completes quickly
watch_folder(tmp, interval=3, duration=9)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** A set snapshot is a simple, efficient way to track directory state — no database or persistent storage needed. Python set arithmetic (`-`) gives the difference in O(n). `daemon=True` on the background thread means it will not prevent the program from exiting when the main thread finishes. For production use, the `watchdog` library provides event-driven file system notifications without polling.

---

## Q5. Log Cleanup

```python
import os
import shutil
import tempfile
import time
from pathlib import Path

def cleanup_logs(log_dir, max_age_days=30):
    """Delete .log files older than max_age_days. Returns count of deleted files."""
    log_dir = Path(log_dir)
    cutoff  = time.time() - (max_age_days * 86400)   # epoch cutoff timestamp
    deleted = 0

    for log_file in log_dir.rglob("*.log"):           # recursive search
        if not log_file.is_file():
            continue
        mtime = log_file.stat().st_mtime
        if mtime < cutoff:                            # file is older than allowed age
            age_days = (time.time() - mtime) / 86400
            print(f"Deleted: {log_file.relative_to(log_dir)}   ({age_days:.0f} days old)")
            log_file.unlink()                         # permanently delete the file
            deleted += 1

    print(f"---\nCleaned up {deleted} log files.")
    return deleted


# --- Setup: create old and recent log files ---
tmp     = Path(tempfile.mkdtemp())
log_dir = tmp / "logs"
(log_dir / "app").mkdir(parents=True)
(log_dir / "archive").mkdir(parents=True)

def backdate(path, age_days):
    """Write a log file and backdate its mtime by age_days."""
    path.write_text("log content")
    old_time = time.time() - (age_days * 86400)
    os.utime(path, (old_time, old_time))    # (atime, mtime)

backdate(log_dir / "app" / "2024-01-01.log",   45)
backdate(log_dir / "app" / "2024-01-15.log",   31)
backdate(log_dir / "archive" / "2023-12.log", 150)
(log_dir / "app" / "recent.log").write_text("recent — should NOT be deleted")

# --- Run ---
cleanup_logs(log_dir, max_age_days=30)

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `path.unlink()` deletes a single file — the Path equivalent of `os.remove()`. For directories, you would use `path.rmdir()` (empty) or `shutil.rmtree()` (non-empty). `os.utime()` modifies a file's access and modification timestamps, which is useful in tests to simulate aged files without waiting days.

---

## Q6. Excel Report

```python
# pip install openpyxl
import shutil
import tempfile
from pathlib import Path

try:
    from openpyxl import Workbook
    from openpyxl.styles import Font
except ImportError:
    print("openpyxl not installed. Run: pip install openpyxl")
    raise

def create_excel_report(data, output_path):
    """Create an Excel workbook with a formatted Summary sheet."""
    output_path = Path(output_path)
    wb = Workbook()

    # Remove the default empty sheet, then create a named one
    wb.remove(wb.active)
    ws = wb.create_sheet("Summary")

    # Write bold headers in row 1
    headers = ["Region", "Revenue", "Units"]
    for col, header in enumerate(headers, start=1):      # columns are 1-indexed
        cell      = ws.cell(row=1, column=col, value=header)
        cell.font = Font(bold=True)                      # bold formatting

    # Write data rows starting at row 2
    for row_idx, record in enumerate(data, start=2):
        ws.cell(row=row_idx, column=1, value=record["region"])

        revenue_cell                = ws.cell(row=row_idx, column=2, value=record["revenue"])
        revenue_cell.number_format  = "#,##0.00"         # thousands separator + 2 decimals

        ws.cell(row=row_idx, column=3, value=record["units"])

    wb.save(str(output_path))
    print(f"Excel report saved: {output_path.name}  ({len(data)} data rows)")
    return output_path


# --- Setup and demo ---
tmp    = Path(tempfile.mkdtemp())
output = tmp / "report.xlsx"

sample_data = [
    {"region": "North", "revenue": 12500.00, "units": 320},
    {"region": "South", "revenue":  9800.50, "units": 280},
    {"region": "East",  "revenue":  4200.75, "units": 105},
]

create_excel_report(sample_data, output)
print(f"File exists: {output.exists()}")

# --- Cleanup ---
shutil.rmtree(tmp)
```

**Explanation:** `openpyxl` works with rows and columns numbered from 1. `wb.remove(wb.active)` drops the default `Sheet` that every new `Workbook` creates, leaving only the `"Summary"` sheet you want. `number_format` is a cell-level attribute — applying it after writing the numeric value is fine; the format only affects how Excel renders the number, not the stored value.
