# Lesson 03 — Scheduled Tasks and Working with Time

**Phase:** 12 — Automation | **Time:** ~45 min

---

## Part 1: The datetime Module

The `datetime` module handles dates, times, durations, and formatting.
It is the foundation of any time-aware automation script.

```python
from datetime import datetime, date, timedelta

# ── Current moment ─────────────────────────────────────────────────────────
now   = datetime.now()    # 2024-03-11 09:15:42.123456  (local time)
today = date.today()      # 2024-03-11  (date only)

# ── Create a specific datetime ─────────────────────────────────────────────
deadline = datetime(2024, 12, 31, 17, 0, 0)   # Dec 31 2024, 17:00:00

# ── Arithmetic with timedelta ──────────────────────────────────────────────
next_week = now + timedelta(days=7)
last_week = now - timedelta(days=7)
one_hour  = now + timedelta(hours=1)
remaining = deadline - now          # a timedelta object
print(f"Days until deadline: {remaining.days}")

# ── Format a datetime → string (strftime) ──────────────────────────────────
print(now.strftime("%Y-%m-%d"))             # 2024-03-11
print(now.strftime("%d/%m/%Y %H:%M"))       # 11/03/2024 09:15
print(now.strftime("%A, %B %d %Y"))         # Monday, March 11 2024
print(now.strftime("%Y-%m-%d_%H%M%S"))      # 2024-03-11_091542 — good for filenames

# ── Parse a string → datetime (strptime) ───────────────────────────────────
raw    = "2024-03-11"
parsed = datetime.strptime(raw, "%Y-%m-%d")
print(type(parsed))     # <class 'datetime.datetime'>
```

Common `strftime` codes: `%Y` year, `%m` month, `%d` day, `%H` hour (24h),
`%M` minute, `%S` second, `%A` weekday name, `%B` month name.

---

## Part 2: The time Module

```python
import time

# ── Pause execution ─────────────────────────────────────────────────────────
time.sleep(2)       # sleep for 2 seconds
time.sleep(0.25)    # sleep for 250 milliseconds

# ── Measure elapsed wall-clock time ────────────────────────────────────────
start = time.time()       # seconds since epoch (float)
for _ in range(100_000):
    _ = 1 + 1
elapsed = time.time() - start
print(f"Elapsed: {elapsed:.4f} seconds")

# ── High-resolution timer for micro-benchmarks ─────────────────────────────
t0 = time.perf_counter()
total = sum(range(10_000_000))
t1 = time.perf_counter()
print(f"Sum in {t1 - t0:.4f}s   result={total}")
```

Use `time.time()` for general elapsed-time logging.
Use `time.perf_counter()` when you need sub-millisecond precision.

---

## Part 3: The schedule Library

`schedule` provides a clean, human-readable in-process scheduler.

```bash
pip install schedule
```

```python
import schedule
import time

def send_daily_report() -> None:
    print("Sending daily report...")

def run_backup() -> None:
    print("Running backup...")

def health_check() -> None:
    print("Health check OK")

# ── Define schedules ────────────────────────────────────────────────────────
schedule.every(10).minutes.do(health_check)
schedule.every().hour.do(health_check)
schedule.every().day.at("09:00").do(send_daily_report)
schedule.every().monday.do(send_daily_report)
schedule.every().friday.at("17:30").do(run_backup)
schedule.every(2).hours.do(run_backup)

# ── Run all pending jobs — the main loop ───────────────────────────────────
while True:
    schedule.run_pending()    # executes any job whose time has come
    time.sleep(30)            # check every 30 seconds
```

`schedule.run_pending()` never blocks. It checks whether any scheduled job
is due and runs it immediately if so, then returns. The `time.sleep()` call
controls how often you poll — 30 to 60 seconds is typical.

---

## Part 4: Passing Arguments to Scheduled Jobs

