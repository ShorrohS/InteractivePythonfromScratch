"""
Score Tracker — Python Mastery Academy
Tracks all quiz scores and progress across phases.

HOW TO RUN:
  python score_tracker.py

FEATURES:
  - View score history
  - Phase progress overview
  - Performance analytics
  - Export to CSV
"""

import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict


SCORES_FILE = "quiz_scores.json"


def load_scores() -> list:
    """Load all stored scores."""
    path = Path(SCORES_FILE)
    if not path.exists():
        return []
    with open(path) as f:
        return json.load(f)


def get_phase_summary(scores: list) -> dict:
    """Summarize scores per phase."""
    summary = defaultdict(lambda: {"attempts": 0, "total_score": 0, "total_possible": 0, "best_pct": 0})
    
    for s in scores:
        phase = s["phase"]
        summary[phase]["attempts"] += 1
        summary[phase]["total_score"] += s["score"]
        summary[phase]["total_possible"] += s["total"]
        pct = s["score"] / s["total"] * 100
        summary[phase]["best_pct"] = max(summary[phase]["best_pct"], pct)
    
    return dict(summary)


def display_phase_overview(scores: list) -> None:
    """Show progress across all phases."""
    if not scores:
        print("  No quiz scores found. Complete some quizzes first!")
        return
    
    summary = get_phase_summary(scores)
    
    print("\n  PHASE PROGRESS OVERVIEW")
    print(f"  {'Phase':<15} {'Attempts':>8} {'Best %':>8} {'Status':>10}")
    print("  " + "─" * 50)
    
    for phase, data in sorted(summary.items()):
        best = data["best_pct"]
        status = "✅ Passed" if best >= 80 else ("⚠️ Review" if best >= 60 else "❌ Retry")
        print(f"  {phase:<15} {data['attempts']:>8} {best:>7.0f}% {status:>10}")


def display_recent_scores(scores: list, n: int = 10) -> None:
    """Show the most recent quiz scores."""
    if not scores:
        print("  No scores to display.")
        return
    
    recent = scores[-n:][::-1]
    print(f"\n  LAST {len(recent)} QUIZ RESULTS")
    print(f"  {'Date':<12} {'Phase':<15} {'Score':>8} {'%':>6} {'Time':>7}")
    print("  " + "─" * 55)
    
    for s in recent:
        date = s["timestamp"][:10]
        pct = s["score"] / s["total"] * 100
        print(f"  {date:<12} {s['phase']:<15} {s['score']:>2}/{s['total']:<2} {pct:>5.0f}% {s['time_taken']:>5.0f}s")


def calculate_overall_stats(scores: list) -> dict:
    """Calculate overall statistics."""
    if not scores:
        return {}
    
    percentages = [s["score"] / s["total"] * 100 for s in scores]
    
    return {
        "total_attempts": len(scores),
        "phases_attempted": len(set(s["phase"] for s in scores)),
        "average_score": sum(percentages) / len(percentages),
        "best_score": max(percentages),
        "phases_passed": sum(1 for p, d in get_phase_summary(scores).items() if d["best_pct"] >= 80),
        "total_questions_answered": sum(s["total"] for s in scores),
        "total_correct": sum(s["score"] for s in scores),
    }


def export_to_csv(scores: list, filename: str = "quiz_history.csv") -> None:
    """Export all scores to CSV."""
    if not scores:
        print("  No data to export.")
        return
    
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=scores[0].keys())
        writer.writeheader()
        writer.writerows(scores)
    
    print(f"  ✅ Exported {len(scores)} records to {filename}")


def main():
    print("=" * 55)
    print("  📊 PYTHON MASTERY ACADEMY — SCORE TRACKER")
    print("=" * 55)
    
    scores = load_scores()
    
    while True:
        print()
        print("  [1] Phase Progress Overview")
        print("  [2] Recent Quiz Scores")
        print("  [3] Overall Statistics")
        print("  [4] Export to CSV")
        print("  [0] Exit")
        print()
        
        choice = input("  Option: ").strip()
        
        if choice == "1":
            display_phase_overview(scores)
        elif choice == "2":
            n = input("  How many recent scores to show? [10]: ").strip()
            n = int(n) if n.isdigit() else 10
            display_recent_scores(scores, n)
        elif choice == "3":
            stats = calculate_overall_stats(scores)
            if stats:
                print("\n  OVERALL STATISTICS")
                print("  " + "─" * 40)
                for k, v in stats.items():
                    label = k.replace("_", " ").title()
                    if isinstance(v, float):
                        print(f"  {label:<30} {v:.1f}%")
                    else:
                        print(f"  {label:<30} {v}")
            else:
                print("  No data available yet.")
        elif choice == "4":
            export_to_csv(scores)
        elif choice == "0":
            break
        else:
            print("  Invalid option.")


if __name__ == "__main__":
    main()
