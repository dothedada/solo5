from parser_input import get_response, get_exit
from ui_elements import bar_info, print_tasks_in
from type_input import Response, Confirm, Command
from config import Defaults
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


input_bar = bar_info()


def program_loop(manager):
    where = manager.tasks
    input_bar(context="GLOBAL")
    while True:
        action = get_response(Response.COMMAND, input(input_bar()))

        if action[0] != Response.COMMAND:
            print("ÑO ENTENDÍ")

        match action[1]:
            case Command.ADD_TASKS:
                input_bar(command="AÑADIR")
                tasks_str = input(input_bar())
                manager.add_tasks(tasks_str)
            case Command.DELETE_TASKS:
                input_bar(command="BORRAR")
                action_loop(manager, Command.DELETE_TASKS, where, False)
            case Command.UPDATE_TASK:
                input_bar(command="ACTUALIZAR")
                action_loop(manager, Command.UPDATE_TASK, where, True)
            case Command.DONE_TASK:
                input_bar(command="TERMINADAS")
                action_loop(manager, Command.DONE_TASK, where, False)
            case Command.IN_GLOBAL:
                change_context(where, manager.tasks, "GLOBAL")
            case Command.IN_TODAY:
                change_context(where, manager.today_tasks, "HOY")
            case Command.IN_DONE:
                change_context(where, manager.done_tasks, "TERMINADAS")
            case Command.SAVE:
                manager.save_tasks_to_csv()
                print("TASKS SAVED")
            case Command.EXIT:
                return
            case Command.PURGE:
                manager.purge_done()
                print("DONE TASKS WERE PURGE")
            case _:
                print("UNKNOWN COMMAND")

        input_bar(command="", action="")


def change_context(current_context, new_context, context_name):
    if current_context != new_context:
        current_context = new_context
        input_bar(context=context_name)
        print("CONTEXTO CAMBIADO", context_name)
    else:
        print("YA ESTAS EN CONTEXTO", context_name)


def action_loop(task_manager, action, where, single):
    while True:
        input_bar(action="BUSCAR")
        search_for = input(input_bar())
        if get_exit(search_for):
            print(feedback_ui["cancel"])
            return

        task_manager.add_to_search_by_task(search_for)

        if len(task_manager.search_results) == 0:
            print(feedback_ui["search_no_match"])
            continue

        if len(task_manager.search_results) == 1:
            print(feedback_ui["warn"])
            print(f'"{task_manager.search_results[0][1].task}"')
        else:
            print(f'\n{feedback_ui["search_results"]}')
            input_bar(action="SELECCIONAR")
            selection_loop(task_manager, single)

        if not task_manager.search_results:
            return

        if Defaults.CARPE_DIEM.value:
            break

        input_bar(action="CONFIRMAR")
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


def resolve_action(task_manager, command):
    actions = {
        Command.ADD_TASKS: task_manager.add_tasks,
        Command.DELETE_TASKS: task_manager.delete_task,
        Command.DONE_TASK: task_manager.mark_tasks_done,  # str arg
        Command.UPDATE_TASK: task_manager.update_task,  # bool arg
    }

    if command == Command.UPDATE_TASK:
        actions[command](input(input_ui["new_data"]))
    else:
        actions[command]()


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
        response = get_response(answer_type, input(input_bar()), *args)
        match response[0]:
            case t if t == answer_type:
                return response[1]
            case Response.OUT:
                print(feedback_ui["cancel"])
                return response[0]
            case _:
                print(feedback_ui["err"])
