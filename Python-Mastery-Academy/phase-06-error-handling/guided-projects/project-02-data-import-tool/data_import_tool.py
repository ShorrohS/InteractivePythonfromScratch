"""
Project 02 - Data Import Tool
Phase 06: Error Handling

SKILLS PRACTICED:
  - FileNotFoundError, PermissionError
  - csv.Error, json.JSONDecodeError
  - KeyError (missing columns/fields)
  - ValueError / TypeError (type conversion and validation)
  - Per-row error recovery — never crash on bad data
  - Structured summary reporting

HOW TO RUN:
  python data_import_tool.py
"""

# ===========================================================
# INLINE SAMPLE DATA
#
# We embed the sample data as string constants so the script
# runs without any external files — pick it up and run it anywhere.
#
# SAMPLE_CSV has 5 rows:
#   Alice (valid), Bob (bad age), Charlie (missing salary),
#   Dave (valid), Eve (negative age)
#
# SAMPLE_JSON has 3 records:
#   Frank (valid), Grace (salary is a string), Heidi (no salary key)
#
# BAD_JSON uses unquoted keys — not valid JSON at all.
# ===========================================================

SAMPLE_CSV = """name,age,salary
Alice,30,75000
Bob,invalid_age,60000
Charlie,25,
Dave,35,90000
Eve,-5,50000"""

SAMPLE_JSON = (
    '[{"name":"Frank","age":28,"salary":82000},'
    '{"name":"Grace","salary":"not_a_number"},'
    '{"name":"Heidi","age":32}]'
)

BAD_JSON = '{name: Alice, age: 30}'

# ===========================================================
# STANDARD LIBRARY IMPORTS
# ===========================================================

import csv        # csv.DictReader, csv.Error
import io         # io.StringIO — treat a string as if it were a file
import json       # json.loads, json.JSONDecodeError


# ===========================================================
# STEP 1 — ImportResult
#
# A plain container that we build up row by row during an import,
# then hand to print_report() at the end.
#
# Design choice: we never raise exceptions out of the import methods.
# Every problem is captured here instead, so the caller always
# gets back a complete result object — not a crash.
# ===========================================================

class ImportResult:
    """
    Tracks the outcome of one import operation.

    Attributes:
        source          — label for where the data came from
        rows_processed  — total rows seen (successful + failed)
        successful      — rows that passed every check
        failed          — rows that failed for any reason
        errors          — list of human-readable error messages
        records         — list of valid, fully converted row dicts
    """

    def __init__(self, source: str):
        self.source          = source
        self.rows_processed  = 0
        self.successful      = 0
        self.failed          = 0
        self.errors: list    = []
        self.records: list   = []

    def record_success(self, row: dict) -> None:
        """Call this when a row passes all validation checks."""
        self.rows_processed += 1
        self.successful     += 1
        self.records.append(row)

    def record_failure(self, row_num: int, reason: str) -> None:
        """
        Call this when a row fails.
        'reason' is a plain-English description that goes into the report.
        """
        self.rows_processed += 1
        self.failed         += 1
        self.errors.append(f"Row {row_num}: {reason}")


# ===========================================================
# STEP 2 — DataImporter class
#
# One method per source format.  Each method catches the specific
# exceptions that format can raise, records them per-row, and
# returns a complete ImportResult — never crashing the whole run.
# ===========================================================

