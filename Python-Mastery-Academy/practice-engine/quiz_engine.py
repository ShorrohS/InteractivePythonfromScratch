"""
Quiz Engine — Python Mastery Academy
Provides interactive quizzes for any phase.

HOW TO RUN:
  python quiz_engine.py

FEATURES:
  - Timed quizzes
  - Score tracking
  - Explanations for wrong answers
  - Phase-specific question banks
"""

import time
import random
import json
from datetime import datetime
from pathlib import Path


# ============================================================
# QUESTION BANK
# ============================================================

QUESTIONS = {
    "phase-01": [
        {
            "question": "What does print() do in Python?",
            "options": [
                "A) Sends data to a printer",
                "B) Displays output on the screen",
                "C) Creates a variable",
                "D) Imports a module"
            ],
            "answer": "B",
            "explanation": "print() is a built-in function that displays text or values to the console (screen)."
        },
        {
            "question": "Which data type stores whole numbers in Python?",
            "options": ["A) float", "B) str", "C) int", "D) bool"],
            "answer": "C",
            "explanation": "int stores whole numbers (integers) like 42, -5, 0. float stores decimals."
        },
        {
            "question": "What is the result of: type('42')?",
            "options": ["A) int", "B) float", "C) str", "D) num"],
            "answer": "C",
            "explanation": "'42' is a string because it's wrapped in quotes. Strings always have type str."
        },
        {
            "question": "Which operator is used for floor division (no decimal)?",
            "options": ["A) /", "B) //", "C) %", "D) **"],
            "answer": "B",
            "explanation": "// is floor division. 17 // 5 = 3 (not 3.4). The % operator gives the remainder."
        },
        {
            "question": "What does input() always return?",
            "options": ["A) int", "B) float", "C) str", "D) None"],
            "answer": "C",
            "explanation": "input() ALWAYS returns a string. Even if the user types a number, you must convert it: int(input())."
        },
        {
            "question": "Which f-string format shows 2 decimal places?",
            "options": [
                "A) f'{x:2}'",
                "B) f'{x:.2f}'",
                "C) f'{x:f2}'",
                "D) f'{x:2d}'"
            ],
            "answer": "B",
            "explanation": ":.2f means: format as float with 2 decimal places. f'{3.14159:.2f}' → '3.14'."
        },
        {
            "question": "What is the output of: print('Hi' * 3)?",
            "options": ["A) Hi3", "B) HiHiHi", "C) Hi Hi Hi", "D) Error"],
            "answer": "B",
            "explanation": "String * integer repeats the string. 'Hi' * 3 = 'HiHiHi'."
        },
        {
            "question": "Which is NOT a valid variable name?",
            "options": ["A) _score", "B) first_name", "C) 2nd_name", "D) salary2024"],
            "answer": "C",
            "explanation": "Variable names cannot start with a digit. 2nd_name is invalid. All others are valid."
        },
        {
            "question": "What does bool('') evaluate to?",
            "options": ["A) True", "B) False", "C) None", "D) Error"],
            "answer": "B",
            "explanation": "An empty string '' is falsy. bool('') returns False. Any non-empty string is truthy."
        },
        {
            "question": "What is the output of: 'hello'.upper()[:3]?",
            "options": ["A) hel", "B) HEL", "C) ello", "D) ELLO"],
            "answer": "B",
            "explanation": "'hello'.upper() returns 'HELLO'. [:3] slices the first 3 chars: 'HEL'."
        },
    ],
    "phase-02": [
        {
            "question": "Which keyword is used to exit a loop immediately?",
            "options": ["A) exit", "B) stop", "C) break", "D) end"],
            "answer": "C",
            "explanation": "break immediately exits the current loop. continue skips the current iteration."
        },
        {
            "question": "What does range(2, 10, 3) produce?",
            "options": [
                "A) [2, 5, 8]",
                "B) [2, 3, 4, ..., 9]",
                "C) [2, 4, 6, 8]",
                "D) [3, 6, 9]"
            ],
            "answer": "A",
            "explanation": "range(start=2, stop=10, step=3): starts at 2, adds 3 each time, stops before 10. → 2, 5, 8."
        },
        {
            "question": "How many times does 'loop' print?\nfor i in range(5):\n    print('loop')",
            "options": ["A) 4", "B) 5", "C) 6", "D) 0"],
            "answer": "B",
            "explanation": "range(5) generates [0, 1, 2, 3, 4] — 5 values, so the loop runs 5 times."
        },
        {
            "question": "What does the else clause in a for/while loop mean?",
            "options": [
                "A) Runs if loop body raised an error",
                "B) Runs after the loop if it didn't hit break",
                "C) Runs at the start of every iteration",
                "D) Required with every loop"
            ],
            "answer": "B",
            "explanation": "The else on a loop runs when the loop finishes normally (without hitting break)."
        },
        {
            "question": "What causes an infinite loop?",
            "options": [
                "A) Using while True",
                "B) A condition that never becomes False",
                "C) Not having a break statement",
                "D) B and C both"
            ],
            "answer": "B",
            "explanation": "An infinite loop occurs when the loop condition never becomes False. 'while True' with a break is fine."
        },
    ],
    "phase-03": [
        {
            "question": "Which collection type is ordered and mutable?",
            "options": ["A) tuple", "B) set", "C) frozenset", "D) list"],
            "answer": "D",
            "explanation": "list is ordered (maintains insertion order) and mutable (can be changed). tuple is immutable."
        },
        {
            "question": "What does [1, 2, 3, 4, 5][2:4] return?",
            "options": ["A) [2, 3]", "B) [3, 4]", "C) [2, 3, 4]", "D) [3, 4, 5]"],
            "answer": "B",
            "explanation": "Slicing [2:4] gets indices 2, 3 (not 4). Index 2 = 3, index 3 = 4. Result: [3, 4]."
        },
        {
            "question": "How do you access a dictionary value safely (no error if key missing)?",
            "options": [
                "A) d[key]",
                "B) d.get(key)",
                "C) d.find(key)",
                "D) d.access(key)"
            ],
            "answer": "B",
            "explanation": "d.get(key) returns None if key doesn't exist. d[key] raises KeyError."
        },
        {
            "question": "What is the result of: {1, 2, 3} & {2, 3, 4}?",
            "options": ["A) {1, 2, 3, 4}", "B) {2, 3}", "C) {1, 4}", "D) {1, 2, 3, 2, 3, 4}"],
            "answer": "B",
            "explanation": "& is set intersection — elements that appear in BOTH sets. {2, 3} appears in both."
        },
        {
            "question": "What does this list comprehension produce: [x**2 for x in range(1,4)]?",
            "options": ["A) [1, 4, 9]", "B) [1, 2, 3]", "C) [2, 4, 6]", "D) [1, 8, 27]"],
            "answer": "A",
            "explanation": "x**2 for x in [1,2,3]: 1²=1, 2²=4, 3²=9. Result: [1, 4, 9]."
        },
    ],
    "phase-07": [
        {
            "question": "What does __init__ do in a Python class?",
            "options": [
                "A) Initializes class-level variables",
                "B) Runs automatically when an instance is created",
                "C) Destroys the object",
                "D) Imports the class"
            ],
            "answer": "B",
            "explanation": "__init__ is the constructor. It runs automatically when you create a new instance with ClassName()."
        },
        {
            "question": "What is 'self' in a class method?",
            "options": [
                "A) A keyword reserved by Python",
                "B) A reference to the current instance",
                "C) The class name",
                "D) A required parameter name (must be 'self')"
            ],
            "answer": "B",
            "explanation": "self is a reference to the instance calling the method. It's a convention — you could name it anything, but 'self' is universal."
        },
        {
            "question": "How do you call the parent class's __init__ in a child class?",
            "options": [
                "A) parent.__init__(self)",
                "B) super().__init__()",
                "C) base.init()",
                "D) inherit()"
            ],
            "answer": "B",
            "explanation": "super().__init__() calls the parent class's __init__ method. This is how you properly extend parent initialization."
        },
        {
            "question": "What does isinstance(obj, ClassName) return for a child class instance?",
            "options": [
                "A) False — obj is the child type, not parent",
                "B) True — child is also an instance of parent",
                "C) None",
                "D) An error"
            ],
            "answer": "B",
            "explanation": "A child class instance IS an instance of the parent class. isinstance(Dog(), Animal) returns True."
        },
    ],
}


