from datetime import date

from taskParser import Parser
from config import Defaults
from fileLoaders import load_csv, add_tasks_to_csv, remove_tasks_from_csv
from task import Task
from heap import Heap

# - [] ToDo manager class
#   - invoke task methods (Update, mark done, mark not done)

#   - set taks for today ->
#     - get all the tasks for today < 5
#     - get 5 by priority
#     - based on energy,
#       - put asside the able ones to delay
#       - add the next in line with the appropiate dificulty
# que si no encuentra la indicada? cual es el fallback???

#   - import - export task batches


class TaskManager:
    def __init__(self):
        self.lang = Defaults.LANG.value
        self.parser = Parser(self.lang)
        self.heap = Heap()
        self.load_csv_to_heap()
        self.search_results = []
        self.today = []

    def load_csv_to_heap(self):
        self.heap.clear()
        tasks_in_file = load_csv(Defaults.DATA_PATH.value, "tasks.csv")
        loaded_tasks = self.csv_to_tasks(tasks_in_file)
        self.heap.push(loaded_tasks)

    def add_tasks(self, tasks_string):
        tasks = self.parser.make_task(tasks_string)
        self.heap.push(tasks)
        tasks_dic = [task.to_dict() for task in tasks]
        add_tasks_to_csv(Defaults.DATA_PATH.value, "tasks.csv", tasks_dic)

    def update_task(self, key, value):
        ids = []
        updated_tasks = []
        for _, task in self.search_results:
            setattr(task, key, value)
            ids.append(task.id)
            updated_tasks.append(task.to_dict())

        self.delete_task(ids)
        add_tasks_to_csv(Defaults.DATA_PATH.value, "tasks.csv", updated_tasks)
        self.search_results.clear()
        self.load_csv_to_heap()

    def delete_task(self, task_ids):
        remove_tasks_from_csv(Defaults.DATA_PATH.value, "tasks.csv", task_ids)
        self.load_csv_to_heap()

    def search_task(self, string):
        self.search_results.clear()
        for i, task in enumerate(self.heap, start=1):
            if string in task.task:
                self.search_results.append((i, task))

    def make_today_tasks_csv(self):
        pass

    def purge_done(self):
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
                "task_csv": task_line.get("task"),
                "done": task_line.get("done") == "True",
                "creation_date": self.parse_csv_date(
                    task_line.get("creation_date"),
                ),
                "project": task_line.get("project"),
                "undelayable": task_line.get("undelayable") == "True",
                "dificulty": int(task_line.get("dificulty")),
                "due_date": self.parse_csv_date(task_line.get("due_date")),
            }
            tasks.append(Task(task_dict))

        return tasks
