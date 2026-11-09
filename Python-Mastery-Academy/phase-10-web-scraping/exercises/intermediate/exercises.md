# Phase 10 — Intermediate Exercises: Web Scraping

> These exercises require complete, runnable programs.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`
>
> Install dependencies first:
> ```
> pip install requests beautifulsoup4
> ```

---

**Q1. CSS Selectors**

Use the HTML string below to practise CSS selector syntax. Using only `.select()` and `.select_one()` (not `.find()` or `.find_all()`):

1. Select all quote text elements with `soup.select("div.quote span.text")` and print each.
2. Select just the first author with `soup.select_one("small.author")` and print the name.

```python
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
```

**Expected output:**
```
Quote 1: "The world as we have created it is a process of our thinking."
Quote 2: "It is our choices that show what we truly are."
Quote 3: "There are only two ways to live your life."
First author: Albert Einstein
```

> **Hints:**
> - `.select()` returns a list; iterate with `enumerate(..., start=1)`.
> - `.select_one()` returns the first match or `None`.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q2. Scrape a Table**

Given the HTML table below, parse it into a list of dictionaries where each dictionary represents one row, using the header row as keys.

```python
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
```

Print each resulting dictionary on its own line.

**Expected output:**
```
{'Name': 'Flask', 'Language': 'Python', 'Stars': '64000'}
{'Name': 'Django', 'Language': 'Python', 'Stars': '74000'}
{'Name': 'FastAPI', 'Language': 'Python', 'Stars': '69000'}
{'Name': 'Express', 'Language': 'JavaScript', 'Stars': '60000'}
{'Name': 'Rails', 'Language': 'Ruby', 'Stars': '54000'}
```

> **Hints:**
> - `soup.find("thead").find_all("th")` gives the header cells; extract `.text` for each.
> - `soup.find("tbody").find_all("tr")` gives the data rows.
> - For each row use `zip(headers, [td.text for td in row.find_all("td")])` to build the dict.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q3. Custom Headers**

Some websites reject requests with the default `requests` User-Agent. Make a GET request to `https://httpbin.org/headers` with a custom `User-Agent` string `"PythonScraper/1.0"`, then parse the JSON response to confirm the header was sent.

Print the `User-Agent` value returned by httpbin.

**Expected output:**
```
Sent User-Agent: PythonScraper/1.0
```

> **Hints:**
> - Pass a `headers` dictionary as the second argument to `requests.get()`.
> - `response.json()` parses the JSON body into a Python dict.
> - The returned JSON has structure: `{"headers": {"User-Agent": "..."}}`

> **Difficulty:** ⭐⭐ Intermediate

---

**Q4. Error Handling**

Write a function `safe_fetch(url)` that:
1. Wraps the request in a `try/except requests.exceptions.RequestException` block.
2. Returns `None` and prints a warning if a network error occurs.
3. After a successful request, checks `response.status_code`:
   - 200 → return the response object
   - 404 → print `"Page not found: {url}"` and return `None`
   - 500 → print `"Server error at: {url}"` and return `None`
   - anything else → print `"Unexpected status {code}: {url}"` and return `None`

Test your function with three URLs:
- `https://httpbin.org/status/200` — should succeed
- `https://httpbin.org/status/404` — should print not-found message
- `https://httpbin.org/status/500` — should print server-error message

> **Hints:**
> - `requests.get(url, timeout=5)` sets a 5-second timeout (good practice).
> - The `requests.exceptions.RequestException` base class catches all network errors.
> - Check `status_code` with `if/elif` after confirming no exception was raised.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q5. Pagination**

Write a function `scrape_quotes(num_pages)` that:
1. Fetches pages 1 through `num_pages` of `https://quotes.toscrape.com/page/{n}/`.
2. Waits 1 second between requests (`time.sleep(1)`).
3. Sets a `User-Agent` header of `"PythonScraper/1.0"`.
4. On each page, collects every quote text (the `<span class="text">` content).
5. Returns a list of all quote strings.

Call the function with `num_pages=3` and print the total number of quotes collected.

**Expected output:**
```
Scraping page 1...
Scraping page 2...
Scraping page 3...
Total quotes collected: 30
```

> **Hints:**
> - `import time` and call `time.sleep(1)` between each request.
> - Build the URL with an f-string: `f"https://quotes.toscrape.com/page/{page}/"`.
> - Use `soup.select("span.text")` to get quote spans.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q6. Save to CSV**

Using the quotes list returned by `scrape_quotes(3)` from Q5:
1. Also collect the author (`<small class="author">`) and tags (`<a class="tag">` — there may be multiple per quote).
2. Write the data to `quotes.csv` with columns: `text`, `author`, `tags` (join multiple tags with `|`).
3. Print the first 3 rows of the CSV to confirm.

The function should return a list of dicts:
```python
[{"text": "...", "author": "...", "tags": "love|inspirational"}, ...]
```

> **Hints:**
> - `import csv`
> - `csv.DictWriter(f, fieldnames=["text", "author", "tags"])` creates a writer.
> - Call `.writeheader()` before writing rows.
> - Join tags list with `"|".join(tags)`.

> **Difficulty:** ⭐⭐ Intermediate

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
