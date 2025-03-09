from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager.heap)

    new_tasks = input("Busca una tarea...")

    print(taskManager.search_task(new_tasks))
    print(taskManager.heap)


if __name__ == "__main__":
    main()
