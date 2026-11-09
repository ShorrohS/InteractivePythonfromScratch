# 📝 Phase 13 — Advanced Exercises: Data Analysis

> Difficulty: ⭐⭐⭐ | Think before you code. Plan on paper first.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. End-to-End Data Pipeline**

Build a complete pipeline in a single script that covers every stage:

**Stage 1 — Load.** Write these two CSV strings to disk (`employees.csv` and
`departments.csv`), then load them with `pd.read_csv()`.

```
employees.csv
emp_id,name,dept_id,salary,hire_date
1,Alice,10,72000,2019-03-15
2,Bob,20,85000,2018-07-01
3,Carol,10,91000,2020-11-20
4,David,30,63000,2021-01-08
5,Eva,20,78000,2017-05-30
6,Frank,10,,2022-02-14
7,Grace,30,54000,2020-09-01
8,Henry,,69000,2019-06-12
```

```
departments.csv
dept_id,dept_name,budget
10,Engineering,500000
20,Marketing,300000
30,HR,200000
```

**Stage 2 — Clean.**
- Drop any row where both `emp_id` and `name` are NaN
- Fill missing `salary` with the median salary
- Fill missing `dept_id` with `0`
- Convert `hire_date` to a proper datetime column

**Stage 3 — Merge.**
- Left-join employees onto departments on `dept_id`
- Fill any `dept_name` that is NaN (e.g., dept_id 0) with `"Unknown"`

**Stage 4 — Aggregate.**
- Group by `dept_name`; compute headcount (`count`), mean salary (`mean`),
  and total salary spend (`sum`)
- Print the aggregated table

**Stage 5 — Chart.**
- Create a horizontal bar chart showing total salary spend per department
- Title, axis labels, `tight_layout()`, `show()`

> 💡 Hint: Use `pd.to_datetime()` for the date column. Chain `.fillna()` after `.merge()` for the dept_name step.

---

**Q2. Pivot Table**

Load (or re-create) a sales dataset with columns:
`region`, `product`, `quarter`, `units_sold`, `revenue`.

Use at least 16 rows covering 2 regions (`"North"`, `"South"`),
3 products (`"A"`, `"B"`, `"C"`), and 4 quarters (`"Q1"`–`"Q4"`).

Tasks:
1. Create a pivot table with `region` as rows, `product` as columns, and
   `revenue` as values (aggregation: `sum`). Print it.
2. Create a second pivot table with `quarter` as rows, `region` as columns,
   and `units_sold` as values (aggregation: `mean`). Print it.
3. Using the first pivot table, answer in a `print()` statement:
   - Which product generated the highest total revenue?
   - Which region generated more total revenue?

> 💡 Hint: `pd.pivot_table(df, values="revenue", index="region", columns="product", aggfunc="sum")`.

---

**Q3. Date Column Analysis — Monthly Trends**

Create a DataFrame representing 24 months of website traffic:

```python
import pandas as pd, numpy as np
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")
np.random.seed(0)
df = pd.DataFrame({
    "date":     dates,
    "visits":   np.random.randint(8000, 25000, 24),
    "signups":  np.random.randint(50, 500, 24),
    "revenue":  np.random.uniform(5000, 30000, 24).round(2)
})
```

Tasks:
1. Set `date` as the index
2. Extract `year` and `month` into new columns
3. Group by `year` to compute total `visits`, total `signups`, and mean `revenue` per year
4. Find the month with the highest `revenue`
5. Plot a line chart of monthly `revenue` over time (x = date index, y = revenue)
6. Calculate the month-over-month percentage change in `visits` using `.pct_change()`

> 💡 Hint: `df["date"].dt.month` extracts the month number. `.pct_change() * 100` gives percentage.

---

**Q4. Reusable Data-Cleaning Function**

Write a function `clean_dataframe(df)` that accepts any DataFrame and applies
the following cleaning steps in order:
1. Strip leading/trailing whitespace from all **string** columns
   (use `.apply()` with a `lambda` on object-dtype columns)
2. Standardise string columns to **Title Case**
3. Drop fully duplicate rows
4. Replace any value of `"N/A"`, `"n/a"`, `"NA"`, `"-"`, or `""` (empty string)
   with `np.nan` in string columns
5. Print a summary: how many duplicates were removed, how many NaN values exist
   per column after cleaning

Demonstrate the function by creating a messy test DataFrame:

```python
messy = pd.DataFrame({
    "name":    ["  alice ", "Bob", "alice ", "  CAROL", "David"],
    "city":    ["london", "paris  ", "London", "N/A", "-"],
    "score":   [85, 90, 85, 78, 92],
    "comment": ["good", "NA", "good", "", "excellent"]
})
```

Call `clean_dataframe(messy)` and print the cleaned result.

> 💡 Hint 1: `df.select_dtypes(include="object")` returns only string columns.
> 💡 Hint 2: `df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)` applies stripping across all columns.

---

**Q5. 2×2 Subplot Figure**

Using the sales data from Q2 (or similar), build a single figure with
a 2×2 grid of subplots:

- **Top-left:** Bar chart — total revenue by region
- **Top-right:** Horizontal bar chart — revenue by product
- **Bottom-left:** Line chart — revenue by quarter for each region
  (two lines, one per region, with a legend)
- **Bottom-right:** Pie chart — share of total revenue by product

Requirements:
- Figure size: `(12, 8)`
- Each subplot has its own title, x-axis label, and y-axis label
- `plt.suptitle("Sales Analysis Dashboard")` as the figure title
- `plt.tight_layout()` before `plt.show()`

> 💡 Hint: `fig, axes = plt.subplots(2, 2, figsize=(12, 8))`.
> Access each subplot as `axes[0][0]`, `axes[0][1]`, `axes[1][0]`, `axes[1][1]`.

---

**Q6. Rolling Averages on a Time Series**

Using the monthly revenue data from Q3 (or recreate a 36-month series):

1. Calculate a **3-month rolling average** of `revenue`
2. Calculate a **6-month rolling average** of `revenue`
3. Plot the original `revenue` (faint/transparent line), the 3-month MA, and
   the 6-month MA on the same axes with a legend
4. Print the month where the 3-month rolling average was at its peak

> 💡 Hint: `df["revenue"].rolling(window=3).mean()` computes the rolling average.
> The first `window - 1` values will be NaN — that's expected.

---

**Q7. Export to CSV and JSON**

Build on the cleaned, merged, aggregated DataFrame from Q1 (or reproduce it):

1. Export the **cleaned employee-department DataFrame** to `"employees_clean.csv"`
   without the index
2. Compute a summary dictionary:
   ```python
   summary = {
       "total_employees": <int>,
       "avg_salary": <float rounded to 2>,
       "total_salary_spend": <float rounded to 2>,
       "departments": <list of unique dept names>,
       "generated_at": <today's date as string YYYY-MM-DD>
   }
   ```
3. Export the summary to `"summary.json"` (indented, human-readable)
4. Read both files back and print confirmation that the row/key counts match

> 💡 Hint 1: `df.to_csv("file.csv", index=False)` suppresses the integer index.
> 💡 Hint 2: `import json; json.dump(summary, f, indent=4)` writes formatted JSON.
> 💡 Hint 3: `datetime.date.today().isoformat()` produces the `YYYY-MM-DD` string.

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
