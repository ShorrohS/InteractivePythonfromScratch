# Lesson 05 — Building a Simple API Client Class

**Phase:** 11 — APIs | **Time:** ~50 min

---

## Part 1: Why Encapsulate API Logic in a Class?

Calling `requests.get()` inline everywhere works for a quick script.
For anything larger it creates problems:

- **Duplicated auth headers** in every single request
- **Scattered base URLs** — a version bump breaks many files
- **Copy-pasted error handling** — inconsistent across callers
- **No connection reuse** — each call opens a new TCP connection

A client class solves all of these. Configure it once in `__init__`, then every call
to the API goes through the same tested, consistent path.

---

## Part 2: Client Class Design

```python
import requests

class MyAPIClient:
    """Pattern: one class per API, private helpers, one public method per endpoint."""

    def __init__(self, base_url: str, api_key: str = ""):
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
        })
        if api_key:
            self._session.headers.update({"Authorization": f"Bearer {api_key}"})

    def _get(self, path: str, params: dict | None = None) -> dict | list:
        """Private — GET with centralised error handling."""
        ...

    def _post(self, path: str, payload: dict) -> dict:
        """Private — POST with centralised error handling."""
        ...

    def get_user(self, user_id: int) -> dict:
        """Public — one method per logical operation."""
        return self._get(f"/users/{user_id}")

    def close(self) -> None:
        self._session.close()
```

---

## Part 3: Private Helpers — _get() and _post()

Centralise the HTTP call, timeout, and error check in two private methods:

```python
import requests
import time

class BaseAPIClient:
    """Reusable base with shared GET/POST helpers."""

    def __init__(self, base_url: str):
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})

    def _get(self, path: str, params: dict | None = None) -> dict | list:
        """GET request — raises on non-2xx status."""
        url = f"{self._base_url}{path}"
        response = self._session.get(url, params=params, timeout=15)
        self._check(response)
        return response.json()

    def _post(self, path: str, payload: dict) -> dict:
        """POST request — raises on non-2xx status."""
        url = f"{self._base_url}{path}"
        response = self._session.post(url, json=payload, timeout=15)
        self._check(response)
        return response.json()

    def _check(self, response: requests.Response) -> None:
        """Inspect status and raise with a useful message."""
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 5))
            raise RateLimitError(
                f"Rate limited — retry after {retry_after}s"
            )
        response.raise_for_status()

    def close(self) -> None:
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class RateLimitError(Exception):
    """Raised when the API returns 429 Too Many Requests."""
```

---

## Part 4: Rate Limiting and Retry Logic

Transient failures (500, 503) and rate limits (429) are handled with exponential back-off:

```python
import requests
import time

def get_with_retry(
    session: requests.Session,
    url: str,
    max_retries: int = 3,
    **kwargs
) -> requests.Response:
    """
    Retry on transient server errors with exponential back-off.
    Respects the Retry-After header on 429 responses.
    """
    for attempt in range(1, max_retries + 1):
        response = session.get(url, timeout=15, **kwargs)

        if response.status_code == 429:
            wait = int(response.headers.get("Retry-After", 5))
            print(f"Rate limited — waiting {wait}s before retry {attempt}/{max_retries}")
            time.sleep(wait)
            continue

        if response.status_code in (500, 503) and attempt < max_retries:
            wait = 2 ** attempt       # 2s → 4s → 8s (exponential back-off)
            print(f"Server error {response.status_code} — retrying in {wait}s")
            time.sleep(wait)
            continue

        return response

    raise requests.exceptions.RetryError(
        f"Request to {url} failed after {max_retries} retries"
    )
```

---

## Part 5: Complete Example — GitHubClient

GitHub's public API works without authentication for basic reads (60 req/hour).
With a personal access token the limit rises to 5 000 req/hour.

```python
import os
import time
import requests
from typing import Optional

class GitHubClient:
    """
    Simple client for the GitHub REST API v3.
    Pass a personal access token for higher rate limits and private data.
    """

    BASE_URL = "https://api.github.com"

    def __init__(self, token: Optional[str] = None):
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        if token:
            self._session.headers.update({"Authorization": f"Bearer {token}"})

    # ── Private helpers ───────────────────────────────────────────────────────

    def _get(self, path: str, params: dict | None = None) -> dict | list:
        url = f"{self.BASE_URL}{path}"
        for attempt in range(3):
            r = self._session.get(url, params=params, timeout=15)
            if r.status_code in (429, 403):
                wait = int(r.headers.get("Retry-After", 10))
                print(f"Rate limited — sleeping {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f"Failed to GET {url} after retries")

    # ── Public methods ────────────────────────────────────────────────────────

    def get_user(self, username: str) -> dict:
        """Return the public profile for a GitHub user (login, name, public_repos, followers)."""
        return self._get(f"/users/{username}")

    def get_repos(self, username: str, per_page: int = 30) -> list[dict]:
        """List public repos for a user, sorted by most recently pushed."""
        return self._get(
            f"/users/{username}/repos",
            params={"per_page": per_page, "sort": "pushed"}
        )

    def search_repos(self, query: str, sort: str = "stars") -> list[dict]:
        """Search GitHub repos. sort can be 'stars', 'forks', or 'updated'."""
        data = self._get(
            "/search/repositories",
            params={"q": query, "sort": sort}
        )
        return data.get("items", [])

    def close(self) -> None:
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


# ── Usage ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")   # optional — works without it too

    with GitHubClient(token=token) as client:
        # Fetch a public profile
        user = client.get_user("torvalds")
        print(f"Name:         {user['name']}")
        print(f"Public repos: {user['public_repos']}")
        print(f"Followers:    {user['followers']}")

        # List their most recently pushed repos
        repos = client.get_repos("torvalds", per_page=5)
        for repo in repos:
            print(f"  {repo['name']:30} ⭐ {repo['stargazers_count']}")
```

---

## Part 6: Typed Response Objects

For larger projects, add type safety with `dataclass` (or `TypedDict` for plain dicts):

```python
from dataclasses import dataclass

@dataclass
class Repo:
    name: str
    full_name: str
    stars: int
    language: str | None

    @classmethod
    def from_api(cls, data: dict) -> "Repo":
        """Build a Repo from a raw API response dict."""
        return cls(
            name=data["name"],
            full_name=data["full_name"],
            stars=data.get("stargazers_count", 0),
            language=data.get("language"),
        )

with GitHubClient() as client:
    raw_repos = client.get_repos("torvalds", per_page=10)
    repos = [Repo.from_api(r) for r in raw_repos]
    for r in repos:
        print(f"{r.full_name} — {r.stars} stars — {r.language}")
```

---

## Practice Exercises

1. Extend `GitHubClient` with a `get_repo(owner, repo)` method that calls
   `GET /repos/{owner}/{repo}` and returns a `Repo` dataclass instance.

2. Add a `get_user_events(username, max_pages)` method that paginates through
   `GET /users/{username}/events` (up to 30 events per page) and returns a flat
   list of all events across up to `max_pages` pages.

3. Add a simple in-memory cache to `get_user()`: store results in a `dict` on `self`
   and return the cached value on repeated calls for the same username.

4. Create a `JSONPlaceholderClient` (base URL `https://jsonplaceholder.typicode.com`)
   with methods: `get_posts(user_id=None)`, `create_post(title, body, user_id)`,
   and `delete_post(post_id)`. Use a `Session` and the `_get`/`_post` pattern.

---

## Next Lesson

**[Lesson 06 → Building a REST API with Flask](lesson-06-flask-api.md)**
