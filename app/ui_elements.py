from fileManagers import load_json
from config import Defaults

feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]


def bar_info():
    state = ["", "", "", ""]
    task_manager = None

    def context_manager(manager=None, context=None, command=None, action=None):
        nonlocal task_manager

        if manager:
            task_manager = manager

        if task_manager:
            state[3] = "V " if task_manager.search_results else ""

        for i, info in enumerate([context, command, action]):
            if info is not None:
                state[i] = info
        return f"{'> '.join(filter(bool,state))}> "

    return context_manager


def print_context(context):
    if len(context) == 0:
        print("SIN TAREAS EN EL CONTEXTO")
        return

    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
    pending = 0
    done = 0
    print(context)
    for i, task in enumerate(context):
        if task.done_date:
            done += 1
            print(f"X) {task.task}")
            continue
        print(f"{i}) {task.task}")
        pending += 1
    print(f"{(done * 100) / len(context)}% DE {len(context)} TAREAS")


def print_tasks_in(task_list, limit):
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
    for i, task in task_list:
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print(f'\n{feedback_ui["search_overflow"]}')
            break
        print(f"{i}) {task.task}")
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
