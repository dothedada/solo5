from enum import Enum
from regexGenerator import UIRegex
import re
from taskParser import InputParser


class Feedback(Enum):
    CONFIRM = "c"
    SELECTION = "n"
    OUT = "o"
    ERR = "e"


def get_selection(input_str):
    if input_str.isdigit():
        return (Feedback.SELECTION, {int(input_str)})

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
            selection.update(range(int(start), int(end) + 1))
        else:
            return None

    return (Feedback.SELECTION, selection) if len(selection) > 0 else None


input_parser = InputParser()


def parse_command(input_str):  # TUPLE (type, value)
    if input_str == "0":
        return (Feedback.OUT, None)
    if numbers_range := get_selection(input_str):
        return numbers_range
    if command := input_parser.confirm(input_str):
        return (Feedback.CONFIRM, command)

    return (Feedback.ERR, f"Invalid input: {input_str}")
