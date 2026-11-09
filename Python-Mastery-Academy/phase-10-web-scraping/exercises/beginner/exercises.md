# Phase 10 — Beginner Exercises: Web Scraping

> Attempt all before checking solutions.
> Solutions: `../../solutions/beginner/solutions.md`
>
> Install dependencies first:
> ```
> pip install requests beautifulsoup4
> ```

---

**Q1. First Request**

Import the `requests` library, send a GET request to `https://httpbin.org/get`, then print:
1. The HTTP status code
2. The first 200 characters of the response body (`response.text`)

**Expected output (approximately):**
```
Status code: 200
First 200 chars:
{
  "args": {},
  "headers": {
    "Accept": "*/*",
    ...
```

> **Hints:**
> - `import requests` at the top of your file.
> - `response = requests.get(url)` sends the request.
> - `response.status_code` gives the numeric HTTP status.
> - `response.text` gives the response body as a string; slice with `[:200]`.

> **Difficulty:** ⭐ Beginner

---

**Q2. Parse HTML**

Use the HTML string below to create a `BeautifulSoup` object with the `"html.parser"` parser, then find and print the content of the `<title>` tag.

```python
SAMPLE_HTML = """
<!DOCTYPE html>
<html>
  <head><title>My Practice Page</title></head>
  <body>
    <h1>Welcome to Web Scraping</h1>
    <p>This is a practice paragraph.</p>
  </body>
</html>
"""
```

**Expected output:**
```
Page title: My Practice Page
```

> **Hints:**
> - `from bs4 import BeautifulSoup`
> - `soup = BeautifulSoup(SAMPLE_HTML, "html.parser")`
> - `soup.find("title")` returns the tag object; add `.text` to get just the string.

> **Difficulty:** ⭐ Beginner

---

**Q3. Find All Links**

Use the HTML string below to find every `<a>` tag, then extract and print each `href` attribute on its own line.

```python
SAMPLE_HTML = """
<html>
  <body>
    <nav>
      <a href="https://python.org">Python</a>
      <a href="https://docs.python.org">Docs</a>
      <a href="https://pypi.org">PyPI</a>
      <a href="#">Home</a>
      <a>No href here</a>
    </nav>
  </body>
</html>
"""
```

**Expected output:**
```
https://python.org
https://docs.python.org
https://pypi.org
#
None
```

> **Hints:**
> - `soup.find_all("a")` returns a list of every `<a>` tag.
> - `tag.get("href")` retrieves the `href` attribute (returns `None` if absent — that is fine for now).

> **Difficulty:** ⭐ Beginner

---

**Q4. Extract Text**

Given the HTML string below, extract and print:
1. The `<h1>` heading text
2. The `<p>` paragraph text
3. Each `<li>` item text, numbered

```python
SAMPLE_HTML = """
<html>
  <body>
    <h1>Python Topics</h1>
    <p>Here are some topics to learn:</p>
    <ul>
      <li>Variables</li>
      <li>Loops</li>
      <li>Functions</li>
      <li>Classes</li>
    </ul>
  </body>
</html>
"""
```

**Expected output:**
```
Heading : Python Topics
Paragraph: Here are some topics to learn:
1. Variables
2. Loops
3. Functions
4. Classes
```

> **Hints:**
> - `soup.find("h1").text` retrieves heading text.
> - `soup.find_all("li")` returns a list; iterate with `enumerate(..., start=1)`.

> **Difficulty:** ⭐ Beginner

---

**Q5. Save to File**

Fetch `https://quotes.toscrape.com/`, find every `<p>` tag with class `"text"`, extract each quote's text, and write them to a file called `quotes.txt` — one quote per line.

After writing, re-open the file, read it back, and print the first 3 lines to confirm it worked.

> **Hints:**
> - `soup.find_all("p", class_="text")` finds the right tags.
> - `tag.get_text()` returns clean text without HTML.
> - Open the file with `open("quotes.txt", "w", encoding="utf-8")`.
> - Use `open("quotes.txt", "r", encoding="utf-8")` to read back.

> **Difficulty:** ⭐ Beginner

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
