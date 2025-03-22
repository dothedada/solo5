from parser_input import parse_response
from ui_elements import (
    print_search,
    print_context,
    print_ui,
    print_line,
    print_div,
    screen,
)
from context import context_wrapper
from type_input import Response, Confirm, Command
from config import Defaults, ui_txt
import os


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


state = context_wrapper()


def program_loop(manager):
    state(task_manager=manager)
    while True:
        action = parse_response(Response.COMMAND, input(state()["bar"]))
        screen.add_line()

        screen.clear()
        if action[0] == Response.ERR:
            print_line(action[1], color="red", style="bold")
            continue

        match action[1]:
            case Command.IN_TODAY:
                state(context="today")

            case Command.IN_GLOBAL:
                state(context="global")

            case Command.IN_DONE:
                state(context="done")

            case Command.PRINT:
                print_context(state()["where"], state()["where_name"])

            case Command.ADD_TASKS:
                if state()["where"] == manager.done_tasks:
                    print_ui("output", "no_effect", color="red")
                    continue
                tasks_str = input(state(command=Command.ADD_TASKS)["bar"])
                screen.add_line()
                if state()["where"] == manager.today_tasks:
                    manager.add_to_today(tasks_str)
                else:
                    manager.add_tasks(tasks_str)

            case Command.UPDATE_TASK:
                if state()["where"] == manager.done_tasks:
                    print_ui("output", "no_effect", color="red")
                    continue
                state(command=Command.UPDATE_TASK)
                action_loop(manager, Command.UPDATE_TASK, True)

            case Command.DONE_TASK:
                if state()["where"] == manager.done_tasks:
                    print_ui("output", "no_effect", color="red")
                    continue
                state(command=Command.DONE_TASK)
                action_loop(manager, Command.DONE_TASK, False)

            case Command.DELETE_TASKS:
                state(command=Command.DELETE_TASKS)
                action_loop(manager, Command.DELETE_TASKS, False)

            case Command.MAKE_TODAY:
                manager.make_today()
                state(context="today")
                print_context(state()["where"], state()["where_name"])

            case Command.ENCORE_TODAY:
                if manager.encore_posible():
                    if amount := input("Cuantas tareas mas? Max XXX> "):
                        if not amount.isdigit():
                            print_ui("err", "only_int", color="red")
                        manager.encore_today(int(amount))
                    screen.add_line()
                    print_ui("output", "done", color="green")
                    print_context(manager.today_tasks, "hoy")
                else:
                    print_ui("output", "today_unfinnished", color="red")

            case Command.FORECAST:
                if forecast := manager.get_forecast():
                    print_context(forecast, ui_txt["output"]["forecast"])
                else:
                    print_ui("output", "no_forecast")

            case Command.SEARCH:
                manager.search_results.clear()
                search_loop(manager, True)

            case Command.CLEAR:
                manager.search_results.clear()

            case Command.SAVE:
                manager.save_tasks_to_csv()
                manager.save_tasks_done()
                print_ui("output", "save", color="green", div=" ", bottom=True)

            case Command.EXIT:
                return

            case Command.PURGE:
                manager.purge_done()
                print_ui("output", "purge", color="green")

            case Command.FIX_DATES:
                fixed_tasks = manager.fix_dates()
                if fixed_tasks:
                    for i, (task, old, new) in enumerate(fixed_tasks):
                        print_line(f"{i}) {task}\n\t{old} -> {new}")
                    print_ui(
                        "output",
                        "fix_dates",
                        top=True,
                        prepend=len(fixed_tasks),
                        color="green",
                    )
                else:
                    print_ui("output", "fix_dates_not", color="green")
                print_line()

            case Command.HELP:
                pass

            case _:
                print_ui("output", "unknown", color="red")

        state(command="", action="")
        if Defaults.SAVE_IN_CICLE.value:
            manager.save_tasks_to_csv()
            manager.save_tasks_done()


def resolve_action(manager, command):
    actions = {
        Command.ADD_TASKS: manager.add_tasks,
        Command.DELETE_TASKS: manager.delete_task,
        Command.DONE_TASK: manager.mark_tasks_done,  # str arg
        Command.UPDATE_TASK: manager.update_task,  # bool arg
    }

    if command == Command.UPDATE_TASK:
        if len(manager.search_results) != 1:
            raise RuntimeError(ui_txt["too_many_items"])

        update_str = parse_response(
            Response.TEXT_INPUT,
            input(ui_txt["input"]["new_data"]),
        )
        screen.add_line()

        if isinstance(update_str, tuple) and update_str[1] == Command.EXIT:
            return Command.EXIT

        actions[command](update_str[1])
    else:
        actions[command]()


def action_loop(manager, action, single):
    while True:
        if not manager.search_results:
            search = search_loop(manager, single)
            if search == Command.EXIT:
                return

        if Defaults.CARPE_DIEM.value:
            break

        state(action="CONFIRMAR")
        print_ui("output", "confirmation", style="bold", color="blue")
        confirmation = input_loop(Response.CONFIRM)

        match confirmation:
            case Command.EXIT | Confirm.CANCEL:
                manager.search_results.clear()
                return
            case Confirm.YES:
                break
            case Confirm.NO:
                manager.search_results.clear()
                continue
            case _:
                raise Exception(ui_txt["unknown"])

    resolve_action(manager, action)
    state(command="", action="")
    manager.search_results.clear()
    print_ui("output", "done")


def search_loop(task_manager, single):
    while True:
        _, search_value = parse_response(
            Response.TEXT_INPUT,
            input(state(action="BUSCAR")["bar"]),
        )
        screen.add_line()
        if search_value == Command.EXIT:
            task_manager.search_results.clear()
            return Command.EXIT

        if not search_value:  # search_value == "", empty string:
            print_ui("output", "search_no_input", color="red", style="bold")
            continue

        task_manager.add_to_search(search_value, state()["where"])
        if not task_manager.search_results:
            print_ui("output", "search_no_match", color="red", style="bold")
            continue

        if len(task_manager.search_results) == 1:
            print_ui("output", "warn", top=True, div=" ")
            print_line(task_manager.search_results[0][1].task, style="bold")
            print_div()
        else:
            state(action="SELECCIONAR")

            selection = selection_loop(task_manager, single)

            if selection == Command.EXIT:
                return Command.EXIT

            if selection is False:
                continue

        return


def selection_loop(manager, single):
    while True:
        print_search(manager.search_results, True)
        print_ui("output", "select_one" if single else "select")
        selection = input_loop(Response.SELECTION, len(manager.search_results))
        if selection == Command.EXIT:
            manager.search_results.clear()
            return Command.EXIT

        if selection == Response.ERR:
            continue

        if not manager.search_results or not selection:
            print_ui("output", "select_cancel", color="red")
            manager.search_results.clear()
            return False

            continue

        manager.select_from_search(selection)

        if single and len(manager.search_results) > 1:
            print_ui("output", "select_reminder", color="red", style="bold")
            continue

        break

    print_search(manager.search_results, False, selected=True)
    return True


def input_loop(answer_type, *args):
    while True:
        response = parse_response(answer_type, input(state()["bar"]), *args)
        screen.add_line()

        match response:
            case (_, Command.EXIT):
                print_ui("output", "cancel")
                return Command.EXIT
            case (t, data) if t == answer_type:
                return data
            case (Response.ERR, message):
                print_line(f"ERROR: {message}", color="red", style="bold")
                return Response.ERR
            case _:
                raise ValueError("Unknown Command")
