# Phase 11 — Completion Assessment

**Pass mark: 80% | Time: 30 minutes**

---

## PART A: Write the Code

**Task 1. `get_user_posts(user_id)`**

Write a function that:
- Accepts a `user_id` integer.
- Fetches all posts for that user from `https://jsonplaceholder.typicode.com/posts` using the query parameter `userId`.
- Handles errors: if the request fails or returns a non-200 status code, print an error message and return an empty list.
- Returns a list of post dicts.

**Example usage:**
```python
posts = get_user_posts(1)
print(len(posts))       # 10
print(posts[0]["title"])
```

---

**Task 2. `create_comment(post_id, name, email, body)`**

Write a function that:
- POSTs a new comment to `https://jsonplaceholder.typicode.com/comments`.
- Sends the payload as JSON: `{"postId": post_id, "name": name, "email": email, "body": body}`.
- Returns the `id` of the created comment.
- Raises a `ValueError` if the response status code is not 201.

**Example usage:**
```python
comment_id = create_comment(1, "Alice", "alice@example.com", "Great post!")
print(comment_id)       # 501 (JSONPlaceholder returns sequential ids)
```

---

## PART B: Predict the Output or Identify the Error

**Q3.** What is printed, or what error occurs?

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
data = response.json()
print(data["userId"])
print(data["address"]["city"])
```

---

**Q4.** What is printed, or what error occurs?

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/posts/9999", timeout=10)
response.raise_for_status()
print("Done")
```

---

## PART C: Short Answer

**Q5.** Explain the difference between `params={}` and `json={}` when making a requests call. Give an example of when you would use each.

---

**Q6.** What does `response.raise_for_status()` do, and why is it useful compared to checking `response.status_code` manually?

---

## PART D: Design

**Q7. APIClient Class Design**

Design an `APIClient` class skeleton that supports two authentication methods: API key via a header and Bearer token. Write the class with these methods:

- `__init__(self, base_url, auth_type=None, credential=None)` — `auth_type` is either `"api_key"`, `"bearer"`, or `None`
- `_build_headers(self)` — returns a headers dict based on the auth type
- `get(self, path, params=None)` — makes a GET request
- `post(self, path, data)` — makes a POST request with a JSON body

Include comments explaining the purpose of each method.

---

## Answers

**Task 1 — `get_user_posts`:**
```python
import requests

def get_user_posts(user_id):
    try:
        response = requests.get(
            "https://jsonplaceholder.typicode.com/posts",
            params={"userId": user_id},
            timeout=10
        )
        if response.status_code != 200:
            print(f"Error: received status {response.status_code}")
            return []
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return []
```

---

**Task 2 — `create_comment`:**
```python
import requests

def create_comment(post_id, name, email, body):
    payload = {"postId": post_id, "name": name, "email": email, "body": body}
    response = requests.post(
        "https://jsonplaceholder.typicode.com/comments",
        json=payload,
        timeout=10
    )
    if response.status_code != 201:
        raise ValueError(f"Unexpected status: {response.status_code}")
    return response.json()["id"]
```

---

**Q3 answer:** `1` is printed for `data["userId"]`. Then a `KeyError` is raised because the `/posts/1` response does not contain an `"address"` key — that field belongs to the `/users/{id}` endpoint. Error: `KeyError: 'address'`.

---

**Q4 answer:** `raise_for_status()` raises `requests.exceptions.HTTPError` because the status is `404 Not Found`. `"Done"` is never printed.

---

**Q5 answer:** `params={}` appends key-value pairs to the URL as a query string (`?key=value`), used for filtering/searching in GET requests. `json={}` serialises a Python dict to a JSON string and sends it in the request body, used for creating or updating resources in POST/PUT requests.

---

**Q6 answer:** `raise_for_status()` raises an `HTTPError` exception automatically for any 4xx or 5xx response. It is useful because it converts error responses into Python exceptions, letting you handle all errors in a single `try/except` block instead of writing `if status_code != 200` checks after every request.

---

**Q7 — APIClient skeleton:**
```python
import requests

class APIClient:
    def __init__(self, base_url, auth_type=None, credential=None):
        # base_url: root URL of the API (e.g. "https://api.example.com")
        # auth_type: "api_key", "bearer", or None
        # credential: the API key string or Bearer token value
        self.base_url = base_url.rstrip("/")
        self.auth_type = auth_type
        self.credential = credential

    def _build_headers(self):
        """Return a headers dict based on the configured auth type."""
        headers = {"Content-Type": "application/json"}
        if self.auth_type == "api_key":
            headers["X-API-Key"] = self.credential
        elif self.auth_type == "bearer":
            headers["Authorization"] = f"Bearer {self.credential}"
        return headers

    def get(self, path, params=None):
        """Send a GET request; params= becomes the query string."""
        url = f"{self.base_url}{path}"
        response = requests.get(url, headers=self._build_headers(),
                                params=params, timeout=10)
        response.raise_for_status()
        return response.json()

    def post(self, path, data):
        """Send a POST request with a JSON body."""
        url = f"{self.base_url}{path}"
        response = requests.post(url, headers=self._build_headers(),
                                 json=data, timeout=10)
        response.raise_for_status()
        return response.json()
```
