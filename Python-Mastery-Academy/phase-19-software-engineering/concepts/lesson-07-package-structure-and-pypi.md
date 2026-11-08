# Lesson 07 — Package Structure and Publishing to PyPI

**Phase:** 19 — Software Engineering | **Time:** ~55 min | **Prerequisite:** Lesson 06 — CI/CD Concepts

---

## Learning Objectives

- Choose between flat layout and src layout for a distributable package
- Write a complete `pyproject.toml` with `[build-system]` and `[project]` sections
- Know when to use `MANIFEST.in` and what to include in it
- Build a wheel and source distribution with `python -m build`
- Upload to TestPyPI to verify the package before releasing to PyPI
- Apply semantic versioning to communicate the impact of each release

---

## Part 1: Flat Layout vs Src Layout for Packaging

Both layouts work for distributing a package; the difference is subtle but matters.

**Flat layout** — package code sits directly at the project root:

```
mypackage/
├── mypackage/
│   ├── __init__.py
│   └── core.py
├── tests/
│   └── test_core.py
├── pyproject.toml
└── README.md
```

The risk: when you run `pytest` from the project root, Python finds the `mypackage/` directory on `sys.path` and imports from it directly — meaning you can pass tests against the uninstalled, unbuilt code. Packaging problems stay hidden until users install the wheel.

**Src layout** — package code lives inside `src/`:

```
mypackage/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── core.py
├── tests/
│   └── test_core.py
├── pyproject.toml
└── README.md
```

With a `src/` prefix, `mypackage` is not on `sys.path` unless you install the package (or use `pip install -e .`). Tests always run against the installed version, catching packaging bugs early. This is the modern recommendation.

---

## Part 2: `pyproject.toml` — The Modern Build File

`pyproject.toml` replaces `setup.py` and `setup.cfg`. It keeps all project metadata in one declarative file.

```toml
# pyproject.toml

# ── Build system ─────────────────────────────────────────────────────────────
[build-system]
requires      = ["hatchling"]           # or "setuptools>=68", "flit_core>=3.9"
build-backend = "hatchling.build"

# ── Project metadata ──────────────────────────────────────────────────────────
[project]
name            = "mypackage"
version         = "1.2.0"
description     = "A concise one-line description of what the package does."
readme          = "README.md"
license         = { file = "LICENSE" }
requires-python = ">=3.11"
keywords        = ["python", "package", "example"]

authors = [
  { name = "Your Name", email = "you@example.com" },
]

classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Topic :: Software Development :: Libraries",
]

# Runtime dependencies — pinned loosely so users are not over-constrained
dependencies = [
  "requests>=2.31,<3",
  "pydantic>=2.0,<3",
]

# ── Optional dependency groups ────────────────────────────────────────────────
[project.optional-dependencies]
dev = [
  "pytest>=7.4",
  "pytest-cov>=4.1",
  "ruff>=0.1",
  "black>=23.0",
  "mypy>=1.6",
]
docs = [
  "sphinx>=7.0",
  "sphinx-rtd-theme>=1.3",
]

# ── Entry points (creates a CLI command on install) ───────────────────────────
[project.scripts]
mypackage = "mypackage.cli:main"

# ── Project URLs ──────────────────────────────────────────────────────────────
[project.urls]
Homepage      = "https://github.com/you/mypackage"
Documentation = "https://mypackage.readthedocs.io"
"Bug Tracker" = "https://github.com/you/mypackage/issues"
Changelog     = "https://github.com/you/mypackage/blob/main/CHANGELOG.md"

# ── Tool configuration (kept in the same file) ───────────────────────────────
[tool.ruff]
line-length = 88
select      = ["E", "F", "I", "UP"]

[tool.black]
line-length = 88

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts   = "--cov=src/mypackage --cov-report=term-missing"

[tool.coverage.report]
fail_under   = 80
show_missing = true
```

The `[project.optional-dependencies]` section lets users install extras:

```bash
pip install mypackage          # runtime only
pip install "mypackage[dev]"   # runtime + dev tools
pip install "mypackage[docs]"  # runtime + sphinx
```

---

## Part 3: `MANIFEST.in` — Controlling the Source Distribution

The source distribution (`.tar.gz`) is what users get when they run `pip install mypackage` on a platform without a matching wheel. `MANIFEST.in` tells the build tool which non-Python files to include.

