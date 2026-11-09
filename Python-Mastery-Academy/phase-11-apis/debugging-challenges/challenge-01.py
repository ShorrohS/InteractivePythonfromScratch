"""
Debugging Challenge 01 — Phase 11: APIs
========================================

INSTRUCTIONS:
  7 bugs are hidden in this file.
  All relate to common mistakes when working with the requests library and REST APIs.
  Find and fix each one.
  When all are fixed, the program runs and prints correct output.

  pip install requests   (if not already installed)
  Run: python challenge-01.py
"""

import requests
import json

print("=" * 55)
print("DEBUGGING CHALLENGE 01 — APIs")
print("=" * 55)

BASE_URL = "https://jsonplaceholder.typicode.com"


# ============================================================
# BUG 1 — Wrong HTTP method
# Should be POST to create a resource, not GET
# ============================================================
print("\nBug 1 - Create a post:")
payload = {"title": "Hello API", "body": "Learning Python APIs", "userId": 1}
response = requests.get(BASE_URL + "/posts", json=payload, timeout=10)   # BUG: should be requests.post(...)
print(f"  Status: {response.status_code}")
data = response.json()
if isinstance(data, list):
    print("  ERROR: GET returned a list instead of creating a post!")
else:
    print(f"  Created post id: {data.get('id')}")


# ============================================================
# BUG 2 — Wrong body kwarg
# data=payload sends form-encoded data, not JSON
# Should be json=payload
# ============================================================
print("\nBug 2 - POST with JSON body:")
new_payload = {"title": "Test", "body": "body text", "userId": 2}
response = requests.post(BASE_URL + "/posts", data=new_payload, timeout=10)  # BUG: should be json=new_payload
print(f"  Status: {response.status_code}")
# With data= the server receives form-encoded text, not JSON — returned id may still work
# on JSONPlaceholder but a real API would reject it
result = response.json()
print(f"  Response id: {result.get('id')}")


# ============================================================
# BUG 3 — Forgot to call .json()
# Printing the Response object gives something like <Response [200]>
# ============================================================
print("\nBug 3 - Print the post title:")
response = requests.get(BASE_URL + "/posts/1", timeout=10)
data = response                      # BUG: should be response.json()
# This will fail with a TypeError or print the wrong thing
try:
    print(f"  Title: {data['title']}")
except TypeError:
    print("  ERROR: forgot to call .json() — got a Response object, not a dict")


# ============================================================
# BUG 4 — Wrong JSON key (case-sensitive)
# JSON keys from this API are lowercase; "Title" does not exist
# ============================================================
print("\nBug 4 - Access the title field:")
response = requests.get(BASE_URL + "/posts/1", timeout=10)
response_data = response.json()
title = response_data.get("Title")          # BUG: key is "title" (lowercase)
if title is None:
    print("  ERROR: key 'Title' not found — JSON keys are case-sensitive!")
else:
    print(f"  Title: {title}")


# ============================================================
# BUG 5 — Auth header missing "Bearer " prefix
# The standard format is "Bearer <token>", not just the raw token
# ============================================================
print("\nBug 5 - Send Authorization header:")
token = "my-secret-token-abc"
headers = {
    "Authorization": token          # BUG: should be f"Bearer {token}"
}
response = requests.get("https://httpbin.org/headers", headers=headers, timeout=10)
echoed = response.json()["headers"].get("Authorization", "")
if not echoed.startswith("Bearer "):
    print(f"  WARNING: Authorization sent as '{echoed}' — missing 'Bearer ' prefix")
else:
    print(f"  Authorization header: {echoed}")


# ============================================================
# BUG 6 — No error check before accessing JSON
# If the resource does not exist (404), calling .json()["id"] will KeyError
# Always check status_code first
# ============================================================
print("\nBug 6 - Fetch non-existent post:")
response = requests.get(BASE_URL + "/posts/9999", timeout=10)
# BUG: no status check — if 404, response.json() may return {} and ["id"] will KeyError
try:
    post_id = response.json()["id"]         # BUG: should check status_code first
    print(f"  Post id: {post_id}")
except KeyError:
    print(f"  ERROR: no 'id' in response — status was {response.status_code}. "
          f"Check status_code before parsing!")


# ============================================================
# BUG 7 — Missing timeout
# Without a timeout, the call hangs forever if the server is slow
# ============================================================
print("\nBug 7 - Missing timeout:")
# BUG: no timeout= argument — can hang indefinitely
response = requests.get(BASE_URL + "/posts/2")   # BUG: add timeout=10
print(f"  Status: {response.status_code}")
print(f"  Title: {response.json()['title']}")


print("\n" + "=" * 55)
print("Fixed all 7 bugs? The output should be logical and complete.")
print("=" * 55)


# ============================================================
# ANSWER KEY
# ============================================================
#
# Bug 1: Change requests.get(...) → requests.post(...)
#        GET does not create resources; POST does.
#
# Bug 2: Change data=new_payload → json=new_payload
#        data= sends form-encoded text; json= sends JSON with the
#        correct Content-Type: application/json header.
#
# Bug 3: Change data = response → data = response.json()
#        response is a Response object; calling .json() returns the
#        parsed dict/list you can index into.
#
# Bug 4: Change response_data.get("Title") → response_data.get("title")
#        JSON keys from this API are lowercase. Python dict lookups
#        are case-sensitive.
#
# Bug 5: Change "Authorization": token → "Authorization": f"Bearer {token}"
#        The OAuth 2.0 Bearer token format requires the "Bearer " prefix.
#
# Bug 6: Add a status check before parsing:
#        if response.status_code == 200:
#            post_id = response.json()["id"]
#        else:
#            print(f"Error: {response.status_code}")
#
# Bug 7: Add timeout=10:
#        requests.get(BASE_URL + "/posts/2", timeout=10)
#        Without a timeout the request can hang forever if the server
#        is unreachable or slow.
