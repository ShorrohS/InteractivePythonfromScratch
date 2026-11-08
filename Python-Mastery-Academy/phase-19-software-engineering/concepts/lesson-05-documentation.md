# Lesson 05 — Documentation

**Phase:** 19 — Software Engineering | **Time:** ~50 min | **Prerequisite:** Lesson 04 — Refactoring Techniques

---

## Learning Objectives

- Write complete Google-style and NumPy-style docstrings with all standard sections
- Add type annotations inside docstrings for compatibility with tools that do not use inline hints
- Understand the Sphinx `sphinx-apidoc` workflow for generating HTML API docs
- Apply README best practices used in professional open-source and team projects

---

## Part 1: Why Documentation Matters

Code explains *how*. Documentation explains *why* and *what for*. Well-documented code:

- Lets teammates use your module without reading its implementation
- Makes your past self explainable to your future self
- Enables automated API reference generation (Sphinx, pdoc)
- Is required by most open-source contribution guidelines

The two most common Python docstring styles are **Google** and **NumPy**. Pick one per project and stick to it. Both are understood by Sphinx, VS Code, and PyCharm.

---

## Part 2: Google-Style Docstrings

Clean, compact. Good for most application code.

```python
def calculate_compound_interest(
    principal: float,
    annual_rate: float,
    years: int,
    compounding_frequency: int = 12,
) -> float:
    """Calculate the final amount after compound interest.

    Uses the standard compound interest formula:
    A = P * (1 + r/n)^(n*t)

    Args:
        principal: The initial investment amount in dollars.
        annual_rate: Annual interest rate as a percentage (e.g. 5.0 for 5%).
        years: Number of years to compound over.
        compounding_frequency: How many times per year interest compounds.
            Defaults to 12 (monthly).

    Returns:
        The total amount after compounding, rounded to two decimal places.

    Raises:
        ValueError: If principal or annual_rate is negative, or years is zero.

    Examples:
        >>> calculate_compound_interest(1000, 5.0, 10)
        1647.01
        >>> calculate_compound_interest(500, 3.5, 5, compounding_frequency=1)
        592.69
    """
    if principal < 0:
        raise ValueError(f"Principal must be non-negative, got {principal}")
    if annual_rate < 0:
        raise ValueError(f"Annual rate must be non-negative, got {annual_rate}")
    if years <= 0:
        raise ValueError(f"Years must be positive, got {years}")

    rate = annual_rate / 100
    n = compounding_frequency
    amount = principal * (1 + rate / n) ** (n * years)
    return round(amount, 2)


class OrderRepository:
    """Manages persistence for Order objects.

    Provides CRUD operations backed by a SQLite database. All methods
    use parameterised queries to prevent SQL injection.

    Attributes:
        db_path: Absolute path to the SQLite database file.
        connection: Active database connection (set after __init__).

    Example:
        >>> repo = OrderRepository(":memory:")
        >>> order = {"customer_id": 1, "total": 99.99, "status": "pending"}
        >>> saved = repo.save(order)
        >>> saved["id"]
        1
    """

    def __init__(self, db_path: str) -> None:
        """Open (or create) the database and ensure the schema exists.

        Args:
            db_path: Path to the SQLite file, or ":memory:" for an in-memory db.
        """
        import sqlite3
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self._create_schema()

    def find_by_id(self, order_id: int) -> dict | None:
        """Fetch a single order by its primary key.

        Args:
            order_id: The integer primary key of the order.

        Returns:
            A dictionary representation of the order row, or None if not found.
        """
        row = self.connection.execute(
            "SELECT * FROM orders WHERE id = ?", (order_id,)
        ).fetchone()
        return dict(row) if row else None

    def _create_schema(self) -> None:
        """Create the orders table if it does not already exist."""
        self.connection.execute(
            """CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending'
            )"""
        )
        self.connection.commit()
```

---

## Part 3: NumPy-Style Docstrings

Verbose but very structured. Preferred for scientific libraries and data-heavy code where parameter types and shapes need detailed description.

