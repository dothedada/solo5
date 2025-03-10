from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager.heap)

    new_task = input("nuevas...\n")

    taskManager.add_tasks(new_task)
    # new_tasks = []
    # new_tasks.append(input("selecciona una tarea para borrar..."))

    search = input("que tareas???...\n")
    taskManager.search_by_task(search)
    taskManager.update_task("done", True)

    # print(taskManager.delete_task(new_tasks))
    print(taskManager.heap)


if __name__ == "__main__":
    main()
