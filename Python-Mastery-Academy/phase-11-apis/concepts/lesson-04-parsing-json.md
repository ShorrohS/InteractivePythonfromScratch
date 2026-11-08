# Lesson 04 — Parsing and Processing JSON Responses

**Phase:** 11 — APIs | **Time:** ~45 min

---

## Part 1: JSON Structure Review

JSON has two container types that map directly to Python:
- `{}` **object** — ordered key/value pairs → Python `dict`
- `[]` **array** — ordered sequence → Python `list`

Every API response is either an object (one resource) or an array (a collection):

```python
# Single resource → dict
# GET /users/1 returns:
# {"id": 1, "name": "Leanne Graham", "email": "Sincere@april.biz"}

# Collection → list of dicts
# GET /users returns:
# [
#   {"id": 1, "name": "Leanne Graham"},
#   {"id": 2, "name": "Ervin Howell"},
#   ...
# ]
```

---

## Part 2: json.loads(), json.dumps(), and response.json()

```python
import json
import requests

# ── String → dict ─────────────────────────────────────────────────────────────
raw = '{"id": 1, "name": "Alice", "active": true, "score": null}'
data = json.loads(raw)
print(data["active"])   # True  (Python bool, not the string "true")
print(data["score"])    # None  (Python None, not the string "null")

# ── dict → String ─────────────────────────────────────────────────────────────
pretty = json.dumps(data, indent=2)
print(pretty)

# ── response.json() shortcut ──────────────────────────────────────────────────
# This is identical to json.loads(response.text) but cleaner
response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
response.raise_for_status()
user = response.json()
print(user["name"])     # Leanne Graham
```

---

## Part 3: Navigating Nested JSON

Real API responses are often deeply nested. Chain `[]` to drill down:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
response.raise_for_status()
user = response.json()

# Flat fields
print(user["id"])                          # 1
print(user["name"])                        # Leanne Graham
print(user["email"])                       # Sincere@april.biz

# One level deep — nested object
print(user["address"]["city"])             # Gwenborough
print(user["address"]["zipcode"])          # 92998-3874

# Two levels deep
print(user["address"]["geo"]["lat"])       # -37.3159
print(user["address"]["geo"]["lng"])       # 81.1496

# Nested under "company"
print(user["company"]["name"])             # Romaguera-Crona
print(user["company"]["catchPhrase"])      # Multi-layered client-server neural-net
```

---

## Part 4: Safe Key Access with .get()

`dict["key"]` raises `KeyError` if the key is absent.
Use `.get()` to supply a fallback instead of crashing:

```python
user = {
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
    # "phone" key is absent from this response
}

# Unsafe — raises KeyError if key is missing
# print(user["phone"])

# Safe — returns None (or your default) if key is missing
phone = user.get("phone")              # None
phone = user.get("phone", "N/A")      # "N/A"

# Chained .get() for nested keys — avoids AttributeError on a None midway
city = user.get("address", {}).get("city", "Unknown")
print(city)   # "Unknown" — doesn't crash even though "address" is absent

# Deep chain pattern
lat = (
    user
    .get("address", {})
    .get("geo", {})
    .get("lat", "0.0")
)
print(lat)    # "0.0"
```

---

## Part 5: Processing Lists of API Objects

When the response is an array, combine list comprehensions with key access:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10)
response.raise_for_status()
users = response.json()   # list of 10 user dicts

# Extract a single field from every item
names = [u["name"] for u in users]
print(names)

# Filter by a condition
early_users = [u for u in users if u["id"] <= 5]

# Build simplified summary dicts
summaries = [
    {
        "name": u["name"],
        "email": u["email"],
        "city": u["address"]["city"]
    }
    for u in users
]
for s in summaries:
    print(f"{s['name']:30} {s['email']:35} {s['city']}")
```

---

## Part 6: Handling Missing and Null Fields

Never assume every field will be present in every response. Defensive access prevents
runtime crashes in production:

```python
def extract_user_info(user: dict) -> dict:
    """
    Safely pull fields from a user dict returned by the API.
    Handles absent keys and null values without raising errors.
    """
    return {
        "id":      user.get("id"),
        "name":    user.get("name", "Unknown"),
        "email":   user.get("email", ""),
        "phone":   user.get("phone"),                      # may be None — that's OK
        "city":    user.get("address", {}).get("city", ""),
        "company": user.get("company", {}).get("name", ""),
    }

import requests

users = requests.get("https://jsonplaceholder.typicode.com/users", timeout=10).json()
cleaned = [extract_user_info(u) for u in users]

for c in cleaned:
    print(f"{c['name']} | {c['city']} | {c['company']}")
```

---

## Part 7: Handling Pagination

Large data sets are split across pages. Two common patterns:

```python
import requests

# ── Pattern 1: page / per_page query parameters ────────────────────────────
def fetch_all_pages(base_url: str, per_page: int = 10) -> list:
    """Collect every page until an empty response signals the end."""
    all_items = []
    page = 1
    while True:
        r = requests.get(
            base_url,
            params={"_page": page, "_limit": per_page},
            timeout=10
        )
        r.raise_for_status()
        batch = r.json()
        if not batch:              # empty list → no more pages
            break
        all_items.extend(batch)
        page += 1
    return all_items

# ── Pattern 2: next URL embedded in response body ─────────────────────────
def fetch_with_next_link(start_url: str) -> list:
    """Follow the 'next' URL field until it is null."""
    all_items = []
    url = start_url
    while url:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        payload = r.json()
        all_items.extend(payload.get("results", []))
        url = payload.get("next")  # None on the last page → loop ends
    return all_items
```

---

## Part 8: Complete Example — Fetch, Filter, and Save

Full pipeline: call the API → parse → filter by city → save results to a JSON file:

```python
import json
import requests

def save_users_from_city(city_fragment: str, output_path: str) -> None:
    """
    Fetch all users from JSONPlaceholder, keep only those whose city
    contains city_fragment (case-insensitive), and write to a JSON file.
    """
    response = requests.get(
        "https://jsonplaceholder.typicode.com/users",
        timeout=10
    )
    response.raise_for_status()
    users = response.json()

    results = []
    for user in users:
        city = user.get("address", {}).get("city", "")
        if city_fragment.lower() in city.lower():
            results.append({
                "name":    user.get("name"),
                "email":   user.get("email"),
                "city":    city,
                "company": user.get("company", {}).get("name", ""),
            })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved {len(results)} user(s) matching '{city_fragment}' → {output_path}")

# Run it — "ville" matches cities like "Gwenborough" or "South Elvira"
save_users_from_city("ville", "city_users.json")
```

---

## Practice Exercises

1. Fetch `https://jsonplaceholder.typicode.com/posts` and use a list comprehension to
   produce a list of dicts containing only `id`, `userId`, and `title` for each post.

2. From the `/users` endpoint, extract each user's `name`, `username`, and `company.name`
   using `.get()` on all three so the code will not crash if a field is absent.

3. Write a `paginate(url, max_pages)` function that fetches up to `max_pages` pages using
   `?_page=N&_limit=5` query params (JSONPlaceholder supports this) and returns a flat list.

4. Extend `save_users_from_city()` to also write a plain `.txt` summary file with one line
   per user in the format `Name | Email | City`.

---

## Next Lesson

**[Lesson 05 → Building a Simple API Client Class](lesson-05-api-client-class.md)**
