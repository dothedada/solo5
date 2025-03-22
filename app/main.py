import readline
from manager import TaskManager
from ui_loops import program_loop
from ui_elements import print_ui, print_context, print_line
from config import Defaults, ui_txt

readline


def main():

    print_ui("main", "head", top=True, style="bold", full=True, color="green")
    print_line()
    manager = TaskManager()

    if not manager.today_tasks:
        manager.make_today()

    print_context(manager.today_tasks, ui_txt["context"]["today"])

    print_ui("main", "tag")

    program_loop(manager)
    if Defaults.SAVE_ON_EXIT.value:
        manager.save_tasks_to_csv()
        manager.save_tasks_done()


if __name__ == "__main__":
    main()