```python
import numpy as np


def normalise_array(data: np.ndarray, axis: int = 0) -> np.ndarray:
    """Normalise an array to zero mean and unit variance.

    Applies z-score normalisation along the specified axis. NaN values
    propagate through — use ``numpy.nanmean`` / ``numpy.nanstd`` before
    calling this function if NaN handling is required.

    Parameters
    ----------
    data : np.ndarray
        Input array of shape (n_samples, n_features) or any shape compatible
        with the chosen axis.
    axis : int, optional
        Axis along which to compute mean and standard deviation.
        Default is 0 (normalise each column independently).

    Returns
    -------
    np.ndarray
        Normalised array with the same shape as ``data``. Columns (or rows)
        with zero standard deviation are left as-is to avoid division by zero.

    Raises
    ------
    ValueError
        If ``data`` is not a numpy array.
    TypeError
        If ``axis`` is not an integer.

    Notes
    -----
    This is equivalent to ``sklearn.preprocessing.StandardScaler`` but
    operates on plain NumPy arrays without fitting a separate object.

    Examples
    --------
    >>> import numpy as np
    >>> x = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
    >>> normalise_array(x)
    array([[-1.22474487, -1.22474487],
           [ 0.        ,  0.        ],
           [ 1.22474487,  1.22474487]])
    """
    if not isinstance(data, np.ndarray):
        raise ValueError(f"Expected np.ndarray, got {type(data).__name__}")
    mean = data.mean(axis=axis, keepdims=True)
    std  = data.std(axis=axis, keepdims=True)
    std  = np.where(std == 0, 1, std)   # avoid divide-by-zero
    return (data - mean) / std
```

---

## Part 4: The Sphinx Workflow

Sphinx converts docstrings into a full HTML documentation site. You do not need to install it to understand the flow.

**Step 1 — Initialise the docs directory**

```bash
# From the project root:
sphinx-quickstart docs
```

This creates `docs/conf.py` (configuration), `docs/index.rst` (root page), and a `Makefile`.

**Step 2 — Configure `conf.py` for autodoc**

```python
# docs/conf.py  (key lines)
extensions = [
    "sphinx.ext.autodoc",       # pull docstrings from source
    "sphinx.ext.napoleon",      # Google/NumPy style support
    "sphinx.ext.viewcode",      # link to source on each page
]

# Point Sphinx at your src/ layout
import sys, os
sys.path.insert(0, os.path.abspath("../src"))
```

**Step 3 — Generate `.rst` stubs from your package**

```bash
sphinx-apidoc -o docs/api src/mypackage
```

This creates one `.rst` file per module. Each file contains `.. automodule::` directives that pull in your docstrings at build time.

**Step 4 — Build the HTML site**

```bash
cd docs
make html
# Output lands in docs/_build/html/index.html
```

**Step 5 — Keep docs in sync**

Re-run `sphinx-apidoc` whenever you add new modules, then rebuild. In CI (see Lesson 06), add a `docs` job that runs `make html` so broken docstrings are caught before merge.

---

## Part 5: README Best Practices

A README is the front door to your project. It should answer four questions in under two minutes of reading: what does it do, how do I install it, how do I use it, and how do I contribute?

```markdown
# MyPackage

[![PyPI version](https://badge.fury.io/py/mypackage.svg)](https://pypi.org/project/mypackage/)
[![Python](https://img.shields.io/pypi/pyversions/mypackage)](https://pypi.org/project/mypackage/)
[![Tests](https://github.com/you/mypackage/actions/workflows/ci.yml/badge.svg)](https://github.com/you/mypackage/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A concise one-sentence description of what the package does and who it is for.

---

## Features

- Bullet list of the three or four headline capabilities
- Keep it to things that differentiate you from alternatives
- Link to the full changelog for more detail

## Requirements

- Python 3.11+
- No external dependencies for the core library

## Installation

```bash
pip install mypackage
```

For development:

```bash
git clone https://github.com/you/mypackage
cd mypackage
pip install -e ".[dev]"
```

## Quick Start

```python
from mypackage import OrderProcessor

processor = OrderProcessor(api_key="your-key")
result = processor.submit({"item": "laptop", "qty": 1})
print(result.order_id)
```

## Documentation

Full API reference and guides at **[docs.mypackage.io](https://docs.mypackage.io)**.

## Contributing

1. Fork the repository and create a feature branch: `git checkout -b feat/my-change`
2. Make changes and add tests for new behaviour
3. Run the test suite: `pytest`
4. Open a pull request with a clear description

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide, including coding standards and commit message format.

## Licence

MIT — see [LICENSE](LICENSE).
```

**Key README rules:**

- Badges go at the top — they communicate project health at a glance
- Code examples go in the README itself, not just linked to documentation
- Installation instructions should work copy-paste from a clean environment
- A contributing section removes the barrier for first-time contributors

---

## Key Takeaways

- **Google style** is compact and readable in most editors; **NumPy style** is verbose and precise — pick one per project
- Every public function and class deserves at least an `Args` / `Returns` block; private helpers need only a one-liner
- Sphinx `autodoc` + `napoleon` turns well-written docstrings into a published API reference with almost no extra work
- A README earns its place by answering install, use, and contribute questions without sending the reader elsewhere first
- Documentation has a maintenance cost — write less that is always accurate rather than more that goes stale

---

## What's Next

**[Lesson 06 → CI/CD Concepts](lesson-06-cicd-concepts.md)**

We set up a GitHub Actions pipeline that automatically lints, tests, and checks coverage every time code is pushed — the foundation of a professional Python project.
