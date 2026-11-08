# Lesson 04 — Data Cleaning

**Phase:** 13 — Data Analysis | **Time:** ~50 min

---

## Part 1: Why Data Cleaning Matters

Dirty data is the single biggest source of errors in data analysis.

**Common problems in real datasets:**
- Missing values: survey respondents skipped fields, sensors failed, exports truncated
- Duplicate rows: the same transaction logged twice, merged spreadsheets
- Wrong data types: prices stored as strings ("$1,299"), dates as plain text
- Inconsistent formatting: "engineering", "Engineering", "ENGINEERING" all mean the same thing
- Outliers and impossible values: age = -5, salary = 9999999

**The rule:** garbage in, garbage out — even the most sophisticated analysis produces
wrong answers when the input data is dirty. Always clean before you analyse.

---

## Part 2: Identifying Missing Data

```python
import pandas as pd

df = pd.read_csv("sales_dirty.csv")

# Count of nulls per column
print(df.isnull().sum())

# Percentage of nulls per column
null_pct = df.isnull().mean().mul(100).round(2)
print(null_pct)

# Which columns have ANY missing values?
print(df.columns[df.isnull().any()].tolist())

# Rows that have at least one null
rows_with_nulls = df[df.isnull().any(axis=1)]
print(f"Rows with at least one null: {len(rows_with_nulls)}")

# Heatmap-style view (text)
print(df.isnull().sum().sort_values(ascending=False))
```

---

## Part 3: Handling Missing Data

Choose the right strategy for each column — there is no single right answer.

```python
import pandas as pd

df = pd.read_csv("sales_dirty.csv")

# Strategy 1: Drop rows that have nulls (only if you can afford to lose data)
df_clean = df.dropna()                         # drop any row with a null
df_clean = df.dropna(subset=["revenue"])       # only where revenue is null
df_clean = df.dropna(thresh=5)                 # keep rows with >= 5 non-null values

# Strategy 2: Drop columns with too many nulls
df_clean = df.dropna(axis=1)                        # drop any column with nulls
df_clean = df.dropna(axis=1, thresh=len(df) * 0.5)  # drop cols >50% null

# Strategy 3: Fill with a constant
df["region"]   = df["region"].fillna("Unknown")
df["discount"] = df["discount"].fillna(0)

# Strategy 4: Fill with column statistics
df["salary"]   = df["salary"].fillna(df["salary"].mean())
df["quantity"] = df["quantity"].fillna(df["quantity"].median())
df["category"] = df["category"].fillna(df["category"].mode()[0])

# Strategy 5: Forward fill and backward fill (for time-series data)
df["price"] = df["price"].ffill()    # carry last known value forward
df["price"] = df["price"].bfill()    # carry next known value backward

# Strategy 6: Interpolation (linear fill between known values)
df["temperature"] = df["temperature"].interpolate(method="linear")
```

---

## Part 4: Removing Duplicates

```python
import pandas as pd

df = pd.read_csv("sales_dirty.csv")

# Detect duplicates
print(f"Duplicate rows: {df.duplicated().sum()}")

# See the actual duplicate rows
print(df[df.duplicated(keep=False)])   # all copies, not just extras

# Drop duplicates (keeps first occurrence by default)
df_clean = df.drop_duplicates()

# Drop duplicates based on specific columns only
df_clean = df.drop_duplicates(subset=["order_id"])
df_clean = df.drop_duplicates(subset=["customer_id", "product", "date"])

# Keep the last occurrence instead of the first
df_clean = df.drop_duplicates(subset=["order_id"], keep="last")

print(f"Rows before: {len(df)}  |  Rows after: {len(df_clean)}")
```

---

## Part 5: Fixing Data Types

```python
import pandas as pd

df = pd.read_csv("sales_dirty.csv")

# Convert a column to a specific type
df["quantity"] = df["quantity"].astype(int)
df["price"]    = df["price"].astype(float)

# Safe numeric conversion — errors='coerce' turns unparseable values into NaN
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

# Convert dates — always do this; keep them as datetime, not strings
df["order_date"] = pd.to_datetime(df["order_date"])
df["order_date"] = pd.to_datetime(df["order_date"], format="%d/%m/%Y")  # explicit format

# Once datetime, you can extract components
df["year"]  = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["day"]   = df["order_date"].dt.day_name()

# Convert to category (saves memory for low-cardinality columns)
df["region"] = df["region"].astype("category")
```

