from datetime import datetime

class Task:
    def __init__(self, title, description, completed=False, created_at=None, completed_at=None):
        self.title = title
        self.description = description
        self.completed = completed
        self.created_at = datetime.fromisoformat(created_at) if created_at else datetime.now()
        self.completed_at = datetime.fromisoformat(completed_at) if completed_at else None

    def complete(self):
        self.completed = True
        self.completed_at = datetime.now()



class TaskManager:
    def __init__(self, storage):
        self.storage = storage

    def add_task(self, title, description):
        task = Task(title, description)
        self.storage.save_task(task)
        return task

    def complete_task(self, title):
        task = self.storage.get_task(title)
        if task:
            task.complete()
            self.storage.update_task(task)
            return True
        return False

    def list_tasks(self, include_completed=False):
        tasks = self.storage.get_all_tasks()
        if not include_completed:
            tasks = [task for task in tasks if not task.completed]
        return tasks

    def generate_report(self):
        tasks = self.storage.get_all_tasks()
        total_tasks = len(tasks)
        completed_tasks = [task for task in tasks if task.completed]
        num_completed = len(completed_tasks)
        num_pending = total_tasks - num_completed

        average_time = None
        if num_completed > 0:
            total_time = sum(
                (task.completed_at - task.created_at).total_seconds()
                for task in completed_tasks
            )
            average_time = total_time / num_completed / 3600  # Average time in hours

        report = {
            "total": total_tasks,
            "completed": num_completed,
            "pending": num_pending,
            "average_completion_time_hours": average_time
        }

        return report
