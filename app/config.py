from enum import Enum


class Defaults(Enum):
    DATA_PATH = "./data/tasks"
    RGX_PATH = "./data/config/lang/regex"
    BASE_DIF = 2
    LANG = "es"
    TASK_SPLIT = "//"
    TASK_AMOUNT = 5
    COUNT_CURRENT_DAY = False

    IMP_W = 0.4
    URG_W = 0.3
    DIF_W = 0.1
