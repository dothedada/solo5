import calendar
from config import Defaults
import re
import time
import random
from regexGenerator import GetRegex
from task import Task
from datetime import date


def matcher(func):
    def wrapper(string, parser, regex_source):
        for i, pattern in enumerate(parser["regex_for"][regex_source]):
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
def parse_month_string(match, match_index):
    return match_index if match else None


@matcher
def get_today_rel(match, match_index):
    return match_index if match else 0


@matcher
def get_day_name(match, match_index):
    return match_index if match else None


@matcher
def parse_weekday(match, match_index):
    return match_index


def get_weekday_days(name, parser):
    return (parse_weekday(name, parser, "week") - date.today().weekday()) % 7


def get_month(data_dict, parser):
    month_num = data_dict.get("month_num")
    month_name = data_dict.get("month_name")

    if month_num:
        return int(data_dict.get("month_num"))
    elif month_name:
        return parse_month_string(month_name, parser, "months") + 1

    return date.today().month


def date_normalizer(year, month, day):
    try:
        date(year, month, day)
        return year, month, day
    except ValueError:
        days_in_mont = calendar.monthrange(year, month)[1]

        while day > days_in_mont:
            day -= days_in_mont
            month += 1
            if month > 12:
                month = 1
                year += 1
            days_in_mont = calendar.monthrange(year, month)[1]

    return year, month, day


def get_date(data_dict, parser):
    if data_dict.get("from") is None:
        return date.today()

    today_rel = data_dict.get("today_rel")
    if today_rel:
        day_offset = get_today_rel(today_rel, parser, "today_rel")
        base_day = date.today().day + day_offset
    elif data_dict.get("weekday"):
        weekday = get_weekday_days(data_dict.get("weekday"), parser)
        base_day = date.today().day + weekday
    elif data_dict.get("day").isnumeric():
        base_day = int(data_dict.get("day"))
    else:
        print("el dia esta mal configurado")
        base_day = 1

    base_month = get_month(data_dict, parser)
    base_year = data_dict.get("year", date.today().year)

    year, month, day = date_normalizer(base_year, base_month, base_day)

    if date(year, month, day) < date.today():
        year += 1

    return date(year, month, day)


def get_date_modifier(data_dict, parser):
    if data_dict.get("modifier") is None:
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
        return amount if data_dict.get(unit) is not None else 0

    days = add_amount("unit_day")
    days += add_amount("unit_week") * 7
    months = add_amount("unit_month")
    years = add_amount("unit_year")

    return days, months, years


@matcher
def parse_due_date(match, match_index):
    loc_parser = GetRegex.of("es")
    if match is None:
        return None

    data_dict = dict(match.groupdict())
    print(data_dict)
    base_date = get_date(data_dict, loc_parser)

    if data_dict.get("date"):
        return base_date

    add_days, add_monts, add_years = get_date_modifier(data_dict, loc_parser)

    year, month, day = date_normalizer(
        base_date.year + add_years,
        base_date.month + add_monts,
        base_date.day + add_days,
    )
    return date(year, month, day)


def id_maker(string):
    char_sum = sum(ord(char) for char in string)
    timestamp = int(time.time() * 1000)
    salt = random.randint(1, 9999)
    base_id = (char_sum * timestamp * salt) % (2**64)

    return hex(base_id)[2:]


def sanitize_task(string):
    string = string.strip()
    string = re.sub(r"\s+", " ", string)
    string = string.replace('"', '""')
    return f'"{string}"'


def parse_task(string, lang):
    parser = GetRegex.of(lang)
    tasks = []

    for i, task_raw in enumerate(string.split(Defaults.TASK_SECUENCER.value)):
        print(task_raw)
        task = Task(
            {
                "lang": lang,
                "id": id_maker(task_raw),
                "task": sanitize_task(task_raw),
                "creation_date": date.today(),
                "project": parse_project(task_raw, parser, "project"),
                "important": parse_important(task_raw, parser, "important"),
                "dificulty": parse_dificulty(task_raw, parser, "dificulty"),
                "due_date": parse_due_date(task_raw, parser, "dates"),
                "parent": None if i == 0 else tasks[i - 1].id,
            }
        )
        print(task)
        tasks.append(task)

    return tasks


test = 'de mañana en 8 días "caigo" a jalizco      si,   ... eso creo \n ñoooo'
# test = "12/05" # 12 de mayo de 2025
# test = "25 de diciembre" # 25 de diciembre de 2025
# test = "01-11" # 1 de noviembre de 2025
# test = "de hoy en 5 días"  # 10 de marzo de 2025
# test = "de este martes en 2 semanas"  # 18 de marzo de 2025
# test = "del lunes en 3 meses"  # 2 de junio de 2025
# test = "el martes de la próxima semana"  # 11 de marzo de 2025
# test = "el viernes de la proxima semana"  # 14 de marzo de 2025
# test = "el domingo de la próxima semana"  # 16 de marzo de 2025
# test = "el próximo lunes"  # 10 de marzo de 2025
# test = "este viernes"  # 6 de marzo de 2025
# test = "el próximo sábado"  # 9 de marzo de 2025
# test = "dentro de 3 días"  # 8 de marzo de 2025
# test = "en 2 semanas"  # 19 de marzo de 2025
# test = "dentro de 1 mes"  # 5 de abril de 2025
# test = "hoy"  # 5 de marzo de 2025
# test = "mañana"  # 6 de marzo de 2025
# test = "pasado mañana"  # 7 de marzo de 2025

parse_task(test, "es")
