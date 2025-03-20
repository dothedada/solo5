from parser_input import parse_response
from ui_elements import (
    print_search,
    print_context,
    print_ui,
    print_line,
    print_div,
)
from context import context_wrapper
from type_input import Response, Confirm, Command
from config import Defaults, ui_txt
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


state = context_wrapper()

# TODO:
# 4. todo lo relacionado con today (make, encore, forecast)
# 4.1 algoritmo para armar día
# 5. completar condicionales del program loop
# 6. Configuracion
# 7. documentacion


def program_loop(manager):
    state(task_manager=manager)
    while True:
        action = parse_response(Response.COMMAND, input(state()["bar"]))

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
                # TODO: bloquear en DONE, complementar en TODAY
                tasks_str = input(state(command=Command.ADD_TASKS)["bar"])
                manager.add_tasks(tasks_str)
            case Command.UPDATE_TASK:
                # TODO: bloquear en DONE, complementar en TODAY
                state(command=Command.UPDATE_TASK)
                action_loop(manager, Command.UPDATE_TASK, True)
            case Command.DONE_TASK:
                # TODO: marcar como UNDONE, devolver a task
                state(command=Command.DONE_TASK)
                action_loop(manager, Command.DONE_TASK, False)
            case Command.DELETE_TASKS:
                # TODO: al borrar de GLOBAL se elimina de HOY
                state(command=Command.DELETE_TASKS)
                action_loop(manager, Command.DELETE_TASKS, False)

            case Command.MAKE_TODAY:
                manager.make_today()
                # print_context("today", "today")

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
                print()
            case _:
                print_ui("output", "unknown", color="red")

        state(command="", action="")


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
            input(input_ui["new_data"]),
        )

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
