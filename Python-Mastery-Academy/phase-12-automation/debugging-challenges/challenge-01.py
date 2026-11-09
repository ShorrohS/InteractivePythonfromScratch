"""
Debugging Challenge 01 — Phase 12: Automation
==============================================

INSTRUCTIONS:
  7 bugs are hidden in this file.
  All relate to automation: pathlib, shutil, csv, schedule, and smtplib.
  Find and fix each bug.
  When all are fixed, the program runs a mini automation pipeline and prints correct output.

Run: python challenge-01.py
"""

import csv
import shutil
import smtplib
import tempfile
import time
from pathlib import Path

print("=" * 55)
print("DEBUGGING CHALLENGE 01 — Phase 12: Automation Bugs")
print("=" * 55)

# Create a throwaway temp directory for all filesystem operations
tmp = Path(tempfile.mkdtemp())


# ============================================================
# BUG 1 — Path string concatenation instead of / operator
# ============================================================
print("\nBug 1 - Build a nested path:")

base_path = tmp / "project"
# BUG: using string concatenation instead of Path's / operator
# This concatenates a Path with a raw string, which raises TypeError on Python 3.12+
# and produces an incorrect raw string on older versions.
subdir = base_path + "\\data\\raw"   # BUG: should be base_path / "data" / "raw"
print(f"  Path built: {subdir}")


# ============================================================
# BUG 2 — mkdir missing parents=True
# ============================================================
print("\nBug 2 - Create nested directories:")

nested = tmp / "reports" / "2024" / "q1"
# BUG: parents=True is missing — this raises FileNotFoundError because
# "reports/2024/" doesn't exist yet; mkdir cannot create intermediate directories.
nested.mkdir(exist_ok=True)   # BUG: needs parents=True
print(f"  Created: {nested.relative_to(tmp)}")


# ============================================================
# BUG 3 — Overwriting destination without an existence check
# ============================================================
print("\nBug 3 - Copy a file safely:")

src_file  = tmp / "source.txt"
dest_dir  = tmp / "backup"
dest_file = dest_dir / src_file.name

src_file.write_text("important original data")
dest_dir.mkdir(exist_ok=True)
dest_file.write_text("existing backup — should not be silently overwritten")

# BUG: shutil.copy2 overwrites dest_file without warning.
# The intent is a safe copy that skips if the destination already exists.
shutil.copy2(str(src_file), str(dest_file))   # BUG: should check dest_file.exists() first
print(f"  Copy result: {dest_file.name} exists = {dest_file.exists()}")


# ============================================================
# BUG 4 — CSV opened in read mode for writing
# ============================================================
print("\nBug 4 - Write a CSV file:")

csv_path = tmp / "output.csv"
# BUG: "r" opens the file for reading; csv.writer requires a writable file handle.
# This raises io.UnsupportedOperation: not writable
with open(csv_path, "r", newline="") as f:    # BUG: should be "w"
    writer = csv.writer(f)
    writer.writerow(["name", "score"])
    writer.writerow(["Alice", 95])
    writer.writerow(["Bob", 87])

print(f"  CSV written: {csv_path.name}")


# ============================================================
# BUG 5 — Missing newline="" causes blank rows on Windows
# ============================================================
print("\nBug 5 - Write CSV without blank rows:")

clean_csv = tmp / "clean.csv"
# BUG: newline="" is missing — on Windows the csv module writes \r\n and the
# default text mode adds another \r, resulting in blank rows between every data row.
with open(clean_csv, "w") as f:               # BUG: should be open(..., newline="")
    writer = csv.writer(f)
    writer.writerow(["city", "population"])
    writer.writerow(["London", 9000000])
    writer.writerow(["Paris", 2161000])

print(f"  Clean CSV written: {clean_csv.name}")


# ============================================================
# BUG 6 — schedule registered but run_pending loop is missing
# ============================================================
print("\nBug 6 - Run a scheduled task:")

