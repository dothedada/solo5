from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager._tasks)
    print(taskManager.get_today())

    while True:
        do = input("Add, Remove, Update, Done, Save, Exit:\n")

        match do:
            case "Add":
                tasks_str = input("Add tasks:\n")
                taskManager.add_tasks(tasks_str)
            case "Remove":
                tasks_search = input("What tasks do you want to delete:\n")
                taskManager.add_to_search_by_task(tasks_search)
                serch_results = []
                print("Search results:")
                for i, task in taskManager.search_results:
                    print(f"{i}) {task.task}")
                select = input("\nselect which ones you wanna delete...")
                taskManager.select_from_search(select)
                taskManager.delete_task()
            case "Save":
                taskManager.save_tasks_to_csv()
                print("Tasks saved")
            case "Exit":
                break
            case _:
                print("No command were choose...")

        print(taskManager._tasks)

    print("Chao BB...")


if __name__ == "__main__":
    main()
