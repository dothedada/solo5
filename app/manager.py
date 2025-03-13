from config import Defaults
from taskParser import Parser
from fileManagers import load_csv, sync_csv, add_record_csv
from heap import Heap
from datetime import date, timedelta
from task import DoneTask, KEYS_DONE_TASK, KEYS_ALLOWED


class TaskManager:
    def __init__(self):
        self._filepath = Defaults.DATA_PATH.value
        self._parser = Parser(Defaults.LANG.value)
        self._tasks = Heap()
        self.search_results = []
        self.today_tasks = []
        self.load_csv_to_heap()
        self.load_csv_to_today()

    def load_csv_to_heap(self):
        self._tasks.clear()
        tasks_in_file = load_csv("tasks.csv", self._filepath)
        loaded_tasks = self._parser.make_tasks_from_csv(tasks_in_file)
        self._tasks.push(loaded_tasks)

    def load_csv_to_today(self):
        today = load_csv(f"today_{date.today()}", self._filepath)
        if today is None:
            print("No tasks for today")
            return None

        today_tasks = self._parser.make_tasks_from_csv(today)
        for task in today_tasks:
            self.today_tasks.append(task)

    def save_tasks_to_csv(self):
        heap_list = [task.to_dict() for task in self._tasks]
        sync_csv("tasks.csv", self._filepath, heap_list, KEYS_ALLOWED)

        if self.today_tasks:
            today_list = [task.to_dict() for task in self.today_tasks]
            today_filename = f"today_{date.today()}.csv"
            sync_csv(today_filename, self._filepath, today_list, KEYS_ALLOWED)

    def add_to_search_by_task(self, string):
        self.search_results.clear()
        number = 1
        for task in self._tasks:
            if string in task.task:
                self.search_results.append((number, task))
                number += 1
        return self.search_results

    # NOTE: Pendiente de testeo
    def add_to_search_by_date(self, date_string):
        self.search_results.clear()
        parsed_date = self._parser.parse_date(date_string)
        for i, task in enumerate(self._tasks, start=1):
            if f"{parsed_date:%Y-%m-%d}" == str(task.date):
                self.search_results.append((i, task))
        return self.search_results

    def search_output(self):
        return self.search_results

    def select_from_search(self, selection_str):
        if "0" in selection_str:
            self.search_results.clear()
            return None

        selection = []
        # BUG: cuando la cadena termina en ,
        for char in selection_str.split(","):
            char = char.strip()
            if char.isdigit():
                selection.append(int(char.strip()))
            else:
                try:
                    start, end = char.split("-")
                    start = start.strip()
                    end = end.strip()
                    secuence = [i for i in range(int(start), int(end) + 1)]
                    selection.extend(secuence)
                except ValueError:
                    raise ValueError(f"Invalid format: {char}")

        selection = set(selection)

        self.search_results = [
            item for item in self.search_results if item[0] in selection
        ]
        return self.search_results

    def add_tasks(self, tasks_string):
        tasks = self._parser.make_task(tasks_string)
        self._tasks.push(tasks)

    def mark_tasks_done(self):
        done_tasks = []
        for task in self.search_results:
            done_tasks.append(DoneTask(task[1]))
            task[1].done = True

        done_tasks = [task.to_dict() for task in done_tasks]
        self.search_results.clear()
        add_record_csv("done.csv", self._filepath, done_tasks, KEYS_DONE_TASK)

    def delete_task(self):
        tasks_ids = set()
        for task in self.search_results:
            tasks_ids.add(task[1].id)

        tasks = [task for task in self._tasks if task.id not in tasks_ids]
        self._tasks.clear()
        self._tasks.push(tasks)

    def update_task(self, task_string):
        if len(self.search_results) != 1 or task_string is None:
            return None

        task_info = task_string.split(Defaults.TASK_SPLIT.value)[0]
        self.delete_task()
        self.add_tasks(task_info)

    def make_today_tasks(self):
        # TODO: Algoritmo de priorizacion
        for _ in range(Defaults.TASK_AMOUNT.value):
            self.today_tasks.append(self._tasks.pop())

        filename = f"today_{date.today()}.csv"
        sync_csv(filename, self._filepath, self.today_tasks, KEYS_ALLOWED)

    def add_to_today_tasks(self):
        for _, task in self.search_results:
            self.today_tasks.append(task)
        self.search_results.clear()

    def remove_from_today_tasks(self, task):
        if len(self.search_results) != 1:
            return None

        task_id = self.search_results[0][1].id
        self.search_results.clear()
        self.today_tasks = [task for task in self.today_tasks if task_id != task.id]

    def print_today(self):
        today = []
        for i, task in enumerate(self.today_tasks):
            enumerator = "X" if task.done else i
            today.append(enumerator, task)
        return today

    def purge_done(self):
        done_ids = set()
        yesterday = date.today() - timedelta(days=1)
        month_ago = date.today() - timedelta(days=30)
        trash_can = []
        for done_task in load_csv("done.csv", self._filepath):
            done_date = date.fromisoformat(done_task["done_date"])
            if yesterday >= done_date:
                done_ids.add(done_task["id"])
            if month_ago <= done_date:
                trash_can.append(done_task)

        avaliable_tasks = []
        for task in self._tasks:
            if task.id in done_ids:
                continue
            avaliable_tasks.append(task)
        self._tasks.clear()
        self.add_tasks(avaliable_tasks)
        sync_csv("done.csv", self._filepath, trash_can, KEYS_DONE_TASK)
