from config import Defaults, sort_key
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
        today = set()
        if today_data := load_csv(f"today_{date.today()}.csv", self._filepath):
            for today_item in today_data:
                today.add(today_item["id"])
        else:
            return

        for task in self.tasks:
            if not today:
                break
            if task.id in today:
                self.today_tasks.add(task)
                today.remove(task.id)

        return self.today_tasks

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
            today_list = [t.to_dict(only_id=True) for t in self.today_tasks]
            today_filename = f"today_{date.today()}.csv"
            sync_csv(today_filename, self._filepath, today_list, ("id",))

    def save_tasks_done(self):
        done_id = set()
        for task in load_csv("done.csv", self._filepath) or []:
            done_id.add(task["id"])

        done_tasks = []
        for task in self.done_tasks:
            if task.id not in done_id:
                done_tasks.append(DoneTask(task).to_dict())
        add_record_csv("done.csv", self._filepath, done_tasks, TASK_DONE_KEYS)

    def sync_tasks_done(self):
        done_tasks = []
        for task in self.done_tasks:
            done_tasks.append(DoneTask(task).to_dict())
        sync_csv("done.csv", self._filepath, done_tasks, TASK_DONE_KEYS)

    def add_to_search(self, string, task_list=None):
        self.search_results.clear()
        searched_tasks = []

        if task_list is None:
            task_list = self.tasks

        for task in task_list:
            if string.lower() in task.task.lower():
                searched_tasks.append(task)

        enumeration = 1
        sorted_tasks = list(sorted(searched_tasks, key=sort_key))
        for task in sorted_tasks:
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
        return len(tasks)

    def mark_tasks_done(self):
        for _, task in self.search_results:
            task.done = True
            task.done_date = date.today()
            self.tasks.update_task(task)
            self.done_tasks.add(DoneTask(task))

        self.search_results.clear()

    def update_task(self, task_string):
        id = self.search_results[0][1].id
        task_info = task_string.split(Defaults.TASK_SPLIT.value)[0]
        task_updated = task_parse.make_tasks(task_info)[0]
        task_updated.id = id

        # self.remove_from_today()
        self.today_tasks.add(task_updated)

        self.tasks.update_task(task_updated)

        self.search_results.clear()
        return task_updated

    def delete_task(self):
        for _, task in self.search_results:
            self.tasks.remove_task(task)
            if task in self.today_tasks:
                self.today_tasks.remove(task)

        self.search_results.clear()

    def make_today(self, amount=Defaults.TASK_AMOUNT.value):
        for _ in range(min(amount, len(self.tasks))):
            if (task := self.tasks.pop()) and task.done is False:
                self.today_tasks.add(task)

        self.tasks.push(self.today_tasks)

    def get_forecast(self):
        tomorrow = set()
        for _ in range(min(Defaults.TASK_AMOUNT.value, len(self.tasks))):
            if (task := self.tasks.pop()) and task.done is False:
                tomorrow.add(task)

        self.tasks.push(self.today_tasks)
        return tomorrow

    def add_to_today(self, new_tasks_str):
        if not new_tasks_str:
            return False

        new_tasks = self.add_tasks(new_tasks_str)
        self.today_tasks.update(new_tasks)
        return len(new_tasks)

    def remove_from_today(self):
        for _, task in self.search_results:
            if task in self.today_tasks:
                print("-- esta en today")
                self.today_tasks.remove(task)
            else:
                print("-- NO esta en today")

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
        self.sync_tasks_done()

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

    def encore_posible(self):
        return all([t.done for t in self.today_tasks])

    def encore_today(self, amount):
        self.make_today(amount=amount)
