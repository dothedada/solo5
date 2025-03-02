class TaskToken:
    keys_allowed = (
        "id",
        "task",
        "dificulty",
        "due_date",
        "dependencies",
        "project",
    )

    def __init__(self, **kwargs):
        if "id" not in kwargs or "task" not in kwargs:
            raise TypeError("id and task are mandatory to create token")
        for key, value in kwargs.items():
            if key not in TaskToken.keys_allowed:
                continue
            setattr(self, key, value)


class Task(TaskToken):
    keys_allowed = TaskToken.keys_allowed + ("priority",)

    def __init__(self, token):
        super().__init__(**token)

    def set_priority(self, priority):
        self.priority = priority

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
