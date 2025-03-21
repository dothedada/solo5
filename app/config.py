from datetime import date
from enum import Enum
from fileManagers import load_json

settings = load_json("./data/config", "setup.json")


class Defaults(Enum):
    DATA_PATH = settings["data_path"]
    RGX_PATH = settings["rgx_path"]
    UI_PATH = settings["ui_path"]
    TASK_SPLIT = settings["task_split"]
    UND_W = settings["undelayable_weight"]
    URG_W = settings["urgent_weight"]
    DIF_W = settings["diffficulty_weight"]

    LANG = settings["lang"]
    TASK_AMOUNT = settings["task_amount"]
    BASE_DIF = settings["base_dif"]
    SEARCH_RESULTS = settings["search_results"]
    CONTEXT = settings["context"]
    TASK_MAX_LENGTH = settings["task_max_length"]
    CARPE_DIEM = settings["carpe_diem"] == "True"
    SAVE_IN_CICLE = settings["save_in_cicle"] == "True"
    SAVE_ON_EXIT = settings["save_on_exit"] == "True"


ui_txt = load_json(Defaults.UI_PATH.value, "es.json")["ui"]


def sort_key(task):
    return (
        getattr(task, "done", False),
        task.due_date is None,
        task.due_date or date.max,
    )
