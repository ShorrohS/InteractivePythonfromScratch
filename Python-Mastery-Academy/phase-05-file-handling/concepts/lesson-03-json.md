# Lesson 03 — JSON Files

**Phase:** 05 — File Handling | **Time:** ~25 min

---

## What is JSON?

JSON (JavaScript Object Notation) is the universal data exchange format for APIs and configuration.

```json
{
  "name": "Alice Johnson",
  "age": 30,
  "skills": ["Python", "SQL", "Excel"],
  "address": {
    "city": "New York",
    "country": "USA"
  },
  "is_active": true
}
```

**JSON ↔ Python mapping:**

| JSON | Python |
|------|--------|
| `{}` | `dict` |
| `[]` | `list` |
| `"string"` | `str` |
| `123` | `int` |
| `1.23` | `float` |
| `true/false` | `True/False` |
| `null` | `None` |

---

## Part 2: Reading JSON

```python
import json

# From file
with open("config.json", "r") as f:
    data = json.load(f)    # file → Python dict/list

print(data["name"])
print(data["skills"][0])

# From string (e.g., API response)
json_string = '{"name": "Alice", "age": 30}'
data = json.loads(json_string)    # string → Python dict
print(data["name"])
```

---

## Part 3: Writing JSON

```python
import json

employee = {
    "name": "Alice",
    "age": 30,
    "salary": 75000.50,
    "skills": ["Python", "SQL"],
    "active": True
}

# To file
with open("employee.json", "w") as f:
    json.dump(employee, f, indent=2)   # indent makes it readable

# To string
json_str = json.dumps(employee, indent=2)
print(json_str)
```

---

## Part 4: JSON Config File Pattern

```python
"""
config.json:
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "myapp"
  },
  "app": {
    "debug": false,
    "max_records": 1000
  }
}
"""

import json
from pathlib import Path

def load_config(config_file: str = "config.json") -> dict:
    """Load configuration from JSON file."""
    path = Path(config_file)
    if not path.exists():
        return {}
    with open(path) as f:
        return json.load(f)

def save_config(config: dict, config_file: str = "config.json") -> None:
    """Save configuration to JSON file."""
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)

config = load_config()
db_host = config.get("database", {}).get("host", "localhost")
```

---

## Part 5: Business Example — Contact Manager

```python
"""Contact manager using JSON for storage."""

import json
import os

CONTACTS_FILE = "contacts.json"

def load_contacts() -> list:
    if not os.path.exists(CONTACTS_FILE):
        return []
    with open(CONTACTS_FILE) as f:
        return json.load(f)

def save_contacts(contacts: list) -> None:
    with open(CONTACTS_FILE, "w") as f:
        json.dump(contacts, f, indent=2)

def add_contact(name: str, phone: str, email: str) -> None:
    contacts = load_contacts()
    contact = {"id": len(contacts) + 1, "name": name, "phone": phone, "email": email}
    contacts.append(contact)
    save_contacts(contacts)
    print(f"✅ Added {name}")

def search_contacts(query: str) -> list:
    return [c for c in load_contacts()
            if query.lower() in c["name"].lower() or query in c["phone"]]

# Add contacts
add_contact("Alice Johnson", "555-0101", "alice@example.com")
add_contact("Bob Smith", "555-0202", "bob@example.com")

# Search
results = search_contacts("Alice")
for c in results:
    print(f"{c['name']}: {c['phone']}")
```

---

## Practice Exercises

1. Write a function `save_to_json(data, filename)` and `load_from_json(filename)`.

2. Create a JSON-based note-taking system: add, list, delete notes.

3. Given a list of dictionaries, save to JSON and load it back, verifying data is identical.

4. What is the difference between `json.load()` and `json.loads()`?

---

## Next Lesson

**[Lesson 04 → File Paths & os Module](lesson-04-paths.md)**
