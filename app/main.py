from manager import TaskManager
from ui_loops import program_loop


def main():
    taskManager = TaskManager()
    print("asdasd", taskManager.tasks)
    program_loop(taskManager)
    print("Chao BB...")


if __name__ == "__main__":
    main()
