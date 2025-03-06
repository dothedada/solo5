import calendar
from config import Defaults
import re
import time
import random
from regexGenerator import GetRegex
from task import Task
from datetime import date


class Parser:
    def __init__(self, lang):
        self.lang = lang
        self.parser = GetRegex.of(lang)

    def matcher(func):
        def wrapper(self, string, regex_src):
            for i, pattern in enumerate(self.parser["regex_for"][regex_src]):
                match = re.search(pattern, string)
                if match:
                    return func(self, match=match, match_index=i)

            return func(self, match=None, match_index=-1)

        return wrapper

    @matcher
    def get_match_bool(self, match, match_index):
        return True if match else False

    @matcher
    def get_match_ind(self, match, match_index):
        return match_index

    @matcher
    def get_match(self, match, match_index):
        return match.group() if match else None

    @matcher
    def get_match_date(self, match, match_index):
        if match is None:
            return None

        date_info = match.groupdict()
        base_date = self.get_date(date_info)

        if date_info.get("date"):
            return base_date

        add_days, add_monts, add_years = self.get_date_modifier(date_info)

        year, month, day = self.date_normalizer(
            base_date.year + add_years,
            base_date.month + add_monts,
            base_date.day + add_days,
        )
        return date(year, month, day)

    @staticmethod
    def id_maker(string):
        char_sum = sum(ord(char) for char in string)
        timestamp = int(time.time() * 1000)
        salt = random.randint(1, 9999)
        base_id = (char_sum * timestamp * salt) % (2**64)

        return hex(base_id)[2:]

    @staticmethod
    def sanitize_task(string, csv):
        string = string.strip()
        string = re.sub(r"\s+", " ", string)

        if csv:
            string = string.replace('"', '""')
            return f'"{string}"'

        return string

    def get_task(self, string):
        tasks = []

        for i, task_raw in enumerate(string.split(Defaults.TASK_SPLIT.value)):
            task = Task(
                {
                    "lang": self.lang,
                    "id": self.id_maker(task_raw),
                    "task": self.sanitize_task(task_raw, False),
                    "task_csv": self.sanitize_task(task_raw, True),
                    "creation_date": date.today(),
                    "project": self.get_match(task_raw, "project"),
                    "important": self.get_match_bool(task_raw, "important"),
                    "dificulty": self.get_match_ind(task_raw, "dificulty"),
                    "due_date": self.get_match_date(task_raw, "dates"),
                    "parent": tasks[i - 1].id if tasks else None,
                }
            )
            tasks.append(task)

        return tasks

    def get_weekday_days(self, name):
        return (self.get_match_ind(name, "week") - date.today().weekday()) % 7

    def get_month(self, data_dict):
        month_num = data_dict.get("month_num")
        month_name = data_dict.get("month_name")

        if month_num:
            return int(month_num)
        elif month_name:
            return self.get_match_ind(month_name, self.parser, "months") + 1

        return date.today().month

    def date_normalizer(self, year, month, day):
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

    def get_date(self, data_dict):
        if data_dict.get("from") is None:
            return date.today()

        today_rel = data_dict.get("today_rel")
        if today_rel:
            day_offset = self.get_match_ind(today_rel, "today_rel")
            b_day = date.today().day + day_offset
        elif data_dict.get("weekday"):
            weekday = self.get_weekday_days(data_dict.get("weekday"))
            b_day = date.today().day + weekday
        elif data_dict.get("day").isnumeric():
            b_day = int(data_dict.get("day"))
        else:
            print("Cannot parse the day setted")
            b_day = 1

        b_month = self.get_month(data_dict)
        b_year = data_dict.get("year", date.today().year)

        year, month, day = self.date_normalizer(b_year, b_month, b_day)

        if date(year, month, day) < date.today():
            year += 1

        return date(year, month, day)

    def get_date_modifier(self, data_dict):
        if data_dict.get("modifier") is None:
            return 0, 0, 0

        parsed_amount = data_dict.get("amount", None)
        amount = 0

        if parsed_amount:
            if parsed_amount.isnumeric():
                amount = int(parsed_amount)
            else:
                # NOTE: lista correspondiente a cantidad? proxima, un, una...?
                amount += 1

        def add_amount(unit):
            return amount if data_dict.get(unit) is not None else 0

        days = add_amount("unit_day")
        days += add_amount("unit_week") * 7
        months = add_amount("unit_month")
        years = add_amount("unit_year")

        return days, months, years


test = ' de este martes * "caigo" a @jalizco'
parser_es = Parser("es")
print(parser_es.get_task(test))
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
