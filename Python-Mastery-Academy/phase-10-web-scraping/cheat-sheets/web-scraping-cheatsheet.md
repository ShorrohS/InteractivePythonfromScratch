# ⚡ Phase 10 Cheat Sheet — Web Scraping

---

## Setup

```bash
pip install requests beautifulsoup4 lxml
```

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://example.com", timeout=10)
soup = BeautifulSoup(response.text, "html.parser")
```

---

## HTTP Request

```python
# GET with headers and params
response = requests.get(
    url,
    headers={"User-Agent": "MyBot/1.0"},
    params={"q": "python", "page": 1},
    timeout=10
)

# Check status
if response.status_code == 200:
    html = response.text
elif response.status_code == 404:
    print("Page not found")
```

---

## Finding Elements

```python
# First match
soup.find("h1")
soup.find("div", id="main")
soup.find("p", class_="intro")

# All matches
soup.find_all("a")
soup.find_all("li", class_="item")

# CSS selectors
soup.select("div.card")          # div with class card
soup.select("#results a")        # links inside #results
soup.select_one("h1")            # first h1
```

---

## Extracting Data

```python
tag.text              # all text content
tag.string            # text (if no nested tags)
tag.get_text(strip=True)  # stripped text

tag["href"]           # attribute value
tag.get("href", "")   # safe with default
tag.attrs             # dict of all attributes
```

---

## Common Patterns

```python
# All links on page
links = [a.get("href") for a in soup.find_all("a", href=True)]

# All images
images = [img.get("src") for img in soup.find_all("img", src=True)]

# Table to list of dicts
table = soup.find("table")
headers = [th.text.strip() for th in table.find_all("th")]
rows = [
    dict(zip(headers, [td.text.strip() for td in tr.find_all("td")]))
    for tr in table.find_all("tr")[1:]
]

# Text cleaning
import re
clean = re.sub(r'\s+', ' ', tag.text).strip()
price = float(tag.text.replace("$","").replace(",",""))
```

---

## Ethics

```python
import time, random

# 1. Check robots.txt
# 2. Add delays
time.sleep(random.uniform(1, 3))

# 3. Set User-Agent
headers = {"User-Agent": "StudentBot/1.0"}

# 4. Use APIs when available
# 5. Don't scrape personal data
# 6. Respect rate limits
```
