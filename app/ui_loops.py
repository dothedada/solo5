from parser_input import get_response, get_exit
from type_input import Response, Confirm, Command
from config import Defaults
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


def bar_info():
    state = ["", "", ""]

    def context_manager(context=None, command=None, action=None):
        for i, info in enumerate([context, command, action]):
            if info is not None:
                state[i] = info
        return f"{'> '.join(filter(bool,state))}> "

    return context_manager


bar = bar_info()


def program_loop(manager):
    where = manager._tasks
    bar(context="GLOBAL")
    while True:
        action = get_response(Response.COMMAND, input(bar()))

        if action[0] != Response.COMMAND:
            print("ÑO ENTENDÍ")

        match action[1]:
            case Command.ADD_TASKS:
                bar(command="AÑADIR")
                tasks_str = input(bar())
                manager.add_tasks(tasks_str)
            case Command.DELETE_TASKS:
                bar(command="BORRAR")
                action_loop(manager, Command.DELETE_TASKS, where, False)
            case Command.UPDATE_TASK:
                bar(command="ACTUALIZAR")
                action_loop(manager, Command.UPDATE_TASK, where, True)
            case Command.DONE_TASK:
                bar(command="TERMINADAS")
                action_loop(manager, Command.DONE_TASK, where, False)
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

        bar(command="", action="")


def action_loop(task_manager, action, where, single):
    while True:
        bar(action="BUSCAR")
        search_for = input(bar())
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
            bar(action="SELECCIONAR")
            selection_loop(task_manager, single)

        if not task_manager.search_results:
            return

        if Defaults.CARPE_DIEM.value:
            break

        bar(action="CONFIRMAR")
        print(input_ui["confirmation"])
        confirmation = input_loop(Response.CONFIRM)
        print(confirmation)
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
        response = get_response(answer_type, input(bar()), *args)
        match response[0]:
            case t if t == answer_type:
                return response[1]
            case Response.OUT:
                print(feedback_ui["cancel"])
                return response[0]
            case _:
                print(feedback_ui["err"])


def print_tasks_in(task_list, limit):
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
    for i, task in task_list:
        if limit and i > Defaults.SEARCH_RESULTS.value:
            print(f'\n{feedback_ui["search_overflow"]}')
            break
        print(f"{i}) {task.task}")
    print(feedback_ui["line"] * len(feedback_ui["search_results"]))
