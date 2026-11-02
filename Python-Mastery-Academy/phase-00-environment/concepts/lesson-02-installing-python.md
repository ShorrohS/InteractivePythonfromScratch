# Lesson 02 — Installing Python

**Phase:** 00 — Environment Setup
**Time:** ~20 minutes
**Prerequisite:** Lesson 01

---

## Part 1: What You Are Installing

When you install Python, you get:

```
Python Interpreter     → Runs your .py files
Python Standard Library → Built-in modules (os, csv, json, etc.)
pip                    → Package manager to install third-party libraries
IDLE                   → Basic IDE (we'll use VS Code instead)
Python Launcher        → Manages multiple Python versions (Windows)
```

---

## Part 2: Installing on Windows

### Step 1 — Download Python

1. Open your browser
2. Go to: **https://www.python.org/downloads/**
3. Click the yellow "Download Python 3.x.x" button
4. Save the installer

### Step 2 — Run the Installer

1. Double-click the downloaded `.exe` file
2. **CRITICAL:** Check the box ✅ **"Add Python to PATH"** at the bottom
   - If you miss this, Python won't work from the terminal
3. Click **"Install Now"**
4. Wait for installation to complete
5. Click **"Close"**

```
⚠️  WARNING: If you forget to check "Add Python to PATH"
    You'll see this error in the terminal:
    'python' is not recognized as an internal or external command

    Fix: Uninstall and reinstall, checking the box this time.
```

### Step 3 — Verify Installation

Open **Command Prompt** or **PowerShell**:
- Press `Win + R`
- Type `cmd` or `powershell`
- Press Enter

Then type:

```bash
python --version
```

Expected output:
```
Python 3.12.x
```

Also verify pip:
```bash
pip --version
```

Expected output:
```
pip 24.x.x from C:\Users\...\pip (python 3.12)
```

---

## Part 3: Installing on macOS

### Option A — Official Installer (Recommended for beginners)

1. Go to: **https://www.python.org/downloads/macos/**
2. Download the latest macOS installer
3. Run the `.pkg` file
4. Follow the installation wizard

### Option B — Homebrew (Recommended for developers)

```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

### Verify on macOS

```bash
python3 --version
pip3 --version
```

Note: On macOS, use `python3` and `pip3` instead of `python` and `pip`.

---

## Part 4: Installing on Linux (Ubuntu/Debian)

Python 3 is usually pre-installed. Check first:

```bash
python3 --version
```

If not installed:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

---

## Part 5: Python Version Notes

```
Python 2 vs Python 3
────────────────────
Python 2: Retired in 2020. Do NOT use.
Python 3: Current version. Always use this.

If you see both installed:
  python   → might be Python 2 (old)
  python3  → definitely Python 3 (correct)

On Windows after installing Python 3.x:
  python   → Python 3 (usually)
  python3  → Python 3 (also works)
```

---

## Part 6: The Python Interactive Shell

Once Python is installed, you can use it interactively:

```bash
python
```

You'll see:
```
Python 3.12.0 (...)
>>> 
```

The `>>>` is the Python prompt. Try:

```python
>>> print("Hello, World!")
Hello, World!

>>> 2 + 2
4

>>> name = "Python"
>>> print(f"I am learning {name}!")
I am learning Python!

>>> exit()
```

Type `exit()` or press `Ctrl+Z` (Windows) / `Ctrl+D` (Mac/Linux) to quit.

---

## Part 7: Running Your First .py File

Create a file called `hello.py` with this content:

```python
print("Hello, World!")
print("My Python setup is working!")
print("Let's start coding.")
```

Run it from the terminal:

```bash
python hello.py
```

Expected output:
```
Hello, World!
My Python setup is working!
Let's start coding.
```

If you see this output — Python is working. 🎉

---

## Part 8: Common Installation Problems

### Problem 1: `python` not found

```
Error: 'python' is not recognized...
```

Fix: Reinstall Python and check "Add to PATH"

Or add manually:
```
Windows: System Properties → Environment Variables → PATH → Add Python directory
```

### Problem 2: Wrong Python version

```
$ python --version
Python 2.7.18
```

Fix: Use `python3` instead of `python`

### Problem 3: pip not found

```
Error: 'pip' is not recognized...
```

Fix:
```bash
python -m pip --version
# or
python -m ensurepip
```

### Problem 4: Permission errors on macOS/Linux

```bash
# Add --user flag
pip install --user package_name

# Or use python3 explicitly
python3 -m pip install package_name
```

---

## Verification Checklist

Run each command and confirm it works:

```bash
# 1. Python version
python --version
# Expected: Python 3.x.x

# 2. pip version
pip --version
# Expected: pip x.x.x from ...

# 3. Run interactive shell
python
# Expected: >>> prompt appears

# 4. Exit interactive shell
>>> exit()

# 5. Run a script
echo print("Python works!") > test.py
python test.py
# Expected: Python works!
```

---

## What's Next

Now that Python is installed, you need a good editor.

**Next → [Lesson 03: VS Code Setup](lesson-03-vscode-setup.md)**
