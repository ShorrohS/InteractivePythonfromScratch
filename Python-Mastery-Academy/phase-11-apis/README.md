# 🔗 Phase 11 — APIs

> **Goal:** Consume REST APIs to get real-world data in your Python programs.

---

## What is an API?

An API (Application Programming Interface) is a way for programs to talk to each other over the internet.

**Analogy:** You're at a restaurant. You (client) tell the waiter (API) what you want. The waiter goes to the kitchen (server) and brings back your food (data).

---

## HTTP Methods

| Method | Use Case |
|--------|---------|
| `GET` | Retrieve data |
| `POST` | Create new data |
| `PUT` | Update/replace data |
| `PATCH` | Partially update data |
| `DELETE` | Delete data |

---

## Lessons

| # | Lesson | Topic |
|---|--------|-------|
| 01 | [lesson-01-http.md](concepts/lesson-01-http.md) | HTTP fundamentals |
| 02 | [lesson-02-requests.md](concepts/lesson-02-requests.md) | Python requests library |
| 03 | [lesson-03-json.md](concepts/lesson-03-json.md) | Working with JSON responses |
| 04 | [lesson-04-auth.md](concepts/lesson-04-auth.md) | API authentication |

---

## Core Skills

```python
import requests

# Basic GET request
response = requests.get("https://api.example.com/data")
print(response.status_code)   # 200 = OK
print(response.json())         # Parse JSON response

# With parameters
params = {"city": "London", "units": "metric"}
response = requests.get("https://api.weather.com/v1/current", params=params)

# With headers (authentication)
headers = {"Authorization": "Bearer YOUR_API_KEY"}
response = requests.get("https://api.example.com/protected", headers=headers)

# POST request
payload = {"name": "Alice", "email": "alice@example.com"}
response = requests.post("https://api.example.com/users", json=payload)

# Error handling
if response.status_code == 200:
    data = response.json()
elif response.status_code == 401:
    print("Unauthorized — check your API key")
elif response.status_code == 404:
    print("Resource not found")
else:
    print(f"Error: {response.status_code}")
```

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 429 | Too Many Requests |
| 500 | Server Error |

---

## Guided Projects

| Project | Description |
|---------|-------------|
| [Weather Dashboard](guided-projects/project-01-weather-dashboard/) | OpenWeatherMap API |

---

## Installation

```bash
pip install requests
pip freeze > requirements.txt
```

---

## ✅ Completion Checklist

- [ ] Understand GET, POST, PUT, DELETE
- [ ] Can make requests with parameters and headers
- [ ] Can parse JSON responses
- [ ] Handle HTTP errors gracefully
- [ ] Built Weather Dashboard or equivalent

---

## Previous: [Phase 10](../phase-10-web-scraping/README.md) | Next: [Phase 12](../phase-12-automation/README.md)
