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
        self.__global = load_json("./data/config/lang/regex", "globals.json")
        self.__local = load_json("./data/config/lang/regex", f"{lang}.json")
        self.regex_for = self.__get_regex()

    def __regex_compiler(self, pattern_name):
        patterns = []
        global_pattern = self.__global.get(pattern_name, None)
        if global_pattern is not None:
            patterns.append(re.compile(global_pattern, re.IGNORECASE))

        for pattern in self.__local.get(pattern_name, []):
            patterns.append(re.compile(pattern, re.IGNORECASE))

        return patterns

    def __get_regex(self):
        week = "|".join(self.__local.get("week", []))
        months = "|".join(self.__local.get("months", []))
        dates_formatted = []
        for date_format in self.__local["dates"]:
            date_pattern = date_format.replace("{week}", week).replace(
                "{months}", months
            )
            dates_formatted.append(date_pattern)
        self.__local["dates"] = dates_formatted

        return {
            "week": week,
            "months": months,
            "project": self.__regex_compiler("project"),
            "important": self.__regex_compiler("important"),
            "dificulty": self.__regex_compiler("dificulty"),
            "dates": self.__regex_compiler("dates"),
        }


def matcher(func):
    def wrapper(string, parser, regex_source):
        for i, pattern in enumerate(parser.regex_for[regex_source]):
            match = re.search(pattern, string)
            if match:
                return func(match=match, match_index=i)

        return func(match=None, match_index=-1)

    return wrapper


@matcher
def parse_important(match, match_index):
    return False if match is None else True


@matcher
def parse_dificulty(match, match_index):
    return Defaults.DIFICULTY.value if match is None else match_index


@matcher
def parse_project(match, match_index):
    return match.group()[1:] if match else None


@matcher
def parse_due_date(match, match_index):
    if match is None:
        return None

    data = dict(match.groupdict())

    return data


def id_maker(string):
    char_sum = sum(ord(char) for char in string)
    timestamp = int(time.time() * 1000)
    salt = random.randint(1, 9999)
    base_id = (char_sum * timestamp * salt) % (2**64)

    return hex(base_id)[2:]


def parse_task(string, lang):
    parser = RegexFactory(lang)
    tasks = []

    for i, task_raw in enumerate(string.split(Defaults.TASK_SECUENCER.value)):
        task = Task(
            {
                "lang": lang,
                "id": id_maker(task_raw),
                "task": task_raw,
                "creation_date": date.today(),
                "project": parse_project(task_raw, parser, "project"),
                "important": parse_important(task_raw, parser, "important"),
                "dificulty": parse_dificulty(task_raw, parser, "dificulty"),
                "due_date": parse_due_date(task_raw, parser, "dates"),
                "parent": None if i == 0 else tasks[i - 1].id,
            }
        )
        tasks.append(task)

    return tasks


test = "hola! 25 de noviembre // proximo martes"
print(parse_task(test, "es"))

# if all(key in data for key in ["day_num", "month_num", "month_name"]):
#     year = date.today().year
#     month = 0
#     day = int(data.get("day_num", 1))
#
#     if data.get("month_num"):
#         month = int(data.get("month_num"))
#     else:
#         month = parser.regex_for["months"].index(data["month_name"]) + 1
#
#     if date(year, month, day) < date.today():
#         year += 1
#
#     return date(year, month, day)
#
# if all(key in data for key in ["day_start_absolute", "addition"]):
#     today = date.today()
#     weekday = 0
#
#     for i, pattern in enumerate(parser.regex_for["week"]):
#         regex = re.compile(pattern, re.IGNORECASE)
#         match = re.match(regex, data["day_start_absolute"])
#         if match:
#             weekday = i
#             break
#
#     difference = (weekday - today.weekday() + 7) % 7
#     difference += int(data["addition"]) - 1
#
#     return date.today() + timedelta(days=difference)
#
# if all(key in data for key in ["day_end_absolute", "add_week"]):
#     weekday = 0
#     today = date.today()
#     print(data)
#
#     for i, pattern in enumerate(parser.regex_for["week"]):
#         regex = re.compile(pattern, re.IGNORECASE)
#         match = re.match(regex, data["day_end_absolute"])
#         if match:
#             weekday = i
#             break
#
#     difference = (weekday - today.weekday() + 7) % 7
#     difference += 7 if data["add_week"] else 0
#
#     return today + timedelta(days=difference)
#
# if "addition" in data:
#     return date.today() + timedelta(days=int(data["addition"]) - 1)
"""
    # Valores absolutos
    abs_day        -> día absoluto (número)
    abs_month_num  -> numero del mes
    abs_month_name -> nombre del mes
    abs_year       -> año (opcional, asume actual/siguiente)

    # Valores relativos
    ref_point      -> inicio del calculo ("de", "de este", "dentro de")

    # Referencias relativas
    rel_base       -> referencia relativo ("hoy", "mañana", "pasado mañana")
    rel_weekday    -> día de la semana relativo("lunes", "martes", ...)
    rel_modifier   -> modificador dw la interpretación ("próximo", "siguiente")

    # Componentes para adiciones
    amount         -> cantidad numérica para incremento/decremento
    unit           -> unidad de tiempo (día, semana, mes, año)

    estructura del tiempo:
    dia
    semana (7 días)
    mes

    "(?P<day_num>[0-9]{1,2})(?:\\/(?P<month_num>[0-9]{1,2})| de (?P<month_name>{months}))",
    "(?:de este (?P<day_start_absolute>{week})) en (?P<addition>\\d+) d[ií]as?",
    "(?:el |este |(?P<add_week>pr[oó]ximo) )(?P<day_end_absolute>{week})",
    "(?:dentro de |en )(?P<addition>\\d+) d[ií]as?"
"""
