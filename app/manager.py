from datetime import date


from config import Defaults
from fileLoaders import load_csv
from task import Task

# - [] ToDo manager class
#   - Load tasks
#   - Make heap tasks available
#   - Make heaps by dificulty
#   - Make heaps by project

#   - invoke task methods (Update, mark done, mark not done)
#   - delete task

#   - set taks for today ->
#     - get all the tasks for today < 5
#     - get 5 by priority
#     - based on energy,
#       - put asside the able ones to delay
#       - add the next in line with the appropiate dificulty

#   - search tasks
#   - import - export task batches


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.csv_to_tasks(Defaults.DATA_PATH.value, "tasks.csv")

    def csv_to_tasks(self, path, filename):
        tasks_list = load_csv(path, filename)
        for task_line in tasks_list:
            task_dict = {
                "lang": task_line.get("lang"),
                "id": task_line.get("id"),
                "task": task_line.get("task"),
                "done": bool(task_line.get("done")),
                "creation_date": date.fromisoformat(
                    task_line.get("creation_date"),
                ),
                "project": task_line.get("project"),
                "important": bool(task_line.get("important")),
                "dificulty": int(task_line.get("dificulty")),
                "due_date": date.fromisoformat(task_line.get("due_date")),
            }
            self.tasks.append(Task(task_dict))

    def save_csv(self):
        pass
