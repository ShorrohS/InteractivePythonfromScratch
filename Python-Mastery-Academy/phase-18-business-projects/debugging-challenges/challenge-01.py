"""
Debugging Challenge 01 — Phase 18: Business Projects
=====================================================

CONTEXT:
  This script is a simple expense report generator for a small company.
  It loads expenses from a JSON file, reads a transactions CSV, computes
  category totals, and writes a summary report.

  The script has 7 bugs. Find and fix every one of them.
  When all bugs are fixed, the script will print:
      "✅ All 7 bugs fixed — report generated successfully!"

INSTRUCTIONS:
  1. Read the whole script before changing anything.
  2. Fix one bug at a time and note what you changed.
  3. Do NOT look at the answer section until you have tried!

BUGS TO FIND:
  Bug 1: Logger created but no output appears anywhere
  Bug 2: Config value always reads as None even when set
  Bug 3: CSV data is empty on second read
  Bug 4: A file-not-found error is silently swallowed
  Bug 5: Category totals accumulate across multiple function calls
  Bug 6: Report file may not be closed if an error occurs during writing
  Bug 7: Average calculation crashes when there are no transactions
"""

import os
import csv
import json
import logging
from pathlib import Path

# ── Logging setup ────────────────────────────────────────────────────────────────

# Bug 1: A logger is created here but it has no handlers and basicConfig() was
#        never called. All log messages vanish silently.
logger = logging.getLogger("expense_report")


# ── Configuration ────────────────────────────────────────────────────────────────

def load_dotenv_simulation():
    """Simulate what python-dotenv's load_dotenv() does."""
    os.environ["REPORT_TITLE"]   = "Monthly Expense Report"
    os.environ["COMPANY_NAME"]   = "Acme Corp"
    os.environ["OUTPUT_DIR"]     = "reports"

# Bug 2: The config value is read BEFORE load_dotenv_simulation() is called,
#        so REPORT_TITLE is not yet in os.environ — it will always be None.
REPORT_TITLE = os.environ.get("REPORT_TITLE")

load_dotenv_simulation()


# ── Sample data helpers ───────────────────────────────────────────────────────────

SAMPLE_CSV = "transactions.csv"
SAMPLE_JSON = "expenses.json"

def create_sample_files():
    """Write sample CSV and JSON files to disk for testing."""
    csv_data = """date,description,amount,category
2024-01-05,Office supplies,45.99,supplies
2024-01-10,Team lunch,87.50,meals
2024-01-12,Software licence,120.00,software
2024-01-15,Printer paper,23.00,supplies
2024-01-20,Client dinner,210.00,meals
"""
    Path(SAMPLE_CSV).write_text(csv_data, encoding="utf-8")

    json_data = [
        {"id": 1, "month": "2024-01", "budget": 500.00},
        {"id": 2, "month": "2024-02", "budget": 500.00},
    ]
    Path(SAMPLE_JSON).write_text(json.dumps(json_data, indent=2), encoding="utf-8")


# ── CSV reading ───────────────────────────────────────────────────────────────────

def read_transactions(filepath: str) -> list[dict]:
    """Read all transactions from a CSV file and return a list of dicts."""
    transactions = []
    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            # Bug 3: csv.DictReader is assigned to a variable and then iterated
            #        inside a comprehension. Then the SAME reader object is
            #        iterated again in the for-loop below. The second iteration
            #        yields nothing because the reader is already exhausted.
            reader = csv.DictReader(f)
            _ = [row for row in reader]    # first pass — consumes the iterator

            for row in reader:             # second pass — yields nothing
                row["amount"] = float(row["amount"])
                transactions.append(row)

    except FileNotFoundError as exc:
        # Bug 4: The exception is caught and silently swallowed with pass.
        #        The caller gets an empty list with no indication of what went wrong.
        pass

    return transactions


# ── Business logic ────────────────────────────────────────────────────────────────

