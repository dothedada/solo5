class Task:
    keys_allowed = (
        "lang",
        "id",
        "task",
        "task_csv",
        "done",
        "important",
        "dificulty",
        "creation_date",
        "lang",
        "due_date",
        "parent",
        "project",
    )

    def __init__(self, task_dict):
        for key, value in task_dict.items():
            if key not in Task.keys_allowed:
                continue
            setattr(self, key, value)

    def update_properties(self, **kwargs):
        for key, value in kwargs.items():
            if key == "id":
                raise Exception("Id cannot be updated")
            if key not in Task.keys_allowed:
                print(f"The key '{key}' does not exist in the Task object")
                continue
            setattr(self, key, value)
        return self

    def __repr__(self):
        output = "Task { \n"
        for key, value in self.__dict__.items():
            output += f"\t{key}: {value}\n"
        output += "}"
        return output
