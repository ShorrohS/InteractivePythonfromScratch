# Lesson 04 — Scraping Real Data

**Phase:** 10 — Web Scraping | **Time:** ~40 min

---

## Part 1: Handling Pagination

**Pattern 1 — predictable URL parameter:**

```python
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

for page_num in range(1, 4):     # pages 1, 2, 3
    url = BASE_URL.format(page_num)
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    print(f"Page {page_num}: {len(soup.find_all('article'))} items")
```

**Pattern 2 — follow the "Next" button** when the URL structure is not predictable:

```python
import requests
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue/"
url = BASE + "page-1.html"

while url:
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    # ... process this page ...

    next_btn = soup.find("li", class_="next")
    if next_btn:
        url = BASE + next_btn.find("a")["href"]
    else:
        url = None     # No more pages
```

---

## Part 2: Rate Limiting

Sending requests too fast can overload a server or trigger an IP ban.

```python
import requests
import time
import random

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

for page in range(1, 6):
    response = requests.get(BASE_URL.format(page), timeout=10)
    print(f"Page {page}: status {response.status_code}")

    # Fixed delay — polite minimum
    time.sleep(2)

    # Random delay — more human-like, harder to detect
    # time.sleep(random.uniform(1.0, 3.0))
```

---

## Part 3: Retry Logic and Error Handling

```python
import requests
import time

def fetch_page(url: str, max_retries: int = 3) -> requests.Response | None:
    """Fetch a URL with exponential back-off. Returns None after all retries fail."""
    headers = {"User-Agent": "StudentScraper/1.0 (Python learning project)"}

    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            return response

        except requests.exceptions.HTTPError as e:
            print(f"  HTTP error attempt {attempt}: {e}")
            if response.status_code in (403, 404):
                return None    # Client errors won't fix themselves

        except requests.exceptions.ConnectionError:
            print(f"  Connection error attempt {attempt}")

        except requests.exceptions.Timeout:
            print(f"  Timeout attempt {attempt}")

        if attempt < max_retries:
            wait = 2 ** attempt    # 2 s, 4 s, 8 s
            print(f"  Retrying in {wait}s...")
            time.sleep(wait)

    return None
```

---

## Part 4: Handling Missing Data

`find()` returns `None` when an element is absent. Guard every extraction.

```python
from bs4 import BeautifulSoup

def extract_product(article) -> dict:
    """Extract product data from a single <article> tag."""
    name_tag   = article.find("h3")
    price_tag  = article.find("p", class_="price_color")
    link_tag   = article.find("a")
    rating_tag = article.find("p", class_="star-rating")

    # Use get_text() safely; calling .text on None raises AttributeError
    name  = name_tag.get_text(strip=True)  if name_tag  else "Unknown"
    price = price_tag.get_text(strip=True) if price_tag else "N/A"

    # .get() on a tag attribute is safer than dict-style access
    url   = link_tag.get("href", "")       if link_tag  else ""

    # "class" returns a list — the rating word is the second item
    if rating_tag and len(rating_tag.get("class", [])) > 1:
        rating = rating_tag["class"][1]
    else:
        rating = "None"

    return {"name": name, "price": price, "url": url, "rating": rating}
```

---

## Part 5: Respecting robots.txt

`robots.txt` at the root of every site tells crawlers which paths are allowed.

```
User-agent: *
Disallow: /admin/
Crawl-delay: 2
Allow: /public/
```

Check it before scraping:

```python
import urllib.robotparser

def is_allowed(site_url: str, path: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{site_url}/robots.txt")
    rp.read()
    return rp.can_fetch("*", f"{site_url}{path}")

if is_allowed("https://books.toscrape.com", "/catalogue/page-1.html"):
    print("Scraping permitted")
else:
    print("Blocked by robots.txt — do not scrape this path")
```

**Ethical scraping checklist:**
- ✅ Check `robots.txt` and honour `Disallow` rules
- ✅ Read the site's Terms of Service
- ✅ Add delays between requests (1–2 s minimum)
- ✅ Use a descriptive `User-Agent` header
- ✅ Only collect data you actually need

---

## Part 6: Saving to CSV

```python
import csv

def save_to_csv(data: list[dict], filename: str) -> None:
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} records to {filename}")
```

---

## Part 7: Saving to JSON

```python
import json

def save_to_json(data: list[dict], filename: str) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(data)} records to {filename}")
```

---

## Part 8: Complete Project — 3-Page Catalog Scraper

```python
import requests, time, random, csv
from bs4 import BeautifulSoup

BASE_URL    = "https://books.toscrape.com/catalogue/page-{}.html"
OUTPUT_FILE = "books.csv"
PAGES       = 3
HEADERS     = {"User-Agent": "StudentScraper/1.0 (Python learning project)"}


def fetch(url: str) -> BeautifulSoup | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"  Error: {e}")
        return None


def extract_books(soup: BeautifulSoup) -> list[dict]:
    books = []
    for art in soup.select("article.product_pod"):
        n = art.find("h3")
        p = art.find("p", class_="price_color")
        r = art.find("p", class_="star-rating")
        a = art.find("a")
        books.append({
            "name":   n.get_text(strip=True) if n else "N/A",
            "price":  p.get_text(strip=True) if p else "N/A",
            "rating": r["class"][1]           if r else "N/A",
            "url":    a.get("href", "")       if a else "",
        })
    return books


def save_csv(data: list[dict], filename: str) -> None:
    if not data:
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} rows → {filename}")


all_books: list[dict] = []

for page_num in range(1, PAGES + 1):
    url = BASE_URL.format(page_num)
    print(f"Scraping page {page_num}: {url}")

    soup = fetch(url)
    if soup:
        books = extract_books(soup)
        all_books.extend(books)
        print(f"  {len(books)} books found (total: {len(all_books)})")
    else:
        print(f"  Skipping page {page_num}")

    if page_num < PAGES:
        delay = random.uniform(1.0, 2.5)
        print(f"  Waiting {delay:.1f}s...")
        time.sleep(delay)

save_csv(all_books, OUTPUT_FILE)
print(f"\nDone. {len(all_books)} books scraped from {PAGES} pages.")
```

---

## Practice Exercises

1. Extend the project to scrape **5 pages** and save to both `books.csv` and
   `books.json`.

2. Add a `robots.txt` check before the loop. Exit gracefully if `/catalogue/` is
   disallowed for the scraper's User-Agent.

3. Replace `fetch()` with the retry version from Part 3 (exponential back-off).

4. Extend `extract_books()` to also capture the availability status from
   `<p class="instock availability">`. Handle pages where the tag is missing.

---

## Next Lesson

**Phase 10 Complete! Continue to
[Phase 11 → Working with APIs](../../phase-11-apis/concepts/lesson-01-http-methods.md)**
