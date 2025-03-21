import time
import random
from datetime import date

TASK_KEYS = (
    "lang",
    "id",
    "task",
    "done",
    "undelayable",
    "dificulty",
    "due_date",
    "done_date",
    "project",
)

TASK_DONE_KEYS = (
    "lang",
    "id",
    "task",
    "due_date",
    "done_date",
)


class Task:
    keys_allowed = TASK_KEYS

    def __init__(self, task_dict):
        if "task" not in task_dict:
            raise TypeError("Task must have id and task parameters")

        # First set, and if the values exist, it will overwrite
        setattr(self, "id", Task.make_id_for(task_dict["task"]))
        setattr(self, "creation_date", date.today())
        setattr(self, "done_date", None)
        for key, value in task_dict.items():
            if key not in self.keys_allowed:
                continue
            setattr(self, key, value)

    @staticmethod
    def make_id_for(string):
        char_sum = sum(ord(char) for char in string)
        timestamp = int(time.time() * 1000)
        salt = random.randint(1, 9999)
        base_id = (char_sum * timestamp * salt) % (2**64)

        return hex(base_id)[2:]

    def to_dict(self, only_id=False):
        dictionary = {}
        if only_id:
            dictionary["id"] = getattr(self, "id")
            return dictionary

        for key in self.keys_allowed:
            dictionary[key] = getattr(self, key, None)

        return dictionary

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.id == other.id

    def __hash__(self):
        return int(self.id, base=16)

    def __repr__(self):
        output = "Task { \n"
        for key, value in self.to_dict().items():
            output += f"\t{key}: {value}\n"
        output += "}\n"
        return output


class DoneTask(Task):
    keys_allowed = TASK_DONE_KEYS

    def __init__(self, task_dict):
        if isinstance(task_dict, Task):
            task_dict = task_dict.to_dict()

        super().__init__(task_dict)
