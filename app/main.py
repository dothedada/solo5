from manager import TaskManager
from ui_loops import program_loop
from config import ui_txt

ui_layout = ui_txt["layout"]
ui_txt = ui_txt["main"]


def main():
    taskManager = TaskManager()

    # print(ui_layout * len(ui_txt["head"]))
    # print(ui_txt["head"])
    # print(ui_layout * len(ui_txt["head"]))
    # print(ui_txt["tag"])
    program_loop(taskManager)
    # print(ui_txt["exit"])
    # print(ui_layout * len(ui_txt["exit"]))


if __name__ == "__main__":
    main()
