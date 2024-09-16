import json
import os
from task_manager import Task

class Storage:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self.load_tasks()

    def save_task(self, task):
        self.tasks.append(task.__dict__)
        self.save_tasks()

    def update_task(self, updated_task):
        for i, task in enumerate(self.tasks):
            if task['title'] == updated_task.title:
                self.tasks[i] = updated_task.__dict__
                self.save_tasks()
                break

    def get_task(self, title):
        for task in self.tasks:
            if task['title'] == title:
                return Task(**task)
        return None

    def get_all_tasks(self):
        return [Task(**task) for task in self.tasks]

    def clear_all_tasks(self):
        self.tasks = []
        self.save_tasks()

    def save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, default=str)

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []
