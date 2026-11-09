# Phase 10 — Advanced Exercises: Web Scraping

> These exercises require complete, well-structured programs.
> Plan your class and function design before writing code.
> Solutions: `../../solutions/advanced/solutions.md`
>
> Install dependencies first:
> ```
> pip install requests beautifulsoup4
> ```

---

**Q1. Scraper Class**

Design a `Scraper` class that encapsulates the HTTP session and rate-limiting logic:

- `__init__(self, base_url, delay=1.0)` — stores `base_url` and `delay`; creates a `requests.Session` with a `User-Agent` header of `"PythonScraper/1.0"`.
- `_get(self, url)` — sends a GET request via the session, sleeps for `self.delay` seconds **after** the request, and returns the response (or `None` on error).
- `scrape_page(self, page_num)` — builds the page URL from `base_url` and `page_num`, fetches it, parses quote texts, and returns a list of text strings.

Demonstrate the class by creating a `Scraper("https://quotes.toscrape.com/page/")` instance and calling `scrape_page(1)` and `scrape_page(2)`.

> **Hints:**
> - `session = requests.Session()` persists headers across requests.
> - `session.headers.update({"User-Agent": "..."})` sets headers once at init.
> - Use `try/except` inside `_get()` so a bad page doesn't crash the whole scraper.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q2. Pagination Loop**

Extend the `Scraper` class from Q1 with a `scrape_all(self)` method that:

1. Starts at page 1.
2. On each page, looks for a `<li class="next"><a href="...">` link.
3. Follows the link to the next page.
4. Stops automatically when no "next" link is found (i.e. last page reached).
5. Returns a flat list of all collected quote texts.

Print the total number of quotes found across all pages.

> **Hints:**
> - `soup.select_one("li.next a")` finds the "Next →" link.
> - `.get("href")` gives the relative path; prepend the site root: `"https://quotes.toscrape.com"`.
> - Maintain a `next_url` variable; set it to `None` when no next link is found.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q3. Deduplication**

When scraping multiple pages (or re-running a scraper), you may collect duplicate items. Extend `scrape_all()` so that:

1. Each quote dict also includes a `"url"` field (the page URL it was found on).
2. Deduplication is performed using the quote text as a unique key.
3. If a quote text is seen a second time, it is silently skipped.
4. Print a summary: `Collected N unique quotes (M duplicates removed)`.

You can simulate duplicates by passing the same page URL twice inside `scrape_all()` before running the real deduplication logic.

> **Hints:**
> - A `set()` of already-seen texts is the most efficient deduplication structure.
> - `if text in seen: duplicates += 1; continue` is the pattern.
> - Each quote dict: `{"text": ..., "author": ..., "tags": [...], "url": ...}`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q4. Retry Logic**

Wrap the `_get(self, url)` method in a retry loop:

- Maximum **3 attempts**.
- On a connection error (`requests.exceptions.RequestException`) or a 5xx response, wait before retrying:
  - Attempt 1 fails → wait 1 second
  - Attempt 2 fails → wait 2 seconds
  - Attempt 3 fails → return `None` and log the failure
- On a successful response (any 2xx status), return immediately without retrying.
- Print a message each time a retry is triggered: `"Retry {attempt}/3 for {url}"`.

Test by temporarily pointing `_get()` at `https://httpbin.org/status/500` to confirm three attempts are made.

> **Hints:**
> - `for attempt in range(1, 4):` gives you 3 tries numbered 1, 2, 3.
> - Exponential backoff: `wait = 2 ** (attempt - 1)` gives 1, 2, 4 seconds.
> - `response.ok` is `True` for status codes 200–299.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q5. Save to JSON**

Using `scrape_all()` (with deduplication) from Q3, scrape all pages of `https://quotes.toscrape.com/` and save the results to `scraped_quotes.json` as a JSON array of objects:

```json
[
  {
    "text": "\u201cThe world as we have created it...\u201d",
    "author": "Albert Einstein",
    "tags": ["change", "deep-thoughts", "thinking", "world"],
    "url": "https://quotes.toscrape.com/page/1/"
  },
  ...
]
```

After writing, print:
- Total quotes saved
- File size in KB (rounded to 1 decimal place)

> **Hints:**
> - `import json`
> - `json.dump(data, f, ensure_ascii=False, indent=2)` writes readable JSON.
> - `import os; os.path.getsize("scraped_quotes.json") / 1024` gives KB.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q6. Data Normalisation**

After scraping, raw data often needs cleaning. Write a function `normalise(records)` that processes a list of quote dicts and:

1. Strips leading/trailing whitespace from `text` and `author`.
2. Removes the curly-quote characters `\u201c` and `\u201d` from the start/end of `text`.
3. Lowercases every tag in the `tags` list.
4. Removes duplicate tags within the same record (preserve order using a seen-set).
5. Drops records where `text` is empty after stripping.
6. Returns the cleaned list.

Demonstrate by constructing a list of messy test records and showing the before/after output.

```python
test_records = [
    {"text": "  \u201cLearn Python.\u201d  ", "author": " Guido ", "tags": ["Python", "python", "Learning"]},
    {"text": "", "author": "Nobody", "tags": []},
    {"text": "\u201cSimple is better.\u201d", "author": "Tim Peters", "tags": ["zen", "ZEN", "simple"]},
]
```

> **Hints:**
> - `text.strip().strip("\u201c\u201d")` removes both outer whitespace and curly quotes.
> - For deduplicating tags while preserving order:
>   ```python
>   seen = set()
>   unique_tags = [t for t in tags if not (t in seen or seen.add(t))]
>   ```
> - Use a list comprehension with a condition to drop empty-text records.

> **Difficulty:** ⭐⭐⭐ Advanced

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
