from datetime import date


from config import Defaults
from fileLoaders import load_csv
from task import Task
from heap import Heap

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
        tasks_in_file = load_csv(Defaults.DATA_PATH.value, "tasks.csv")
        loaded_tasks = self.csv_to_tasks(tasks_in_file)
        self.global_heap = Heap(loaded_tasks)

    # TODO: cambiar importante por inaplazable
    def csv_to_tasks(self, tasks_list):
        tasks = []
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
                "undelayable": bool(task_line.get("undelayable")),
                "dificulty": int(task_line.get("dificulty")),
                "due_date": date.fromisoformat(task_line.get("due_date")),
            }
            tasks.append(Task(task_dict))

        return tasks

    def save_csv(self):
        pass
