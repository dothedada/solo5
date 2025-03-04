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


@matcher
def parse_due_date(match, match_index):
    if match is None:
        return None

    data = dict(match.groupdict())
    print(data)

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

"""
    (- from -)  (- modifier -)
    end         -> fecha absoluta sin calulos adicionales
    from        -> de, este, de este, el
    day         -> numero del día de calendario
    weekday     -> nombre del día de la semana("lunes", "martes", ...)
    month_num   -> numero del mes en el calendario
    month_name  -> nombre del mes en el calendario
    year        -> año (opcional, asume actual/siguiente)
    name_base   -> hoy, mañana, pasado mañana

                modifier    -> de, de este, dentro de, próximo, siguiente
                amount      -> cantidad numérica para incremento/decremento
                unit        -> unidad de tiempo (día, semana, mes, año)

    estructura del tiempo:
    dia
    semana (7 días)
    mes

    "(?P<day_num>[0-9]{1,2})(?:\\/(?P<month_num>[0-9]{1,2})| de (?P<month_name>{months}))",
    "(?:de este (?P<day_start_absolute>{week})) en (?P<addition>\\d+) d[ií]as?",
    "(?:el |este |(?P<add_week>pr[oó]ximo) )(?P<day_end_absolute>{week})",
    "(?:dentro de |en )(?P<addition>\\d+) d[ií]as?"
"""
