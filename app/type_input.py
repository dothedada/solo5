from enum import Enum


class Response(Enum):
    CONFIRM = "confirm"
    COMMAND = "command"
    SELECTION = "selection"
    TEXT_INPUT = "text_input"
    OUT = "out"

    ERR = "error"


class Confirm(Enum):
    YES = "yes"
    NO = "no"
    CANCEL = "cancel"


class Select(Enum):
    ALL = "all"
    NONE = "none"


class Command(Enum):
    IN_TODAY = "in_today"
    IN_GLOBAL = "in_global"
    IN_DONE = "in_done"
    PRINT = "print"
    ADD_TASKS = "add_tasks"
    UPDATE_TASK = "update_task"
    DONE_TASK = "done_task"
    DELETE_TASKS = "delete_tasks"
    MAKE_TODAY = "make_today"
    ENCORE_TODAY = "encore"
    FORECAST = "forecast"
    SEARCH = "search"
    CLEAR = "clear"
    SAVE = "save"
    EXIT = "exit"
    PURGE = "purge"
    FIX_DATES = "fix_dates"
    HELP = "help"
