import re

from config import ui_txt
from regexGenerator import parser_ui
from type_input import Confirm, Command, Response, Select
from parser_task import sanitize_text


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
        response = handler(*args)

        if isinstance(response, tuple):
            return response  # Error tuple
        else:
            return (response_type, response)

    return (Response.ERR, ui_txt["err"]["no_match"])


def exit_command(input_str):
    return bool(re.search(parser_ui["command"]["exit"], input_str))


def instruction(instruction_type):
    if instruction_type not in parser_ui:
        raise ValueError(f"'{instruction_type}' {ui_txt['err']['no_parser']}")

    instructions = {
        "confirm": Confirm,
        "command": Command,
        "select": Select,
    }
    instruction_enum = instructions.get(instruction_type)

    def parse_input(string):
        for response, regex in parser_ui[instruction_type].items():
            if re.match(regex, string):
                return instruction_enum(response)

        return (Response.ERR, f"{ui_txt['err']['no_instruction']} '{string}'")

    return parse_input


def text_input(input_str):
    string = sanitize_text(input_str)
    return string if string else None


def select(input_str, task_list_length):
    batch_selection = select_string(input_str, task_list_length)
    if batch_selection is not None:
        return batch_selection

    input_str = input_str.strip(" ,-")
    if not input_str:
        return None

    tokens = [token.strip(" -") for token in input_str.split(",")]
    selection = set()

    for token in tokens:
        if set_digit := select_single_number(token, task_list_length):
            if isinstance(set_digit, tuple) and set_digit[0] == Response.ERR:
                return set_digit

            selection.update(set_digit)
            continue
        if set_range := select_range(token, task_list_length):
            if isinstance(set_range, tuple) and set_range[0] == Response.ERR:
                return set_range

            selection.update(set_range)
            continue

    return selection


def select_string(input_str, task_list_length):
    select_string = instruction("select")(input_str)
    if select_string is None:
        return None

    if select_string == Select.NONE:
        return set()  # Empty Selection

    if select_string == Select.ALL:
        return set(range(1, task_list_length + 1))


def select_single_number(input_str, task_list_length):
    if not input_str.isdigit():
        return None

    number = int(input_str)
    return (
        {number}
        if 0 < number <= task_list_length
        else (Response.ERR, f"{ui_txt['err']['out_range']} '{number}'")
    )


def select_range(input_str, task_list_length):
    if input_str.count("-") != 1:
        return None

    start, end = map(str.strip, input_str.split("-"))
    if not (start.isdigit() and end.isdigit()):
        return (Response.ERR, f"{ui_txt['err']['only_int']} '{input_str}'")

    start, end = int(start), int(end)
    if 0 < start <= task_list_length and 1 < end <= task_list_length:
        return set(range(start, end + 1))

    return (Response.ERR, f"{ui_txt['err']['out_range']} '{start} - {end}'")
