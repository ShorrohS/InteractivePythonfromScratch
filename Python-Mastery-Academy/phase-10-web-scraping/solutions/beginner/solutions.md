# Phase 10 — Beginner Solutions: Web Scraping

---

## Q1. First Request

```python
import requests

url = "https://httpbin.org/get"

response = requests.get(url)           # send the GET request

print(f"Status code: {response.status_code}")
print("First 200 chars:")
print(response.text[:200])             # slice the response body
```

**Explanation:** `requests.get()` returns a `Response` object. `status_code` is the integer HTTP status (200 = OK). `response.text` is the full body decoded as a string.

---

## Q2. Parse HTML

```python
from bs4 import BeautifulSoup

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

# "html.parser" is Python's built-in parser — no extra install needed
soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

title_tag = soup.find("title")         # returns the first <title> element
print(f"Page title: {title_tag.text}") # .text strips the HTML tags
```

**Explanation:** `BeautifulSoup()` takes the HTML string and a parser name. `"html.parser"` is the built-in choice; `"lxml"` is faster but requires a separate install. `soup.find("tag")` returns the **first** match as a Tag object; `.text` extracts just the string content.

---

## Q3. Find All Links

```python
from bs4 import BeautifulSoup

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

soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

links = soup.find_all("a")             # returns a list of ALL <a> tags

for link in links:
    href = link.get("href")            # .get() returns None if attr is absent
    print(href)
```

**Explanation:** `find_all("a")` returns every `<a>` element in document order. `.get("attr")` is safer than `link["attr"]` because it returns `None` instead of raising a `KeyError` when the attribute is missing.

---

## Q4. Extract Text

```python
from bs4 import BeautifulSoup

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

soup = BeautifulSoup(SAMPLE_HTML, "html.parser")

# Extract heading and paragraph
heading = soup.find("h1").text
paragraph = soup.find("p").text

print(f"Heading  : {heading}")
print(f"Paragraph: {paragraph}")

# Extract list items with numbering
items = soup.find_all("li")
for i, item in enumerate(items, start=1):
    print(f"{i}. {item.text}")
```

**Explanation:** `find("h1")` finds the first `<h1>`; chaining `.text` returns its string content. `find_all("li")` returns all list items. `enumerate(..., start=1)` provides a 1-based counter without a manual variable.

---

## Q5. Save to File

```python
import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"

# Fetch the page
response = requests.get(url)

# Parse only if the request succeeded
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Select all <p> tags with class="text"
    quote_tags = soup.find_all("p", class_="text")
    quotes = [tag.get_text() for tag in quote_tags]

    # Write to file — always specify encoding to avoid surprises
    with open("quotes.txt", "w", encoding="utf-8") as f:
        for quote in quotes:
            f.write(quote + "\n")

    print(f"Wrote {len(quotes)} quotes to quotes.txt")

    # Read back and confirm
    print("\nFirst 3 lines:")
    with open("quotes.txt", "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            print(f"  {i}: {line.rstrip()}")
            if i == 3:
                break
else:
    print(f"Request failed with status {response.status_code}")
```

**Explanation:** Always check `status_code` before parsing — a failed request still returns a `Response` object, just with error HTML. `get_text()` is equivalent to `.text` but slightly more flexible (you can pass `separator` and `strip` arguments). `encoding="utf-8"` is essential for pages containing curly quotes or accented characters.
