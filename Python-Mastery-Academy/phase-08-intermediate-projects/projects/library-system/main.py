"""
Library System (CLI Version)
Phase 08: Intermediate Projects

SKILLS USED: OOP, JSON persistence, search, borrowing logic, date tracking

HOW TO RUN: python main.py
"""

import json
import os
from datetime import datetime, date, timedelta


class Book:
    LOAN_DAYS = 14

    def __init__(self, isbn: str, title: str, author: str,
                 year: int, copies: int = 1):
        self.isbn      = isbn
        self.title     = title
        self.author    = author
        self.year      = year
        self.total     = copies
        self.available = copies

    @property
    def is_available(self) -> bool:
        return self.available > 0

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Book":
        b = cls.__new__(cls)
        b.__dict__.update(d)
        return b

    def __str__(self) -> str:
        status = f"{self.available}/{self.total}"
        return f"[{self.isbn}] {self.title} by {self.author} ({self.year}) — {status} avail"


class Loan:
    def __init__(self, member_id: str, isbn: str):
        self.id         = None
        self.member_id  = member_id
        self.isbn       = isbn
        self.borrowed   = date.today().isoformat()
        self.due        = (date.today() + timedelta(days=Book.LOAN_DAYS)).isoformat()
        self.returned   = None

    @property
    def is_overdue(self) -> bool:
        return not self.returned and date.fromisoformat(self.due) < date.today()

    @property
    def days_overdue(self) -> int:
        if not self.is_overdue: return 0
        return (date.today() - date.fromisoformat(self.due)).days

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Loan":
        loan = cls.__new__(cls)
        loan.__dict__.update(d)
        return loan


class Member:
    MAX_LOANS = 5

    def __init__(self, mid: str, name: str, email: str):
        self.id    = mid
        self.name  = name
        self.email = email
        self.joined = date.today().isoformat()

    def to_dict(self) -> dict:
        return self.__dict__.copy()

    @classmethod
    def from_dict(cls, d: dict) -> "Member":
        m = cls.__new__(cls)
        m.__dict__.update(d)
        return m

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.email})"


class LibrarySystem:
    FILE = "library_data.json"

    def __init__(self):
        self._books:   dict[str, Book]   = {}
        self._members: dict[str, Member] = {}
        self._loans:   list[Loan]        = []
        self._next_loan_id = 1
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.FILE): return
        with open(self.FILE) as f:
            data = json.load(f)
            self._books   = {k: Book.from_dict(v)   for k,v in data.get("books",   {}).items()}
            self._members = {k: Member.from_dict(v) for k,v in data.get("members", {}).items()}
            self._loans   = [Loan.from_dict(l)       for l    in data.get("loans",   [])]
            self._next_loan_id = data.get("next_loan_id", len(self._loans) + 1)

    def _save(self) -> None:
        with open(self.FILE, "w") as f:
            json.dump({
                "books":         {k: v.to_dict() for k,v in self._books.items()},
                "members":       {k: v.to_dict() for k,v in self._members.items()},
                "loans":         [l.to_dict()    for l    in self._loans],
                "next_loan_id":  self._next_loan_id
            }, f, indent=2)

    def add_book(self, isbn, title, author, year, copies=1) -> None:
        self._books[isbn] = Book(isbn, title, author, year, copies)
        self._save()

    def register_member(self, mid, name, email) -> None:
        self._members[mid] = Member(mid, name, email)
        self._save()

    def checkout(self, member_id: str, isbn: str) -> str:
        if isbn not in self._books:         return "Book not found."
        if member_id not in self._members:  return "Member not found."
        book   = self._books[isbn]
        active = [l for l in self._loans if l.member_id == member_id and not l.returned]
        if len(active) >= Member.MAX_LOANS: return f"Loan limit ({Member.MAX_LOANS}) reached."
        if not book.is_available:           return f"'{book.title}' not available."
        book.available -= 1
        loan = Loan(member_id, isbn)
        loan.id = self._next_loan_id
        self._next_loan_id += 1
        self._loans.append(loan)
        self._save()
        return f"Checked out '{book.title}'. Due: {loan.due}"

    def return_book(self, member_id: str, isbn: str) -> str:
        loan = next((l for l in self._loans
                     if l.member_id == member_id and l.isbn == isbn and not l.returned), None)
        if not loan: return "No active loan found."
        loan.returned = date.today().isoformat()
        self._books[isbn].available += 1
        fine = loan.days_overdue * 0.50
        self._save()
        msg = f"'{self._books[isbn].title}' returned."
        if fine > 0: msg += f" Overdue fine: ${fine:.2f}"
        return msg

    def search_books(self, query: str) -> list[Book]:
        q = query.lower()
        return [b for b in self._books.values()
                if q in b.title.lower() or q in b.author.lower() or q in b.isbn]

    def member_loans(self, member_id: str) -> list[Loan]:
        return [l for l in self._loans if l.member_id == member_id and not l.returned]

    def overdue_loans(self) -> list[Loan]:
        return [l for l in self._loans if l.is_overdue]


