# Phase 11 — Beginner Solutions: APIs

> All solutions use JSONPlaceholder (`https://jsonplaceholder.typicode.com`).
> Install the requests library before running: `pip install requests`

---

## Q1. First API Call

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url, timeout=10)        # always set a timeout

print(f"Status: {response.status_code}")

data = response.json()                          # parse JSON body into a dict

print(f"Post id   : {data['id']}")
print(f"Title     : {data['title']}")
print(f"User id   : {data['userId']}")
```

**Explanation:** `requests.get()` sends an HTTP GET request. `.status_code` gives the numeric HTTP status (200 = OK). `.json()` deserialises the response body into a Python dict so you can access fields by name.

---

## Q2. Nested JSON

```python
import requests

url = "https://jsonplaceholder.typicode.com/users/1"

response = requests.get(url, timeout=10)

data = response.json()

# Top-level field
print(f"Name    : {data['name']}")

# Nested field — chain square brackets like nested dicts
print(f"City    : {data['address']['city']}")
print(f"Company : {data['company']['name']}")
```

**Explanation:** JSON objects become Python dicts. Nested objects are just dicts inside dicts. `data["address"]["city"]` first retrieves the `address` dict, then the `city` key inside it.

---

## Q3. Query Parameters

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

# params= is URL-encoded automatically by requests
params = {"userId": 1, "_limit": 3}

response = requests.get(url, params=params, timeout=10)

data = response.json()                          # a list of post dicts

print(f"Posts returned: {len(data)}")

for i, post in enumerate(data, start=1):
    print(f"{i}. {post['title']}")
```

**Explanation:** Passing `params=` tells requests to append `?userId=1&_limit=3` to the URL for you. The response is a JSON array, which `.json()` converts to a Python list.

---

## Q4. Error Check

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/9999"

response = requests.get(url, timeout=10)

# Check status before attempting to parse JSON
if response.status_code == 200:
    data = response.json()
    print(f"Post: {data['title']}")
else:
    # A 404 body may be empty — don't call .json() blindly
    print(f"Error: could not retrieve post. Status code: {response.status_code}")
```

**Explanation:** Always check the status code before calling `.json()`. A 404 response body may be empty or `{}`, so parsing it without checking can produce confusing errors or silent failures.

---

## Q5. Print Formatted Data

```python
import requests

url = "https://jsonplaceholder.typicode.com/todos"
params = {"userId": 1, "_limit": 5}

response = requests.get(url, params=params, timeout=10)

todos = response.json()

print("To-Do List for user 1")
print("=====================")

for item in todos:
    # Ternary: "[x]" if completed, "[ ]" if not
    status = "[x]" if item["completed"] else "[ ]"
    print(f"{status} {item['title']}")
```

**Explanation:** Each item in the response list has `"completed"` (a boolean) and `"title"` (a string). The ternary expression `"[x]" if item["completed"] else "[ ]"` picks the right marker in one line.

---

> **Exercises:** → [../../exercises/beginner/exercises.md](../../exercises/beginner/exercises.md)
