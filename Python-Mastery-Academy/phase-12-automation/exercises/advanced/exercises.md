# Phase 12 — Advanced Exercises: Automation

> These exercises combine multiple automation libraries to build real-world tools.
> Plan your approach before writing any code.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Backup Automation** ⭐⭐⭐ Advanced

Write a function `backup_recent(src_dir, dest_dir, days=7)` that:
1. Recursively finds all files in `src_dir` whose modification time falls within the last `days` days.
2. Copies them into `dest_dir/YYYY-MM-DD/`, preserving the relative path structure from `src_dir`.
3. Compresses the dated folder into a `.zip` archive using `shutil.make_archive`.
4. Removes the unzipped copy with `shutil.rmtree`.
5. Prints the archive path and total file count.

**Example output:**
```
Backing up files modified in the last 7 days...
Copied: config.json        → backup/2024-05-20/config.json
Copied: data/sales.csv     → backup/2024-05-20/data/sales.csv
Archive created: backup/2024-05-20.zip
Total files backed up: 2
```

> **Hints:**
> - `time.time() - (days * 86400)` gives the cutoff as an epoch timestamp.
> - Compare `path.stat().st_mtime` against the cutoff to decide what to include.
> - `shutil.make_archive(base_name, "zip", root_dir, base_dir)` zips `root_dir/base_dir/`.
> - Create any missing parent directories before copying: `dest.parent.mkdir(parents=True, exist_ok=True)`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q2. Email with Attachment** ⭐⭐⭐ Advanced

