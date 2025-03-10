from datetime import date

from taskParser import Parser
from config import Defaults
from fileLoaders import load_csv, sync_csv
from task import Task
from heap import Heap
import functools

#   - set taks for today ->
#     - get all the tasks for today < 5
#     - get 5 by priority
#     - based on energy,
#       - put asside the able ones to delay
#       - add the next in line with the appropiate dificulty
# que si no encuentra la indicada? cual es el fallback???


# NOTE: Evaluar si implemento decorador
def sync_to_heap(filename, heap):
    def decorator(func):
        functools.wraps(func)

        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            heap_list = [task.to_dict() for task in heap]
            sync_csv(filename, heap_list)

        return wrapper

    return decorator


class TaskManager:
    def __init__(self):
        self.parser = Parser(Defaults.LANG.value)
        self.heap = Heap()
        self.load_csv_to_heap()
        self.search_results = []
        self.today = []

    def load_csv_to_heap(self):
        self.heap.clear()
        tasks_in_file = load_csv("tasks.csv")
        loaded_tasks = self.csv_to_tasks(tasks_in_file)
        self.heap.push(loaded_tasks)

    def sync_csv_to_heap(self):
        heap_list = [task.to_dict() for task in self.heap]
        sync_csv("tasks.csv", heap_list)

    def search_by_task(self, string, at_task_repository):
        self.search_results.clear()
        for i, task in enumerate(at_task_repository, start=1):
            if string in task.task:
                self.search_results.append((i, task))

    def search_by_date(self, date_string, at_task_repository):
        self.search_results.clear()
        date = self.parser.parse_date(date_string)
        for i, task in enumerate(at_task_repository, start=1):
            if f"{date:%Y-%m-%d}" == task.date:
                self.search_results.append((i, task))

    def select_from_search(self, enumerator):
        # All tasks
        if int(enumerator) == 0:
            return None

        return filter(
            lambda item: item[0] == int(enumerator),
            self.search_results,
        )

    def add_tasks(self, tasks_string):
        tasks = self.parser(tasks_string)
        self.heap.push(tasks)
        self.sync_csv_to_heap()

    def update_task(self, string):
        if len(self.search_results) != 1:
            return None

        task_string = string.split(Defaults.TASK_SPLIT.value)[0]
        new_task_info = self.parser.make_task(task_string)
        task_update = self.search_results[0][1]
        task_update.update_properties(**new_task_info)
        self.search_results.clear()
        return task_update

    def set_task_done(self, is_done):
        if len(self.search_results) > 1:
            return None

        task = self.search_results[0][1]
        task.update_properties(done=is_done)
        self.search_results.clear()
        # TODO: if is_done # Evaluar el flujo con done.csv
        # -> grabar en done.csv,
        # -> borrar de tasks.csv
        # else
        # -> grabar en tasks.csv
        # -> borrar de done.csv

    def delete_task(self):
        if len(self.search_results) != 1:
            return None

        task_id = self.search_results[0][1].id
        new_tasks = []
        for task in self.heap:
            if task.id == task_id:
                continue
            new_tasks.append(task)
        self.heap.push(new_tasks)
        self.search_results.clear()

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
