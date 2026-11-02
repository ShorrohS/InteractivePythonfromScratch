"""
To-Do Application
Phase 08: Intermediate Projects

FEATURES:
  - Add, list, complete, delete tasks
  - Mark tasks as priority
  - Persistent storage (JSON file)
  - Filter by status

SKILLS USED:
  - OOP (Task, TodoApp classes)
  - File handling (JSON)
  - List and dictionary operations
  - Input validation
  - Error handling

HOW TO RUN:
  python main.py
"""

import json
import os
from datetime import datetime
from enum import Enum


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task:
    """Represents a single to-do task."""
    
    def __init__(self, title: str, priority: Priority = Priority.MEDIUM, notes: str = ""):
        self.id = None
        self.title = title
        self.priority = priority
        self.notes = notes
        self.completed = False
        self.created_at = datetime.now().isoformat()
        self.completed_at = None
    
    def complete(self) -> None:
        """Mark task as completed."""
        self.completed = True
        self.completed_at = datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority.value,
            "notes": self.notes,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        task = cls(data["title"], Priority(data["priority"]), data.get("notes", ""))
        task.id = data["id"]
        task.completed = data["completed"]
        task.created_at = data["created_at"]
        task.completed_at = data.get("completed_at")
        return task
    
    def __str__(self) -> str:
        status = "✅" if self.completed else "⬜"
        priority_icons = {Priority.HIGH: "🔴", Priority.MEDIUM: "🟡", Priority.LOW: "🟢"}
        icon = priority_icons.get(self.priority, "🟡")
        return f"  {status} [{self.id:03d}] {icon} {self.title}"


class TodoApp:
    """To-Do Application Manager."""
    
    def __init__(self, storage_file: str = "tasks.json"):
        self.storage_file = storage_file
        self.tasks: list[Task] = []
        self._next_id = 1
        self.load()
    
    def load(self) -> None:
        """Load tasks from file."""
        if os.path.exists(self.storage_file):
            with open(self.storage_file) as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(t) for t in data["tasks"]]
                self._next_id = data.get("next_id", len(self.tasks) + 1)
    
    def save(self) -> None:
        """Save tasks to file."""
        with open(self.storage_file, "w") as f:
            json.dump({
                "tasks": [t.to_dict() for t in self.tasks],
                "next_id": self._next_id
            }, f, indent=2)
    
    def add_task(self, title: str, priority: str = "medium", notes: str = "") -> Task:
        """Add a new task."""
        task = Task(title, Priority(priority.lower()), notes)
        task.id = self._next_id
        self._next_id += 1
        self.tasks.append(task)
        self.save()
        return task
    
    def get_task(self, task_id: int) -> Task | None:
        """Find task by ID."""
        return next((t for t in self.tasks if t.id == task_id), None)
    
    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete."""
        task = self.get_task(task_id)
        if task and not task.completed:
            task.complete()
            self.save()
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save()
            return True
        return False
    
    def get_pending(self) -> list[Task]:
        return [t for t in self.tasks if not t.completed]
    
    def get_completed(self) -> list[Task]:
        return [t for t in self.tasks if t.completed]
    
    def display_tasks(self, tasks: list[Task] | None = None) -> None:
        """Display a list of tasks."""
        if tasks is None:
            tasks = self.tasks
        
        if not tasks:
            print("  No tasks found.")
            return
        
        # Group by priority
        for priority in [Priority.HIGH, Priority.MEDIUM, Priority.LOW]:
            group = [t for t in tasks if t.priority == priority]
            if group:
                print(f"\n  {priority.value.upper()} PRIORITY:")
                for task in group:
                    print(task)
                    if task.notes:
                        print(f"        📝 {task.notes}")
    
    def summary(self) -> None:
        total = len(self.tasks)
        done = len(self.get_completed())
        pending = len(self.get_pending())
        pct = (done / total * 100) if total > 0 else 0
        print(f"\n  Total: {total} | Completed: {done} | Pending: {pending} | {pct:.0f}% done")


def main():
    """Main application loop."""
    app = TodoApp()
    
    print("=" * 50)
    print("  ✅ TO-DO APPLICATION")
    print("  Powered by Python OOP")
    print("=" * 50)
    
    while True:
        app.summary()
        print()
        print("  [1] View All Tasks")
        print("  [2] View Pending Tasks")
        print("  [3] Add New Task")
        print("  [4] Complete Task")
        print("  [5] Delete Task")
        print("  [6] View Completed Tasks")
        print("  [0] Exit")
        print()
        
        choice = input("  Option: ").strip()
        print()
        
        if choice == "1":
            print("  ALL TASKS:")
            app.display_tasks()
            
        elif choice == "2":
            pending = app.get_pending()
            print(f"  PENDING TASKS ({len(pending)}):")
            app.display_tasks(pending)
            
        elif choice == "3":
            title = input("  Task title: ").strip()
            if not title:
                print("  ❌ Title cannot be empty.")
                continue
            
            print("  Priority: (1) High  (2) Medium  (3) Low")
            p_choice = input("  Priority [2]: ").strip()
            priority_map = {"1": "high", "2": "medium", "3": "low"}
            priority = priority_map.get(p_choice, "medium")
            
            notes = input("  Notes (optional): ").strip()
            task = app.add_task(title, priority, notes)
            print(f"  ✅ Task added: {task}")
            
        elif choice == "4":
            try:
                task_id = int(input("  Enter task ID to complete: "))
                if app.complete_task(task_id):
                    print(f"  ✅ Task {task_id} marked as complete!")
                else:
                    print("  ❌ Task not found or already complete.")
            except ValueError:
                print("  ❌ Invalid ID.")
                
        elif choice == "5":
            try:
                task_id = int(input("  Enter task ID to delete: "))
                confirm = input(f"  Delete task {task_id}? (yes/no): ")
                if confirm.lower() == "yes":
                    if app.delete_task(task_id):
                        print(f"  ✅ Task {task_id} deleted.")
                    else:
                        print("  ❌ Task not found.")
            except ValueError:
                print("  ❌ Invalid ID.")
                
        elif choice == "6":
            completed = app.get_completed()
            print(f"  COMPLETED TASKS ({len(completed)}):")
            app.display_tasks(completed)
            
        elif choice == "0":
            print("  Goodbye! Keep being productive. ✅")
            break
        else:
            print("  ❌ Invalid option. Choose 0-6.")
        
        input("\n  Press Enter to continue...")
        print("\n" + "─" * 50)


if __name__ == "__main__":
    main()
