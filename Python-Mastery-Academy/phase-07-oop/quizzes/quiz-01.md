# Phase 07 — Quiz 01: OOP

**Questions:** 20 | **Pass:** 16/20 | **Time:** 20 min

---

**Q1.** What is `__init__` used for?
`A) Import the class  B) Called automatically when creating an instance  C) Define class attributes  D) Import methods`

**Q2.** What does `self` refer to?
`A) The class itself  B) The current instance  C) The parent class  D) The module`

**Q3.** What is a class attribute?
`A) Only accessible via self  B) Shared by all instances  C) Created inside __init__  D) Private by default`

**Q4.** What does `super().__init__()` do in a child class?
`A) Calls the child's __init__  B) Calls the parent's __init__  C) Creates a new instance  D) Overwrites parent methods`

**Q5.** Which decorator makes a read-only computed attribute?
`A) @staticmethod  B) @classmethod  C) @property  D) @computed`

**Q6.** What is the difference between `__str__` and `__repr__`?
`A) No difference  B) __str__ is user-facing; __repr__ is developer-facing  C) __repr__ is called by print()  D) Only __str__ exists`

**Q7.** What is polymorphism?
`A) Having many attributes  B) Same method name behaves differently in different classes  C) Multiple inheritance  D) Private methods`

**Q8.** What is encapsulation?
`A) Copying a class  B) Bundling data + methods and controlling access  C) Inheriting from multiple parents  D) Making all methods static`

**Q9.** What does the `_` prefix on an attribute mean?
`A) The attribute is deleted  B) Convention: treat as private/internal  C) It's a class attribute  D) It cannot be changed`

**Q10.** What does `isinstance(obj, ParentClass)` return for a child class instance?
`A) False  B) True  C) None  D) Depends on the class`

**Q11.** What is an abstract class?
`A) A class with no methods  B) A class that cannot be instantiated directly  C) A class with only class methods  D) A class without __init__`

**Q12.** How do you create an abstract method?
`A) def abstract_method()  B) @abstractmethod before def  C) method.abstract = True  D) abstract def method()`

**Q13.** What is duck typing?
`A) Only ducks can use the method  B) If an object has the required method, it works regardless of type  C) Type checking before method calls  D) A type of inheritance`

**Q14.** What does `__len__` enable?
`A) str(obj)  B) len(obj)  C) iter(obj)  D) repr(obj)`

**Q15.** What is a `@classmethod`?
`A) A method that can only be called on instances  B) A method that receives the class as first argument  C) A method with no parameters  D) Same as @staticmethod`

**Q16.** When does the `@property.setter` run?
`A) When you call the property as a function  B) When you assign a value: obj.prop = value  C) When you delete the attribute  D) At class creation`

**Q17.** What is composition vs inheritance?
`A) Same concept  B) Inheritance = "is a"; Composition = "has a"  C) Composition is only for abstract classes  D) Inheritance is always better`

**Q18.** What does `__enter__` enable?
`A) Entering a class  B) Using an object with the with statement  C) Calling an object like a function  D) Iteration`

**Q19.** What is the output?
```python
class A:
    x = 10

class B(A):
    pass

b = B()
b.x = 20
print(A.x, B.x, b.x)
```
`A) 10 10 20  B) 20 20 20  C) 10 20 20  D) Error`

**Q20.** What is name mangling (`__attr`)?
`A) Renames the attribute to something unreadable  B) Changes attribute name to _ClassName__attr  C) Makes the attribute truly private  D) Encrypts the attribute`

---

## Answers

| Q | A | Q | A | Q | A | Q | A |
|---|---|---|---|---|---|---|---|
| 1 | B | 6 | B | 11 | B | 16 | B |
| 2 | B | 7 | B | 12 | B | 17 | B |
| 3 | B | 8 | B | 13 | B | 18 | B |
| 4 | B | 9 | B | 14 | B | 19 | A |
| 5 | C | 10 | B | 15 | B | 20 | B |
