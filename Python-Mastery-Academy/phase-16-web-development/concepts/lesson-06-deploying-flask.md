# Lesson 06 — Deploying a Flask App

**Phase:** 16 — Web Development | **Time:** ~45 min

---

## Part 1: Development vs Production

The built-in Flask dev server is single-threaded, shows full tracebacks in the browser, and is not designed to handle real traffic. Never run it in production.

| Setting | Development | Production |
|---------|-------------|------------|
| `debug` | `True` | **`False`** |
| `SECRET_KEY` | Any string | Random, from environment variable |
| Server | Flask dev server | Gunicorn / Waitress |
| HTTPS | Not needed | **Required** |
| Error pages | Full traceback | Generic error page |

```python
# ❌ Development only — never deploy this
app.run(debug=True)

# ✅ Production — debug off, secret from environment
import os

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["DEBUG"]      = False
```

---

## Part 2: Environment Variables with python-dotenv

Hard-coding secrets in source code leaks credentials if the repository is ever made public. Store them in a `.env` file and load them at runtime.

```bash
pip install python-dotenv
```

**.env** — never commit this file:

```
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=sqlite:///app.db
FLASK_ENV=production
```

**.gitignore** — add this line so the file is never staged:

```
.env
```

**app.py:**

```python
import os
from dotenv import load_dotenv
from flask import Flask

load_dotenv()   # reads .env into os.environ before the app reads anything

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"]      = os.getenv("FLASK_ENV") != "production"
```

Provide a `.env.example` in the repo with placeholder values so teammates know which variables to set:

```
SECRET_KEY=replace-with-a-random-string
DATABASE_URL=sqlite:///app.db
FLASK_ENV=development
```

---

## Part 3: requirements.txt

A `requirements.txt` lets any machine reproduce your exact set of dependencies.

```bash
# Generate from your active virtual environment
pip freeze > requirements.txt
```

Minimal **requirements.txt** for a Flask app:

```
flask==3.0.3
gunicorn==22.0.0
python-dotenv==1.0.1
```

Install on a fresh machine or build server:

```bash
pip install -r requirements.txt
```

Pin exact versions so a future release of a dependency cannot break your deployed app.

---

## Part 4: Gunicorn — WSGI Production Server

Gunicorn spawns multiple worker processes so the app handles concurrent requests. It is the standard Python WSGI server for production.

```bash
pip install gunicorn

# Basic: gunicorn <module>:<flask_app_variable>
gunicorn app:app

# Recommended production settings
gunicorn app:app --workers 4 --bind 0.0.0.0:8000 --timeout 60

# App factory pattern (create_app function)
gunicorn "app:create_app()" --workers 2
```

Gunicorn runs on **Linux and macOS only**. On Windows use Waitress instead:

```bash
pip install waitress
waitress-serve --port=8000 app:app
```

Number of workers rule of thumb: `(2 × CPU cores) + 1`. For a free-tier server with 1 core, start with 2 workers.

---

## Part 5: Deploying to Render.com (Free Tier)

Render is a cloud platform with a free tier well suited to small Flask apps. It reads from a GitHub repository and redeploys automatically on every push.

**Step 1** — Push your project to GitHub. Your repository should contain:

```
app.py
requirements.txt
.env.example        ← template with placeholder values, not real secrets
templates/
static/
```

**Step 2** — Log in to [render.com](https://render.com) and click **New → Web Service**.

**Step 3** — Connect your GitHub repository.

**Step 4** — Configure the service:

| Field | Value |
|-------|-------|
| Environment | Python 3 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn app:app` |

**Step 5** — Set environment variables under **Environment** in the dashboard:

```
SECRET_KEY   = <generate a random 32-character string>
FLASK_ENV    = production
```

**Step 6** — Click **Deploy**. Render builds the image and starts the service. The app is live at `https://your-app.onrender.com`.

Subsequent deployments happen automatically whenever you push to the connected branch.

---

## Part 6: Dockerfile for Flask

Containerising with Docker makes the app run identically on any machine and is required by many cloud platforms.

**Dockerfile:**

```dockerfile
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies first — this layer is cached separately
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
COPY . .

# Expose the port Gunicorn will listen on
EXPOSE 8000

# Start Gunicorn when the container runs
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000", "--workers", "2"]
```

Build and run locally to verify the image works before pushing to a registry:

```bash
# Build the image
docker build -t my-flask-app .

# Run with environment variables from .env
docker run -p 8000:8000 --env-file .env my-flask-app

# Visit http://localhost:8000 to confirm it works
```

---

## Part 7: Common Deployment Mistakes

```
✘  debug=True in production
   → exposes full stack traces and an interactive debugger to the internet

✘  SECRET_KEY hardcoded in source code
   → leaks to anyone with repository access; sessions can be forged

✘  No HTTPS
   → cookies and form data travel in plain text; modern browsers warn users

✘  requirements.txt missing or out of date
   → the build server installs a different package version than you tested

✘  SQLite .db file inside a container
   → data is lost on every restart; use a hosted database for production

✘  Not setting FLASK_ENV=production
   → Flask may still show debug-friendly error pages to real users
```

---

## Practice Exercises

1. Create a `.env` file with `SECRET_KEY` and `DATABASE_URL`. Update `app.py` to read both values with `python-dotenv` and confirm the app starts correctly.

2. Generate a `requirements.txt` for the Task Manager from Lesson 05. Add `gunicorn` and `python-dotenv` to it, then install from it in a fresh virtual environment to confirm nothing is missing.

3. Write a `Dockerfile` for the Task Manager. Build the image and run it locally, then verify the app loads at `http://localhost:8000`.

4. Deploy your Flask app to Render.com following the steps in Part 5. Take note of which environment variables you set in the dashboard and why each one matters.

5. Add a `/health` route that returns `{"status": "ok", "debug": app.debug}`. Confirm that `debug` is `False` in production. Explain why a health-check endpoint is useful when running behind a load balancer.

---

## Phase 16 Complete

You have covered the full Flask web development stack: HTTP fundamentals, routing, Jinja2 templating, databases, and deployment to production.

**Up next:** [Phase 17 → Advanced Python](../../phase-17-advanced-python/concepts/lesson-01-decorators.md)
