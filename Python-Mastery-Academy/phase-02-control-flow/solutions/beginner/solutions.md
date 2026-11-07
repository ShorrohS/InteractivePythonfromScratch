# Phase 02 — Beginner Exercise Solutions

---

## Q1. Positive / Negative / Zero

```python
num = float(input("Enter a number: "))
if num > 0:
    print("Positive")
elif num < 0:
    print("Negative")
else:
    print("Zero")
```

---

## Q2. Traffic Light

```python
signal = input("Enter signal colour: ").strip().lower()
match signal:
    case "red":
        print("STOP")
    case "yellow":
        print("SLOW DOWN")
    case "green":
        print("GO")
    case _:
        print("INVALID SIGNAL")
```

---

## Q3. Temperature Classifier

```python
temp = float(input("Temperature in Celsius: "))
if temp > 35:
    print("Extreme Heat")
elif temp >= 25:
    print("Hot")
elif temp >= 15:
    print("Warm")
elif temp >= 5:
    print("Cool")
else:
    print("Cold")
```

---

## Q4. Output with nested if

```
A
B
C
D
```

Explanation:
- `x=10 > 5` → prints "A"
- `x=10 > 8` → prints "B" (nested if is True)
- "C" prints after the inner if block (still inside outer if)
- "D" prints at top level (always runs)

---

## Q5. Grade classifier

```python
score = float(input("Score (0-100): "))
if score >= 90:
    letter, status = "A", "Pass"
elif score >= 80:
    letter, status = "B", "Pass"
elif score >= 70:
    letter, status = "C", "Pass"
elif score >= 60:
    letter, status = "D", "Pass"
else:
    letter, status = "F", "Fail"
print(f"Grade: {letter} — {status}")
```

---

## Q6. Fix the code

```python
# Bugs: missing colon after if, using = instead of ==, missing colon after else
score = 75
if score >= 90:
    print("A")
elif score == 80:    # Changed = to == (also: this should be >= 80)
    print("B")
else:
    print("Other")
```

---

## Q7. Simple login

```python
username = input("Username: ").strip()
password = input("Password: ").strip()
if username == "admin" and password == "1234":
    print("Access granted")
else:
    print("Access denied")
```

---

## Q8. Multiplication table (while loop)

```python
n = int(input("Enter a number: "))
i = 1
while i <= 12:
    print(f"  {n} x {i:2d} = {n*i:3d}")
    i += 1
```

---

## Q9. Number guessing game

```python
import random
secret = random.randint(1, 10)
attempts = 0
while True:
    guess = int(input("Guess (1-10): "))
    attempts += 1
    if guess == secret:
        print(f"Correct! You got it in {attempts} attempt(s).")
        break
    elif guess < secret:
        print("Too low!")
    else:
        print("Too high!")
```

---

## Q10. Sum of 1 to 5

```
total = 0 + 1 + 2 + 3 + 4 + 5 = 15
```

---

## Q11. Password length check

```python
while True:
    pwd = input("Enter password (min 8 chars): ")
    if len(pwd) >= 8:
        print("Password accepted!")
        break
    print(f"Too short ({len(pwd)} chars). Need at least 8.")
```

---

## Q12. Infinite loop fix

```python
count = 0
while count < 10:
    print(count)
    count += 1    # FIX: add this line
```

---

## Q13. Even numbers 2–20

```python
for i in range(2, 21, 2):
    print(i, end=" ")
# OR:
for i in range(1, 21):
    if i % 2 == 0:
        print(i, end=" ")
```

---

## Q14. Find sum/max/min manually

```python
numbers = [7, 2, 9, 4, 5]
total = 0
maximum = numbers[0]
minimum = numbers[0]
for n in numbers:
    total += n
    if n > maximum: maximum = n
    if n < minimum: minimum = n
count = len(numbers)
print(f"Sum: {total}, Max: {maximum}, Min: {minimum}, Avg: {total/count:.2f}")
```

---

## Q15. enumerate output

```
1. APPLE
2. BANANA
3. CHERRY
```

---

## Q16. First 10 Fibonacci

```python
a, b = 0, 1
count = 0
while count < 10:
    print(a, end=" ")
    a, b = b, a + b
    count += 1
```

---

## Q17. 5x5 multiplication table

```python
for i in range(1, 6):
    for j in range(1, 6):
        print(f"{i*j:3}", end="")
    print()
```

---

## Q18. Running sum until 0

```python
total = 0
while True:
    n = int(input("Enter number (0 to stop): "))
    if n == 0:
        break
    total += n
print(f"Sum: {total}")
```

---

## Q19. Numbers not divisible by 3

```python
for i in range(1, 21):
    if i % 3 == 0:
        continue
    print(i, end=" ")
```

---

## Q20. Triangle pattern

```python
n = 5
for i in range(1, n + 1):
    print("*" * i)
```
