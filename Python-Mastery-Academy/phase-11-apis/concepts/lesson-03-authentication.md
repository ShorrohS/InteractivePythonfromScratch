# Lesson 03 — Authentication: API Keys, Headers, Bearer Tokens

**Phase:** 11 — APIs | **Time:** ~40 min

---

## Part 1: Why APIs Require Authentication

Authentication proves who is making the request. APIs use it to:
- Identify callers and enforce **rate limits** per account
- Control **access** — some endpoints require a paid plan or elevated permissions
- Provide an **audit trail** of who accessed what data and when
- **Protect** private user data from unauthorized reads

An unauthenticated call either returns `401 Unauthorized` or is limited to a very small
public quota (e.g. GitHub allows only 60 requests per hour without a token).

---

## Part 2: API Key as a Query Parameter

The simplest pattern — append the key directly to the URL:

```python
import requests
import os

# Load key from environment — never hardcode (see Part 7)
API_KEY = os.getenv("OPENWEATHER_KEY", "YOUR_KEY_HERE")

url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": "London",
    "units": "metric",
    "appid": API_KEY           # key travels in the query string
}
response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

data = response.json()
print(f"Temperature: {data['main']['temp']}°C")
print(f"Conditions:  {data['weather'][0]['description']}")
```

**Downside:** the key appears in server logs and browser history because it is in the URL.
Prefer header-based auth when the API supports it.

---

## Part 3: API Key in Request Headers

A safer approach — send the key in a header so it never appears in the URL:

```python
import requests
import os

API_KEY = os.getenv("MY_API_KEY")

# Pattern 1: X-API-Key header (many public APIs use this exact name)
headers = {"X-API-Key": API_KEY}
response = requests.get("https://some-api.com/data", headers=headers, timeout=10)

# Pattern 2: Authorization header without a scheme (some APIs)
headers = {"Authorization": API_KEY}
response = requests.get("https://some-api.com/data", headers=headers, timeout=10)

# With a Session — set the header once, it applies to every request
with requests.Session() as session:
    session.headers.update({"X-API-Key": API_KEY})

    r1 = session.get("https://some-api.com/users", timeout=10)
    r2 = session.get("https://some-api.com/orders", timeout=10)
    r3 = session.get("https://some-api.com/products", timeout=10)
```

---

## Part 4: Bearer Tokens

Bearer tokens are the most common auth scheme for modern APIs (GitHub, Twitter/X, Stripe).
The header value must be the literal word `Bearer` followed by a space and the token:

```python
import requests
import os

TOKEN = os.getenv("GITHUB_TOKEN")   # personal access token from GitHub settings

headers = {"Authorization": f"Bearer {TOKEN}"}
response = requests.get(
    "https://api.github.com/user",  # returns YOUR profile when authenticated
    headers=headers,
    timeout=10
)
response.raise_for_status()

user = response.json()
print(f"Logged in as: {user['login']}")
print(f"Name:         {user.get('name', 'not set')}")
print(f"Private repos:{user.get('total_private_repos', 0)}")
```

Bearer tokens are often short-lived (minutes to hours). When they expire you must request a
new one from the token endpoint. OAuth 2.0 automates that refresh cycle for you.

---

## Part 5: Basic Authentication

Basic auth sends a username and password encoded in the `Authorization` header.
`requests` handles the encoding automatically:

```python
import requests
from requests.auth import HTTPBasicAuth

# Shorthand tuple — requests base64-encodes it for you
response = requests.get(
    "https://httpbin.org/basic-auth/alice/secret",
    auth=("alice", "secret"),          # (username, password)
    timeout=10
)
print(response.status_code)            # 200 if credentials are correct
print(response.json())

# Explicit class — same result, clearer intent
response = requests.get(
    "https://httpbin.org/basic-auth/alice/secret",
    auth=HTTPBasicAuth("alice", "secret"),
    timeout=10
)
print(response.json()["authenticated"])  # True
```

Basic auth is rarely used for public APIs today but is common for internal services,
CI pipelines, and legacy systems.

---

## Part 6: OAuth 2.0 — What It Is

OAuth 2.0 is an authorization framework rather than a direct key system.
You encounter it when an app says "Connect with Google" or "Login with GitHub".

**The high-level flow:**
1. Your app redirects the user to the provider's auth page
2. The user logs in and approves the permissions your app requested
3. The provider redirects back to your app with a short-lived **authorization code**
4. Your app exchanges the code for an **access token** (and usually a refresh token)
5. Your app uses the access token as a Bearer token in all subsequent API calls
6. When the access token expires, the refresh token gets you a new one silently

OAuth 2.0 is complex to implement from scratch.
Use a library — `authlib` or `requests-oauthlib` — rather than building the flow manually.

---

## Part 7: Security Best Practices — Environment Variables

**Never hardcode credentials in source code.**
If you commit a key to git, it is compromised — even if you delete it in a later commit,
the history is permanent and bots scan GitHub continuously for leaked keys.

```python
import os
import requests

# BAD — key is visible in source and version control history
API_KEY = "sk-abc123xyz"   # do not do this

# GOOD — read from the environment at runtime
API_KEY = os.environ.get("MY_API_KEY")
if not API_KEY:
    raise RuntimeError(
        "MY_API_KEY environment variable is not set. "
        "Export it before running this script."
    )

response = requests.get(
    "https://some-api.com/data",
    headers={"X-API-Key": API_KEY},
    timeout=10
)
```

**Set environment variables in your shell:**

```bash
# macOS / Linux
export MY_API_KEY="your-key-here"

# Windows PowerShell
$env:MY_API_KEY = "your-key-here"
```

---

## Part 8: .env Files and python-dotenv

For local development, a `.env` file is more convenient than setting shell variables
in every terminal session:

```bash
# .env  — NEVER commit this file; add it to .gitignore immediately
MY_API_KEY=your-key-here
OPENWEATHER_KEY=another-key
GITHUB_TOKEN=ghp_yourtokenhere
```

```python
from dotenv import load_dotenv
import os
import requests

load_dotenv()   # reads .env and injects values into os.environ

API_KEY = os.getenv("MY_API_KEY")             # None if variable is missing
WEATHER_KEY = os.getenv("OPENWEATHER_KEY", "fallback-value")

print(API_KEY)  # value from .env — never hardcoded in the source file
```

Install the library:

```bash
pip install python-dotenv
```

**.gitignore** — add this line before your first commit to prevent accidental exposure:

```
.env
```

---

## Practice Exercises

1. Using `os.getenv()`, write a short script that reads `API_KEY` from the environment,
   raises a `RuntimeError` with a helpful message if it is missing, and prints the key
   with only the last 4 characters visible (e.g. `****xyz`).

2. Create a `.env` file containing `GITHUB_TOKEN=fake_test_value` and a Python script
   that uses `python-dotenv` to load it and prints the value. Add `.env` to `.gitignore`.

3. What is the difference between `401 Unauthorized` and `403 Forbidden`?
   Write a function `check_auth_error(response)` that inspects `response.status_code`
   and prints a specific, helpful message for 401, 403, and 429.

4. Look up the GitHub REST API endpoint `GET /repos/{owner}/{repo}`.
   Write a request that sends a Bearer token loaded from an environment variable.
   Print the repo's star count (`stargazers_count`) and open issue count (`open_issues_count`).

---

## Next Lesson

**[Lesson 04 → Parsing and Processing JSON Responses](lesson-04-parsing-json.md)**
