# Phase 13 — Advanced Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/advanced/exercises.md`

---

## Q1. End-to-End Data Pipeline

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import io

# ── Stage 1: Load ──────────────────────────────────────────────────
emp_csv = """emp_id,name,dept_id,salary,hire_date
1,Alice,10,72000,2019-03-15
2,Bob,20,85000,2018-07-01
3,Carol,10,91000,2020-11-20
4,David,30,63000,2021-01-08
5,Eva,20,78000,2017-05-30
6,Frank,10,,2022-02-14
7,Grace,30,54000,2020-09-01
8,Henry,,69000,2019-06-12
"""

dept_csv = """dept_id,dept_name,budget
10,Engineering,500000
20,Marketing,300000
30,HR,200000
"""

# Write to disk then read back
with open("employees.csv", "w") as f:
    f.write(emp_csv)
with open("departments.csv", "w") as f:
    f.write(dept_csv)

employees   = pd.read_csv("employees.csv")
departments = pd.read_csv("departments.csv")

# ── Stage 2: Clean ─────────────────────────────────────────────────
# Drop rows where both emp_id AND name are NaN (none here, but defensive)
employees.dropna(subset=["emp_id", "name"], how="all", inplace=True)

# Fill missing salary with the median salary
median_salary = employees["salary"].median()
employees["salary"] = employees["salary"].fillna(median_salary)

# Fill missing dept_id with 0 (will become "Unknown" after merge)
employees["dept_id"] = employees["dept_id"].fillna(0).astype(int)

# Convert hire_date to proper datetime
employees["hire_date"] = pd.to_datetime(employees["hire_date"])

print("Cleaned employees:\n", employees)

# ── Stage 3: Merge ─────────────────────────────────────────────────
# Left join keeps all employees; unmatched dept_id (0) gets NaN dept_name
merged = pd.merge(employees, departments, on="dept_id", how="left")
merged["dept_name"] = merged["dept_name"].fillna("Unknown")  # label unknown dept

print("\nMerged table:\n", merged[["name", "dept_name", "salary", "hire_date"]])

# ── Stage 4: Aggregate ─────────────────────────────────────────────
summary = merged.groupby("dept_name")["salary"].agg(
    headcount="count",
    mean_salary="mean",
    total_spend="sum"
).round(2)
print("\nDepartment summary:\n", summary)

# ── Stage 5: Chart ─────────────────────────────────────────────────
summary["total_spend"].plot(kind="barh", color="steelblue", figsize=(8, 4))
plt.title("Total Salary Spend by Department")
plt.xlabel("Total Salary ($)")
plt.ylabel("Department")
plt.tight_layout()
plt.show()
```

---

## Q2. Pivot Table

```python
import pandas as pd
import numpy as np

# Build a 16-row sales dataset
data = {
    "region":   ["North"]*8 + ["South"]*8,
    "product":  ["A","A","B","B","C","C","A","B",
                 "A","B","B","C","C","A","C","A"],
    "quarter":  ["Q1","Q2","Q3","Q4","Q1","Q2","Q3","Q4",
                 "Q1","Q2","Q3","Q4","Q1","Q2","Q3","Q4"],
    "units_sold":[120,130,90,100,80,85,110,95,
                  110,95,105,70,90,115,80,125],
    "revenue":  [6000,6500,3600,4000,3200,3400,5500,3800,
                 5500,3800,4200,2800,3600,5750,3200,6250]
}
df = pd.DataFrame(data)

# 1. Pivot: region (rows) × product (cols), sum of revenue
pivot1 = pd.pivot_table(df, values="revenue",
                        index="region", columns="product",
                        aggfunc="sum")
print("Revenue by region × product:\n", pivot1)

# 2. Pivot: quarter (rows) × region (cols), mean of units_sold
pivot2 = pd.pivot_table(df, values="units_sold",
                        index="quarter", columns="region",
                        aggfunc="mean")
print("\nMean units sold by quarter × region:\n", pivot2)