try:
    import schedule

    run_count = 0

    def heartbeat():
        global run_count
        run_count += 1
        print(f"  [heartbeat] tick #{run_count}")

    schedule.every(1).seconds.do(heartbeat)

    # BUG: the job is registered but there is no loop calling schedule.run_pending().
    # The heartbeat function will never execute.
    time.sleep(3)   # BUG: missing the while loop below

    # FIXED version:
    # start = time.time()
    # while time.time() - start < 3:
    #     schedule.run_pending()
    #     time.sleep(0.1)

    print(f"  Heartbeat ran {run_count} time(s)")
    schedule.clear()    # clear registered jobs so they don't affect other tests

except ImportError:
    print("  (schedule not installed — skipping Bug 6 demo)")


# ============================================================
# BUG 7 — SMTP login without calling starttls first
# ============================================================
print("\nBug 7 - SMTP STARTTLS before login:")

def send_email_buggy(host, port, user, password, to_addr, subject):
    """Buggy version: logs in before upgrading to TLS."""
    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        # BUG: server.login() is called before server.starttls().
        # This sends the username and password over an unencrypted connection,
        # and most servers (including Gmail on port 587) will reject the login.
        server.login(user, password)     # BUG: should call server.starttls() first
        server.ehlo()
        # server.sendmail(user, to_addr, f"Subject: {subject}\r\n\r\nTest")

def send_email_fixed(host, port, user, password, to_addr, subject):
    """Fixed version: starttls() upgrades the connection before login."""
    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls()                # FIXED: upgrade to TLS first
        server.login(user, password)
        server.ehlo()
        # server.sendmail(user, to_addr, f"Subject: {subject}\r\n\r\nTest")

# We don't call either function (no real credentials), but the structure is clear.
print("  send_email_fixed() defined — starttls() called before login().")


# ---- Cleanup ---
shutil.rmtree(tmp)

print("\n" + "=" * 55)
print("Fixed all 7 bugs? Each section should print without errors.")
print("=" * 55)


# ============================================================
# ANSWER KEY
# ============================================================
#
# BUG 1: Replace string concatenation with the / operator:
#   subdir = base_path / "data" / "raw"
#   Path objects only support the / operator, not + for path building.
#
# BUG 2: Add parents=True to mkdir:
#   nested.mkdir(parents=True, exist_ok=True)
#   Without parents=True, mkdir raises FileNotFoundError when any
#   intermediate directory in the path does not yet exist.
#
# BUG 3: Check dest_file.exists() before copying:
#   if not dest_file.exists():
#       shutil.copy2(str(src_file), str(dest_file))
#   else:
#       print("  Skipped: destination already exists")
#   shutil.copy2 silently overwrites existing files — add an explicit guard
#   when overwriting would be unintentional.
#
# BUG 4: Open the output CSV in write mode, not read mode:
#   with open(csv_path, "w", newline="") as f:
#   Opening with "r" makes the file handle read-only; csv.writer raises
#   io.UnsupportedOperation: not writable.
#
# BUG 5: Add newline="" to the open() call for CSV output:
#   with open(clean_csv, "w", newline="") as f:
#   Without newline="", Python's text mode adds an extra \r on Windows,
#   combining with the csv module's own \r\n to produce blank rows.
#
# BUG 6: Add a while loop that calls schedule.run_pending():
#   start = time.time()
#   while time.time() - start < 3:
#       schedule.run_pending()
#       time.sleep(0.1)
#   schedule.every(...).do(job) only registers the task. Without a loop
#   calling run_pending(), the task never executes.
#
# BUG 7: Call server.starttls() before server.login():
#   server.ehlo()
#   server.starttls()    # upgrade the connection to TLS first
#   server.login(user, password)
#   Sending credentials before TLS is active transmits them in plaintext.
#   Most servers on port 587 will reject the login attempt entirely.
