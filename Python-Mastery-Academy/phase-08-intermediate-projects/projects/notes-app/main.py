"""
Notes Application
Phase 08: Intermediate Projects

SKILLS USED: OOP, JSON persistence, string search, datetime

HOW TO RUN: python main.py
"""

import json
import os
from datetime import datetime


class Note:
    def __init__(self, title: str, content: str, tags: list[str] = None):
        self.id        = None
        self.title     = title.strip()
        self.content   = content.strip()
        self.tags      = [t.strip().lower() for t in (tags or [])]
        self.created   = datetime.now().isoformat()
        self.modified  = self.created

    def update(self, title: str = None, content: str = None) -> None:
        if title:   self.title   = title.strip()
        if content: self.content = content.strip()
        self.modified = datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, d: dict) -> "Note":
        n = cls(d["title"], d["content"], d.get("tags", []))
        n.id       = d["id"]
        n.created  = d["created"]
        n.modified = d["modified"]
        return n

    def __str__(self) -> str:
        tags = f" [{', '.join(self.tags)}]" if self.tags else ""
        date = self.modified[:10]
        return f"[{self.id:03d}] {self.title}{tags}  ({date})"


class NotesApp:
    FILE = "notes.json"

    def __init__(self):
        self._notes: list[Note] = []
        self._next_id = 1
        self._load()

    def _load(self) -> None:
        if os.path.exists(self.FILE):
            with open(self.FILE) as f:
                data = json.load(f)
                self._notes  = [Note.from_dict(d) for d in data["notes"]]
                self._next_id = data.get("next_id", len(self._notes) + 1)

    def _save(self) -> None:
        with open(self.FILE, "w") as f:
            json.dump({"notes": [n.to_dict() for n in self._notes],
                       "next_id": self._next_id}, f, indent=2)

    def add(self, title: str, content: str, tags: list[str] = None) -> Note:
        note = Note(title, content, tags)
        note.id = self._next_id
        self._next_id += 1
        self._notes.append(note)
        self._save()
        return note

    def get(self, note_id: int) -> Note | None:
        return next((n for n in self._notes if n.id == note_id), None)

    def update(self, note_id: int, title: str = None, content: str = None) -> bool:
        note = self.get(note_id)
        if not note: return False
        note.update(title, content)
        self._save()
        return True

    def delete(self, note_id: int) -> bool:
        note = self.get(note_id)
        if not note: return False
        self._notes.remove(note)
        self._save()
        return True

    def search(self, query: str) -> list[Note]:
        q = query.lower()
        return [n for n in self._notes
                if q in n.title.lower()
                or q in n.content.lower()
                or any(q in t for t in n.tags)]

    def by_tag(self, tag: str) -> list[Note]:
        return [n for n in self._notes if tag.lower() in n.tags]

    def all_tags(self) -> set[str]:
        tags = set()
        for n in self._notes:
            tags.update(n.tags)
        return tags

    @property
    def count(self) -> int:
        return len(self._notes)


def main():
    app = NotesApp()
    print("=" * 50)
    print("  NOTES APPLICATION")
    print("=" * 50)

    while True:
        print(f"\n  Notes: {app.count}  |  Tags: {', '.join(sorted(app.all_tags())) or 'none'}")
        print("\n  [1] View All   [2] Add Note   [3] View Note")
        print("  [4] Edit Note  [5] Delete     [6] Search")
        print("  [7] By Tag     [0] Exit")

        choice = input("\n  Option: ").strip()

        if choice == "1":
            if not app._notes:
                print("  No notes yet.")
            else:
                for note in app._notes:
                    print(f"  {note}")

        elif choice == "2":
            title   = input("  Title: ").strip()
            print("  Content (type END on new line to finish):")
            lines = []
            while True:
                line = input("  > ")
                if line.strip().upper() == "END": break
                lines.append(line)
            content = "\n".join(lines)
            tags_input = input("  Tags (comma-separated, or blank): ").strip()
            tags = [t.strip() for t in tags_input.split(",") if t.strip()] if tags_input else []
            note = app.add(title, content, tags)
            print(f"  Saved: {note}")

        elif choice == "3":
            try:
                nid = int(input("  Note ID: "))
                note = app.get(nid)
                if note:
                    print(f"\n  Title:    {note.title}")
                    print(f"  Tags:     {', '.join(note.tags) or 'none'}")
                    print(f"  Created:  {note.created[:10]}")
                    print(f"  Modified: {note.modified[:10]}")
                    print(f"\n{note.content}")
                else:
                    print("  Note not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "4":
            try:
                nid     = int(input("  Note ID to edit: "))
                title   = input("  New title (blank to keep): ").strip() or None
                content = input("  New content (blank to keep): ").strip() or None
                if app.update(nid, title, content):
                    print("  Updated.")
                else:
                    print("  Note not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "5":
            try:
                nid = int(input("  Note ID to delete: "))
                if input(f"  Delete note {nid}? (yes/no): ").lower() == "yes":
                    print("  Deleted." if app.delete(nid) else "  Not found.")
            except ValueError:
                print("  Invalid ID.")

        elif choice == "6":
            q = input("  Search: ").strip()
            results = app.search(q)
            print(f"  {len(results)} result(s):")
            for n in results: print(f"  {n}")

        elif choice == "7":
            tag = input("  Tag: ").strip()
            results = app.by_tag(tag)
            for n in results: print(f"  {n}")

        elif choice == "0":
            print("  Goodbye!")
            break


if __name__ == "__main__":
    main()
