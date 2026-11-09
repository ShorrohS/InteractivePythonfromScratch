# ⚡ Phase 10 Cheat Sheet — Web Scraping

---

## requests Basics

```python
import requests

# Simple GET
response = requests.get("https://example.com")

# With headers and timeout
headers = {"User-Agent": "MyBot/1.0"}
response = requests.get(url, headers=headers, timeout=10)

# Check status before using response
if response.status_code == 200:
    html = response.text          # decoded string body
    raw  = response.content       # raw bytes
    data = response.json()        # parse JSON body → dict/list

# Raise immediately on 4xx/5xx
response.raise_for_status()      # raises requests.exceptions.HTTPError

# POST request
response = requests.post(url, json={"key": "value"})
response = requests.post(url, data={"field": "value"})

# Common status codes
# 200  OK            — success
# 301  Redirect      — resource moved
# 404  Not Found     — URL doesn't exist
# 429  Too Many Req  — rate-limited
# 500  Server Error  — server-side fault
```

---

## BeautifulSoup Setup

```python
from bs4 import BeautifulSoup

# Parse from string
soup = BeautifulSoup(html_string, "html.parser")

# Parse from response
soup = BeautifulSoup(response.text, "html.parser")

# Parser options:
# "html.parser"  — built-in, no install needed
# "lxml"         — faster, pip install lxml
# "html5lib"     — most lenient, pip install html5lib
```

---

## Finding Elements

```python
# find() — first match or None
soup.find("h1")                          # by tag
soup.find("p", class_="intro")          # by tag + class
soup.find("a", id="main-link")          # by tag + id
soup.find("div", attrs={"data-id": "5"})  # by any attribute

# find_all() — list of all matches (empty list if none)
soup.find_all("li")
soup.find_all("a", class_="tag")
soup.find_all(["h1", "h2", "h3"])       # multiple tag names

# Safe attribute access
tag = soup.find("a")
tag.get("href")           # None if absent (safe)
tag["href"]               # KeyError if absent (unsafe)

# Text extraction
tag.text                  # string content of tag (shortcut)
tag.get_text()            # same, but accepts separator/strip params
tag.get_text(strip=True)  # strips surrounding whitespace
```

---

## CSS Selectors

```python
# select() — list; select_one() — first match or None
soup.select("div")                       # by tag
soup.select(".classname")                # by class
soup.select("#id-name")                  # by id
soup.select("div.quote")                 # tag with class
soup.select("div.quote span.text")       # descendant
soup.select("ul > li")                   # direct child
soup.select("a[href]")                   # has attribute
soup.select("a[href^='https']")          # href starts with
soup.select("a[href$='.pdf']")           # href ends with

# Examples from quotes.toscrape.com
soup.select("div.quote span.text")       # quote texts
soup.select("small.author")             # author names
soup.select("a.tag")                    # tag links
soup.select_one("li.next a")            # next-page link
```

---

## Pagination Pattern

```python
import requests, time
from bs4 import BeautifulSoup

SITE = "https://quotes.toscrape.com"
next_url = f"{SITE}/page/1/"

all_items = []

while next_url:
    response = requests.get(next_url, headers={"User-Agent": "Bot/1.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Collect items from this page
    for el in soup.select("span.text"):
        all_items.append(el.get_text())

    # Find next page link
    next_tag = soup.select_one("li.next a")
    next_url = SITE + next_tag.get("href") if next_tag else None

    time.sleep(1)        # rate limit between requests
```

---

## Rate Limiting

```python
import time

# Simple fixed delay
time.sleep(1)            # pause 1 second

# Exponential backoff for retries
for attempt in range(1, 4):          # 3 attempts
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            break
    except requests.exceptions.RequestException:
        pass
    wait = 2 ** (attempt - 1)        # 1s, 2s, 4s
    print(f"Retry {attempt}/3 — waiting {wait}s")
    time.sleep(wait)

# Session reuse (faster, respects keep-alive)
session = requests.Session()
session.headers.update({"User-Agent": "Bot/1.0"})
response = session.get(url)          # reuses connection
```

---

## Saving Data (CSV / JSON)

```python
import csv, json

records = [
    {"text": "Quote one", "author": "Author A", "tags": "life|love"},
    {"text": "Quote two", "author": "Author B", "tags": "humor"},
]

# --- CSV ---
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["text", "author", "tags"])
    writer.writeheader()
    writer.writerows(records)

# Read CSV back
with open("data.csv", "r", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(row)

# --- JSON ---
json_records = [
    {"text": "Quote one", "author": "Author A", "tags": ["life", "love"]},
    {"text": "Quote two", "author": "Author B", "tags": ["humor"]},
]

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(json_records, f, ensure_ascii=False, indent=2)

# Read JSON back
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
print(loaded[0])
```

---

## Quick Reference

| Task | Code |
|------|------|
| Fetch page | `requests.get(url, headers=h, timeout=10)` |
| Check success | `response.status_code == 200` |
| Parse HTML | `BeautifulSoup(response.text, "html.parser")` |
| First match | `soup.find("tag")` |
| All matches | `soup.find_all("tag")` |
| CSS selector | `soup.select("div.class span")` |
| Text content | `tag.text` or `tag.get_text(strip=True)` |
| Attribute | `tag.get("href")` |
| Rate limit | `time.sleep(1)` |
| Save CSV | `csv.DictWriter` + `writeheader()` + `writerows()` |
| Save JSON | `json.dump(data, f, ensure_ascii=False, indent=2)` |
