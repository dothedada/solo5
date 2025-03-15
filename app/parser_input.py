import re

from config import Defaults
from regexGenerator import UIRegex
from type_input import Confirm, Command, Response


_PARSER = UIRegex.of(Defaults.LANG.value)


def confirm(input_str):
    for response, regex in _PARSER["confirm"].items():
        if re.search(regex, input_str):
            return Confirm(response)
    return None


def command(input_str):
    for response, regex in _PARSER["command"].items():
        if re.search(regex, input_str):
            return Command(response)
    return None


def select(input_str, task_list_length):
    if input_str.isdigit():
        return {int(input_str)}

    selection = set()
    input_str = input_str.strip(" ,-")
    tokens = map(lambda token: token.strip(" -"), input_str.split(","))
    for token in tokens:
        if token.isdigit():
            selection.add(int(token))
        elif token.count("-") == 1:
            start, end = map(str.strip, token.split("-"))
            if not start.isdigit() or not end.isdigit():
                return None
            floor = max(1, int(start))
            # TODO: mientras soluciono el paso de la tabla
            ceil = min(task_list_length, int(end))
            selection.update(range(floor, ceil + 1))
        else:
            return None

    return selection if len(selection) > 0 else None


def get_response(response_type, *args):
    if args and args[0] == "0":
        return (Response.OUT, None)

    handlers = {
        Response.CONFIRM: confirm,
        Response.COMMAND: command,
        Response.SELECTION: select,
        Response.TASKS: "0",
    }

    if handler := handlers.get(response_type):
        if response := handler(*args):
            return (response_type, response)

    return (Response.ERR, None)
