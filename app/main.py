from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager.heap)

    new_task = input("nuevas...\n")

    taskManager.add_tasks(new_task)
    # new_tasks = []
    # new_tasks.append(input("selecciona una tarea para borrar..."))

    del_task = []
    task_id = input("cual es el id...\n")
    del_task.append(task_id)
    taskManager.delete_task(del_task)

    # print(taskManager.delete_task(new_tasks))
    print(taskManager.heap)


if __name__ == "__main__":
    main()
