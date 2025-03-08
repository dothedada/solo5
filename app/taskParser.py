import calendar
import re
import time
import random
from datetime import date

from config import Defaults
from regexGenerator import GetRegex
from task import Task


class Parser:
    def __init__(self, lang):
        self._lang = lang
        self._parser = GetRegex.of(lang)

    # Compares the string with the regex source to get the object or the index
    def _matcher(func):
        def wrapper(self, string, regex_src):
            for i, pattern in enumerate(self._parser["regex_for"][regex_src]):
                match = re.search(pattern, string)
                if match:
                    return func(self, match=match, match_index=i)

            return func(self, match=None, match_index=-1)

        return wrapper

    @_matcher
    def _match_bool(self, match, match_index):
        return True if match else False

    @_matcher
    def _match_ind(self, match, match_index):
        return match_index

    @_matcher
    def _match_dict(self, match, match_index):
        return match.group() if match else None

    @_matcher
    def _match_date(self, match, match_index):
        if match is None:
            return None

        date_info = match.groupdict()
        base_date = self._get_date(date_info)

        if date_info.get("date"):
            return base_date

        add_days, add_monts, add_years = self._get_date_modifier(date_info)

        year, month, day = Parser.normalize_date(
            base_date.year + add_years,
            base_date.month + add_monts,
            base_date.day + add_days,
        )
        return date(year, month, day)

    def _get_next_weekday(self, name):
        return (self._match_ind(name, "week") - date.today().weekday()) % 7

    def _get_month(self, data_dict):
        if month_num := data_dict.get("month_num"):
            return int(month_num)
        elif month_name := data_dict.get("month_name"):
            return self._match_ind(month_name, "months") + 1

        return date.today().month

    def _get_date(self, data_dict):
        if data_dict.get("from") is None:
            return date.today()

        b_day = date.today().day
        if today_rel := data_dict.get("today_rel"):
            b_day += self._match_ind(today_rel, "today_rel")
        elif weekday := data_dict.get("weekday"):
            b_day += self._get_next_weekday(weekday)
        elif day_str := data_dict.get("day_str"):
            b_day = self._match_ind(day_str, "enumeration_str")
        elif (day := data_dict.get("day")) and day.isnumeric():
            b_day = int(day)
        else:
            print("Cannot parse the day setted")

        b_month = self._get_month(data_dict)
        b_year = data_dict.get("year", date.today().year)

        year, month, day = Parser.normalize_date(b_year, b_month, b_day)

        if date(year, month, day) < date.today():
            year += 1

        return date(year, month, day)

    def _get_date_modifier(self, data_dict):
        if data_dict.get("modifier") is None:
            return 0, 0, 0

        amount = 0
        if parsed_amount := data_dict.get("amount", None):
            if parsed_amount.isnumeric():
                amount = int(parsed_amount)
            else:
                amount += self._match_ind(parsed_amount, "amount_str")

        def add_amount(unit):
            return amount if data_dict.get(unit) is not None else 0

        days = add_amount("unit_day")
        days += add_amount("unit_week") * 7
        months = add_amount("unit_month")
        years = add_amount("unit_year")

        return days, months, years

    def _get_dificulty(self, task_raw):
        if (parsed_diff := self._match_ind(task_raw, "dificulty")) > 0:
            return parsed_diff

        if parsed_diff == -1:
            return Defaults.BASE_DIF.value

        dificulty_l = re.search(self._parser["globals"]["dificulty"], task_raw)
        return int(dificulty_l.group()[1:])

    @staticmethod
    def make_id_for(string):
        char_sum = sum(ord(char) for char in string)
        timestamp = int(time.time() * 1000)
        salt = random.randint(1, 9999)
        base_id = (char_sum * timestamp * salt) % (2**64)

        return hex(base_id)[2:]

    @staticmethod
    def sanitize_text(string, is_csv):
        string = string.strip()
        string = re.sub(r"\s+", " ", string)

        if is_csv:
            string = string.replace('"', '""')
            return f'"{string}"'

        return string

    @staticmethod
    def normalize_date(year, month, day):
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

    def make_task(self, string):
        tasks = []

        for i, task_raw in enumerate(string.split(Defaults.TASK_SPLIT.value)):
            if task_raw.strip() == "":
                continue

            task = Task(
                {
                    "lang": self._lang,
                    "id": Parser.make_id_for(task_raw),
                    "task": Parser.sanitize_text(task_raw, False),
                    "task_csv": Parser.sanitize_text(task_raw, True),
                    "done": False,
                    "creation_date": date.today(),
                    "project": self._match_dict(task_raw, "project"),
                    "important": self._match_bool(task_raw, "important"),
                    "dificulty": self._get_dificulty(task_raw),
                    "due_date": self._match_date(task_raw, "dates"),
                }
            )
            tasks.append(task)

        return tasks


# test = 'el próximo viernes // el diez de mayo * difícil "caigo" a @jalizco'
# parser_es = Parser("es")
# tasks = parser_es.make_task(test)
# print(tasks)
# tasks[0].mark_done()
# print(tasks[0])
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

# parse_task(test, "es")
#
