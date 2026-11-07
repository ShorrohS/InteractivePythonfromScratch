"""
Project 01 - Library Management System
Phase 07: OOP

SKILLS PRACTICED:
  - Classes with __init__, properties, dunder methods
  - Inheritance (Book types)
  - Encapsulation (private attributes)
  - Composition (Library contains Books and Members)

HOW TO RUN:
  python main.py
"""

from datetime import datetime, date
from typing import Optional


# ============================================================
# BOOK CLASSES
# ============================================================

class Book:
    """Represents a library book."""

    def __init__(self, isbn: str, title: str, author: str, year: int, copies: int = 1):
        self._isbn    = isbn
        self.title    = title
        self.author   = author
        self.year     = year
        self._total   = copies
        self._available = copies

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def available(self) -> int:
        return self._available

    @property
    def total_copies(self) -> int:
        return self._total

    @property
    def is_available(self) -> bool:
        return self._available > 0

    def checkout(self) -> bool:
        if self._available > 0:
            self._available -= 1
            return True
        return False

    def return_book(self) -> None:
        if self._available < self._total:
            self._available += 1

    def __str__(self) -> str:
        status = f"{self._available}/{self._total} available"
        return f"[{self._isbn}] {self.title!r} by {self.author} ({self.year}) — {status}"

    def __repr__(self) -> str:
        return f"Book(isbn={self._isbn!r}, title={self.title!r})"

    def __eq__(self, other) -> bool:
        return isinstance(other, Book) and self._isbn == other._isbn


class EBook(Book):
    """Digital book — unlimited simultaneous access."""

    def __init__(self, isbn, title, author, year, format_: str = "PDF"):
        super().__init__(isbn, title, author, year, copies=999)
        self.format = format_

    @property
    def is_available(self) -> bool:
        return True    # always available

    def checkout(self) -> bool:
        return True    # never reduces

    def __str__(self) -> str:
        return f"[{self.isbn}] {self.title!r} [eBook/{self.format}] by {self.author}"


class AudioBook(Book):
    """Audio version with duration."""

    def __init__(self, isbn, title, author, year, duration_hours: float):
        super().__init__(isbn, title, author, year, copies=1)
        self.duration = duration_hours

    def __str__(self) -> str:
        return (f"[{self.isbn}] {self.title!r} [Audio: {self.duration}h] "
                f"by {self.author} — {'Available' if self.is_available else 'Checked out'}")


# ============================================================
# MEMBER CLASS
# ============================================================

class Member:
    """Library member with borrowing history."""

    MAX_LOANS = 5

    def __init__(self, member_id: str, name: str, email: str):
        self._member_id = member_id
        self.name       = name
        self.email      = email
        self._active    = True
        self._loans: list[dict] = []
        self._history:  list[dict] = []

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def active_loans(self) -> list:
        return [l for l in self._loans if not l.get("returned")]

    @property
    def can_borrow(self) -> bool:
        return self._active and len(self.active_loans) < self.MAX_LOANS

    def borrow(self, book: Book) -> bool:
        if not self.can_borrow:
            return False
        if not book.checkout():
            return False
        self._loans.append({
            "isbn":      book.isbn,
            "title":     book.title,
            "borrowed":  date.today().isoformat(),
            "returned":  None
        })
        return True

    def return_book(self, isbn: str) -> bool:
        for loan in self.active_loans:
            if loan["isbn"] == isbn:
                loan["returned"] = date.today().isoformat()
                self._history.append(loan)
                return True
        return False

    def __str__(self) -> str:
        return f"Member({self._member_id}): {self.name} — {len(self.active_loans)} loans"


# ============================================================
# LIBRARY CLASS (Composition)
# ============================================================

class Library:
    """Manages books and members. Demonstrates composition."""

    def __init__(self, name: str):
        self.name     = name
        self._books:   dict[str, Book] = {}
        self._members: dict[str, Member] = {}

    # ── Book management ─────────────────────────────────
    def add_book(self, book: Book) -> None:
        self._books[book.isbn] = book
        print(f"  Added: {book.title}")

    def find_book(self, query: str) -> list[Book]:
        q = query.lower()
        return [
            b for b in self._books.values()
            if q in b.title.lower()
            or q in b.author.lower()
            or q in b.isbn.lower()
        ]

    # ── Member management ────────────────────────────────
    def register_member(self, member: Member) -> None:
        self._members[member.member_id] = member
        print(f"  Registered: {member.name} ({member.member_id})")

    # ── Borrowing ────────────────────────────────────────
    def checkout(self, member_id: str, isbn: str) -> bool:
        member = self._members.get(member_id)
        book   = self._books.get(isbn)

        if not member:
            print(f"  Member {member_id} not found.")
            return False
        if not book:
            print(f"  Book {isbn} not found.")
            return False
        if not book.is_available:
            print(f"  '{book.title}' is not available.")
            return False
        if not member.can_borrow:
            print(f"  {member.name} has reached their borrowing limit.")
            return False

        if member.borrow(book):
            print(f"  Checked out: '{book.title}' to {member.name}")
            return True
        return False

    def return_book(self, member_id: str, isbn: str) -> bool:
        member = self._members.get(member_id)
        book   = self._books.get(isbn)

        if not member or not book:
            return False

        if member.return_book(isbn):
            book.return_book()
            print(f"  Returned: '{book.title}' from {member.name}")
            return True
        return False

    # ── Reports ──────────────────────────────────────────
    def catalogue(self) -> None:
        print(f"\n  {self.name.upper()} — CATALOGUE ({len(self._books)} books)")
        print("  " + "-" * 70)
        for book in sorted(self._books.values(), key=lambda b: b.title):
            print(f"  {book}")

    def available_books(self) -> list[Book]:
        return [b for b in self._books.values() if b.is_available]

    def __repr__(self) -> str:
        return f"Library({self.name!r}, {len(self._books)} books, {len(self._members)} members)"


# ============================================================
# MAIN
# ============================================================

def main():
    lib = Library("Python City Public Library")

    # Add books
    lib.add_book(Book("978-0001", "Python Cookbook",    "David Beazley", 2023, 3))
    lib.add_book(Book("978-0002", "Clean Code",          "Robert Martin", 2008, 2))
    lib.add_book(Book("978-0003", "Design Patterns",     "Gang of Four",  1994, 1))
    lib.add_book(EBook("978-0004", "FastAPI in Practice","Bill Lubanovic", 2023))
    lib.add_book(AudioBook("978-0005", "The Pragmatic Programmer", "Hunt & Thomas", 2019, 6.5))

    # Register members
    alice = Member("M001", "Alice Johnson", "alice@example.com")
    bob   = Member("M002", "Bob Smith",     "bob@example.com")
    lib.register_member(alice)
    lib.register_member(bob)

    # Demonstrate borrowing
    print("\n--- Checkouts ---")
    lib.checkout("M001", "978-0001")
    lib.checkout("M001", "978-0002")
    lib.checkout("M002", "978-0001")   # 2nd copy
    lib.checkout("M002", "978-0003")

    # Show catalogue
    lib.catalogue()

    # Return
    print("\n--- Returns ---")
    lib.return_book("M001", "978-0001")

    # Search
    print("\n--- Search: 'python' ---")
    results = lib.find_book("python")
    for book in results:
        print(f"  {book}")

    print(f"\n{lib}")


if __name__ == "__main__":
    main()