class DataImporter:

    # -----------------------------------------------------------
    # STEP 2a — import_csv
    # -----------------------------------------------------------

    def import_csv(self, csv_string: str) -> ImportResult:
        """
        Parse a CSV string and return an ImportResult.

        We use io.StringIO so csv.DictReader can work directly on the
        string — no temp files needed.

        Exception types handled:
          csv.Error   — structural CSV problems (e.g. too many fields)
          KeyError    — a required column is absent from the header row
          ValueError  — a field value cannot be converted to the right type,
                        or fails a business rule (age >= 0, salary >= 0)
        """
        result = ImportResult("CSV string")

        # ── Outer try: structural CSV errors ──────────────────────
        # csv.DictReader itself rarely raises csv.Error, but wrapping
        # the reader construction catches any malformed-format errors
        # before we start iterating.
        try:
            reader = csv.DictReader(io.StringIO(csv_string))
        except csv.Error as e:
            # Fatal for this import — we cannot process any rows.
            result.errors.append(f"CSV parse error: {e}")
            return result

        # ── Row-by-row processing ────────────────────────────────
        for row_num, row in enumerate(reader, start=1):
            try:
                # ── KeyError: required column absent ──────────────
                # csv.DictReader returns None (not KeyError) for columns
                # that ARE in the header but empty.  A missing HEADER
                # column raises KeyError when accessed.
                name    = row["name"]
                age_raw = row["age"]
                sal_raw = row["salary"]

                # ── ValueError: type conversion ───────────────────
                # int("invalid_age") raises ValueError.  We catch it
                # and raise a clearer message before the outer except
                # captures it.
                try:
                    age = int(age_raw)
                except (ValueError, TypeError):
                    raise ValueError(
                        f"age conversion failed — "
                        f"{age_raw!r} is not a valid integer"
                    )

                # Empty string → float("") raises ValueError.
                # We treat that as "salary is missing".
                try:
                    if not sal_raw:
                        raise ValueError("salary is missing (empty string)")
                    salary = float(sal_raw)
                except ValueError as e:
                    raise ValueError(f"salary conversion failed — {e}") from e

                # ── Business rule validation ───────────────────────
                # These raise ValueError just like bad conversions — the
                # outer except handles them the same way.
                if age < 0:
                    raise ValueError(f"age must be non-negative, got {age}")
                if salary < 0:
                    raise ValueError(f"salary must be non-negative, got {salary}")

                # All checks passed — store the clean, typed row.
                result.record_success({
                    "name":   name,
                    "age":    age,
                    "salary": salary,
                })

            except KeyError as e:
                result.record_failure(row_num, f"missing column {e}")
            except ValueError as e:
                result.record_failure(row_num, str(e))
            # Note: we deliberately do NOT have a bare 'except Exception'
            # here.  Unknown exceptions should propagate so bugs are visible.

        return result

    # -----------------------------------------------------------
    # STEP 3 — import_json
    # -----------------------------------------------------------

    def import_json(self, json_string: str) -> ImportResult:
        """
        Parse a JSON array-of-objects string and return ImportResult.

        Exception types handled:
          json.JSONDecodeError — the string is not valid JSON syntax
          TypeError            — the top-level value is not a list, or
                                 an element is not a dict (JSON object)
          KeyError             — a required field is absent in a record
          ValueError           — a field has the wrong range/value
        """
        result = ImportResult("JSON string")

        # ── json.JSONDecodeError: completely invalid JSON ──────────
        # This is a subclass of ValueError, but we name it explicitly
        # so the error message mentions JSON rather than generic ValueError.
        # It is fatal: if the JSON won't parse we cannot process any rows.
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError as e:
            result.errors.append(f"JSON parse error: {e}")
            return result

        # ── TypeError: top-level must be a list ───────────────────
        # A valid JSON file containing a single object ({}) would parse
        # successfully above but still be the wrong shape for us.
        if not isinstance(data, list):
            result.errors.append(
                f"Expected a JSON array at top level, "
                f"got {type(data).__name__}"
            )
            return result

        # ── Row-by-row processing ────────────────────────────────
        for row_num, record in enumerate(data, start=1):
            try:
                # Each element must be a dict (JSON object).
                if not isinstance(record, dict):
                    raise TypeError(
                        f"expected a JSON object, got {type(record).__name__}"
                    )

                # ── KeyError: required fields ──────────────────────
                name   = record["name"]      # raises KeyError if absent
                salary = record["salary"]    # raises KeyError if absent
                age    = record.get("age")   # optional — None if missing

                # ── TypeError: numeric fields must actually be numbers ──
                # JSON lets any value be any type; "not_a_number" is
                # a perfectly valid JSON string even in a salary field.
                if age is not None and not isinstance(age, (int, float)):
                    raise TypeError(
                        f"age must be numeric, got {type(age).__name__!r}"
                    )

                if not isinstance(salary, (int, float)):
                    raise TypeError(
                        f"salary must be numeric, got "
                        f"{type(salary).__name__!r} "
                        f"(value: {salary!r})"
                    )

                # ── ValueError: range checks ───────────────────────
                if age is not None and age < 0:
                    raise ValueError(f"age must be non-negative, got {age}")
                if salary < 0:
                    raise ValueError(
                        f"salary must be non-negative, got {salary}"
                    )

                result.record_success({
                    "name":   name,
                    "age":    age,
                    "salary": float(salary),
                })

            except KeyError as e:
                result.record_failure(row_num, f"missing field {e}")
            except TypeError as e:
                result.record_failure(row_num, str(e))
            except ValueError as e:
                result.record_failure(row_num, str(e))

        return result

    # -----------------------------------------------------------
    # STEP 4 — import_from_file
    # -----------------------------------------------------------

    def import_from_file(self, filepath: str) -> ImportResult:
        """
        Read a file from disk and route it to the right importer.

        Exception types handled:
          FileNotFoundError — the path does not exist
          PermissionError   — we do not have read access
          ValueError        — unsupported file extension
        """
        result = ImportResult(filepath)

        # ── Read the file ──────────────────────────────────────────
        # We separate the file I/O from the parsing so each error
        # type is handled in the right place.
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                contents = f.read()
        except FileNotFoundError:
            # The path simply doesn't exist — record it, return early.
            result.errors.append(f"File not found: {filepath}")
            return result
        except PermissionError:
            result.errors.append(f"Permission denied: {filepath}")
            return result

        # ── Route by extension ─────────────────────────────────────
        # We delegate to the format-specific methods so the per-row
        # error handling lives in one place.
        if filepath.endswith(".csv"):
            return self.import_csv(contents)
        elif filepath.endswith(".json"):
            return self.import_json(contents)
        else:
            # We raise ValueError here because this is a programming
            # error (the caller chose a bad extension), not a data error.
            raise ValueError(
                f"Unsupported file extension in {filepath!r}. "
                "Only .csv and .json are supported."
            )


