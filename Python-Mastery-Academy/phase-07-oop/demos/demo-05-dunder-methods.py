"""
Demo 05 - Dunder (Magic) Methods
Phase 07: OOP

Run: python demo-05-dunder-methods.py
"""

import functools

print("=" * 55)
print("DEMO 05 - Dunder (Magic) Methods")
print("=" * 55)

# --- 1. __str__ vs __repr__ ---
print("\n1. __str__ vs __repr__:")

class Book:
    def __init__(self, title: str, author: str, pages: int):
        self.title  = title
        self.author = author
        self.pages  = pages

    def __str__(self) -> str:
        """
        Human-readable.  Called by print(), str(), f-strings.
        Aim: readable for end users.
        """
        return f'"{self.title}" by {self.author} ({self.pages}pp)'

    def __repr__(self) -> str:
        """
        Unambiguous / machine-readable.  Called by repr(), debuggers,
        the REPL.  Ideal: something you could paste back into Python.
        """
        return f"Book({self.title!r}, {self.author!r}, {self.pages})"

b = Book("Fluent Python", "Luciano Ramalho", 792)
print(f"  str:  {b}")               # calls __str__
print(f"  repr: {repr(b)}")         # calls __repr__
print(f"  list: {[b]}")             # list uses __repr__ for items


# --- 2. COMPARISON DUNDERS + total_ordering ---
print("\n2. Comparison dunders and functools.total_ordering:")

@functools.total_ordering      # generates __le__, __gt__, __ge__ from just
                               # __eq__ + __lt__.  Avoids writing all six.
class Temperature:
    def __init__(self, celsius: float):
        self.celsius = celsius

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius == other.celsius

    def __lt__(self, other: "Temperature") -> bool:
        if not isinstance(other, Temperature):
            return NotImplemented
        return self.celsius < other.celsius

    def __repr__(self) -> str:
        return f"Temperature({self.celsius}°C)"

temps = [Temperature(100), Temperature(0), Temperature(37), Temperature(20)]
print(f"  Unsorted: {temps}")
print(f"  Sorted:   {sorted(temps)}")
print(f"  Max:      {max(temps)}")
print(f"  37°C == 37°C: {Temperature(37) == Temperature(37)}")
print(f"  0°C  <  37°C: {Temperature(0)  < Temperature(37)}")
print(f"  100°C >= 37°C: {Temperature(100) >= Temperature(37)}")  # from total_ordering


# --- 3. ARITHMETIC DUNDERS ---
print("\n3. Arithmetic dunders:")

class Money:
    def __init__(self, amount: float, currency: str = "USD"):
        self.amount   = round(float(amount), 2)
        self.currency = currency

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot mix {self.currency} and {other.currency}"
            )

    def __add__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        self._check_currency(other)
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, factor: float) -> "Money":
        return Money(self.amount * factor, self.currency)

    def __rmul__(self, factor: float) -> "Money":
        """Allows 2 * money, not just money * 2."""
        return self.__mul__(factor)

    def __neg__(self) -> "Money":
        """Unary minus — for deductions."""
        return Money(-self.amount, self.currency)

    def __repr__(self) -> str:
        return f"Money({self.amount:.2f}, {self.currency!r})"

    def __str__(self) -> str:
        return f"${self.amount:,.2f} {self.currency}"

price   = Money(49.99)
tax     = Money(4.00)
total   = price + tax
doubled = total * 2
print(f"  price: {price}")
print(f"  price + tax = {total}")
print(f"  total * 2   = {doubled}")
print(f"  3 * price   = {3 * price}")
print(f"  -price      = {-price}")

try:
    Money(10, "USD") + Money(10, "EUR")
except ValueError as e:
    print(f"  ValueError: {e}")


# --- 4. CONTAINER DUNDERS ---
print("\n4. Container dunders — __len__, __getitem__, __iter__, __contains__:")

class Playlist:
    def __init__(self, name: str):
        self.name   = name
        self._songs: list = []

    def add(self, song: str) -> None:
        self._songs.append(song)

    def __len__(self) -> int:
        """len(playlist)"""
        return len(self._songs)

    def __getitem__(self, index):
        """playlist[0], playlist[1:3], etc."""
        return self._songs[index]

    def __iter__(self):
        """for song in playlist:"""
        return iter(self._songs)

    def __contains__(self, song: str) -> bool:
        """'Song' in playlist"""
        return song in self._songs

    def __repr__(self) -> str:
        return f"Playlist({self.name!r}, {len(self)} songs)"

p = Playlist("Road Trip")
for song in ["Bohemian Rhapsody", "Hotel California", "Stairway to Heaven", "Purple Rain"]:
    p.add(song)

print(f"  {p}")
print(f"  len:     {len(p)}")
print(f"  p[0]:    {p[0]}")
print(f"  p[1:3]:  {p[1:3]}")
print(f"  'Hotel California' in p: {'Hotel California' in p}")
print(f"  'Never Gonna Give You Up' in p: {'Never Gonna Give You Up' in p}")
print(f"  Iterating:")
for song in p:
    print(f"    ♪ {song}")


# --- 5. __call__ — CALLABLE OBJECTS ---
print("\n5. __call__ — making an instance callable like a function:")

class Multiplier:
    """
    __call__ makes an instance behave like a function.
    Useful for stateful callables — functions that remember data.
    """
    def __init__(self, factor: float):
        self.factor = factor
        self.call_count = 0

    def __call__(self, value: float) -> float:
        self.call_count += 1
        return value * self.factor

    def __repr__(self) -> str:
        return f"Multiplier(×{self.factor}, called {self.call_count}× so far)"

double = Multiplier(2)
triple = Multiplier(3)

print(f"  double(5)   = {double(5)}")
print(f"  double(10)  = {double(10)}")
print(f"  triple(7)   = {triple(7)}")
print(f"  double: {double}")
print(f"  triple: {triple}")

# Works wherever a function is expected
numbers = [1, 2, 3, 4, 5]
print(f"  list(map(double, {numbers})) = {list(map(double, numbers))}")
print(f"  double was called {double.call_count} times total")
