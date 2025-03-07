from enum import Enum


class Defaults(Enum):
    DATA_PATH = "./data/tasks"
    RGX_PATH = "./data/config/lang/regex"
    BASE_DIF = 3
    LANG = "es"
    TASK_SPLIT = "//"
    TASK_AMOUNT = 5
    COUNT_CURRENT_DAY = False

    IMP_W = 13
    URG_W = 17
    DIF_W = 11
