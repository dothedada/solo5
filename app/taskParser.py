from datetime import date, timedelta
from config import Defaults
import re
import time
import random
from regexGenerator import RegexFactory
from task import Task


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


def get_month(data_dict, parser):
    month_num = data_dict.get("month_num")
    month_name = data_dict.get("month_name")

    if month_num:
        return int(data_dict.get("month_num"))
    elif month_name:
        return parser.regex_for["months"].index(month_name) + 1

    return date.today().month


def get_weekday(name, parser):
    return parser.regex_for["week"].index(name)


@matcher
def get_today_rel(match, match_index):
    return match_index


def get_date(data_dict, parser):
    if data_dict.get("from") is None:
        return date.today()

    today_rel = data_dict.get("today_rel")
    if today_rel:
        day = date.today().day + get_today_rel(today_rel, parser, "today_rel")
    else:
        day = int(data_dict["day"])
    # TODO: calcular el dia base a partir del weekday
    # weekday     -> nombre del día de la semana("lunes", "martes", ...)

    month = get_month(data_dict, parser)
    year = data_dict.get("year", date.today().year)

    if date(year, month, day) < date.today():
        year += 1

    return date(year, month, day)


def get_date_modifier(data_dict, parser):
    if data_dict.get("modifier"):
        return 0, 0, 0

    parsed_amount = data_dict.get("amount", None)
    amount = 0

    if parsed_amount:
        if parsed_amount.isnumeric():
            amount = int(parsed_amount)
        else:
            # NOTE: lista correspondiente a cantidad? proxima, un, una...???
            amount += 1

    def add_amount(unit):
        if data_dict.get(unit) is None:
            return 0
        return int(unit) + amount

    days = add_amount("unit_day") + add_amount("unit_week") * 7
    months = add_amount("unit_month")
    years = add_amount("unit_year")

    return days, months, years


@matcher
def parse_due_date(match, match_index):
    if match is None:
        return None

    data_dict = dict(match.groupdict())
    print(data_dict)
    base_date = get_date(data_dict, RegexFactory("es"))

    if data_dict.get("date"):
        return base_date

    add_days, add_monts, add_years = get_date_modifier(data_dict, RegexFactory("es"))

    return base_date + timedelta(
        days=add_days,
        months=add_monts,
        years=add_years,
    )


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


test = "12 de noviembre // este martes // hoy // mañana"
parse_task(test, "es")
