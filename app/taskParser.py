import re
from datetime import date, timedelta
import time
import random
from fileLoaders import load_json
from enum import Enum
from task import Task


class Defaults(Enum):
    DIFICULTY = 2
    LANG = "es"
    TASK_SECUENCER = "//"


class RegexFactory:
    def __init__(self, lang):
        self.globals = load_json("./data/config/lang/regex", "globals.json")
        self.locals = load_json("./data/config/lang/regex", f"{lang}.json")
        self.regex_for = self.__get_regex()

    def __compile_rgx(self, *patterns):
        return re.compile("|".join(patterns), re.IGNORECASE)

    def __get_regex(self):
        self.__dificulty_ptt = [self.__compile_rgx(self.globals["dificulty"])]
        self.__date_ptt = []

        for dificulty_level in self.locals.get("dificulty", []):
            self.__dificulty_ptt.append(self.__compile_rgx(dificulty_level))

        date_names = {
            "week": "|".join(self.locals.get("week", [])),
            "months": "|".join(self.locals.get("months", [])),
        }
        for date_format in self.locals["dates"]:
            date_pattern = date_format.replace(
                "{week}",
                date_names["week"],
            ).replace(
                "{months}",
                date_names["months"],
            )
            date_regex = self.__compile_rgx(date_pattern)
            self.__date_ptt.append(date_regex)

        return {
            "week": self.locals.get("week", []),
            "months": self.locals.get("months", []),
            "important": self.__compile_rgx(
                self.globals["important"],
                *self.locals.get("important", ""),
            ),
            "project": self.__compile_rgx(
                self.globals["project"],
                *self.locals.get("project", []),
            ),
            "dificulty": self.__dificulty_ptt,
            "dates": self.__date_ptt,
        }


def id_maker(string):
    char_sum = sum(ord(char) for char in string)
    timestamp = int(time.time() * 1000)
    salt = random.randint(1, 9999)
    base_id = (char_sum * timestamp * salt) % (2**64)

    return hex(base_id)[2:]


def parse_important(string, parser):
    parsed = re.search(parser.regex_for["important"], string)
    return parsed is not None


def parse_dificulty(string, parser):
    current = None
    for i, pattern in enumerate(parser.regex_for["dificulty"]):
        match = re.search(pattern, string)
        if match:
            current = i

    return Defaults.DIFICULTY.value if current is None else current


def parse_project(string, parser):
    parsed = re.search(parser.regex_for["project"], string)
    return parsed.group()[1:] if parsed else None


def parse_due_date(string, parser):
    data = {}

    for date_format in parser.regex_for["dates"]:
        match = re.search(date_format, string)
        if match:
            data = dict(match.groupdict())
            break

    if len(data) == 0:
        return None

    if all(key in data for key in ["day_num", "month_num", "month_name"]):
        year = date.today().year
        month = 0
        day = int(data.get("day_num", 1))

        if data.get("month_num"):
            month = int(data.get("month_num"))
        else:
            month = parser.regex_for["months"].index(data["month_name"]) + 1

        if date(year, month, day) < date.today():
            year += 1

        return date(year, month, day)

    if all(key in data for key in ["day_start_absolute", "addition"]):
        today = date.today()
        weekday = 0

        for i, pattern in enumerate(parser.regex_for["week"]):
            regex = re.compile(pattern, re.IGNORECASE)
            match = re.match(regex, data["day_start_absolute"])
            if match:
                weekday = i
                break

        difference = (weekday - today.weekday() + 7) % 7
        difference += int(data["addition"]) - 1

        return date.today() + timedelta(days=difference)

    if all(key in data for key in ["day_end_absolute", "add_week"]):
        weekday = 0
        today = date.today()
        print(data)

        for i, pattern in enumerate(parser.regex_for["week"]):
            regex = re.compile(pattern, re.IGNORECASE)
            match = re.match(regex, data["day_end_absolute"])
            if match:
                weekday = i
                break

        difference = (weekday - today.weekday() + 7) % 7
        if data["add_week"]:
            difference += 7

        return today + timedelta(days=difference)

    if "addition" in data:
        return date.today() + timedelta(days=int(data["addition"]) - 1)


def parse_task(string, lang):
    # NOTE: ver como vinculamos la regex factory
    parser = RegexFactory(lang)
    tasks = []

    for i, task_raw in enumerate(string.split(Defaults.TASK_SECUENCER.value)):
        tasks.append(
            Task(
                {
                    "lang": lang,
                    "id": id_maker(task_raw),
                    "task": task_raw,
                    "creation_date": date.today(),
                    "due_date": parse_due_date(task_raw, parser),
                    "project": parse_project(task_raw, parser),
                    "important": parse_important(task_raw, parser),
                    "dificulty": parse_dificulty(task_raw, parser),
                    "parent": None if i == 0 else tasks[i - 1].id,
                }
            )
        )

    return tasks


test = "Holi! muy fácil // creo que difícil // y si es muy dificil? // sin lio"
print(parse_task(test, "es"))
