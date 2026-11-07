"""
Project 01 - Journal App
Phase 05: File Handling

SKILLS PRACTICED:
  - Writing and reading text files (append mode)
  - Date and time formatting
  - File existence checks with os
  - Line-by-line reading and parsing

HOW TO RUN:
  python main.py
"""

import os
from datetime import datetime
from pathlib import Path

JOURNAL_FILE = "my_journal.txt"
SEPARATOR = "=" * 50


def get_timestamp() -> str:
    return datetime.now().strftime("%A, %B %d %Y — %H:%M")


def write_entry(entry_text: str) -> None:
    """Append a new journal entry to the file."""
    timestamp = get_timestamp()
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n[{timestamp}]\n")
        f.write(entry_text.strip())
        f.write(f"\n{'-'*50}\n")
    print("  Entry saved.")


def read_all_entries() -> str:
    """Read and return all journal entries."""
    if not os.path.exists(JOURNAL_FILE):
        return "  No entries yet."
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        return f.read()


def count_entries() -> int:
    """Count total journal entries."""
    if not os.path.exists(JOURNAL_FILE):
        return 0
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        return sum(1 for line in f if line.startswith("["))


def search_entries(keyword: str) -> list:
    """Find all entries containing the keyword."""
    if not os.path.exists(JOURNAL_FILE):
        return []
    results = []
    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by separator dashes
    entries = content.split("-" * 50)
    for entry in entries:
        entry = entry.strip()
        if keyword.lower() in entry.lower() and entry:
            results.append(entry)
    return results


def show_last_n(n: int = 5) -> None:
    """Show the last N entries."""
    if not os.path.exists(JOURNAL_FILE):
        print("  No entries yet.")
        return

    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    entries = [e.strip() for e in content.split("-" * 50) if e.strip()]
    last_entries = entries[-n:]

    print(f"\n  LAST {len(last_entries)} ENTRIES")
    print(SEPARATOR)
    for entry in last_entries:
        print(entry)
        print("-" * 50)


def get_journal_stats() -> dict:
    """Get journal statistics."""
    if not os.path.exists(JOURNAL_FILE):
        return {"entries": 0, "words": 0, "size_kb": 0}

    with open(JOURNAL_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    size = os.path.getsize(JOURNAL_FILE)
    words = len(content.split())
    entries = content.count("[") - content.count("[[")    # count timestamp lines

    return {
        "entries":  entries,
        "words":    words,
        "size_kb":  round(size / 1024, 2),
        "file":     JOURNAL_FILE
    }


def main():
    print(SEPARATOR)
    print("  MY PERSONAL JOURNAL")
    print(SEPARATOR)

    while True:
        stats = get_journal_stats()
        print(f"\n  Entries: {stats['entries']} | Words: {stats['words']}")
        print()
        print("  [1] Write New Entry")
        print("  [2] Read All Entries")
        print("  [3] View Last 5 Entries")
        print("  [4] Search Entries")
        print("  [5] Journal Stats")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            print("\n  Write your entry (type END on a new line to finish):")
            lines = []
            while True:
                line = input("  > ")
                if line.strip().upper() == "END":
                    break
                lines.append(line)
            if lines:
                write_entry("\n".join(lines))
            else:
                print("  Empty entry — not saved.")

        elif choice == "2":
            print("\n  ALL JOURNAL ENTRIES")
            print(SEPARATOR)
            print(read_all_entries())

        elif choice == "3":
            show_last_n(5)

        elif choice == "4":
            keyword = input("  Search for: ").strip()
            results = search_entries(keyword)
            if results:
                print(f"\n  Found {len(results)} matching entries:")
                for r in results:
                    print(r[:200] + "..." if len(r) > 200 else r)
                    print("-" * 50)
            else:
                print(f"  No entries found containing '{keyword}'.")

        elif choice == "5":
            stats = get_journal_stats()
            print(f"\n  JOURNAL STATISTICS")
            print(f"  File:      {stats['file']}")
            print(f"  Entries:   {stats['entries']}")
            print(f"  Words:     {stats['words']:,}")
            print(f"  Size:      {stats['size_kb']} KB")

        elif choice == "0":
            print("\n  Goodbye! Keep writing.")
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
