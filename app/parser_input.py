import re

from config import Defaults
from regexGenerator import UIRegex
from type_input import Confirm, Command, Response, Select


_PARSER = UIRegex.of(Defaults.LANG.value)


def parse_response(response_type, *args):
    # Exit command override
    if args and exit_command(args[0]):
        return (Response.COMMAND, Command.EXIT)

    handlers = {
        Response.CONFIRM: instruction("confirm"),
        Response.COMMAND: instruction("command"),
        Response.TEXT_INPUT: text_input,
        Response.SELECTION: select,
    }

    if handler := handlers.get(response_type):
        if response := handler(*args):
            return (response_type, response)

    return (Response.ERR, "NO PUDO INTERPRETAR EL INPUT")


def exit_command(input_str):
    return bool(re.search(_PARSER["command"]["exit"], input_str))


def instruction(instruction_type):
    if instruction_type not in _PARSER:
        raise ValueError(f"Key '{instruction_type}' not in Input parser")

    instructions = {"confirm": Confirm, "command": Command, "select": Select}
    instruction_enum = instructions.get(instruction_type)

    def parse_input(input_str):
        for response, regex in _PARSER[instruction_type].items():
            if re.match(regex, input_str):
                return instruction_enum(response)
        return None

    return parse_input


def text_input(input_str):
    forbidden_chars = r"[&|;`$<>\\]"
    clean_string = re.sub(forbidden_chars, "", input_str)
    if clean_string.strip():
        return clean_string[: Defaults.TASK_MAX_LENGTH.value]
    else:
        return None


def select(input_str, task_list_length):
    if batch_selection := select_string(input_str, task_list_length):
        return batch_selection

    input_str = input_str.strip(" ,-")
    if not input_str:
        return None

    tokens = [token.strip(" -") for token in input_str.split(",")]
    selection = set()

    for token in tokens:
        if set_digit := select_single_number(token, task_list_length):
            selection.update(set_digit)
            continue
        if set_range := select_range(token, task_list_length):
            selection.update(set_range)
            continue

    if not selection:
        return (Response.ERR, "ERROR AL OBTENER LA SELECCIÓN")

    return selection


def select_string(input_str, task_list_length):
    select_string = instruction("select")(input_str)
    if select_string is None or select_string == Select.NONE:
        return None

    if select_string == Select.ALL:
        return set(range(1, task_list_length + 1))


def select_single_number(input_str, task_list_length):
    if not input_str.isdigit():
        return None

    number = int(input_str)
    if 0 < number <= task_list_length:
        return {number}

    return (Response.ERR, f"FUERA DEL RANGO DE SELECCION '{number}'")


def select_range(input_str, task_list_length):
    if input_str.count("-") != 1:
        return None

    start, end = map(str.strip, input_str.split("-"))
    if not (start.isdigit() and end.isdigit()):
        print()
        return (Response.ERR, f"RANGO SOLO ACEPTA NUMEROS '{start}-{end}'")

    start, end = int(start), int(end)
    if 0 < start <= task_list_length and 1 < end <= task_list_length:
        return set(range(start, end + 1))

    return (Response.ERR, f"FUERA DEL RANGO DE SELECCION '{start} - {end}'")
