# Phase 11 — Advanced Solutions: APIs

> Install dependencies before running: `pip install requests`
> All code targets Python 3.8+.

---

## Q1. API Client Class

```python
import requests


class JSONPlaceholderClient:
    """Reusable client for the JSONPlaceholder fake REST API."""

    def __init__(self, base_url="https://jsonplaceholder.typicode.com", api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, method, path, **kwargs):
        """Central dispatcher: builds URL, injects auth header, enforces timeout."""
        url = f"{self.base_url}{path}"

        # Build headers, injecting Bearer token when an api_key is set
        headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        response = requests.request(
            method,
            url,
            headers=headers,
            timeout=10,
            **kwargs,
        )

        response.raise_for_status()             # raise HTTPError on 4xx/5xx

        # Guard against empty bodies (e.g. 204 No Content or DELETE responses)
        return response.json() if response.content else {}

    # --- public methods -------------------------------------------------------

    def get_post(self, post_id):
        return self._request("GET", f"/posts/{post_id}")

    def create_post(self, data):
        return self._request("POST", "/posts", json=data)

    def update_post(self, post_id, data):
        return self._request("PUT", f"/posts/{post_id}", json=data)

    def delete_post(self, post_id):
        return self._request("DELETE", f"/posts/{post_id}")


# --- demonstration -----------------------------------------------------------
if __name__ == "__main__":
    client = JSONPlaceholderClient()

    post = client.get_post(1)
    print(f"GET  post 1 title : {post['title']}")

    new_post = client.create_post({"title": "Hello API", "body": "test", "userId": 1})
    print(f"POST created id   : {new_post['id']}")

    updated = client.update_post(1, {"id": 1, "title": "New Title", "body": "x", "userId": 1})
    print(f"PUT  updated title: {updated['title']}")

    result = client.delete_post(1)
    print(f"DELETE response   : {result}")
```

---

## Q2. Retry with Exponential Backoff

```python
import time
import requests
from unittest.mock import patch, MagicMock


class JSONPlaceholderClient:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com", api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def _request_with_retry(self, method, path, max_retries=3, **kwargs):
        """Retry on 429 or 5xx with exponential backoff (1s, 2s, 4s)."""
        delay = 1                               # initial wait in seconds
        last_error = None

        for attempt in range(1, max_retries + 1):
            try:
                return self._request(method, path, **kwargs)
            except requests.exceptions.HTTPError as e:
                status = e.response.status_code if e.response is not None else 0
                if status == 429 or status >= 500:
                    last_error = e
                    print(f"  Attempt {attempt} failed (HTTP {status}). "
                          f"Retrying in {delay}s...")
                    time.sleep(delay)
                    delay *= 2                  # double the wait time
                else:
                    raise                       # non-retryable error — propagate immediately

        raise last_error                        # all retries exhausted


# --- demonstration with mock (no real failed requests) -----------------------
if __name__ == "__main__":
    client = JSONPlaceholderClient()

    call_count = 0

    def fake_request(method, url, **kwargs):
        """First two calls → 429, third call → 200."""
        nonlocal call_count
        call_count += 1

        mock_resp = MagicMock()
        if call_count < 3:
            mock_resp.status_code = 429
            error = requests.exceptions.HTTPError(response=mock_resp)
            mock_resp.raise_for_status.side_effect = error
        else:
            mock_resp.status_code = 200
            mock_resp.content = b'{"id": 1, "title": "ok"}'
            mock_resp.json.return_value = {"id": 1, "title": "ok"}
            mock_resp.raise_for_status.side_effect = None

        return mock_resp

    with patch("requests.request", side_effect=fake_request), \
         patch("time.sleep"):                   # skip real sleeps in demo
        result = client._request_with_retry("GET", "/posts/1")
        print(f"Success after {call_count} attempts: {result}")
```

---

## Q3. Rate Limit Header Awareness

```python
import time
import requests
from unittest.mock import patch, MagicMock

RATE_LIMIT_THRESHOLD = 10
RATE_LIMIT_SLEEP = 60       # seconds to pause when limit is low


def check_rate_limit(response):
    """Inspect X-RateLimit-Remaining and throttle if needed."""
    remaining = response.headers.get("X-RateLimit-Remaining")

    if remaining is None:
        print("Rate limit header not present — no throttling needed.")
        return

    remaining = int(remaining)
    print(f"X-RateLimit-Remaining: {remaining}")

    if remaining < RATE_LIMIT_THRESHOLD:
        print(f"WARNING: only {remaining} requests left. "
              f"Sleeping for {RATE_LIMIT_SLEEP}s...")
        time.sleep(RATE_LIMIT_SLEEP)
    else:
        print("Rate limit OK — continuing.")


# --- demonstration without real network or actual sleep ----------------------
if __name__ == "__main__":
    # Simulate a response with a low remaining count
    mock_response = MagicMock()
    mock_response.headers = {"X-RateLimit-Remaining": "3"}

    with patch("time.sleep") as mock_sleep:
        check_rate_limit(mock_response)
        print(f"time.sleep called with: {mock_sleep.call_args}")

    print()

    # Simulate a response with no rate limit header (like JSONPlaceholder)
    mock_response2 = MagicMock()
    mock_response2.headers = {}
    check_rate_limit(mock_response2)
```

