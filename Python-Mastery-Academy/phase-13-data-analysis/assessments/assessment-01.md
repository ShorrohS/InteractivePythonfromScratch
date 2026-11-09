# Phase 13 — Completion Assessment: Data Analysis

> Complete before moving to Phase 14.
> Pass mark: 80% | Time: 40 minutes

---

## PART A: Practical Coding Tasks

Use the following hard-coded DataFrame as your starting point for Tasks 1–4.
Do **not** read from a CSV file — build the DataFrame directly in Python.

```python
import pandas as pd
import numpy as np

data = {
    "month":      ["Jan","Feb","Mar","Apr","May",
                   "Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
    "product":    ["Widget","Gadget","Widget","Gadget","Widget",
                   "Gadget","Widget","Gadget","Widget","Gadget","Widget","Gadget"],
    "region":     ["North","South","East","North","South",
                   "East","North","South","East","North","South","East"],
    "units_sold": [120, 85, 200, 150, 60,
                   175, 130, 95, 210, 140, 80, 165],
    "revenue":    ["$6000","$4250","$10000","$7500","$3000",
                   "$8750","$6500","$4750","$10500","$7000","$4000","$8250"]
}
df = pd.DataFrame(data)
```

---

### Task 1: Load and Explore (20 marks)

Using only the DataFrame `df` defined above, print:

1. The shape of the DataFrame
2. The dtypes of each column
3. The number of missing values per column (`.isnull().sum()`)
4. The statistical summary (`.describe()`) — you should notice that `units_sold` appears but `revenue` does not (why?)

Answer the follow-up question in a comment: **Why does `revenue` not appear in `.describe()` by default?**

---

### Task 2: Clean the Data (25 marks)

Start from a fresh copy of `df`:

```python
df_dirty = df.copy()

# Introduce 2 rows with NaN
df_dirty.loc[12] = ["Jan", "Widget", "North", np.nan, "$5000"]
df_dirty.loc[13] = ["Feb", "Gadget", "South", np.nan, "$4250"]

# Introduce a duplicate row
df_dirty.loc[14] = df_dirty.loc[0].values
```

Perform all of the following:
1. Drop duplicate rows
2. Fill NaN values in `units_sold` with `0`
3. Convert the `revenue` column from strings like `"$6000"` to proper float values
   (remove the `$` sign, then cast to float)

After cleaning, print the cleaned DataFrame and confirm:
- No duplicates remain
- No NaN values remain
- `revenue` dtype is `float64`

---

### Task 3: Analyse (30 marks)

Using your cleaned DataFrame from Task 2:

1. Group by `region` and compute:
   - Total revenue per region
   - Average `units_sold` per region
   Print the result sorted by total revenue descending.

2. Find the **month with the highest total revenue** across all products.
   Print: `"Best month: <month> ($<revenue>)"`

3. Filter the DataFrame to show only rows where `units_sold > 50`.
   Print the filtered DataFrame.

---

### Task 4: Visualise (25 marks)

1. **Bar chart** — total revenue by region.
   - Title: `"Total Revenue by Region"`
   - X-axis: `"Region"`, Y-axis: `"Revenue ($)"`

2. **Line chart** — monthly revenue trend (x = month in order, y = revenue per row).
   - Title: `"Monthly Revenue Trend"`
   - X-axis: `"Month"`, Y-axis: `"Revenue ($)"`
   - Rotate x-axis labels 45° for readability: `plt.xticks(rotation=45)`

Both charts must include `plt.tight_layout()` and `plt.show()`.

---

## PART B: Written Questions

**Q5.** Explain the difference between a NumPy array and a Pandas Series.
Give one scenario where you would choose each.

---

**Q6.** What is the `SettingWithCopyWarning` in Pandas, and what does it warn you about?
Show an example of code that triggers it and the correct fix.

---

**Q7.** What does `how="left"` mean in `pd.merge()` and when would you use it instead
of `how="inner"`? Give a real-world example.

---

