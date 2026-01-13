import argparse
import json
import os
import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any
from rich.console import Console
from rich.table import Table

# --- CONFIGURATION ---
DATA_FILE = "tasks.json"
console = Console()

# --- DATA MODEL ---
@dataclass
class Task:
    """Class representing a single To-Do item."""
    id: int
    description: str
    category: str
    status: str = "Pending"
    created_at: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary for JSON storage."""
        return {
            "id": self.id,
            "description": self.description,
            "category": self.category,
            "status": self.status,
            "created_at": self.created_at
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Task':
        """Create a Task object from a dictionary."""
        return Task(
            id=data["id"],
            description=data["description"],
            category=data["category"],
            status=data["status"],
            created_at=data["created_at"]
        )

# --- LOGIC MANAGER ---
class TodoManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from the JSON file."""
        if not os.path.exists(DATA_FILE):
            return
        
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError):
            self.tasks = []

    def save_tasks(self):
        """Save current tasks to the JSON file."""
        with open(DATA_FILE, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(self, description: str, category: str):
        """Add a new task."""
        new_id = 1 if not self.tasks else max(t.id for t in self.tasks) + 1
        task = Task(id=new_id, description=description, category=category)
        self.tasks.append(task)
        self.save_tasks()

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as Done."""
        for task in self.tasks:
            if task.id == task_id:
                task.status = "Done ✅"
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        initial_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) < initial_count:
            self.save_tasks()
            return True
        return False

    def get_all_tasks(self) -> List[Task]:
        return self.tasks

# --- CLI & DISPLAY FUNCTIONS ---
def display_tasks(manager: TodoManager):
    """Render the list of tasks using Rich Table."""
    tasks = manager.get_all_tasks()
    
    if not tasks:
        console.print("[yellow]No tasks found. Add one using 'add'![/yellow]")
        return

    table = Table(title="Your To-Do List")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Category", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Created", style="dim")

    for task in tasks:
        status_color = "green" if "Done" in task.status else "red"
        table.add_row(
            str(task.id), 
            task.description, 
            task.category, 
            f"[{status_color}]{task.status}[/{status_color}]", 
            task.created_at
        )

    console.print(table)

def main():
    manager = TodoManager()
    
    parser = argparse.ArgumentParser(description="CLI To-Do List App")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Add
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("description", type=str, help="Task description")
    add_parser.add_argument("--cat", type=str, default="General", help="Category (e.g., Work, Personal)")

    # Command: List
    subparsers.add_parser("list", help="View all tasks")

    # Command: Done
    done_parser = subparsers.add_parser("done", help="Mark task as complete")
    done_parser.add_argument("id", type=int, help="Task ID to complete")

    # Command: Delete
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID to delete")

    args = parser.parse_args()

    # --- EXECUTION LOGIC ---
    if args.command == "add":
        manager.add_task(args.description, args.cat)
        console.print(f"[bold green]Task added successfully![/bold green]")

    elif args.command == "list":
        display_tasks(manager)

    elif args.command == "done":
        if manager.complete_task(args.id):
            console.print(f"[bold green]Task {args.id} marked as done![/bold green]")
        else:
            console.print(f"[bold red]Task {args.id} not found.[/bold red]")

    elif args.command == "delete":
        if manager.delete_task(args.id):
            console.print(f"[bold red]Task {args.id} deleted.[/bold red]")
        else:
            console.print(f"[bold red]Task {args.id} not found.[/bold red]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()