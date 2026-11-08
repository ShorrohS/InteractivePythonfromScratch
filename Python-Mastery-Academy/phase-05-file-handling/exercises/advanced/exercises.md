# Phase 05 — Advanced Exercises: File Handling

> Attempt all before checking solutions.
> Solutions: `../../solutions/advanced/solutions.py`

---

**Q1. Large File Line Streamer**

Write two functions that process a text file **without ever loading the entire file into memory**:

- `stream_process(filename)` — iterates line by line and returns a summary dict:
  - `line_count` — total number of lines
  - `word_count` — total number of words across all lines
  - `char_count` — total characters, excluding newline characters
  - `longest_line` — the longest stripped line
  - `empty_lines` — count of blank lines
- `grep_file(filename, pattern)` — a **generator** that yields `(line_number, line)` tuples for every line containing `pattern` (case-insensitive)

**Expected behaviour:**
```python
stats = stream_process("server.log")
# {"line_count": 5000, "word_count": 31200, "char_count": 189000,
#  "longest_line": "...", "empty_lines": 12}

for lineno, line in grep_file("server.log", "ERROR"):
    print(f"Line {lineno}: {line}")
```

**Hints:**
- Iterate directly over the file object (`for line in f:`) — Python reads one line at a time
- Use `enumerate(f, 1)` to get 1-based line numbers without storing all lines
- Never call `f.read()` or `f.readlines()` — that loads the whole file

**Difficulty:** Advanced

---

**Q2. CSV Sales Aggregator**

Using the `csv` module, build a data aggregation pipeline:

1. Read `sales.csv` with columns: `date`, `region`, `product`, `quantity`, `unit_price`
2. Compute per-region totals: `total_revenue` (quantity × unit_price), `total_units`, `avg_order_value`
3. Write aggregated results to `sales_summary.csv` (columns: `region`, `total_revenue`, `total_units`, `avg_order_value`)
4. Write the single top-selling product (by revenue) for each region to `top_products.csv`

Wrap everything in `aggregate_sales(csv_file, summary_file, top_file)`.

**Expected behaviour:**
```python
aggregate_sales("sales.csv", "sales_summary.csv", "top_products.csv")

# sales_summary.csv:
# region,total_revenue,total_units,avg_order_value
# North,15400.00,310,49.68
# South,9200.00,190,48.42
```

**Hints:**
- Use `csv.DictReader` to access columns by name — no need to track column indices
- Use `csv.DictWriter` with `fieldnames=` and call `writeheader()` before `writerows()`
- Accumulate per-region data in a `dict` before writing; use a nested `dict` for product revenue

**Difficulty:** Advanced

---

**Q3. JSON Config Merger**

Build a layered configuration system:

- `load_config(base_file, override_file)` — loads both JSON files; keys in the override replace those in the base; nested dicts are **merged recursively** (not replaced wholesale)
- `save_config(filename, config)` — writes the config as pretty-printed JSON (indent=2)
- `get_value(config, dotted_key)` — retrieves a nested value using dot notation: `get_value(cfg, "database.host")` is equivalent to `cfg["database"]["host"]`
- `diff_configs(base_file, override_file)` — returns a flat dict of dotted keys whose values differ, mapping each to `(base_value, override_value)`

**Expected behaviour:**
```python
config = load_config("base.json", "prod.json")
host   = get_value(config, "database.host")  # "prod-db.example.com"

diffs = diff_configs("base.json", "prod.json")
# {"database.host": ("localhost", "prod-db.example.com"),
#  "debug":         (True, False)}
```

**Hints:**
- Use `json.load()` / `json.dump()` with `indent=2`
- For recursive merge, check `isinstance(v, dict)` on both sides before deciding to recurse
- For dot notation, split on `"."` and loop: `cfg = cfg[part]` at each step
- For `diff_configs`, flatten both configs into dotted-key dicts first, then compare

**Difficulty:** Advanced

---

**Q4. Pathlib Directory Inventory**

Use `pathlib.Path` exclusively (no `os.walk`) to build a directory inventory tool:

- `inventory(root_dir, extensions=None)` — recursively collects all files under `root_dir`; if `extensions` is a list (e.g. `[".py", ".txt"]`), includes only matching files; returns a list of dicts with keys `path`, `size_bytes`, `modified`, `extension`
- `summary_report(inventory_list)` — prints a formatted table grouped by extension showing file count and total size in KB
- `find_duplicates(inventory_list)` — returns a dict mapping file size to a list of `Path` objects; only includes sizes that appear more than once

**Expected behaviour:**
```python
files = inventory("./src", extensions=[".py"])
summary_report(files)
# Extension   Count   Total Size
# ---------   -----   ----------
# .py         14      42.3 KB

dupes = find_duplicates(files)
# {1024: [PosixPath("a.py"), PosixPath("b.py")]}
```

