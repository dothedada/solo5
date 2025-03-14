from config import Defaults
import parser_task as task_parse
from fileManagers import load_csv, sync_csv, add_record_csv, clean_directory
from heap import Heap
from datetime import date, timedelta
from task import DoneTask, TASK_DONE_KEYS, TASK_KEYS


class TaskManager:
    def __init__(self):
        self._filepath = Defaults.DATA_PATH.value
        self._tasks = Heap()
        self.search_results = []
        self.today_tasks = set()
        self.load_csv_to_heap()
        self.load_csv_to_today()

    def load_csv_to_heap(self):
        self._tasks.clear()
        tasks_in_file = load_csv("tasks.csv", self._filepath)
        if tasks_in_file is None:
            return

        loaded_tasks = []
        cutoff_date = date.today() - timedelta(days=1)
        for task in tasks_in_file:
            done = task["done"] == "False"
            if done or cutoff_date < date.fromisoformat(task["done_date"]):
                loaded_tasks.append(task)

        tasks = task_parse.make_tasks_from_csv(loaded_tasks)
        self._tasks.push(tasks)

    def load_csv_to_today(self):
        today = load_csv(f"today_{date.today()}", self._filepath)
        if today is None:
            print("No tasks for today")
            return None

        today_tasks = task_parse.make_tasks_from_csv(today)
        for task in today_tasks:
            self.today_tasks.add(task)

    def save_tasks_to_csv(self):
        heap_list = [task.to_dict() for task in self._tasks]
        sync_csv("tasks.csv", self._filepath, heap_list, TASK_KEYS)

        if self.today_tasks:
            today_list = [task.to_dict() for task in self.today_tasks]
            today_filename = f"today_{date.today()}.csv"
            sync_csv(today_filename, self._filepath, today_list, TASK_KEYS)

    def add_to_search(self, tasks):
        index = 1

        if len(self.search_results):
            index = self.search_results[len(self.search_results) - 1][0]

        for task in tasks:
            self.search_results.append((index, task))
            index += 1

    def add_to_search_by_task(self, string, global_tasks=True):
        self.search_results.clear()
        task_list = self._tasks if global_tasks else self.today_tasks
        results = []
        for task in task_list:
            if string.lower() in task.task.lower():
                results.append(task)
        self.add_to_search(results)

    def add_to_search_by_date(self, date_string):
        self.search_results.clear()
        parsed_date = task_parse.get_date(date_string)
        tasks_list = list(
            filter(
                lambda item: str(item.due_date) == str(parsed_date),
                self._tasks,
            )
        )
        self.add_to_search(tasks_list)

    def select_from_search(self, selection, just_one=False):
        if just_one:
            selection = {min(selection)}

        selected_tasks = [t for t in self.search_results if t[0] in selection]
        self.search_results = selected_tasks

    def add_tasks(self, tasks_string):
        tasks = task_parse.make_task(tasks_string)
        self._tasks.push(tasks)

    def mark_tasks_done(self, is_done=True):
        for task in self.search_results:
            task[1].done = True if is_done else False
            task[1].done_date = date.today() if is_done else None

    def save_tasks_done(self):
        done_tasks = []
        done_id = set()
        for done_task in load_csv("done.csv", self._filepath) or []:
            done_id.add(done_task["id"])

        for task in self._tasks:
            if task.done and task.id not in done_id:
                done_tasks.append(DoneTask(task).to_dict())
        add_record_csv("done.csv", self._filepath, done_tasks, TASK_DONE_KEYS)

    def delete_task(self):
        tasks_ids = set()
        for task in self.search_results:
            tasks_ids.add(task[1].id)

        tasks = []
        for task in self._tasks:
            if task.id in tasks_ids:
                continue
            tasks.append(task)
        self._tasks.clear()
        self._tasks.push(tasks)
        self.search_results.clear()

    def update_task(self, task_string):
        self.delete_task()
        task_info = task_string.split(Defaults.TASK_SPLIT.value)[0]
        self.add_tasks(task_info)
        self.search_results.clear()

    def make_today(self):
        # TODO: Algoritmo de priorizacion
        for _ in range(min(Defaults.TASK_AMOUNT.value, len(self._tasks))):
            self.today_tasks.add(self._tasks.pop())

        filename = f"today_{date.today()}.csv"
        sync_csv(filename, self._filepath, self.today_tasks, TASK_KEYS)

    def get_today(self):
        today = []
        for i, task in enumerate(self.today_tasks):
            enumerator = f"{i}, done)" if task.done else f"{i})"
            today.append((enumerator, task))
        return today

    def add_to_today(self, new_tasks_str=""):
        if not self.search_results:
            return

        if new_tasks_str:
            new_tasks = self.add_tasks(new_tasks_str)
            self.add_to_search(new_tasks)

        for _, task in self.search_results:
            self.today_tasks.add(task)

        self.search_results.clear()

    def remove_from_today(self):
        for _, task in self.search_results:
            self.today_tasks.remove(task)

    def purge_done(self):
        today = date.today()
        month_ago = today - timedelta(days=30)

        # Purge old today files
        clean_directory("today_*.csv", self._filepath)

        # Purge heap tasks from heap
        tasks_not_done = []
        for task in self._tasks:
            if task.done:
                continue
            tasks_not_done.append(task)
        self._tasks.push(tasks_not_done)

        # Purge done tasks file from old done tasks
        tasks_done = []
        for task in load_csv("done.csv", self._filepath):
            done_date = date.fromisoformat(task["done_date"])
            if done_date < month_ago:
                continue
            tasks_done.append(task)

        # Save tasks
        self.save_tasks_to_csv()
        sync_csv("done.csv", self._filepath, tasks_done, TASK_DONE_KEYS)
