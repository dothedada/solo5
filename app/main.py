from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager.global_heap)

    new_tasks = input("Añade una tarea...")

    taskManager.add_tasks(new_tasks)
    print(taskManager.global_heap)


if __name__ == "__main__":
    main()
