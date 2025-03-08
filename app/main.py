from taskParser import Parser
from heap import Heap
from manager import TaskManager
from fileLoaders import load_csv
from config import Defaults


def main():

    tasks_txt = """
facil // muy facil // dificil // normal // muy dificil // nada //
"""
    parser_es = Parser("es")
    tasks = parser_es.make_task(tasks_txt)

    heap = Heap()
    taskManager = TaskManager()

    heap.push(taskManager.tasks)
    print(heap)

    # tareas = load_csv(Defaults.DATA_PATH.value, "tasks.csv")
    # print(tareas)


if __name__ == "__main__":
    main()
