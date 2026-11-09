# Phase 11 — Intermediate Exercises: APIs

> These exercises require complete programs involving POST, PUT, DELETE, authentication, pagination, and file I/O.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. POST Request**

Send a POST request to `https://jsonplaceholder.typicode.com/posts` to create a new post.

Use this payload:
```python
payload = {
    "title": "Learning APIs with Python",
    "body": "The requests library makes it easy to call REST APIs.",
    "userId": 1
}
```

Print the status code and the `id` of the newly created resource.

**Expected output:**
```
Status: 201
Created post with id: 101
```

> **Hints:**
> - Use `requests.post(url, json=payload, timeout=10)` — passing `json=` automatically sets the `Content-Type: application/json` header.
> - JSONPlaceholder returns 201 Created on success, not 200.
> - The created resource is in `response.json()["id"]`.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q2. PUT Request**

Send a PUT request to `https://jsonplaceholder.typicode.com/posts/1` to replace the post entirely.

Use this updated body:
```python
updated = {
    "id": 1,
    "title": "Updated Title",
    "body": "This post has been fully replaced.",
    "userId": 1
}
```

Print the status code and confirm the response reflects your updated title.

**Expected output:**
```
Status: 200
Updated title: Updated Title
```

> **Hints:**
> - Use `requests.put(url, json=updated, timeout=10)`.
> - PUT replaces the entire resource; use PATCH for partial updates.
> - Access the returned title with `response.json()["title"]`.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q3. DELETE Request**

Send a DELETE request to `https://jsonplaceholder.typicode.com/posts/1`.

Print the status code and a confirmation message.

**Note:** JSONPlaceholder simulates deletion — it always returns `200 OK` with an empty JSON body `{}` rather than actually removing data. This is normal behavior for a fake API.

**Expected output:**
```
Status: 200
Post deleted (simulated). Response body: {}
```

> **Hints:**
> - Use `requests.delete(url, timeout=10)`.
> - A real API often returns 204 No Content with an empty body on deletion.
> - `response.json()` will return `{}` here.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q4. Auth Header**

Build a GET request that includes a custom `Authorization` header, then verify the header was sent.

Steps:
1. Make a GET request to `https://httpbin.org/headers` with the header `Authorization: Bearer fake-token-12345`.
2. Parse the response and print the value of the `Authorization` header that httpbin echoes back.

**Expected output:**
```
Authorization header sent: Bearer fake-token-12345
```

> **Hints:**
> - Pass `headers={"Authorization": "Bearer fake-token-12345"}` to `requests.get()`.
> - httpbin echoes all received headers inside `response.json()["headers"]`.
> - The key in the echoed dict is `"Authorization"`.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q5. Pagination**

JSONPlaceholder supports pagination via `_page` and `_limit` query parameters.

Fetch posts in two pages (10 posts per page) and collect them all into one list:
- Page 1: `GET /posts?_page=1&_limit=10`
- Page 2: `GET /posts?_page=2&_limit=10`

Print the total number of posts collected and the title of the last post.

**Expected output:**
```
Total posts collected: 20
Last post title: doloremque ullam ut sint nisi voluptatem omnis debitis in
```

> **Hints:**
> - Make two separate requests, each with the appropriate `params` dict.
> - Combine with `all_posts = page1_data + page2_data`.
> - `len(all_posts)` gives the total; `all_posts[-1]["title"]` gives the last title.

> **Difficulty:** ⭐⭐ Intermediate

---

**Q6. Save Response to File**

Fetch all posts from `https://jsonplaceholder.typicode.com/posts`, filter to only those where `userId == 1`, and save the filtered list to a file named `posts_user1.json`.

Print how many posts were saved.

**Expected output:**
```
Total posts fetched: 100
Posts for userId=1: 10
Saved to posts_user1.json
```

> **Hints:**
> - `import json` and use `json.dump(filtered, f, indent=2)` to write.
> - Filter with a list comprehension: `[p for p in data if p["userId"] == 1]`.
> - Open the file with `open("posts_user1.json", "w")`.

> **Difficulty:** ⭐⭐ Intermediate

---

> **Solutions:** → [../../solutions/intermediate/solutions.md](../../solutions/intermediate/solutions.md)
