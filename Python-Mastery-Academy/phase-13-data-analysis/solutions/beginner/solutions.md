# Phase 13 — Beginner Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/beginner/exercises.md`

---

## A1. Create and Inspect a NumPy Array

```python
import numpy as np

# Create a 1-D array of 8 integers
arr = np.array([12, 45, 7, 89, 23, 56, 34, 78])

# Print key attributes and statistics
print(f"Shape:  {arr.shape}")   # (8,) — one dimension with 8 elements
print(f"DType:  {arr.dtype}")   # int64 on most systems
print(f"Sum:    {arr.sum()}")   # adds all elements
print(f"Mean:   {arr.mean()}")  # sum / count
print(f"Max:    {arr.max()}")   # largest element
print(f"Min:    {arr.min()}")   # smallest element
```

Output:
```
Shape:  (8,)
DType:  int64
Sum:    344
Mean:   43.0
Max:    89
Min:    7
```

---

## A2. Build a DataFrame and Explore It

```python
import pandas as pd

# Build the DataFrame from a plain Python dictionary
data = {
    "name":   ["Alice", "Bob", "Carol", "David", "Eva"],
    "age":    [25, 30, 22, 35, 28],
    "score":  [88.5, 92.0, 76.5, 95.0, 83.5],
    "passed": [True, True, False, True, True]
}
df = pd.DataFrame(data)

# First three rows
print("--- head(3) ---")
print(df.head(3))

# Column names, non-null counts, and dtypes
print("\n--- info() ---")
df.info()

# Count, mean, std, min, max etc. for numeric columns
print("\n--- describe() ---")
print(df.describe())
```

`.head(3)` returns the first 3 rows by index.
`.info()` is printed directly — it uses its own output stream.
`.describe()` skips boolean and string columns by default; pass `include="all"` to include them.

---

## A3. Read a CSV File

```python
import pandas as pd

# Hard-code the CSV content as a Python string
csv_content = """product,units_sold,price
Laptop,12,899.99
Mouse,45,19.99
Keyboard,30,49.99
Monitor,8,349.99
Headset,22,79.99
Webcam,18,59.99
USB Hub,35,29.99
"""

# Write the string to disk so pd.read_csv can open it
with open("sample_sales.csv", "w") as f:
    f.write(csv_content)

# Read it back — Pandas infers column names from the header row
df = pd.read_csv("sample_sales.csv")

# Print the first 5 rows (default for .head())
print(df.head())
```

Output:
```
    product  units_sold   price
0    Laptop          12  899.99
1     Mouse          45   19.99
2  Keyboard          30   49.99
3   Monitor           8  349.99
4   Headset          22   79.99
```

---

## A4. Column Selection and Basic Statistics

```python
import pandas as pd

# Re-create the DataFrame (or use the file from A3)
csv_content = """product,units_sold,price
Laptop,12,899.99
Mouse,45,19.99
Keyboard,30,49.99
Monitor,8,349.99
Headset,22,79.99
Webcam,18,59.99
USB Hub,35,29.99
"""
with open("sample_sales.csv", "w") as f:
    f.write(csv_content)

df = pd.read_csv("sample_sales.csv")

# Select the units_sold column — returns a Series
units = df["units_sold"]

# Compute statistics on the Series
print(f"Mean units sold:  {units.mean():.2f}")  # average
print(f"Max units sold:   {units.max()}")        # highest value
print(f"Min units sold:   {units.min()}")        # lowest value
```

---

## A5. Simple Bar Chart

```python
import matplotlib.pyplot as plt

# Data
months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales  = [12000, 15500, 9800, 18200, 21000]

# Create the bar chart
plt.bar(months, sales, color="steelblue")   # one bar per month

# Labels and title
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Sales ($)")

# Prevent label clipping and display
plt.tight_layout()
plt.show()
```

`plt.bar(x, height)` draws one vertical bar per element of `x`.
`plt.tight_layout()` adjusts padding so nothing is clipped.
`plt.show()` renders the figure window.
