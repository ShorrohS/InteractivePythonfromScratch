# ⚡ Phase 13 Cheat Sheet — Data Analysis

---

## NumPy

```python
import numpy as np

arr = np.array([1, 2, 3, 4, 5])
arr.mean()    # 3.0
arr.std()     # 1.41
arr.sum()     # 15
arr.min(), arr.max()

# Operations (element-wise)
arr * 2          # [2, 4, 6, 8, 10]
arr[arr > 3]     # [4, 5]  — boolean filter

# 2D array
matrix = np.array([[1,2],[3,4]])
matrix.shape     # (2, 2)
matrix.T         # transpose
np.dot(m1, m2)   # matrix multiplication
```

---

## Pandas — Create / Load

```python
import pandas as pd

df = pd.DataFrame({"col1": [1,2], "col2": [3,4]})
df = pd.read_csv("file.csv")
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")
df = pd.read_json("file.json")
```

---

## Explore

```python
df.shape          # (rows, cols)
df.head(5)        # first 5
df.info()         # dtypes + nulls
df.describe()     # statistics
df.dtypes
df["col"].unique()
df["col"].value_counts()
df.isnull().sum()
```

---

## Select

```python
df["col"]                          # Series
df[["col1","col2"]]                # DataFrame
df[df["col"] > 100]                # filter rows
df[(c1) & (c2)]                    # multiple conditions
df.loc[row_label, col_name]        # by label
df.iloc[row_idx, col_idx]          # by position
```

---

## Transform

```python
df["new"]  = df["col"] * 2          # add column
df["tax"]  = df["salary"].apply(lambda x: x * 0.20)
df["name"] = df["name"].str.upper()
df.drop(columns=["col"])
df.rename(columns={"old": "new"})
df.sort_values("col", ascending=False)
df.reset_index(drop=True)
```

---

## Aggregate

```python
df["col"].sum()
df["col"].mean()
df["col"].max()

df.groupby("dept")["salary"].mean()
df.groupby("dept").agg(
    avg=("salary","mean"),
    count=("name","count")
)
```

---

## Clean

```python
df.dropna()                        # drop null rows
df.fillna(0)                       # fill nulls
df.drop_duplicates()               # remove dupes
df["col"].astype(float)            # convert type
df["date"] = pd.to_datetime(df["date"])
df["name"] = df["name"].str.strip().str.title()
```

---

## Matplotlib

```python
import matplotlib.pyplot as plt

# Bar chart
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color="steelblue")
plt.title("Title")
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart.png")
plt.show()

# Line chart
plt.plot(x, y, marker="o")

# Pie chart
plt.pie(values, labels=labels, autopct="%1.1f%%")

# Histogram
plt.hist(df["salary"], bins=20)
```

---

## Export

```python
df.to_csv("out.csv", index=False)
df.to_excel("out.xlsx", index=False)
```