**Q8.** Describe the two-step process for computing grouped statistics with `groupby()`.
What does `df.groupby("region").agg({"revenue": "sum", "units": "mean"})` do?

---

## Scoring

| Score     | Action |
|-----------|--------|
| 80–100 %  | Move to Phase 14 |
| 65–79 %   | Review weak areas, then proceed |
| < 65 %    | Redo Phase 13 lessons before continuing |

---

## Answer Key

### Task 1 expected code

```python
print("Shape:", df.shape)
print("\nDtypes:\n", df.dtypes)
print("\nMissing values:\n", df.isnull().sum())
print("\nDescribe:\n", df.describe())

# revenue is object (string) dtype because the values contain "$" — Pandas
# cannot infer numeric type. .describe() only processes numeric columns by default.
```

### Task 2 expected code

```python
df_clean = df_dirty.copy()

# 1. Drop duplicates
df_clean.drop_duplicates(inplace=True)

# 2. Fill NaN units_sold with 0
df_clean["units_sold"] = df_clean["units_sold"].fillna(0)

# 3. Strip "$" and convert revenue to float
df_clean["revenue"] = df_clean["revenue"].str.replace("$", "", regex=False).astype(float)

print(df_clean)
print("\nDuplicates:", df_clean.duplicated().sum())     # 0
print("NaN count:\n", df_clean.isnull().sum())         # all 0
print("revenue dtype:", df_clean["revenue"].dtype)     # float64
```

### Task 3 expected code

```python
# 1. GroupBy region
region_stats = (
    df_clean.groupby("region")
            .agg(total_revenue=("revenue", "sum"),
                 avg_units=("units_sold", "mean"))
            .sort_values("total_revenue", ascending=False)
)
print(region_stats)

# 2. Best month
best_idx   = df_clean.groupby("month")["revenue"].sum().idxmax()
best_rev   = df_clean.groupby("month")["revenue"].sum().max()
print(f"Best month: {best_idx} (${best_rev:,.0f})")

# 3. Filter units_sold > 50
active = df_clean[df_clean["units_sold"] > 50]
print(active)
```

### Task 4 expected code

```python
import matplotlib.pyplot as plt

# Bar chart — revenue by region
region_rev = df_clean.groupby("region")["revenue"].sum()
plt.bar(region_rev.index, region_rev.values, color="steelblue")
plt.title("Total Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.show()

# Line chart — monthly revenue trend
plt.plot(df_clean["month"], df_clean["revenue"], marker="o", color="darkorange")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### Q5 answer

A **NumPy array** is a fixed-type, multi-dimensional container optimised for numeric operations (fast math, linear algebra). A **Pandas Series** is a one-dimensional labelled array built on top of NumPy that supports mixed-operation workflows, missing values, and named indexes. Choose NumPy for pure numeric computation (e.g., matrix operations, machine learning inputs); choose Series/DataFrame when working with labelled, tabular, or heterogeneous data.

### Q6 answer

`SettingWithCopyWarning` warns that you are trying to modify a DataFrame that may be a copy (a view) of another DataFrame. The change might not apply to the original. Trigger example:

```python
subset = df[df["region"] == "North"]
subset["revenue"] = 0   # warns — subset may be a copy
```

Fix — use `.copy()` to make an explicit copy, or use `.loc[]` on the original:

```python
subset = df[df["region"] == "North"].copy()
subset["revenue"] = 0   # safe — modifying an independent copy
```

### Q7 answer

`how="left"` returns every row from the **left** DataFrame plus any matching rows from the right. Rows in the left with no match in the right get NaN for right-side columns. Use it when you want to keep all records from one table regardless of whether a match exists — e.g., all customers even if they haven't placed an order yet.

### Q8 answer

`groupby("region")` splits the DataFrame into one group per unique region value. `.agg(...)` applies an aggregation function to each group. The dict form `{"revenue": "sum", "units": "mean"}` applies `sum` to the `revenue` column and `mean` to the `units` column independently, returning a new DataFrame indexed by region.
