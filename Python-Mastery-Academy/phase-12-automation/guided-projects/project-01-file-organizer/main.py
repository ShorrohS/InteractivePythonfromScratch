"""
Project 01 - File Organizer
Phase 12: Automation

SKILLS PRACTICED:
  - os and pathlib for file system operations
  - Moving and copying files
  - Building file extension rules
  - Logging operations
  - Dry-run mode (preview before executing)

HOW TO RUN:
  python main.py

  By default, organizes the current directory.
  Use --dry-run to preview without moving files.
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────────────────

RULES: dict[str, list[str]] = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg", ".ico"],
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".md", ".csv", ".xlsx", ".pptx"],
    "Videos":     [".mp4", ".avi", ".mov", ".mkv", ".wmv", ".flv"],
    "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c",
                   ".go", ".rs", ".sql", ".sh", ".json", ".yaml", ".toml"],
    "Data":       [".json", ".xml", ".csv", ".db", ".sqlite"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm"],
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("organizer.log")
    ]
)
logger = logging.getLogger(__name__)


# ── Core Functions ──────────────────────────────────────────────────────────

def get_category(extension: str) -> str:
    """Return category folder for a given file extension."""
    ext = extension.lower()
    for category, extensions in RULES.items():
        if ext in extensions:
            return category
    return "Other"


def organize_directory(source_dir: str = ".",
                        target_dir: str = None,
                        dry_run: bool = False,
                        recursive: bool = False) -> dict:
    """
    Organize files in source_dir by moving them to category folders.

    Returns:
        Summary dict with counts per category and any errors
    """
    source = Path(source_dir).resolve()
    target = Path(target_dir).resolve() if target_dir else source

    if not source.exists():
        raise FileNotFoundError(f"Source directory not found: {source}")

    summary = {"moved": 0, "skipped": 0, "errors": 0, "categories": {}}
    mode = "DRY RUN" if dry_run else "LIVE"

    logger.info(f"[{mode}] Organizing: {source}")

    # Get files to process
    if recursive:
        files = [f for f in source.rglob("*") if f.is_file()]
    else:
        files = [f for f in source.iterdir() if f.is_file()]

    # Skip organizer itself and its log
    skip_names = {"organizer.log", "main.py", "__pycache__"}
    files = [f for f in files if f.name not in skip_names and not f.suffix == ".pyc"]

    for file_path in files:
        category = get_category(file_path.suffix)
        dest_dir  = target / category
        dest_file = dest_dir / file_path.name

        # Handle duplicate filenames
        if dest_file.exists():
            stem      = file_path.stem
            suffix    = file_path.suffix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_file = dest_dir / f"{stem}_{timestamp}{suffix}"

        if dry_run:
            logger.info(f"  WOULD MOVE: {file_path.name} → {category}/")
        else:
            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(dest_file))
                logger.info(f"  MOVED: {file_path.name} → {category}/")
            except (PermissionError, shutil.Error) as e:
                logger.error(f"  ERROR moving {file_path.name}: {e}")
                summary["errors"] += 1
                continue

        summary["moved"] += 1
        summary["categories"][category] = summary["categories"].get(category, 0) + 1

    return summary


def print_summary(summary: dict) -> None:
    """Print organization summary."""
    print("\n  SUMMARY")
    print("  " + "-" * 35)
    print(f"  Files processed: {summary['moved']}")
    print(f"  Errors:          {summary['errors']}")
    print()
    if summary["categories"]:
        print("  By category:")
        for cat, count in sorted(summary["categories"].items(), key=lambda x: x[1], reverse=True):
            print(f"    {cat:<15} {count:>3} file(s)")


def analyze_directory(directory: str = ".") -> dict:
    """Analyze directory without moving anything."""
    source = Path(directory).resolve()
    analysis = {}

    for f in source.iterdir():
        if f.is_file():
            cat = get_category(f.suffix)
            if cat not in analysis:
                analysis[cat] = {"count": 0, "size": 0, "files": []}
            analysis[cat]["count"] += 1
            analysis[cat]["size"]  += f.stat().st_size
            analysis[cat]["files"].append(f.name)

    return analysis


def main():
    print("=" * 55)
    print("  FILE ORGANIZER")
    print("=" * 55)
    print("\n  Organizes files in a directory by type.")
    print("  Default: current directory.")

    directory = input("\n  Directory to organize [.]: ").strip() or "."
    dry_run   = input("  Dry run first? (yes/no) [yes]: ").strip().lower() != "no"

    # Analyze first
    print(f"\n  Analyzing: {Path(directory).resolve()}")
    try:
        analysis = analyze_directory(directory)
    except FileNotFoundError as e:
        print(f"  Error: {e}")
        return

    if not analysis:
        print("  No files found in directory.")
        return

    total = sum(v["count"] for v in analysis.values())
    print(f"\n  Found {total} file(s) to organize:")
    print(f"  {'Category':<15} {'Files':>6}")
    print("  " + "-" * 24)
    for cat, data in sorted(analysis.items()):
        print(f"  {cat:<15} {data['count']:>6}")

    if not input("\n  Proceed? (yes/no): ").strip().lower() in ("yes", "y"):
        print("  Cancelled.")
        return

    try:
        summary = organize_directory(
            source_dir=directory,
            dry_run=dry_run
        )
        print_summary(summary)

        if dry_run and summary["moved"] > 0:
            if input("\n  Execute for real? (yes/no): ").strip().lower() in ("yes", "y"):
                summary = organize_directory(source_dir=directory, dry_run=False)
                print_summary(summary)
                print("\n  Organization complete!")

    except FileNotFoundError as e:
        print(f"  Error: {e}")
    except PermissionError:
        print("  Permission denied. Try running as administrator.")


if __name__ == "__main__":
    main()
