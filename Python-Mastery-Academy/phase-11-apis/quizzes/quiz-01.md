# Phase 11 — Quiz 01: APIs

**Questions: 20 | Pass: 16/20 | Time: 20 min**

---

## Section 1: HTTP Methods and Status Codes (Q1–Q5)

**Q1.** Which HTTP method is used to retrieve a resource without modifying it?
`A) POST  B) PUT  C) GET  D) DELETE`

---

**Q2.** What status code does a successful POST request that creates a new resource typically return?
`A) 200 OK  B) 201 Created  C) 204 No Content  D) 301 Moved Permanently`

---

**Q3.** Which status code means the client sent an invalid or malformed request?
`A) 401  B) 403  C) 400  D) 500`

---

**Q4.** Which HTTP method is considered idempotent — meaning calling it multiple times with the same data produces the same result?
`A) POST  B) PUT  C) Both POST and PUT  D) Neither`

---

**Q5.** What does a `429 Too Many Requests` response tell a client to do?
`A) Retry immediately  B) Switch to a different endpoint  C) Slow down — rate limit exceeded  D) Re-authenticate`

---

## Section 2: requests Library (Q6–Q10)

**Q6.** What does `response.status_code` return?
`A) A string like "200 OK"  B) An integer like 200  C) A boolean  D) The response body`

---

**Q7.** What is the difference between passing `params={"q": "python"}` and `data={"q": "python"}` to `requests.get()`?
`A) No difference  B) params= appends to the URL as a query string; data= sends a request body  C) data= is for GET; params= is for POST  D) params= sends JSON; data= sends form data`

---

**Q8.** Which call correctly sends a JSON body in a POST request?
```
A) requests.post(url, body={"key": "val"})
B) requests.post(url, json={"key": "val"})
C) requests.post(url, data={"key": "val"})
D) requests.post(url, payload={"key": "val"})
```

---

**Q9.** What does `response.raise_for_status()` do?
`A) Always raises an exception  B) Raises HTTPError only on 4xx or 5xx status codes  C) Returns the status code as an integer  D) Retries the request on failure`

---

**Q10.** When should you use a `requests.Session` instead of calling `requests.get()` directly?
`A) Never — Sessions are for advanced users only  B) When making multiple requests to the same host, to reuse connections and share headers/cookies  C) Only when you need authentication  D) When using HTTPS`

---

## Section 3: Auth and Headers (Q11–Q15)

**Q11.** What is the correct format for a Bearer token in an Authorization header?
`A) Authorization: fake-token  B) Authorization: Token fake-token  C) Authorization: Bearer fake-token  D) Auth: Bearer fake-token`

---

**Q12.** How do you add a custom header to a `requests.get()` call?
```
A) requests.get(url, header={"X-API-Key": "abc"})
B) requests.get(url, headers={"X-API-Key": "abc"})
C) requests.get(url, auth={"X-API-Key": "abc"})
D) requests.get(url).add_header("X-API-Key", "abc")
```

---

**Q13.** Which content type header must be set when sending a JSON body?
`A) Content-Type: text/plain  B) Content-Type: application/xml  C) Content-Type: application/json  D) Content-Type: multipart/form-data`

---

**Q14.** How do you send HTTP Basic Auth with the requests library?
`A) headers={"Authorization": "Basic user:pass"}  B) auth=("username", "password")  C) basic_auth=("username", "password")  D) credentials=("username", "password")`

---

**Q15.** An API requires an API key sent as a query parameter `?api_key=abc123`. How do you include it?
`A) headers={"api_key": "abc123"}  B) params={"api_key": "abc123"}  C) json={"api_key": "abc123"}  D) auth=("api_key", "abc123")`

---

## Section 4: JSON and Advanced (Q16–Q20)

**Q16.** What is the difference between `json.loads(text)` and `response.json()`?
`A) No difference  B) json.loads() parses a JSON string; response.json() decodes the response body automatically  C) response.json() is faster  D) json.loads() only works with files`

---

**Q17.** Given this JSON response, how do you access the city?
```python
data = {
    "name": "Alice",
    "address": {"city": "London", "zip": "EC1A"}
}
```
`A) data["city"]  B) data["address.city"]  C) data["address"]["city"]  D) data.address.city`

---

**Q18.** Which pattern correctly handles pagination until the API returns an empty page?
```
A) for page in range(100): fetch(page)
B) while True: page = fetch(); if not page: break
C) fetch(page=1); fetch(page=2)
D) page = fetch_all()
```

---

**Q19.** An API returns `429` with a `Retry-After: 30` header. What should your code do?
`A) Switch to a different API  B) Raise an exception immediately  C) Sleep for 30 seconds then retry  D) Ignore it and retry right away`

---

**Q20.** Which is the best reason to wrap API calls in a client class?
`A) Classes are always faster than functions  B) To centralise URL building, auth headers, and error handling in one place  C) To avoid using the requests library  D) Python requires it for making HTTP calls`

---

## Answers

| Q | Answer | Key Point |
|---|--------|-----------|
| 1 | C | GET is the read-only method — it never modifies server state |
| 2 | B | 201 Created signals a new resource was made |
| 3 | C | 400 Bad Request — malformed syntax or invalid input from the client |
| 4 | B | PUT is idempotent; POST creates a new resource each time |
| 5 | C | 429 means you are sending requests too fast — back off and retry |
| 6 | B | status_code is an integer (200, 404, etc.) |
| 7 | B | params= builds the query string; data= sends a form-encoded body |
| 8 | B | json= serialises the dict and sets Content-Type: application/json |
| 9 | B | raise_for_status() is a no-op on 2xx; raises HTTPError on 4xx/5xx |
| 10 | B | Sessions reuse TCP connections and share cookies/headers across calls |
| 11 | C | The standard format is `Authorization: Bearer <token>` |
| 12 | B | headers= (plural) is the correct keyword argument |
| 13 | C | JSON APIs expect Content-Type: application/json |
| 14 | B | requests handles Basic Auth encoding with auth=("user", "pass") |
| 15 | B | API key as query parameter goes in params= |
| 16 | B | response.json() is a shortcut for json.loads(response.text) |
| 17 | C | Chain square brackets to navigate nested dicts |
| 18 | B | while True with a break on empty page is the standard pattern |
| 19 | C | Honour Retry-After — sleep the specified seconds before retrying |
| 20 | B | A client class is a reusability and maintainability pattern |
