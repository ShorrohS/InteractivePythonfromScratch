# Phase 10 — Advanced Solutions: Web Scraping

> Install dependencies:
> ```
> pip install requests beautifulsoup4
> ```

---

## Q1. Scraper Class

```python
import time
import requests
from bs4 import BeautifulSoup


class Scraper:
    """A reusable scraper with session management and rate limiting."""

    def __init__(self, base_url, delay=1.0):
        self.base_url = base_url
        self.delay = delay

        # A Session reuses the same TCP connection and persists headers
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PythonScraper/1.0"})

    def _get(self, url):
        """Fetch url using the shared session; return Response or None."""
        try:
            response = self.session.get(url, timeout=10)
            time.sleep(self.delay)      # polite delay after every request
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] {url}: {e}")
            return None

    def scrape_page(self, page_num):
        """Fetch one page and return a list of quote text strings."""
        url = f"{self.base_url}{page_num}/"
        response = self._get(url)

        if response is None or response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        return [span.get_text() for span in soup.select("span.text")]


# Demonstration
scraper = Scraper("https://quotes.toscrape.com/page/")

page1 = scraper.scrape_page(1)
print(f"Page 1: {len(page1)} quotes")
for q in page1[:3]:
    print(f"  {q[:60]}...")

page2 = scraper.scrape_page(2)
print(f"Page 2: {len(page2)} quotes")
```

---

## Q2. Pagination Loop

```python
import time
import requests
from bs4 import BeautifulSoup

SITE_ROOT = "https://quotes.toscrape.com"


class Scraper:
    """Scraper with session, rate limiting, and auto-pagination."""

    def __init__(self, base_url, delay=1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PythonScraper/1.0"})

    def _get(self, url):
        try:
            response = self.session.get(url, timeout=10)
            time.sleep(self.delay)
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] {url}: {e}")
            return None

    def scrape_all(self):
        """Follow 'next' links until none is found; return all quote texts."""
        all_quotes = []
        next_url = f"{SITE_ROOT}/page/1/"

        while next_url:
            print(f"Fetching: {next_url}")
            response = self._get(next_url)

            if response is None or response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")

            # Collect quotes from this page
            for span in soup.select("span.text"):
                all_quotes.append(span.get_text())

            # Look for a "next" pagination link
            next_tag = soup.select_one("li.next a")
            if next_tag:
                href = next_tag.get("href")          # e.g. "/page/2/"
                next_url = SITE_ROOT + href          # absolute URL
            else:
                next_url = None                      # no more pages

        return all_quotes


scraper = Scraper(SITE_ROOT)
all_quotes = scraper.scrape_all()
print(f"\nTotal quotes: {len(all_quotes)}")
```

---

## Q3. Deduplication

```python
import time
import requests
from bs4 import BeautifulSoup

SITE_ROOT = "https://quotes.toscrape.com"


class Scraper:
    """Scraper with session, auto-pagination, and deduplication."""

    def __init__(self, base_url, delay=1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PythonScraper/1.0"})

    def _get(self, url):
        try:
            response = self.session.get(url, timeout=10)
            time.sleep(self.delay)
            return response
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] {url}: {e}")
            return None

    def scrape_all(self):
        """Scrape all pages with deduplication; return unique quote dicts."""
        unique_quotes = []
        seen_texts = set()          # track texts already collected
        duplicates = 0
        next_url = f"{SITE_ROOT}/page/1/"

        while next_url:
            print(f"Fetching: {next_url}")
            response = self._get(next_url)

            if response is None or response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            page_url = next_url

            for div in soup.select("div.quote"):
                text = div.select_one("span.text").get_text()
                author = div.select_one("small.author").get_text()
                tags = [a.get_text() for a in div.select("a.tag")]

                if text in seen_texts:
                    duplicates += 1
                    continue        # skip duplicate

                seen_texts.add(text)
                unique_quotes.append({
                    "text": text,
                    "author": author,
                    "tags": tags,
                    "url": page_url,
                })

            next_tag = soup.select_one("li.next a")
            next_url = SITE_ROOT + next_tag.get("href") if next_tag else None

        print(f"Collected {len(unique_quotes)} unique quotes "
              f"({duplicates} duplicates removed)")
        return unique_quotes


scraper = Scraper(SITE_ROOT)
results = scraper.scrape_all()
```

---

## Q4. Retry Logic

```python
import time
import requests
from bs4 import BeautifulSoup

SITE_ROOT = "https://quotes.toscrape.com"
MAX_RETRIES = 3


class Scraper:
    """Scraper with session, auto-pagination, deduplication, and retry."""

    def __init__(self, base_url, delay=1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PythonScraper/1.0"})

    def _get(self, url):
        """Fetch url with up to MAX_RETRIES attempts and exponential backoff."""
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.get(url, timeout=10)
                time.sleep(self.delay)

                # Retry on server errors (5xx)
                if response.status_code >= 500:
                    wait = 2 ** (attempt - 1)   # 1s, 2s, 4s
                    print(f"[RETRY {attempt}/{MAX_RETRIES}] "
                          f"status {response.status_code} for {url} "
                          f"— waiting {wait}s")
                    if attempt < MAX_RETRIES:
                        time.sleep(wait)
                    continue

                return response                 # success

            except requests.exceptions.RequestException as e:
                wait = 2 ** (attempt - 1)
                print(f"[RETRY {attempt}/{MAX_RETRIES}] error: {e} "
                      f"— waiting {wait}s")
                if attempt < MAX_RETRIES:
                    time.sleep(wait)

        print(f"[FAILED] Gave up on {url} after {MAX_RETRIES} attempts")
        return None

    def scrape_page(self, page_num):
        url = f"{self.base_url}{page_num}/"
        response = self._get(url)
        if response is None or response.status_code != 200:
            return []
        soup = BeautifulSoup(response.text, "html.parser")
        return [span.get_text() for span in soup.select("span.text")]


# Test retry with a 500-returning endpoint
print("=== Testing retry logic ===")
test_scraper = Scraper("https://httpbin.org/status/")
test_scraper.scrape_page(500)   # should trigger 3 retries then give up

# Normal usage
print("\n=== Normal scrape ===")
scraper = Scraper(SITE_ROOT)
quotes = scraper.scrape_page(1)
print(f"Page 1 quotes: {len(quotes)}")
```

