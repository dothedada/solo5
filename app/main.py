from manager import TaskManager
from fileManagers import clean_directory
from config import Defaults


def main():

    taskManager = TaskManager()

    print(taskManager._tasks)
    print(taskManager.get_today())

    clean_directory("today_*.csv", Defaults.DATA_PATH.value)
    while True:
        do = input("Add, Remove, Update, Done, Save, Exit:\n")

        match do:
            case "Add":
                tasks_str = input("Add tasks:\n")
                taskManager.add_tasks(tasks_str)
            case "Remove":
                tasks_search = input("What tasks do you want to delete:\n")
                taskManager.add_to_search_by_task(tasks_search)
                print("Search results:")
                if len(taskManager.search_results) == 0:
                    print("No match found")
                    continue
                elif len(taskManager.search_results) == 1:
                    print("Do you want to delete:")
                    print(taskManager.search_results[0][1])
                    confirm = input("[y]es / [n]o")
                    if confirm == "n":
                        print("deletion aborted")
                        continue
                else:
                    for i, task in taskManager.search_results:
                        print(f"{i}) {task.task}")
                    select = input("\nselect which ones you wanna delete...")
                    taskManager.select_from_search(select)
                taskManager.delete_task()
            case "Update":
                tasks_search = input("What tasks do you want to update:\n")
                taskManager.add_to_search_by_task(tasks_search)
                print("Search results:")
                if len(taskManager.search_results) == 0:
                    print("No match found")
                    continue
                elif len(taskManager.search_results) == 1:
                    print("Do you want to update:")
                    print(taskManager.search_results[0][1])
                    confirm = input("[y]es / [n]o\n")
                    if confirm == "n":
                        print("update aborted")
                        continue
                else:
                    for i, task in taskManager.search_results:
                        print(f"{i}) {task.task}")
                    select = input("\nselect the task you want to update...")
                    taskManager.select_from_search(select, just_one=True)
                new_task = input("What is the new task?")
                taskManager.update_task(new_task)
                print("Task updated")
            case "Done":
                task_search = input("Whitch task you want to mark as done:\n")
                taskManager.add_to_search_by_task(task_search)
                print("Search results:")
                if len(taskManager.search_results) == 0:
                    print("No match found")
                    continue
                elif len(taskManager.search_results) == 1:
                    print("Do you want to mark done:")
                    print(taskManager.search_results[0][1])
                    confirm = input("[y]es / [n]o\n")
                    if confirm == "n":
                        print("update aborted")
                        continue
                else:
                    for i, task in taskManager.search_results:
                        print(f"{i}) {task.task}")
                    select = input("\nselect the tasks you want to mark as done...")
                    taskManager.select_from_search(select)
                taskManager.mark_tasks_done()
                taskManager.save_tasks_done()
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
