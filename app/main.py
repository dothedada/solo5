from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager._tasks)
    print(taskManager.get_today())

    new_task = input("nuevas...\n")
    taskManager.add_tasks(new_task)

    search = input("que tareas???...\n")
    taskManager.add_to_search_by_task(search)
    for i, task in taskManager.search_output():
        print(f"{i}) {task.task}")

    if len(taskManager.search_output()) > 9:
        print(f"too many tasks by {search}")
    elif len(taskManager.search_output()) == 1:
        print("una")
    else:
        selection = input("select:\n")
        taskManager.search_selection(selection)

    # nuevo = input("Ahora que???\n")
    taskManager.mark_tasks_done()
    taskManager.save_tasks_to_csv()

    # print(taskManager.delete_task(new_tasks))
    print(taskManager._tasks)


if __name__ == "__main__":
    main()
