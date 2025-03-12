from datetime import date

KEYS_ALLOWED = (
    "lang",
    "id",
    "task",
    "done",
    "undelayable",
    "dificulty",
    "due_date",
    "project",
)

KEYS_DONE_TASK = (
    "lang",
    "id",
    "task",
    "due_date",
    "date_done",
)


class Task:
    keys_allowed = KEYS_ALLOWED

    def __init__(self, task_dict):
        if "id" not in task_dict or "task" not in task_dict:
            raise TypeError("Task must have id and task parameters")

        for key, value in task_dict.items():
            if key not in self.keys_allowed:
                continue
            setattr(self, key, value)
            setattr(self, "creation_date", date.today())

    def to_dict(self):
        dictionary = {}
        for key in self.keys_allowed:

            dictionary[key] = getattr(self, key, None)

        return dictionary

    def __repr__(self):
        output = "Task { \n"
        for key, value in self.to_dict().items():
            output += f"\t{key}: {value}\n"
        output += "}\n"
        return output


class DoneTask(Task):
    keys_allowed = KEYS_DONE_TASK

    def __init__(self, task_dict):
        super().__init__(task_dict)
        setattr(self, "date_done", date.today())
