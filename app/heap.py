from config import Defaults
from datetime import date
from task import Task


class Heap:
    def __init__(self, tasks=[]):
        self._heap = []
        self.levels = {}
        self.push(tasks)

    def task_wrapper(self, task):
        if isinstance(task, Task) is False:
            raise TypeError("Object must be a Task instance")

        triage = prioritizer(task)
        return (triage, task)

    def clear(self):
        self._heap.clear()

    def push(self, tasks):
        for task in tasks:
            task_with_wrapper = self.task_wrapper(task)
            self._heap.append(task_with_wrapper)
            self.heappify_up(len(self._heap) - 1)

            if task.dificulty in self.levels:
                self.levels[task.dificulty].append(task_with_wrapper)
            else:
                self.levels[task.dificulty] = [task_with_wrapper]

        for level in self.levels:
            self.levels[level] = list(
                sorted(
                    self.levels[level],
                    key=lambda item: item[0],
                    reverse=True,
                )
            )

    def pop(self):
        if len(self._heap) == 0:
            return None

        task = self._heap[0][1]
        alocate_task = self._heap.pop()

        if len(self._heap) == 0:
            return task

        self._heap[0] = alocate_task
        self.heappify_down(0)

        return task

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

    def remove_task(self, task_to_remove):
        index = None
        old_priority = None

        for i, (priority, task) in enumerate(self._heap):
            if task_to_remove == task:
                index = i
                old_priority = priority
                break

        if index is None:
            return

        if index == len(self._heap) - 1:
            self._heap.pop()
            return

        self._heap[index] = self._heap.pop()

        if old_priority > self._heap[index][0]:
            self.heappify_down(index)
        else:
            self.heappify_up(index)

    def update_task(self, new_task):
        index = None
        old_priority = None
        new_priority = prioritizer(new_task)

        for i, (priority, old_task) in enumerate(self._heap):
            if old_task == new_task:
                old_priority = priority
                self._heap[i] = (new_priority, new_task)
                index = i
                break

        if index is None:
            return

        if old_priority > new_priority:
            self.heappify_down(index)
        else:
            self.heappify_up(index)

    def __repr__(self):
        string = "Heap [\n"
        for value, task in self._heap:
            string += f"\t({value}) {task.task}, d:{task.done}\n"
        string += "]\n"
        return string

    def __iter__(self):
        self._iter_index = 0
        return self

    def __next__(self):
        if self._iter_index >= len(self._heap):
            raise StopIteration

        task = self._heap[self._iter_index][1]
        self._iter_index += 1
        return task

    def __len__(self):
        return len(self._heap)


def get_urgency(task_urgency):
    if task_urgency is None:
        return 0.7

    days_available = (task_urgency - date.today()).days

    if days_available >= 14:
        return 1
    if days_available >= 7:
        return 1.2
    if days_available >= 3:
        return 1.5
    if days_available >= 2:
        return 2
    if days_available >= 1:
        return 3
    if days_available == 0:
        return 4
    return 5


def prioritizer(task):
    if task.done:
        return 0
    urgency = (get_urgency(task.due_date) + 1) ** 1.5 * Defaults.URG_W.value
    undelayable = (1 if task.undelayable else 0) * Defaults.UND_W.value
    difficulty = task.dificulty * Defaults.DIF_W.value

    priority = 0
    priority += undelayable
    priority += urgency * difficulty

    return round(priority, 2)
