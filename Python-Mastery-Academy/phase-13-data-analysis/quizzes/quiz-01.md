# Phase 13 — Quiz 01: Data Analysis

**Questions:** 18 | **Pass:** 14/18 | **Time:** 20 min (no notes)

---

## Section 1: NumPy Arrays (Q1–Q5)

**Q1.** What does `np.array([1, 2, 3]).shape` return?
```
A) 3          B) (3,)          C) [3]          D) (1, 3)
```

**Q2.** What is the output of this code?
```python
import numpy as np
a = np.array([2, 4, 6])
print(a * 3)
```
```
A) [2, 4, 6, 2, 4, 6, 2, 4, 6]
B) [6, 12, 18]
C) 36
D) Error — can't multiply array by scalar
```

**Q3.** Which NumPy function creates an array of 5 zeros?
```
A) np.empty(5)      B) np.zeros(5)      C) np.null(5)      D) np.blank(5)
```

**Q4.** What does this return?
```python
import numpy as np
a = np.array([10, 20, 30, 40, 50])
print(a[a > 25])
```
```
A) [False False True True True]
B) [30, 40, 50]
C) [10, 20]
D) Error
```

**Q5.** What is the difference between `arr.mean()` and `arr.sum()`?
```
A) No difference — they both add elements
B) .mean() divides the total by the number of elements; .sum() just adds them
C) .sum() is only for integers; .mean() works on floats
D) .mean() is a Python built-in; .sum() is a NumPy method
```

---

## Section 2: Pandas Basics (Q6–Q10)

**Q6.** What does `pd.DataFrame(data)` require `data` to be?
```
A) A list of values
B) A NumPy array only
C) A dictionary (or other tabular structure like a list of dicts)
D) A CSV file path
```

**Q7.** What is the output of `df.shape` on a DataFrame with 10 rows and 4 columns?
```
A) 40          B) (4, 10)          C) (10, 4)          D) [10, 4]
```

**Q8.** How do you select a single column called `"price"` from DataFrame `df`?
```
A) df.price()          B) df["price"]          C) df.get("price")          D) df.col("price")
```

**Q9.** What does `df.describe()` show by default?
```
A) The first 5 rows
B) The column names and dtypes
C) Count, mean, std, min, max, and quartiles for numeric columns
D) The number of missing values per column
```

**Q10.** What does `df.head(3)` return?
```
A) The first 3 columns
B) The last 3 rows
C) The first 3 rows
D) The 3 rows with the highest index
```

---

## Section 3: Data Cleaning (Q11–Q13)

**Q11.** Which method counts missing values in each column?
```python
df.______().sum()
```
```
A) isnan          B) isnull          C) missing          D) empty
```

**Q12.** What does `df.fillna(0)` do?
```
A) Drops all rows with NaN values
B) Replaces every NaN in the DataFrame with 0
C) Fills only the first NaN in each column
D) Raises a ValueError if NaN is present
```

**Q13.** You have a `"price"` column stored as strings like `"$29.99"`. Which code
correctly converts it to float?
```
A) df["price"] = float(df["price"])
B) df["price"] = df["price"].astype(float)
C) df["price"] = df["price"].str.replace("$", "").astype(float)
D) df["price"] = df["price"].to_float()
```

---

## Section 4: GroupBy & Merge (Q14–Q15)

**Q14.** What does `df.groupby("region")["revenue"].sum()` return?
```
A) The total revenue across all regions
B) The revenue for the first row of each region
C) The total revenue per region as a Series indexed by region
D) A new column called "sum" added to df
```

**Q15.** You have two DataFrames: `customers` (with `customer_id`) and `orders`
(with `customer_id`). Which call returns ONLY the rows that exist in BOTH?
```
A) pd.merge(customers, orders, on="customer_id", how="left")
B) pd.merge(customers, orders, on="customer_id", how="outer")
C) pd.merge(customers, orders, on="customer_id", how="inner")
D) pd.concat([customers, orders])
```

---

## Section 5: Visualisation (Q16–Q18)

**Q16.** Which Matplotlib call creates a bar chart?
```
A) plt.line(x, y)
B) plt.bar(x, height)
C) plt.scatter(x, y)
D) plt.histogram(x)
```

**Q17.** You call `plt.plot()` three times for three different series. What must you
also call to show a legend?
```
A) plt.title("legend")
B) plt.labels()
C) Each plt.plot() must include label="..." AND you must call plt.legend()
D) Matplotlib adds a legend automatically after three series
```

**Q18.** What does `fig, axes = plt.subplots(2, 2)` create?
```
A) A single plot with 4 data series
B) Four separate figure windows
C) One figure with a 2×2 grid of subplots (4 axes total)
D) A 2-column, 2-row table in a text output
```

---

## Answers

.
.
.
.
.
.

| Q  | Answer | Explanation |
|----|--------|-------------|
| 1  | B | A 1-D array of 3 elements has shape `(3,)` — a tuple with one element |
| 2  | B | NumPy broadcasts the scalar 3 to each element: 2×3=6, 4×3=12, 6×3=18 |
| 3  | B | `np.zeros(5)` creates `[0. 0. 0. 0. 0.]` — float zeros by default |
| 4  | B | `a > 25` is a boolean mask; `a[mask]` returns elements where True |
| 5  | B | `.sum()` returns the total; `.mean()` divides that total by the element count |
| 6  | C | The most common input is a dict of column-name → list pairs |
| 7  | C | `.shape` returns `(rows, columns)` — always rows first |
| 8  | B | `df["price"]` is bracket notation for column selection |
| 9  | C | `.describe()` shows statistical summary: count, mean, std, min, 25%, 50%, 75%, max |
| 10 | C | `.head(n)` returns the first `n` rows (default 5) |
| 11 | B | `df.isnull().sum()` — `.isnull()` produces a boolean mask, `.sum()` counts Trues |
| 12 | B | `.fillna(0)` replaces every NaN with the value 0 |
| 13 | C | Must strip the `$` sign first, then cast to float; `astype(float)` alone fails on `"$29.99"` |
| 14 | C | Returns a Series with one row per unique region, indexed by region name |
| 15 | C | `how="inner"` returns only rows with matching keys in both DataFrames |
| 16 | B | `plt.bar(x, height)` is the correct function for a bar chart |
| 17 | C | Each series needs `label=` and `plt.legend()` must be called to render the legend |
| 18 | C | `plt.subplots(2, 2)` creates one figure with a 2-row × 2-column grid of axes |
