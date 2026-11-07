# Lesson 02 — Pandas Fundamentals

**Phase:** 13 — Data Analysis | **Time:** ~45 min

---

## Part 1: Setup

```bash
pip install pandas openpyxl
```

```python
import pandas as pd
```

---

## Part 2: Creating DataFrames

```python
# From dict
df = pd.DataFrame({
    "name":   ["Alice", "Bob", "Carol"],
    "salary": [85000,   65000,  92000],
    "dept":   ["Eng",   "Sales","Eng"]
})

# From CSV
df = pd.read_csv("employees.csv")

# From Excel
df = pd.read_excel("report.xlsx", sheet_name="Data")

# From list of dicts
data = [{"name": "Alice", "salary": 85000}, {"name": "Bob", "salary": 65000}]
df = pd.DataFrame(data)
```

---

## Part 3: Exploring Data

```python
df.head()             # first 5 rows
df.tail(10)           # last 10 rows
df.shape              # (rows, cols)
df.info()             # dtypes, nulls
df.describe()         # statistics
df.columns            # column names
df.dtypes             # column types
df["salary"].unique() # unique values
df["dept"].value_counts()  # frequency count
```

---

## Part 4: Selecting Data

```python
# Single column → Series
df["salary"]
df.salary          # dot notation (if no spaces)

# Multiple columns → DataFrame
df[["name", "salary"]]

# Rows by condition
df[df["salary"] > 70000]
df[df["dept"] == "Engineering"]
df[(df["salary"] > 70000) & (df["dept"] == "Eng")]

# loc — label based (row label, column name)
df.loc[0]                    # row 0
df.loc[0, "name"]            # specific cell
df.loc[0:3, ["name","salary"]]  # range

# iloc — position based (row index, col index)
df.iloc[0]           # first row
df.iloc[0, 1]        # first row, second column
df.iloc[:5, :3]      # first 5 rows, first 3 cols
```

---

## Part 5: Common Operations

```python
# Sort
df.sort_values("salary", ascending=False)
df.sort_values(["dept", "salary"])

# Add column
df["annual_bonus"] = df["salary"] * 0.10

# Apply function
df["name_upper"] = df["name"].str.upper()
df["salary_k"]   = df["salary"].apply(lambda x: f"${x/1000:.0f}k")

# Drop column
df.drop(columns=["salary_k"])

# Rename column
df.rename(columns={"salary": "annual_salary"})

# Filter + reset index
high_earners = df[df["salary"] > 80000].reset_index(drop=True)
```

---

## Part 6: Aggregation

```python
# Basic stats
df["salary"].mean()
df["salary"].sum()
df["salary"].max()
df["salary"].std()

# groupby
dept_stats = df.groupby("dept")["salary"].agg(["mean","max","count"])

# Multiple agg
summary = df.groupby("dept").agg(
    avg_salary=("salary", "mean"),
    total_payroll=("salary", "sum"),
    headcount=("name", "count")
).round(2)

# pivot_table
pivot = df.pivot_table(
    values="salary",
    index="dept",
    aggfunc=["mean", "count"]
)
```

---

## Part 7: Data Cleaning

```python
# Check nulls
df.isnull().sum()
df.isnull().any()

# Fill nulls
df["salary"].fillna(0)
df.fillna({"salary": 0, "dept": "Unknown"})

# Drop rows with nulls
df.dropna()
df.dropna(subset=["salary"])    # only where salary is null

# Drop duplicates
df.drop_duplicates()
df.drop_duplicates(subset=["email"])  # by specific cols

# Convert types
df["salary"]  = df["salary"].astype(float)
df["date"]    = pd.to_datetime(df["date"])
df["dept"]    = df["dept"].astype("category")

# String cleaning
df["name"] = df["name"].str.strip().str.title()
df["email"]= df["email"].str.lower()
```

---

## Part 8: Export

```python
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", sheet_name="Data", index=False)
df.to_json("output.json", orient="records", indent=2)
```

---

## Practice Exercises

1. Load a CSV into a DataFrame and display its shape, dtypes, and first 5 rows.

2. Filter rows where salary > 70000 and department == 'Engineering'.

3. Add a column `tax` that is 20% of `salary`.

4. Group by department, get average salary per department.

5. Find the top 3 earners using `sort_values` + `head`.

---

## Next Lesson

**[Lesson 03 → Data Cleaning](lesson-03-data-cleaning.md)**
