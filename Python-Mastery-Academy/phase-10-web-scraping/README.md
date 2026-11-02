# 🌐 Phase 10 — Web Scraping

> **Goal:** Extract data from websites automatically.

---

## What is Web Scraping?

Web scraping is writing code that automatically visits websites and extracts the data you need.

**Use cases:** Price monitoring, job listings, news aggregation, research data, competitive analysis.

---

## Core Libraries

```python
# Install
pip install requests beautifulsoup4 lxml

# Basic pattern
import requests
from bs4 import BeautifulSoup

url = "https://example.com/products"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find elements
title = soup.find("h1").text
prices = soup.find_all("span", class_="price")
table = soup.find("table", id="data")

# Extract from table
rows = table.find_all("tr")
for row in rows:
    cells = row.find_all("td")
    data = [cell.text.strip() for cell in cells]
```

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-html-basics.md](concepts/lesson-01-html-basics.md) | HTML structure basics |
| 02 | [lesson-02-requests.md](concepts/lesson-02-requests.md) | requests for web pages |
| 03 | [lesson-03-beautifulsoup.md](concepts/lesson-03-beautifulsoup.md) | Parsing HTML with BS4 |
| 04 | [lesson-04-data-extraction.md](concepts/lesson-04-data-extraction.md) | Extracting and cleaning data |

---

## Ethics & Legality

```
BEFORE SCRAPING:
  1. Check robots.txt (e.g., https://example.com/robots.txt)
  2. Check the website's Terms of Service
  3. Don't overload the server (add delays)
  4. Use official APIs when available

BEST PRACTICES:
  - Add time.sleep(1) between requests
  - Set a User-Agent header
  - Cache results to avoid repeated requests
  - Never scrape personal/private data
```

---

## Projects

| Project | Description |
|---------|-------------|
| [News Scraper](guided-projects/project-01-news-scraper/) | Extract news headlines |

---

## ✅ Completion Checklist

- [ ] Understand HTML structure (tags, classes, IDs)
- [ ] Can make requests and parse HTML with BeautifulSoup
- [ ] Can extract text, links, tables
- [ ] Follow ethical scraping practices

---

## Previous: [Phase 09](../phase-09-databases/README.md) | Next: [Phase 11](../phase-11-apis/README.md)
