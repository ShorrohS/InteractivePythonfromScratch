"""
Password Manager
Phase 08: Intermediate Projects

SKILLS USED: OOP, JSON, base64 encoding (basic obfuscation),
             string generation, search, clipboard

NOTE: This uses simple base64 encoding — NOT real encryption.
      For production, use the 'cryptography' library.
      This demonstrates the programming concepts only.

HOW TO RUN: python main.py
"""

import json
import os
import base64
import secrets
import string
from datetime import datetime


def encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

def decode(text: str) -> str:
    return base64.b64decode(text.encode()).decode()

def generate_password(length: int = 16,
                      use_upper: bool = True,
                      use_digits: bool = True,
                      use_symbols: bool = True) -> str:
    chars = string.ascii_lowercase
    if use_upper:   chars += string.ascii_uppercase
    if use_digits:  chars += string.digits
    if use_symbols: chars += "!@#$%^&*"
    return ''.join(secrets.choice(chars) for _ in range(length))

def mask_password(pwd: str) -> str:
    if len(pwd) <= 4:
        return "*" * len(pwd)
    return pwd[:2] + "*" * (len(pwd) - 4) + pwd[-2:]


class Entry:
    def __init__(self, site: str, username: str, password: str, notes: str = ""):
        self.id        = None
        self.site      = site.strip()
        self.username  = username.strip()
        self._password = encode(password)
        self.notes     = notes.strip()
        self.created   = datetime.now().isoformat()
        self.modified  = self.created

    @property
    def password(self) -> str:
        return decode(self._password)

    @password.setter
    def password(self, new_pwd: str) -> None:
        self._password = encode(new_pwd)
        self.modified  = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "id": self.id, "site": self.site,
            "username": self.username, "_password": self._password,
            "notes": self.notes, "created": self.created, "modified": self.modified
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Entry":
        e = cls.__new__(cls)
        e.__dict__.update(d)
        return e

    def __str__(self) -> str:
        return f"[{self.id:03d}] {self.site:<25} {self.username}"


class PasswordManager:
    FILE = "vault.json"

    def __init__(self, master_pin: str = "1234"):
        self._master   = encode(master_pin)
        self._entries: list[Entry] = []
        self._next_id  = 1
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.FILE): return
        with open(self.FILE) as f:
            data = json.load(f)
            self._entries  = [Entry.from_dict(d) for d in data.get("entries", [])]
            self._next_id  = data.get("next_id", len(self._entries) + 1)
            self._master   = data.get("master", self._master)

    def _save(self) -> None:
        with open(self.FILE, "w") as f:
            json.dump({
                "entries":  [e.to_dict() for e in self._entries],
                "next_id":  self._next_id,
                "master":   self._master
            }, f, indent=2)

    def verify_master(self, pin: str) -> bool:
        return encode(pin) == self._master

    def add(self, site: str, username: str, password: str, notes: str = "") -> Entry:
        entry = Entry(site, username, password, notes)
        entry.id = self._next_id
        self._next_id += 1
        self._entries.append(entry)
        self._save()
        return entry

    def get(self, entry_id: int) -> Entry | None:
        return next((e for e in self._entries if e.id == entry_id), None)

    def update_password(self, entry_id: int, new_password: str) -> bool:
        e = self.get(entry_id)
        if not e: return False
        e.password = new_password
        self._save()
        return True

    def delete(self, entry_id: int) -> bool:
        e = self.get(entry_id)
        if not e: return False
        self._entries.remove(e)
        self._save()
        return True

    def search(self, query: str) -> list[Entry]:
        q = query.lower()
        return [e for e in self._entries
                if q in e.site.lower() or q in e.username.lower()]


def main():
    mgr = PasswordManager(master_pin="1234")
    print("=" * 50)
    print("  PASSWORD MANAGER")
    print("  [Demo uses PIN: 1234]")
    print("=" * 50)

    # Authenticate
    for attempt in range(3):
        pin = input(f"\n  Master PIN (attempt {attempt+1}/3): ").strip()
        if mgr.verify_master(pin):
            print("  Unlocked!")
            break
        if attempt == 2:
            print("  Too many failed attempts.")
            return

    while True:
        print(f"\n  Stored: {len(mgr._entries)} entries")
        print("\n  [1] List All    [2] Add Entry     [3] View Password")
        print("  [4] Update Pwd  [5] Delete        [6] Search")
        print("  [7] Generate    [0] Lock & Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            if not mgr._entries:
                print("  No entries.")
            else:
                print(f"\n  {'ID':<5} {'Site':<25} {'Username'}")
                print("  " + "-" * 45)
                for e in mgr._entries:
                    print(f"  {e}")

        elif choice == "2":
            site     = input("  Website/App: ").strip()
            username = input("  Username/Email: ").strip()
            gen = input("  Generate password? (yes/no): ").lower()
            if gen in ("yes", "y"):
                length = int(input("  Length [16]: ").strip() or 16)
                pwd    = generate_password(length)
                print(f"  Generated: {pwd}")
            else:
                pwd = input("  Password: ").strip()
            notes = input("  Notes (optional): ").strip()
            entry = mgr.add(site, username, pwd, notes)
            print(f"  Saved: {entry}")

        elif choice == "3":
            try:
                eid  = int(input("  Entry ID: "))
                e    = mgr.get(eid)
                pin  = input("  Confirm master PIN: ").strip()
                if e and mgr.verify_master(pin):
                    print(f"\n  Site:     {e.site}")
                    print(f"  Username: {e.username}")
                    print(f"  Password: {e.password}")
                    if e.notes: print(f"  Notes:    {e.notes}")
                else:
                    print("  Not found or wrong PIN.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "4":
            try:
                eid = int(input("  Entry ID: "))
                gen = input("  Generate new password? (yes/no): ").lower()
                if gen in ("yes", "y"):
                    new_pwd = generate_password()
                    print(f"  New password: {new_pwd}")
                else:
                    new_pwd = input("  New password: ").strip()
                print("  Updated." if mgr.update_password(eid, new_pwd) else "  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "5":
            try:
                eid = int(input("  Entry ID to delete: "))
                if input(f"  Delete entry {eid}? (yes/no): ").lower() == "yes":
                    print("  Deleted." if mgr.delete(eid) else "  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "6":
            q = input("  Search site or username: ").strip()
            for e in mgr.search(q):
                print(f"  {e}")

        elif choice == "7":
            length  = int(input("  Length [16]: ").strip() or 16)
            symbols = input("  Include symbols? (yes/no) [yes]: ").lower() != "no"
            pwd     = generate_password(length, use_symbols=symbols)
            print(f"  Generated: {pwd}")
            print(f"  Masked:    {mask_password(pwd)}")

        elif choice == "0":
            print("  Vault locked. Goodbye!")
            break


if __name__ == "__main__":
    main()
