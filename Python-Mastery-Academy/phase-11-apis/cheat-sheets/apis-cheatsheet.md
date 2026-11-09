# ⚡ Phase 11 Cheat Sheet — APIs

---

## All HTTP Methods

```python
import requests

BASE = "https://jsonplaceholder.typicode.com"

# GET — retrieve a resource
response = requests.get(f"{BASE}/posts/1", timeout=10)

# POST — create a new resource
response = requests.post(f"{BASE}/posts", json={"title": "hi", "userId": 1}, timeout=10)

# PUT — replace a resource entirely
response = requests.put(f"{BASE}/posts/1", json={"id": 1, "title": "new"}, timeout=10)

# PATCH — update specific fields only
response = requests.patch(f"{BASE}/posts/1", json={"title": "patched"}, timeout=10)

# DELETE — remove a resource
response = requests.delete(f"{BASE}/posts/1", timeout=10)
```

---

## Query Parameters and Request Body

```python
# Query string — appended to URL as ?key=value
# Use for: filtering, searching, pagination
response = requests.get(url, params={"userId": 1, "_limit": 10}, timeout=10)
# Sends: GET /posts?userId=1&_limit=10

# JSON body — sent as the request body
# Use for: POST/PUT/PATCH with structured data
response = requests.post(url, json={"title": "hello", "userId": 1}, timeout=10)
# Sets Content-Type: application/json automatically

# Form-encoded body — use for HTML form submissions
response = requests.post(url, data={"username": "alice", "password": "secret"}, timeout=10)
# Sets Content-Type: application/x-www-form-urlencoded
```

---

## Headers and Authentication

```python
# Custom headers
response = requests.get(url, headers={"X-Custom-Header": "value"}, timeout=10)

# API key in header (common pattern)
response = requests.get(url, headers={"X-API-Key": "your-api-key"}, timeout=10)

# Bearer token (OAuth 2.0)
token = "your-access-token"
response = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)

# HTTP Basic Auth
response = requests.get(url, auth=("username", "password"), timeout=10)

# Session — reuse headers and connections across multiple requests
session = requests.Session()
session.headers.update({"Authorization": "Bearer my-token"})
r1 = session.get(f"{BASE}/posts/1", timeout=10)    # header sent automatically
r2 = session.get(f"{BASE}/posts/2", timeout=10)    # same header, new connection reused
```

---

## Response Handling

```python
response = requests.get(url, timeout=10)

# Status code (integer)
print(response.status_code)        # 200, 201, 404, 500, etc.

# Parse JSON body into Python dict or list
data = response.json()

# Raw text body
text = response.text

# Raw bytes
raw = response.content             # useful to check if body is empty: if response.content:

# Response headers (case-insensitive dict)
content_type = response.headers.get("Content-Type")
rate_remaining = response.headers.get("X-RateLimit-Remaining")

# Accessing nested JSON
city = data["address"]["city"]     # chain brackets for nested objects
```

---

## Error Handling

```python
import requests

# Option 1 — manual status check
response = requests.get(url, timeout=10)
if response.status_code == 200:
    data = response.json()
else:
    print(f"Error: {response.status_code}")

# Option 2 — raise_for_status() (raises HTTPError on 4xx/5xx)
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()              # no-op on 2xx; raises on 4xx/5xx
    data = response.json()
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the server")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")            # catch-all for any requests error
```

---

## API Client Class Pattern

```python
import requests


class APIClient:
    """Reusable wrapper that centralises URL building, auth, and error handling."""

    def __init__(self, base_url, token=None):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self):
        h = {"Content-Type": "application/json"}
        if self.token:
            h["Authorization"] = f"Bearer {self.token}"
        return h

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = requests.request(
            method, url, headers=self._headers(), timeout=10, **kwargs
        )
        response.raise_for_status()
        return response.json() if response.content else {}

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, data):
        return self._request("POST", path, json=data)

    def put(self, path, data):
        return self._request("PUT", path, json=data)

    def delete(self, path):
        return self._request("DELETE", path)


# Usage
client = APIClient("https://jsonplaceholder.typicode.com")
post = client.get("/posts/1")
new  = client.post("/posts", {"title": "hi", "userId": 1})
```

---

## Status Code Quick Reference

| Code | Name | Meaning |
|------|------|---------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created (POST success) |
| 204 | No Content | Success, no body (common for DELETE) |
| 400 | Bad Request | Invalid request syntax or parameters |
| 401 | Unauthorized | Authentication required or failed |
| 403 | Forbidden | Authenticated but not permitted |
| 404 | Not Found | Resource does not exist |
| 429 | Too Many Requests | Rate limit exceeded — slow down |
| 500 | Internal Server Error | Server-side bug |
| 503 | Service Unavailable | Server overloaded or down |
