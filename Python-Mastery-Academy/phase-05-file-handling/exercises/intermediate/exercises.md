# Phase 05 — Intermediate Exercises: File Handling

---

**Q1. Log File Manager**

Write a logging system:
- `log(message, level="INFO", filename="app.log")` appends timestamped entries
- `read_logs(filename, level=None)` returns entries, optionally filtered by level
- `count_by_level(filename)` returns `{"INFO": n, "ERROR": n, ...}`
- `clear_logs(filename)` empties the log file

---

**Q2. CSV Contact Book**

Build a contacts system backed by CSV:
- `add_contact(name, phone, email, group="General")`
- `find_contact(query)` — search by name or email
- `list_by_group(group)` — filter contacts
- `export_groups_to_files()` — create separate CSV per group

---

**Q3. JSON Settings Manager**

Build an app settings manager:
- `load_settings(filename, defaults={})` — loads JSON, fills missing keys with defaults
- `save_settings(filename, settings)` — writes settings
- `update_setting(filename, key, value)` — update single key
- `reset_to_defaults(filename, defaults)` — overwrites with defaults

---

**Q4. Word Frequency Analyzer**

Read a text file and produce:
- Total words
- Unique words
- Top 10 most frequent words (excluding common words: the, a, an, is, are, in, on, at)
- Save the analysis to a JSON report file

---

**Q5. File Backup Utility**

Write a `backup_file(source, backup_dir)` function that:
- Copies the file to backup_dir
- Renames it with a timestamp: `original_20240115_143022.txt`
- Creates backup_dir if it doesn't exist
- Returns the backup file path

---

> **Solutions:** `../../solutions/intermediate/solutions.md`