```
# MANIFEST.in

include README.md
include LICENSE
include CHANGELOG.md
include pyproject.toml

recursive-include src/mypackage/templates *.html *.txt
recursive-include src/mypackage/static    *.css *.js
recursive-include docs                    *.rst *.py *.txt

global-exclude *.pyc
global-exclude __pycache__
global-exclude *.egg-info
```

Common rules:
- `include` — add specific files
- `recursive-include <dir> <pattern>` — add files matching a pattern under a directory
- `global-exclude` — exclude file patterns everywhere
- `prune <dir>` — exclude an entire directory tree

With `hatchling` as the build backend (as in the `pyproject.toml` above), you configure the same rules inside `pyproject.toml` under `[tool.hatch.build.targets.sdist]` instead, making `MANIFEST.in` optional.

---

## Part 4: Building with `python -m build`

Install the `build` tool once:

```bash
pip install build
```

Then build from the project root (where `pyproject.toml` lives):

```bash
python -m build
```

This produces two files in `dist/`:

```
dist/
├── mypackage-1.2.0-py3-none-any.whl   # wheel (binary distribution)
└── mypackage-1.2.0.tar.gz             # source distribution
```

- **Wheel** (`.whl`) — a zip archive installed directly, no build step. Faster and preferred.
- **Source distribution** (`.tar.gz`) — raw source that `pip` builds on the target machine. Needed for packages that compile C extensions.

Inspect the wheel contents before publishing:

```bash
# A wheel is just a zip file
python -m zipfile -l dist/mypackage-1.2.0-py3-none-any.whl
```

---

## Part 5: TestPyPI First, Then PyPI

**TestPyPI** is a separate, throwaway registry for practising uploads. It is safe to use; packages there are routinely purged and do not affect real users.

Install `twine`:

```bash
pip install twine
```

Check the distribution files for common errors before uploading:

```bash
twine check dist/*
```

Upload to TestPyPI:

```bash
twine upload --repository testpypi dist/*
# Username: __token__
# Password: <your TestPyPI API token>
```

Verify the install from TestPyPI:

```bash
pip install --index-url https://test.pypi.org/simple/ mypackage==1.2.0
```

When everything looks correct, upload to the real PyPI:

```bash
twine upload dist/*
# Username: __token__
# Password: <your PyPI API token>
```

Store tokens in environment variables (`TWINE_USERNAME`, `TWINE_PASSWORD`) or in `~/.pypirc` — never hard-code them.

---

## Part 6: Semantic Versioning

Semantic versioning (`SemVer`) is a three-part version number: `MAJOR.MINOR.PATCH`.

| Change type | Bump | Example | Meaning |
|-------------|------|---------|---------|
| Breaking API change | MAJOR | `1.2.0` → `2.0.0` | Existing code may break |
| New backwards-compatible feature | MINOR | `1.2.0` → `1.3.0` | Add without breaking |
| Bug fix | PATCH | `1.2.0` → `1.2.1` | No new features |
| Pre-release | suffix | `1.3.0a1`, `1.3.0b2`, `1.3.0rc1` | Not production-ready |

```python
# src/mypackage/__init__.py

__version__ = "1.2.0"   # single source of truth

# Reference it in pyproject.toml via dynamic versioning, or
# keep both in sync manually — teams have strong preferences either way.
```

Automate version bumps with `bump-my-version`:

```bash
pip install bump-my-version

bump-my-version bump patch   # 1.2.0 → 1.2.1
bump-my-version bump minor   # 1.2.1 → 1.3.0
bump-my-version bump major   # 1.3.0 → 2.0.0
```

Each bump updates the version string, commits the change, and creates a Git tag — ready for the CI/CD deploy workflow from Lesson 06.

---

## Key Takeaways

- **Src layout** is the modern packaging standard; it prevents tests from hiding packaging bugs
- `pyproject.toml` is the single configuration file for metadata, dependencies, and tool settings
- Always test on **TestPyPI** before releasing to PyPI — uploads to PyPI cannot be deleted
- `twine check dist/*` catches common metadata errors before the upload attempt
- Semantic versioning communicates the impact of a release: MAJOR breaks, MINOR adds, PATCH fixes

---

## What's Next

**[Lesson 08 → Code Review Practices](lesson-08-code-review-practices.md)**

We cover what to look for in a review, how to give constructive feedback, pre-commit hooks, and pull request etiquette for collaborative Python development.
