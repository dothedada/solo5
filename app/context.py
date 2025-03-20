from types import SimpleNamespace
from config import Defaults, ui_txt
from type_input import Command
from fileManagers import load_json

ui_feed = ui_txt["feedback_"]
# FIX: esta linea de abajo se va
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
            raise ValueError(ui_feed["context_manager_manager_error"])

        context_values = {
            "global": [ui_txt["context"]["global"], manager.tasks],
            "today": [ui_txt["context"]["today"], manager.today_tasks],
            "done": [ui_txt["context"]["done"], manager.done_tasks],
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
        state.search_i = f"{tasks} {ui_feed['task_name']} " if tasks else ""

        bar = filter(
            bool,
            [state.context, state.command, state.action, state.search_i],
        )

        return {
            "bar": f"{'> '.join(bar)}> ",
            "where": where,
            "where_name": state.context,
        }

    return context_manager


def change_context(current, new):
    print(
        ui_feed["context_same"] if current == new else ui_feed["context_change"],
    )
    return new
