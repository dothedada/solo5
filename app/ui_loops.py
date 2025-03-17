from parser_input import get_response, get_exit
from ui_elements import context_wrapper, print_search, print_context
from type_input import Response, Confirm, Command
from config import Defaults
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


state = context_wrapper()

# TODO:
# 2. Revisar los EXIT y los CANCEL, y el clear que deben detonar
# 3. asignar textos de UI
# 3.1 crear ALL para seleccionar todas las casillas en select y NONE para 0
# 4. todo lo relacionado con today (make, encore, forecast)
# 4.1 algoritmo para armar día
# 5. completar condicionales del program loop
# 6. revisar textos ui
# 7. documentacion


def program_loop(task_manager):
    state(manager=task_manager)
    while True:
        action = get_response(Response.COMMAND, input(state()["bar"]))

        if action[0] != Response.COMMAND:
            print("ÑO ENTENDÍ")

        match action[1]:
            case Command.IN_TODAY:
                state(context="today")
            case Command.IN_GLOBAL:
                state(context="global")
            case Command.IN_DONE:
                state(context="done")
            case Command.PRINT:
                print_context(state()["where"])
            case Command.ADD_TASKS:
                # TODO: bloquear en DONE, complementar en TODAY
                tasks_str = input(state(command=Command.ADD_TASKS)["bar"])
                task_manager.add_tasks(tasks_str)
            case Command.UPDATE_TASK:
                # TODO: bloquear en DONE, complementar en TODAY
                state(command=Command.UPDATE_TASK)
                action_loop(task_manager, Command.UPDATE_TASK, True)
            case Command.DONE_TASK:
                # TODO: marcar como UNDONE, devolver a task
                state(command=Command.DONE_TASK)
                action_loop(task_manager, Command.DONE_TASK, False)
            case Command.DELETE_TASKS:
                # TODO: al borrar de GLOBAL se elimina de HOY
                state(command=Command.DELETE_TASKS)
                action_loop(task_manager, Command.DELETE_TASKS, False)

            case Command.SEARCH:
                task_manager.search_results.clear()
                search_loop(task_manager, True)
            case Command.CLEAR:
                task_manager.search_results.clear()
            case Command.SAVE:
                task_manager.save_tasks_to_csv()
                task_manager.save_tasks_done()
                print("TASKS SAVED")
            case Command.EXIT:
                return
            case Command.PURGE:
                task_manager.purge_done()
                print("DONE TASKS WERE PURGE")
            case Command.FIX_DATES:
                fixed_tasks = task_manager.fix_dates()
                if fixed_tasks:
                    print("ALL TASK DUE DATES WERE UPDATES", fixed_tasks)
                else:
                    print("NO DUE DATES NEEDED TO BE FIXED")
            case _:
                print("UNKNOWN COMMAND")

        state(command="", action="")
        print("----")


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

        look_for = input(state(action="BUSCAR")["bar"])
        if get_exit(look_for):
            print(feedback_ui["cancel"])
            return False

        task_manager.add_to_search_by_task(look_for, state()["where"])

        if task_manager.search_results:
            if len(task_manager.search_results) == 1:
                print(feedback_ui["warn"])
                print(f'"{task_manager.search_results[0][1].task}"')
            else:
                print(f'\n{feedback_ui["search_results"]}')
                state(action="SELECCIONAR")
                selection_loop(task_manager, single)

            if not task_manager.search_results:
                return False

            return True

        print(feedback_ui["search_no_match"])


def action_loop(task_manager, action, single):
    while True:
        if not task_manager.search_results:
            if search_loop(task_manager, single) is False:
                return

        if Defaults.CARPE_DIEM.value:
            break

        state(action="CONFIRMAR")
        print(input_ui["confirmation"])
        confirmation = input_loop(Response.CONFIRM)
        if confirmation == Response.OUT:
            task_manager.search_results.clear()
            return
        match Confirm(confirmation):
            case Confirm.YES:
                break
            case Confirm.CANCEL:
                print(feedback_ui["cancel"])
                task_manager.search_results.clear()
                return
            case Confirm.NO:
                pass
            case Response.OUT:
                return

    resolve_action(task_manager, action)
    state(command="", action="")
    print(feedback_ui["done"])


def selection_loop(task_manager, single):
    while True:
        print_search(task_manager.search_results, True)
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
        print_search(task_manager.search_results, False)
        break


def input_loop(answer_type, *args):
    while True:
        response = get_response(answer_type, input(state()["bar"]), *args)
        print(response)
        match response[0]:
            case t if t == answer_type:
                return response[1]
            case Response.OUT:
                print(feedback_ui["cancel"])
                return response[0]
            case _:
                print(feedback_ui["err"])
