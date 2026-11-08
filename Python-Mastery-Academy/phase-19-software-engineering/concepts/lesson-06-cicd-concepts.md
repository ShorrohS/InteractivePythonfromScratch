# Lesson 06 — CI/CD Concepts for Python Projects

**Phase:** 19 — Software Engineering | **Time:** ~55 min | **Prerequisite:** Lesson 05 — Documentation

---

## Learning Objectives

- Explain what Continuous Integration and Continuous Delivery mean in practice
- Write a GitHub Actions workflow that installs, lints, and tests a Python project
- Configure Tox to run the test suite against multiple Python versions
- Measure and report test coverage with `pytest-cov`
- Understand the difference between staging and production environments

---

## Part 1: What Is CI/CD?

**Continuous Integration (CI)** is the practice of merging every developer's changes into a shared branch frequently — at least once a day — and verifying each merge automatically with a build and test pipeline.

**Continuous Delivery (CD)** extends that: after CI passes, the artifact (package, Docker image, deployed app) is automatically pushed to a staging environment and can be promoted to production with a single human approval.

**Continuous Deployment** goes one step further: production is updated automatically when CI passes, with no human gate.

For most Python projects the pipeline looks like this:

```
Push / Pull Request
        │
        ▼
  ┌─────────────┐
  │   Lint      │  flake8, ruff, black --check
  └──────┬──────┘
         │ pass
  ┌──────▼──────┐
  │   Test      │  pytest across Python 3.11, 3.12
  └──────┬──────┘
         │ pass
  ┌──────▼──────┐
  │  Coverage   │  pytest-cov, fail if < 80%
  └──────┬──────┘
         │ pass
  ┌──────▼──────┐
  │  Build      │  python -m build (wheel + sdist)
  └──────┬──────┘
         │ pass (on tag only)
  ┌──────▼──────┐
  │  Deploy     │  twine upload to PyPI / deploy to staging
  └─────────────┘
```

---

## Part 2: GitHub Actions Workflow

GitHub Actions workflows live in `.github/workflows/`. Each file is a YAML document describing triggers, jobs, and steps.

```yaml
# .github/workflows/ci.yml

name: CI

on:
  push:
    branches: ["main", "develop"]
  pull_request:
    branches: ["main"]

jobs:
  lint:
    name: Lint
    runs-on: ubuntu-latest

    steps:
      - name: Check out source
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install linting tools
        run: pip install ruff black

      - name: Run ruff (fast linter + import sorter)
        run: ruff check src/ tests/

      - name: Check formatting with black
        run: black --check src/ tests/

  test:
    name: Test (Python ${{ matrix.python-version }})
    runs-on: ubuntu-latest
    needs: lint   # only run if lint passes

    strategy:
      matrix:
        python-version: ["3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: "pip"

      - name: Install package and test dependencies
        run: pip install -e ".[dev]"

      - name: Run tests with coverage
        run: |
          pytest \
            --cov=src/mypackage \
            --cov-report=term-missing \
            --cov-fail-under=80 \
            -v

      - name: Upload coverage report
        uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.12'
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: false

  build:
    name: Build distribution
    runs-on: ubuntu-latest
    needs: test

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Build wheel and source distribution
        run: |
          pip install build
          python -m build

      - name: Store build artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

Key points:
- `needs: lint` ensures the test job only starts after linting passes
- The `matrix` strategy runs the same test job against both Python 3.11 and 3.12 in parallel
- `--cov-fail-under=80` fails the build if coverage drops below 80%

---

## Part 3: Tox for Multi-Version Testing

Tox is a local equivalent of the matrix strategy above. It creates isolated virtual environments, installs your package into each, and runs the test suite — all in one command.

```ini
# tox.ini  (project root)

[tox]
envlist = py311, py312, lint, type
isolated_build = true

[testenv]
deps =
    pytest
    pytest-cov
commands =
    pytest \
        --cov={envsitepackagesdir}/mypackage \
        --cov-report=term-missing \
        {posargs}

[testenv:lint]
deps =
    ruff
    black
commands =
    ruff check src/ tests/
    black --check src/ tests/

[testenv:type]
deps =
    mypy
    pytest
commands =
    mypy src/mypackage --strict
```

Run everything locally before pushing:

```bash
tox                 # all envs
tox -e py312        # single version
tox -e lint         # linting only
```

Tox reads your `pyproject.toml` or `setup.cfg` for package metadata, so keep those in sync.

---

## Part 4: Coverage Reporting with pytest-cov

Install once:

```bash
pip install pytest-cov
```

Basic run:

```bash
pytest --cov=src/mypackage --cov-report=term-missing
```

```
Name                        Stmts   Miss  Cover   Missing
---------------------------------------------------------
src/mypackage/__init__.py       5      0   100%
src/mypackage/orders.py        42      6    86%   45-47, 89, 103-104
src/mypackage/shipping.py      28      3    89%   62, 71-72
---------------------------------------------------------
TOTAL                          75      9    88%
```

Generate an HTML report you can open in a browser:

```bash
pytest --cov=src/mypackage --cov-report=html
open htmlcov/index.html    # macOS; on Windows use start htmlcov/index.html
```

Configure defaults so you do not type flags every run:

```ini
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--cov=src/mypackage --cov-report=term-missing"
testpaths = ["tests"]

[tool.coverage.run]
source = ["src/mypackage"]
omit = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
fail_under = 80
show_missing = true
```

---

## Part 5: Staging vs Production Environments

Deploying directly to production without validation is high-risk. Professional workflows use at least two environments.

| Environment | Purpose | Triggered by |
|-------------|---------|--------------|
| **Development** | Local machine; mocks or SQLite | Developer's own machine |
| **Staging** | Production-like; real data copy | Merge to `develop` branch |
| **Production** | Live; real users and data | Git tag (`v1.2.3`) or manual approval |

A typical CD extension to the workflow above:

```yaml
# .github/workflows/deploy.yml

name: Deploy

on:
  push:
    tags:
      - "v[0-9]+.[0-9]+.[0-9]+"   # trigger on version tags only

jobs:
  publish:
    name: Publish to PyPI
    runs-on: ubuntu-latest
    environment: production        # requires manual approval in GitHub

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Build and publish
        env:
          TWINE_USERNAME: __token__
          TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          pip install build twine
          python -m build
          twine upload dist/*
```

Using `environment: production` in GitHub lets you configure required reviewers — no deployment happens until a named person approves it.

Secrets (API tokens, database passwords) are stored in GitHub repository settings under **Settings → Secrets and variables → Actions**, never in the code.

---

## Key Takeaways

- CI catches broken code before it reaches the main branch; do not merge without a passing pipeline
- GitHub Actions workflows are YAML files in `.github/workflows/` — version-controlled alongside the code
- The `matrix` strategy lets you test against multiple Python versions in parallel for free
- `pytest-cov` with `--cov-fail-under` enforces a coverage floor; 80% is a reasonable starting point
- Staging environments absorb deployment mistakes before real users see them; secrets belong in environment variables, never in source

---

## What's Next

**[Lesson 07 → Package Structure and Publishing to PyPI](lesson-07-package-structure-and-pypi.md)**

We go from a working project to a published Python package — `pyproject.toml`, building wheels, TestPyPI, and semantic versioning.
