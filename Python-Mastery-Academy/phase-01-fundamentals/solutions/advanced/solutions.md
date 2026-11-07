# Phase 01 — Advanced Exercise Solutions

---

## Q1. Caesar Cipher

```python
def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shifted = chr((ord(char) - base + shift) % 26 + base)
            result.append(shifted)
        else:
            result.append(char)   # preserve non-letters unchanged
    return ''.join(result)

def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)   # decrypt = encrypt with negative shift

message = input("Enter message: ")
shift   = int(input("Enter shift (1-25): "))

encrypted = caesar_encrypt(message, shift)
decrypted = caesar_decrypt(encrypted, shift)

print(f"\n  Original:  {message}")
print(f"  Encrypted: {encrypted}")
print(f"  Decrypted: {decrypted}")
```

---

## Q2. Mortgage Calculator

```python
import math

price    = float(input("Property price ($): "))
down_pct = float(input("Down payment (%): ")) / 100
rate_yr  = float(input("Annual rate (%): ")) / 100
years    = int(input("Loan term (years): "))

loan        = price * (1 - down_pct)
r           = rate_yr / 12
n           = years * 12
monthly     = loan * r * (1 + r)**n / ((1 + r)**n - 1)
total_paid  = monthly * n
total_int   = total_paid - loan

print(f"\n  Loan amount:   ${loan:,.2f}")
print(f"  Monthly pay:   ${monthly:,.2f}")
print(f"  Total paid:    ${total_paid:,.2f}")
print(f"  Total interest:${total_int:,.2f}")

print(f"\n  AMORTISATION SCHEDULE (first 6 months)")
print(f"  {'Month':>5} {'Payment':>10} {'Principal':>10} {'Interest':>10} {'Balance':>12}")
print(f"  {'-'*52}")
balance = loan
for month in range(1, 7):
    interest_due = balance * r
    principal_due = monthly - interest_due
    balance -= principal_due
    print(f"  {month:>5} ${monthly:>9,.2f} ${principal_due:>9,.2f} ${interest_due:>9,.2f} ${balance:>11,.2f}")
```

---

## Q3. Password Strength Meter

```python
def strength_score(pwd: str) -> tuple:
    score = 0
    feedback = []

    # Length (up to 30 points)
    length_pts = min(30, len(pwd) * 2)
    score += length_pts
    if len(pwd) < 8:
        feedback.append("Make it at least 8 characters")

    # Uppercase
    if any(c.isupper() for c in pwd):
        score += 10
    else:
        feedback.append("Add uppercase letters")

    # Lowercase
    if any(c.islower() for c in pwd):
        score += 10
    else:
        feedback.append("Add lowercase letters")

    # Digits
    if any(c.isdigit() for c in pwd):
        score += 10
    else:
        feedback.append("Add at least one digit")

    # Special characters
    specials = "!@#$%^&*"
    if any(c in specials for c in pwd):
        score += 20
    else:
        feedback.append(f"Add special characters ({specials})")

    # Common patterns
    common = ["1234", "password", "qwerty", "abc", "111", "000"]
    for p in common:
        if p in pwd.lower():
            score -= 20
            feedback.append(f"Remove common pattern: '{p}'")

    score = max(0, min(100, score))

    if score < 20:   label = "Very Weak"
    elif score < 40: label = "Weak"
    elif score < 60: label = "Fair"
    elif score < 80: label = "Strong"
    else:            label = "Very Strong"

    return score, label, feedback

pwd = input("Enter password: ")
score, label, feedback = strength_score(pwd)

filled = score // 10
bar = "[" + "#" * filled + " " * (10 - filled) + "]"
print(f"\n  Strength: {bar} {score}% — {label}")
if feedback:
    print("\n  Suggestions:")
    for tip in feedback:
        print(f"    - {tip}")
```

---

## Q4. Text Statistics Engine

```python
import re

text = """
Python is a high-level programming language. It is widely used for web development,
data analysis, artificial intelligence, and automation. Python is easy to learn because
its syntax is clear and readable. Many programmers prefer Python because it is
versatile and has a large community. Python continues to grow in popularity each year.
"""

stop_words = {"the", "a", "an", "is", "are", "was", "it", "its", "and", "for", "in", "of"}
words      = re.findall(r'\b[a-zA-Z]+\b', text.lower())
sentences  = re.split(r'[.!?]+', text.strip())
sentences  = [s.strip() for s in sentences if s.strip()]

# Word frequency (excluding stop words)
freq = {}
for w in words:
    if w not in stop_words:
        freq[w] = freq.get(w, 0) + 1

top5 = sorted(freq, key=freq.get, reverse=True)[:5]

def count_syllables(word):
    return max(1, len(re.findall(r'[aeiou]+', word.lower())))

total_syllables = sum(count_syllables(w) for w in words)
n_words, n_sent  = len(words), len(sentences)
fk_score = 206.835 - 1.015*(n_words/n_sent) - 84.6*(total_syllables/n_words)

print(f"  Characters:   {len(text)}")
print(f"  Words:        {n_words}")
print(f"  Sentences:    {n_sent}")
print(f"  Avg word len: {sum(len(w) for w in words)/n_words:.1f}")
print(f"  Avg sent len: {n_words/n_sent:.1f} words")
print(f"  Longest word: {max(words, key=len)}")
print(f"  Top 5 words:  {', '.join(top5)}")
print(f"  Flesch score: {fk_score:.1f} ({'Easy' if fk_score > 60 else 'Difficult'})")
```

---

## Q5. Unit Conversion System

```python
conversions = {
    "Length": {
        "mm": 1, "cm": 10, "m": 1000, "km": 1_000_000,
        "inch": 25.4, "foot": 304.8, "yard": 914.4, "mile": 1_609_344
    },
    "Weight": {
        "mg": 1, "g": 1000, "kg": 1_000_000,
        "ounce": 28_349.5, "pound": 453_592, "ton": 1_000_000_000
    },
    "Time": {
        "second": 1, "minute": 60, "hour": 3600,
        "day": 86400, "week": 604800
    }
}

print("  Categories:", ", ".join(conversions.keys()))
cat = input("  Select category: ").strip().title()
if cat not in conversions:
    print("Invalid category.")
    exit()

print(f"  Units: {', '.join(conversions[cat].keys())}")
val  = float(input("  Enter value: "))
unit = input("  Enter unit: ").strip().lower()

if unit not in conversions[cat]:
    print("Invalid unit.")
    exit()

base_val = val * conversions[cat][unit]

print(f"\n  {val} {unit} =")
for target, factor in conversions[cat].items():
    result = base_val / factor
    print(f"    {result:>14.6g} {target}")
```
