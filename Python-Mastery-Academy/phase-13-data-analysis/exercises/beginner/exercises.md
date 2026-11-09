# 📝 Phase 13 — Beginner Exercises: Data Analysis

> Difficulty: ⭐ | Attempt ALL questions before opening solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

**Q1. Create and Inspect a NumPy Array**

Write a Python script that:
1. Imports NumPy as `np`
2. Creates a 1-D array of 8 integers: `[12, 45, 7, 89, 23, 56, 34, 78]`
3. Prints the array's **shape**, **dtype**, **sum**, **mean**, **max**, and **min**

Expected output:
```
Shape:  (8,)
DType:  int64
Sum:    344
Mean:   43.0
Max:    89
Min:    7
```

> 💡 Hint 1: Use `arr.shape`, `arr.dtype`, `arr.sum()`, `arr.mean()`, `arr.max()`, `arr.min()`.
> 💡 Hint 2: Import NumPy with `import numpy as np` at the top of your script.

---

**Q2. Build a DataFrame and Explore It**

Create a Pandas DataFrame from the following Python dictionary, then print
the first three rows (`.head(3)`), the column info (`.info()`), and a
statistical summary (`.describe()`).

```python
data = {
    "name":   ["Alice", "Bob", "Carol", "David", "Eva"],
    "age":    [25, 30, 22, 35, 28],
    "score":  [88.5, 92.0, 76.5, 95.0, 83.5],
    "passed": [True, True, False, True, True]
}
```

> 💡 Hint 1: `import pandas as pd`, then `df = pd.DataFrame(data)`.
> 💡 Hint 2: `.info()` shows column names, non-null counts, and dtypes. `.describe()` shows numeric statistics.

---

**Q3. Read a CSV File**

First, write a hard-coded CSV string to disk, then read it back with
`pd.read_csv()` and print the first 5 rows.

The CSV should contain three columns — `product`, `units_sold`, `price` — and
at least 7 rows of sample data.

Step-by-step:
1. Write the CSV content to `"sample_sales.csv"` using plain Python file I/O.
2. Read it back with `pd.read_csv("sample_sales.csv")`.
3. Print the first 5 rows with `.head()`.

Expected output (column values will vary, just ensure the shape is right):
```
     product  units_sold  price
0     Laptop          12  899.99
1      Mouse          45   19.99
2   Keyboard          30   49.99
3    Monitor           8  349.99
4    Headset          22   79.99
```

> 💡 Hint 1: Use `with open("sample_sales.csv", "w") as f: f.write(csv_string)`.
> 💡 Hint 2: `pd.read_csv("sample_sales.csv")` automatically infers column names from the header row.

---

**Q4. Column Selection and Basic Statistics**

Using the DataFrame from Q3 (or re-create it), select the `units_sold` column
and compute:
- Mean number of units sold
- Maximum units sold
- Minimum units sold

Print each with a label.

Expected output:
```
Mean units sold:  24.57
Max units sold:   45
Min units sold:   8
```

> 💡 Hint 1: Select a column with `df["column_name"]` — this returns a Pandas Series.
> 💡 Hint 2: A Series has `.mean()`, `.max()`, and `.min()` methods just like NumPy arrays.

---

**Q5. Simple Bar Chart with Matplotlib**

Create a bar chart showing the following monthly sales figures:

```python
months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales  = [12000, 15500, 9800, 18200, 21000]
```

Requirements:
- Title: `"Monthly Sales"`
- X-axis label: `"Month"`
- Y-axis label: `"Sales ($)"`
- Use any bar colour you like
- Call `plt.tight_layout()` before `plt.show()`

> 💡 Hint 1: Use `import matplotlib.pyplot as plt`, then `plt.bar(months, sales)`.
> 💡 Hint 2: Add title and axis labels with `plt.title()`, `plt.xlabel()`, `plt.ylabel()`.

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
