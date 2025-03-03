import re
from datetime import date
import time
import random
from fileLoaders import load_json
from enum import Enum


class Defaults(Enum):
    DIFICULTY = 3
    LANG = "es"


class RegexFactory:
    def __init__(self, lang):
        self.globals = load_json("./data/config/lang/regex", "globals.json")
        self.locals = load_json("./data/config/lang/regex", f"{lang}.json")
        self.regex_for = self.__get_regex()

    def __compile_rgx(self, *patterns):
        return re.compile("|".join(patterns), re.IGNORECASE)

    def __get_regex(self):
        self.__date_patterns = []
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
            self.__date_patterns.append(date_regex)
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
            "dificulty": self.__compile_rgx(
                self.globals["dificulty"],
                *self.locals.get("dificulty", []),
            ),
            "dates": self.__date_patterns,
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
    # NOTE: implementar la misma estructura de parseo por loop de fechas
    parsed = re.search(parser.regex_for["dificulty"], string)

    if parsed is None:
        return Defaults.DIFICULTY.value

    if parsed.group()[1:].isnumeric():
        return int(parsed[1:])

    for i, pattern in enumerate(parser.locals["dificulty"]):
        regex = re.compile(f"^{pattern}", re.IGNORECASE)
        match = re.match(regex, parsed.group())
        if match:
            return i + 1


def parse_project(string, parser):
    parsed = re.search(parser.regex_for["project"], string)
    return parsed.group()[1:] if parsed else None


def parse_due_date(string, parser):
    values = {}

    for date_format in parser.regex_for["dates"]:
        match = re.search(date_format, string)
        if match:
            values = dict(match.groupdict())
            break

    if len(values) == 0:
        return None

    if "day_num" in values and "month_num" in values and "month_name" in values:
        day = int(values.get("day_num", 1))
        month = 0
        year = date.today().year
        if values.get("month_num"):
            month = int(values.get("month_num"))
        else:
            month = parser.regex_for["months"].index(values["month_name"]) + 1

        if date(year, month, day) < date.today():
            year += 1

        return date(year, month, day)

    if "day_start_absolute" in values and "addition" in values:
        days = 0
        weekday = 0
        for i, pattern in enumerate(parser.regex_for["week"]):
            regex = re.compile(pattern, re.IGNORECASE)
            match = re.match(regex, values["day_start_absolute"])
            if match:
                weekday = i
                break

        if weekday < date.today().weekday():
            days += date.today().weekday() - weekday + 7
        else:
            days += weekday - date.today().weekday()

        print("asd", days)
        days += int(values["addition"]) - 1

        return date(date.today().year, date.today().month, date.today().day + days)

    # (?:de este (?P<day_start_absolute>lunes|martes|mi[ee]rcoles|jueves|viernes|s[aá]bado|domingo)) en (?P<addition>\d+) d[ií]as?
    #
    if "day_relative" in values and "day_absolute" in values and "addition" in values:
        pass
    # (?P<day_relative>hoy|ma[nñ]ana)|(?:el |este |(?P<adition>pr[oó]ximo) )(?P<day_absolute>lunes|martes|mi[eé]rcoles|jueves|viernes|s[aá]bado|domingo)
    #
    if "addition" in values and "unit" in values:
        pass
    # (?:dentro de |en )(?P<addition>\d+) (?P<unit>d[ií]as?|semanas?)


def parse_task(string, lang):

    # NOTE: ver como vinculamos la regex factory
    parser = RegexFactory(lang)

    project = parse_project(string, parser)
    important = parse_important(string, parser)
    dificulty = parse_dificulty(string, parser)
    due_date = parse_due_date(string, parser)

    # "due_date",
    # "dependencies",

    return {
        "id": id_maker(string),
        "task": string,
        "creation_date": date.today(),
        "due_date": due_date,
        "lang": lang,
        "important": important,
        "project": project,
        "dificulty": dificulty,
    }


test = "el de este miercoles en 15 dias de enero martes va a ser DIFIc, @pero es importante"
print(parse_task(test, "es"))
