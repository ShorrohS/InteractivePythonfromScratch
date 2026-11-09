# Phase 13 — Data Analysis Quick Reference

> Keep this open while coding. One-line examples for every common operation.

---

## NumPy — Array Creation

```python
import numpy as np

np.array([1, 2, 3])            # from a Python list
np.zeros((3, 4))               # 3×4 array of 0.0
np.ones((2, 5))                # 2×5 array of 1.0
np.arange(0, 10, 2)            # [0 2 4 6 8]  — start, stop, step
np.linspace(0, 1, 5)           # [0.0 0.25 0.5 0.75 1.0]  — evenly spaced
np.random.seed(42)
np.random.randint(1, 100, 10)  # 10 random ints between 1 and 99
np.random.uniform(0, 1, 10)    # 10 random floats between 0 and 1
```

---

## NumPy — Reshape and Math

```python
arr = np.array([1, 2, 3, 4, 5, 6])

arr.reshape(2, 3)              # 2 rows × 3 cols — total elements must match
arr.flatten()                  # collapse back to 1-D

arr + 10                       # broadcast: add 10 to every element
arr * 2                        # broadcast: multiply every element by 2
arr ** 2                       # element-wise square
np.sqrt(arr)                   # element-wise square root
np.abs(arr)                    # element-wise absolute value
```

---

## NumPy — Statistics

```python
arr.sum()                      # total of all elements
arr.mean()                     # arithmetic mean
arr.std()                      # standard deviation
arr.min()  /  arr.max()        # minimum and maximum
arr.argmin()  /  arr.argmax()  # index of min / max
np.median(arr)                 # median value
np.percentile(arr, 75)         # 75th percentile
```

---

## Pandas — I/O

```python
import pandas as pd

df = pd.read_csv("data.csv")                  # read CSV
df = pd.read_csv("data.csv", index_col=0)     # use first column as index
df = pd.read_json("data.json")                # read JSON
df.to_csv("out.csv", index=False)             # write CSV without row numbers
df.to_json("out.json", indent=4)              # write formatted JSON
df.to_excel("out.xlsx", index=False)          # write Excel (needs openpyxl)
```

---

## Pandas — Exploration

```python
df.head()           # first 5 rows (pass n for different count)
df.tail(3)          # last 3 rows
df.shape            # (rows, columns) as a tuple
df.dtypes           # dtype of each column
df.info()           # columns, non-null counts, dtypes, memory usage
df.describe()       # count/mean/std/min/max for numeric columns
df.columns          # column names as an Index
df.index            # row labels
df.nunique()        # number of unique values per column
df["col"].value_counts()   # frequency table for a column
```

---

## Pandas — Cleaning

```python
df.isnull().sum()                              # NaN count per column
df.dropna()                                    # drop rows with any NaN
df.dropna(subset=["col"])                      # drop rows with NaN in "col" only
df.fillna(0)                                   # replace NaN with 0
df["col"].fillna(df["col"].median())           # fill with column median
df.drop_duplicates()                           # remove exact duplicate rows
df.drop_duplicates(subset=["col"])             # remove dupes by column
df["col"].astype(float)                        # change dtype
df["col"].str.strip()                          # remove leading/trailing whitespace
df["col"].str.lower()                          # to lowercase
df["col"].str.replace("$", "", regex=False)    # remove a character
df["col"].str.replace(r"\s+", " ", regex=True) # collapse multiple spaces
```

---

## Pandas — Analysis

```python
# GroupBy
df.groupby("region")["revenue"].sum()
df.groupby("region").agg({"revenue": "sum", "units": "mean"})

# Merge
pd.merge(df1, df2, on="key", how="inner")   # inner join
pd.merge(df1, df2, on="key", how="left")    # left join — keep all of df1
pd.merge(df1, df2, on="key", how="outer")   # outer join — keep all rows

# Pivot table
pd.pivot_table(df, values="revenue",
               index="region", columns="product", aggfunc="sum")

# Sort
df.sort_values("revenue", ascending=False)

# Boolean filter
df[df["salary"] > 50000]
df[(df["dept"] == "IT") & (df["salary"] > 70000)]

# Rolling / time-series
df["revenue"].rolling(window=3).mean()   # 3-period rolling average
df["revenue"].pct_change()               # period-over-period % change
```

---

## Matplotlib — Common Patterns

```python
import matplotlib.pyplot as plt

# Basic charts
plt.bar(x, height, color="steelblue")       # bar chart
plt.barh(y, width)                           # horizontal bar chart
plt.plot(x, y, marker="o", label="Series")  # line chart
plt.scatter(x, y, c="red", alpha=0.5)       # scatter chart
plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)  # pie

# Labels and layout
plt.title("Chart Title")
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()    # adjust padding to prevent clipping
plt.show()            # render the figure

# Subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Dashboard Title")
axes[0][0].bar(x, y)          # top-left
axes[0][1].plot(x, y)         # top-right
axes[1][0].scatter(x, y)      # bottom-left
axes[1][1].pie(sizes)         # bottom-right

# Save to file instead of showing
plt.savefig("chart.png", dpi=150, bbox_inches="tight")
```

---

## Common Gotchas

**SettingWithCopyWarning**
```python
# ❌ Risky — subset may be a view, not a copy
subset = df[df["region"] == "North"]
subset["price"] = 0

# ✅ Safe — explicitly make a copy first
subset = df[df["region"] == "North"].copy()
subset["price"] = 0
```

**Chained indexing**
```python
# ❌ Unpredictable — two separate indexing operations
df["region"]["North"] = "N"

# ✅ Use .loc[] for a single, unambiguous operation
df.loc[df["region"] == "North", "region"] = "N"
```

**inplace=True**
```python
# inplace=True modifies df directly and returns None
df.drop_duplicates(inplace=True)   # df is modified
result = df.dropna()               # df is unchanged; result is a new DataFrame

# If you chain methods, do NOT use inplace=True on intermediate steps
df = df.dropna().reset_index(drop=True)  # safe chaining without inplace
```

**axis argument**
```python
df.dropna(axis=0)   # drop ROWS with NaN  (default)
df.dropna(axis=1)   # drop COLUMNS with NaN
df.mean(axis=0)     # mean of each COLUMN (default)
df.mean(axis=1)     # mean of each ROW
```
