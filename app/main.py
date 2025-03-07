from taskParser import Parser
from heap import Heap


def main():

    tasks_txt = """
facil // muy facil // dificil // normal // muy dificil // nada //
"""
    parser_es = Parser("es")
    tasks = parser_es.make_task(tasks_txt)

    heap = Heap()

    heap.push(tasks)
    print(heap)


if __name__ == "__main__":
    main()
