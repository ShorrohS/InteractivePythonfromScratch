# Lesson 03 — Parsing HTML with BeautifulSoup

**Phase:** 10 — Web Scraping | **Time:** ~35 min

---

## Part 1: Setup

```bash
pip install requests beautifulsoup4 lxml
```

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com")
soup = BeautifulSoup(response.text, "html.parser")
# or faster: BeautifulSoup(response.text, "lxml")
```

---

## Part 2: Navigating the Tree

```python
# Accessing by attribute
soup.title          # <title> tag
soup.title.string   # text inside title
soup.body           # <body> tag
soup.h1             # first h1
soup.h1.text        # text content (strips tags)
soup.h1.string      # only if no children tags

# Parent/children
tag.parent
tag.children        # generator
tag.contents        # list
tag.next_sibling
tag.previous_sibling
```

---

## Part 3: find() and find_all()

```python
# find() — first match
soup.find("h2")                          # first h2
soup.find("div", id="content")           # by id
soup.find("p", class_="description")    # by class
soup.find("a", href=True)               # has href

# find_all() — all matches
soup.find_all("p")                       # all paragraphs
soup.find_all(["h1","h2","h3"])          # multiple tags
soup.find_all("li", limit=5)             # first 5
soup.find_all("div", class_="product")  # by class

# Nested search
container = soup.find("div", class_="products")
items = container.find_all("div", class_="item")
```

---

## Part 4: CSS Selectors with select()

```python
# select() returns a list
soup.select("div.product")         # div with class product
soup.select("#results")            # id=results
soup.select("table > tr > td")    # direct children
soup.select("a[href]")             # links with href
soup.select("span.price")[0]       # first price span

# select_one() returns first match
soup.select_one("h1")
soup.select_one("#main-title")
```

---

## Part 5: Extracting Data

```python
tag = soup.find("a")

# Text content
tag.text        # all text (includes children)
tag.string      # only if no nested tags
tag.get_text()  # same as .text
tag.get_text(strip=True)          # remove whitespace
tag.get_text(separator=", ")      # join with separator

# Attributes
tag["href"]                       # direct access
tag.get("href")                   # safe access (None if missing)
tag.get("href", "#")              # with default
tag.attrs                         # all attributes as dict

# Numbers — always strip and convert
price_text = soup.find("span", class_="price").text.strip()
price = float(price_text.replace("$","").replace(",",""))
```

---

## Part 6: Scraping a Table

```python
table = soup.find("table", class_="data-table")
headers = [th.text.strip() for th in table.find_all("th")]

rows = []
for tr in table.find_all("tr")[1:]:   # skip header row
    cells = [td.text.strip() for td in tr.find_all("td")]
    if cells:
        rows.append(dict(zip(headers, cells)))
```

---

## Part 7: Ethics & Best Practices

```python
import time, random

# 1. Always check robots.txt
# 2. Add delays between requests
time.sleep(random.uniform(1, 3))

# 3. Set User-Agent header (identify yourself)
headers = {"User-Agent": "MyResearchBot/1.0 (student project)"}
response = requests.get(url, headers=headers)

# 4. Handle errors gracefully
if response.status_code != 200:
    print(f"Failed: {response.status_code}")
    return

# 5. Cache results — don't re-scrape unnecessarily
```

---

## Practice Exercises

1. Using the `requests` + `BeautifulSoup` libraries, write a program that fetches `https://books.toscrape.com` (a legal practice site) and extracts all book titles.

2. Extend it to also extract prices.

3. Save the results to a CSV file.

---

## Next Lesson

**[Project → News Scraper](../guided-projects/project-01-news-scraper/)**
