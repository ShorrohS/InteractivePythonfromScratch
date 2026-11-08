# Lesson 05 — Data Visualization with Matplotlib

**Phase:** 13 — Data Analysis | **Time:** ~55 min

---

## Part 1: Matplotlib Architecture

Matplotlib has three layers — understanding them prevents most confusion.

```python
import matplotlib.pyplot as plt
import numpy as np

# Figure — the outer canvas (the whole window or image)
# Axes   — one plot area inside the figure (has x-axis, y-axis, title)
# pyplot — the scripting interface (plt.xxx shortcuts)

# Method 1: quick pyplot interface (fine for single charts)
plt.plot([1, 2, 3], [4, 5, 6])
plt.title("Simple Line")
plt.show()

# Method 2: explicit Figure + Axes (preferred for anything real)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot([1, 2, 3], [4, 5, 6])
ax.set_title("Simple Line")
plt.tight_layout()
plt.show()

# figsize=(width, height) in inches — (10, 6) is a good default for reports
```

---

## Part 2: Line and Bar Charts

```python
import matplotlib.pyplot as plt
import numpy as np

months  = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
revenue = [42000, 38000, 55000, 61000, 58000, 70000]

# --- Line chart: trends over time ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(months, revenue,
        marker="o",          # dot at each data point
        color="#2196F3",     # hex colour
        linewidth=2,
        linestyle="--",      # dashed line
        label="Monthly Revenue")
ax.set_title("Monthly Revenue Trend", fontsize=14)
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# --- Bar chart: categorical comparisons ---
products = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard"]
sales    = [320, 580, 210, 145, 890]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(products, sales, color="#4CAF50", edgecolor="white", width=0.6)
ax.set_title("Sales by Product", fontsize=14)
ax.set_xlabel("Product")
ax.set_ylabel("Units Sold")
# Add value labels on top of each bar
for bar, val in zip(bars, sales):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 5,
            str(val), ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.show()

# --- Horizontal bar: better when labels are long ---
fig, ax = plt.subplots(figsize=(10, 5))
ax.barh(products, sales, color="#FF9800")
ax.set_title("Sales by Product (Horizontal)")
ax.set_xlabel("Units Sold")
plt.tight_layout()
plt.show()
```

---

## Part 3: Histogram, Scatter, and Pie Charts

```python
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)
salaries = np.random.normal(loc=75000, scale=15000, size=500)

# --- Histogram: distribution of a numeric variable ---
fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(salaries, bins=20, color="#9C27B0", edgecolor="white", alpha=0.8)
ax.set_title("Salary Distribution", fontsize=14)
ax.set_xlabel("Salary ($)")
ax.set_ylabel("Frequency")
ax.axvline(salaries.mean(), color="red", linewidth=2, linestyle="--",
           label=f"Mean: ${salaries.mean():,.0f}")
ax.legend()
plt.tight_layout()
plt.show()

# --- Scatter plot: correlation between two numeric variables ---
experience = np.random.randint(1, 20, size=80)
salary_sc  = experience * 4500 + np.random.normal(0, 8000, 80) + 30000

fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(experience, salary_sc, color="#00BCD4", alpha=0.7, edgecolors="white")
ax.set_title("Experience vs Salary", fontsize=14)
ax.set_xlabel("Years of Experience")
ax.set_ylabel("Salary ($)")
plt.tight_layout()
plt.show()

# --- Pie chart: proportion of a whole ---
categories = ["Electronics", "Clothing", "Food", "Books", "Sports"]
values     = [35, 25, 20, 12, 8]

fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(values, labels=categories, autopct="%1.1f%%",
       startangle=90, colors=["#2196F3","#4CAF50","#FF9800","#E91E63","#9C27B0"])
ax.set_title("Sales by Category", fontsize=14)
plt.tight_layout()
plt.show()
```

---

## Part 4: Customising Charts

```python
import matplotlib.pyplot as plt

months  = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
team_a  = [42, 38, 55, 61, 58, 70]
team_b  = [30, 44, 48, 52, 65, 60]

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(months, team_a, marker="o", label="Team A", color="#2196F3", linewidth=2)
ax.plot(months, team_b, marker="s", label="Team B", color="#FF5722", linewidth=2)

# Titles and labels
ax.set_title("Team Revenue Comparison (H1)", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Revenue ($000)", fontsize=12)

# Legend
ax.legend(fontsize=11, loc="upper left")

# Grid — subtle horizontal lines aid readability
ax.grid(True, axis="y", alpha=0.3, linestyle="--")

# Tick rotation — prevents overlap with long labels
plt.xticks(rotation=45, ha="right")

# Remove top and right spines for a cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# Save to file (do this BEFORE plt.show())
plt.savefig("team_comparison.png", dpi=150, bbox_inches="tight")
plt.show()
```