```python
import schedule
import time

def process_file(filename: str, notify: bool = False) -> None:
    print(f"Processing {filename}  notify={notify}")

# Use functools.partial or a lambda to pass arguments
import functools

job = functools.partial(process_file, "sales.csv", notify=True)
schedule.every().day.at("08:00").do(job)

# Alternative: lambda wrapper
schedule.every().day.at("18:00").do(lambda: process_file("archive.csv"))

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## Part 5: Running the Scheduler in the Background

Use a daemon thread when the scheduler should run alongside other work
without blocking the main program.

```python
import schedule
import time
import threading
from datetime import datetime


def hourly_job() -> None:
    print(f"[{datetime.now().strftime('%H:%M')}] Hourly job running...")


schedule.every().hour.do(hourly_job)


def run_scheduler() -> None:
    """Background thread — polls for pending jobs every second."""
    while True:
        schedule.run_pending()
        time.sleep(1)


# daemon=True means the thread exits when the main program exits
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Main program continues here uninterrupted
print("Scheduler started in background. Main program running.")
time.sleep(7200)    # keep alive for 2 hours, then exit
```

---

## Part 6: Complete Example — Daily Timestamped Backup

```python
"""
daily_backup.py
Copies a source folder to a timestamped backup destination each night.
Scheduled with: schedule.every().day.at("23:00").do(backup)
"""

import shutil
from pathlib import Path
from datetime import datetime
import time
import schedule

SOURCE      = Path("data/reports")
BACKUP_ROOT = Path("backups")


def backup() -> None:
    """Copy SOURCE into a new timestamped folder under BACKUP_ROOT."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    dest      = BACKUP_ROOT / f"reports_{timestamp}"

    if not SOURCE.exists():
        print(f"[BACKUP] Source not found: {SOURCE}")
        return

    try:
        shutil.copytree(SOURCE, dest)
        all_files = [f for f in dest.rglob("*") if f.is_file()]
        size_kb   = sum(f.stat().st_size for f in all_files) / 1024
        print(f"[BACKUP] {timestamp} — {dest.name}  ({size_kb:.1f} KB, {len(all_files)} files)")
    except Exception as e:
        print(f"[BACKUP] FAILED: {e}")


def main() -> None:
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    print(f"Backup scheduler started — {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    schedule.every().day.at("23:00").do(backup)

    # Run once immediately so you can confirm it works before going overnight
    backup()

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
```

---

## Part 7: Production Alternatives

`schedule` is ideal for scripts you run yourself in a persistent process.
For long-running production systems, use platform-native or library tools:

| Platform | Tool | Example |
|----------|------|---------|
| Linux / macOS | `cron` | `0 9 * * 1 python3 /scripts/report.py` |
| Windows | Task Scheduler | `schtasks /create /tn "Report" /tr "python report.py" /sc weekly` |
| Cross-platform | **APScheduler** | `pip install apscheduler` — persists jobs, survives restarts |
| Cloud / CI | GitHub Actions | `.github/workflows/report.yml` with `on: schedule: cron:` |

```python
# APScheduler example — non-blocking, persistent
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(backup, "cron", hour=23, minute=0)
scheduler.start()

# Application continues running here...
```

APScheduler supports multiple job stores (SQLAlchemy, MongoDB, Redis) so
jobs survive restarts and can be inspected or cancelled at runtime.

---

## Practice Exercises

1. Write a `countdown(seconds: int)` function that prints the remaining
   seconds once per second using `time.sleep(1)`. After the countdown
   reaches zero, print "Time's up!" and return.

2. Write a Pomodoro timer script using `schedule`: print "Focus time!" every
   25 minutes and "Take a long break!" every 2 hours. Let it run for 4 hours
   (use `time.sleep` to keep the process alive).

3. Modify the daily backup example to keep only the 7 most recent backups.
   After each successful run, list all folders in `BACKUP_ROOT`, sort them
   by name (the timestamp format sorts lexicographically), and call
   `shutil.rmtree()` on any beyond the 7 most recent.

4. Write a utility function `time_it(func, *args, **kwargs)` that calls
   `func(*args, **kwargs)`, measures execution time with
   `time.perf_counter()`, and returns `(result, elapsed_seconds)`.

---

## Next Lesson

**[Lesson 04 → Email Automation](lesson-04-email-automation.md)**
