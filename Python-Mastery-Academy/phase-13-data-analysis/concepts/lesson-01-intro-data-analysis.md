# Lesson 01 — Introduction to Data Analysis

**Phase:** 13 — Data Analysis | **Time:** ~35 min

---

## Part 1: What is Data Analysis?

Data analysis is the process of inspecting, cleaning, and modeling data to discover
useful information and support decision-making.

**Why it matters for business:**
- Data-driven decisions consistently outperform gut-feeling choices
- Python has become the dominant language for data analysis in finance, retail, healthcare, and tech
- A single well-framed analysis can uncover millions in savings or new revenue opportunities

**Common use cases:**
- Retail: which products to stock, which stores underperform, demand forecasting
- Finance: fraud detection, cash flow forecasting, credit risk scoring
- Healthcare: predicting patient readmissions, optimising resource allocation
- Marketing: campaign ROI measurement, customer segmentation

---

## Part 2: The Data Analysis Workflow

Every project follows the same six-step cycle:

```
Collect → Clean → Explore → Analyze → Visualize → Communicate
```

1. **Collect** — CSV files, databases, APIs, web scraping, Excel spreadsheets
2. **Clean** — handle missing values, fix data types, remove duplicates, standardise formats
3. **Explore** — understand shape, distributions, and patterns (EDA — Exploratory Data Analysis)
4. **Analyze** — apply statistics, groupings, aggregations, correlations
5. **Visualize** — turn numbers into charts that stakeholders can act on
6. **Communicate** — write findings in plain language for decision-makers

> In real projects, steps 2 and 3 consume 60–80% of total project time.

---

## Part 3: Python's Data Science Stack

```python
# Install the full stack in one command
# pip install numpy pandas matplotlib seaborn openpyxl

import numpy as np                  # fast numerical arrays (C-speed)
import pandas as pd                 # DataFrames — the core analysis tool
import matplotlib.pyplot as plt     # charts and figures
import seaborn as sns               # statistical plots built on matplotlib

# Verify installations
print(f"NumPy:      {np.__version__}")
print(f"Pandas:     {pd.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Seaborn:    {sns.__version__}")
```

| Library    | Role                                    | Think of it as...     |
|------------|-----------------------------------------|------------------------|
| NumPy      | Fast numeric arrays, C-speed math       | Turbo Excel formulas   |
| Pandas     | Tables, file I/O, filtering, grouping   | Python spreadsheet     |
| Matplotlib | Line, bar, pie, scatter charts          | Python chart engine    |
| Seaborn    | Statistical charts, heatmaps            | Python Power BI        |
| openpyxl   | Read and write .xlsx Excel files        | Excel file adapter     |

---

## Part 4: Loading Your First Dataset

```python
import pandas as pd

# Read a CSV — works the same for 100 rows or 10 million rows
df = pd.read_csv("sales_data.csv")

# Immediate first look
print(df.shape)         # (10000, 6) — rows × columns
print(df.head())        # first 5 rows
print(df.tail(3))       # last 3 rows
print(df.info())        # dtypes, memory usage, null counts
print(df.describe())    # summary statistics for numeric columns
```

Sample `.info()` output for a sales dataset:

```
RangeIndex: 10000 entries, 0 to 9999
Data columns (total 6 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   date        10000 non-null  object
 1   product     10000 non-null  object
 2   quantity     9980 non-null  float64   <- 20 missing values
 3   unit_price  10000 non-null  float64
 4   revenue     10000 non-null  float64
 5   region      10000 non-null  object
dtypes: float64(3), object(3)
```

Two things to notice: `quantity` has 20 missing values, and `date` is stored as `object`
(string) — it needs conversion before date-based analysis.

---

## Part 5: Answering Business Questions in 3 Lines

A business analyst receives a 10,000-row sales CSV and needs three answers fast.

```python
import pandas as pd

df = pd.read_csv("sales_data.csv")

# Q1: What was total revenue?
total = df["revenue"].sum()
print(f"Total revenue: ${total:,.2f}")
# → Total revenue: $4,827,391.50

# Q2: Which product sold the most units?
top_product = df.groupby("product")["quantity"].sum().idxmax()
print(f"Top product by units: {top_product}")
# → Top product by units: Wireless Keyboard

# Q3: Which month had the highest revenue?
df["month"] = pd.to_datetime(df["date"]).dt.month_name()
best_month  = df.groupby("month")["revenue"].sum().idxmax()
print(f"Best month: {best_month}")
# → Best month: November
```

Three business questions. Three short code blocks. Under five minutes of work.

---

## Part 6: Quick Exploration Checklist

Run this checklist on every new dataset before doing any analysis.

```python
import pandas as pd

df = pd.read_csv("sales_data.csv")

# 1. How big is the dataset?
print(f"Rows: {df.shape[0]:,}  |  Columns: {df.shape[1]}")

# 2. Column names and types
print(df.dtypes)

# 3. Missing data — count and percentage
print("--- Missing counts ---")
print(df.isnull().sum())
print("--- Missing % ---")
print(df.isnull().mean().mul(100).round(1))

# 4. Unique values in categorical columns
for col in df.select_dtypes(include="object").columns:
    print(f"  {col}: {df[col].nunique()} unique values")

# 5. Numeric summary statistics
print(df.describe())

# 6. Duplicate rows
dup_count = df.duplicated().sum()
print(f"Duplicate rows: {dup_count}")
```

---

## Part 7: Reading Different File Formats

```python
import pandas as pd

# CSV — the most common format
df = pd.read_csv("data.csv")

# Excel — requires openpyxl installed
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# JSON — common from APIs
df = pd.read_json("data.json")

# From a URL — pandas reads remote files directly
df = pd.read_csv("https://example.com/sales.csv")

# Save back to any format
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
df.to_json("output.json", orient="records", indent=2)
```

---

## Practice Exercises

1. Load any CSV and print its shape, column names, data types, and missing value count per
   column. Use `pd.read_csv()` and `df.isnull().sum()`.

2. Given a DataFrame with `product`, `quantity`, and `price` columns, add a `revenue` column
   (`quantity * price`). Then find the product with the highest total revenue using
   `.groupby()` and `.idxmax()`.

3. Install numpy, pandas, matplotlib, and seaborn using pip. Write a script that imports all
   four and prints each library's version number using `np.__version__`, `pd.__version__`, etc.

4. Load a CSV with at least five numeric columns and run `.describe()`. Identify which column
   has the highest standard deviation. In one sentence, explain what that means for the data.

---

## Next Lesson

**[Lesson 02 → Pandas Basics](lesson-02-pandas-basics.md)**
