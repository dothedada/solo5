from enum import Enum


class Defaults(Enum):
    DATA_PATH = "./data/tasks"
    RGX_PATH = "./data/config/lang/regex"
    DIFFICULTY = 2
    LANG = "es"
    TASK_SPLIT = "//"
    TASK_AMOUNT = 5
    COUNT_CURRENT_DAY = False
