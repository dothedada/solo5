from manager import TaskManager
from ui_loops import program_loop
from config import ui_txt


def main():
    taskManager = TaskManager()
    print("--MAIN--", taskManager.tasks)
    program_loop(taskManager)
    print(ui_txt["exit_program"])


if __name__ == "__main__":
    main()
