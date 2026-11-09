# Phase 11 — Beginner Exercises: APIs

> Attempt all before checking solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

**Q1. First API Call**

Make a GET request to `https://jsonplaceholder.typicode.com/posts/1`.

- Print the HTTP status code.
- Parse the JSON response and print the `id`, `title`, and `userId` fields.

**Expected output:**
```
Status: 200
Post id   : 1
Title     : sunt aut facere repellat provident occaecati excepturi optio reprehenderit
User id   : 1
```

> **Hints:**
> - `import requests` first.
> - `response = requests.get(url, timeout=10)`
> - `response.status_code` gives the HTTP status.
> - `data = response.json()` parses the body; then access fields like a dict: `data["title"]`.

> **Difficulty:** ⭐ Beginner

---

**Q2. Nested JSON**

Make a GET request to `https://jsonplaceholder.typicode.com/users/1`.

The response contains nested objects. Extract and print:
- The user's name
- Their `address.city`
- Their `company.name`

**Expected output:**
```
Name    : Leanne Graham
City    : Gwenborough
Company : Romaguera-Crona
```

> **Hints:**
> - `data["address"]["city"]` — chain square brackets to reach nested values.
> - `data["company"]["name"]` works the same way.

> **Difficulty:** ⭐ Beginner

---

**Q3. Query Parameters**

Make a GET request to `https://jsonplaceholder.typicode.com/posts` with these query parameters:

```python
params = {"userId": 1, "_limit": 3}
```

Print the number of posts returned and the title of each one.

**Expected output:**
```
Posts returned: 3
1. sunt aut facere repellat provident occaecati excepturi optio reprehenderit
2. qui est esse
3. ea molestiae nihil consequatur fugiat harum ut
```

> **Hints:**
> - Pass `params={"userId": 1, "_limit": 3}` as a keyword argument to `requests.get()`.
> - The library builds `?userId=1&_limit=3` for you automatically.
> - `len(data)` gives the count.

> **Difficulty:** ⭐ Beginner

---

**Q4. Error Check**

Fetch `https://jsonplaceholder.typicode.com/posts/9999` (a post that does not exist).

- Check `response.status_code`.
- If it is not 200, print a friendly error message that includes the status code.

**Expected output:**
```
Error: could not retrieve post. Status code: 404
```

> **Hints:**
> - JSONPlaceholder returns 404 for missing resources.
> - Use `if response.status_code != 200:` to detect the problem.
> - Do NOT call `.json()` on a 404 response — it may return an empty body.

> **Difficulty:** ⭐ Beginner

---

**Q5. Print Formatted Data**

Make a GET request to `https://jsonplaceholder.typicode.com/todos` with params `{"userId": 1, "_limit": 5}`.

Print a formatted to-do list showing the completion status and title of each item.

**Expected output:**
```
To-Do List for user 1
=====================
[ ] delectus aut autem
[ ] quis ut nam facilis et officia qui
[x] fugiat veniam minus
[ ] et porro tempora
[x] laboriosam mollitia et enim quasi adipisci quia provident illum
```

> **Hints:**
> - Each item has `"completed"` (bool) and `"title"` fields.
> - Use `"[x]"` for completed items and `"[ ]"` for incomplete ones.
> - A ternary works cleanly: `"[x]" if item["completed"] else "[ ]"`.

> **Difficulty:** ⭐ Beginner

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
