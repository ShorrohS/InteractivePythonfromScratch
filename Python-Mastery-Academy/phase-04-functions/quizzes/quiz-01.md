# Phase 04 — Quiz 01: Functions

**Questions:** 20 | **Pass:** 16/20 | **Time:** 20 min

---

**Q1.** What is the difference between a parameter and an argument?
```
A) Same thing
B) Parameter = variable in definition; Argument = value passed when calling
C) Arguments are optional; parameters are required
D) Parameters are in () of call; arguments are in def
```

**Q2.** What does this function return?
```python
def f(x, y):
    z = x + y
```
```
A) z   B) x + y   C) None   D) 0
```

**Q3.** Which line causes an error?
```python
def calc(a, b=10, c=20):
    return a + b + c
```
```
A) calc(1)
B) calc(1, 2)
C) calc(b=5, a=1)
D) No error possible
```

**Q4.** What is the output?
```python
def greet(name, msg="Hello"):
    return f"{msg}, {name}!"
print(greet("Alice"))
print(greet("Bob", "Hi"))
```
```
A) Hello, Alice! / Hello, Bob!
B) Hello, Alice! / Hi, Bob!
C) Hello, Alice! / Hi, Hi!
D) Error
```

**Q5.** What is the classic Python mutable default trap?
```
A) Using int as default
B) Using list or dict as default — shared across all calls
C) Using None as default
D) Having too many defaults
```

**Q6.** What does `*args` capture?
```
A) All keyword arguments as a dict
B) All positional arguments as a tuple
C) Only the first argument
D) Optional arguments only
```

**Q7.** What does `**kwargs` capture?
```
A) All positional arguments as a list
B) Only required keyword arguments
C) All keyword arguments as a dict
D) Named arguments only
```

**Q8.** What is the output?
```python
def add(*nums):
    return sum(nums)
print(add(1, 2, 3, 4))
```
```
A) 10   B) (1,2,3,4)   C) Error   D) [1,2,3,4]
```

**Q9.** What is the LEGB rule?
```
A) A Python coding standard
B) The order Python looks up variable names (Local, Enclosing, Global, Built-in)
C) Lambda, Expression, Generator, Boolean
D) A memory management rule
```

**Q10.** What prints?
```python
x = "global"
def f():
    x = "local"
    print(x)
f()
print(x)
```
```
A) local / global
B) global / global
C) local / local
D) Error
```

**Q11.** A closure is:
```
A) A function with no return statement
B) A function that captures variables from its enclosing scope
C) A function inside a class
D) A function called with no arguments
```

**Q12.** What is a lambda function?
```
A) A function with no name defined with lambda keyword
B) A very large function
C) A function that only works with lists
D) A built-in Python function
```

**Q13.** What does `sorted(items, key=lambda x: x["age"])` do?
```
A) Sorts by the string "age"
B) Sorts items using the "age" field of each item as the sort key
C) Removes items where age is missing
D) Error — sorted() doesn't accept lambdas
```

**Q14.** What is the base case in recursion?
```
A) The first call to the function
B) The condition that STOPS the recursion
C) The recursive call
D) The return statement
```

**Q15.** What happens without a base case?
```
A) Function returns None
B) RecursionError (stack overflow)
C) Function runs once
D) Nothing — Python stops automatically
```

**Q16.** What is a pure function?
```
A) A function with no parameters
B) A function with no side effects that returns same output for same input
C) A function that only uses built-ins
D) A function shorter than 10 lines
```

**Q17.** Which is equivalent to `list(map(lambda x: x**2, nums))`?
```
A) [x for x in nums if x**2]
B) [x**2 for x in nums]
C) filter(lambda x: x**2, nums)
D) sorted(nums, key=lambda x: x**2)
```

**Q18.** What does `filter()` return?
```
A) A list
B) A lazy iterator (need list() to get all results)
C) A generator
D) A tuple
```

**Q19.** What is the output?
```python
def outer():
    n = 10
    def inner():
        return n * 2
    return inner

f = outer()
print(f())
```
```
A) Error   B) 20   C) 10   D) inner
```

**Q20.** When should you use a lambda vs def?
```
A) Always use lambda — it's shorter
B) Always use def — it's clearer
C) Lambda for simple one-expression throwaway functions; def for complex or reusable ones
D) Only lambda works with map/filter
```

---

## Answers

| Q | A | Q | A | Q | A | Q | A |
|---|---|---|---|---|---|---|---|
| 1 | B | 6 | B | 11 | B | 16 | B |
| 2 | C | 7 | C | 12 | A | 17 | B |
| 3 | D | 8 | A | 13 | B | 18 | B |
| 4 | B | 9 | B | 14 | B | 19 | B |
| 5 | B | 10 | A | 15 | B | 20 | C |
