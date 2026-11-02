"""
Demo 06 — Strings
Phase 01: Python Fundamentals

Run: python demo-06-strings.py
"""

print("=" * 55)
print("DEMO 06 — String Operations")
print("=" * 55)

text = "  Hello, Python World!  "

# --- CASE METHODS ---
print("\n1. Case methods:")
print(f"Original:    '{text}'")
print(f"upper():     '{text.upper()}'")
print(f"lower():     '{text.lower()}'")
print(f"title():     '{text.title()}'")
print(f"strip():     '{text.strip()}'")

# --- INDEXING ---
print("\n2. Indexing and slicing:")
word = "Python"
print(f"String: '{word}'")
print(f"[0]:    '{word[0]}'   (first char)")
print(f"[-1]:   '{word[-1]}'  (last char)")
print(f"[0:3]:  '{word[0:3]}' (first 3)")
print(f"[3:]:   '{word[3:]}'  (from index 3)")
print(f"[::-1]: '{word[::-1]}' (reversed)")

# --- SEARCH METHODS ---
print("\n3. Search and check:")
sentence = "Python is easy and Python is powerful"
print(f"Text: '{sentence}'")
print(f"find('Python'):     {sentence.find('Python')}")
print(f"count('Python'):    {sentence.count('Python')}")
print(f"startswith('Python'): {sentence.startswith('Python')}")
print(f"'easy' in sentence: {'easy' in sentence}")

# --- REPLACE AND SPLIT ---
print("\n4. Replace and Split:")
csv_data = "Alice,30,Sales,75000"
print(f"CSV: {csv_data}")
parts = csv_data.split(",")
print(f"split(','):  {parts}")
rejoined = " | ".join(parts)
print(f"join(' | '): {rejoined}")

replaced = csv_data.replace(",", " → ")
print(f"replace:     {replaced}")

# --- F-STRING FORMATTING ---
print("\n5. f-string formatting:")
name = "Alice"
salary = 75000.5
score = 0.925
print(f"Name: {name}")
print(f"Salary: ${salary:,.2f}")
print(f"Score: {score:.1%}")
print(f"Name padded: {'|'}{name:<15}{'|'}")
print(f"Name padded: {'|'}{name:>15}{'|'}")

# --- PRACTICAL EXAMPLE ---
print("\n6. Practical — Name formatter:")
full_name = "  alice mae johnson  "
clean = full_name.strip().title()
first, *middle, last = clean.split()
initials = ". ".join([n[0] for n in clean.split()]) + "."
username = (first[0] + last).lower()
print(f"Raw input:  '{full_name}'")
print(f"Clean:       {clean}")
print(f"First name:  {first}")
print(f"Last name:   {last}")
print(f"Initials:    {initials}")
print(f"Username:    {username}")

print("\n" + "=" * 55)
