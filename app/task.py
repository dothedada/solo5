class Task:
    def __init__(self, task):
        self.id = task.id
        self.task = task.task
        self.dificulty = task.dificulty
        self.dueDate = task.dueDate
        self.dependencies = task.dependencies
        self.project = task.project
        self.priority = 0

    def set_priority(self, value):
        self.priority = value
        return self

    def update_properties(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self

    def __repr__(self):
        output = "Task {"
        output += f"id: { self.id }, "
        output += f"priority: { self.priority }, "
        output += f"task: { self.task }, "
        output += f"dificulty: { self.dificulty }, "
        if self.dueDate:
            output += f"dueDate: { self.dueDate }, "
        if self.dependencies:
            output += f"dependencies: { self.dependencies }, "
        if self.project:
            output += f"project: { self.project }, "
        output += "}"
        return output
