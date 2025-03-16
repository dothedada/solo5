from fileManagers import load_json
from config import Defaults

feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]


def bar_info():
    state = ["", "", ""]

    def context_manager(context=None, command=None, action=None):
        for i, info in enumerate([context, command, action]):
            if info is not None:
                state[i] = info
        return f"{'> '.join(filter(bool,state))}> "

    return context_manager


def print_context(context):
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
    for i, task in enumerate(context):
        if task.done:
            print(f"X) {task.task}")
        print(f"{i}) {task.task}")


def print_tasks_in(task_list, limit):
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
    for i, task in task_list:
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print(f'\n{feedback_ui["search_overflow"]}')
            break
        print(f"{i}) {task.task}")
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
