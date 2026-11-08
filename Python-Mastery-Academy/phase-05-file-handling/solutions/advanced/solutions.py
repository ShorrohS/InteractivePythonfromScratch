# ============================================================
# Phase 05 — Advanced Solutions: File Handling
# ============================================================
# Run:  python solutions.py
#
# Solves every exercise in exercises/advanced/exercises.md.
# Where a solution needs a file to exist, sample data is
# created inline at the start of that section.  Every temp
# file and directory is removed before the script exits.
# ============================================================

import collections
import csv
import datetime
import json
import os
import shutil
import struct
from pathlib import Path


# ============================================================
# Q1. Large File Line Streamer
# ============================================================
# Key insight: iterating over a file object (`for line in f:`)
# uses Python's internal line buffer — only one line lives in
# memory at a time, regardless of file size.  This is the
# canonical way to process files that are too large to load.

def stream_process(filename):
    """Process a text file line by line and return summary stats.

    Returns a dict with:
        line_count, word_count, char_count, longest_line, empty_lines
    Never loads the entire file into memory.
    """
    line_count  = 0
    word_count  = 0
    char_count  = 0
    empty_lines = 0
    longest     = ""

    with open(filename, "r", encoding="utf-8") as f:
        for raw_line in f:                       # one line at a time
            line = raw_line.rstrip("\n")
            line_count += 1

            if not line.strip():
                empty_lines += 1
                continue                         # skip blank lines for word/char counts

            words       = line.split()
            word_count += len(words)
            char_count += len(line)              # chars excluding the newline

            if len(line) > len(longest):
                longest = line

    return {
        "line_count":   line_count,
        "word_count":   word_count,
        "char_count":   char_count,
        "longest_line": longest,
        "empty_lines":  empty_lines,
    }


