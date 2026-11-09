# Phase 10 — Quiz 01: Web Scraping

**Questions: 20 | Pass: 16/20 | Time: 20 min**

---

## Section 1: HTTP Basics (Q1–Q5)

**Q1.** A server returns status code `404`. What does this mean?

```
A) The request succeeded and the body contains data
B) The server encountered an internal error
C) The requested resource was not found on the server
D) The client is being rate-limited
```

---

**Q2.** What is the HTTP status code for a permanent redirect?

```
A) 200
B) 301
C) 404
D) 500
```

---

**Q3.** What does a status code of `429` indicate?

```
A) The server is down for maintenance
B) Too many requests — the client is being rate-limited
C) The resource has moved permanently
D) The request body was malformed
```

---

**Q4.** What is the primary difference between HTTP `GET` and `POST` requests?

```
A) GET is faster; POST is slower
B) GET retrieves data without a body; POST sends data in the request body
C) GET is encrypted; POST is plain text
D) GET is for HTML pages only; POST is for APIs only
```

---

**Q5.** What is the purpose of the `User-Agent` request header?

```
A) It provides authentication credentials to the server
B) It tells the server which language the client prefers
C) It identifies the client software making the request
D) It sets the maximum response size the client will accept
```

---

## Section 2: requests Library (Q6–Q10)

**Q6.** What does `response.json()` return?

```
A) A JSON-formatted string
B) A Python dict or list parsed from the JSON response body
C) The raw bytes of the response
D) A BeautifulSoup object
```

---

**Q7.** Which attribute gives you the response body as a decoded string?

```
A) response.content
B) response.body
C) response.data
D) response.text
```

---

**Q8.** What is the correct way to set a custom `User-Agent` header in a `requests.get()` call?

```python
A) requests.get(url, user_agent="MyBot/1.0")
B) requests.get(url, headers={"User-Agent": "MyBot/1.0"})
C) requests.get(url, agent="MyBot/1.0")
D) requests.get(url, meta={"User-Agent": "MyBot/1.0"})
```

---

**Q9.** What is the benefit of using `requests.Session()` instead of plain `requests.get()`?

```
A) It automatically retries failed requests
B) It persists headers, cookies, and TCP connections across multiple requests
C) It parses HTML responses automatically
D) It enforces rate limiting between requests
```

---

**Q10.** What does `response.raise_for_status()` do?

```
A) Prints the status code to the console
B) Returns True if the status is 200, False otherwise
C) Raises an HTTPError exception if the status code is 4xx or 5xx
D) Retries the request if the status indicates an error
```

---

## Section 3: BeautifulSoup (Q11–Q15)

**Q11.** What is the difference between `soup.find("div")` and `soup.find_all("div")`?

```
A) find() searches only the first level; find_all() searches recursively
B) find() returns the first matching tag; find_all() returns a list of all matches
C) find() accepts CSS selectors; find_all() accepts tag names only
D) find() is case-sensitive; find_all() is case-insensitive
```

---

**Q12.** What does `tag.get("href")` do compared to `tag["href"]`?

```
A) They are identical in every way
B) get() returns None if the attribute is missing; ["href"] raises a KeyError
C) get() returns a string; ["href"] returns a list
D) get() is only for input tags; ["href"] works on all tags
```

---

**Q13.** Which CSS selector finds all `<span>` elements with class `"text"` inside a `<div>` with class `"quote"`?

```
A) soup.select("div quote span text")
B) soup.select("div.quote span.text")
C) soup.select("#quote .text")
D) soup.select("div[quote] > span[text]")
```

---

**Q14.** What is the difference between `.text` and `.get_text()` on a BeautifulSoup tag?

```
A) .text raises an error on nested tags; .get_text() handles them
B) They return the same string; .get_text() additionally accepts separator and strip arguments
C) .text decodes bytes; .get_text() decodes strings
D) .text includes HTML; .get_text() strips all markup
```

---

**Q15.** What type does `soup.find("h1")` return when no `<h1>` exists in the document?

```
A) An empty string ""
B) An empty list []
C) None
D) A NavigableString with no content
```

---

## Section 4: Pagination and Ethics (Q16–Q20)

**Q16.** How do you typically detect the "next page" link in a paginated HTML site?

```
A) Count the total number of items and divide by items-per-page
B) Find an anchor tag inside a next/pagination element and read its href
C) Check the response headers for a Link: rel="next" value
D) Call soup.next_page() which is built into BeautifulSoup
```

---

**Q17.** Why should you call `time.sleep(1)` between scraping requests?

```
A) Python requires a sleep between network calls to prevent socket errors
B) It gives your code time to parse the previous response
C) It reduces server load and avoids triggering rate-limit blocks
D) It is required by the HTTP specification
```

---

**Q18.** What is `robots.txt` and why should a scraper check it?

```
A) A file listing all URLs on the site for search engine indexing
B) A plain-text file specifying which paths crawlers are permitted or forbidden to access
C) A configuration file that sets rate limits for API calls
D) An HTML meta tag that blocks automated requests
```

---

**Q19.** Which of the following is considered polite scraping practice?

```
A) Sending requests as fast as possible to finish sooner
B) Removing the User-Agent header so the server cannot identify your script
C) Setting a descriptive User-Agent, respecting robots.txt, and adding delays between requests
D) Scraping only during weekends when server traffic is lower
```

---

**Q20.** A website's Terms of Service explicitly prohibit automated scraping. What should you do?

```
A) Scrape anyway — Terms of Service are not legally enforceable
B) Use a VPN to avoid detection and proceed
C) Do not scrape the site; check whether an official API or data export is available instead
D) Limit your scraper to 10 requests per session to stay under the radar
```

---

## Answers

| Q | Answer | Key Point |
|---|--------|-----------|
| 1 | C | 404 = Not Found — the URL exists on the server but no resource is there |
| 2 | B | 301 = Moved Permanently; 302 = Moved Temporarily |
| 3 | B | 429 = Too Many Requests — server is rate-limiting the client |
| 4 | B | GET has no body; POST sends data in the body |
| 5 | C | User-Agent identifies the client (browser, bot, script) |
| 6 | B | response.json() returns a Python dict/list |
| 7 | D | response.text is the decoded string body |
| 8 | B | Pass a dict to the `headers` keyword argument |
| 9 | B | Session persists headers, cookies, and connections |
| 10 | C | raise_for_status() raises HTTPError on 4xx/5xx |
| 11 | B | find() → first Tag or None; find_all() → list of all matches |
| 12 | B | .get() is safe (returns None); ["attr"] raises KeyError |
| 13 | B | CSS class selector: element.classname; space = descendant |
| 14 | B | Both return the same text; get_text() has extra parameters |
| 15 | C | find() returns None when no match exists — always guard against this |
| 16 | B | Look for `<li class="next"><a href="...">` or similar pagination links |
| 17 | C | Delays reduce server load and prevent rate-limit bans |
| 18 | B | robots.txt defines crawl permissions — checking it is ethical |
| 19 | C | Descriptive UA + robots.txt + delays = polite scraping |
| 20 | C | ToS violations can have legal consequences; use APIs when available |
