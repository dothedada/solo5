from enum import Enum
from fileManagers import load_json

data_config = load_json("./data/config", "setup.json")


class Defaults(Enum):
    LANG = data_config["lang"]
    DATA_PATH = data_config["data_path"]
    RGX_PATH = data_config["rgx_path"]
    UI_PATH = data_config["ui_path"]
    TASK_SPLIT = data_config["task_split"]

    TASK_AMOUNT = data_config["task_amount"]
    BASE_DIF = data_config["base_difficulty"]
    UND_W = data_config["undelayable_weight"]
    URG_W = data_config["urgent_weight"]
    DIF_W = data_config["diffficulty_weight"]

    SEARCH_RESULTS = 5  # Limitar la salida de los resultados
    CARPE_DIEM = False  # No confirmar acciones

    CONTEXT = "global"

    TASK_MAX_LENGTH = 140

    SAVE_IN_CICLE = True
    SAVE_ON_EXIT = True

    COUNT_CURRENT_DAY = data_config["count_current_day"] == "False"


ui_txt = load_json(Defaults.UI_PATH.value, "es.json")["ui"]

colors = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

styles = {
    "bold": "\033[1m",
    "underline": "\033[4m",
    "strike": "\033[9m",
}
