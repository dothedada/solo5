from manager import TaskManager


def main():

    taskManager = TaskManager()

    print(taskManager.global_heap)

    # tareas = load_csv(Defaults.DATA_PATH.value, "tasks.csv")
    # print(tareas)


if __name__ == "__main__":
    main()
