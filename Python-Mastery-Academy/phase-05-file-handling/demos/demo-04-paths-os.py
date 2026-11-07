"""
Demo 04 - Paths & os Module
Phase 05: File Handling

Run: python demo-04-paths-os.py
"""

import os
from pathlib import Path

print("=" * 55)
print("DEMO 04 - File Paths and os Module")
print("=" * 55)

# --- CURRENT DIRECTORY ---
print("\n1. Working directory:")
print(f"  os.getcwd():     {os.getcwd()}")
print(f"  Path.cwd():      {Path.cwd()}")
print(f"  Path.home():     {Path.home()}")

# --- PATH BUILDING ---
print("\n2. Building paths:")
# Old way
path_os = os.path.join("data", "exports", "report.csv")
# Modern way
path_pl = Path("data") / "exports" / "report.csv"

print(f"  os.path.join:    {path_os}")
print(f"  pathlib:         {path_pl}")

# --- PATH COMPONENTS ---
print("\n3. Path components:")
p = Path("reports") / "sales" / "q4_2024.csv"
print(f"  Full path:  {p}")
print(f"  .name:      {p.name}")
print(f"  .stem:      {p.stem}")
print(f"  .suffix:    {p.suffix}")
print(f"  .parent:    {p.parent}")

# --- CREATING DIRECTORIES ---
print("\n4. Creating directory structure:")
test_dir = Path("_demo_workspace")
(test_dir / "src").mkdir(parents=True, exist_ok=True)
(test_dir / "data").mkdir(parents=True, exist_ok=True)
(test_dir / "output").mkdir(parents=True, exist_ok=True)

# Create some test files
(test_dir / "main.py").write_text("print('hello')")
(test_dir / "data" / "sales.csv").write_text("name,amount\nAlice,500")
(test_dir / "data" / "config.json").write_text('{"version": "1.0"}')

print(f"  Created: {test_dir}/")

# --- LISTING FILES ---
print("\n5. Listing files:")
for f in test_dir.rglob("*"):
    if f.is_file():
        size = f.stat().st_size
        print(f"  {f.relative_to(test_dir)}  ({size} bytes)")

# --- GLOB PATTERNS ---
print("\n6. Glob patterns:")
csv_files  = list(test_dir.rglob("*.csv"))
json_files = list(test_dir.rglob("*.json"))
py_files   = list(test_dir.rglob("*.py"))
print(f"  CSV files:  {[f.name for f in csv_files]}")
print(f"  JSON files: {[f.name for f in json_files]}")
print(f"  Py files:   {[f.name for f in py_files]}")

# --- SAFE OPERATIONS ---
print("\n7. Safe file check patterns:")
target = test_dir / "data" / "sales.csv"
print(f"  exists():   {target.exists()}")
print(f"  is_file():  {target.is_file()}")
print(f"  is_dir():   {target.is_dir()}")
print(f"  size (bytes): {target.stat().st_size}")

# --- CLEANUP ---
import shutil
shutil.rmtree(test_dir)
print(f"\n  Cleaned up: {test_dir}")
print("=" * 55)
