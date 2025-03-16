from parser_input import get_response, get_exit
from ui_elements import bar_info, print_tasks_in, print_context
from type_input import Response, Confirm, Command
from config import Defaults
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


status_bar = bar_info()

# "make_today": "^h(?:acer hoy)?$",
# "encore_today": "^extra$",
# "fix_dates": "^arreglar$",
# "help": "^ayuda$",
# "forecast": "^m(?:a[nñ]ana)?$"


def program_loop(task_manager):
    where = task_manager.tasks
    status_bar(manager=task_manager, context="GLOBAL")
    while True:
        action = get_response(Response.COMMAND, input(status_bar()))

        if action[0] != Response.COMMAND:
            print("ÑO ENTENDÍ")

        match action[1]:
            case Command.IN_TODAY:
                where = change_context(where, task_manager.today_tasks, "HOY")
            case Command.IN_GLOBAL:
                where = change_context(where, task_manager.tasks, "GLOBAL")
            case Command.IN_DONE:
                where = change_context(where, task_manager.done_tasks, "TERMINADAS")
            case Command.PRINT:
                print_context(where)
            case Command.ADD_TASKS:
                status_bar(command="AÑADIR")
                tasks_str = input(status_bar())
                task_manager.add_tasks(tasks_str)
            case Command.UPDATE_TASK:
                status_bar(command="ACTUALIZAR")
                action_loop(task_manager, Command.UPDATE_TASK, True)
            case Command.DONE_TASK:
                status_bar(command="TERMINADAS")
                action_loop(task_manager, Command.DONE_TASK, False)
            case Command.DELETE_TASKS:
                status_bar(command="BORRAR")
                action_loop(task_manager, Command.DELETE_TASKS, False)

            case Command.SEARCH:
                search_loop(task_manager, True)
            case Command.SAVE:
                task_manager.save_tasks_to_csv()
                print("TASKS SAVED")
            case Command.EXIT:
                return
            case Command.PURGE:
                task_manager.purge_done()
                print("DONE TASKS WERE PURGE")
            case _:
                print("UNKNOWN COMMAND")

        status_bar(command="", action="")


def change_context(current_context, new_context, context_name):
    if current_context != new_context:
        print("CONTEXTO CAMBIADO", context_name)
    else:
        print("YA ESTAS EN CONTEXTO", context_name)

    status_bar(context=context_name)
    return new_context


def resolve_action(task_manager, command):
    actions = {
        Command.ADD_TASKS: task_manager.add_tasks,
        Command.DELETE_TASKS: task_manager.delete_task,
        Command.DONE_TASK: task_manager.mark_tasks_done,  # str arg
        Command.UPDATE_TASK: task_manager.update_task,  # bool arg
    }

    if command == Command.UPDATE_TASK:
        if len(task_manager.search_results) != 1:
            raise RuntimeError("TOO MANY ELEMENTS ON FOR THE ACTION")

        actions[command](input(input_ui["new_data"]))
    else:
        actions[command]()


def search_loop(task_manager, single):
    while True:

        look_for = input(status_bar(action="BUSCAR"))
        if get_exit(look_for):
            print(feedback_ui["cancel"])
            return False

        task_manager.add_to_search_by_task(look_for)

        if task_manager.search_results:
            print("--LEEA AQUI--", single)
            if len(task_manager.search_results) == 1:
                print(feedback_ui["warn"])
                print(f'"{task_manager.search_results[0][1].task}"')
            else:
                print(f'\n{feedback_ui["search_results"]}')
                status_bar(action="SELECCIONAR")
                selection_loop(task_manager, single)
            return True

        print(feedback_ui["search_no_match"])


def action_loop(task_manager, action, single):
    while True:

        if not task_manager.search_results:
            if search_loop(task_manager, single) is False:
                return

        if Defaults.CARPE_DIEM.value:
            break

        status_bar(action="CONFIRMAR")
        print(input_ui["confirmation"])
        confirmation = input_loop(Response.CONFIRM)
        match Confirm(confirmation):
            case Confirm.YES:
                break
            case Confirm.CANCEL:
                print(feedback_ui["cancel"])
                return
            case Confirm.NO:
                pass

    resolve_action(task_manager, action)
    print(feedback_ui["done"])


def selection_loop(task_manager, single):
    while True:
        print_tasks_in(task_manager.search_results, True)
        print(input_ui["which_one"] if single else input_ui["which_ones"])
        select = input_loop(
            Response.SELECTION,
            len(task_manager.search_results),
        )
        if select == Response.OUT:
            task_manager.search_results.clear()
            return
        if len(task_manager.search_results) == 0:
            print("NO SELECCIONASTE NARAAAA")
            return

        task_manager.select_from_search(select)

        if single and len(task_manager.search_results) > 1:
            print("\nSOLO UNO PERRO")
            continue

        print(feedback_ui["selection"])
        print_tasks_in(task_manager.search_results, False)
        break


def input_loop(answer_type, *args):
    while True:
        response = get_response(answer_type, input(status_bar()), *args)
        match response[0]:
            case t if t == answer_type:
                return response[1]
            case Response.OUT:
                print(feedback_ui["cancel"])
                return response[0]
            case _:
                print(feedback_ui["err"])