**Hints:**
- Use `Path.rglob("*")` for recursive traversal and `p.is_file()` to skip directories
- `p.stat().st_size` gives size in bytes; `p.stat().st_mtime` gives modification timestamp
- Use `p.suffix` for the file extension
- Group by extension with `collections.defaultdict(list)` before printing the table

**Difficulty:** Advanced

---

**Q5. Binary File Pack / Unpack**

Define a simple binary record format for storing student data:

- Each record is exactly **40 bytes**: `student_id` (4-byte unsigned int) + `score` (4-byte IEEE float) + `name` (32-byte null-padded UTF-8 string)
- `write_records(filename, records)` — pack a list of `{"id": int, "score": float, "name": str}` dicts and write them to a binary file (overwrites)
- `read_records(filename)` — read all records from the binary file and return a list of dicts
- `append_record(filename, record)` — append exactly one record to an existing binary file

**Expected behaviour:**
```python
records = [
    {"id": 1, "score": 92.5, "name": "Alice"},
    {"id": 2, "score": 78.0, "name": "Bob"},
]
write_records("students.bin", records)
loaded = read_records("students.bin")
# [{"id": 1, "score": 92.5, "name": "Alice"}, {"id": 2, "score": 78.0, "name": "Bob"}]

append_record("students.bin", {"id": 3, "score": 85.5, "name": "Carol"})
print(len(read_records("students.bin")))  # 3
```

**Hints:**
- Use the `struct` module: `struct.pack("!If32s", id, score, name_bytes)` where `!` = big-endian, `I` = unsigned int, `f` = float, `32s` = 32-byte string
- `name.encode("utf-8").ljust(32, b"\x00")` pads to exactly 32 bytes
- Each record is 40 bytes; loop with `f.read(40)` and stop when `read()` returns `b""`
- Open in `"wb"` to create/overwrite, `"rb"` to read, `"ab"` to append

**Difficulty:** Advanced

---

**Q6. Multi-File Log Combiner**

Write a tool that merges several log files into a single sorted output:

- `combine_logs(log_files, output_file, level_filter=None, start_date=None, end_date=None)`:
  - Reads all files in `log_files` (list of paths)
  - Expected line format: `YYYY-MM-DD HH:MM:SS [LEVEL] message`
  - Filters by `level_filter` (e.g. `"ERROR"`) and/or `start_date` / `end_date` strings (`"YYYY-MM-DD"`) if provided
  - Sorts all matching lines chronologically (by the timestamp prefix)
  - Writes the result to `output_file`
- `top_errors(output_file, n=5)` — reads the combined file and returns the `n` most common message strings (the part after `[LEVEL]`) as `[(message, count), ...]`

**Expected behaviour:**
```python
combine_logs(["app.log", "worker.log"], "combined.log",
             level_filter="ERROR", start_date="2024-01-10")

errors = top_errors("combined.log", n=3)
# [("connection refused", 12), ("timeout", 8), ("null pointer", 3)]
```

**Hints:**
- Split each line with `line.split(" ", 3)` to extract `date`, `time`, `[LEVEL]`, `message`; the sort key is `date + " " + time`
- String comparison works for ISO-format dates: `"2024-01-15" >= "2024-01-10"` is `True`
- Use `collections.Counter` for `top_errors`; the message is the 4th token after splitting

**Difficulty:** Advanced

---

**Q7. CSV-to-JSON ETL Pipeline**

Build a three-stage Extract-Transform-Load pipeline:

- `extract(csv_file)` — reads the CSV with `csv.DictReader` and returns a list of row dicts
- `transform(rows, filters=None, sort_by=None, rename=None)`:
  - `rename`: dict mapping old column names to new names — apply **before** filters
  - `filters`: list of `(field, op, value)` tuples; supported ops: `>`, `<`, `=`, `!=`; cast both sides to `float` for numeric comparisons, fall back to string comparison
  - `sort_by`: field name to sort the results on (ascending)
- `load(rows, json_file, pretty=True)` — write the list of dicts as a JSON array; `pretty=True` uses `indent=2`
- `run_pipeline(csv_file, json_file, **kwargs)` — calls extract → transform → load in sequence and prints a one-line summary: `"Pipeline complete: N rows in → M rows out → filename"`

**Expected behaviour:**
```python
run_pipeline(
    "employees.csv", "filtered.json",
    filters=[("department", "=", "Engineering"), ("salary", ">", "60000")],
    sort_by="name",
    rename={"dept": "department"},
)
# Pipeline complete: 120 rows in → 34 rows out → filtered.json
```

**Hints:**
- A `rename` pass: `{rename.get(k, k): v for k, v in row.items()}` rewrites keys in one line
- For `filters`, wrap the comparison in a `try/except` so non-numeric strings fall back to string comparison instead of crashing
- `json.dump(rows, f, indent=2)` writes a formatted JSON array

**Difficulty:** Advanced

---

> **Solutions:** `../../solutions/advanced/solutions.py`
