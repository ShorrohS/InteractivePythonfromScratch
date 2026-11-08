# Lesson 03 — Pandas Fundamentals

**Phase:** 13 — Data Analysis | **Time:** ~50 min

---

## Part 1: Series vs DataFrame

```python
import pandas as pd

# Series — 1D labeled array (like a single spreadsheet column)
salaries = pd.Series([85000, 65000, 92000, 71000], name="salary")
print(salaries.dtype)    # int64
print(salaries.mean())   # 78250.0
print(salaries[0])       # 85000

# Series with a custom index (labels instead of 0,1,2...)
ratings = pd.Series(
    [4.8, 3.9, 4.5],
    index=["Alice", "Bob", "Carol"],
    name="performance"
)
print(ratings["Alice"])   # 4.8

# DataFrame — 2D table (like an entire spreadsheet)
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol", "Dave"],
    "dept":   ["Eng",   "Sales", "Eng", "HR"],
    "salary": [85000, 65000, 92000, 71000],
    "active": [True,  True,  False,  True]
})

# A DataFrame column IS a Series
print(type(df["salary"]))   # <class 'pandas.core.series.Series'>
```

---

## Part 2: Reading Files with `pd.read_csv()`

```python
import pandas as pd

# Basic read
df = pd.read_csv("employees.csv")

# Common parameters
df = pd.read_csv(
    "employees.csv",
    sep=",",              # delimiter (use sep="\t" for TSV)
    header=0,             # row index to use as column names (0 = first row)
    index_col="emp_id",   # use a column as the row index
    dtype={"salary": float, "dept": str},   # force data types
    parse_dates=["hire_date", "exit_date"],  # auto-parse date columns
    encoding="utf-8",     # file encoding
    nrows=1000            # only load first 1000 rows (great for testing)
)

# Read Excel files — same API, different function
df = pd.read_excel("employees.xlsx", sheet_name="Staff")

# After reading, always check what you got
print(df.shape)
print(df.dtypes)
print(df.head())
```

---

## Part 3: Selecting Data

```python
import pandas as pd

df = pd.read_csv("employees.csv")

# Single column → returns a Series
names   = df["name"]
salaries = df["salary"]

# Multiple columns → returns a DataFrame
subset = df[["name", "dept", "salary"]]

# loc[] — label-based selection (row label, column name)
df.loc[0]                           # entire first row as Series
df.loc[0, "name"]                   # single cell: row 0, column "name"
df.loc[0:3, ["name", "salary"]]     # rows 0-3, two columns

# iloc[] — position-based selection (integer index)
df.iloc[0]          # first row
df.iloc[0, 1]       # first row, second column
df.iloc[:5, :3]     # first 5 rows, first 3 columns
df.iloc[-1]         # last row

# Key difference:
# loc[0:3] includes row 3  (label-based, inclusive)
# iloc[0:3] excludes row 3 (position-based, like Python slicing)
```

---

## Part 4: Filtering Rows

```python
import pandas as pd

df = pd.read_csv("employees.csv")

# Single condition
eng_team  = df[df["dept"] == "Engineering"]
high_pay  = df[df["salary"] > 80000]
active    = df[df["active"] == True]

# Multiple conditions — use & (and) and | (or), always parenthesise
eng_senior = df[(df["dept"] == "Engineering") & (df["salary"] > 80000)]
sales_or_hr = df[(df["dept"] == "Sales") | (df["dept"] == "HR")]

# NOT condition
non_eng = df[df["dept"] != "Engineering"]

# isin() — match a list of values
key_depts = df[df["dept"].isin(["Engineering", "Finance"])]

# between() — numeric range
mid_range = df[df["salary"].between(60000, 90000)]

# Filter using string methods
j_names = df[df["name"].str.startswith("J")]
managers = df[df["title"].str.contains("Manager", na=False)]
```

---

## Part 5: Adding, Sorting, and Counting

```python
import pandas as pd

df = pd.read_csv("employees.csv")

# Add a new column
df["annual_bonus"]  = df["salary"] * 0.10
df["total_comp"]    = df["salary"] + df["annual_bonus"]
df["seniority_tag"] = df["years"].apply(lambda y: "Senior" if y >= 5 else "Junior")

# Sort rows
df_sorted = df.sort_values("salary", ascending=False)
df_sorted = df.sort_values(["dept", "salary"], ascending=[True, False])

# Value counts — frequency of each category
print(df["dept"].value_counts())
print(df["dept"].value_counts(normalize=True).mul(100).round(1))  # as %

# String operations on a column
df["name_upper"]  = df["name"].str.upper()
df["name_clean"]  = df["name"].str.strip().str.title()
df["email_lower"] = df["email"].str.lower()
email_match       = df[df["email"].str.contains("@company.com", na=False)]

# Save results
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", sheet_name="Results", index=False)
```

---

## Part 6: Complete Business Example

Load an employees CSV, explore it, filter to active employees, add a `total_comp`
column, sort by compensation, and save the top 20 earners to a new file.

```python
import pandas as pd

# --- Step 1: Load ---
df = pd.read_csv("employees.csv", parse_dates=["hire_date"])

# --- Step 2: Explore ---
print(f"Shape: {df.shape}")
print(df.dtypes)
print(df.isnull().sum())

# --- Step 3: Filter to active employees only ---
df_active = df[df["active"] == True].reset_index(drop=True)
print(f"Active employees: {len(df_active)}")

# --- Step 4: Add computed columns ---
df_active["annual_bonus"] = df_active["salary"] * 0.15
df_active["total_comp"]   = df_active["salary"] + df_active["annual_bonus"]

# --- Step 5: Sort by total compensation ---
df_sorted = df_active.sort_values("total_comp", ascending=False)

# --- Step 6: Inspect top earners ---
top20 = df_sorted.head(20)[["name", "dept", "salary", "annual_bonus", "total_comp"]]
print(top20.to_string())

# --- Step 7: Department summary ---
dept_summary = df_active.groupby("dept").agg(
    headcount    = ("name", "count"),
    avg_salary   = ("salary", "mean"),
    total_payroll= ("salary", "sum")
).round(2).sort_values("avg_salary", ascending=False)
print(dept_summary)

# --- Step 8: Save ---
top20.to_csv("top20_earners.csv", index=False)
print("Saved top20_earners.csv")
```

---

## Practice Exercises

1. Load an employees CSV and use `loc[]` to select the first 10 rows and only the `name`,
   `dept`, and `salary` columns. Then do the same using `iloc[]`.

2. Filter a DataFrame to employees in the Engineering or Finance department with salary above
   $75,000. Use `isin()` for the department filter and `&` to combine conditions.

3. Add a `grade` column to a DataFrame: `"A"` if salary > 90000, `"B"` if between 70000–90000,
   and `"C"` otherwise. Use `.apply()` with a lambda or a helper function.

4. Group a sales DataFrame by `region` and compute count, mean revenue, and total revenue per
   region. Sort by total revenue descending and save the result to a CSV.

---

## Next Lesson

**[Lesson 04 → Data Cleaning](lesson-04-data-cleaning.md)**
