from parser_input import get_response, get_exit
from type_input import Response, Confirm, Command
from config import Defaults
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


def program_loop(manager):
    where = manager._tasks
    position = "> "
    while True:
        do = get_response(Response.COMMAND, input(position))

        print("cmd:", do)

        if do[0] != Response.COMMAND:
            print("ÑO ENTENDÍ")

        match do[1]:
            case Command.ADD_TASKS:
                tasks_str = input("ADD TASKS:\n")
                manager.add_tasks(tasks_str)
            case Command.DELETE_TASKS:
                action_loop(manager, Command.DELETE_TASKS, where, False)
            case Command.UPDATE_TASK:
                action_loop(manager, Command.UPDATE_TASK, where, True)
            case Command.DONE_TASK:
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

        print(manager._tasks)


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


def action_loop(task_manager, action, where, single):
    while True:
        search_for = input(f'\n{input_ui["look_for"]}')
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
            selection_loop(task_manager, single)

        if Defaults.CARPE_DIEM.value:
            break

        confirmation = input_loop(input_ui["confirmation"], Response.CONFIRM)
        match Confirm(confirmation):
            case Confirm.YES:
                break
            case Confirm.CANCEL:
                print(feedback_ui["cancel"])
                return
            case _:
                pass

    resolve_action(task_manager, action)
    print(feedback_ui["done"])


def selection_loop(task_manager, single):
    while True:
        print_tasks_in(task_manager.search_results, True)
        select = input_loop(
            input_ui["which_one"] if single else input_ui["which_ones"],
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


def input_loop(question, answer_type, *args):
    while True:
        response = get_response(answer_type, input(f"\n{question}:\n"), *args)
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