Write a function `send_report(to_addr, subject, body, attachment_path)` that:
1. Reads SMTP settings from environment variables: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`.
2. Builds an `email.mime.multipart.MIMEMultipart` message with a plain-text `MIMEText` body.
3. Reads the attachment file and attaches it as `MIMEApplication` with `Content-Disposition: attachment`.
4. Connects via `smtplib.SMTP(host, port)`, upgrades to TLS with `starttls()`, logs in, sends, and closes.

```python
# IMPORTANT: Never hardcode credentials.
# Store credentials in environment variables, never in source code.
# Example (load with python-dotenv or export in your shell):
#   SMTP_HOST=smtp.gmail.com
#   SMTP_PORT=587
#   SMTP_USER=YOUR_EMAIL
#   SMTP_PASS=YOUR_APP_PASSWORD   ← Gmail: use an App Password, not your account password
```

**Example usage:**
```python
send_report(
    to_addr="manager@example.com",
    subject="Weekly Sales Report",
    body="Please find the weekly report attached.",
    attachment_path=Path("reports/sales_2024_05_20.csv")
)
```

> **Hints:**
> - `int(os.environ.get("SMTP_PORT", 587))` reads the port with a sensible default.
> - `attachment_path.read_bytes()` loads the binary content for attaching.
> - `server.starttls()` must be called **before** `server.login()` — skipping it sends credentials in plaintext.
> - `server.sendmail(user, to_addr, msg.as_string())` transmits the assembled message.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q3. CSV Aggregation Pipeline** ⭐⭐⭐ Advanced

Given a `sales.csv` with columns `date, region, product, units, revenue`:

Write a function `aggregate_by_region(input_path, output_path)` that:
1. Reads the CSV with `csv.DictReader`.
2. Aggregates `total_revenue` and `total_units` per `region`.
3. Sorts results by `total_revenue` descending.
4. Writes the summary to `output_path` using `csv.DictWriter` (columns: `region, total_revenue, total_units`).
5. Prints a formatted summary table.

**Sample `sales.csv`:**
```
date,region,product,units,revenue
2024-01-15,North,Widget A,10,500.00
2024-01-16,South,Widget B,5,250.00
2024-01-17,North,Widget C,8,400.00
2024-01-18,South,Widget A,12,600.00
2024-01-19,East,Widget B,3,150.00
```

**Expected output:**
```
Region          Revenue     Units
-----------     --------    -----
North           900.00         18
South           850.00         17
East            150.00          3
```

> **Hints:**
> - `from collections import defaultdict` — `defaultdict(lambda: {"total_revenue": 0.0, "total_units": 0})` is a clean accumulator.
> - Convert: `float(row["revenue"])` and `int(row["units"])` before adding.
> - Sort: `sorted(totals.items(), key=lambda item: item[1]["total_revenue"], reverse=True)`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q4. File Watcher** ⭐⭐⭐ Advanced

Write a function `watch_folder(folder, interval=5, duration=30)` that:
1. Takes an initial snapshot of all files in `folder` (a `set` of filenames).
2. Every `interval` seconds, takes a new snapshot.
3. Prints a timestamped message whenever a new file appears or an existing file is deleted.
4. Stops automatically after `duration` seconds.
5. Prints a final summary of total new and deleted files seen.

**Example output:**
```
Watching: /path/to/folder (checking every 5s, stopping in 30s)
[14:00:05] NEW:     data_2024.csv
[14:00:10] DELETED: old_report.txt
[14:00:25] NEW:     summary.xlsx
Watcher stopped after 30s. 2 new, 1 deleted.
```

> **Hints:**
> - A snapshot is: `{p.name for p in folder.iterdir() if p.is_file()}`.
> - `new_files = current - previous`; `deleted = previous - current` — set arithmetic.
> - Track elapsed time with `time.time()`; `time.sleep(interval)` between checks.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q5. Log Cleanup** ⭐⭐⭐ Advanced

Write a function `cleanup_logs(log_dir, max_age_days=30)` that:
1. Recursively scans `log_dir` for all `.log` files using `Path.rglob`.
2. Deletes any file whose modification time is older than `max_age_days` days.
3. Prints each deleted file's path (relative to `log_dir`) and its age in days.
4. Returns the total count of deleted files.

**Example output:**
```
Deleted: app/2024-01-01.log    (45 days old)
Deleted: app/2024-01-15.log    (31 days old)
Deleted: archive/2023-12.log   (150 days old)
---
Cleaned up 3 log files.
```

> **Hints:**
> - `cutoff = time.time() - (max_age_days * 86400)` sets the age threshold.
> - `path.stat().st_mtime < cutoff` identifies files that are too old.
> - `path.unlink()` deletes a single file.
> - Age formula: `(time.time() - path.stat().st_mtime) / 86400`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q6. Excel Report** ⭐⭐⭐ Advanced

> `pip install openpyxl`

Write a function `create_excel_report(data, output_path)` that:
1. Creates a new `openpyxl.Workbook`.
2. Creates a sheet named `"Summary"` (remove the default empty sheet).
3. Writes bold headers: `Region`, `Revenue`, `Units`.
4. Fills rows from `data` — a list of dicts with keys `region`, `revenue`, `units`.
5. Applies number format `"#,##0.00"` to every cell in the Revenue column.
6. Saves the workbook to `output_path`.

**Example call:**
```python
data = [
    {"region": "North", "revenue": 12500.00, "units": 320},
    {"region": "South", "revenue":  9800.50, "units": 280},
    {"region": "East",  "revenue":  4200.75, "units": 105},
]
create_excel_report(data, Path("report.xlsx"))
```

**Expected workbook (Summary sheet):**

| Region | Revenue    | Units |
|--------|------------|-------|
| North  | 12,500.00  | 320   |
| South  |  9,800.50  | 280   |
| East   |  4,200.75  | 105   |

> **Hints:**
> - `from openpyxl.styles import Font` — `cell.font = Font(bold=True)` makes a cell bold.
> - `ws.cell(row=r, column=c, value=v)` sets a cell by row/column number (both 1-indexed).
> - `ws.cell(row=r, column=2).number_format = "#,##0.00"` applies the format after writing the value.
> - `wb.remove(wb.active)` removes the default `Sheet` before creating your named one.

> **Difficulty:** ⭐⭐⭐ Advanced

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
