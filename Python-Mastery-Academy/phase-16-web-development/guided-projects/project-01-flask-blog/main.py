"""
Project 01 - Flask Blog API
Phase 16: Web Development

SKILLS PRACTICED:
  - Flask routing (GET, POST, PUT, DELETE)
  - request.json for input
  - jsonify for output
  - HTTP status codes
  - In-memory data store
  - Input validation

SETUP:
  pip install flask

HOW TO RUN:
  python main.py
  Then open: http://localhost:5000/api/posts

TEST WITH CURL:
  curl http://localhost:5000/api/posts
  curl http://localhost:5000/api/posts/1
  curl -X POST -H "Content-Type: application/json" \\
       -d '{"title":"My Post","content":"Hello world","author":"Alice"}' \\
       http://localhost:5000/api/posts
"""

from flask import Flask, jsonify, request, abort
from datetime import datetime

app = Flask(__name__)
app.json.sort_keys = False   # keep JSON key order


# ── In-memory data store ────────────────────────────────────────────────────

posts = [
    {
        "id": 1, "title": "Welcome to Flask",
        "content": "Flask is a lightweight web framework for Python.",
        "author": "Admin", "tags": ["python", "flask"],
        "created": "2024-01-01", "updated": "2024-01-01", "published": True
    },
    {
        "id": 2, "title": "Building REST APIs",
        "content": "REST APIs use HTTP methods to create, read, update, delete data.",
        "author": "Alice", "tags": ["api", "rest"],
        "created": "2024-01-05", "updated": "2024-01-05", "published": True
    },
]
next_id = 3


# ── Helper ──────────────────────────────────────────────────────────────────

def find_post(pid: int) -> dict | None:
    return next((p for p in posts if p["id"] == pid), None)

def validate_post(data: dict) -> list[str]:
    errors = []
    if not data.get("title", "").strip():
        errors.append("Title is required")
    if not data.get("content", "").strip():
        errors.append("Content is required")
    if not data.get("author", "").strip():
        errors.append("Author is required")
    return errors


# ── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def home():
    return jsonify({
        "name": "Flask Blog API",
        "version": "1.0",
        "endpoints": {
            "GET /api/posts":          "List all posts",
            "GET /api/posts/<id>":     "Get a post",
            "POST /api/posts":         "Create a post",
            "PUT /api/posts/<id>":     "Update a post",
            "DELETE /api/posts/<id>":  "Delete a post",
            "GET /api/posts/search":   "Search posts (?q=keyword)",
            "GET /api/stats":          "Blog statistics",
        }
    })


@app.route("/api/posts", methods=["GET"])
def get_posts():
    """List all posts, optionally filtered by author or tag."""
    author = request.args.get("author")
    tag    = request.args.get("tag")
    page   = request.args.get("page",  1, type=int)
    limit  = request.args.get("limit", 10, type=int)

    result = posts[:]
    if author:
        result = [p for p in result if p["author"].lower() == author.lower()]
    if tag:
        result = [p for p in result if tag.lower() in [t.lower() for t in p.get("tags", [])]]

    published_only = request.args.get("published", "true").lower() == "true"
    if published_only:
        result = [p for p in result if p.get("published", True)]

    start = (page - 1) * limit
    paginated = result[start:start + limit]

    return jsonify({
        "posts": paginated,
        "total": len(result),
        "page":  page,
        "limit": limit,
        "pages": -(-len(result) // limit)   # ceiling division
    })


@app.route("/api/posts/<int:pid>", methods=["GET"])
def get_post(pid: int):
    """Get a single post by ID."""
    post = find_post(pid)
    if not post:
        return jsonify({"error": f"Post {pid} not found"}), 404
    return jsonify(post)


@app.route("/api/posts", methods=["POST"])
def create_post():
    """Create a new post."""
    global next_id
    data = request.json or {}
    errors = validate_post(data)
    if errors:
        return jsonify({"errors": errors}), 400

    today = datetime.now().strftime("%Y-%m-%d")
    post = {
        "id":        next_id,
        "title":     data["title"].strip(),
        "content":   data["content"].strip(),
        "author":    data["author"].strip(),
        "tags":      data.get("tags", []),
        "created":   today,
        "updated":   today,
        "published": data.get("published", True)
    }
    posts.append(post)
    next_id += 1
    return jsonify(post), 201


@app.route("/api/posts/<int:pid>", methods=["PUT"])
def update_post(pid: int):
    """Replace an entire post."""
    post = find_post(pid)
    if not post:
        return jsonify({"error": "Not found"}), 404

    data = request.json or {}
    errors = validate_post(data)
    if errors:
        return jsonify({"errors": errors}), 400

    post.update({
        "title":     data["title"].strip(),
        "content":   data["content"].strip(),
        "author":    data["author"].strip(),
        "tags":      data.get("tags", post.get("tags", [])),
        "published": data.get("published", post.get("published", True)),
        "updated":   datetime.now().strftime("%Y-%m-%d")
    })
    return jsonify(post)


@app.route("/api/posts/<int:pid>", methods=["PATCH"])
def patch_post(pid: int):
    """Update specific fields of a post."""
    post = find_post(pid)
    if not post:
        return jsonify({"error": "Not found"}), 404

    data   = request.json or {}
    fields = ("title", "content", "author", "tags", "published")
    post.update({k: v for k, v in data.items() if k in fields})
    post["updated"] = datetime.now().strftime("%Y-%m-%d")
    return jsonify(post)


@app.route("/api/posts/<int:pid>", methods=["DELETE"])
def delete_post(pid: int):
    """Delete a post."""
    post = find_post(pid)
    if not post:
        return jsonify({"error": "Not found"}), 404
    posts.remove(post)
    return "", 204


@app.route("/api/posts/search", methods=["GET"])
def search_posts():
    """Search posts by keyword in title or content."""
    q = request.args.get("q", "").lower()
    if not q:
        return jsonify({"error": "Query parameter 'q' is required"}), 400
    results = [p for p in posts
               if q in p["title"].lower() or q in p["content"].lower()]
    return jsonify({"query": q, "results": results, "count": len(results)})


@app.route("/api/stats", methods=["GET"])
def blog_stats():
    """Blog statistics."""
    authors = {}
    for p in posts:
        authors[p["author"]] = authors.get(p["author"], 0) + 1

    all_tags = {}
    for p in posts:
        for tag in p.get("tags", []):
            all_tags[tag] = all_tags.get(tag, 0) + 1

    return jsonify({
        "total_posts":     len(posts),
        "published":       sum(1 for p in posts if p.get("published")),
        "drafts":          sum(1 for p in posts if not p.get("published")),
        "authors":         authors,
        "top_tags":        sorted(all_tags.items(), key=lambda x: x[1], reverse=True)[:5]
    })


# ── Error Handlers ──────────────────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found"}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed"}), 405

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    print("Flask Blog API")
    print("Docs: http://localhost:5000/")
    app.run(debug=True, port=5000)
