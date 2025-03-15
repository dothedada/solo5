from parser_input import Response, command
from config import Defaults
from fileManagers import load_json
from parser_input import Confirm

feedback_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["feedback"]
input_ui = load_json(Defaults.UI_PATH.value, "es.json")["ui"]["input"]


def user_input(question, type_of_answer, selection_limit):
    while True:
        response = command(input(f"\n{question}:\n"))
        match response[0]:
            case t if t == type_of_answer:
                if (
                    type_of_answer == Response.SELECTION
                    and len(response[1]) > selection_limit
                ):
                    print(feedback_ui["err_many_items"])
                    continue
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


def task_loop(task_manager, callback, single, action_input=None):
    selection_limit = 1 if single else float("inf")
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
            print_tasks_in(task_manager.search_results, True)
            select = user_input(
                input_ui["which_one"] if single else input_ui["which_ones"],
                Response.SELECTION,
                selection_limit,
            )
            if select == Response.OUT:
                return

            task_manager.select_from_search(select)
            print(feedback_ui["selection"])
            print_tasks_in(task_manager.search_results, False)

        if Defaults.CARPE_DIEM.value:
            break

        action = user_input(
            input_ui["confirmation"],
            Response.CONFIRM,
            selection_limit,
        )

        match Confirm(action):
            case Confirm.YES:
                break
            case Confirm.NO:
                continue
            case Confirm.ERR:  # NOTE: Evaluar
                print(feedback_ui["err"])
            case _:
                return

    if action_input is not None:
        string = input(input_ui["new_data"])
        callback(string)
    else:
        callback()

    print(feedback_ui["done"])
