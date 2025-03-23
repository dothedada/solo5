from datetime import date
from enum import Enum
from fileManagers import load_json

settings = load_json("./data/config", "setup.json")

default_values = {
    "lang": "en",
    "task_amount": 5,
    "base_dif": 3,
    "search_results": 10,
    "context": "global",
    "task_max_length": 140,
    "carpe_diem": "False",
    "save_in_cicle": "False",
    "save_on_exit": "True",
}


class Defaults(Enum):
    DATA_PATH = "./data/tasks"
    RGX_PATH = "./data/config/lang/regex"
    UI_PATH = "./data/config/lang/ui"
    HELP_PATH = "./data/config/lang/help"
    SETUP_PATH = "./data/config"
    TASK_SPLIT = "//"
    UND_W = 2
    URG_W = 1.2
    DIF_W = 1.5

    LANG = settings["lang"]
    TASK_AMOUNT = settings["task_amount"]
    BASE_DIF = settings["base_dif"]
    SEARCH_RESULTS = settings["search_results"]
    CONTEXT = settings["context"]
    TASK_MAX_LENGTH = settings["task_max_length"]
    CARPE_DIEM = settings["carpe_diem"] == "True"
    SAVE_IN_CICLE = settings["save_in_cicle"] == "True"
    SAVE_ON_EXIT = settings["save_on_exit"] == "True"


ui_txt = load_json(Defaults.UI_PATH.value, f"{Defaults.LANG.value}.json")["ui"]


def sort_key(task):
    return (
        getattr(task, "done", False),
        task.due_date is None,
        task.due_date or date.max,
    )