# Bug 5: Mutable default argument — the transactions list is created ONCE when
#        Python loads the module, not on each call. Every call that uses the
#        default shares the same list object, so totals accumulate across calls.
def calculate_totals(transactions=[]) -> dict:
    """Sum transaction amounts by category."""
    totals: dict[str, float] = {}
    for txn in transactions:
        cat = txn.get("category", "uncategorised")
        totals[cat] = totals.get(cat, 0.0) + txn["amount"]
    return totals


def calculate_average(transactions: list[dict]) -> float:
    """Return the average transaction amount."""
    # Bug 7: If transactions is empty, len() returns 0 and this raises ZeroDivisionError.
    #        No guard exists for the empty-list case.
    return sum(t["amount"] for t in transactions) / len(transactions)


# ── Report writing ────────────────────────────────────────────────────────────────

def write_report(totals: dict, average: float, output_path: str) -> None:
    """Write a plain-text expense summary report to a file."""
    # Bug 6: The file is opened without a context manager (no 'with' statement).
    #        If an exception occurs during writing, the file handle is never
    #        closed — this can corrupt the file or hold a lock on Windows.
    f = open(output_path, "w", encoding="utf-8")
    f.write(f"=== {REPORT_TITLE} ===\n\n")
    f.write("Category Totals:\n")
    for category, total in sorted(totals.items()):
        f.write(f"  {category:<20} ${total:,.2f}\n")
    f.write(f"\nAverage transaction: ${average:.2f}\n")
    f.close()


# ── Main ──────────────────────────────────────────────────────────────────────────

def main():
    create_sample_files()
    logger.info("Starting expense report generation")

    transactions = read_transactions(SAMPLE_CSV)
    logger.info("Loaded %d transactions", len(transactions))

    if not transactions:
        logger.error("No transactions loaded — cannot generate report")
        return

    totals  = calculate_totals(transactions)
    average = calculate_average(transactions)

    output_dir = Path(os.environ.get("OUTPUT_DIR", "reports"))
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "expense_summary.txt"

    write_report(totals, average, str(output_path))
    logger.info("Report written to %s", output_path)
    print(f"Report saved: {output_path.resolve()}")
    print("✅ All 7 bugs fixed — report generated successfully!")


if __name__ == "__main__":
    main()


# ====================================================================
# ANSWERS  (scroll only after you have tried!)
# ====================================================================
#
# Bug 1 — Logger has no output:
#   Add before the logger line (or inside main()):
#     logging.basicConfig(
#         level=logging.DEBUG,
#         format="%(asctime)s | %(levelname)-8s | %(message)s"
#     )
#   Without this, the root logger has no handler and messages are discarded.
#
# Bug 2 — Config value always None:
#   Move the assignment AFTER load_dotenv_simulation() is called:
#     load_dotenv_simulation()
#     REPORT_TITLE = os.environ.get("REPORT_TITLE")   # ← now it's set
#
# Bug 3 — CSV reader exhausted on second pass:
#   Remove the first comprehension and iterate the reader only once:
#     for row in reader:
#         row["amount"] = float(row["amount"])
#         transactions.append(row)
#
# Bug 4 — Silent exception swallowing:
#   Replace 'pass' with a proper log statement:
#     except FileNotFoundError as exc:
#         logger.error("Transactions file not found: %s — %s", filepath, exc)
#
# Bug 5 — Mutable default argument:
#   Use None as the default and assign an empty list inside the function:
#     def calculate_totals(transactions=None) -> dict:
#         if transactions is None:
#             transactions = []
#
# Bug 6 — File not closed on exception:
#   Use a context manager:
#     with open(output_path, "w", encoding="utf-8") as f:
#         f.write(...)
#         ...
#
# Bug 7 — ZeroDivisionError on empty list:
#   Add a guard before dividing:
#     if not transactions:
#         return 0.0
#     return sum(t["amount"] for t in transactions) / len(transactions)
#
# ====================================================================