# ============================================================
# SCORE TRACKER
# ============================================================

class ScoreTracker:
    def __init__(self):
        self.session_scores = []
        self.score_file = Path("quiz_scores.json")
    
    def record_score(self, phase: str, score: int, total: int, time_taken: float):
        record = {
            "phase": phase,
            "score": score,
            "total": total,
            "percentage": round(score / total * 100, 1),
            "time_taken": round(time_taken, 1),
            "timestamp": datetime.now().isoformat()
        }
        self.session_scores.append(record)
        self._save_to_file(record)
    
    def _save_to_file(self, record: dict):
        scores = []
        if self.score_file.exists():
            with open(self.score_file) as f:
                scores = json.load(f)
        scores.append(record)
        with open(self.score_file, "w") as f:
            json.dump(scores, f, indent=2)
    
    def show_history(self):
        if not self.score_file.exists():
            print("  No quiz history yet.")
            return
        with open(self.score_file) as f:
            history = json.load(f)
        print(f"\n  {'Phase':<12} {'Score':>8} {'%':>6} {'Time':>8}  {'Date'}")
        print("  " + "─" * 55)
        for h in history[-10:]:   # Show last 10
            print(f"  {h['phase']:<12} {h['score']:>2}/{h['total']:<2}{h['percentage']:>6.0f}%  {h['time_taken']:>5.0f}s  {h['timestamp'][:10]}")


