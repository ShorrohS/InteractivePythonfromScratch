# Phase 01 — Advanced Exercises

> These are harder. Think before you code. Plan on paper first.
> Solutions: `../../solutions/advanced/solutions.md`

---

**Q1. Caesar Cipher**

Implement a Caesar cipher that:
- Asks for a message and a shift number
- Encrypts the message (each letter shifted by N positions in the alphabet)
- Also decrypts it back
- Preserves spaces, punctuation, and numbers (only shift letters)
- Works for both upper and lowercase

Example: "Hello" with shift 3 → "Khoor"

---

**Q2. Mortgage Calculator**

Build a complete mortgage calculator:

Inputs:
- Property price
- Down payment percentage
- Annual interest rate
- Loan term in years

Calculate:
- Loan amount
- Monthly payment (use EMI formula)
- Total amount paid
- Total interest paid
- Show first 6 months of amortisation schedule (principal and interest breakdown per payment)

Formula: `M = P * r(1+r)^n / ((1+r)^n - 1)`
Where: P=principal, r=monthly rate, n=total months

---

**Q3. Password Strength Meter**

Build a password strength checker that:
- Rates password from 0–100 based on:
  - Length (up to 30 points)
  - Uppercase letters (10 points)
  - Lowercase letters (10 points)
  - Digits (10 points)
  - Special characters `!@#$%^&*` (20 points)
  - No common patterns like "1234", "password", "qwerty" (-20 points each)
- Shows a visual strength bar: `[========== ] 80%`
- Labels: Very Weak / Weak / Fair / Strong / Very Strong
- Suggests specific improvements

---

**Q4. Text Statistics Engine**

Build a full text analyser that takes a multi-line paragraph (hard-code a sample) and reports:
- Total characters
- Total words
- Total sentences
- Total paragraphs
- Average word length
- Average sentence length (words)
- Top 5 most frequent words (excluding: the, a, an, is, are, was)
- Longest word
- Reading level estimate (use Flesch–Kincaid simplified: `206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)`)

---

**Q5. Unit Conversion System**

Build a comprehensive unit converter that handles ALL of these categories:
1. Length: mm, cm, m, km, inch, foot, yard, mile
2. Weight: mg, g, kg, ounce, pound, ton
3. Temperature: Celsius, Fahrenheit, Kelvin
4. Time: seconds, minutes, hours, days, weeks

The user selects a category, enters a value and source unit, then the program displays conversions to ALL other units in that category, formatted neatly in a table.

---

> **Solutions:** `../../solutions/advanced/solutions.md`
