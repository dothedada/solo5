from parser_input import get_response
from type_input import Response, Confirm, Command
from config import Defaults
from fileManagers import load_json

# NOTE: UBICAR en algún puto lado
feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


def program_loop(manager):
    where = manager._tasks
    while True:
        do = get_response(
            Response.COMMAND,
            input("[A]GREGAR, [ACT]UALIZAR, [BORRAR]"),
        )

        print("asdasdasd", do)

        if do[0] != Response.COMMAND:
            raise ValueError("ÑO ENTENDÍ")

        match do[1]:
            case Command.ADD_TASKS:
                tasks_str = input("ADD TASKS:\n")
                manager.add_tasks(tasks_str)
            case Command.DELETE_TASKS:
                action_loop(manager, manager.delete_task, where, False)
            case Command.UPDATE_TASK:
                action_loop(manager, manager.update_task, where, True, True)
            case Command.DONE_TASK:
                action_loop(manager, manager.mark_tasks_done, where, False)
            case Command.SAVE:
                manager.save_tasks_to_csv()
                print("TASKS SAVED")
            case Command.EXIT:
                return
            case Command.PURGE:
                manager.purge_done()
                print("DONE TASKS WERE PURGE")
            case _:
                print("NO COMMAND WERE CHOOSE...")

        print(manager._tasks)


def action_loop(task_manager, callback, where, single, action_imput=False):
    while True:
        search_for = input(f'\n{input_ui["look_for"]}')
        task_manager.add_to_search_by_task(search_for)

        if len(task_manager.search_results) == 0:
            print(feedback_ui["search_no_match"])
            continue
        elif len(task_manager.search_results) == 1:
            print(feedback_ui["warn"])
            print(f'"{task_manager.search_results[0][1].task}"')
        else:
            print(f'\n{feedback_ui["search_results"]}')
            selection_loop(task_manager, single)

        if Defaults.CARPE_DIEM.value:
            break

        action = input_loop(
            input_ui["confirmation"],
            Response.CONFIRM,
        )

        match Confirm(action):
            case Confirm.YES:
                break
            case Confirm.NO:
                continue
            case Confirm.CANCEL:
                print(feedback_ui["cancel"])
                return

    if action_imput:
        string = input(input_ui["new_data"])
        callback(string)
    else:
        callback()

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