# ============================================================
# QUIZ ENGINE
# ============================================================

class QuizEngine:
    def __init__(self):
        self.tracker = ScoreTracker()
    
    def run_quiz(self, phase: str, num_questions: int = 5) -> None:
        """Run an interactive quiz for a specific phase."""
        
        if phase not in QUESTIONS:
            print(f"\n  ❌ No questions found for {phase}.")
            print(f"  Available: {', '.join(QUESTIONS.keys())}")
            return
        
        questions = QUESTIONS[phase].copy()
        random.shuffle(questions)
        questions = questions[:num_questions]
        
        print()
        print("=" * 55)
        print(f"  📚 QUIZ: {phase.upper().replace('-', ' ')}")
        print(f"  {num_questions} questions  |  Good luck!")
        print("=" * 55)
        
        score = 0
        start_time = time.time()
        
        for i, q in enumerate(questions, 1):
            print(f"\n  Question {i}/{num_questions}:")
            print(f"  {q['question']}")
            print()
            for option in q["options"]:
                print(f"  {option}")
            print()
            
            while True:
                answer = input("  Your answer (A/B/C/D): ").strip().upper()
                if answer in ("A", "B", "C", "D"):
                    break
                print("  Please enter A, B, C, or D")
            
            if answer == q["answer"]:
                print("  ✅ Correct!")
                score += 1
            else:
                print(f"  ❌ Incorrect. The answer is {q['answer']}.")
                print(f"  💡 {q['explanation']}")
        
        elapsed = time.time() - start_time
        percentage = score / num_questions * 100
        
        print()
        print("=" * 55)
        print(f"  QUIZ COMPLETE!")
        print(f"  Score:   {score}/{num_questions}  ({percentage:.0f}%)")
        print(f"  Time:    {elapsed:.0f} seconds")
        
        if percentage == 100:
            print("  🏆 Perfect score! Excellent!")
        elif percentage >= 80:
            print("  🥇 Great job! Ready for the next phase.")
        elif percentage >= 60:
            print("  👍 Good effort. Review the topics you missed.")
        else:
            print("  📚 Re-read the lessons for this phase.")
        
        print("=" * 55)
        
        self.tracker.record_score(phase, score, num_questions, elapsed)
    
    def main_menu(self):
        """Main quiz selection menu."""
        print()
        print("=" * 55)
        print("  🐍 PYTHON MASTERY ACADEMY — QUIZ ENGINE")
        print("=" * 55)
        
        while True:
            print()
            print("  Available Phases:")
            for i, phase in enumerate(QUESTIONS.keys(), 1):
                count = len(QUESTIONS[phase])
                print(f"  {i}. {phase.upper().replace('-', ' ')} ({count} questions)")
            print()
            print("  H. View Score History")
            print("  Q. Quit")
            print()
            
            choice = input("  Select phase (1-4, H, Q): ").strip().upper()
            
            phases = list(QUESTIONS.keys())
            
            if choice == "Q":
                print("  Good luck in your studies! 🐍")
                break
            elif choice == "H":
                self.tracker.show_history()
            elif choice.isdigit() and 1 <= int(choice) <= len(phases):
                phase = phases[int(choice) - 1]
                max_q = len(QUESTIONS[phase])
                try:
                    n = int(input(f"  How many questions? (1-{max_q}): "))
                    n = max(1, min(n, max_q))
                except ValueError:
                    n = 5
                self.run_quiz(phase, n)
            else:
                print("  Invalid choice.")


if __name__ == "__main__":
    engine = QuizEngine()
    engine.main_menu()
