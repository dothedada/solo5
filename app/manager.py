from config import Defaults
from taskParser import Parser
from fileManagers import load_csv, sync_csv, add_record_csv
from heap import Heap
from task import DoneTask, KEYS_DONE_TASK


class TaskManager:
    def __init__(self):
        self.parser = Parser(Defaults.LANG.value)
        self.heap = Heap()
        self.load_csv_to_heap()
        self.search_results = []
        self.today = []

    def load_csv_to_heap(self):
        self.heap.clear()
        tasks_in_file = load_csv("tasks.csv", Defaults.DATA_PATH.value)
        loaded_tasks = self.parser.make_tasks_from_csv(tasks_in_file)
        self.heap.push(loaded_tasks)

    def update_csv_from_heap(self):
        heap_list = [task.to_dict() for task in self.heap]
        sync_csv("tasks.csv", Defaults.DATA_PATH.value, heap_list)

    def search_by_task(self, string):
        self.search_results.clear()
        number = 1
        for task in self.heap:
            if string in task.task:
                self.search_results.append((number, task))
                number += 1
        return self.search_results

    def search_by_date(self, date_string):
        self.search_results.clear()
        parsed_date = self.parser.parse_date(date_string)
        for i, task in enumerate(self.heap, start=1):
            if f"{parsed_date:%Y-%m-%d}" == str(task.date):
                self.search_results.append((i, task))
        return self.search_results

    def search_output(self):
        return self.search_results

    def search_selection(self, selection_str):
        if "0" in selection_str:
            self.search_results.clear()
            return None

        selection = []
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

        self.search_results = list(
            filter(
                lambda item: item[0] in selection,
                self.search_results,
            )
        )
        return self.search_results

    def add_tasks(self, tasks_string):
        tasks = self.parser.make_task(tasks_string)
        self.heap.push(tasks)

    def mark_tasks_done(self):
        done_tasks = []
        for task in self.search_results:
            task = task[1]
            done_tasks.append(DoneTask(task.to_dict()))
            task.done = True

        print(
            [task.to_dict() for task in done_tasks],
        )
        self.search_results.clear()
        add_record_csv(
            "done.csv",
            Defaults.DATA_PATH.value,
            [task.to_dict() for task in done_tasks],
            KEYS_DONE_TASK,
        )

    def delete_task(self):
        tasks_ids = set()
        for task in self.search_results:
            tasks_ids.add(task[1].id)

        tasks = [task for task in self.heap if task.id not in tasks_ids]
        self.heap.clear()
        self.heap.push(tasks)

    def update_task(self, task_string):
        if len(self.search_results) != 1 or task_string is None:
            return None

        task_info = task_string.split(Defaults.TASK_SPLIT.value)[0]
        self.delete_task()
        self.add_tasks(task_info)

    def make_today_tasks(self):
        # TODO: Algoritmo de priorizacion
        pass

    def add_to_today_tasks(self):
        for _, task in self.search_results:
            self.today.append(task)
        self.search_results.clear()

    def remove_from_today_tasks(self, task):
        if len(self.search_results) != 1:
            return None

        task_id = self.search_results[0][1].id
        self.search_results.clear()
        self.today = [task for task in self.today if task_id != task.id]

    def print_today(self):
        today = []
        for i, task in enumerate(self.today):
            enumerator = "X" if task.done else i
            today.append(enumerator, task)
        return today

    def purge_done(self):
        # NOTE: crear lista de done???
        # TODO: limpiar el CSV de tareas realizadas
        # pasarlas a nuevo CSV
        # borrar del csv de done, las que esten con mas de 30 días de done
        pass
