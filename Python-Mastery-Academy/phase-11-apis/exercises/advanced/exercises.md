# Phase 11 — Advanced Exercises: APIs

> These exercises tackle production-level patterns: client class design, retry logic, caching, and mock testing.
> Plan your class structure before writing any code.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. API Client Class**

Design a reusable `JSONPlaceholderClient` class that wraps the JSONPlaceholder API.

Requirements:
- `__init__(self, base_url, api_key=None)` — store base URL and optional API key
- `_request(self, method, path, **kwargs)` — internal method that:
  - Prepends `base_url` to `path`
  - Adds `Authorization: Bearer <api_key>` header if an `api_key` was provided
  - Always passes `timeout=10`
  - Calls `response.raise_for_status()` to raise on 4xx/5xx
  - Returns the parsed JSON (or `{}` for empty bodies)
- `get_post(self, post_id)` — GET `/posts/{id}`
- `create_post(self, data)` — POST `/posts`
- `update_post(self, post_id, data)` — PUT `/posts/{id}`
- `delete_post(self, post_id)` — DELETE `/posts/{id}`

Demonstrate the client by calling each method once and printing the result.

> **Hints:**
> - `requests.request(method, url, **kwargs)` dispatches any HTTP verb.
> - Guard `.json()` with `if response.content:` to avoid errors on 204/empty bodies.
> - Pass `headers={...}` inside `**kwargs` so callers can add extra headers.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q2. Retry with Exponential Backoff**

Add a `_request_with_retry(self, method, path, max_retries=3, **kwargs)` method to your client.

Behavior:
- On a successful response, return immediately.
- On `429 Too Many Requests` or any `5xx` server error, wait and retry.
- Delay doubles each attempt: 1 s → 2 s → 4 s (exponential backoff).
- After `max_retries` exhausted, re-raise the last exception.
- Print a message for each retry attempt.

Use `unittest.mock.patch` to simulate a 429 response for the first two calls, then a 200 on the third, to prove the retry logic works without making real failed requests.

> **Hints:**
> - `response.raise_for_status()` raises `requests.exceptions.HTTPError` — catch that.
> - `response.status_code` is available on the exception via `e.response.status_code`.
> - `time.sleep(delay)` pauses execution; `delay *= 2` doubles it.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q3. Rate Limit Header Awareness**

After every API response, inspect the `X-RateLimit-Remaining` response header.

- If the header is present and its value is below `10`, print a warning and sleep for `60` seconds before the next request.
- If the header is absent (JSONPlaceholder does not send it), print `"Rate limit header not present — no throttling needed."`.

Simulate the throttling by building a small test harness:
1. Create a mock response object where `headers = {"X-RateLimit-Remaining": "3"}`.
2. Pass it through a `check_rate_limit(response)` function.
3. Confirm it prints the warning (without actually sleeping 60 s — use a mock for `time.sleep`).

> **Hints:**
> - `response.headers.get("X-RateLimit-Remaining")` returns `None` if absent.
> - Convert the header value to `int()` before comparing.
> - Mock `time.sleep` with `unittest.mock.patch("time.sleep")` to keep tests fast.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q4. SQLite Response Cache**

Wrap GET requests to `/posts/{id}` in a local SQLite cache to avoid redundant network calls.

Requirements:
- On first call: fetch from API, store `(post_id, json_text)` in a `cache` table, print `MISS`.
- On subsequent calls with the same `post_id`: read from DB, print `HIT`.
- The cache should persist between runs (use a file, not `:memory:`).

Demonstrate by fetching post 1 twice and post 2 once, then printing the HIT/MISS log.

**Expected output:**
```
MISS — fetched post 1 from API
HIT  — loaded post 1 from cache
MISS — fetched post 2 from API
```

> **Hints:**
> - `import sqlite3`; `conn = sqlite3.connect("posts_cache.db")`.
> - Create table: `CREATE TABLE IF NOT EXISTS cache (post_id INTEGER PRIMARY KEY, data TEXT)`.
> - `json.dumps(data)` to store; `json.loads(row[0])` to retrieve.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q5. Mock Testing**

Write a `unittest.TestCase` that verifies your `JSONPlaceholderClient` behaves correctly without making real HTTP calls.

Requirements — write at least these three test methods:
- `test_get_post_returns_correct_data` — mock `requests.request` to return a fake post; assert the returned dict matches.
- `test_create_post_returns_id` — mock a 201 response; assert the returned dict contains `"id"`.
- `test_get_post_raises_on_404` — mock a 404 response that raises `HTTPError`; assert the client propagates it.

All tests must pass with `python -m unittest`.

> **Hints:**
> - `@patch("requests.request")` decorates the test method; the mock is passed as an argument.
> - Set `mock_response.json.return_value = {...}` and `mock_response.status_code = 200`.
> - For the 404 test: `mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError`.

> **Difficulty:** ⭐⭐⭐ Advanced

---

**Q6. Generic Paginator**

Write a `paginate_all(client, path, page_size=10)` generator function that:

- Starts at `_page=1`.
- Fetches one page at a time using `client._request("GET", path, params={"_page": page, "_limit": page_size})`.
- Yields each item individually (not the whole page at once).
- Stops when the API returns an empty list (no more data).

Use it to iterate through all 100 posts from JSONPlaceholder and print the total count.

**Expected output:**
```
Fetching page 1 ... 10 items
Fetching page 2 ... 10 items
...
Fetching page 10 ... 10 items
Fetching page 11 ... 0 items — done.
Total items yielded: 100
```

> **Hints:**
> - A generator uses `yield item` inside a `for item in page:` loop.
> - The loop condition is `while True:`, broken with `if not page_data: break`.
> - Keep a `page` counter and increment it after each successful fetch.

> **Difficulty:** ⭐⭐⭐ Advanced

---

> **Solutions:** → [../../solutions/advanced/solutions.md](../../solutions/advanced/solutions.md)
