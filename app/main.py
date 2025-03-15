from manager import TaskManager
import parser_input as usr_input
from ui import task_loop


def main():

    taskManager = TaskManager()

    print(taskManager._tasks)
    print(taskManager.get_today())

    print(usr_input.confirm("sis i si si").value)

    while True:
        do = input("Add, Remove, Update, Done, Save, Exit:\n")

        # print(parse_command(do))

        match do:
            case "Add":
                tasks_str = input("Add tasks:\n")
                taskManager.add_tasks(tasks_str)
            case "Remove":
                task_loop(taskManager, taskManager.delete_task, False)
            case "Update":
                task_loop(taskManager, taskManager.update_task, True, True)
            case "Done":
                task_loop(taskManager, taskManager.mark_tasks_done(), False)
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
