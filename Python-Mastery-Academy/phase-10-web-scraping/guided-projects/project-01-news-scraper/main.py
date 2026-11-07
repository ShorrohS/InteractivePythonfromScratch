"""
Project 01 - News Headlines Scraper
Phase 10: Web Scraping

SKILLS PRACTICED:
  - requests library for HTTP
  - BeautifulSoup for HTML parsing
  - Extracting text and attributes
  - Saving results to CSV
  - Error handling for network requests

NOTE: Uses https://news.ycombinator.com (Hacker News) — public, scraping-friendly.

SETUP:
  pip install requests beautifulsoup4

HOW TO RUN:
  python main.py
"""

import csv
import os
from datetime import datetime

try:
    import requests
    from bs4 import BeautifulSoup
    LIBRARIES_AVAILABLE = True
except ImportError:
    LIBRARIES_AVAILABLE = False


def fetch_hackernews(pages: int = 1) -> list[dict]:
    """Scrape top stories from Hacker News."""
    stories = []
    headers = {"User-Agent": "PythonMasteryAcademy/1.0 (learning project)"}

    for page in range(1, pages + 1):
        url = f"https://news.ycombinator.com/news?p={page}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"  Failed page {page}: HTTP {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            # Hacker News structure: each story is in a <tr class="athing">
            items = soup.find_all("tr", class_="athing")
            for item in items:
                # Title link
                title_cell = item.find("span", class_="titleline")
                if not title_cell:
                    continue
                link_tag = title_cell.find("a")
                if not link_tag:
                    continue

                title = link_tag.text.strip()
                url   = link_tag.get("href", "")

                # Score and metadata from next row
                next_row = item.find_next_sibling("tr")
                score_tag = next_row.find("span", class_="score") if next_row else None
                score = score_tag.text.strip() if score_tag else "0 points"

                stories.append({
                    "rank":  len(stories) + 1,
                    "title": title,
                    "url":   url,
                    "score": score,
                    "page":  page,
                    "scraped": datetime.now().strftime("%Y-%m-%d %H:%M")
                })

        except requests.exceptions.ConnectionError:
            print("  Connection error. Check your internet connection.")
            break
        except requests.exceptions.Timeout:
            print(f"  Timeout on page {page}.")

    return stories


def demo_without_internet() -> list[dict]:
    """Return sample data when no internet or libraries available."""
    return [
        {"rank": 1, "title": "Python 3.13 Released with Major Performance Improvements",
         "url": "https://python.org", "score": "423 points", "page": 1,
         "scraped": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"rank": 2, "title": "SQLite's approach to database design",
         "url": "https://sqlite.org", "score": "312 points", "page": 1,
         "scraped": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"rank": 3, "title": "FastAPI vs Flask: When to use which",
         "url": "https://fastapi.tiangolo.com", "score": "287 points", "page": 1,
         "scraped": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"rank": 4, "title": "The Power of Python Type Hints",
         "url": "https://mypy.readthedocs.io", "score": "201 points", "page": 1,
         "scraped": datetime.now().strftime("%Y-%m-%d %H:%M")},
        {"rank": 5, "title": "Building REST APIs with Python Best Practices",
         "url": "https://realpython.com", "score": "178 points", "page": 1,
         "scraped": datetime.now().strftime("%Y-%m-%d %H:%M")},
    ]


def save_to_csv(stories: list[dict], filename: str = None) -> str:
    """Save scraped stories to CSV."""
    filename = filename or f"news_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "title", "url", "score", "scraped"])
        writer.writeheader()
        writer.writerows(stories)
    return filename


def display_stories(stories: list[dict], limit: int = 10) -> None:
    """Display stories in a formatted table."""
    print(f"\n  {'#':<4} {'Score':<12} {'Title'}")
    print("  " + "-" * 80)
    for s in stories[:limit]:
        title = s["title"][:60] + "..." if len(s["title"]) > 60 else s["title"]
        print(f"  {s['rank']:<4} {s['score']:<12} {title}")


def main():
    print("=" * 60)
    print("  NEWS SCRAPER")
    print("=" * 60)

    if not LIBRARIES_AVAILABLE:
        print("\n  Libraries not installed.")
        print("  Run: pip install requests beautifulsoup4")
        print("\n  Showing demo data instead:")
        stories = demo_without_internet()
    else:
        print("\n  Scraping Hacker News top stories...")
        stories = fetch_hackernews(pages=1)

        if not stories:
            print("  Could not connect. Using demo data.")
            stories = demo_without_internet()

    print(f"\n  Fetched {len(stories)} stories.")
    display_stories(stories)

    save = input("\n  Save to CSV? (yes/no): ").strip().lower()
    if save in ("yes", "y"):
        filename = save_to_csv(stories)
        print(f"  Saved: {filename}")

    # Filter example
    keyword = input("\n  Filter by keyword (or blank to skip): ").strip().lower()
    if keyword:
        filtered = [s for s in stories if keyword in s["title"].lower()]
        print(f"\n  {len(filtered)} stories containing '{keyword}':")
        display_stories(filtered)


if __name__ == "__main__":
    main()
