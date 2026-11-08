# Lesson 02 — Requests and BeautifulSoup Basics

**Phase:** 10 — Web Scraping | **Time:** ~30 min

---

## Part 1: Installing the Libraries

```bash
pip install requests beautifulsoup4 lxml
```

- **requests** — sends HTTP requests and receives responses
- **beautifulsoup4** — parses HTML and lets you search the document tree
- **lxml** — a faster HTML parser (optional but recommended)

---

## Part 2: Making an HTTP GET Request

```python
import requests

response = requests.get("https://example.com")
print(response.status_code)  # 200

# Always set a timeout; pass query parameters as a dict
params = {"q": "python", "page": 1}
response = requests.get(
    "https://example.com/search",
    params=params,
    timeout=10
)
print(response.url)   # https://example.com/search?q=python&page=1
```

---

## Part 3: The Response Object

```python
import requests

response = requests.get("https://httpbin.org/get", timeout=10)

print(response.status_code)              # 200, 404, 500 …
print(response.ok)                       # True when status code < 400
print(response.text)                     # Body decoded as a string
print(response.content)                  # Body as raw bytes
print(response.encoding)                 # e.g. "utf-8"
print(response.url)                      # Final URL after any redirects
print(response.headers.get("Content-Type"))  # "text/html; charset=utf-8"
```

---

## Part 4: Error Handling with raise_for_status()

Call `raise_for_status()` immediately after the request. It raises `HTTPError` for
any 4xx or 5xx response, so you never silently parse an error page as real data.

```python
import requests

try:
    response = requests.get("https://example.com/missing", timeout=10)
    response.raise_for_status()           # Raises HTTPError for 4xx/5xx
    print("Success:", response.status_code)

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")             # 404, 403, 500 …

except requests.exceptions.ConnectionError:
    print("Could not connect to server")  # DNS failure, network down

except requests.exceptions.Timeout:
    print("Request timed out")

except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")         # Catch-all base class
```

---

## Part 5: Sending Headers — User-Agent

Many sites block requests that look automated. Set a `User-Agent` to identify your
client; the default `"python-requests/2.x"` is blocked by some servers.

```python
import requests

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

response = requests.get("https://example.com", headers=headers, timeout=10)

# For educational projects a transparent name is fine
headers = {"User-Agent": "StudentScraper/1.0 (Python learning project)"}
```

---

## Part 6: Creating a BeautifulSoup Object

Pass `response.text` and a parser name to the `BeautifulSoup` constructor.
Omitting the parser triggers a warning — always name one explicitly.

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com", timeout=10)
response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")  # built-in, good default
# soup = BeautifulSoup(response.text, "lxml")        # faster; pip install lxml
# soup = BeautifulSoup(response.text, "html5lib")    # browser-accurate, slowest

# Parse a raw string directly — handy for testing
html = "<html><body><h1>Hello</h1></body></html>"
soup = BeautifulSoup(html, "html.parser")
```

---

## Part 7: Basic Soup Navigation

```python
from bs4 import BeautifulSoup

html = """
<html>
  <head><title>Python Weekly</title></head>
  <body>
    <h1 id="headline">Top Articles</h1>
    <p class="intro">Welcome to this week's digest.</p>
    <p>Don't miss the async Python tutorial.</p>
  </body>
</html>
"""
soup = BeautifulSoup(html, "html.parser")

print(soup.head)             # the entire <head> block
print(soup.body)             # the entire <body> block
print(soup.title)            # <title>Python Weekly</title>
print(soup.title.string)     # Python Weekly

print(soup.h1.text)          # Top Articles
print(soup.p.text)           # Welcome to this week's digest.  (first <p> only)

# find() — first match, returns None if not found
intro = soup.find("p", class_="intro")
print(intro.text)            # Welcome to this week's digest.

# find_all() — all matches as a list
for p in soup.find_all("p"):
    print(p.text)
```

> Lesson 03 covers `find()`, `find_all()`, CSS selectors, and attribute extraction
> in full detail.

---

## Part 8: Inspecting HTML with prettify()

`prettify()` formats the parsed HTML with indentation — useful for understanding
the document structure while building a scraper.

```python
from bs4 import BeautifulSoup

html = "<html><body><div class='card'><h2>Title</h2><p>Body.</p></div></body></html>"
soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())
# <html>
#  <body>
#   <div class="card">
#    <h2>Title</h2><p>Body.</p>
#   </div>
#  </body>
# </html>

# Prettify a single tag
card = soup.find("div", class_="card")
print(card.prettify())
```

---

## Part 9: Complete Example — Fetch and Parse a Wikipedia Article

```python
import requests
from bs4 import BeautifulSoup


def scrape_wikipedia(url: str) -> dict:
    """Return the article title and first paragraph from a Wikipedia URL."""
    headers = {"User-Agent": "WikiScraper/1.0 (Python learning project)"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch page: {e}")
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    # Article title is in <h1 id="firstHeading">
    h1 = soup.find("h1", id="firstHeading")
    title = h1.get_text(strip=True) if h1 else "Unknown"

    # First content paragraph lives inside div.mw-parser-output
    first_para = ""
    content = soup.find("div", class_="mw-parser-output")
    if content:
        for p in content.find_all("p", recursive=False):
            text = p.get_text(strip=True)
            if text:
                first_para = text
                break

    return {"title": title, "first_paragraph": first_para, "url": response.url}


result = scrape_wikipedia(
    "https://en.wikipedia.org/wiki/Python_(programming_language)"
)
if result:
    print(f"Title: {result['title']}")
    print(f"\nFirst paragraph:\n{result['first_paragraph'][:300]}...")
```

---

## Practice Exercises

1. Fetch `https://example.com`. Print its status code, `Content-Type` header, and
   page title using BeautifulSoup.

2. Fetch `https://httpbin.org/status/404` and handle the `HTTPError` raised by
   `raise_for_status()`. Print the status code from the exception.

3. Modify the Wikipedia example to also count and print the number of `<h2>` tags
   found in the article body.

4. Write a function `safe_fetch(url, retries=3)` that retries on `ConnectionError`
   or `Timeout` and returns a `BeautifulSoup` object, or `None` after all retries.

---

## Next Lesson

**[Lesson 03 → Parsing HTML with BeautifulSoup](lesson-03-beautifulsoup.md)**
