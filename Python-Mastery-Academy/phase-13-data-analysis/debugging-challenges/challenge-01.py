"""
Debugging Challenge 01 — Phase 13: Data Analysis
=================================================

INSTRUCTIONS:
  This file contains 7 bugs.
  Find and fix every bug.
  Run the file — when all bugs are fixed it will print 'All bugs fixed!'

HINTS:
  - Read every error message carefully — it tells you the line and type of error
  - Common issues: wrong axis argument, method called on wrong type,
    wrong data type for a calculated value, wrong column name,
    wrong comparison operator, missing function call, bad file path
  - Try to fix one bug at a time, run the file, then fix the next

DO NOT LOOK AT THE ANSWERS BELOW UNTIL YOU'VE TRIED!
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend so script can run headlessly
import matplotlib.pyplot as plt
import os

# ── Set up sample data ─────────────────────────────────────────────

csv_content = """name,department,salary,units_sold
Alice,Sales,55000,120
Bob,IT,72000,0
Carol,Sales,61000,95
David,HR,48000,30
Eva,IT,80000,0
Frank,Sales,59000,110
"""

# Write CSV to a temp file so pd.read_csv can open it
with open("debug_data.csv", "w") as f:
    f.write(csv_content)

# === BUG HUNT BEGIN ===

# BUG 1: pd.read_csv called on a path that does not exist
df = pd.read_csv("wrong_path_data.csv")          # BUG 1: wrong file path

# BUG 2: .mean() called on the entire DataFrame instead of a single column
avg_salary = df.mean()                            # BUG 2: should be df["salary"].mean()
print(f"Average salary: ${avg_salary:,.2f}")

# BUG 3: using int() instead of float() for a computed value
# The salary ratio will silently truncate to 0 for anyone earning less than the mean
salary_ratio = int(df["salary"].mean()) / 100000  # BUG 3: should use float(), not int()
print(f"Salary ratio vs 100k: {salary_ratio:.4f}")

# BUG 4: wrong column name in bracket notation
# The column is called 'units_sold', not 'units'
top_sellers = df[df["units"] > 50]               # BUG 4: should be df["units_sold"] > 50
print(f"Top sellers:\n{top_sellers[['name','units_sold']]}")

# BUG 5: using = (assignment) instead of == (comparison) in boolean filter
# This will raise a SyntaxError in recent Python versions
sales_team = df[df["department"] = "Sales"]      # BUG 5: should be == not =
print(f"Sales team:\n{sales_team[['name','salary']]}")

# BUG 6: wrong axis kwarg — axis=1 drops columns, axis=0 drops rows
# We want to drop rows that have any NaN, not columns
df_clean = df.dropna(axis=1)                     # BUG 6: should be axis=0
print(f"Shape after dropna: {df_clean.shape}")

# BUG 7: plt.show() is missing — the chart is created but never displayed
dept_counts = df["department"].value_counts()
plt.bar(dept_counts.index, dept_counts.values, color="steelblue")
plt.title("Headcount by Department")
plt.xlabel("Department")
plt.ylabel("Count")
plt.tight_layout()
# BUG 7: plt.show() call is missing here

# Clean up the temp file
if os.path.exists("debug_data.csv"):
    os.remove("debug_data.csv")

print("All bugs fixed!")


# ====================================================================
# ANSWERS (don't scroll until you've tried!)
# ====================================================================
#
# BUG 1: Change "wrong_path_data.csv" → "debug_data.csv"
#        pd.read_csv raises FileNotFoundError if the path doesn't exist.
#        Fix: wrap in try/except or use the correct filename.
#
# BUG 2: Change  df.mean()  →  df["salary"].mean()
#        df.mean() returns a Series of means for ALL numeric columns,
#        not a scalar. Calling f"${avg_salary:,.2f}" would fail.
#
# BUG 3: Change  int(df["salary"].mean())  →  float(df["salary"].mean())
#        int() truncates the decimal part. float() preserves precision.
#        For salary data this can introduce a significant calculation error.
#
# BUG 4: Change  df["units"]  →  df["units_sold"]
#        "units" does not exist as a column — Pandas raises a KeyError.
#
# BUG 5: Change  df["department"] = "Sales"  →  df["department"] == "Sales"
#        Single = is assignment, not comparison. Use == inside boolean filters.
#
# BUG 6: Change  axis=1  →  axis=0
#        axis=0 drops rows (default); axis=1 drops columns.
#        We want to remove rows with NaN, not entire columns.
#
# BUG 7: Add  plt.show()  after plt.tight_layout()
#        Without plt.show() the figure is created in memory but never rendered.
#
# ====================================================================
