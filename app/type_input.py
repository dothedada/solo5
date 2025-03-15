from enum import Enum


class Confirm(Enum):
    YES = "yes"
    NO = "no"
    CANCEL = "cancel"


class Command(Enum):
    IN_TODAY = "in_today"
    IN_GLOBAL = "in_global"
    IN_DONE = "in_done"
    ADD_TASKS = "add_tasks"
    UPDATE_TASK = "update_task"
    DONE_TASK = "done_task"
    DELETE_TASKS = "delete_tasks"
    MAKE_TODAY = "make_today"
    ENCORE_TODAY = "encore"
    SEARCH = "search"
    EXIT = "exit"
    PURGE = "purge"
    FIX_DATES = "fix_dates"
    HELP = "help"


class Response(Enum):
    CONFIRM = "confirm"
    COMMAND = "command"
    SELECTION = "selection"
    TASKS = "tasks"
    OUT = "out"

    ERR = "error"
