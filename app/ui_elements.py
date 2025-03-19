from types import SimpleNamespace
from fileManagers import load_json
from config import Defaults, ui_txt
from type_input import Command

commands_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["command"]


def context_wrapper():
    manager = None
    state = SimpleNamespace(context="", command="", action="", search_i="")
    where = None

    def context_manager(
        task_manager=None,
        context=None,
        command=None,
        action=None,
    ):
        nonlocal manager, state, where

        manager = task_manager if task_manager else manager

        if manager is None:
            raise ValueError(ui_txt["context_manager_manager_error"])

        context_values = {
            "global": ["global_str", manager.tasks],
            "today": ["today_str", manager.today_tasks],
            "done": ["done_str", manager.done_tasks],
        }

        if where is None:
            state.context = context_values[Defaults.CONTEXT.value][0]
            where = context_values[Defaults.CONTEXT.value][1]

        if context is not None:
            state.context = context_values[context][0]
            where = change_context(where, context_values[context][1])

        if command is not None:
            if isinstance(command, Command):
                state.command = commands_ui[command.value]
            else:
                state.command = ""

        if action is not None:
            state.action = action

        tasks = len(manager.search_results)
        state.search_i = f"{tasks} {ui_txt['task_name']} " if tasks else ""

        bar = filter(
            bool,
            [state.context, state.command, state.action, state.search_i],
        )

        return {
            "bar": f"{'> '.join(bar)}> ",
            "where": where,
        }

    return context_manager


def change_context(current, new):
    print(
        ui_txt["context_same"] if current == new else ui_txt["context_change"],
    )
    return new


def print_context(context):
    # NOTE: SORT search???

    if len(context) == 0:
        print(ui_txt["no_tasks_in_context"])
        return

    print(ui_txt["line"] * len(ui_txt["search_results"]))
    pending = 0
    done = 0
    for i, task in enumerate(context):
        if task.done_date:
            done += 1
            print(f"X) {task.task}")
            continue
        print(f"{i}) {task.task}")
        pending += 1
    print(f"{(done * 100) / len(context)}{ui_txt['done_%_of']}")
    print(f"{len(context)} {ui_txt['total_tasks_context']}")


def print_search(task_list, limit):
    print(ui_txt["line"] * len(ui_txt["search_results"]))
    task_number = 1
    for _, task in task_list:
        if limit and task_number > Defaults.SEARCH_RESULTS.value:
            print(f'\n{ui_txt["search_overflow"]}')
            break
        print(f"{task_number}) {task.task}")
        task_number += 1
    print(ui_txt["line"] * len(ui_txt["search_results"]))
