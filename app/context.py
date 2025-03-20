from types import SimpleNamespace
from config import Defaults, ui_txt
from type_input import Command
from ui_elements import print_ui

# FIX: esta linea de abajo se va
# commands_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["command"]
ui_context = ui_txt["context"]
ui_command = ui_txt["command"]


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
            raise ValueError("Task manager needs to be assigned in context")

        context_values = {
            "global": [ui_context["global"], manager.tasks],
            "today": [ui_context["today"], manager.today_tasks],
            "done": [ui_context["done"], manager.done_tasks],
        }

        if where is None:
            state.context = context_values[Defaults.CONTEXT.value][0]
            where = context_values[Defaults.CONTEXT.value][1]

        if context is not None:
            state.context = context_values[context][0]
            where = change_context(where, context_values[context][1])

        if command is not None:
            if isinstance(command, Command):
                state.command = ui_command[command.value]
            else:
                state.command = ""

        if action is not None:
            state.action = action

        tasks = len(manager.search_results)
        state.search_i = f"{tasks} {ui_context['selected']} " if tasks else ""

        bar = filter(
            bool,
            [state.context, state.command, state.action, state.search_i],
        )

        return {
            "bar": f"\033[1m{'> '.join(bar)}> \033[0m",
            "where": where,
            "where_name": state.context,
        }

    return context_manager


def change_context(current, new):
    print_ui("context", "same" if current == new else "change")
    return new
