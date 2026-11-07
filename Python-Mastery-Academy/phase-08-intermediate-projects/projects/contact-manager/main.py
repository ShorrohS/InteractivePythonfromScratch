"""
Contact Manager
Phase 08: Intermediate Projects

SKILLS USED: OOP, JSON persistence, search/filter, sorting, @property

HOW TO RUN: python main.py
"""

import json
import os
import re
from datetime import datetime


class Contact:
    def __init__(self, first: str, last: str, email: str = "",
                 phone: str = "", company: str = "", group: str = "General"):
        self.id        = None
        self.first     = first.strip().title()
        self.last      = last.strip().title()
        self._email    = ""
        self._phone    = ""
        self.email     = email
        self.phone     = phone
        self.company   = company.strip()
        self.group     = group.strip()
        self.created   = datetime.now().strftime("%Y-%m-%d")

    @property
    def full_name(self) -> str:
        return f"{self.first} {self.last}"

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if value and "@" not in value:
            raise ValueError(f"Invalid email: {value}")
        self._email = value.strip().lower()

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = re.sub(r"[^\d\-\+\(\) ]", "", value)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "first": self.first, "last": self.last,
            "_email": self._email, "_phone": self._phone,
            "company": self.company, "group": self.group, "created": self.created
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Contact":
        c = cls.__new__(cls)
        c.id      = d["id"]
        c.first   = d["first"]
        c.last    = d["last"]
        c._email  = d.get("_email", "")
        c._phone  = d.get("_phone", "")
        c.company = d.get("company", "")
        c.group   = d.get("group", "General")
        c.created = d.get("created", "")
        return c

    def __str__(self) -> str:
        info = []
        if self._email: info.append(self._email)
        if self._phone: info.append(self._phone)
        detail = " | ".join(info) if info else "No contact info"
        return f"[{self.id:03d}] {self.full_name:<25} {detail}"


class ContactBook:
    FILE = "contacts.json"

    def __init__(self):
        self._contacts: list[Contact] = []
        self._next_id  = 1
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.FILE): return
        with open(self.FILE) as f:
            data = json.load(f)
            self._contacts = [Contact.from_dict(d) for d in data.get("contacts", [])]
            self._next_id  = data.get("next_id", len(self._contacts) + 1)

    def _save(self) -> None:
        with open(self.FILE, "w") as f:
            json.dump({"contacts": [c.to_dict() for c in self._contacts],
                       "next_id":   self._next_id}, f, indent=2)

    def add(self, **kwargs) -> Contact:
        c = Contact(**kwargs)
        c.id = self._next_id
        self._next_id += 1
        self._contacts.append(c)
        self._save()
        return c

    def get(self, cid: int) -> Contact | None:
        return next((c for c in self._contacts if c.id == cid), None)

    def delete(self, cid: int) -> bool:
        c = self.get(cid)
        if not c: return False
        self._contacts.remove(c)
        self._save()
        return True

    def search(self, query: str) -> list[Contact]:
        q = query.lower()
        return [c for c in self._contacts
                if q in c.full_name.lower()
                or q in c._email.lower()
                or q in c._phone
                or q in c.company.lower()]

    def by_group(self, group: str) -> list[Contact]:
        return [c for c in self._contacts if c.group.lower() == group.lower()]

    def all_groups(self) -> set[str]:
        return {c.group for c in self._contacts}

    @property
    def sorted(self) -> list[Contact]:
        return sorted(self._contacts, key=lambda c: (c.last, c.first))

    @property
    def count(self) -> int:
        return len(self._contacts)


def main():
    book = ContactBook()
    print("=" * 55)
    print("  CONTACT MANAGER")
    print("=" * 55)

    while True:
        print(f"\n  Contacts: {book.count}  |  Groups: {', '.join(sorted(book.all_groups()))}")
        print("\n  [1] View All   [2] Add Contact  [3] View Detail")
        print("  [4] Search     [5] By Group     [6] Delete")
        print("  [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            if not book._contacts:
                print("  No contacts.")
            else:
                for c in book.sorted:
                    print(f"  {c}")

        elif choice == "2":
            try:
                first   = input("  First name: ").strip()
                last    = input("  Last name: ").strip()
                email   = input("  Email: ").strip()
                phone   = input("  Phone: ").strip()
                company = input("  Company: ").strip()
                groups  = list(book.all_groups()) or ["General", "Work", "Family", "Friend"]
                print(f"  Groups: {', '.join(groups)}")
                group   = input("  Group [General]: ").strip() or "General"
                c = book.add(first=first, last=last, email=email,
                             phone=phone, company=company, group=group)
                print(f"  Saved: {c}")
            except ValueError as e:
                print(f"  Error: {e}")

        elif choice == "3":
            try:
                cid = int(input("  Contact ID: "))
                c = book.get(cid)
                if c:
                    print(f"\n  Name:    {c.full_name}")
                    print(f"  Email:   {c._email or 'N/A'}")
                    print(f"  Phone:   {c._phone or 'N/A'}")
                    print(f"  Company: {c.company or 'N/A'}")
                    print(f"  Group:   {c.group}")
                    print(f"  Added:   {c.created}")
                else:
                    print("  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "4":
            q = input("  Search: ").strip()
            results = book.search(q)
            print(f"  {len(results)} result(s):")
            for c in results: print(f"  {c}")

        elif choice == "5":
            group = input("  Group name: ").strip()
            results = book.by_group(group)
            print(f"  {len(results)} contact(s) in '{group}':")
            for c in results: print(f"  {c}")

        elif choice == "6":
            try:
                cid = int(input("  Contact ID to delete: "))
                if input(f"  Delete contact {cid}? (yes/no): ").lower() == "yes":
                    print("  Deleted." if book.delete(cid) else "  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
