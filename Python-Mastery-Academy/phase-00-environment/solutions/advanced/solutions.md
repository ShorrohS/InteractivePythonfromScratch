# Phase 00 — Advanced Exercise Solutions

---

## Challenge 1 — Project Setup Script

**Windows PowerShell version:**

```powershell
# setup-project.ps1
param([string]$projectName)

if (-not $projectName) {
    Write-Error "Usage: .\setup-project.ps1 <project-name>"
    exit 1
}

# 1. Create project folder
New-Item -ItemType Directory -Path $projectName
Set-Location $projectName

# 2. Initialise git
git init

# 3. Create virtual environment
python -m venv venv

# 4. Create project files
New-Item main.py, README.md, requirements.txt

# 5. Create .gitignore with standard Python entries
@"
# Virtual environment
venv/
env/

# Python cache
__pycache__/
*.pyc
*.pyo

# Secrets
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"@ | Set-Content .gitignore

# 6. Initial commit
git add .gitignore main.py README.md requirements.txt
git commit -m "Initial project setup"

Write-Host "Project '$projectName' created successfully!"
```

**Bash version (Mac/Linux):**

```bash
#!/bin/bash
# setup-project.sh

PROJECT_NAME=$1

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./setup-project.sh <project-name>"
    exit 1
fi

mkdir "$PROJECT_NAME" && cd "$PROJECT_NAME"
git init
python3 -m venv venv
touch main.py README.md requirements.txt

cat > .gitignore << 'EOF'
venv/
__pycache__/
*.pyc
.env
.vscode/
.DS_Store
EOF

git add .gitignore main.py README.md requirements.txt
git commit -m "Initial project setup"

echo "Project '$PROJECT_NAME' created successfully!"
```

---

## Challenge 2 — Git Disaster Recovery

### Situation: Not yet pushed

```bash
# Remove the file from the commit but keep it locally
git rm --cached passwords.txt
git commit --amend -m "Add database module"

# Now add to .gitignore so it's never committed
echo "passwords.txt" >> .gitignore
git add .gitignore
git commit -m "Add passwords.txt to gitignore"
```

### Situation: Already pushed to GitHub

This is a serious incident. Steps:

```bash
# 1. Remove from history (rewrites git history — coordinate with team)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch passwords.txt' \
  --prune-empty --tag-name-filter cat -- --all

# 2. Force push (all teammates must re-clone)
git push origin --force --all

# 3. Immediately revoke/rotate any exposed credentials
# 4. Check GitHub's "Secret scanning" alerts
# 5. Notify your security team
```

**Prevention:**
```bash
# Install pre-commit hooks that block secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline
```

---

## Challenge 3 — Dependency Conflict

**Why it occurs:**
Flask 2.1.0 requires Werkzeug >= 2.0, but pip found Werkzeug 1.0.1 already installed (possibly from a different project or an older global installation).

**Solution 1 — Upgrade the conflicting package:**
```bash
pip install --upgrade werkzeug
pip install -r requirements.txt
```

**Solution 2 — Use a fresh virtual environment:**
```bash
python -m venv fresh-venv
source fresh-venv/bin/activate
pip install -r requirements.txt
# pip resolves dependencies from scratch, avoids conflicts
```

**Solution 3 — Use pip's dependency resolver:**
```bash
pip install --upgrade pip           # ensure latest pip
pip install -r requirements.txt     # new pip has better conflict resolution
```

**How virtual environments prevent this:**
Each virtual environment is isolated — Werkzeug 1.0.1 in one project never clashes with Werkzeug 2.3.0 in another because they're in separate `site-packages` folders.

---

## Challenge 4 — Multi-Environment Setup

**File structure:**
```
my-project/
├── .env                    ← NEVER committed (dev secrets)
├── .env.example            ← Committed (template with no real values)
├── .env.staging            ← NEVER committed
├── .env.production         ← NEVER committed
├── requirements.txt        ← Production dependencies only
├── requirements-dev.txt    ← Dev dependencies (pytest, black, etc.)
└── src/
    └── config.py           ← Reads environment variables
```

**requirements-dev.txt:**
```
-r requirements.txt        # includes everything from requirements.txt
pytest==7.4.3
black==23.10.1
python-dotenv==1.0.0
```

**config.py:**
```python
import os
from dotenv import load_dotenv

# Load environment-specific .env file
env = os.getenv("APP_ENV", "development")
load_dotenv(f".env.{env}")

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY   = os.getenv("SECRET_KEY")
DEBUG        = os.getenv("DEBUG", "false").lower() == "true"
```

**Managing secrets safely:**
- Development: `.env` with local database URL
- Staging: Set environment variables on the staging server directly
- Production: Use cloud secrets manager (AWS Secrets Manager, Azure Key Vault) — never files

---

## Challenge 5 — Terminal Scripting

**Mac/Linux:**
```bash
# Find all .py files recursively
find . -name "*.py" -type f

# Count them
find . -name "*.py" -type f | wc -l

# Print full paths
find . -name "*.py" -type f -print

# Save to file
find . -name "*.py" -type f > python_files.txt
cat python_files.txt
```

**Windows PowerShell:**
```powershell
# Find and count
$files = Get-ChildItem -Recurse -Filter "*.py"
$files.Count

# Print paths
$files | Select-Object -ExpandProperty FullName

# Save to file
$files | Select-Object -ExpandProperty FullName | Out-File python_files.txt
Get-Content python_files.txt
```
