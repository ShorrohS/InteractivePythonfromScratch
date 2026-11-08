# Lesson 08 — Code Review Practices and Collaborative Development

**Phase:** 19 — Software Engineering | **Time:** ~45 min | **Prerequisite:** Lesson 07 — Package Structure and PyPI

---

## Learning Objectives

- Know what to check during a code review: correctness, style, tests, and documentation
- Give feedback that is specific, actionable, and kind
- Set up the `pre-commit` framework with flake8 and black hooks
- Follow pull request etiquette that respects your teammates' time
- Use `git diff` and `git log` to understand changes before reviewing them

---

## Part 1: What to Look for in a Code Review

A code review is not a style argument. Its purpose is to catch problems before they reach main and to share knowledge across the team. Work through these categories in order — correctness first, polish last.

**1. Correctness**
- Does the code do what the PR description says it does?
- Are edge cases handled (empty list, None, zero, very large input)?
- Are errors raised or returned in a way callers can handle?
- Are there race conditions or state-mutation bugs?

**2. Security**
- Is any user input validated before use?
- Are secrets handled via environment variables, not hard-coded?
- Are SQL queries parameterised (no string concatenation into queries)?

**3. Tests**
- Is new behaviour covered by at least one test?
- Do tests verify failure cases, not just the happy path?
- Are tests independent (no shared mutable state between tests)?

**4. Readability and Style**
- Do names communicate intent?
- Is the code self-explanatory, or does it need comments to explain what it does?
- Is the change consistent with the surrounding code style?

**5. Documentation**
- Are public functions and classes documented with docstrings?
- Is the README or CHANGELOG updated if the public API changed?

---

## Part 2: Giving Constructive Feedback

Feedback is most useful when it is specific, actionable, and separates the code from the person. These patterns help.

```
# ── Vague (not useful) ───────────────────────────────────────────────────────
"This is messy."
"Not the right approach."
"This won't scale."

# ── Specific and actionable ──────────────────────────────────────────────────
"This function is doing validation and formatting in one pass.
 Could we extract the validation into `_validate_order()` to make
 both pieces unit-testable separately? Happy to discuss if you
 had a reason for keeping them together."

"Line 42: `user_data['email']` will raise KeyError if the key is
 missing. Consider using `.get('email')` or checking the key first,
 depending on whether a missing email is expected."

"The test only covers the happy path. Could you add one test where
 the input is an empty list? Based on the docstring it should raise
 ValueError, but the current code would return 0."
```

**Tone markers that help:**
- "Could we…" — collaborative, not prescriptive
- "Consider…" — suggestion, not demand
- "I think…" — signals opinion, not objective fact
- "nit:" — marks a minor style comment the author can choose to skip

**Nits are low-stakes** — leave them but do not block a merge over them. Reserve "request changes" for correctness and security issues.

---

## Part 3: Pre-commit Hooks

Pre-commit hooks run checks automatically before each `git commit`, catching formatting and linting issues locally before they hit CI.

### Installation

```bash
pip install pre-commit
```

### Configuration

```yaml
# .pre-commit-config.yaml  (project root)

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.4
    hooks:
      - id: ruff                    # fast linter
        args: [--fix]               # auto-fix safe issues
      - id: ruff-format             # ruff's built-in formatter

  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black                   # opinionated formatter

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace     # strip trailing spaces
      - id: end-of-file-fixer       # ensure files end with a newline
      - id: check-yaml              # validate YAML syntax
      - id: check-toml              # validate TOML syntax
      - id: check-merge-conflict    # catch unresolved merge markers
      - id: debug-statements        # flag leftover pdb/breakpoint() calls

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: ["pydantic>=2.0"]
```

Install the hooks into the local `.git/hooks/` directory:

```bash
pre-commit install
```

From now on, every `git commit` triggers the hooks. A failing hook aborts the commit and shows the issue.

Run hooks manually across all files (useful after first install or adding a new hook):

```bash
pre-commit run --all-files
```

Update hook versions to the latest tagged release:

```bash
pre-commit autoupdate
```

---

## Part 4: Pull Request Etiquette

A pull request is a communication artefact as much as a technical one. These habits reduce review friction.

**Keep PRs small.** A PR that touches two files and changes one behaviour takes five minutes to review. A PR that rewrites six files takes two hours and gets worse feedback. Break large changes into a sequence of small, reviewable PRs.

**Write a descriptive title.** The title should say *what* changed, not *that* something changed.

```
# BAD
Update code

# BAD  
Fix bug

# GOOD
fix: validate email format before saving to database

# GOOD
feat: add CSV export to the orders report endpoint
```

**Link related issues.** Closing keywords automatically close the issue when the PR merges:

```
Closes #142
Fixes #98, #103
Part of #200
```

**Describe the change in the body.** Answer three questions:
1. What does this change do?
2. Why is it needed?
3. How was it tested?

```markdown
## What
Adds email validation to `create_user()`. Previously, any string was
accepted as an email, causing downstream failures when the mailer
tried to send confirmation emails.

## Why
Fixes #142. Users could register with invalid emails and then never
receive the confirmation link.

## How tested
- Added `test_create_user_rejects_invalid_email` in `tests/test_users.py`
- Manually tested with `user@`, `@domain.com`, and a valid address
- Existing tests pass (no regression)
```

---

## Part 5: Using `git diff` and `git log`

Before reviewing someone else's PR — or before writing your own commit message — get a clear picture of what changed.

```bash
# See all uncommitted changes (staged + unstaged)
git diff

# See only staged changes (what will go into the next commit)
git diff --staged

# Compare your branch to main to see the full PR diff
git diff main...feature/add-email-validation

# Stat summary: which files changed and by how many lines
git diff --stat main...feature/add-email-validation

# One-line log for the current branch relative to main
git log main..HEAD --oneline

# Full log with author, date, and diff for each commit
git log --patch main..HEAD

# Show all files changed in a specific commit
git show --stat abc1234

# Find which commit introduced a specific line
git log -S "def validate_email" --oneline
```

When reviewing a PR on GitHub, the diff view shows the same information. Use `git log --oneline` locally to understand how many commits are in the PR and whether they are logically ordered.

---

## Key Takeaways

- Review correctness and security before commenting on style — prioritise what actually matters
- Effective feedback names the specific line, explains the problem, and suggests a fix; "nit:" marks optional style notes
- `pre-commit` enforces formatting and linting before every commit, keeping CI clean and review focused on logic
- Small, focused PRs with clear titles and issue links get reviewed faster and get better feedback
- `git diff main...HEAD` and `git log main..HEAD --oneline` give you a reviewer's-eye view of your own changes before you open the PR

---

## What's Next

**Phase 19 — Software Engineering is complete.**

You have covered clean code, design patterns, SOLID, refactoring, documentation, CI/CD, packaging, and code review. The next phase puts all of this together in the **Phase 20 — Capstone Project**, where you design, build, test, document, and publish a complete Python application from scratch.