---

## Q4. SQLite Response Cache

```python
import sqlite3
import json
import requests


DB_FILE = "posts_cache.db"
BASE_URL = "https://jsonplaceholder.typicode.com"


def init_db(conn):
    """Create cache table if it doesn't already exist."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS cache "
        "(post_id INTEGER PRIMARY KEY, data TEXT)"
    )
    conn.commit()


def get_post_cached(conn, post_id):
    """Return post from cache (HIT) or fetch from API and store it (MISS)."""
    cursor = conn.execute(
        "SELECT data FROM cache WHERE post_id = ?", (post_id,)
    )
    row = cursor.fetchone()

    if row:
        print(f"HIT  — loaded post {post_id} from cache")
        return json.loads(row[0])               # deserialise stored JSON text

    # Cache miss — fetch from the real API
    response = requests.get(f"{BASE_URL}/posts/{post_id}", timeout=10)
    response.raise_for_status()
    data = response.json()

    # Store in DB for future calls
    conn.execute(
        "INSERT INTO cache (post_id, data) VALUES (?, ?)",
        (post_id, json.dumps(data))             # serialise to text for storage
    )
    conn.commit()

    print(f"MISS — fetched post {post_id} from API")
    return data


if __name__ == "__main__":
    conn = sqlite3.connect(DB_FILE)
    init_db(conn)

    # Post 1 twice — first call MISS, second call HIT
    get_post_cached(conn, 1)
    get_post_cached(conn, 1)

    # Post 2 once — MISS
    get_post_cached(conn, 2)

    conn.close()
```

---

## Q5. Mock Testing

```python
import unittest
from unittest.mock import patch, MagicMock
import requests


class JSONPlaceholderClient:
    """Minimal client for testing (same as Q1 solution)."""

    def __init__(self, base_url="https://jsonplaceholder.typicode.com", api_key=None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        headers = kwargs.pop("headers", {})
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.request(method, url, headers=headers, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}

    def get_post(self, post_id):
        return self._request("GET", f"/posts/{post_id}")

    def create_post(self, data):
        return self._request("POST", "/posts", json=data)


class TestJSONPlaceholderClient(unittest.TestCase):

    @patch("requests.request")
    def test_get_post_returns_correct_data(self, mock_request):
        """get_post() should return the parsed JSON dict."""
        fake_post = {"id": 1, "title": "Test Post", "body": "hello", "userId": 1}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b'{"id":1}'     # truthy so .json() is called
        mock_response.json.return_value = fake_post
        mock_response.raise_for_status.return_value = None  # no exception
        mock_request.return_value = mock_response

        client = JSONPlaceholderClient()
        result = client.get_post(1)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["title"], "Test Post")

    @patch("requests.request")
    def test_create_post_returns_id(self, mock_request):
        """create_post() should return a dict that includes 'id'."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.content = b'{"id":101}'
        mock_response.json.return_value = {"id": 101, "title": "New", "userId": 1}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        client = JSONPlaceholderClient()
        result = client.create_post({"title": "New", "body": "x", "userId": 1})

        self.assertIn("id", result)
        self.assertEqual(result["id"], 101)

    @patch("requests.request")
    def test_get_post_raises_on_404(self, mock_request):
        """get_post() should propagate HTTPError when server returns 404."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error", response=mock_response
        )
        mock_request.return_value = mock_response

        client = JSONPlaceholderClient()

        with self.assertRaises(requests.exceptions.HTTPError):
            client.get_post(9999)


if __name__ == "__main__":
    unittest.main()
```

---

## Q6. Generic Paginator

```python
import requests


class JSONPlaceholderClient:
    """Minimal client used by the paginator."""

    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url.rstrip("/")

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, timeout=10, **kwargs)
        response.raise_for_status()
        return response.json() if response.content else {}


def paginate_all(client, path, page_size=10):
    """Generator that yields items one at a time, fetching pages on demand."""
    page = 1

    while True:
        params = {"_page": page, "_limit": page_size}
        page_data = client._request("GET", path, params=params)

        print(f"Fetching page {page} ... {len(page_data)} items")

        if not page_data:                       # empty page means no more data
            print(f"Fetching page {page} ... 0 items — done.")
            break

        for item in page_data:
            yield item                          # yield one item at a time

        page += 1


if __name__ == "__main__":
    client = JSONPlaceholderClient()

    total = 0
    for post in paginate_all(client, "/posts", page_size=10):
        total += 1

    print(f"Total items yielded: {total}")
```

---

> **Exercises:** → [../../exercises/advanced/exercises.md](../../exercises/advanced/exercises.md)