# 3. Interpret the first pivot table
best_product = pivot1.sum(axis=0).idxmax()   # sum across regions per product
best_region  = pivot1.sum(axis=1).idxmax()   # sum across products per region
print(f"\nHighest-revenue product: {best_product}")
print(f"Higher-revenue region:   {best_region}")
```

`.sum(axis=0)` sums down each column (across regions); `.sum(axis=1)` sums across columns (across products).

---

## Q3. Date Column Analysis — Monthly Trends

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create 24-month dataset
dates = pd.date_range(start="2022-01-01", periods=24, freq="MS")
np.random.seed(0)
df = pd.DataFrame({
    "date":    dates,
    "visits":  np.random.randint(8000, 25000, 24),
    "signups": np.random.randint(50, 500, 24),
    "revenue": np.random.uniform(5000, 30000, 24).round(2)
})

# 1. Set date as the index
df.set_index("date", inplace=True)

# 2. Extract year and month into new columns
df["year"]  = df.index.year
df["month"] = df.index.month

# 3. Group by year: total visits, total signups, mean revenue
yearly = df.groupby("year").agg(
    total_visits=("visits", "sum"),
    total_signups=("signups", "sum"),
    mean_revenue=("revenue", "mean")
).round(2)
print("Yearly summary:\n", yearly)

# 4. Month with highest revenue
peak_month = df["revenue"].idxmax()
print(f"\nPeak revenue month: {peak_month.strftime('%B %Y')} "
      f"(${df.loc[peak_month, 'revenue']:,.2f})")

# 5. Line chart of monthly revenue
df["revenue"].plot(figsize=(10, 4), color="steelblue", marker="o")
plt.title("Monthly Revenue (2022–2023)")
plt.xlabel("Date")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.show()

# 6. Month-over-month % change in visits
df["visits_pct_change"] = df["visits"].pct_change() * 100
print("\nMonth-over-month visits % change:\n",
      df["visits_pct_change"].round(1))
```

---

## Q4. Reusable Data-Cleaning Function

```python
import pandas as pd
import numpy as np

def clean_dataframe(df):
    """
    Applies a standard cleaning pipeline to any DataFrame.
    Returns the cleaned DataFrame and prints a summary.
    """
    df = df.copy()  # never mutate the caller's DataFrame

    # 1. Strip whitespace from every string column
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # 2. Standardise string columns to Title Case
    df[str_cols] = df[str_cols].apply(lambda col: col.str.title())

    # 3. Drop fully duplicate rows — track how many are removed
    before = len(df)
    df.drop_duplicates(inplace=True)
    removed = before - len(df)

    # 4. Replace sentinel missing-value strings with np.nan
    MISSING = {"N/A", "N/a", "Na", "Na", "-", ""}
    df[str_cols] = df[str_cols].apply(
        lambda col: col.where(~col.isin(MISSING), other=np.nan)
    )

    # 5. Print cleaning summary
    print(f"Duplicates removed: {removed}")
    print("NaN counts after cleaning:")
    print(df.isnull().sum())
    return df


# ── Demonstration ──────────────────────────────────────────────────
messy = pd.DataFrame({
    "name":    ["  alice ", "Bob", "alice ", "  CAROL", "David"],
    "city":    ["london", "paris  ", "London", "N/A", "-"],
    "score":   [85, 90, 85, 78, 92],
    "comment": ["good", "NA", "good", "", "excellent"]
})

print("Original:\n", messy)
cleaned = clean_dataframe(messy)
print("\nCleaned:\n", cleaned)
```

`df.copy()` is important — it prevents the function from silently modifying the caller's object.
`col.where(~col.isin(MISSING))` replaces matching values with NaN while leaving others unchanged.

---

## Q5. 2×2 Subplot Figure

