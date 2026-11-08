# ============================================================
# Phase 05 — Intermediate Solutions: File Handling
# ============================================================
# Run:  python solutions.py
#
# Solves every exercise in exercises/intermediate/exercises.md.
# Each section defines the required functions, then runs a
# self-contained demo that creates any needed temp files and
# removes them before the script exits.
# ============================================================

import csv
import datetime
import json
import os
import shutil
from collections import Counter
from pathlib import Path


# ============================================================
# Q1. Log File Manager
# ============================================================
# Key idea: "a" mode appends without erasing; "w" truncates.
# We parse the bracketed [LEVEL] token out of each stored line
# to support filtering without a separate index structure.

def log(message, level="INFO", filename="app.log"):
    """Append one timestamped entry to the log file.

    Line format: YYYY-MM-DD HH:MM:SS [LEVEL] message
    Opens in "a" mode so existing entries are never overwritten.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a") as f:
        f.write(f"{timestamp} [{level}] {message}\n")


def read_logs(filename, level=None):
    """Return all log entries as a list of strings.

    If `level` is provided (e.g. "ERROR"), only lines containing
    that bracketed token are returned.  Returns [] if the file
    does not yet exist.
    """
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as f:
        lines = [ln.rstrip("\n") for ln in f if ln.strip()]
    if level:
        # Keep only lines where the [LEVEL] token matches
        lines = [ln for ln in lines if f"[{level}]" in ln]
    return lines


def count_by_level(filename):
    """Count log entries by level; returns {"INFO": n, "ERROR": n, ...}.

    Parses the text between the first '[' and ']' on each line.
    Returns an empty dict if the file does not exist.
    """
    counts = {}
    if not os.path.exists(filename):
        return counts
    with open(filename, "r") as f:
        for line in f:
            start = line.find("[")
            end   = line.find("]", start)
            if start != -1 and end != -1:
                level = line[start + 1 : end]
                counts[level] = counts.get(level, 0) + 1
    return counts


def clear_logs(filename):
    """Truncate the log file to zero bytes (the file itself is kept).

    Opening in "w" mode with no writes produces an empty file.
    """
    with open(filename, "w"):
        pass  # no writes needed — the file is now 0 bytes


# --- Q1 demo ---
_LOG = "_q1_app.log"

log("Application started",     level="INFO",    filename=_LOG)
log("Disk usage at 82%",        level="WARNING", filename=_LOG)
log("Auth service ready",       level="INFO",    filename=_LOG)
log("Database connection lost", level="ERROR",   filename=_LOG)
log("Retrying connection ...",  level="WARNING", filename=_LOG)

print("=== Q1: Log File Manager ===")
print(f"All entries ({len(read_logs(_LOG))}):")
for entry in read_logs(_LOG):
    print("  ", entry)
print("Counts by level:", count_by_level(_LOG))
print("Error entries only:", read_logs(_LOG, level="ERROR"))

clear_logs(_LOG)
print(f"After clear_logs: {len(read_logs(_LOG))} entries")
os.remove(_LOG)
print()


# ============================================================
# Q2. CSV Contact Book
# ============================================================
# Key idea: csv.DictReader / csv.DictWriter work with named
# columns.  We check whether the CSV already exists before the
# first append so we can write the header exactly once — never
# on subsequent appends.

_CONTACTS_FILE = "_q2_contacts.csv"
_FIELDNAMES    = ["name", "phone", "email", "group"]


def _load_contacts():
    """Internal helper: read all contacts from the CSV.

    Returns a list of row dicts; [] if the file is missing.
    """
    if not os.path.exists(_CONTACTS_FILE):
        return []
    with open(_CONTACTS_FILE, newline="") as f:
        return list(csv.DictReader(f))


def _save_contacts(contacts):
    """Internal helper: overwrite the CSV with the given list."""
    with open(_CONTACTS_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
        writer.writeheader()   # always write a fresh header on full rewrite
        writer.writerows(contacts)


def add_contact(name, phone, email, group="General"):
    """Append one contact.  Creates the file with a header if brand-new.

    Using "a" mode means existing contacts are never disturbed.
    We only write the header when the file doesn't exist yet.
    """
    file_is_new = not os.path.exists(_CONTACTS_FILE)
    with open(_CONTACTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
        if file_is_new:
            writer.writeheader()   # header written once, on first use only
        writer.writerow({"name": name, "phone": phone,
                         "email": email, "group": group})


def find_contact(query):
    """Search by name or email substring (case-insensitive).

    Returns a list of matching contact dicts.
    """
    q = query.lower()
    return [c for c in _load_contacts()
            if q in c["name"].lower() or q in c["email"].lower()]


def list_by_group(group):
    """Return every contact whose group matches (case-insensitive)."""
    return [c for c in _load_contacts()
            if c["group"].lower() == group.lower()]


def export_groups_to_files():
    """Write a separate CSV per distinct group; return list of filenames.

    Filename format: _groupname_group.csv  (spaces replaced with _).
    """
    groups = {}
    for c in _load_contacts():
        groups.setdefault(c["group"], []).append(c)

    created = []
    for grp, members in groups.items():
        out_name = f"_{grp.replace(' ', '_').lower()}_group.csv"
        with open(out_name, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=_FIELDNAMES)
            writer.writeheader()
            writer.writerows(members)
        created.append(out_name)
    return created


# --- Q2 demo ---
if os.path.exists(_CONTACTS_FILE):
    os.remove(_CONTACTS_FILE)   # start clean

add_contact("Alice Smith",  "555-0101", "alice@example.com",  "Friends")
add_contact("Bob Jones",    "555-0102", "bob@work.com",        "Work")
add_contact("Carol Lee",    "555-0103", "carol@example.com",   "Friends")
add_contact("Dan Park",     "555-0104", "dan@work.com",        "Work")
add_contact("Eve Chen",     "555-0105", "eve@personal.net",    "Family")

print("=== Q2: CSV Contact Book ===")
print("Search 'alice':", find_contact("alice"))
print("Work group:",     list_by_group("Work"))
group_files = export_groups_to_files()
print("Exported files:", group_files)

os.remove(_CONTACTS_FILE)
for gf in group_files:
    if os.path.exists(gf):
        os.remove(gf)
print()


# ============================================================
# Q3. JSON Settings Manager
# ============================================================
# Key idea: json.load / json.dump handle serialisation.
# indent=2 makes the file human-readable.  setdefault fills
# only the keys the user has not yet set — it never overwrites
# customised values.

_SETTINGS_FILE = "_q3_settings.json"


def load_settings(filename, defaults=None):
    """Load settings from JSON; fill missing keys from defaults.

    If the file does not exist, returns a fresh copy of defaults.
    Passing `defaults=None` is treated as an empty dict.
    """
    defaults = defaults or {}
    if not os.path.exists(filename):
        return dict(defaults)   # return a copy so the caller can mutate it
    with open(filename, "r") as f:
        settings = json.load(f)
    # Add any key the user hasn't set yet
    for key, value in defaults.items():
        settings.setdefault(key, value)
    return settings


def save_settings(filename, settings):
    """Write the settings dict to a pretty-printed JSON file."""
    with open(filename, "w") as f:
        json.dump(settings, f, indent=2)   # indent=2 → one key per line


def update_setting(filename, key, value):
    """Load → change one key → save.  All other keys are preserved."""
    settings = load_settings(filename)
    settings[key] = value
    save_settings(filename, settings)


def reset_to_defaults(filename, defaults):
    """Overwrite the settings file with the default values.

    Any user customisations are discarded.
    """
    save_settings(filename, defaults)


# --- Q3 demo ---
DEFAULTS = {"theme": "light", "font_size": 12, "autosave": True, "lang": "en"}

save_settings(_SETTINGS_FILE, {"theme": "dark", "font_size": 14})
loaded = load_settings(_SETTINGS_FILE, DEFAULTS)

print("=== Q3: JSON Settings Manager ===")
print("Loaded (with defaults filled):", loaded)

update_setting(_SETTINGS_FILE, "font_size", 18)
print("After update font_size → 18:", load_settings(_SETTINGS_FILE))

reset_to_defaults(_SETTINGS_FILE, DEFAULTS)
print("After reset to defaults:", load_settings(_SETTINGS_FILE))

os.remove(_SETTINGS_FILE)
print()


# ============================================================
# Q4. Word Frequency Analyzer
# ============================================================
# Key idea: iterate the file line by line (memory-efficient),
# strip punctuation, exclude stop words, then use Counter for
# fast frequency aggregation.  The JSON report is written with
# indent so it can be read back or opened in a text editor.

STOP_WORDS = {
    "the", "a", "an", "is", "are", "in", "on", "at",
    "of", "and", "to", "it", "that", "for", "with", "be",
}


def analyze_words(text_file, report_file="word_report.json"):
    """Count word frequencies in text_file; save a JSON report.

    Returns the report dict so the caller can inspect it inline.
    Raises FileNotFoundError if text_file is missing.
    """
    if not os.path.exists(text_file):
        raise FileNotFoundError(f"Input file not found: {text_file}")

    all_words = []
    with open(text_file, "r") as f:
        for line in f:
            for raw in line.split():
                # Lowercase and strip surrounding punctuation chars
                word = raw.lower().strip(".,!?;:\"'()-–")
                if word and word not in STOP_WORDS:
                    all_words.append(word)

    freq   = Counter(all_words)   # {word: count} sorted by count
    top_10 = freq.most_common(10)

    report = {
        "source":       text_file,
        "total_words":  len(all_words),
        "unique_words": len(freq),
        "top_10":       [{"word": w, "count": c} for w, c in top_10],
    }

    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)   # pretty-print for readability

    return report


# --- Q4 demo ---
_TEXT   = "_q4_sample.txt"
_REPORT = "_q4_report.json"

# Build a small sample text file inline so the demo is self-contained
_SAMPLE_TEXT = (
    "Python is a versatile programming language. Python makes programming fun.\n"
    "The language is easy to learn and Python is powerful for data analysis.\n"
    "Data analysis with Python is popular in science and industry alike.\n"
    "Many developers love Python because Python is readable and clear.\n"
    "Learning Python programming opens doors to machine learning and automation.\n"
)
with open(_TEXT, "w") as f:
    f.write(_SAMPLE_TEXT)

report = analyze_words(_TEXT, _REPORT)

print("=== Q4: Word Frequency Analyzer ===")
print(f"Total words  : {report['total_words']}")
print(f"Unique words : {report['unique_words']}")
print("Top 10:")
for entry in report["top_10"]:
    print(f"  {entry['word']:<18} {entry['count']}")

os.remove(_TEXT)
os.remove(_REPORT)
print()


# ============================================================
# Q5. File Backup Utility
# ============================================================
# Key ideas:
#   • shutil.copy2 copies the file AND preserves timestamps.
#   • pathlib handles path composition cleanly (no string joins).
#   • mkdir(parents=True, exist_ok=True) creates nested dirs
#     without raising an error if they already exist.

def backup_file(source, backup_dir):
    """Copy source to backup_dir with a timestamp in the filename.

    New name format: original_YYYYMMDD_HHMMSS.ext
    Returns the absolute path of the backup file.
    Raises FileNotFoundError if the source does not exist.
    """
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    dst_dir = Path(backup_dir)
    dst_dir.mkdir(parents=True, exist_ok=True)   # create directory tree

    # Compose the timestamped filename: stem_YYYYMMDD_HHMMSS.suffix
    timestamp   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{src.stem}_{timestamp}{src.suffix}"
    dst         = dst_dir / backup_name

    shutil.copy2(src, dst)   # copy2 preserves modification time metadata
    return str(dst)


# --- Q5 demo ---
_SRC        = "_q5_report.txt"
_BACKUP_DIR = "_q5_backups"

with open(_SRC, "w") as f:
    f.write("Monthly report data — version 1\nGenerated automatically.\n")

backup_path = backup_file(_SRC, _BACKUP_DIR)

print("=== Q5: File Backup Utility ===")
print(f"Original : {_SRC}")
print(f"Backup   : {backup_path}")
print(f"Exists   : {os.path.exists(backup_path)}")

os.remove(_SRC)
shutil.rmtree(_BACKUP_DIR)
print()

print("All intermediate solutions completed successfully.")
