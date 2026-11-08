# Lesson 01 — What Are APIs: REST, JSON, HTTP Methods

**Phase:** 11 — APIs | **Time:** ~35 min

---

## Part 1: What is an API?

An API (Application Programming Interface) is a contract between two software systems.
One side defines what it can do; the other calls those defined operations.

**Why APIs exist:**
- Share data between applications without exposing the underlying database
- Let developers build on top of existing services: maps, payments, weather data
- Separate the front end from the back end cleanly
- Enable third-party integrations ("Login with Google", "Pay with Stripe")

**Real-world examples:**
- A weather app calls a weather API to get forecast data
- An online store calls the Stripe API to process card payments
- A delivery app calls a mapping API to calculate routes and ETAs
- A news site calls a social media API to display share counts

---

## Part 2: REST Architecture

REST (Representational State Transfer) is the dominant style for web APIs today.

**Core principles:**
- **Stateless** — every request carries all the information the server needs; no session is stored between calls
- **Resource-based** — data is modelled as resources, each with its own URL (`/users`, `/orders/42`)
- **Standard methods** — HTTP verbs signal the intended operation (GET, POST, PUT, PATCH, DELETE)
- **JSON bodies** — almost all REST APIs send and receive JSON

A REST API maps directly to **CRUD** operations:

| CRUD | HTTP Method | Example |
|------|-------------|---------|
| Create | POST | `POST /posts` |
| Read | GET | `GET /posts` or `GET /posts/1` |
| Update (full) | PUT | `PUT /posts/1` |
| Update (partial) | PATCH | `PATCH /posts/1` |
| Delete | DELETE | `DELETE /posts/1` |

---

## Part 3: HTTP Methods

```python
# GET — fetch data (safe, no side effects, idempotent)
# GET /users        → returns list of all users
# GET /users/42     → returns only user 42

# POST — create a new resource (not idempotent — two calls create two records)
# POST /users       → creates a new user from the request body

# PUT — replace an entire resource (idempotent)
# PUT /users/42     → fully replaces user 42 with the data you send
#                     any field you omit gets cleared or reset to default

# PATCH — partial update (only the fields you send are changed)
# PATCH /users/42   → updates only the fields included in the body
#                     everything else stays as-is

# DELETE — remove a resource (idempotent)
# DELETE /users/42  → removes user 42 permanently
```

---

## Part 4: URL Structure

```
https://api.example.com/v1/products/99?format=json&limit=10
  │         │            │     │    │       │
  protocol  host       version │   id    query params
                           resource
```

- **Protocol** — always `https` for real APIs (never plain `http`)
- **Host** — the API server domain
- **Version** — `/v1`, `/v2` — lets the API evolve without breaking old clients
- **Resource path** — the noun: `/products`, `/users`, `/orders/99`
- **Query parameters** — start with `?`, separated by `&`; used for filters, sorting, pagination

```python
import requests

# requests builds the full query string automatically from a dict
base_url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": "London",
    "units": "metric",
    "appid": "YOUR_API_KEY"
}
# Actual URL sent: .../weather?q=London&units=metric&appid=YOUR_API_KEY
response = requests.get(base_url, params=params)
```

---

## Part 5: HTTP Status Codes

Every response includes a 3-digit code that signals the outcome:

```python
# 2xx — Success
200  # OK            — standard success for GET, PUT, PATCH
201  # Created       — resource created successfully (POST)
204  # No Content    — success with no response body (common for DELETE)

# 3xx — Redirect
301  # Moved Permanently — URL has changed; update your bookmarks
302  # Found             — temporary redirect

# 4xx — Client error (something in your request is wrong)
400  # Bad Request   — malformed syntax or invalid parameter value
401  # Unauthorized  — missing or invalid credentials
403  # Forbidden     — authenticated but not allowed to access this resource
404  # Not Found     — the resource does not exist
429  # Too Many Reqs — rate limit exceeded; check the Retry-After header

# 5xx — Server error (the API has a problem on its end)
500  # Internal Server Error — generic server-side failure
503  # Service Unavailable   — server temporarily down or overloaded

# Rule of thumb:
# 2xx → you're good    4xx → fix your request    5xx → wait and retry
```

---

## Part 6: JSON — The Data Format

JSON (JavaScript Object Notation) is the universal body format for REST APIs.
Python dicts and lists map almost directly to JSON objects and arrays:

```python
import json

# ── JSON object  ↔  Python dict ──────────────────────────────────────────────
json_str = '{"id": 1, "name": "Alice", "active": true, "score": 9.5}'
data = json.loads(json_str)    # string  → dict
print(data["name"])            # Alice
print(data["active"])          # True   (Python bool, not JSON true)
print(data["score"])           # 9.5

# ── JSON array  ↔  Python list ───────────────────────────────────────────────
json_arr = '[{"id": 1, "city": "London"}, {"id": 2, "city": "Paris"}]'
cities = json.loads(json_arr)
print(cities[0]["city"])       # London
print(len(cities))             # 2

# ── Nested JSON  ↔  Nested dict/list ─────────────────────────────────────────
user = {
    "id": 42,
    "name": "Bob",
    "address": {
        "city": "Tokyo",
        "country": "Japan"
    },
    "tags": ["admin", "verified"]
}
print(user["address"]["city"])   # Tokyo
print(user["tags"][1])           # verified

# ── Python dict → JSON string ─────────────────────────────────────────────────
output = json.dumps(user, indent=2)
print(output)
```

**JSON ↔ Python type mapping:**

| JSON | Python |
|------|--------|
| `{}` object | `dict` |
| `[]` array | `list` |
| `"string"` | `str` |
| `123` / `1.5` | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

---

## Part 7: Reading API Documentation

Before calling any API, read its docs and look for:

1. **Base URL** — e.g. `https://api.github.com`
2. **Endpoint** — method + path, e.g. `GET /users/{username}`
3. **Parameters** — required vs optional, and where they go (path / query / body)
4. **Authentication** — API key? Bearer token? No auth needed?
5. **Example response** — the JSON shape you will receive
6. **Rate limits** — how many requests per minute or hour are allowed

```python
import requests

# Example: GitHub docs say GET /users/{username} needs no auth for public data
# Rate limit: 60 req/hour unauthenticated, 5 000 req/hour with a token
# Response fields include: login, name, public_repos, followers, ...

response = requests.get("https://api.github.com/users/torvalds")
print(response.status_code)         # 200

data = response.json()
print(data["name"])                  # Linus Torvalds
print(data["public_repos"])          # number of public repos
print(data["followers"])             # follower count
```

---

## Practice Exercises

1. Visit `https://jsonplaceholder.typicode.com`. List at least 4 endpoints it provides, the HTTP method each uses, and what resource each targets.

2. Given the URL `https://api.store.com/v2/products?category=books&sort=price&limit=20` — identify the protocol, host, API version, resource path, and each query parameter with its value.

3. Match each scenario to the correct HTTP method: (a) fetch a user's profile, (b) register a new account, (c) change only a user's email, (d) delete a comment, (e) completely replace a product record.

4. Write a Python dict that mirrors this JSON, then convert it back with `json.dumps(indent=2)`:
   `{"order": {"id": 99, "items": [{"sku": "A1", "qty": 2}], "shipped": false, "total": null}}`

---

## Next Lesson

**[Lesson 02 → Making API Requests with the requests Library](lesson-02-api-requests.md)**
