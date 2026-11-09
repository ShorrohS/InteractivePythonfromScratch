# Phase 16 — Quiz 01: Web Development with Flask

**Questions:** 18 | **Pass:** 14/18 | **Time:** 20 min (no notes)

---

## Section 1: HTTP Concepts (Q1–Q3)

**Q1.** A browser visits `http://example.com/users/42`. Which part is the **path**?
```
A) http
B) example.com
C) /users/42
D) 42
```

**Q2.** Which HTTP method is conventionally used to **create** a new resource?
```
A) GET
B) DELETE
C) POST
D) HEAD
```

**Q3.** A server responds with status code **404**. What does that mean?
```
A) The request was malformed
B) The server had an internal error
C) The requested resource was not found
D) The request succeeded with no content
```

---

## Section 2: Flask Routing (Q4–Q7)

**Q4.** What URL does this route handle?
```python
@app.route("/users/<int:user_id>")
def get_user(user_id):
    return str(user_id)
```
```
A) /users/<int:user_id>
B) /users/42  (and any other integer after /users/)
C) Only /users/1
D) /users/  with query parameter user_id
```

**Q5.** A route is decorated with `@app.route("/items")`. What HTTP method does it accept by default?
```
A) POST
B) GET and POST
C) GET
D) All methods
```

**Q6.** What is the output when a client visits `/hello/world`?
```python
@app.route("/hello/<name>")
def hello(name):
    return f"Hi, {name.upper()}!"
```
```
A) Hi, name!
B) Hi, world!
C) Hi, WORLD!
D) 404 Not Found
```

**Q7.** Which decorator registers a function to run **before every request** in Flask?
```
A) @app.before_request
B) @app.setup
C) @app.on_request
D) @app.middleware
```

---

## Section 3: Templates (Q8–Q10)

**Q8.** In Jinja2, which syntax outputs the value of a variable called `title`?
```
A) %title%
B) ${title}
C) {{title}}
D) <% title %>
```

**Q9.** What does this Jinja2 snippet render if `items = ["apple", "banana"]`?
```jinja
{% for item in items %}
  <li>{{ item }}</li>
{% endfor %}
```
```
A) <li>items</li>
B) <li>apple</li><li>banana</li>
C) <li>["apple", "banana"]</li>
D) Nothing — loops are not supported in Jinja2
```

**Q10.** A child template begins with `{% extends "base.html" %}`. What does this mean?
```
A) The child template replaces base.html
B) The child template imports macros from base.html
C) The child template inherits the layout of base.html and fills in its blocks
D) base.html must include the child template explicitly
```

---

## Section 4: Forms & Requests (Q11–Q13)

**Q11.** A form is submitted via POST. How do you safely read a field named `email` in Flask without risking a KeyError?
```python
A) email = request.form["email"]
B) email = request.form.get("email")
C) email = request.args["email"]
D) email = request.json["email"]
```

**Q12.** What is wrong with this route?
```python
@app.route("/submit")
def submit():
    name = request.form.get("name")
    return f"Hello, {name}!"
```
```
A) f-strings are not supported in Flask
B) request.form is only available on POST requests; the route has no methods= argument
C) The route returns a string instead of jsonify()
D) Nothing is wrong
```

**Q13.** After successfully processing a POST form, what is the Flask best practice for the response?
```
A) Return the same page with a success message rendered in the template
B) Return an empty 200 response
C) Redirect to another URL using redirect(url_for(...))
D) Raise a 201 status code
```

---

## Section 5: Database & APIs (Q14–Q16)

**Q14.** Which call returns a Python dict/list from a Flask route as a proper JSON HTTP response?
```python
A) return {"key": "value"}
B) return json.dumps({"key": "value"})
C) return jsonify({"key": "value"})
D) return str({"key": "value"})
```

**Q15.** What does `db.row_factory = sqlite3.Row` do when set on an sqlite3 connection?
```
A) Converts all column values to strings
B) Allows row columns to be accessed by name (like a dict) in addition to index
C) Automatically commits after every query
D) Creates a new table called Row
```

**Q16.** A POST route returns `jsonify(new_item), 201`. What is the significance of `201`?
```
A) It is an error code meaning "Created with warnings"
B) It signals the client that a resource was successfully created
C) It is the default Flask status code for JSON responses
D) It redirects the client to the new resource
```

---

## Section 6: Deployment (Q17–Q18)

**Q17.** Which of these is the correct way to read an environment variable in Python, with a fallback default?
```python
A) os.env["SECRET_KEY"]
B) os.environ.get("SECRET_KEY", "default")
C) env.get("SECRET_KEY")
D) os.getenv.SECRET_KEY
```

**Q18.** Why should `debug=True` **never** be used in production?
```
A) It makes the app run slower
B) It disables JSON responses
C) It exposes an interactive debugger in the browser that can execute arbitrary code
D) It prevents the app from binding to port 80
```

---

## Answers

.
.
.
.
.
.

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | C | The path is everything after the domain: `/users/42` |
| 2 | C | POST is the conventional method for creating a new resource |
| 3 | C | 404 = Not Found |
| 4 | B | `<int:id>` matches any integer segment in the URL |
| 5 | C | Flask routes accept GET only by default unless `methods=` is specified |
| 6 | C | `name = "world"`, `.upper()` → `"WORLD"` |
| 7 | A | `@app.before_request` runs the decorated function before each request |
| 8 | C | `{{ variable }}` is Jinja2 output syntax |
| 9 | B | The for loop renders one `<li>` per item |
| 10 | C | `extends` makes the child inherit the parent layout and fill its blocks |
| 11 | B | `.get()` returns `None` instead of raising `KeyError` for missing keys |
| 12 | B | `request.form` is only populated on POST; without `methods=["GET","POST"]` a POST to this URL would 405 |
| 13 | C | Post/Redirect/Get (PRG) pattern prevents duplicate submissions on browser refresh |
| 14 | C | `jsonify()` sets the correct `Content-Type: application/json` header |
| 15 | B | `sqlite3.Row` enables column-name access: `row["title"]` instead of `row[0]` |
| 16 | B | HTTP 201 Created is the standard response for a successful resource creation |
| 17 | B | `os.environ.get(key, default)` is the standard pattern |
| 18 | C | The Werkzeug debugger allows running Python code in the browser — a critical security hole |
