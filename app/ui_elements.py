from fileManagers import load_json
from config import Defaults
from type_input import Command

feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
commands_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["command"]


def context_wrapper():
    task_manager = None
    state = ["", "", "", ""]  # [context_str, command_str, action_str, search_i
    where = None

    def context_manager(manager=None, context=None, command=None, action=None):
        nonlocal task_manager, state, where

        task_manager = manager if manager else task_manager

        if task_manager is None:
            raise ValueError("a MANAGER needs to be assigned before use")

        context_values = {
            "global": ["global_str", task_manager.tasks],
            "today": ["today_str", task_manager.today_tasks],
            "done": ["done_str", task_manager.done_tasks],
        }

        if where is None:
            state[0] = context_values[Defaults.CONTEXT.value][0]
            where = context_values[Defaults.CONTEXT.value][1]

        if context:
            state[0] = context_values[context][0]
            where = change_context(where, context)

        state[1] = commands_ui[command.value] if command else state[1]
        state[2] = action if action else state[2]

        search_items = len(task_manager.search_results)
        state[3] = f"{search_items} ITEMS " if search_items else ""

        return {
            "bar": f"{'> '.join(filter(bool,state))}> ",
            "where": where,
        }

    return context_manager


def change_context(current, new):
    print("YA ESTAS EN CONTEXTO" if current != new else "CONTEXTO CAMBIADO")
    return new


def print_context(context):
    # NOTE: SORT search???

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


def print_search(task_list, limit):
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
    for i, task in task_list:
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print(f'\n{feedback_ui["search_overflow"]}')
            break
        print(f"{i}) {task.task}")
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