---

## Part 5: Subplots — Dashboard Layout

```python
import matplotlib.pyplot as plt
import numpy as np

months   = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
revenue  = [42, 38, 55, 61, 58, 70, 75, 68, 82, 90, 95, 88]
products = ["Laptop","Phone","Tablet","Monitor"]
units    = [320, 580, 210, 145]
np.random.seed(0)
daily_rev = np.random.normal(2500, 500, 365)
cat_share = [35, 25, 20, 20]
cat_names = ["Electronics","Clothing","Food","Other"]

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Sales Dashboard — 2024", fontsize=16, fontweight="bold")

# Chart 1 — top-left: monthly revenue line
axes[0, 0].plot(months, revenue, marker="o", color="#2196F3", linewidth=2)
axes[0, 0].set_title("Monthly Revenue ($000)")
axes[0, 0].set_xlabel("Month")
axes[0, 0].grid(True, alpha=0.3)
plt.setp(axes[0, 0].xaxis.get_majorticklabels(), rotation=45, ha="right")

# Chart 2 — top-right: top products bar
axes[0, 1].bar(products, units, color="#4CAF50", edgecolor="white")
axes[0, 1].set_title("Top Products by Units")
axes[0, 1].set_ylabel("Units Sold")

# Chart 3 — bottom-left: daily revenue histogram
axes[1, 0].hist(daily_rev, bins=25, color="#FF9800", edgecolor="white", alpha=0.85)
axes[1, 0].axvline(daily_rev.mean(), color="red", linestyle="--", linewidth=1.5,
                   label=f"Mean: ${daily_rev.mean():,.0f}")
axes[1, 0].set_title("Daily Revenue Distribution")
axes[1, 0].set_xlabel("Daily Revenue ($)")
axes[1, 0].legend()

# Chart 4 — bottom-right: category pie
axes[1, 1].pie(cat_share, labels=cat_names, autopct="%1.1f%%", startangle=90)
axes[1, 1].set_title("Revenue by Category")

plt.tight_layout()
plt.savefig("sales_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("Dashboard saved as sales_dashboard.png")
```

---

## Part 6: Seaborn Quick Intro

Seaborn wraps matplotlib with prettier defaults and statistical chart types.

```python
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("employees.csv")

# --- Bar plot with confidence intervals ---
fig, ax = plt.subplots(figsize=(9, 5))
sns.barplot(data=df, x="dept", y="salary", ax=ax,
            palette="Blues_d", errorbar="sd")
ax.set_title("Average Salary by Department")
ax.set_xlabel("Department")
ax.set_ylabel("Salary ($)")
plt.tight_layout()
plt.show()

# --- Correlation heatmap ---
numeric_df = df.select_dtypes(include="number")
corr_matrix = numeric_df.corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, square=True, ax=ax)
ax.set_title("Feature Correlation Matrix")
plt.tight_layout()
plt.show()

# --- Histogram with KDE overlay ---
fig, ax = plt.subplots(figsize=(9, 5))
sns.histplot(data=df, x="salary", bins=20, kde=True, ax=ax, color="#673AB7")
ax.set_title("Salary Distribution with KDE")
plt.tight_layout()
plt.show()
```

---

## Practice Exercises

1. Load a CSV with monthly sales data and create a line chart showing the trend over time.
   Add a title, axis labels, a grid, and save it as `monthly_trend.png`.

2. Create a horizontal bar chart (`barh`) of the top 10 products by total revenue from a
   sales DataFrame. Sort bars from highest to lowest and add value labels to each bar.

3. Generate 1,000 random salary values from a normal distribution (`np.random.normal`) and
   plot a histogram with 30 bins. Add a vertical dashed line at the mean and another at the
   median. Include a legend.

4. Using `plt.subplots(1, 2)`, create a side-by-side figure: a bar chart of sales by region
   on the left, and a pie chart of the same data on the right. Give the figure a shared
   title using `fig.suptitle()`.

---

## Next Lesson

**Phase 13 complete — continue to [Phase 14 → Testing](../../phase-14-testing/concepts/lesson-01-intro-testing.md)**
