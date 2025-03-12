from taskParser import Parser
from config import Defaults
from fileManagers import load_csv, sync_csv
from heap import Heap


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
        loaded_tasks = self.parser.make_tasks_from_csv(tasks_in_file)
        self.heap.push(loaded_tasks)

    def update_csv_from_heap(self):
        heap_list = [task.to_dict() for task in self.heap]
        sync_csv("tasks.csv", heap_list)

    def search_by_task(self, string):
        self.search_results.clear()
        for i, task in enumerate(self.heap, start=1):
            if string in task.task:
                self.search_results.append((i, task))
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
        self.update_csv_from_heap()

    def update_task(self, task_string):
        if len(self.search_results) != 1:
            return None

        task_info = self.parser.make_task(task_string)
        base_task = self.search_results[0][1]
        base_task.update_properties(**task_info)
        self.update_csv_from_heap()

    def mark_tasks_done(self, is_done):
        for task in self.search_results:
            task[1].done = is_done

        self.search_results.clear()
        self.update_csv_from_heap()
        # NOTE: crear lista de done???

    def delete_task(self):
        if len(self.search_results) != 1:
            return None

        task_id = self.search_results[0][1].id
        tasks = [task for task in self.heap if task.id != task_id]
        self.heap.clear()
        self.heap.push(tasks)
        self.update_csv_from_heap()

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
