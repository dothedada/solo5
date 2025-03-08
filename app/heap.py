from config import Defaults
from datetime import date
from task import Task


class Heap:
    def __init__(self, tasks=[]):
        self._heap = []
        self.push(tasks)

    def task_wrapper(self, task):
        if isinstance(task, Task) is False:
            raise TypeError("Objext must be a Task instance")

        triage = prioritizer(task)
        return (triage, task)

    def push(self, tasks):
        for task in tasks:
            self._heap.append(self.task_wrapper(task))
            self.heappify_up(len(self._heap) - 1)

    def pop(self):
        if len(self._heap) == 0:
            return None

        task = self.peek()
        last_item = self._heap.pop()
        self._heap[0] = last_item
        self.heappify_down(0)
        return task

    def peek(self):
        if len(self._heap) == 0:
            return None

        return self._heap[0][1]

    def heappify_up(self, index):
        if index == 0:
            return

        parent_index = self.get_parent_ind(index)
        if parent_index < 0:
            return

        if self._heap[index][0] < self._heap[parent_index][0]:
            return

        temp = self._heap[index]
        self._heap[index] = self._heap[parent_index]
        self._heap[parent_index] = temp

        self.heappify_up(parent_index)

    def heappify_down(self, index):
        if index >= len(self._heap):
            return

        l_child_index = self.get_l_child_ind(index)
        r_child_index = self.get_r_child_ind(index)
        largest = index

        if l_child_index >= len(self._heap):
            return

        if self._heap[index][0] < self._heap[l_child_index][0]:
            largest = l_child_index

        if r_child_index >= len(self._heap):
            return

        if self._heap[largest][0] < self._heap[r_child_index][0]:
            largest = r_child_index

        if index == largest:
            return

        temp = self._heap[index]
        self._heap[index] = self._heap[largest]
        self._heap[largest] = temp

        return self.heappify_down(largest)

    def get_parent_ind(self, index):
        return (index - 1) // 2

    def get_l_child_ind(self, index):
        return (index * 2) + 1

    def get_r_child_ind(self, index):
        return (index * 2) + 2

    def __repr__(self):
        string = "Heap [\n"
        for value, task in self._heap:
            string += f"\t({value}, {task.task})\n"
        string += "]\n"
        return string


def get_urgency(task_urgency):
    if task_urgency is None:
        return 1

    days_available = (task_urgency - date.today()).days

    if days_available > 14:
        return 2
    if days_available > 7:
        return 3
    if days_available > 3:
        return 5
    if days_available > 2:
        return 7
    if days_available > 1:
        return 11
    if days_available > 0:
        return 13
    if days_available == 0:
        return 17
    return 29


def prioritizer(task):
    undelayable = 1 if task.undelayable else 0
    dificulty = task.dificulty * (task.dificulty - 1)
    urgency = get_urgency(task.due_date)

    return int(
        (undelayable * Defaults.UND_W.value)
        + (dificulty * Defaults.DIF_W.value)
        + (urgency * Defaults.URG_W.value)
    )
    pass
