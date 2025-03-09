from datetime import date


from taskParser import Parser
from config import Defaults
from fileLoaders import load_csv, add_tasks_to_csv
from task import Task
from heap import Heap

# - [] ToDo manager class
#   - invoke task methods (Update, mark done, mark not done)
#   - delete task

#   - set taks for today ->
#     - get all the tasks for today < 5
#     - get 5 by priority
#     - based on energy,
#       - put asside the able ones to delay
#       - add the next in line with the appropiate dificulty
# que si no encuentra la indicada? cual es el fallback???

#   - search tasks
#   - import - export task batches


class TaskManager:
    def __init__(self):
        self.lang = Defaults.LANG.value
        self.parser = Parser(self.lang)
        tasks_in_file = load_csv(Defaults.DATA_PATH.value, "tasks.csv")
        loaded_tasks = self.csv_to_tasks(tasks_in_file)
        self.global_heap = Heap(loaded_tasks)

    def add_tasks(self, task_string):
        tasks = self.parser.make_task(task_string)
        self.global_heap.push(tasks)
        tasks_dic = [task.to_dict() for task in tasks]
        add_tasks_to_csv(Defaults.DATA_PATH.value, "tasks.csv", tasks_dic)

    def update_task(self, task_id):
        pass

    def delete_task(self, task_id):
        pass

    def search_task(self, string):
        # Por task, por proyecto, por fecha de finalizacion \
        # usar distancia de cadenas
        pass

    def make_today_tasks_csv(self):
        pass

    def parse_csv_date(self, date_data):
        if date_data:
            return date.fromisoformat(date_data)
        else:
            return None

    def csv_to_tasks(self, tasks_list):
        tasks = []
        for task_line in tasks_list:
            task_dict = {
                "lang": task_line.get("lang"),
                "id": task_line.get("id"),
                "task": task_line.get("task"),
                "done": bool(task_line.get("done")),
                "creation_date": self.parse_csv_date(
                    task_line.get("creation_date"),
                ),
                "project": task_line.get("project"),
                "undelayable": bool(task_line.get("undelayable")),
                "dificulty": int(task_line.get("dificulty")),
                "due_date": self.parse_csv_date(task_line.get("due_date")),
            }
            tasks.append(Task(task_dict))

        return tasks