---

## Part 6: Renaming and Cleaning Strings

```python
import pandas as pd

df = pd.read_csv("sales_dirty.csv")

# Rename specific columns
df = df.rename(columns={"cust_nm": "customer_name", "amt": "amount"})

# Rename all columns at once (must provide full list)
df.columns = ["date", "customer", "product", "qty", "price", "revenue"]

# Make all column names lowercase with underscores (common cleanup)
df.columns = df.columns.str.lower().str.replace(" ", "_")

# String cleaning on column values
df["customer_name"] = df["customer_name"].str.strip()       # remove leading/trailing spaces
df["customer_name"] = df["customer_name"].str.title()       # Title Case
df["category"]      = df["category"].str.lower()            # normalise case
df["category"]      = df["category"].str.replace("-", "_")  # standardise separators
df["phone"]         = df["phone"].str.replace("[^0-9]", "", regex=True)  # digits only

# Remove currency symbols and commas before converting
df["price"] = df["price"].str.replace("$", "").str.replace(",", "")
df["price"] = pd.to_numeric(df["price"])

# Filter outliers
df = df[df["salary"].between(0, 500_000)]        # realistic salary range
df = df[df["quantity"] > 0]                       # no zero or negative quantities
```

---

## Part 7: Complete Cleaning Example

Load a messy sales CSV, clean it step by step, and save the clean version.

```python
import pandas as pd

# --- Step 1: Load raw data ---
df = pd.read_csv("sales_messy.csv")
print(f"Raw shape: {df.shape}")
print(df.isnull().sum())

# --- Step 2: Standardise column names ---
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
print("Columns:", df.columns.tolist())

# --- Step 3: Remove full duplicate rows ---
before = len(df)
df = df.drop_duplicates()
print(f"Dropped {before - len(df)} duplicate rows")

# --- Step 4: Fix data types ---
df["order_date"]  = pd.to_datetime(df["order_date"], errors="coerce")
df["unit_price"]  = pd.to_numeric(
    df["unit_price"].str.replace("[$,]", "", regex=True),
    errors="coerce"
)
df["quantity"]    = pd.to_numeric(df["quantity"], errors="coerce")

# --- Step 5: Handle missing values ---
df["region"]      = df["region"].fillna("Unknown")
df["quantity"]    = df["quantity"].fillna(df["quantity"].median())
df["unit_price"]  = df["unit_price"].fillna(df["unit_price"].mean())
df               = df.dropna(subset=["order_date", "product"])

# --- Step 6: Clean strings ---
df["product"]     = df["product"].str.strip().str.title()
df["region"]      = df["region"].str.strip().str.upper()

# --- Step 7: Remove outliers ---
df = df[df["unit_price"].between(0.01, 10_000)]
df = df[df["quantity"].between(1, 10_000)]

# --- Step 8: Add derived columns ---
df["revenue"] = df["quantity"] * df["unit_price"]

# --- Step 9: Save clean data ---
df.to_csv("sales_clean.csv", index=False)
print(f"Clean shape: {df.shape}")
print("Saved to sales_clean.csv")
```

---

## Practice Exercises

1. Load a CSV and report: total rows, rows with at least one null, null count per column,
   and number of duplicate rows — all in a single printed summary block.

2. Given a DataFrame with a `price` column stored as strings (e.g., `"$1,299.99"`), convert
   it to `float` by stripping the `$` and `,` characters, then fill missing prices with the
   column median.

3. A `hire_date` column contains dates in mixed formats (`"2021-03-15"` and `"15/03/2021"`).
   Use `pd.to_datetime()` with `errors="coerce"` to parse the column, then count how many
   dates failed to parse.

4. Write a cleaning pipeline function `clean_df(df)` that: (a) lowercases all column names,
   (b) strips whitespace from all string columns, (c) drops duplicate rows, and (d) drops
   columns where more than 50% of values are null. Return the cleaned DataFrame.

---

## Next Lesson

**[Lesson 05 → Data Visualization](lesson-05-data-visualization.md)**