---

## Q5. Save to JSON

```python
import json
import os
import time
import requests
from bs4 import BeautifulSoup

SITE_ROOT = "https://quotes.toscrape.com"
MAX_RETRIES = 3
OUTPUT_FILE = "scraped_quotes.json"


class Scraper:
    """Full scraper: session, pagination, deduplication, retry, JSON output."""

    def __init__(self, base_url, delay=1.0):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "PythonScraper/1.0"})

    def _get(self, url):
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = self.session.get(url, timeout=10)
                time.sleep(self.delay)
                if response.status_code >= 500:
                    wait = 2 ** (attempt - 1)
                    if attempt < MAX_RETRIES:
                        time.sleep(wait)
                    continue
                return response
            except requests.exceptions.RequestException as e:
                if attempt < MAX_RETRIES:
                    time.sleep(2 ** (attempt - 1))
        return None

    def scrape_all(self):
        """Scrape every page; return deduplicated list of quote dicts."""
        unique_quotes = []
        seen_texts = set()
        next_url = f"{SITE_ROOT}/page/1/"

        while next_url:
            print(f"Fetching: {next_url}")
            response = self._get(next_url)
            if response is None or response.status_code != 200:
                break

            soup = BeautifulSoup(response.text, "html.parser")
            page_url = next_url

            for div in soup.select("div.quote"):
                text = div.select_one("span.text").get_text()
                author = div.select_one("small.author").get_text()
                tags = [a.get_text() for a in div.select("a.tag")]

                if text in seen_texts:
                    continue
                seen_texts.add(text)
                unique_quotes.append({
                    "text": text,
                    "author": author,
                    "tags": tags,
                    "url": page_url,
                })

            next_tag = soup.select_one("li.next a")
            next_url = SITE_ROOT + next_tag.get("href") if next_tag else None

        return unique_quotes


scraper = Scraper(SITE_ROOT)
data = scraper.scrape_all()

# Write JSON — ensure_ascii=False preserves curly quotes and accents
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

size_kb = os.path.getsize(OUTPUT_FILE) / 1024
print(f"\nSaved {len(data)} quotes to {OUTPUT_FILE} ({size_kb:.1f} KB)")
```

---

## Q6. Data Normalisation

```python
def normalise(records):
    """
    Clean a list of quote dicts:
    - Strip whitespace and curly quotes from text and author.
    - Lowercase all tags.
    - Remove duplicate tags (preserve order).
    - Drop records with empty text.
    """
    cleaned = []

    for record in records:
        text = record.get("text", "")
        author = record.get("author", "")
        tags = record.get("tags", [])

        # 1. Strip whitespace then curly-quote characters
        text = text.strip().strip("\u201c\u201d")
        author = author.strip()

        # 2. Drop records with empty text
        if not text:
            continue

        # 3. Lowercase all tags
        tags = [t.lower() for t in tags]

        # 4. Deduplicate tags while preserving order
        seen = set()
        unique_tags = []
        for t in tags:
            if t not in seen:
                seen.add(t)
                unique_tags.append(t)

        cleaned.append({
            "text": text,
            "author": author,
            "tags": unique_tags,
        })

    return cleaned


# --- Demonstration ---
test_records = [
    {
        "text": "  \u201cLearn Python.\u201d  ",
        "author": " Guido ",
        "tags": ["Python", "python", "Learning"],
    },
    {
        "text": "",
        "author": "Nobody",
        "tags": [],
    },
    {
        "text": "\u201cSimple is better.\u201d",
        "author": "Tim Peters",
        "tags": ["zen", "ZEN", "simple"],
    },
]

print("=== BEFORE ===")
for r in test_records:
    print(r)

result = normalise(test_records)

print("\n=== AFTER ===")
for r in result:
    print(r)
```

**Expected output:**
```
=== BEFORE ===
{'text': '  \u201cLearn Python.\u201d  ', 'author': ' Guido ', 'tags': ['Python', 'python', 'Learning']}
{'text': '', 'author': 'Nobody', 'tags': []}
{'text': '\u201cSimple is better.\u201d', 'author': 'Tim Peters', 'tags': ['zen', 'ZEN', 'simple']}

=== AFTER ===
{'text': 'Learn Python.', 'author': 'Guido', 'tags': ['python', 'learning']}
{'text': 'Simple is better.', 'author': 'Tim Peters', 'tags': ['zen', 'simple']}
```

**Explanation:** The empty-text record is dropped entirely. Curly quotes (`\u201c` / `\u201d`) are removed with `.strip()` chained — Python's `.strip()` accepts a string of characters to remove, not a substring, so you pass the two characters directly. Tag deduplication uses a `set` for O(1) membership testing while a separate list preserves insertion order.
