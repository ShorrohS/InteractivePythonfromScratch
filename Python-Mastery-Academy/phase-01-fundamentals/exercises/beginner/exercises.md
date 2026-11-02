# 📝 Phase 01 — Beginner Exercises

> Attempt ALL questions before opening solutions.
> Solutions: `../../solutions/beginner/solutions.md`

---

## Section A: Variables & Data Types (Q1–Q5)

**Q1.** Create variables for a person's profile:
- Name: "Jordan Smith"
- Age: 28
- Height in meters: 1.75
- Is employed: True

Print each variable with its label using f-strings.

---

**Q2.** What is the output of this code?

```python
x = 10
y = x
x = 20
print(x)
print(y)
```

---

**Q3.** Which of these variable names are invalid? Explain why.

```
score       valid_user    2fast      my-name
_private    first name    total$     class
salary2024  TRUE
```

---

**Q4.** What is the data type of each value?

```python
a = "42"
b = 42
c = 42.0
d = True
e = None
```

---

**Q5.** Write code to:
1. Create a variable `price = 100`
2. Increase it by 25 using `+=`
3. Multiply it by 2 using `*=`
4. Print the final result

What is the final value?

---

## Section B: Input & Output (Q6–Q10)

**Q6.** Write a program that:
1. Asks for the user's name
2. Asks for their favorite number
3. Prints: "Hello [name], your favorite number doubled is [double]."

---

**Q7.** Fix this code so it runs correctly:

```python
age = input("Enter your age: ")
next_year = age + 1
print(f"Next year you will be {next_year}")
```

---

**Q8.** What is the output of these f-strings?

```python
price = 1234.5678
print(f"{price:.2f}")
print(f"{price:,.2f}")
print(f"{price:.0f}")
```

---

**Q9.** Write a program that asks for:
- Item name
- Item price
- Quantity to buy

Then prints:
```
Item:      Widget
Price:     $9.99
Quantity:  3
Subtotal:  $29.97
```

---

**Q10.** What is the output?

```python
name = "python"
print(name.upper())
print(name.title())
print(len(name))
print(name.replace("p", "P"))
```

---

## Section C: Operators (Q11–Q15)

**Q11.** Calculate and print the result of each:

```python
a = 25
b = 7
# Print: a + b, a - b, a * b, a / b, a // b, a % b, a ** b
```

---

**Q12.** What is the output? Explain operator precedence.

```python
print(2 + 3 * 4)
print((2 + 3) * 4)
print(10 - 2 ** 3)
print(10 / 2 + 3 * 2)
```

---

**Q13.** Write a program that:
- Takes a number of minutes as input
- Prints how many full hours and remaining minutes

Example: 137 minutes → "2 hours and 17 minutes"

(Hint: use `//` and `%`)

---

**Q14.** Predict the output of these comparisons:

```python
x = 15
print(x > 10)
print(x == 15)
print(x != 20)
print(x >= 15)
print(x < 20 and x > 10)
print(x < 5 or x > 10)
```

---

**Q15.** Write an expression (no if/else) that returns True if:
- A number `n` is divisible by both 3 and 5

Test it with n = 15, n = 9, n = 10.

---

## Section D: Strings (Q16–Q20)

**Q16.** Given `text = "  Hello, World!  "`, write code to:
1. Remove whitespace from both sides
2. Convert to all uppercase
3. Count how many times 'l' appears
4. Replace "World" with "Python"

---

**Q17.** Given `name = "Alice Johnson"`, extract:
1. The first name only
2. The last name only
3. The first letter of each name (initials)
4. A username: first letter of first name + last name, all lowercase

---

**Q18.** What does each line print?

```python
s = "Python"
print(s[0])
print(s[-1])
print(s[2:5])
print(s[::-1])
print(s * 3)
```

---

**Q19.** Write a program that:
1. Asks for a sentence
2. Prints the sentence in reverse
3. Prints how many words are in it
4. Prints whether it's a palindrome (same forwards and backwards, ignoring spaces and case)

---

**Q20.** Fix this code:

```python
full_name = "Alice Johnson"
parts = full_name.split()
first = parts[0]
last = parts[1]
print(f"First: {first}, Last: {last}")
email = first + "." + last + "@company.com"
print(f"Email: {email})
```

---

> **Solutions:** → [../../solutions/beginner/solutions.md](../../solutions/beginner/solutions.md)
