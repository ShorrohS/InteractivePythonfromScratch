"""
Debugging Challenge 01 — Phase 10: Web Scraping
================================================

INSTRUCTIONS:
  7 bugs are hidden in this file.
  All relate to web scraping: imports, BeautifulSoup usage, status
  checking, NoneType safety, attribute names, pagination logic, and
  file encoding.
  Find and fix each one.
  When all are fixed, the program runs and writes output.txt correctly.

Run: python challenge-01.py
"""

import time
import requests
# NOTE: missing import lives on the next import line — check it carefully

SAMPLE_HTML = """
<html>
  <head><title>Debug Practice</title></head>
  <body>
    <h1>Web Scraping Bugs</h1>
    <p>Find all the bugs below.</p>
    <ul>
      <li><a href="https://python.org">Python</a></li>
      <li><a href="https://pypi.org">PyPI</a></li>
    </ul>
  </body>
</html>
"""

print("=" * 55)
print("DEBUGGING CHALLENGE 01 - Web Scraping Bugs")
print("=" * 55)


# ============================================================
# BUG 1 — Missing import
# ============================================================
print("\nBug 1 - Parse HTML:")
# BeautifulSoup is used below but the import is missing.
# The line above only imports time and requests.
# Fix: add   from bs4 import BeautifulSoup   at the top of the file.

soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
print(f"  Title: {soup.find('title').text}")


# ============================================================
# BUG 2 — Wrong parser string
# ============================================================
print("\nBug 2 - Wrong parser:")
# The parser name below is incorrect.
bad_soup = BeautifulSoup(SAMPLE_HTML, "html")   # BUG: should be "html.parser"
heading = bad_soup.find("h1")
print(f"  Heading: {heading.text if heading else 'Not found'}")


# ============================================================
# BUG 3 — Status code not checked
# ============================================================
print("\nBug 3 - Status not checked:")

def fetch_and_parse(url):
    response = requests.get(url, timeout=5)
    # BUG: response.text is parsed without checking status_code first.
    # A 404 or 500 response will still have a body, but it won't be the
    # expected page content — parsing it silently produces wrong results.
    page_soup = BeautifulSoup(response.text, "html.parser")
    return page_soup.find("title")

result = fetch_and_parse("https://httpbin.org/status/200")
# (httpbin /status/200 returns an empty body — title will be None, which is fine here)
print(f"  Title tag: {result}")


# ============================================================
# BUG 4 — NoneType error on missing element
# ============================================================
print("\nBug 4 - NoneType safety:")
partial_html = "<html><body><p>No heading here.</p></body></html>"
partial_soup = BeautifulSoup(partial_html, "html.parser")

# BUG: .find("h1") returns None when <h1> is absent.
# Chaining .text on None raises AttributeError: 'NoneType' object has no attribute 'text'
heading_text = partial_soup.find("h1").text   # BUG: no None check
print(f"  Heading: {heading_text}")


# ============================================================
# BUG 5 — Wrong attribute name
# ============================================================
print("\nBug 5 - Wrong attribute:")
link_soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
links = link_soup.find_all("a")

for link in links:
    # BUG: <a> tags carry href, not src.
    # .get("src") will always return None for anchor tags.
    url = link.get("src")   # BUG: should be link.get("href")
    print(f"  URL: {url}")


# ============================================================
# BUG 6 — Infinite pagination loop
# ============================================================
print("\nBug 6 - Pagination loop:")

def scrape_pages(max_pages):
    page = 1
    all_items = []

    while page <= max_pages:
        print(f"  Scraping page {page}...")
        # Simulate scraping: normally you'd fetch a URL here
        all_items.append(f"item-from-page-{page}")

        # BUG: page is never incremented — this loop runs forever.
        # Fix: add   page += 1   here.

    return all_items

# Call with a small limit so you can observe the bug quickly
# items = scrape_pages(3)   ← commented out to avoid hanging; fix the bug first
print("  (Loop body not called — fix the bug to enable it)")


# ============================================================
# BUG 7 — File encoding missing
# ============================================================
print("\nBug 7 - File encoding:")
quotes = [
    "\u201cLife is what happens when you\u2019re busy making other plans.\u201d",
    "\u201cThe world is a book and those who do not travel read only one page.\u201d",
]

# BUG: open() without encoding="utf-8" uses the system default (often cp1252
# on Windows), which cannot encode curly quotes (\u201c / \u2019) and raises
# UnicodeEncodeError at runtime.
with open("output.txt", "w") as f:    # BUG: missing encoding="utf-8"
    for q in quotes:
        f.write(q + "\n")

print("  Wrote output.txt")

print("\n" + "=" * 55)
print("Fixed all 7 bugs? The program should complete without errors.")
print("=" * 55)


# ============================================================
# ANSWER KEY
# ============================================================
#
# Bug 1 — Missing import:
#   Add at the top of the file:
#       from bs4 import BeautifulSoup
#
# Bug 2 — Wrong parser string:
#   Change:  BeautifulSoup(SAMPLE_HTML, "html")
#   To:      BeautifulSoup(SAMPLE_HTML, "html.parser")
#   ("html" is not a valid parser name; use "html.parser", "lxml", or "html5lib")
#
# Bug 3 — Status code not checked:
#   Add a check before parsing:
#       if response.status_code == 200:
#           page_soup = BeautifulSoup(response.text, "html.parser")
#           ...
#   Return None (or raise) for non-200 responses.
#
# Bug 4 — NoneType error:
#   Guard with a None check before accessing .text:
#       h1_tag = partial_soup.find("h1")
#       heading_text = h1_tag.text if h1_tag else "No heading found"
#
# Bug 5 — Wrong attribute:
#   Change:  link.get("src")
#   To:      link.get("href")
#   (<a> elements carry href; <img> and <script> carry src)
#
# Bug 6 — Infinite pagination loop:
#   Add inside the while loop, after the scraping logic:
#       page += 1
#   Without this increment, page stays 1 forever.
#
# Bug 7 — File encoding:
#   Change:  open("output.txt", "w")
#   To:      open("output.txt", "w", encoding="utf-8")
#   Always specify encoding="utf-8" when writing text that may contain
#   non-ASCII characters (curly quotes, accents, emoji, etc.).