```python
import pandas as pd
import matplotlib.pyplot as plt

# Compact sales dataset
data = {
    "region":   ["North","North","North","South","South","South"],
    "product":  ["A","B","C","A","B","C"],
    "quarter":  ["Q1","Q1","Q1","Q1","Q1","Q1"],
    "revenue":  [17500, 10400, 8700, 17500, 8000, 9600]
}
df = pd.DataFrame(data)

region_rev  = df.groupby("region")["revenue"].sum()
product_rev = df.groupby("product")["revenue"].sum()

# Build 2×2 figure
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Sales Analysis Dashboard", fontsize=14)

# Top-left: bar chart — revenue by region
axes[0][0].bar(region_rev.index, region_rev.values, color="steelblue")
axes[0][0].set_title("Revenue by Region")
axes[0][0].set_xlabel("Region")
axes[0][0].set_ylabel("Revenue ($)")

# Top-right: horizontal bar — revenue by product
axes[0][1].barh(product_rev.index, product_rev.values, color="darkorange")
axes[0][1].set_title("Revenue by Product")
axes[0][1].set_xlabel("Revenue ($)")
axes[0][1].set_ylabel("Product")

# Bottom-left: line chart per region across products (x = products)
for region, group in df.groupby("region"):
    grp = group.groupby("product")["revenue"].sum()
    axes[1][0].plot(grp.index, grp.values, marker="o", label=region)
axes[1][0].set_title("Revenue by Product per Region")
axes[1][0].set_xlabel("Product")
axes[1][0].set_ylabel("Revenue ($)")
axes[1][0].legend()

# Bottom-right: pie chart — share of revenue by product
axes[1][1].pie(product_rev.values,
               labels=product_rev.index,
               autopct="%1.1f%%",
               startangle=90)
axes[1][1].set_title("Revenue Share by Product")

plt.tight_layout()
plt.show()
```

---

## Q6. Rolling Averages on a Time Series

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 36-month revenue series
np.random.seed(7)
dates   = pd.date_range(start="2021-01-01", periods=36, freq="MS")
revenue = pd.Series(np.random.uniform(8000, 30000, 36).round(2), index=dates,
                    name="revenue")

# 1. 3-month and 6-month rolling averages
ma3 = revenue.rolling(window=3).mean()
ma6 = revenue.rolling(window=6).mean()

# 2. Plot — original faint, MAs bold
plt.figure(figsize=(12, 5))
plt.plot(revenue.index, revenue,        color="lightsteelblue", alpha=0.6,
         linewidth=1, label="Actual revenue")
plt.plot(ma3.index, ma3, color="steelblue",  linewidth=2, label="3-month MA")
plt.plot(ma6.index, ma6, color="darkorange", linewidth=2, label="6-month MA")

plt.title("Monthly Revenue with Rolling Averages")
plt.xlabel("Date")
plt.ylabel("Revenue ($)")
plt.legend()
plt.tight_layout()
plt.show()

# 3. Peak of 3-month rolling average
peak_date = ma3.idxmax()
print(f"3-month MA peak: {peak_date.strftime('%B %Y')} "
      f"(${ma3[peak_date]:,.2f})")
```

The first `window - 1` values of a rolling average are NaN because there are not yet enough preceding data points to fill the window.

---

## Q7. Export to CSV and JSON

```python
import pandas as pd
import numpy as np
import json
import datetime

# Re-use the cleaned merged DataFrame from Q1 (abbreviated here)
employees = pd.read_csv("employees.csv")
departments = pd.read_csv("departments.csv")
employees["salary"]   = employees["salary"].fillna(employees["salary"].median())
employees["dept_id"]  = employees["dept_id"].fillna(0).astype(int)
employees["hire_date"] = pd.to_datetime(employees["hire_date"])
merged = pd.merge(employees, departments, on="dept_id", how="left")
merged["dept_name"] = merged["dept_name"].fillna("Unknown")

# 1. Export cleaned DataFrame to CSV without the integer index
merged.to_csv("employees_clean.csv", index=False)
print("Exported employees_clean.csv")

# 2. Build summary dictionary
summary = {
    "total_employees":   int(len(merged)),
    "avg_salary":        round(float(merged["salary"].mean()), 2),
    "total_salary_spend": round(float(merged["salary"].sum()), 2),
    "departments":       sorted(merged["dept_name"].unique().tolist()),
    "generated_at":      datetime.date.today().isoformat()
}

# 3. Export summary to indented JSON
with open("summary.json", "w") as f:
    json.dump(summary, f, indent=4)
print("Exported summary.json")

# 4. Read back and confirm
df_check = pd.read_csv("employees_clean.csv")
print(f"\nCSV rows read back:   {len(df_check)} (expected {len(merged)})")

with open("summary.json") as f:
    summary_check = json.load(f)
print(f"JSON keys read back:  {list(summary_check.keys())}")
print(f"Departments:          {summary_check['departments']}")
```

`index=False` prevents Pandas from writing the row numbers as a column.
`json.dump(..., indent=4)` writes human-readable, indented JSON.
