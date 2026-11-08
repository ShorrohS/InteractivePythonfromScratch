# Lesson 02 — Making API Requests with the requests Library

**Phase:** 11 — APIs | **Time:** ~45 min

---

## Part 1: Installing requests

The `requests` library is the standard way to make HTTP calls in Python.
The built-in `urllib` works but is verbose; `requests` is cleaner and far more readable.

```python
# Install once
# pip install requests

import requests   # that's all you need
```

---

## Part 2: GET Requests and the Response Object

`requests.get(url)` returns a `Response` object packed with everything the server sent back:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")

# ── Status ────────────────────────────────────────────────────────────────────
print(response.status_code)            # 200
print(response.ok)                     # True for any 2xx status

# ── Body ──────────────────────────────────────────────────────────────────────
data = response.json()                 # parse JSON body → Python dict
print(data["title"])                   # post title
print(response.text)                   # raw body as a string (for non-JSON)

# ── Metadata ──────────────────────────────────────────────────────────────────
print(response.headers["Content-Type"])  # application/json; charset=utf-8
print(response.url)                    # final URL after any redirects
print(response.elapsed)                # timedelta — how long the request took
```

---

## Part 3: Query Parameters and Custom Headers

Pass query parameters as a dict — `requests` handles URL encoding automatically:

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

# Query parameters via params={} → builds ?userId=1 automatically
params = {"userId": 1}
response = requests.get(url, params=params, timeout=10)
posts = response.json()
print(f"User 1 has {len(posts)} posts")

# Custom headers via headers={}
headers = {
    "Accept": "application/json",
    "User-Agent": "MyApp/1.0"
}
response = requests.get(url, headers=headers, params={"userId": 2}, timeout=10)
print(response.status_code)            # 200
```

---

## Part 4: POST, PUT, and DELETE Requests

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

# ── POST — create a new resource ─────────────────────────────────────────────
new_post = {
    "title": "My New Post",
    "body": "Post content here.",
    "userId": 1
}
# json={} serialises the dict and sets Content-Type: application/json automatically
response = requests.post(f"{BASE}/posts", json=new_post, timeout=10)
print(response.status_code)            # 201 Created
created = response.json()
print(f"New post id: {created['id']}") # id assigned by the server

# ── PUT — replace an entire resource ─────────────────────────────────────────
updated = {
    "id": 1,
    "title": "Replaced Title",
    "body": "Completely new body.",
    "userId": 1
}
response = requests.put(f"{BASE}/posts/1", json=updated, timeout=10)
print(response.status_code)            # 200 OK
print(response.json()["title"])        # Replaced Title

# ── DELETE — remove a resource ────────────────────────────────────────────────
response = requests.delete(f"{BASE}/posts/1", timeout=10)
print(response.status_code)            # 200 (JSONPlaceholder); real APIs often 204
```

---

## Part 5: Error Handling

```python
import requests

# raise_for_status() raises HTTPError for any 4xx or 5xx response
try:
    response = requests.get(
        "https://jsonplaceholder.typicode.com/posts/9999",
        timeout=10
    )
    response.raise_for_status()        # safe for 200; raises for 404, 500, etc.
    data = response.json()
    print(data)

except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code} — {e}")

except requests.exceptions.ConnectionError:
    print("Could not connect to the server — check network or URL")

except requests.exceptions.Timeout:
    print("Request timed out — server took too long to respond")

except requests.exceptions.RequestException as e:
    # Base class — catches any requests error not caught above
    print(f"Request failed: {e}")
```

Always pass `timeout=` — without it, a slow server will hang your program indefinitely.

---

## Part 6: The Session Object

A `Session` reuses the same TCP connection across requests and lets you set defaults once:

```python
import requests

# Context manager ensures the session is closed when done
with requests.Session() as session:
    # Set headers once — applied to every request in this session
    session.headers.update({
        "Accept": "application/json",
        "User-Agent": "MyApp/1.0"
    })

    # All three requests share the connection pool
    r1 = session.get("https://jsonplaceholder.typicode.com/users/1", timeout=10)
    r2 = session.get("https://jsonplaceholder.typicode.com/posts?userId=1", timeout=10)
    r3 = session.get("https://jsonplaceholder.typicode.com/comments?postId=1", timeout=10)

    print(r1.json()["name"])   # name of user 1
    print(len(r2.json()))      # number of user 1's posts
    print(len(r3.json()))      # number of comments on post 1
```

Use a `Session` whenever you make more than one request to the same host —
it reduces latency and overhead significantly.

---

## Part 7: Complete JSONPlaceholder Example

Full walkthrough using every HTTP method against the free test API at
`https://jsonplaceholder.typicode.com`:

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

def demo_rest_api() -> None:
    """Demonstrate GET, POST, PUT, DELETE against JSONPlaceholder."""
    with requests.Session() as session:
        session.headers.update({"Accept": "application/json"})

        # 1. GET — fetch all posts
        r = session.get(f"{BASE}/posts", timeout=10)
        r.raise_for_status()
        posts = r.json()
        print(f"Total posts: {len(posts)}")             # 100
        print(f"First title: {posts[0]['title']}")

        # 2. GET — fetch a single post
        r = session.get(f"{BASE}/posts/1", timeout=10)
        r.raise_for_status()
        print(f"Post 1 author (userId): {r.json()['userId']}")

        # 3. GET — filter with query parameter
        r = session.get(f"{BASE}/posts", params={"userId": 2}, timeout=10)
        r.raise_for_status()
        print(f"User 2 post count: {len(r.json())}")

        # 4. POST — create a new post
        r = session.post(
            f"{BASE}/posts",
            json={"title": "Test Post", "body": "Hello, API!", "userId": 1},
            timeout=10
        )
        r.raise_for_status()
        print(f"Created post id: {r.json()['id']}")     # 101

        # 5. PUT — replace post 1
        r = session.put(
            f"{BASE}/posts/1",
            json={"id": 1, "title": "Replaced", "body": "New body", "userId": 1},
            timeout=10
        )
        r.raise_for_status()
        print(f"Updated title: {r.json()['title']}")    # Replaced

        # 6. DELETE — remove post 1
        r = session.delete(f"{BASE}/posts/1", timeout=10)
        r.raise_for_status()
        print(f"Delete status: {r.status_code}")        # 200

demo_rest_api()
```

---

## Practice Exercises

1. Using `requests.get()`, fetch all users from `https://jsonplaceholder.typicode.com/users` and print each user's `name` and `email`.

2. Fetch posts with `userId=3` using the `params={}` argument. Print the `title` of each post returned.

3. Add proper error handling (using `raise_for_status()` and `except` blocks) to a GET request targeting `/posts/9999`. Print a different message for `404` vs any other `HTTPError`.

4. Rewrite exercise 1 using a `requests.Session()` context manager. Add a custom `User-Agent` header of `"PythonLearner/1.0"` that applies to the whole session.

---

## Next Lesson

**[Lesson 03 → Authentication: API Keys, Headers, Bearer Tokens](lesson-03-authentication.md)**
