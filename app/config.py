from enum import Enum
from fileManagers import load_json

data_config = load_json("./data/config", "setup.json")


class Defaults(Enum):
    LANG = data_config["lang"]
    DATA_PATH = data_config["data_path"]
    RGX_PATH = data_config["rgx_path"]
    TASK_SPLIT = data_config["task_split"]

    TASK_AMOUNT = data_config["task_amount"]
    BASE_DIF = data_config["base_difficulty"]
    UND_W = data_config["undelayable_weight"]
    URG_W = data_config["urgent_weight"]
    DIF_W = data_config["diffficulty_weight"]

    COUNT_CURRENT_DAY = data_config["count_current_day"] == "False"
