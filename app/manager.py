from config import Defaults
import parser_task as task_parse
from fileManagers import load_csv, sync_csv, add_record_csv, clean_directory
from heap import Heap
from datetime import date, timedelta
from task import DoneTask, TASK_DONE_KEYS, TASK_KEYS


class TaskManager:
    def __init__(self):
        self._filepath = Defaults.DATA_PATH.value
        self.tasks = Heap()
        self.search_results = []
        self.today_tasks = set()
        self.done_tasks = set()
        self.load_csv_to_heap()
        self.load_csv_to_today()
        self.load_csv_to_done()

    def load_csv_to_heap(self):
        self.tasks.clear()
        tasks_in_file = load_csv("tasks.csv", self._filepath)
        if tasks_in_file is None:
            return

        loaded_tasks = []
        cutoff_date = date.today() - timedelta(days=1)
        for task in tasks_in_file:
            done_date = task["done_date"]
            if done_date == "" or cutoff_date < date.fromisoformat(done_date):
                loaded_tasks.append(task)

        tasks = task_parse.make_tasks_from_csv(loaded_tasks)
        self.tasks.push(tasks)

    def load_csv_to_today(self):
        today = load_csv(f"today_{date.today()}", self._filepath)
        if today is None:
            print("NO TASKS FOR TODAY")
            return None

        today_tasks = task_parse.make_tasks_from_csv(today)
        for task in today_tasks:
            self.today_tasks.add(task)

    def load_csv_to_done(self):
        done = load_csv("done.csv", self._filepath)
        if done is None:
            return None

        if len(done):
            for task in done:
                self.done_tasks.add(DoneTask(task))
        return self.done_tasks

    def save_tasks_to_csv(self):
        heap_list = [task.to_dict() for task in self.tasks]
        sync_csv("tasks.csv", self._filepath, heap_list, TASK_KEYS)

        if self.today_tasks:
            today_list = [task.to_dict() for task in self.today_tasks]
            today_filename = f"today_{date.today()}.csv"
            sync_csv(today_filename, self._filepath, today_list, TASK_KEYS)

    def save_tasks_done(self):
        done_id = set()
        for task in load_csv("done.csv", self._filepath) or []:
            done_id.add(task["id"])

        done_tasks = []
        for task in self.done_tasks:
            if task.id not in done_id:
                done_tasks.append(DoneTask(task).to_dict())
        add_record_csv("done.csv", self._filepath, done_tasks, TASK_DONE_KEYS)

    def add_to_search(self, string, task_list=None):
        self.search_results.clear()
        searched_tasks = []

        if task_list is None:
            task_list = self.tasks

        for task in task_list:
            if string.lower() in task.task.lower():
                searched_tasks.append(task)

        sort_search = list(
            sorted(
                searched_tasks,
                key=lambda t: (
                    t.done,
                    t.due_date is None,
                    t.due_date or date.max,
                ),
            )
        )

        enumeration = 1
        for task in sort_search:
            self.search_results.append((enumeration, task))
            enumeration += 1

    def select_from_search(self, selection):
        selected_tasks = []
        new_index = 1
        for old_index, task in self.search_results:
            if old_index in selection:
                selected_tasks.append((new_index, task))
                new_index += 1
        self.search_results = selected_tasks

    def add_tasks(self, tasks_string):
        tasks = task_parse.make_tasks(tasks_string)
        self.tasks.push(tasks)

    def mark_tasks_done(self, is_done=True):
        for _, task in self.search_results:
            task.done = True if is_done else False
            task.done_date = date.today()
            self.tasks.update_task(task)
            self.done_tasks.add(DoneTask(task))

        self.search_results.clear()

    def update_task(self, task_string):
        id = self.search_results[0][1].id
        task_info = task_string.split(Defaults.TASK_SPLIT.value)[0]
        task_updated = task_parse.make_tasks(task_info)[0]
        task_updated.id = id
        self.tasks.update_task(task_updated)

        self.search_results.clear()
        return task_updated

    def delete_task(self):
        for _, task in self.search_results:
            self.tasks.remove_task(task)

        self.search_results.clear()

    def make_today(self):
        # TODO: Algoritmo de priorizacion
        for i in range(min(Defaults.TASK_AMOUNT.value, len(self.tasks))):
            self.today_tasks.add(self.tasks.pop())

        self.tasks.push(self.today_tasks)
        # filename = f"today_{date.today()}.csv"
        # sync_csv(filename, self._filepath, self.today_tasks, TASK_KEYS)

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
        for task in self.tasks:
            if task.done:
                continue
            tasks_not_done.append(task)
        self.tasks.clear()
        self.tasks.push(tasks_not_done)

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

    def fix_dates(self):
        today = date.today()
        self.search_results.clear()
        fix_tasks = []
        for task in self.tasks:
            if task.due_date and task.due_date < today:
                old_d = task.due_date
                self.search_results.append((0, task))
                new_task = self.update_task(task.task)
                fix_tasks.append([new_task.task, old_d, new_task.due_date])

        return fix_tasks
