from config import Defaults
from taskParser import Parser
from fileManagers import load_csv, sync_csv, add_record_csv
from heap import Heap
from datetime import date, timedelta
from task import DoneTask, TASK_DONE_KEYS, TASK_KEYS


class TaskManager:
    def __init__(self):
        self._filepath = Defaults.DATA_PATH.value
        self._parser = Parser(Defaults.LANG.value)
        self._tasks = Heap()
        self.search_results = []
        self.today_tasks = set()
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
        parsed_date = self._parser.parse_date(date_string)
        tasks_list = list(
            filter(
                lambda item: str(item.due_date) == str(parsed_date),
                self._tasks,
            )
        )
        self.add_to_search(tasks_list)

    def select_from_search(self, selection_str, just_one=False):
        selection_str = selection_str.strip(" ,-")
        if selection_str == "0":
            self.search_results.clear()
            return None

        select = set()
        for char in selection_str.split(","):
            char = char.strip()
            if char.isdigit():
                select.add(int(char))
            elif char.count("-") == 1:
                try:
                    start, end = map(str.strip, char.split("-"))
                    if not start.isdigit() or not end.isdigit():
                        raise ValueError(f"Invalid format: {char}")
                    select.update(range(int(start), int(end) + 1))
                except ValueError:
                    raise ValueError(f"Invalid format: {char}")
            else:
                raise ValueError(f"Invalid format: {char}")

        if just_one and len(select) > 1:
            raise Exception("Select only one")

        if not all(0 < i <= len(self.search_results) for i in select):
            raise ValueError("Selection must be within the search range")

        selected = [task for task in self.search_results if task[0] in select]
        self.search_results = selected

    def add_tasks(self, tasks_string):
        tasks = self._parser.make_task(tasks_string)
        self._tasks.push(tasks)
        return tasks

    def mark_tasks_done(self):
        done_tasks = []
        for task in self.search_results:
            done_tasks.append(DoneTask(task[1]))
            task[1].done = True

    def save_tasks_done(self):
        done_tasks = []
        for task in self._tasks:
            if task.done:
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
        if len(self.search_results) != 1 or task_string is None:
            return None

        task_info = task_string.split(Defaults.TASK_SPLIT.value)[0]
        self.delete_task()
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

    # def purge_done(self):
    #     done_ids = set()
    #     yesterday = date.today() - timedelta(days=1)
    #     month_ago = date.today() - timedelta(days=30)
    #     trash_can = []
    #     for done_task in load_csv("done.csv", self._filepath):
    #         done_date = date.fromisoformat(done_task["done_date"])
    #         if yesterday >= done_date:
    #             done_ids.add(done_task["id"])
    #         if month_ago <= done_date:
    #             trash_can.append(done_task)
    #
    #     avaliable_tasks = []
    #     for task in self._tasks:
    #         if task.id in done_ids:
    #             continue
    #         avaliable_tasks.append(task)
    #     self._tasks.clear()
    #     self.add_tasks(avaliable_tasks)
    #     sync_csv("done.csv", self._filepath, trash_can, TASK_DONE_KEYS)
