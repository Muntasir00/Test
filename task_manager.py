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
        pending_tasks = total_tasks - len(completed_tasks)

        #Average time for completed tasks
        if completed_tasks:
             total_time = sum(
				(task.completed_at - task.created_at).total_seconds()
				for task in completed_tasks
				if task.completed_at is not None and task.created_at is not None
        )
             average_time = total_time / len(completed_tasks)
        else:
            average_time = 0 # Average Time 0 for no completed tasks

        report = {
            "total": total_tasks,
            "completed": len(completed_tasks),
            "pending": pending_tasks,
            "average_completion_time_hours": average_time
        }

        return report
