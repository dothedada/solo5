from config import Defaults


class Task:
    keys_allowed = Defaults.KEYS_ALLOWED.value

    def __init__(self, task_dict):
        if "id" not in task_dict or "task" not in task_dict:
            raise TypeError("Task must have id and task parameters")

        for key, value in task_dict.items():
            if key not in Task.keys_allowed:
                continue
            setattr(self, key, value)

    def update_properties(self, **kwargs):
        for key, value in kwargs.items():
            if key == "id":
                # print("Id cannot be updated")
                continue
            if key not in Task.keys_allowed:
                print(f"The key '{key}' does not exist in the Task object")
                continue
            setattr(self, key, value)
        return self

    def to_dict(self):
        dictionary = {}
        for key in Task.keys_allowed:

            dictionary[key] = getattr(self, key, None)

        return dictionary

    def __repr__(self):
        output = "Task { \n"
        for key, value in self.__dict__.items():
            output += f"\t{key}: {value}\n"
        output += "}\n"
        return output
