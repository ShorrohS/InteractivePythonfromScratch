# Phase 10 — Intermediate Solutions: Web Scraping

---

## Q1. CSS Selectors

```python
from bs4 import BeautifulSoup

SAMPLE_HTML = """
<div class="quotes-page">
  <div class="quote">
    <span class="text">"The world as we have created it is a process of our thinking."</span>
    <small class="author">Albert Einstein</small>
  </div>
  <div class="quote">
    <span class="text">"It is our choices that show what we truly are."</span>
    <small class="author">J.K. Rowling</small>
  </div>
  <div class="quote">
    <span class="text">"There are only two ways to live your life."</span>
    <small class="author">Albert Einstein</small>
  </div>
</div>
"""

soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

# CSS selector: element.class  (div.quote span.text)
quote_spans = soup.select("div.quote span.text")
for i, span in enumerate(quote_spans, start=1):
    print(f"Quote {i}: {span.text}")

# select_one returns the first match only
first_author = soup.select_one("small.author")
print(f"First author: {first_author.text}")
```

**Explanation:** `.select("div.quote span.text")` uses CSS selector syntax: `div.quote` means a `<div>` with class `quote`; the space means "descendant". `.select_one()` is equivalent to `find()` but accepts CSS syntax, which is often more concise for class/id selectors.

---

## Q2. Scrape a Table

```python
from bs4 import BeautifulSoup

SAMPLE_HTML = """
<table>
  <thead>
    <tr><th>Name</th><th>Language</th><th>Stars</th></tr>
  </thead>
  <tbody>
    <tr><td>Flask</td><td>Python</td><td>64000</td></tr>
    <tr><td>Django</td><td>Python</td><td>74000</td></tr>
    <tr><td>FastAPI</td><td>Python</td><td>69000</td></tr>
    <tr><td>Express</td><td>JavaScript</td><td>60000</td></tr>
    <tr><td>Rails</td><td>Ruby</td><td>54000</td></tr>
  </tbody>
</table>
"""

soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

# Extract header names from <thead>
headers = [th.text for th in soup.find("thead").find_all("th")]

# Extract data rows from <tbody>
rows = soup.find("tbody").find_all("tr")
records = []
for row in rows:
    cells = [td.text for td in row.find_all("td")]
    record = dict(zip(headers, cells))  # pair each header with its cell value
    records.append(record)

for record in records:
    print(record)
```

**Explanation:** `zip(headers, cells)` pairs each header string with the matching cell value in the same column position. `dict(zip(...))` converts those pairs directly into a dictionary. This pattern works for any table regardless of column count.

---

## Q3. Custom Headers

```python
import requests

url = "https://httpbin.org/headers"

# Define custom headers — User-Agent tells the server who is making the request
headers = {
    "User-Agent": "PythonScraper/1.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()                         # parse JSON response body
    sent_ua = data["headers"]["User-Agent"]        # httpbin echoes back headers
    print(f"Sent User-Agent: {sent_ua}")
else:
    print(f"Request failed: {response.status_code}")
```

**Explanation:** `requests.get()` accepts a `headers` dict; these are merged with the default `requests` headers. `httpbin.org/headers` is a handy echo endpoint that returns whatever headers it received as JSON — useful for testing.

---

## Q4. Error Handling

```python
import requests


def safe_fetch(url):
    """Fetch url safely; return Response or None."""
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        print(f"Network error for {url}: {e}")
        return None

    # Check for known error status codes
    if response.status_code == 200:
        return response
    elif response.status_code == 404:
        print(f"Page not found: {url}")
        return None
    elif response.status_code == 500:
        print(f"Server error at: {url}")
        return None
    else:
        print(f"Unexpected status {response.status_code}: {url}")
        return None


# Test with three endpoints
test_urls = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
]

for url in test_urls:
    result = safe_fetch(url)
    if result:
        print(f"Success: {url}")
```

**Explanation:** `requests.exceptions.RequestException` is the base class for all `requests` errors — it catches DNS failures, connection resets, and timeouts in one clause. Always set a `timeout` so your script never hangs indefinitely on a slow server.

---

## Q5. Pagination

```python
import requests
import time
from bs4 import BeautifulSoup


def scrape_quotes(num_pages):
    """Scrape quote texts from quotes.toscrape.com across num_pages pages."""
    headers = {"User-Agent": "PythonScraper/1.0"}
    all_quotes = []

    for page in range(1, num_pages + 1):
        url = f"https://quotes.toscrape.com/page/{page}/"
        print(f"Scraping page {page}...")

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print(f"  Skipping page {page} (status {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        quote_spans = soup.select("span.text")

        for span in quote_spans:
            all_quotes.append(span.get_text())

        # Polite delay between requests
        if page < num_pages:
            time.sleep(1)

    return all_quotes


quotes = scrape_quotes(3)
print(f"Total quotes collected: {len(quotes)}")
```

**Explanation:** `time.sleep(1)` pauses execution for 1 second, preventing the script from hammering the server with rapid requests. The conditional `if page < num_pages` skips the sleep after the final page since no further request follows.

---

## Q6. Save to CSV

```python
import requests
import time
import csv
from bs4 import BeautifulSoup


def scrape_quotes_full(num_pages):
    """Scrape quotes with text, author, and tags from quotes.toscrape.com."""
    headers = {"User-Agent": "PythonScraper/1.0"}
    results = []

    for page in range(1, num_pages + 1):
        url = f"https://quotes.toscrape.com/page/{page}/"
        print(f"Scraping page {page}...")

        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"  Skipping page {page} (status {response.status_code})")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        quote_divs = soup.select("div.quote")

        for div in quote_divs:
            text = div.select_one("span.text").get_text()
            author = div.select_one("small.author").get_text()

            # Collect all tag links within this quote block
            tag_links = div.select("a.tag")
            tags = "|".join(a.get_text() for a in tag_links)  # join with pipe

            results.append({"text": text, "author": author, "tags": tags})

        if page < num_pages:
            time.sleep(1)

    return results


data = scrape_quotes_full(3)

# Write to CSV
fieldnames = ["text", "author", "tags"]
with open("quotes.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()          # writes the column header row
    writer.writerows(data)        # writes all data rows

print(f"\nWrote {len(data)} rows to quotes.csv")

# Print first 3 rows for confirmation
print("\nFirst 3 rows:")
with open("quotes.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader, start=1):
        print(f"  {i}. {row['author']}: {row['text'][:50]}...")
        if i == 3:
            break
```

**Explanation:** `csv.DictWriter` maps dictionary keys to column headers automatically, making it easy to add or reorder columns later. `newline=""` is required on Windows to prevent extra blank lines between rows. Tags are joined with `|` so the CSV stays single-column per record while still being parseable.
