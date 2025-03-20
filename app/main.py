from manager import TaskManager
from ui_loops import program_loop
from ui_elements import print_ui
from config import ui_txt

ui_layout = ui_txt["layout"]
ui_txt = ui_txt["main"]


def main():

    print_ui("main", "head", top=True, style="bold", full=True)
    taskManager = TaskManager()
    print("\n")
    print_ui("main", "tag")

    program_loop(taskManager)

    print("\n")
    print_ui("main", "exit", bottom=True, color="green", full=True)
    print("\n")


if __name__ == "__main__":
    main()
