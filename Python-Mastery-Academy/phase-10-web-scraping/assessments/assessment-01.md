# Phase 10 — Completion Assessment

**Pass mark: 80% | Time: 30 minutes**

> Install dependencies before starting:
> ```
> pip install requests beautifulsoup4
> ```

---

## PART A: Write the Code

**Task 1. fetch_links(url)**

Write a function `fetch_links(url)` that:
1. Makes a GET request to `url` using a `User-Agent` header of `"PythonScraper/1.0"` and a 10-second timeout.
2. Returns a list of all `href` attribute values from `<a>` tags on the page.
3. Handles errors gracefully:
   - If a `requests.exceptions.RequestException` occurs, print a warning and return an empty list.
   - If the status code is not 200, print a warning and return an empty list.
4. Skips `<a>` tags that have no `href` attribute (do not include `None` in the result).

Test your function:
```python
links = fetch_links("https://quotes.toscrape.com/")
print(f"Found {len(links)} links")
for link in links[:5]:
    print(f"  {link}")
```

---

**Task 2. table_to_dicts(html)**

Write a function `table_to_dicts(html)` that:
1. Accepts an HTML string containing a single `<table>` element.
2. Uses the `<th>` cells in the first `<tr>` as dictionary keys.
3. Returns a list of dicts, one per data row.

Test your function with this HTML:

```python
TABLE_HTML = """
<table>
  <tr>
    <th>Product</th><th>Category</th><th>Price</th><th>Stock</th>
  </tr>
  <tr><td>Laptop</td><td>Electronics</td><td>999.99</td><td>15</td></tr>
  <tr><td>Desk</td><td>Furniture</td><td>249.00</td><td>8</td></tr>
  <tr><td>Notebook</td><td>Stationery</td><td>3.50</td><td>200</td></tr>
</table>
"""

rows = table_to_dicts(TABLE_HTML)
for row in rows:
    print(row)
```

**Expected output:**
```
{'Product': 'Laptop', 'Category': 'Electronics', 'Price': '999.99', 'Stock': '15'}
{'Product': 'Desk', 'Category': 'Furniture', 'Price': '249.00', 'Stock': '8'}
{'Product': 'Notebook', 'Category': 'Stationery', 'Price': '3.50', 'Stock': '200'}
```

---

## PART B: Predict the Output / Explain the Error

**Q3.** What does this code print? Explain each line of output.

```python
from bs4 import BeautifulSoup

html = """
<ul>
  <li class="active">Home</li>
  <li>About</li>
  <li class="active">Contact</li>
</ul>
"""

soup = BeautifulSoup(html, "html.parser")
items = soup.find_all("li", class_="active")
print(len(items))
for item in items:
    print(item.text)
```

---

**Q4.** This code raises an error at runtime. Identify the error type, explain why it happens, and write the corrected version.

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://quotes.toscrape.com/page/999/")
soup = BeautifulSoup(response.text, "html.parser")

# Page 999 does not exist — the "next" link will be absent
next_link = soup.select_one("li.next a")
print(next_link.get("href"))
```

---

## PART C: Find the Bugs

**Q5.** The following scraper has **3 bugs**. Identify each bug and state the fix.

```python
import requests
from bs4 import BeautifulSoup
import time

def scrape_books():
    results = []
    page = 1

    while page <= 3:
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html")        # Bug A

        books = soup.select("article.product_pod h3 a")
        for book in books:
            title = book["title"]
            results.append(title)

        page += 1

    with open("books.txt", "w") as f:                     # Bug B
        for title in results:
            f.write(title + "\n")

    return results

scrape_books()
# time.sleep is never called between requests                # Bug C
```

---

## Answers

### PART A — Task 1: fetch_links

```python
import requests
from bs4 import BeautifulSoup

def fetch_links(url):
    headers = {"User-Agent": "PythonScraper/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Warning: network error for {url}: {e}")
        return []

    if response.status_code != 200:
        print(f"Warning: status {response.status_code} for {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    hrefs = []
    for a in soup.find_all("a"):
        href = a.get("href")
        if href is not None:        # skip tags without href
            hrefs.append(href)
    return hrefs
```

---

### PART A — Task 2: table_to_dicts

```python
from bs4 import BeautifulSoup

def table_to_dicts(html):
    soup = BeautifulSoup(html, "html.parser")
    all_rows = soup.find("table").find_all("tr")

    # First row contains headers
    headers = [th.text for th in all_rows[0].find_all("th")]

    # Remaining rows are data
    records = []
    for row in all_rows[1:]:
        cells = [td.text for td in row.find_all("td")]
        records.append(dict(zip(headers, cells)))
    return records
```

---

### PART B — Q3 Answer

**Output:**
```
2
Home
Contact
```

**Explanation:**
- `find_all("li", class_="active")` returns only the two `<li>` elements that have `class="active"` — the "About" item is excluded.
- `len(items)` is therefore `2`.
- The loop prints the `.text` of each matched element: `"Home"` then `"Contact"`.

---

### PART B — Q4 Answer

**Error type:** `AttributeError: 'NoneType' object has no attribute 'get'`

**Why:** Page 999 does not exist on `quotes.toscrape.com`, so there is no "next" pagination link in the HTML. `soup.select_one("li.next a")` returns `None`. Calling `.get("href")` on `None` raises `AttributeError`.

**Fix:**
```python
next_link = soup.select_one("li.next a")
if next_link:
    print(next_link.get("href"))
else:
    print("No next page.")
```

---

### PART C — Q5 Bugs

**Bug A — Wrong parser string:**
```python
# Wrong:
soup = BeautifulSoup(response.text, "html")
# Fixed:
soup = BeautifulSoup(response.text, "html.parser")
```
`"html"` is not a recognised parser. Use `"html.parser"` (built-in) or `"lxml"`.

**Bug B — Missing file encoding:**
```python
# Wrong:
with open("books.txt", "w") as f:
# Fixed:
with open("books.txt", "w", encoding="utf-8") as f:
```
Book titles may contain non-ASCII characters; `encoding="utf-8"` prevents `UnicodeEncodeError`.

**Bug C — No rate limiting:**
```python
# Missing: time.sleep() between requests
# Fix: add inside the while loop, after page += 1 (or before the next iteration):
import time
# ...
page += 1
time.sleep(1)   # polite 1-second delay between pages
```
Without a delay, the scraper hammers the server with rapid requests, which is impolite and risks triggering a ban.
