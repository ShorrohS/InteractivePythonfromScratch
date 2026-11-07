"""
Demo 03 - JSON Files
Phase 05: File Handling

Run: python demo-03-json-files.py
"""

import json
import os
from datetime import datetime

print("=" * 55)
print("DEMO 03 - JSON Files")
print("=" * 55)

# --- WRITING JSON ---
print("\n1. Writing JSON:")
config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    "debug": False,
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "allowed_hosts": ["localhost", "127.0.0.1"],
    "max_connections": 100
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
print("  Written: config.json")

# Show the file content
with open("config.json", "r") as f:
    print(f"  File content:\n{f.read()}")

# --- READING JSON ---
print("\n2. Reading JSON:")
with open("config.json", "r") as f:
    loaded = json.load(f)

print(f"  App name:   {loaded['app_name']}")
print(f"  DB host:    {loaded['database']['host']}")
print(f"  DB port:    {loaded['database']['port']}")
print(f"  Hosts:      {loaded['allowed_hosts']}")
print(f"  Type check: {type(loaded['debug'])} {type(loaded['max_connections'])}")

# --- JSON STRINGS ---
print("\n3. JSON string serialization:")
user = {"name": "Alice", "age": 30, "active": True}

# Python dict → JSON string
json_str = json.dumps(user)
print(f"  json.dumps: {json_str}")

json_pretty = json.dumps(user, indent=2)
print(f"  Pretty:\n{json_pretty}")

# JSON string → Python dict
back = json.loads(json_str)
print(f"  json.loads: {back} (type: {type(back).__name__})")

# --- UPDATING JSON ---
print("\n4. Updating a JSON file:")
with open("config.json", "r") as f:
    data = json.load(f)

data["version"] = "1.1.0"
data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
data["database"]["port"] = 5433

with open("config.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"  Updated version to: {data['version']}")

# --- JSON LIST OF RECORDS ---
print("\n5. JSON array of records:")
employees = [
    {"id": "E001", "name": "Alice", "dept": "Eng",   "salary": 85000},
    {"id": "E002", "name": "Bob",   "dept": "Sales", "salary": 65000},
]

with open("employees.json", "w") as f:
    json.dump(employees, f, indent=2)

with open("employees.json", "r") as f:
    loaded_employees = json.load(f)

for emp in loaded_employees:
    print(f"  {emp['id']}: {emp['name']:<10} ${emp['salary']:,}")

# Cleanup
for fn in ["config.json", "employees.json"]:
    os.remove(fn)
print("\n  Cleaned up demo files.")
print("=" * 55)
