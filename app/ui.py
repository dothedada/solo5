text_ui = {
    "delete": {
        "search_i": "What tasks do you want to delete:\n",
        "search_no_results_p": "Sorry, 0 tasks match.",
        "search_one_match_p": "Do you want to delete:",
        "search_results_p": "Search results:",
        "confirm_i": "[y]es | [n]o, search again | [c]ancel\n",
        "deleted_p": "deleted!",
        "invalid_input_p": "input non valid",
        "select_range_p": "select which ones you wanna delete...",
        "select_instructions_i": "type the number of the task, separete with a comma",
    },
    "feedback": {
        "yes": ["y", "yes"],
        "no": ["n", "no"],
        "cancel": ["c", "cancel"],
    },
}

# NOTE: LA SELECCION MULTIPLE DEBE IR ACÁ Y PASAR EL LISTADO AL MÉTODO,
# O EL MÉTODO DEBE CONTENER TODO??? INCLUSO LOS TEXTOS DE UI???


def handle_single_match(task_manager, texts_ui):
    while True:
        print(texts_ui["search_one_match_p"])
        print(task_manager.search_results[0][1].task)
        confirmation = input(texts_ui["confirm_i"])
        if confirmation == "n":
            task_manager.search_results.clear()
            return True
        elif confirmation == "c":
            return False
        elif confirmation == "y":
            return True
        else:
            print(texts_ui["invalid_input_p"])
            continue


def handle_multiple_match(task_manager, texts_ui):
    while True:
        print(texts_ui["search_results_p"])
        for i, task in task_manager.search_results:
            print(f"{i}) {task.task}")
        print(texts_ui["select_range_p"])
        select = input(texts_ui["select_instructions_i"])
        task_manager.select_from_search(select)


def task_loop(task_manager, end_action, texts_ui, single_selection):
    while True:
        search_for = input(texts_ui["search"])
        task_manager.add_to_search_by_task(search_for)

        if len(task_manager.search_results) == 0:
            print(texts_ui["search_no_results_p"])
        elif len(task_manager.search_results) == 1:
            if handle_single_match(task_manager, texts_ui) is False:
                break
        else:
            print(texts_ui["search_results_p"])
            for i, task in task_manager.search_results:
                print(f"{i}) {task.task}")
            print(texts_ui["select_range_p"])
            select = input(texts_ui["select_instructions_i"])
            task_manager.select_from_search(select)
            task_manager[end_action]()

        if len(task_manager.search_results) > 0:
            task_manager[end_action]()
            print(text_ui["deleted_p"])

    pass


tasks_search = input("What tasks do you want to delete:\n")
taskManager.add_to_search_by_task(tasks_search)
print("Search results:")
if len(taskManager.search_results) == 0:
    print("No match found")
    continue
elif len(taskManager.search_results) == 1:
    print("Do you want to delete:")
    print(taskManager.search_results[0][1])
    confirm = input("[y]es / [n]o")
    if confirm == "n":
        print("deletion aborted")
        continue
else:
    for i, task in taskManager.search_results:
        print(f"{i}) {task.task}")
    select = input("\nselect which ones you wanna delete...")
    taskManager.select_from_search(select)
taskManager.delete_task()