def grep_file(filename, pattern):
    """Yield (line_number, line) for every line containing pattern.

    Case-insensitive.  This is a generator — it yields one result
    at a time so it works on arbitrarily large files.
    """
    pattern_lower = pattern.lower()
    with open(filename, "r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):     # 1-based line numbers
            if pattern_lower in line.lower():
                yield lineno, line.rstrip("\n")


# --- Q1 demo ---
_BIG_FILE = "_q1_large.txt"

# Create a sample file with enough lines to demonstrate streaming
with open(_BIG_FILE, "w") as f:
    f.write("Application started successfully\n")
    f.write("INFO: Loading configuration\n")
    f.write("ERROR: Could not connect to database\n")
    f.write("\n")                                # blank line
    f.write("WARNING: Retry attempt 1\n")
    f.write("ERROR: Timeout on connection\n")
    f.write("INFO: Fallback to cache activated\n")
    for i in range(93):
        f.write(f"INFO: Processing record {i + 1}\n")

stats = stream_process(_BIG_FILE)

print("=== Q1: Large File Line Streamer ===")
print(f"Lines      : {stats['line_count']}")
print(f"Words      : {stats['word_count']}")
print(f"Characters : {stats['char_count']}")
print(f"Empty lines: {stats['empty_lines']}")
print(f"Longest    : '{stats['longest_line']}'")
print("grep 'ERROR':")
for lineno, line in grep_file(_BIG_FILE, "ERROR"):
    print(f"  Line {lineno}: {line}")

os.remove(_BIG_FILE)
print()


# ============================================================
# Q2. CSV Sales Aggregator
# ============================================================
# Key ideas:
#   • csv.DictReader gives each row as a named dict — no column
#     index arithmetic required.
#   • We accumulate per-region stats in a plain dict before
#     writing; a nested dict tracks per-product revenue.
#   • csv.DictWriter + writeheader() + writerows() is the
#     standard pattern for writing typed CSV output.

def aggregate_sales(csv_file, summary_file, top_file):
    """Read sales CSV, aggregate by region, write two output CSVs.

    Expects columns: date, region, product, quantity, unit_price
    Writes:
        summary_file  — region, total_revenue, total_units, avg_order_value
        top_file      — region, top_product, top_product_revenue
    """
    # Accumulators keyed by region
    region_stats = collections.defaultdict(lambda: {
        "total_revenue": 0.0,
        "total_units":   0,
        "order_count":   0,
        "products":      collections.defaultdict(float),
    })

    with open(csv_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            region   = row["region"]
            qty      = int(row["quantity"])
            price    = float(row["unit_price"])
            revenue  = qty * price

            region_stats[region]["total_revenue"] += revenue
            region_stats[region]["total_units"]   += qty
            region_stats[region]["order_count"]   += 1
            region_stats[region]["products"][row["product"]] += revenue

    # Write summary CSV
    with open(summary_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["region", "total_revenue", "total_units", "avg_order_value"],
        )
        writer.writeheader()
        for region, s in sorted(region_stats.items()):
            avg = s["total_revenue"] / s["order_count"] if s["order_count"] else 0
            writer.writerow({
                "region":          region,
                "total_revenue":   f"{s['total_revenue']:.2f}",
                "total_units":     s["total_units"],
                "avg_order_value": f"{avg:.2f}",
            })

    # Write top-product CSV (highest revenue product per region)
    with open(top_file, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["region", "top_product", "top_product_revenue"],
        )
        writer.writeheader()
        for region, s in sorted(region_stats.items()):
            top_prod = max(s["products"], key=s["products"].get)
            writer.writerow({
                "region":               region,
                "top_product":          top_prod,
                "top_product_revenue":  f"{s['products'][top_prod]:.2f}",
            })


# --- Q2 demo ---
_SALES_CSV   = "_q2_sales.csv"
_SUMMARY_CSV = "_q2_summary.csv"
_TOP_CSV     = "_q2_top_products.csv"

# Build sample sales data inline
_SALES_ROWS = [
    ["date",       "region", "product",  "quantity", "unit_price"],
    ["2024-01-05", "North",  "Widget A", "50",        "30.00"],
    ["2024-01-06", "North",  "Widget B", "20",        "75.00"],
    ["2024-01-07", "South",  "Widget A", "30",        "30.00"],
    ["2024-01-08", "South",  "Gadget X", "15",        "120.00"],
    ["2024-01-09", "North",  "Gadget X", "10",        "120.00"],
    ["2024-01-10", "East",   "Widget B", "40",        "75.00"],
    ["2024-01-11", "East",   "Widget A", "60",        "30.00"],
]
with open(_SALES_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(_SALES_ROWS)

aggregate_sales(_SALES_CSV, _SUMMARY_CSV, _TOP_CSV)

print("=== Q2: CSV Sales Aggregator ===")
print("sales_summary.csv:")
with open(_SUMMARY_CSV) as f:
    for line in f:
        print(" ", line.rstrip())
print("top_products.csv:")
with open(_TOP_CSV) as f:
    for line in f:
        print(" ", line.rstrip())

for path in (_SALES_CSV, _SUMMARY_CSV, _TOP_CSV):
    os.remove(path)
print()


# ============================================================
# Q3. JSON Config Merger
# ============================================================
# Key ideas:
#   • Recursive merge: when both base[k] and override[k] are
#     dicts, merge them recursively instead of replacing.
#   • Dot-notation access: split the key on "." and traverse.
#   • diff_configs: flatten both configs to {dotted.key: value}
#     first, then compare the flat dicts.

def _deep_merge(base, override):
    """Return a new dict that is `base` merged with `override`.

    If both values for a key are dicts, they are merged recursively.
    Otherwise the override value wins.
    """
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)   # recurse into nested dicts
        else:
            result[key] = value   # override wins for scalars and lists
    return result


def load_config(base_file, override_file):
    """Load two JSON config files and return their merged result."""
    with open(base_file, "r") as f:
        base = json.load(f)
    with open(override_file, "r") as f:
        override = json.load(f)
    return _deep_merge(base, override)


def save_config(filename, config):
    """Write a config dict to a pretty-printed JSON file."""
    with open(filename, "w") as f:
        json.dump(config, f, indent=2)   # indent=2 → human-readable


def get_value(config, dotted_key):
    """Retrieve a nested value using dot notation.

    E.g. get_value(cfg, "database.host") returns cfg["database"]["host"].
    Raises KeyError if any segment of the path is missing.
    """
    keys   = dotted_key.split(".")
    cursor = config
    for k in keys:
        cursor = cursor[k]   # KeyError propagates naturally if missing
    return cursor


def _flatten(d, prefix=""):
    """Recursively flatten a nested dict to {dotted.key: value} pairs."""
    items = {}
    for key, value in d.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            items.update(_flatten(value, full_key))   # recurse into nested dicts
        else:
            items[full_key] = value
    return items


def diff_configs(base_file, override_file):
    """Return a dict of keys that differ between two config files.

    Format: {dotted_key: (base_value, override_value)}
    Only keys that exist in both files but have different values are included.
    """
    with open(base_file, "r") as f:
        base = json.load(f)
    with open(override_file, "r") as f:
        override = json.load(f)

    flat_base     = _flatten(base)
    flat_override = _flatten(override)

    diffs = {}
    for key in set(flat_base) | set(flat_override):
        bval = flat_base.get(key)
        oval = flat_override.get(key)
        if bval != oval:
            diffs[key] = (bval, oval)
    return diffs


# --- Q3 demo ---
_BASE_JSON     = "_q3_base.json"
_OVERRIDE_JSON = "_q3_prod.json"
_MERGED_JSON   = "_q3_merged.json"

_base_data = {
    "app": {"name": "MyApp", "version": "1.0"},
    "database": {"host": "localhost", "port": 5432, "name": "mydb"},
    "debug": True,
    "log_level": "DEBUG",
}
_override_data = {
    "database": {"host": "prod-db.example.com", "name": "proddb"},
    "debug": False,
    "log_level": "WARNING",
}
save_config(_BASE_JSON, _base_data)
save_config(_OVERRIDE_JSON, _override_data)

merged = load_config(_BASE_JSON, _OVERRIDE_JSON)
save_config(_MERGED_JSON, merged)

print("=== Q3: JSON Config Merger ===")
print("Merged config:", merged)
print("database.host:", get_value(merged, "database.host"))
print("database.port:", get_value(merged, "database.port"))   # kept from base
print("Diffs:")
for dotted_key, (bval, oval) in diff_configs(_BASE_JSON, _OVERRIDE_JSON).items():
    print(f"  {dotted_key}: {bval!r} → {oval!r}")

for path in (_BASE_JSON, _OVERRIDE_JSON, _MERGED_JSON):
    os.remove(path)
print()


# ============================================================
# Q4. Pathlib Directory Inventory
# ============================================================
# Key ideas:
#   • Path.rglob("*") does a recursive glob — no os.walk needed.
#   • p.is_file() skips directories returned by rglob.
#   • p.stat() gives size, mtime, etc. without separate os calls.
#   • defaultdict(list) groups files by extension cleanly.

def inventory(root_dir, extensions=None):
    """Collect file metadata recursively under root_dir.

    If `extensions` is given (list of strings like [".py", ".txt"]),
    only files with matching suffixes are included.

    Returns a list of dicts: {path, size_bytes, modified, extension}
    """
    root  = Path(root_dir)
    files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue                              # skip directories
        if extensions and p.suffix not in extensions:
            continue                              # skip non-matching types
        stat = p.stat()
        files.append({
            "path":       p,
            "size_bytes": stat.st_size,
            "modified":   datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension":  p.suffix,
        })
    return files


def summary_report(inventory_list):
    """Print a formatted table grouped by file extension."""
    groups = collections.defaultdict(list)
    for entry in inventory_list:
        groups[entry["extension"]].append(entry["size_bytes"])

    header = f"{'Extension':<12} {'Count':>6}   {'Total Size':>12}"
    print(header)
    print("-" * len(header))
    for ext, sizes in sorted(groups.items()):
        total_kb = sum(sizes) / 1024
        print(f"{ext:<12} {len(sizes):>6}   {total_kb:>10.1f} KB")


def find_duplicates(inventory_list):
    """Return {size_bytes: [Path, ...]} for sizes that appear more than once.

    Files with the same byte size are candidates for deduplication.
    """
    size_map = collections.defaultdict(list)
    for entry in inventory_list:
        size_map[entry["size_bytes"]].append(entry["path"])
    # Keep only sizes with more than one file
    return {size: paths for size, paths in size_map.items() if len(paths) > 1}


# --- Q4 demo ---
_INV_DIR = "_q4_project"

# Build a small directory tree with sample files
os.makedirs(f"{_INV_DIR}/src",      exist_ok=True)
os.makedirs(f"{_INV_DIR}/tests",    exist_ok=True)
os.makedirs(f"{_INV_DIR}/docs",     exist_ok=True)

for name, content in [
    (f"{_INV_DIR}/src/main.py",          "print('hello')\n"),
    (f"{_INV_DIR}/src/utils.py",         "def helper(): pass\n"),
    (f"{_INV_DIR}/tests/test_main.py",   "import main\n"),
    (f"{_INV_DIR}/docs/readme.txt",      "Project documentation.\n"),
    (f"{_INV_DIR}/docs/notes.txt",       "Project documentation.\n"),  # same size → duplicate
]:
    with open(name, "w") as f:
        f.write(content)

print("=== Q4: Pathlib Directory Inventory ===")
py_files = inventory(_INV_DIR, extensions=[".py"])
print(f"Python files found: {len(py_files)}")
summary_report(inventory(_INV_DIR))
dupes = find_duplicates(inventory(_INV_DIR, extensions=[".txt"]))
print("Duplicate sizes (txt):", {k: [p.name for p in v] for k, v in dupes.items()})

shutil.rmtree(_INV_DIR)
print()


# ============================================================
# Q5. Binary File Pack / Unpack
# ============================================================
# Key ideas:
#   • struct.pack / struct.unpack serialise Python values to
#     raw bytes using a format string.
#   • "!If32s": ! = big-endian, I = 4-byte uint, f = 4-byte
#     float, 32s = 32-byte bytes object.
#   • Record size = 4 + 4 + 32 = 40 bytes; read exactly 40
#     bytes per loop iteration.
#   • Names are encoded to UTF-8 and left-padded with null
#     bytes (b"\x00") to fill exactly 32 bytes.

RECORD_FORMAT = "!If32s"   # big-endian: unsigned int, float, 32-byte string
RECORD_SIZE   = struct.calcsize(RECORD_FORMAT)   # always 40 bytes


def _pack_record(record):
    """Pack one dict into 40 raw bytes."""
    name_bytes = record["name"].encode("utf-8").ljust(32, b"\x00")[:32]
    return struct.pack(RECORD_FORMAT, record["id"], record["score"], name_bytes)


def _unpack_record(raw_bytes):
    """Unpack 40 raw bytes into a dict."""
    id_, score, name_bytes = struct.unpack(RECORD_FORMAT, raw_bytes)
    name = name_bytes.rstrip(b"\x00").decode("utf-8")   # strip null padding
    return {"id": id_, "score": round(score, 4), "name": name}


def write_records(filename, records):
    """Write a list of student record dicts to a binary file (overwrites)."""
    with open(filename, "wb") as f:       # "wb" = write binary, truncates first
        for record in records:
            f.write(_pack_record(record))


def read_records(filename):
    """Read all records from a binary file; return a list of dicts."""
    records = []
    with open(filename, "rb") as f:       # "rb" = read binary
        while True:
            raw = f.read(RECORD_SIZE)     # read exactly one record's worth of bytes
            if not raw:
                break                     # end of file
            records.append(_unpack_record(raw))
    return records


def append_record(filename, record):
    """Append a single record to an existing binary file."""
    with open(filename, "ab") as f:       # "ab" = append binary
        f.write(_pack_record(record))


# --- Q5 demo ---
_BIN_FILE = "_q5_students.bin"

students = [
    {"id": 1, "score": 92.5,  "name": "Alice"},
    {"id": 2, "score": 78.0,  "name": "Bob"},
    {"id": 3, "score": 85.25, "name": "Carol"},
]
write_records(_BIN_FILE, students)

print("=== Q5: Binary File Pack / Unpack ===")
loaded = read_records(_BIN_FILE)
print("After write:", loaded)

append_record(_BIN_FILE, {"id": 4, "score": 91.0, "name": "David"})
all_records = read_records(_BIN_FILE)
print(f"After append ({len(all_records)} records):", all_records)

os.remove(_BIN_FILE)
print()


# ============================================================
# Q6. Multi-File Log Combiner
# ============================================================
# Key ideas:
#   • Log lines start with an ISO-format datetime prefix; string
#     comparison on ISO dates is the same as chronological order
#     so `sorted(lines)` is enough to sort chronologically.
#   • Splitting with maxsplit=3 keeps the message intact even if
#     it contains spaces.
#   • collections.Counter.most_common(n) gives top-n in one call.

def combine_logs(log_files, output_file, level_filter=None,
                 start_date=None, end_date=None):
    """Merge, filter, and sort lines from multiple log files.

    Line format expected: YYYY-MM-DD HH:MM:SS [LEVEL] message
    Filters applied (all optional):
        level_filter — e.g. "ERROR" keeps only [ERROR] lines
        start_date   — "YYYY-MM-DD" keeps lines on or after this date
        end_date     — "YYYY-MM-DD" keeps lines on or before this date
    Output is sorted chronologically by the leading timestamp.
    """
    collected = []

    for log_path in log_files:
        if not os.path.exists(log_path):
            continue
        with open(log_path, "r") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line.strip():
                    continue

                # Split into: date, time, [LEVEL], message
                parts = line.split(" ", 3)
                if len(parts) < 4:
                    continue   # skip malformed lines

                line_date  = parts[0]    # "YYYY-MM-DD"
                line_level = parts[2]    # "[ERROR]"
                message    = parts[3]    # "connection refused"

                # Apply optional filters
                if level_filter and f"[{level_filter}]" != line_level:
                    continue
                if start_date and line_date < start_date:
                    continue
                if end_date   and line_date > end_date:
                    continue

                collected.append(line)

    # Sort chronologically — ISO timestamps sort lexicographically
    collected.sort()

    with open(output_file, "w") as f:
        for line in collected:
            f.write(line + "\n")


def top_errors(output_file, n=5):
    """Return the n most common message strings from the combined log.

    Each line is split on the first three spaces to isolate the message.
    Returns [(message, count), ...] sorted by count descending.
    """
    messages = []
    with open(output_file, "r") as f:
        for line in f:
            parts = line.strip().split(" ", 3)
            if len(parts) >= 4:
                messages.append(parts[3].strip())   # the message portion
    counter = collections.Counter(messages)
    return counter.most_common(n)


# --- Q6 demo ---
_LOG_A    = "_q6_app.log"
_LOG_B    = "_q6_worker.log"
_COMBINED = "_q6_combined.log"

# Create two sample log files with overlapping dates
_log_entries_a = [
    "2024-01-10 08:00:01 [INFO] Application started",
    "2024-01-10 08:01:15 [ERROR] connection refused",
    "2024-01-11 09:15:00 [ERROR] timeout",
    "2024-01-11 09:16:00 [INFO] Retry succeeded",
    "2024-01-12 10:00:00 [ERROR] connection refused",
]
_log_entries_b = [
    "2024-01-09 23:59:59 [ERROR] connection refused",   # before start_date
    "2024-01-10 14:30:00 [ERROR] null pointer",
    "2024-01-11 14:31:00 [ERROR] timeout",
    "2024-01-12 09:00:00 [WARNING] high memory",
    "2024-01-12 11:00:00 [ERROR] connection refused",
]
with open(_LOG_A, "w") as f:
    f.write("\n".join(_log_entries_a) + "\n")
with open(_LOG_B, "w") as f:
    f.write("\n".join(_log_entries_b) + "\n")

combine_logs([_LOG_A, _LOG_B], _COMBINED,
             level_filter="ERROR", start_date="2024-01-10")

print("=== Q6: Multi-File Log Combiner ===")
print("Combined ERROR entries (from 2024-01-10):")
with open(_COMBINED) as f:
    for line in f:
        print(" ", line.rstrip())
print("Top errors:", top_errors(_COMBINED, n=3))

for path in (_LOG_A, _LOG_B, _COMBINED):
    os.remove(path)
print()


# ============================================================
# Q7. CSV-to-JSON ETL Pipeline
# ============================================================
# Key ideas:
#   • extract uses csv.DictReader — no manual column tracking.
#   • transform applies rename first so filters can reference
#     the new column names.
#   • Numeric comparison uses float(); a try/except falls back
#     to string comparison so mixed-type columns don't crash.
#   • load uses json.dump with indent=2 for readability.

def extract(csv_file):
    """Read a CSV file and return a list of row dicts."""
    with open(csv_file, newline="") as f:
        return list(csv.DictReader(f))   # DictReader uses header row as keys


def transform(rows, filters=None, sort_by=None, rename=None):
    """Apply rename, filters, and sort to a list of row dicts.

    rename  : {old_col: new_col}       — applied first
    filters : [(field, op, value), …]  — ops: >, <, =, !=
    sort_by : field name               — ascending sort
    """
    result = rows

    # Step 1 — rename columns
    if rename:
        result = [{rename.get(k, k): v for k, v in row.items()} for row in result]

    # Step 2 — filter rows
    if filters:
        def row_passes(row):
            for field, op, value in filters:
                cell = row.get(field, "")
                try:
                    # Try numeric comparison first
                    lhs, rhs = float(cell), float(value)
                except (ValueError, TypeError):
                    # Fall back to string comparison
                    lhs, rhs = str(cell), str(value)
                if   op == ">"  and not (lhs >  rhs): return False
                elif op == "<"  and not (lhs <  rhs): return False
                elif op == "="  and not (lhs == rhs): return False
                elif op == "!=" and not (lhs != rhs): return False
            return True
        result = [row for row in result if row_passes(row)]

    # Step 3 — sort
    if sort_by:
        result = sorted(result, key=lambda r: r.get(sort_by, ""))

    return result


def load(rows, json_file, pretty=True):
    """Write rows to a JSON file.

    pretty=True uses indent=2 for human-readable output.
    """
    with open(json_file, "w") as f:
        json.dump(rows, f, indent=2 if pretty else None)


def run_pipeline(csv_file, json_file, **kwargs):
    """Orchestrate extract → transform → load and print a summary.

    Keyword args forwarded to transform(): filters, sort_by, rename.
    """
    rows_in  = extract(csv_file)
    rows_out = transform(
        rows_in,
        filters  = kwargs.get("filters"),
        sort_by  = kwargs.get("sort_by"),
        rename   = kwargs.get("rename"),
    )
    load(rows_out, json_file, pretty=kwargs.get("pretty", True))
    print(f"Pipeline complete: {len(rows_in)} rows in "
          f"→ {len(rows_out)} rows out → {json_file}")


# --- Q7 demo ---
_EMP_CSV     = "_q7_employees.csv"
_FILTERED_JS = "_q7_filtered.json"

# Build a sample employee CSV inline
_emp_data = [
    ["name",      "department",  "salary", "years"],
    ["Alice",     "Engineering", "75000",  "5"],
    ["Bob",       "Marketing",   "55000",  "3"],
    ["Carol",     "Engineering", "90000",  "8"],
    ["Dan",       "HR",          "48000",  "2"],
    ["Eve",       "Engineering", "62000",  "4"],
    ["Frank",     "Marketing",   "70000",  "6"],
    ["Grace",     "Engineering", "58000",  "1"],
]
with open(_EMP_CSV, "w", newline="") as f:
    csv.writer(f).writerows(_emp_data)

print("=== Q7: CSV-to-JSON ETL Pipeline ===")
run_pipeline(
    _EMP_CSV, _FILTERED_JS,
    filters = [("department", "=", "Engineering"), ("salary", ">", "60000")],
    sort_by = "name",
)
print("Output JSON:")
with open(_FILTERED_JS) as f:
    print(f.read())

os.remove(_EMP_CSV)
os.remove(_FILTERED_JS)

print("All advanced solutions completed successfully.")
