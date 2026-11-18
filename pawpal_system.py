
from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Task:
    """Represents a single pet care task."""
    description: str
    time: str
    frequency: str
    completed: bool = False

    def mark_complete(self):
        """Mark a task as completed and return its recurring copy."""
        self.completed = True

        if self.frequency == "Daily":
            return Task(self.description, self.time, self.frequency)

        if self.frequency == "Weekly":
            return Task(self.description, self.time, self.frequency)

        return None


@dataclass
class Pet:
    """Represents a pet belonging to an owner."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to the pet's schedule."""
        self.tasks.append(task)

    def get_tasks(self):
        """Return all tasks belonging to the pet."""
        return self.tasks


class Owner:
    """Represents a pet owner and their pets."""

    def __init__(self, name: str):
        self.name = name
        self.pets = []

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's account."""
        self.pets.append(pet)

    def get_all_tasks(self):
        """Return tasks belonging to all the owner's pets."""
        return [
            task
            for pet in self.pets
            for task in pet.get_tasks()
        ]


class Scheduler:
    """Manages and organizes pet care tasks."""

    def __init__(self, owner: Owner):
        self.owner = owner

    def get_all_tasks(self):
        """Return all tasks belonging to the owner."""
        return self.owner.get_all_tasks()

    def sort_by_time(self):
        """Sort all tasks chronologically, earliest to latest."""

        def convert_to_time(task):
            time_formats = [
                "%H:%M",
                "%I:%M %p",
                "%I:%M%p"
            ]

            for time_format in time_formats:
                try:
                    return datetime.strptime(
                        task.time.strip().upper(),
                        time_format
                    ).time()

                except ValueError:
                    continue

            # Place invalid or unrecognized times at the bottom
            return datetime.max.time()

        return sorted(
            self.get_all_tasks(),
            key=convert_to_time
        )

    def filter_tasks(self, pet_name=None, completed=None):
        """Filter tasks by pet name and completion status."""
        tasks = self.get_all_tasks()

        if pet_name is not None:
            filtered_tasks = []

            for pet in self.owner.pets:
                if pet.name.lower() == pet_name.lower():
                    filtered_tasks.extend(pet.get_tasks())

            tasks = filtered_tasks

        if completed is not None:
            tasks = [
                task
                for task in tasks
                if task.completed == completed
            ]

        return tasks

    def detect_conflicts(self):
        """Identify tasks scheduled at the same time."""
        tasks = self.get_all_tasks()
        conflicts = []

        for i, task in enumerate(tasks):

            for other_task in tasks[i + 1:]:

                if task.time == other_task.time:
                    conflicts.append((task, other_task))

        return conflicts
