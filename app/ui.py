from uiInput import Feedback, parse_command
from config import Defaults


def user_feedback(question, type_of_answer, selection_limit):
    while True:
        response = parse_command(input(question))
        match response[0]:
            case Feedback.ERR:
                print("CANNOT UNDERSTAND YOUR INPUT, TRY AGAIN OR CANCEL.")
            case t if t == type_of_answer:
                if (
                    type_of_answer == Feedback.SELECTION
                    and len(response[1]) > selection_limit
                ):
                    print("YOU SELECTED MORE ITEMS THAT YOU WHERE ASKED")
                    continue
                return response[1]
            case Feedback.OUT:
                print("AS YOU WISH, FUCKR...")
                return response[0]
            case _:
                print("WRONG INPUT, TRY AGAIN... OR CANCEL")


def task_loop(task_manager, end_action, texts_ui, single, action_input=None):
    selection_limit = 1 if single else float("inf")
    while True:
        search_for = input("Que busca prro???")
        task_manager.add_to_search_by_task(search_for)

        if len(task_manager.search_results) == 0:
            print("SIN RESULTADOS QUE COINCIDAN...")
        elif len(task_manager.search_results) == 1:
            action = user_feedback(
                "SI, NO O QUÉ???",
                Feedback.CONFIRM,
                selection_limit,
            )
            if action == 0:
                print("SISAS")
                break
            if action == 1:
                print("NONAS, de nuevo")
                continue
            if action == 2:
                print("CANCELARRRR")
                return
        else:
            print("resultados de la busqueda")
            print("-------------------------")
            for i, task in task_manager.search_results:
                print(f"{i}) {task.task}")
                if i >= Defaults.SEARCH_RESULTS.value:
                    print("Prro, selecione mejor, porque mucho resultado")
                    break
            print("-------------------------")
            print("ea ea ea salieron varias")
            select = user_feedback(
                "Cuales???",
                Feedback.SELECTION,
                selection_limit,
            )
            print(select)
            if select == Feedback.OUT:
                print("SUETERRRRRRR :)")
                return
            task_manager.select_from_search(select)
            action = user_feedback(
                "Seguro prro?",
                Feedback.CONFIRM,
                selection_limit,
            )
            if action == 0:
                print("SISAS")
                break
            if action == 1:
                print("NONAS, de nuevo")
                continue
            if action == 2:
                print("CANCELARRRR")
                return

    if action_input is not None:
        string = input("escribe la nueva cadena")
        end_action(string)
    else:
        end_action()

    print("LISTONES!!!")
