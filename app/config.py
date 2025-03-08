from enum import Enum


class Defaults(Enum):
    LANG = "es"
    DATA_PATH = "./data/tasks"
    RGX_PATH = "./data/config/lang/regex"
    TASK_SPLIT = "//"

    TASK_AMOUNT = 5
    BASE_DIF = 3
    UND_W = 13
    URG_W = 17
    DIF_W = 11

    COUNT_CURRENT_DAY = False
