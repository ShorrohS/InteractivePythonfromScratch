# Phase 01 — Intermediate Exercises

> These require writing complete programs, not just single lines.
> Attempt all before checking solutions.
> Solutions: `../../solutions/intermediate/solutions.md`

---

**Q1. Salary Calculator**

Ask the user for:
- Name
- Annual salary
- Tax rate as a percentage (e.g., 20)
- Bonus amount

Calculate and display:
- Monthly gross salary
- Annual tax amount
- Annual take-home (after tax)
- Monthly take-home
- Total earnings with bonus

Format all money values as `$1,234.56`.

---

**Q2. Temperature Converter**

Build a program that:
- Asks the user for a temperature and the unit (C, F, or K)
- Converts it to the other two units
- Displays all three with 2 decimal places

Formulas:
- C to F: `(C * 9/5) + 32`
- C to K: `C + 273.15`
- F to C: `(F - 32) * 5/9`

---

**Q3. String Statistics**

Ask the user to enter any sentence. Display:
- Original sentence
- Word count
- Character count (without spaces)
- Character count (with spaces)
- Number of vowels
- Most repeated word (hint: split and count)
- Sentence in UPPER case, lower case, Title Case

---

**Q4. Product Price Tag Generator**

Ask for:
- Product name
- Original price
- Discount percentage
- Tax rate percentage

Display a formatted price tag showing:
- Product name (centred in a 40-character border)
- Original price
- Discount amount and discounted price
- Tax on discounted price
- Final price
- Savings amount

---

**Q5. Personal Finance Summary**

Ask the user for 5 monthly expenses (label each one).
Calculate:
- Total monthly expenses
- Average expense
- Highest expense and which category
- Lowest expense and which category
- What percentage of a `$5000` monthly income this represents

---

**Q6. Data Type Detective**

Write a program that:
1. Asks the user to enter any value
2. Tries to determine if it's a valid int, float, or bool ("true"/"false")
3. Converts it to the detected type
4. Displays: original input, detected type, converted value, and `bool(value)`

---

**Q7. Receipt Generator**

Build a shopping receipt program:
- Ask how many items the user bought (1–5)
- For each item: ask name, quantity, unit price
- Display a formatted receipt with:
  - Each item line: `Item Name    Qty x $Price = $Subtotal`
  - Subtotal
  - Tax (8.5%)
  - Total
  - "THANK YOU" centred in a border

---

**Q8. Number Analyser**

Ask the user for a number and print ALL of the following:
- Is it positive, negative, or zero?
- Is it even or odd? (if integer)
- Is it divisible by 7?
- Square root (rounded to 4 decimals)
- Square (number ** 2)
- Cube (number ** 3)
- Formatted with commas if > 1000

---

**Q9. Username & Password Validator**

Ask for a username and password. Check and report:

Username rules:
- At least 4 characters
- Only letters, numbers, underscores
- No spaces

Password rules:
- At least 8 characters
- Contains at least one digit
- Contains at least one uppercase letter

Show which rules pass and which fail. Show overall result.

---

**Q10. Age in Different Units**

Ask for name and birth year. Calculate and display their age:
- In years
- In months (approximate)
- In weeks (approximate)
- In days (approximate)
- In hours (approximate)

Also tell them the year they will turn 100.

---

> **Solutions:** `../../solutions/intermediate/solutions.md`