def main():
    lib = LibrarySystem()

    if not lib._books:
        for isbn, title, author, year, copies in [
            ("978-001","Clean Code","Robert Martin",2008,2),
            ("978-002","Python Cookbook","David Beazley",2023,3),
            ("978-003","Design Patterns","Gang of Four",1994,1),
            ("978-004","The Pragmatic Programmer","Hunt & Thomas",2019,2),
        ]:
            lib.add_book(isbn, title, author, year, copies)

    if not lib._members:
        for mid, name, email in [
            ("M001","Alice Johnson","alice@example.com"),
            ("M002","Bob Smith","bob@example.com"),
        ]:
            lib.register_member(mid, name, email)

    print("=" * 60)
    print("  LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)

    while True:
        print(f"\n  Books: {len(lib._books)}  |  Members: {len(lib._members)}  |  "
              f"Active Loans: {sum(1 for l in lib._loans if not l.returned)}")
        print("\n  [1] Search Books     [2] Checkout Book")
        print("  [3] Return Book      [4] Member Loans")
        print("  [5] Overdue Report   [6] All Books")
        print("  [7] Add Book         [8] Register Member")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            q = input("  Search (title/author/ISBN): ").strip()
            for book in lib.search_books(q):
                print(f"  {book}")

        elif choice == "2":
            mid  = input("  Member ID: ").strip().upper()
            isbn = input("  Book ISBN: ").strip()
            print(f"  {lib.checkout(mid, isbn)}")

        elif choice == "3":
            mid  = input("  Member ID: ").strip().upper()
            isbn = input("  Book ISBN: ").strip()
            print(f"  {lib.return_book(mid, isbn)}")

        elif choice == "4":
            mid   = input("  Member ID: ").strip().upper()
            loans = lib.member_loans(mid)
            if not loans:
                print("  No active loans.")
            else:
                for l in loans:
                    book = lib._books.get(l.isbn)
                    title = book.title if book else l.isbn
                    flag  = " [OVERDUE]" if l.is_overdue else ""
                    print(f"  {title}  —  Due: {l.due}{flag}")

        elif choice == "5":
            overdue = lib.overdue_loans()
            if not overdue:
                print("  No overdue loans.")
            else:
                print(f"\n  {len(overdue)} overdue loan(s):")
                for l in overdue:
                    book   = lib._books.get(l.isbn)
                    member = lib._members.get(l.member_id)
                    fine   = l.days_overdue * 0.50
                    print(f"  {member.name if member else l.member_id} — "
                          f"{book.title if book else l.isbn} — "
                          f"{l.days_overdue} days overdue — Fine: ${fine:.2f}")

        elif choice == "6":
            for book in sorted(lib._books.values(), key=lambda b: b.title):
                print(f"  {book}")

        elif choice == "7":
            isbn   = input("  ISBN: ").strip()
            title  = input("  Title: ").strip()
            author = input("  Author: ").strip()
            try:
                year   = int(input("  Year: "))
                copies = int(input("  Copies [1]: ").strip() or 1)
                lib.add_book(isbn, title, author, year, copies)
                print("  Book added.")
            except ValueError:
                print("  Invalid input.")

        elif choice == "8":
            mid   = input("  Member ID: ").strip().upper()
            name  = input("  Name: ").strip().title()
            email = input("  Email: ").strip()
            lib.register_member(mid, name, email)
            print(f"  Registered: {name}")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
