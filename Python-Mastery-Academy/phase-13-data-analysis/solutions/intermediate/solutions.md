# Phase 13 — Intermediate Exercise Solutions

> Open this ONLY after attempting the exercises.
> Exercises file: `../../exercises/intermediate/exercises.md`

---

## Q1. NumPy Broadcasting and Vectorised Operations

```python
import numpy as np

a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

# 1. Element-wise sum — arrays must be the same shape
print("a + b =", a + b)           # [11 22 33 44 55]

# 2. Element-wise product
print("a * b =", a * b)           # [10 40 90 160 250]

# 3. a squared — each element raised to the power 2
print("a ** 2 =", a ** 2)         # [1 4 9 16 25]

# 4. b divided by 10 — scalar division broadcasts to every element
print("b / 10 =", b / 10)         # [1. 2. 3. 4. 5.]

# 5. Broadcasting: scalar 100 added to every element of a
print("a + 100 =", a + 100)       # [101 102 103 104 105]

# 6. Boolean array — True where condition holds
mask = a > 2
print("a > 2 =", mask)            # [False False  True  True  True]

# 7. Fancy indexing — select only the True elements
print("a[a > 2] =", a[a > 2])     # [3 4 5]
```

---

## Q2. Boolean Indexing to Filter a DataFrame

```python
import pandas as pd

data = {
    "name":       ["Alice", "Bob", "Carol", "David", "Eva", "Frank"],
    "department": ["Sales", "IT", "Sales", "HR", "IT", "Sales"],
    "salary":     [55000, 72000, 61000, 48000, 80000, 59000],
    "years":      [3, 7, 5, 2, 9, 4]
}
df = pd.DataFrame(data)

# 1. IT department only
it_staff = df[df["department"] == "IT"]
print("IT employees:\n", it_staff, "\n")

# 2. Salary above 60,000
high_earners = df[df["salary"] > 60000]
print("Salary > 60000:\n", high_earners, "\n")

# 3. Sales employees AND years > 3 — combine conditions with &
senior_sales = df[(df["department"] == "Sales") & (df["years"] > 3)]
print("Senior Sales staff:\n", senior_sales, "\n")

# 4. Salary between 50000 and 70000 inclusive
mid_band = df[(df["salary"] >= 50000) & (df["salary"] <= 70000)]
print("Salary 50k–70k:\n", mid_band)
```

Each condition in parentheses produces a boolean Series; `&` combines them row-by-row.

---

## Q3. Handling Missing Values

```python
import pandas as pd
import numpy as np

data = {
    "product": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam", "Headset"],
    "price":   [899.99, np.nan, 49.99, 349.99, np.nan, 79.99],
    "stock":   [5, 30, np.nan, 8, 15, np.nan],
    "rating":  [4.5, 4.2, np.nan, 4.7, np.nan, 4.3]
}
df = pd.DataFrame(data)

# 1. Count NaN per column
print("Missing values per column:")
print(df.isnull().sum())

# 2. Drop rows with ANY missing value — returns a new DataFrame
df_dropped = df.dropna()
print("\nAfter dropna():\n", df_dropped)

# 3. Selective fills — use median for price; 0 for stock and rating
df_filled = df.copy()
df_filled["price"]  = df_filled["price"].fillna(df_filled["price"].median())
df_filled["stock"]  = df_filled["stock"].fillna(0)
df_filled["rating"] = df_filled["rating"].fillna(0)
print("\nSelective fillna:\n", df_filled)

# 4. Fill ALL remaining NaN with column mean
df_mean_fill = df.copy()
df_mean_fill = df_mean_fill.fillna(df_mean_fill.mean(numeric_only=True))
print("\nFilled with column mean:\n", df_mean_fill)
```

`.fillna()` does not modify the DataFrame in place by default — always assign the result.

---

## Q4. GroupBy and Multi-Column Aggregation

