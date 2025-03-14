from enum import Enum
from regexGenerator import UIRegex
import re


class Input_t(Enum):
    CONFIRM = "c"
    RANGE = "r"
    NUMBER = "n"
    OUT = "o"
    ERR = "e"


def get_command(input_str):
    regex = UIRegex.of("es")

    for i, pattern in enumerate(regex["confirmation"]):
        if re.search(pattern, input_str):
            return (Input_t.CONFIRM, i)

    for pattern in regex["exit"]:
        if re.search(pattern, input_str):
            return (Input_t.OUT, 0)

    return None


def get_number(input_str):
    if input_str.isdigit():
        return (Input_t.NUMBER, int(input_str))

    return None


def get_range(input_str):
    selection = set()
    tokens = map(lambda token: token.strip(" -"), input_str.split(","))
    for token in tokens:
        if token.isdigit():
            selection.add(int(token))
        elif token.count("-") == 1:
            start, end = map(str.strip, token.split("-"))
            if not start.isdigit() or not end.isdigit():
                return None
            selection.update(range(int(start), int(end) + 1))
        else:
            return None

    return (Input_t.RANGE, selection) if len(selection) > 0 else None


def parse_command(input_str):  # TUPLE (type, value)
    if input_str == "0":
        return (Input_t.OUT, None)
    if number := get_number(input_str):
        return number
    if numbers_range := get_range(input_str):
        return numbers_range
    if command := get_command(input_str):
        return command

    return (Input_t.ERR, f"Invalid input: {input_str}")
