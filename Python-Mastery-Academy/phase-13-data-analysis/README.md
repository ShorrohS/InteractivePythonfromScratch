# 📊 Phase 13 — Data Analysis

> **Goal:** Analyze, transform, and visualize data using Python's data science stack.

---

## The Data Science Stack

```
NumPy   → Fast numerical computation
Pandas  → Data manipulation and analysis
Matplotlib/Seaborn → Data visualization
```

---

## Installation

```bash
pip install numpy pandas matplotlib seaborn openpyxl
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-numpy.md](concepts/lesson-01-numpy.md) | NumPy arrays |
| 02 | [lesson-02-pandas-basics.md](concepts/lesson-02-pandas-basics.md) | DataFrames and Series |
| 03 | [lesson-03-data-cleaning.md](concepts/lesson-03-data-cleaning.md) | Cleaning messy data |
| 04 | [lesson-04-groupby.md](concepts/lesson-04-groupby.md) | Groupby and aggregation |
| 05 | [lesson-05-matplotlib.md](concepts/lesson-05-matplotlib.md) | Charts and visualization |

---

## Core Skills

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# NumPy
arr = np.array([1, 2, 3, 4, 5])
print(arr.mean(), arr.std(), arr.sum())

# Pandas
df = pd.read_csv("sales.csv")
df.head()
df.describe()
df.info()

# Data cleaning
df.dropna()                          # Remove missing values
df.fillna(0)                         # Fill missing with 0
df["col"] = df["col"].str.strip()    # Clean strings
df = df[df["salary"] > 0]            # Filter invalid data

# Analysis
monthly = df.groupby("month")["revenue"].sum()
by_dept = df.groupby("department")["salary"].agg(["mean", "count", "sum"])

# Visualization
plt.figure(figsize=(10, 6))
plt.bar(monthly.index, monthly.values)
plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig("monthly_revenue.png")
plt.show()
```

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Sales Dashboard](guided-projects/project-01-sales-dashboard/) | Full sales analysis with charts |

---

## ✅ Completion Checklist

- [ ] Can create and manipulate NumPy arrays
- [ ] Can read CSV/Excel with Pandas
- [ ] Can clean data (handle NaN, duplicates, types)
- [ ] Can use groupby for aggregations
- [ ] Can create bar, line, pie charts with Matplotlib

---

## Previous: [Phase 12](../phase-12-automation/README.md) | Next: [Phase 14](../phase-14-testing/README.md)