```python
import pandas as pd

data = {
    "region":  ["North","South","North","East","South","East","North","South"],
    "product": ["A","B","A","C","A","B","C","C"],
    "units":   [100, 80, 120, 60, 90, 70, 110, 85],
    "revenue": [5000,3200,6000,2400,3600,2800,5500,3400]
}
df = pd.DataFrame(data)

# 1. Total units and revenue by region
region_totals = df.groupby("region")[["units", "revenue"]].sum()
print("By region (sum):\n", region_totals)

# 2. Mean units and max revenue by product
product_agg = df.groupby("product").agg({"units": "mean", "revenue": "max"})
print("\nBy product (mean units, max revenue):\n", product_agg)

# 3. Revenue sum by region AND product, reset index, sort descending
region_product = (
    df.groupby(["region", "product"])["revenue"]
      .sum()
      .reset_index()                            # turns multi-index into columns
      .sort_values("revenue", ascending=False)  # highest revenue first
)
print("\nBy region + product (revenue desc):\n", region_product)
```

---

## Q5. Merging Two DataFrames

```python
import pandas as pd

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

# 1. Inner join — only customers who appear in orders
inner = pd.merge(customers, orders, on="customer_id", how="inner")
print("Inner join:\n", inner)

# 2. Left join — ALL customers; NaN for David who has no order
left = pd.merge(customers, orders, on="customer_id", how="left")
print("\nLeft join:\n", left)

# 3. Total spend per customer, sorted descending
spend = (
    inner.groupby("name")["amount"]
         .sum()
         .reset_index()
         .rename(columns={"amount": "total_spend"})
         .sort_values("total_spend", ascending=False)
)
print("\nTotal spend per customer:\n", spend)
```

`how="inner"` is the default. `how="left"` keeps every row of the left DataFrame.

---

## Q6. Line Chart with Multiple Series

```python
import matplotlib.pyplot as plt

months    = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
product_a = [12000, 15000, 13500, 17000, 19500, 22000]
product_b = [ 8000,  9200, 10500, 11800, 10200, 13000]
product_c = [ 5000,  6500,  7200,  8100,  9300, 11500]

# Each plt.plot() call adds one series to the same axes
plt.plot(months, product_a, marker="o", color="steelblue",  label="Product A")
plt.plot(months, product_b, marker="s", color="darkorange", label="Product B")
plt.plot(months, product_c, marker="^", color="seagreen",   label="Product C")

plt.title("Monthly Revenue by Product Line")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.legend()           # renders the legend using the label= values
plt.tight_layout()
plt.show()
```

---

## Q7. Correlation Matrix

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
n = 50
df = pd.DataFrame({
    "study_hours":  np.random.uniform(1, 10, n),
    "sleep_hours":  np.random.uniform(4, 9, n),
    "stress_level": np.random.uniform(1, 10, n),
    "exam_score":   np.random.uniform(40, 100, n)
})
# Create a genuine correlation with study_hours
df["exam_score"] = df["study_hours"] * 7 + np.random.uniform(-10, 10, n)

# 1. Compute the correlation matrix
corr = df.corr()

# 2. Print rounded to 2 decimal places
print("Correlation matrix:\n", corr.round(2))

# 3. Find highest and lowest off-diagonal pairs
corr_no_diag = corr.where(~np.eye(len(corr), dtype=bool))  # mask the diagonal
highest_pair = corr_no_diag.stack().idxmax()
lowest_pair  = corr_no_diag.stack().idxmin()
print(f"\nHighest correlation: {highest_pair} = {corr_no_diag.stack().max():.2f}")
print(f"Lowest  correlation: {lowest_pair}  = {corr_no_diag.stack().min():.2f}")

# 4. Optional heatmap with imshow
fig, ax = plt.subplots()
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=45, ha="right")
ax.set_yticklabels(corr.columns)
plt.colorbar(im, ax=ax)
plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()
```
