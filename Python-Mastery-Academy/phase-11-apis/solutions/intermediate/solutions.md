# Phase 11 — Intermediate Solutions: APIs

> All solutions use JSONPlaceholder (`https://jsonplaceholder.typicode.com`).
> Install: `pip install requests`

---

## Q1. POST Request

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "Learning APIs with Python",
    "body": "The requests library makes it easy to call REST APIs.",
    "userId": 1
}

# json= serialises the dict and sets Content-Type: application/json automatically
response = requests.post(url, json=payload, timeout=10)

print(f"Status: {response.status_code}")          # 201 Created

data = response.json()
print(f"Created post with id: {data['id']}")      # JSONPlaceholder returns id 101
```

**Explanation:** `requests.post()` sends an HTTP POST. Passing `json=payload` handles JSON serialisation and sets the correct `Content-Type` header. JSONPlaceholder echoes the payload back with a new `id` (always 101 for this fake API, but a real API would assign a unique one).

---

## Q2. PUT Request

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

updated = {
    "id": 1,
    "title": "Updated Title",
    "body": "This post has been fully replaced.",
    "userId": 1
}

# PUT replaces the entire resource — include all fields
response = requests.put(url, json=updated, timeout=10)

print(f"Status: {response.status_code}")          # 200 OK

data = response.json()
print(f"Updated title: {data['title']}")          # confirm the server echoes new title
```

**Explanation:** PUT is idempotent — sending the same request multiple times produces the same result. It replaces the whole resource. PATCH would update only the specified fields. Here JSONPlaceholder echoes back the body you sent.

---

## Q3. DELETE Request

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.delete(url, timeout=10)

print(f"Status: {response.status_code}")          # 200 OK (JSONPlaceholder convention)

# JSONPlaceholder returns an empty JSON object {} rather than 204 No Content
body = response.json()
print(f"Post deleted (simulated). Response body: {body}")
```

**Explanation:** A real API typically returns `204 No Content` (empty body) on deletion. JSONPlaceholder instead returns `200 OK` with `{}`, which is a simulated response. Always check the docs for what status code and body to expect from a specific API.

---

## Q4. Auth Header

```python
import requests

# httpbin.org echoes the exact headers your client sends — great for testing
url = "https://httpbin.org/headers"

headers = {
    "Authorization": "Bearer fake-token-12345"
}

response = requests.get(url, headers=headers, timeout=10)

echoed_headers = response.json()["headers"]       # httpbin nests headers here
print(f"Authorization header sent: {echoed_headers['Authorization']}")
```

**Explanation:** The `headers=` keyword argument adds custom HTTP headers to the request. `Bearer <token>` is the standard format for OAuth 2.0 token authentication. httpbin.org is a handy debugging tool that reflects back everything it receives.

---

## Q5. Pagination

```python
import requests

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

all_posts = []

for page_num in range(1, 3):                      # pages 1 and 2
    params = {"_page": page_num, "_limit": 10}
    response = requests.get(BASE_URL, params=params, timeout=10)
    page_data = response.json()
    all_posts.extend(page_data)                   # append this page's items
    print(f"Fetched page {page_num}: {len(page_data)} posts")

print(f"\nTotal posts collected: {len(all_posts)}")
print(f"Last post title: {all_posts[-1]['title']}")
```

**Explanation:** Pagination means fetching data in chunks. The server controls page size; the client increments `_page` each time. `list.extend()` appends all items from another list — more efficient than `+=` item-by-item.

---

## Q6. Save Response to File

```python
import requests
import json

url = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(url, timeout=10)
all_posts = response.json()                       # list of 100 posts

print(f"Total posts fetched: {len(all_posts)}")

# Filter to user 1 only
user1_posts = [post for post in all_posts if post["userId"] == 1]

print(f"Posts for userId=1: {len(user1_posts)}")

# Write to a JSON file with human-readable indentation
with open("posts_user1.json", "w") as f:
    json.dump(user1_posts, f, indent=2)

print("Saved to posts_user1.json")
```

**Explanation:** `json.dump(data, file_object, indent=2)` serialises Python data to JSON and writes it to an open file. `indent=2` produces readable formatting with 2-space indentation. The `with` block ensures the file is closed even if an error occurs.

---

> **Exercises:** → [../../exercises/intermediate/exercises.md](../../exercises/intermediate/exercises.md)