# ===========================================================
# STEP 5 — print_report
#
# A standalone function (not a method) because it doesn't need
# any state — it only reads from the ImportResult it receives.
# ===========================================================

def print_report(result: ImportResult, source_name: str) -> None:
    """
    Print a formatted summary of one import operation.
    Shows counts, all error messages, and a preview of valid records.
    """
    print(f"\nImport Report — {source_name}")
    print(f"  {'Rows processed':<20}: {result.rows_processed}")
    print(f"  {'Successful':<20}: {result.successful}")
    print(f"  {'Failed':<20}: {result.failed}")

    if result.errors:
        print("  Errors:")
        for err in result.errors:
            print(f"    • {err}")
    else:
        print("  No errors — all rows imported cleanly.")

    if result.records:
        preview_count = min(3, len(result.records))
        print(f"  Preview of valid records ({preview_count} shown):")
        for rec in result.records[:preview_count]:
            age_str = str(rec.get("age", "N/A"))
            print(f"    {rec['name']:<12} age={age_str:<5} "
                  f"salary=${rec['salary']:,.2f}")


# ===========================================================
# STEP 6 — main()
#
# Demonstrates all four import scenarios automatically.
# Notice that the program NEVER crashes — every error is caught,
# recorded, and reported cleanly.
# ===========================================================

def main():
    print("=" * 60)
    print("DATA IMPORT TOOL — Phase 06 Error Handling Project")
    print("=" * 60)

    importer = DataImporter()

    # ── Scenario 1: CSV with deliberate errors ─────────────────
    print("\n" + "─" * 60)
    print("Scenario 1: SAMPLE_CSV (mix of valid and invalid rows)")
    print("─" * 60)
    # Rows 2, 3, and 5 intentionally contain bad data so we can
    # see how the importer handles each error type separately.
    csv_result = importer.import_csv(SAMPLE_CSV)
    print_report(csv_result, "SAMPLE_CSV")

    # ── Scenario 2: JSON with deliberate errors ─────────────────
    print("\n" + "─" * 60)
    print("Scenario 2: SAMPLE_JSON (mix of valid and invalid records)")
    print("─" * 60)
    # Frank is valid; Grace has a string salary; Heidi has no salary key.
    json_result = importer.import_json(SAMPLE_JSON)
    print_report(json_result, "SAMPLE_JSON")

    # ── Scenario 3: Completely invalid JSON ─────────────────────
    print("\n" + "─" * 60)
    print("Scenario 3: BAD_JSON (unparseable JSON string)")
    print("─" * 60)
    # BAD_JSON uses unquoted keys — not valid JSON.
    # json.JSONDecodeError is caught and recorded; no rows can be processed.
    bad_result = importer.import_json(BAD_JSON)
    print_report(bad_result, "BAD_JSON")

    # ── Scenario 4: Non-existent file ───────────────────────────
    print("\n" + "─" * 60)
    print("Scenario 4: import_from_file('nonexistent.csv')")
    print("─" * 60)
    # The file doesn't exist — FileNotFoundError is caught and recorded.
    file_result = importer.import_from_file("nonexistent.csv")
    print_report(file_result, "nonexistent.csv")

    print("\n" + "=" * 60)
    print("All scenarios complete.")
    print("Key takeaway: every error was caught, recorded, and reported.")
    print("The program never crashed — that is the goal of robust")
    print("error handling.")
    print("=" * 60)


if __name__ == "__main__":
    main()
