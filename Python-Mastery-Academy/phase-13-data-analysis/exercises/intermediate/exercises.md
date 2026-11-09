# 📝 Phase 13 — Intermediate Exercises: Data Analysis

> Difficulty: ⭐⭐ | These require writing complete programs.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. NumPy Broadcasting and Vectorised Operations**

Create two NumPy arrays:
```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])
```

Without using any Python loops, compute and print:
1. Element-wise sum (`a + b`)
2. Element-wise product (`a * b`)
3. `a` squared (`a ** 2`)
4. `b` divided by 10 (`b / 10`)
5. The result of adding the scalar `100` to every element of `a` (broadcasting)
6. Which elements of `a` are greater than 2 (boolean array)
7. The values of `a` where the condition in step 6 is True (fancy indexing)

> 💡 Hint 1: NumPy applies operations element-by-element — no loop needed.
> 💡 Hint 2: `a[a > 2]` returns only the elements that satisfy the condition.

---

**Q2. Boolean Indexing to Filter a DataFrame**

Build the following DataFrame:

```python
data = {
    "name":       ["Alice", "Bob", "Carol", "David", "Eva", "Frank"],
    "department": ["Sales", "IT", "Sales", "HR", "IT", "Sales"],
    "salary":     [55000, 72000, 61000, 48000, 80000, 59000],
    "years":      [3, 7, 5, 2, 9, 4]
}
```

Using **only** boolean indexing (no `.query()` or `.loc[]` with string expressions),
filter the DataFrame to show:
1. Employees in the `"IT"` department
2. Employees with salary greater than `60000`
3. Sales employees who have been with the company for more than 3 years
4. Employees with salary between `50000` and `70000` (inclusive)

Print each filtered result.

> 💡 Hint 1: Combine conditions with `&` (and) or `|` (or); wrap each in parentheses.
> 💡 Hint 2: `df[df["salary"] > 60000]` returns all rows where the condition is True.

---

**Q3. Handling Missing Values**

Create the following DataFrame that contains NaN values:

```python
import numpy as np
data = {
    "product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam", "Headset"],
    "price":   [899.99, np.nan, 49.99, 349.99, np.nan, 79.99],
    "stock":   [5, 30, np.nan, 8, 15, np.nan],
    "rating":  [4.5, 4.2, np.nan, 4.7, np.nan, 4.3]
}
```

Perform and print results for:
1. Count of missing values per column (`.isnull().sum()`)
2. Drop all rows that have ANY missing value
3. Fill `price` NaN with the **median** price; fill `stock` and `rating` NaN with `0`
4. Fill all remaining NaN in the original with the column mean

> 💡 Hint 1: `df.fillna(value)` fills NaN; `df.dropna()` removes rows with NaN.
> 💡 Hint 2: `df["price"].median()` computes the median of a column.

---

**Q4. GroupBy and Multi-Column Aggregation**

Build this sales DataFrame (or load from a CSV string you write to disk):

```python
data = {
    "region":    ["North","South","North","East","South","East","North","South"],
    "product":   ["A","B","A","C","A","B","C","C"],
    "units":     [100, 80, 120, 60, 90, 70, 110, 85],
    "revenue":   [5000,3200,6000,2400,3600,2800,5500,3400]
}
```

Using `.groupby()` and `.agg()`:
1. Group by `region` and compute total `units` and total `revenue`
2. Group by `product` and compute mean `units` and max `revenue`
3. Group by both `region` and `product`, compute sum of `revenue`, then
   reset the index and display the result sorted by `revenue` descending

> 💡 Hint 1: `df.groupby("region")[["units","revenue"]].sum()` groups and sums.
> 💡 Hint 2: Pass a dict to `.agg()` to apply different functions per column:
> `agg({"units": "sum", "revenue": "mean"})`.

---

**Q5. Merging Two DataFrames**

Create these two DataFrames:

```python
customers = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "name":        ["Alice", "Bob", "Carol", "David", "Eva"],
    "city":        ["London", "Paris", "Berlin", "London", "Paris"]
})

orders = pd.DataFrame({
    "order_id":    [101, 102, 103, 104, 105, 106],
    "customer_id": [1, 2, 1, 3, 5, 2],
    "amount":      [250.0, 180.0, 320.0, 95.0, 430.0, 210.0]
})
```

Perform:
1. An **inner join** on `customer_id` — only customers who placed orders
2. A **left join** — all customers, including those with no orders (customer 4)
3. After the inner join, group by `name` to find the total order amount per customer,
   sorted from highest to lowest

> 💡 Hint 1: `pd.merge(df1, df2, on="customer_id", how="inner")`.
> 💡 Hint 2: `how="left"` keeps all rows from the left DataFrame even without matches.

---

**Q6. Line Chart with Multiple Series**

Create a line chart showing the revenue of three product lines over 6 months:

```python
months   = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
product_a = [12000, 15000, 13500, 17000, 19500, 22000]
product_b = [ 8000,  9200, 10500, 11800, 10200, 13000]
product_c = [ 5000,  6500,  7200,  8100,  9300, 11500]
```

Requirements:
- Plot all three series on the same axes with different colours/markers
- Add a legend labelled `"Product A"`, `"Product B"`, `"Product C"`
- Title: `"Monthly Revenue by Product Line"`
- X-axis label: `"Month"`, Y-axis label: `"Revenue ($)"`
- Use `plt.tight_layout()` and `plt.show()`

> 💡 Hint 1: Call `plt.plot(months, series, label="...")` once per series.
> 💡 Hint 2: `plt.legend()` renders the legend using the `label=` values you set.

---

**Q7. Correlation Matrix**

Create a DataFrame with four numeric columns that represent student performance:

```python
import numpy as np
np.random.seed(42)
n = 50
df = pd.DataFrame({
    "study_hours": np.random.uniform(1, 10, n),
    "sleep_hours": np.random.uniform(4, 9, n),
    "stress_level": np.random.uniform(1, 10, n),
    "exam_score":   np.random.uniform(40, 100, n)
})
# Make exam_score positively correlated with study_hours
df["exam_score"] = df["study_hours"] * 7 + np.random.uniform(-10, 10, n)
```

1. Compute the correlation matrix with `.corr()`
2. Print it rounded to 2 decimal places
3. Identify the pair with the highest and lowest correlation (excluding the
   diagonal `1.00` values)
4. *(Optional)* Visualise the correlation matrix as a heatmap using
   `plt.imshow()` or `seaborn.heatmap()` if seaborn is available

> 💡 Hint 1: `df.corr()` returns a DataFrame where each cell is the Pearson
> correlation coefficient between two columns.
> 💡 Hint 2: Values close to `1.0` indicate strong positive correlation;
> values close to `-1.0` indicate strong negative correlation.

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
