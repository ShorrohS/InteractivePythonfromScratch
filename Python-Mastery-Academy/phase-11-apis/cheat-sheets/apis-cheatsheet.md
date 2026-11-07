# ⚡ Phase 11 Cheat Sheet — APIs

---

## Making Requests

```python
import requests

# GET
r = requests.get(url, params={"key": "val"}, headers={}, timeout=10)

# POST
r = requests.post(url, json={"key": "val"}, headers={})

# PUT / PATCH / DELETE
r = requests.put(url, json=data)
r = requests.patch(url, json={"field": "new_val"})
r = requests.delete(url)
```

---

## Response Object

```python
r.status_code       # 200, 404, 500, ...
r.json()            # parse JSON → dict/list
r.text              # raw text
r.headers           # response headers
r.ok                # True if status < 400
r.raise_for_status()  # raises if error status
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Server Error |

---

## Authentication

```python
# API Key in header
headers = {"Authorization": "Bearer YOUR_API_KEY"}
headers = {"X-API-Key": "YOUR_KEY"}

# API Key in params
params = {"apikey": "YOUR_KEY", "q": "query"}

# Basic auth
r = requests.get(url, auth=("username", "password"))
```

---

## Error Handling

```python
try:
    r = requests.get(url, timeout=10)
    r.raise_for_status()   # raises for 4xx/5xx
    data = r.json()
except requests.exceptions.ConnectionError:
    print("No internet connection")
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.HTTPError as e:
    print(f"HTTP {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

---

## Environment Variables (API Keys)

```python
import os
from dotenv import load_dotenv    # pip install python-dotenv

load_dotenv()    # reads .env file
API_KEY = os.getenv("MY_API_KEY", "default_key")

# .env file (never commit!):
# MY_API_KEY=abc123xyz
```

---

## Common API Patterns

```python
# Pagination
all_items = []
page = 1
while True:
    r = requests.get(url, params={"page": page, "per_page": 100})
    data = r.json()
    if not data["items"]:
        break
    all_items.extend(data["items"])
    page += 1

# Retry with backoff
import time
for attempt in range(3):
    r = requests.get(url)
    if r.status_code == 200:
        break
    time.sleep(2 ** attempt)   # 1s, 2s, 4s
```
